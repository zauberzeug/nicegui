import sys
from datetime import datetime

from nicegui import ui
from nicegui.client import Client
from nicegui.testing import User
from nicegui.testing.user_simulation import user_simulation


async def test_diagnostics_endpoint_returns_json_when_enabled() -> None:
    async with user_simulation(diagnostics=True) as user:
        @ui.page('/')
        def index():
            ui.label('Hello')

        await user.open('/')
        response = await user.http_client.get('/_nicegui/diagnostics')
        assert response.status_code == 200
        data = response.json()
        assert 'server' in data
        assert 'client' in data
        datetime.fromisoformat(data['timestamp'])


async def test_diagnostics_endpoint_returns_404_when_disabled(user: User) -> None:
    @ui.page('/')
    def index():
        ui.label('Hello')

    await user.open('/')
    response = await user.http_client.get('/_nicegui/diagnostics')
    assert response.status_code == 404


async def test_task_summary_grouped_by_coroutine() -> None:
    async with user_simulation(diagnostics=True) as user:
        @ui.page('/')
        def index():
            ui.label('Hello')

        await user.open('/')
        response = await user.http_client.get('/_nicegui/diagnostics')
        assert response.status_code == 200
        data = response.json()
        tasks = data['server']['asyncio_tasks']
        assert isinstance(tasks['total'], int)
        assert tasks['total'] > 0
        assert isinstance(tasks['by_coroutine'], dict)
        assert len(tasks['by_coroutine']) > 0
        for key in tasks['by_coroutine']:
            assert isinstance(key, str)


async def test_coroutine_groups_include_count_and_names() -> None:
    async with user_simulation(diagnostics=True) as user:
        @ui.page('/')
        def index():
            ui.label('Hello')

        await user.open('/')
        response = await user.http_client.get('/_nicegui/diagnostics')
        assert response.status_code == 200
        data = response.json()['server']['asyncio_tasks']
        for group in data['by_coroutine'].values():
            assert isinstance(group['count'], int)
            assert group['count'] > 0
            assert isinstance(group['names'], list)
            assert len(group['names']) == group['count']
            for name in group['names']:
                assert isinstance(name, str)


async def test_memory_metrics_with_source_labels() -> None:
    async with user_simulation(diagnostics=True) as user:
        @ui.page('/')
        def index():
            ui.label('Hello')

        await user.open('/')
        response = await user.http_client.get('/_nicegui/diagnostics')
        assert response.status_code == 200
        memory = response.json()['server']['memory']
        assert isinstance(memory['peak_rss_source'], str)
        assert len(memory['peak_rss_source']) > 0
        assert isinstance(memory['current_rss_source'], str)
        assert len(memory['current_rss_source']) > 0
        if sys.platform == 'linux':
            assert isinstance(memory['peak_rss_bytes'], int)
            assert memory['peak_rss_bytes'] > 0
            assert isinstance(memory['current_rss_bytes'], int)
            assert memory['current_rss_bytes'] > 0


async def test_per_client_detail_with_valid_client_id() -> None:
    async with user_simulation(diagnostics=True) as user:
        @ui.page('/')
        def index():
            ui.label('Hello')

        await user.open('/')
        client_id = next(iter(Client.instances))
        response = await user.http_client.get(f'/_nicegui/diagnostics?client_id={client_id}')
        assert response.status_code == 200
        client_data = response.json()['client']
        assert client_data is not None
        assert client_data['id'] == client_id
        assert isinstance(client_data['elements'], int)
        assert isinstance(client_data['outbox_pending_updates'], int)
        assert isinstance(client_data['outbox_pending_messages'], int)
        assert isinstance(client_data['has_socket_connection'], bool)


async def test_invalid_client_id_returns_null_with_error() -> None:
    async with user_simulation(diagnostics=True) as user:
        @ui.page('/')
        def index():
            ui.label('Hello')

        await user.open('/')
        response = await user.http_client.get('/_nicegui/diagnostics?client_id=nonexistent')
        assert response.status_code == 200
        data = response.json()
        assert data['client'] is None
        assert data['client_error'] == 'not found'
        assert 'server' in data


async def test_server_config_includes_event_handling_settings() -> None:
    async with user_simulation(diagnostics=True) as user:
        @ui.page('/')
        def index():
            ui.label('Hello')

        await user.open('/')
        response = await user.http_client.get('/_nicegui/diagnostics')
        assert response.status_code == 200
        config = response.json()['server']['config']
        assert isinstance(config['async_handlers'], bool)
        assert isinstance(config['reconnect_timeout'], (int, float))
        assert isinstance(config['binding_refresh_interval'], (int, float, type(None)))
        assert isinstance(config['transports'], list)
        assert len(config['transports']) > 0


async def test_diagnostics_view_renders_log_and_refresh_button(user: User) -> None:
    @ui.page('/')
    def index():
        ui.diagnostics_view()

    await user.open('/')
    await user.should_see('Refresh')


async def test_diagnostics_view_append_mode_preserves_history(user: User) -> None:
    @ui.page('/')
    def index():
        ui.diagnostics_view()

    await user.open('/')
    user.find(ui.button).click()
    first_separators = len(user.find(content='---').elements)
    user.find(ui.button).click()
    second_separators = len(user.find(content='---').elements)
    assert second_separators > first_separators


async def test_diagnostics_view_replace_mode_clears_log(user: User) -> None:
    @ui.page('/')
    def index():
        ui.diagnostics_view(mode='replace')

    await user.open('/')
    user.find(ui.button).click()
    first_separators = len(user.find(content='---').elements)
    assert first_separators > 0
    user.find(ui.button).click()
    assert len(user.find(content='---').elements) == first_separators


async def test_diagnostics_view_client_scope_includes_client_data(user: User) -> None:
    @ui.page('/')
    def index():
        ui.diagnostics_view(scope='client')

    await user.open('/')
    user.find(ui.button).click()
    await user.should_see('Elements:')
    await user.should_see('Connected:')
    await user.should_see('Tasks:')


async def test_diagnostics_view_global_scope_includes_clients_summary(user: User) -> None:
    @ui.page('/')
    def index():
        ui.diagnostics_view(scope='global')

    await user.open('/')
    user.find(ui.button).click()
    await user.should_see('Clients:')
    await user.should_see('Tasks:')


async def test_element_count_reflects_page_content() -> None:
    async with user_simulation(diagnostics=True) as user:
        @ui.page('/')
        def index():
            for _ in range(10):
                ui.label('item')

        await user.open('/')
        client_id = next(iter(Client.instances))
        response = await user.http_client.get(f'/_nicegui/diagnostics?client_id={client_id}')
        assert response.status_code == 200
        elements = response.json()['client']['elements']
        assert elements >= 10, f'expected at least 10 elements from labels, got {elements}'


async def test_diagnostics_view_interval_creates_timer(user: User) -> None:
    @ui.page('/')
    def index():
        ui.diagnostics_view(interval=10)

    await user.open('/')
    timers = [t for t in user.find(ui.timer).elements if t.interval == 10]
    assert len(timers) == 1
    assert timers[0].active
