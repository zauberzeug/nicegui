import httpx

from nicegui import app, binding, logging


@binding.bindable_dataclass
class GitHubStars:
    string: str = app.storage.general.get('github_stars', '0')


stars = GitHubStars()


async def _fetch() -> None:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get('https://api.github.com/repos/zauberzeug/nicegui', timeout=10)
            response.raise_for_status()
            stars.string = f'{response.json()["stargazers_count"] // 1000}k+'
            app.storage.general.update(github_stars=stars.string)
    except Exception:
        logging.log.warning('failed to fetch GitHub star count')


app.timer(3600, _fetch)
