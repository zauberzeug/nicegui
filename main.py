from copy import deepcopy
import redis
import time
from nicegui import app, ui
from dotenv import load_dotenv

load_dotenv()

app.storage.general['counter'] = 0


def get_redis_client_info(host='localhost', port=6379, password=None, db=0):
    try:
        # Create Redis connection
        r = redis.Redis(host=host, port=port, password=password, db=db, decode_responses=True)
        # Get client info
        info = r.info('clients')
        return {
            'connected_clients': int(info.get('connected_clients', 0)),
            'pubsub_clients': int(info.get('pubsub_clients', 0))
        }
    except redis.RedisError as e:
        print(f'Redis error: {e}')
        return None
    except Exception as e:
        print(f'Error: {e}')
        return None


@app.get('/api')
def some_json():
    # use this api endpoint to confirm that NICEGUI_STORAGE_USER_IGNORE_URI_PREFIXES is working as intended
    print('---------------  START API CALL ---------------  ')
    counter_before = app.storage.general['counter']
    if app.storage.general['counter'] % 2 == 0:
        if app.storage.user:
            app.storage.user['counter'] = int(deepcopy(app.storage.general['counter']))
    app.storage.general['counter'] += 1
    counter_after = deepcopy(app.storage.general['counter'])
    clients = get_redis_client_info()
    ret = {
        'client_count': clients,
        'counter_before': counter_before,
        'counter_after': counter_after
    }
    return ret


@app.get('/other')
def some_json():
    # use this api endpoint to confirm the NICEGUI_STORAGE_USER_IGNORE_URI_PREFIXES is not interfering
    print('------------------------------  ')
    counter_before = app.storage.general['counter']
    if app.storage.general['counter'] % 2 == 0:
        app.storage.user['counter'] = int(deepcopy(app.storage.general['counter']))
    app.storage.general['counter'] += 1
    counter_after = deepcopy(app.storage.general['counter'])
    clients = get_redis_client_info()
    ret = {
        'client_count': clients,
        'counter_before': counter_before,
        'counter_after': counter_after
    }
    return ret


@ui.page('/')
async def root_page():
    # use this page to check that app.storage.user behaves as expected '
    ui.label('root page')
    if not app.storage.user.get('root_page_counter'):
        app.storage.user['root_page_counter'] = 1
    else:
        app.storage.user['root_page_counter'] += 1
    ui.label(f"You have visited {app.storage.user['root_page_counter']} times")


@ui.page('/api/hello')
async def api_hello_page():
    # use this page to that app.storage.user changes are not published to redis
    # check redis before going back to /
    ui.label('api hello page')
    if not app.storage.user.get('root_page_counter'):
        app.storage.user['root_page_counter'] = 1
    else:
        app.storage.user['root_page_counter'] += 1
    ui.label(f"You have visited {app.storage.user['root_page_counter']} times")


ui.run(storage_secret='my_secret')
