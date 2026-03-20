import httpx

from nicegui import app, binding, logging


@binding.bindable_dataclass
class GitHubStars:
    count: int = 0
    short_string: str = '0'
    long_string: str = '0'


stars = GitHubStars()


async def _fetch() -> None:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get('https://api.github.com/repos/zauberzeug/nicegui', timeout=10)
            response.raise_for_status()
            stars.count = response.json()['stargazers_count']
            stars.short_string = f'{stars.count // 1000}k+'
            stars.long_string = f'\u2605 {(stars.count // 1000) * 1000:,}+ GitHub stars'
    except Exception:
        logging.log.warning('failed to fetch GitHub star count')


app.timer(3600, _fetch)
