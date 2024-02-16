import hashlib
import mimetypes
from datetime import datetime
from pathlib import Path
from typing import Generator

from fastapi import Request
from fastapi.responses import Response, StreamingResponse

mimetypes.init()

def get_range_response(file: Path, request: Request, chunk_size: int) -> Response:
    """
    Get a Response for the given file, supporting range-requests, E-Tag and Last-Modified.

    Args:
        - file (Path): The path to the file to be served.
        - request (Request): The HTTP request object.
        - chunk_size (int): The size of each chunk to be read from the file.

    Returns:
        - Response: The HTTP response object.

    Raises:
        - FileNotFoundError: If the file does not exist.
        - PermissionError: If the file cannot be accessed due to insufficient permissions.

    Notes:
        - This function calculates the file size, last modified time, and E-Tag of the file.
        - It checks if the request contains an If-None-Match header and returns a 304 Not Modified response if the E-Tag matches.
        - It sets the E-Tag and Last-Modified headers in the response.
        - If the request contains a range header, it parses the range and sets the appropriate status code and headers.
        - It reads the file in chunks and yields each chunk as a response.
        - The media type of the file is determined using the mimetypes module.
        - The response includes the Content-Length, Content-Range, and Accept-Ranges headers.

    Example:
        >>> from nicegui.app.range_response import get_range_response
        >>> from nicegui.app.request import Request
        >>> from nicegui.app.response import Response
        >>> from pathlib import Path
        >>> file = Path('/path/to/file.txt')
        >>> request = Request(headers={'range': 'bytes=0-100'})
        >>> chunk_size = 1024
        >>> response = get_range_response(file, request, chunk_size)
    """
    file_size = file.stat().st_size
    last_modified_time = datetime.utcfromtimestamp(file.stat().st_mtime)
    start = 0
    end = file_size - 1
    status_code = 200
    e_tag = md5((str(last_modified_time) + str(file_size)).encode()).hexdigest()
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
