import asyncio
import hashlib
import mimetypes
import weakref
from collections.abc import AsyncGenerator
from datetime import UTC, datetime
from pathlib import Path
from typing import BinaryIO

from fastapi import Request
from fastapi.responses import Response, StreamingResponse

mimetypes.init()

MIN_CHUNK_SIZE = 1024
MAX_CHUNK_SIZE = 8192


def get_range_response(file: Path, request: Request, chunk_size: int) -> Response:
    """Get a Response for the given file, supporting range-requests, ETag and Last-Modified."""
    chunk_size = max(MIN_CHUNK_SIZE, min(chunk_size, MAX_CHUNK_SIZE))
    file_size = file.stat().st_size
    last_modified_time = datetime.fromtimestamp(file.stat().st_mtime, UTC)
    start = 0
    end = file_size - 1
    status_code = 200
    e_tag = f'"{hashlib.md5((str(last_modified_time) + str(file_size)).encode()).hexdigest()}"'
    headers = {
        'ETag': e_tag,
        'Last-Modified': last_modified_time.strftime(r'%a, %d %b %Y %H:%M:%S GMT'),
    }
    if_none_match = request.headers.get('If-None-Match', '')
    if if_none_match.strip() == '*' or e_tag in [tag.strip().removeprefix('W/') for tag in if_none_match.split(',')]:
        return Response(status_code=304, headers=headers)  # Not Modified
    range_header = request.headers.get('range')
    media_type = mimetypes.guess_type(str(file))[0] or 'application/octet-stream'
    if range_header is not None:
        try:
            unit, _, range_spec = range_header.partition('=')
            if unit.strip().lower() != 'bytes':
                raise ValueError('unsupported range unit')
            byte1, byte2 = range_spec.split('-', 1)
            if byte1 == '':
                # suffix range, e.g. "bytes=-4" is the last 4 bytes (RFC 9110)
                suffix_length = int(byte2)
                start = max(file_size - suffix_length, 0)
                end = file_size - 1
            else:
                start = int(byte1)
                end = int(byte2) if byte2 else file_size - 1
        except (IndexError, ValueError):
            return Response(status_code=416, headers={'Content-Range': f'bytes */{file_size}'})
        if start > end or start >= file_size:
            return Response(status_code=416, headers={'Content-Range': f'bytes */{file_size}'})
        end = min(end, file_size - 1)
        status_code = 206  # Partial Content
    content_length = end - start + 1
    headers.update({
        'Content-Length': str(content_length),
        'Content-Range': f'bytes {start}-{end}/{file_size}',
        'Accept-Ranges': 'bytes',
    })

    async def content_reader(data: BinaryIO, start: int, end: int) -> AsyncGenerator[bytes, None]:
        try:
            data.seek(start)
            remaining_bytes = end - start + 1
            while remaining_bytes > 0:
                chunk = await asyncio.to_thread(data.read, min(chunk_size, remaining_bytes))
                if not chunk:
                    break
                yield chunk
                remaining_bytes -= len(chunk)
        finally:
            data.close()
    data = open(file, 'rb')  # pylint: disable=consider-using-with
    generator = content_reader(data, start, end)
    weakref.finalize(generator, data.close)  # close if the iterator is abandoned without aclose()
    return StreamingResponse(
        generator,
        media_type=media_type,
        headers=headers,
        status_code=status_code,
    )
