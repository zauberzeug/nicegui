import hashlib
import mimetypes
from datetime import datetime
from pathlib import Path
from typing import Generator

from fastapi import Request
from fastapi.responses import Response, StreamingResponse

mimetypes.init()


def get_range_response(file: Path, request: Request, chunk_size: int) -> Response:
    """Get a Response for the given file, supporting range-requests, E-Tag and Last-Modified."""
    file_size = file.stat().st_size
    last_modified_time = datetime.utcfromtimestamp(file.stat().st_mtime)
    start = 0
    end = file_size - 1
    status_code = 200
    e_tag = hashlib.md5((str(last_modified_time) + str(file_size)).encode()).hexdigest()
    if_match_header = request.headers.get('If-None-Match')
    if if_match_header and if_match_header == e_tag:
        return Response(status_code=304)  # Not Modified
    headers = {
        'E-Tag': e_tag,
        'Last-Modified': last_modified_time.strftime(r'%a, %d %b %Y %H:%M:%S GMT'),
    }
    range_header = request.headers.get('range')
    media_type = mimetypes.guess_type(str(file))[0] or 'application/octet-stream'
    if range_header is not None:
        byte1, byte2 = range_header.split('=')[1].split('-')
        start = int(byte1)
        if byte2:
            end = int(byte2)
        status_code = 206  # Partial Content
    content_length = end - start + 1
    headers.update({
        'Content-Length': str(content_length),
        'Content-Range': f'bytes {start}-{end}/{file_size}',
        'Accept-Ranges': 'bytes',
    })

    def content_reader(file: Path, start: int, end: int) -> Generator[bytes, None, None]:
        with open(file, 'rb') as data:
            data.seek(start)
            remaining_bytes = end - start + 1
            while remaining_bytes > 0:
                chunk = data.read(min(chunk_size, remaining_bytes))
                if not chunk:
                    break
                yield chunk
                remaining_bytes -= len(chunk)
    return StreamingResponse(
        content_reader(file, start, end),
        media_type=media_type,
        headers=headers,
        status_code=status_code,
    )
