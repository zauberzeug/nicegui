from typing import Dict

from .language import Language

translations: Dict[Language, Dict[str, str]] = {
    'de': {
        'connection_lost': 'Verbindung verloren',
        'trying_to_reconnect': 'Versuche erneut zu verbinden...'
    },
    'de-CH': {
        'connection_lost': 'Verbindung verloren',
        'trying_to_reconnect': 'Versuche erneut zu verbinden...'
    },
    'de-DE': {
        'connection_lost': 'Verbindung verloren',
        'trying_to_reconnect': 'Versuche erneut zu verbinden...'
    },
    'en-GB': {
        'connection_lost': 'Connection lost.',
        'trying_to_reconnect': 'Trying to reconnect...'
    },
    'en-US': {
        'connection_lost': 'Connection lost.',
        'trying_to_reconnect': 'Trying to reconnect...'
    },
    'es': {
        'connection_lost': 'Conexión perdida',
        'trying_to_reconnect': 'Intentando reconectar...'
    },
    'fr': {
        'connection_lost': 'Connexion perdue',
        'trying_to_reconnect': 'Tentative de reconnexion...'
    },
    'it': {
        'connection_lost': 'Connessione persa',
        'trying_to_reconnect': 'Tentativo di riconnessione...'
    },
    'ja': {
        'connection_lost': '接続が切断されました',
        'trying_to_reconnect': '再接続を試みています...'
    },
    'ko-KR': {
        'connection_lost': '연결이 끊어졌습니다',
        'trying_to_reconnect': '다시 연결하는 중...'
    },
    'ru': {
        'connection_lost': 'Соединение потеряно',
        'trying_to_reconnect': 'Попытка переподключения...'
    },
    'zh-CN': {
        'connection_lost': '连接丢失',
        'trying_to_reconnect': '正在尝试重新连接...'
    },
    'zh-TW': {
        'connection_lost': '連線丟失',
        'trying_to_reconnect': '正在嘗試重新連線...'
    },
}
