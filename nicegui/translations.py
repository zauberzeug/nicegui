from .language import Language

translations: dict[Language, dict[str, str]] = {
    'de': {
        'connection_lost': 'Verbindung verloren',
        'trying_to_reconnect': 'Versuche erneut zu verbinden...',
        'message_too_long': 'Nachricht zu lang',
        'message_too_long_body': 'Die Nachricht ist zu groß für die Übertragung via WebSocket.'
    },
    'de-CH': {
        'connection_lost': 'Verbindung verloren',
        'trying_to_reconnect': 'Versuche erneut zu verbinden...',
        'message_too_long': 'Nachricht zu lang',
        'message_too_long_body': 'Die Nachricht ist zu groß für die Übertragung via WebSocket.'
    },
    'de-DE': {
        'connection_lost': 'Verbindung verloren',
        'trying_to_reconnect': 'Versuche erneut zu verbinden...',
        'message_too_long': 'Nachricht zu lang',
        'message_too_long_body': 'Die Nachricht ist zu groß für die Übertragung via WebSocket.'
    },
    'en-GB': {
        'connection_lost': 'Connection lost.',
        'trying_to_reconnect': 'Trying to reconnect...',
        'message_too_long': 'Message too long',
        'message_too_long_body': 'The message is too large for WebSocket transmission.'
    },
    'en-US': {
        'connection_lost': 'Connection lost.',
        'trying_to_reconnect': 'Trying to reconnect...',
        'message_too_long': 'Message too long',
        'message_too_long_body': 'The message is too large for WebSocket transmission.'
    },
    'es': {
        'connection_lost': 'Conexión perdida',
        'trying_to_reconnect': 'Intentando reconectar...',
        'message_too_long': 'Mensaje demasiado largo',
        'message_too_long_body': 'El mensaje excede el límite de tamaño de WebSocket.'
    },
    'fr': {
        'connection_lost': 'Connexion perdue',
        'trying_to_reconnect': 'Tentative de reconnexion...',
        'message_too_long': 'Message trop long',
        'message_too_long_body': 'Le message dépasse la limite de taille WebSocket.'
    },
    'it': {
        'connection_lost': 'Connessione persa',
        'trying_to_reconnect': 'Tentativo di riconnessione...',
        'message_too_long': 'Messaggio troppo lungo',
        'message_too_long_body': 'Il messaggio supera il limite di dimensione WebSocket.'
    },
    'ja': {
        'connection_lost': '接続が切断されました',
        'trying_to_reconnect': '再接続を試みています...',
        'message_too_long': 'メッセージが長すぎます',
        'message_too_long_body': 'メッセージがWebSocketの送信制限を超えています。'
    },
    'ko-KR': {
        'connection_lost': '연결이 끊어졌습니다',
        'trying_to_reconnect': '다시 연결하는 중...',
        'message_too_long': '메시지가 너무 깁니다',
        'message_too_long_body': '메시지가 WebSocket 크기 제한을 초과합니다.'
    },
    'ru': {
        'connection_lost': 'Соединение потеряно',
        'trying_to_reconnect': 'Попытка переподключения...',
        'message_too_long': 'Сообщение слишком длинное',
        'message_too_long_body': 'Сообщение превышает ограничение размера WebSocket.'
    },
    'zh-CN': {
        'connection_lost': '连接丢失',
        'trying_to_reconnect': '正在尝试重新连接...',
        'message_too_long': '消息太长',
        'message_too_long_body': '消息超过WebSocket大小限制。'
    },
    'zh-TW': {
        'connection_lost': '連線丟失',
        'trying_to_reconnect': '正在嘗試重新連線...',
        'message_too_long': '訊息過長',
        'message_too_long_body': '訊息超過WebSocket大小限制。'
    },
}
