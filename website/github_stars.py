import httpx

from nicegui import app, binding, logging


@binding.bindable_dataclass
class GitHubStars:
    string: str = '0'


stars = GitHubStars()


async def _fetch() -> None:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get('https://api.github.com/repos/zauberzeug/nicegui', timeout=10)
            response.raise_for_status()
            stars.string = f'{response.json()["stargazers_count"] // 1000}k+'
    except Exception:
        logging.log.warning('failed to fetch GitHub star count')


app.timer(3600, _fetch)
