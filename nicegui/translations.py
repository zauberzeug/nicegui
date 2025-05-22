from typing import Dict

from .language import Language

translations: Dict[Language, Dict[str, str]] = {
    'de': {
        'server_error': 'Serverfehler',
        'connection_lost': 'Verbindung verloren',
        'trying_to_reconnect': 'Versuche erneut zu verbinden...'
    },
    'de-CH': {
        'server_error': 'Serverfehler',
        'connection_lost': 'Verbindung verloren',
        'trying_to_reconnect': 'Versuche erneut zu verbinden...'
    },
    'de-DE': {
        'server_error': 'Serverfehler',
        'connection_lost': 'Verbindung verloren',
        'trying_to_reconnect': 'Versuche erneut zu verbinden...'
    },
    'en-GB': {
        'server_error': 'Server error',
        'connection_lost': 'Connection lost.',
        'trying_to_reconnect': 'Trying to reconnect...'
    },
    'en-US': {
        'server_error': 'Server error',
        'connection_lost': 'Connection lost.',
        'trying_to_reconnect': 'Trying to reconnect...'
    },
    'es': {
        'server_error': 'Error del servidor',
        'connection_lost': 'Conexión perdida',
        'trying_to_reconnect': 'Intentando reconectar...'
    },
    'fr': {
        'server_error': 'Erreur du serveur',
        'connection_lost': 'Connexion perdue',
        'trying_to_reconnect': 'Tentative de reconnexion...'
    },
    'it': {
        'server_error': 'Errore del server',
        'connection_lost': 'Connessione persa',
        'trying_to_reconnect': 'Tentativo di riconnessione...'
    },
    'ja': {
        'server_error': 'サーバーエラー',
        'connection_lost': '接続が切断されました',
        'trying_to_reconnect': '再接続を試みています...'
    },
    'ko-KR': {
        'server_error': '서버 오류',
        'connection_lost': '연결이 끊어졌습니다',
        'trying_to_reconnect': '다시 연결하는 중...'
    },
    'ru': {
        'server_error': 'Ошибка сервера',
        'connection_lost': 'Соединение потеряно',
        'trying_to_reconnect': 'Попытка переподключения...'
    },
    'zh-CN': {
        'server_error': '服务器错误',
        'connection_lost': '连接丢失',
        'trying_to_reconnect': '正在尝试重新连接...'
    },
    'zh-TW': {
        'server_error': '伺服器錯誤',
        'connection_lost': '連線丟失',
        'trying_to_reconnect': '正在嘗試重新連線...'
    },
}
