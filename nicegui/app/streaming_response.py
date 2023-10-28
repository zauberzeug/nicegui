import mimetypes
from pathlib import Path
from typing import Generator

from fastapi import Request
from fastapi.responses import StreamingResponse

mimetypes.init()


def get_streaming_response(file: Path, request: Request) -> StreamingResponse:
    """Get a StreamingResponse for the given file and request."""
    file_size = file.stat().st_size
    start = 0
    end = file_size - 1
    range_header = request.headers.get('Range')
    if range_header:
        byte1, byte2 = range_header.split('=')[1].split('-')
        start = int(byte1)
        if byte2:
            end = int(byte2)
    content_length = end - start + 1
    headers = {
        'Content-Range': f'bytes {start}-{end}/{file_size}',
        'Content-Length': str(content_length),
        'Accept-Ranges': 'bytes',
    }

    def content_reader(file: Path, start: int, end: int, chunk_size: int = 8192) -> Generator[bytes, None, None]:
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
        media_type=mimetypes.guess_type(str(file))[0] or 'application/octet-stream',
        headers=headers,
        status_code=206,
    )
