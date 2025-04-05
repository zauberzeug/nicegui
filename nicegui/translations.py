from typing import Dict

from .language import Language

translations: Dict[Language, Dict[str, str]] = {
    'de': {
        'connection_lost': 'Verbindung verloren',
        'trying_to_reconnect': 'Versuche erneut zu verbinden...',
        'message_too_long': 'Nachricht zu lang',
        'message_too_long_body': 'Die Nachricht ist länger als der Server verarbeiten kann.'
    },
    'de-CH': {
        'connection_lost': 'Verbindung verloren',
        'trying_to_reconnect': 'Versuche erneut zu verbinden...',
        'message_too_long': 'Nachricht zu lang',
        'message_too_long_body': 'Die Nachricht ist länger als der Server verarbeiten kann.'
    },
    'de-DE': {
        'connection_lost': 'Verbindung verloren',
        'trying_to_reconnect': 'Versuche erneut zu verbinden...',
        'message_too_long': 'Nachricht zu lang',
        'message_too_long_body': 'Die Nachricht ist länger als der Server verarbeiten kann.'
    },
    'en-GB': {
        'connection_lost': 'Connection lost.',
        'trying_to_reconnect': 'Trying to reconnect...',
        'message_too_long': 'Message too long',
        'message_too_long_body': 'The message is longer than what the server can handle.'
    },
    'en-US': {
        'connection_lost': 'Connection lost.',
        'trying_to_reconnect': 'Trying to reconnect...',
        'message_too_long': 'Message too long',
        'message_too_long_body': 'The message is longer than what the server can handle.'
    },
    'es': {
        'connection_lost': 'Conexión perdida',
        'trying_to_reconnect': 'Intentando reconectar...',
        'message_too_long': 'Mensaje demasiado largo',
        'message_too_long_body': 'El mensaje es más largo de lo que el servidor puede manejar.'
    },
    'fr': {
        'connection_lost': 'Connexion perdue',
        'trying_to_reconnect': 'Tentative de reconnexion...',
        'message_too_long': 'Message trop long',
        'message_too_long_body': 'Le message est plus long que ce que le serveur peut gérer.'
    },
    'it': {
        'connection_lost': 'Connessione persa',
        'trying_to_reconnect': 'Tentativo di riconnessione...',
        'message_too_long': 'Messaggio troppo lungo',
        'message_too_long_body': 'Il messaggio è più lungo di quanto il server possa gestire.'
    },
    'ja': {
        'connection_lost': '接続が切断されました',
        'trying_to_reconnect': '再接続を試みています...',
        'message_too_long': 'メッセージが長すぎます',
        'message_too_long_body': 'メッセージはサーバーが処理できるよりも長くなっています。'
    },
    'ko-KR': {
        'connection_lost': '연결이 끊어졌습니다',
        'trying_to_reconnect': '다시 연결하는 중...',
        'message_too_long': '메시지가 너무 깁니다',
        'message_too_long_body': '메시지가 서버에서 처리할 수 있는 것보다 깁니다.'
    },
    'ru': {
        'connection_lost': 'Соединение потеряно',
        'trying_to_reconnect': 'Попытка переподключения...',
        'message_too_long': 'Сообщение слишком длинное',
        'message_too_long_body': 'Сообщение длиннее, чем может обработать сервер.'
    },
    'zh-CN': {
        'connection_lost': '连接丢失',
        'trying_to_reconnect': '正在尝试重新连接...',
        'message_too_long': '消息太长',
        'message_too_long_body': '消息长度超过服务器的处理能力。'
    },
    'zh-TW': {
        'connection_lost': '連線丟失',
        'trying_to_reconnect': '正在嘗試重新連線...',
        'message_too_long': '訊息過長',
        'message_too_long_body': '訊息超過伺服器能處理的長度。'
    },
}
