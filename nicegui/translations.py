from .language import Language

translations: dict[Language, dict[str, str]] = {
    'de': {
        'connection_lost': 'Verbindung verloren',
        'trying_to_reconnect': 'Versuche erneut zu verbinden...',
        'message_too_long': 'Nachricht zu lang',
        'message_too_long_body': 'Die Nachricht ist zu groß für die Übertragung via WebSocket.',
        'element_listener_changed': 'Element-Listener geändert',
        're_rendering_element': 'Element wird neu gerendert...'
    },
    'de-CH': {
        'connection_lost': 'Verbindung verloren',
        'trying_to_reconnect': 'Versuche erneut zu verbinden...',
        'message_too_long': 'Nachricht zu lang',
        'message_too_long_body': 'Die Nachricht ist zu groß für die Übertragung via WebSocket.',
        'element_listener_changed': 'Element-Listener geändert',
        're_rendering_element': 'Element wird neu gerendert...'
    },
    'de-DE': {
        'connection_lost': 'Verbindung verloren',
        'trying_to_reconnect': 'Versuche erneut zu verbinden...',
        'message_too_long': 'Nachricht zu lang',
        'message_too_long_body': 'Die Nachricht ist zu groß für die Übertragung via WebSocket.',
        'element_listener_changed': 'Element-Listener geändert',
        're_rendering_element': 'Element wird neu gerendert...'
    },
    'en-GB': {
        'connection_lost': 'Connection lost.',
        'trying_to_reconnect': 'Trying to reconnect...',
        'message_too_long': 'Message too long',
        'message_too_long_body': 'The message is too large for WebSocket transmission.',
        'element_listener_changed': 'Element listener changed',
        're_rendering_element': 'Re-rendering element...'
    },
    'en-US': {
        'connection_lost': 'Connection lost.',
        'trying_to_reconnect': 'Trying to reconnect...',
        'message_too_long': 'Message too long',
        'message_too_long_body': 'The message is too large for WebSocket transmission.',
        'element_listener_changed': 'Element listener changed',
        're_rendering_element': 'Re-rendering element...'
    },
    'es': {
        'connection_lost': 'Conexión perdida',
        'trying_to_reconnect': 'Intentando reconectar...',
        'message_too_long': 'Mensaje demasiado largo',
        'message_too_long_body': 'El mensaje excede el límite de tamaño de WebSocket.',
        'element_listener_changed': 'El oyente del elemento ha cambiado',
        're_rendering_element': 'Volviendo a renderizar el elemento...'
    },
    'fr': {
        'connection_lost': 'Connexion perdue',
        'trying_to_reconnect': 'Tentative de reconnexion...',
        'message_too_long': 'Message trop long',
        'message_too_long_body': 'Le message dépasse la limite de taille WebSocket.',
        'element_listener_changed': "L'écouteur d'élément a changé",
        're_rendering_element': "Rendu de l'élément en cours..."
    },
    'it': {
        'connection_lost': 'Connessione persa',
        'trying_to_reconnect': 'Tentativo di riconnessione...',
        'message_too_long': 'Messaggio troppo lungo',
        'message_too_long_body': 'Il messaggio supera il limite di dimensione WebSocket.',
        'element_listener_changed': "Il listener dell'elemento è cambiato",
        're_rendering_element': "Rendere di nuovo l'elemento..."
    },
    'ja': {
        'connection_lost': '接続が切断されました',
        'trying_to_reconnect': '再接続を試みています...',
        'message_too_long': 'メッセージが長すぎます',
        'message_too_long_body': 'メッセージがWebSocketの送信制限を超えています。',
        'element_listener_changed': '要素リスナーが変更されました',
        're_rendering_element': '要素を再レンダリングしています...'
    },
    'ko-KR': {
        'connection_lost': '연결이 끊어졌습니다',
        'trying_to_reconnect': '다시 연결하는 중...',
        'message_too_long': '메시지가 너무 깁니다',
        'message_too_long_body': '메시지가 WebSocket 크기 제한을 초과합니다.',
        'element_listener_changed': '요소 리스너가 변경되었습니다',
        're_rendering_element': '요소를 다시 렌더링하는 중...'
    },
    'ru': {
        'connection_lost': 'Соединение потеряно',
        'trying_to_reconnect': 'Попытка переподключения...',
        'message_too_long': 'Сообщение слишком длинное',
        'message_too_long_body': 'Сообщение превышает ограничение размера WebSocket.',
        'element_listener_changed': 'Слушатель элемента изменен',
        're_rendering_element': 'Повторный рендеринг элемента...'
    },
    'zh-CN': {
        'connection_lost': '连接丢失',
        'trying_to_reconnect': '正在尝试重新连接...',
        'message_too_long': '消息太长',
        'message_too_long_body': '消息超过WebSocket大小限制。',
        'element_listener_changed': '元素监听器已更改',
        're_rendering_element': '正在重新渲染元素...'
    },
    'zh-TW': {
        'connection_lost': '連線丟失',
        'trying_to_reconnect': '正在嘗試重新連線...',
        'message_too_long': '訊息過長',
        'message_too_long_body': '訊息超過WebSocket大小限制。',
        'element_listener_changed': '元素監聽器已更改',
        're_rendering_element': '正在重新渲染元素...'
    },
}
