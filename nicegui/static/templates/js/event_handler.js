// {% raw %}

var files_chosen = {};

function eventHandler(props, event, form_data, aux) {

    if (props.jp_props.debug) {
        console.log('-------------------------');
        console.log('In eventHandler: ' + event.type + '  ' + props.jp_props.vue_type + '  ' + props.jp_props.class_name);
        console.log(event);
        console.log(props.jp_props);
        console.log('-------------------------');
    }
    if (!websocket_ready && use_websockets) {
        setTimeout(function(){ eventHandler(props, event, form_data, aux); }, 100);
        return;
    }
    let event_type = event.type;
    if (event_type == 'input' && (props.jp_props.vue_type == 'quasar_component') && (props.jp_props.disable_input_event)) {
        comp_dict[props.jp_props.id].value = event.target.value;
        return;
    }
    if (event_type == 'focusin' && (props.jp_props.vue_type == 'quasar_component')) {
        event_type = 'focus';
        event.target.value = comp_dict[props.jp_props.id].value;
    }
    if (event_type == 'focusout' && (props.jp_props.vue_type == 'quasar_component')) {
        event_type = 'blur';
        event.target.value = comp_dict[props.jp_props.id].value;
    }
    e = {
        'event_type': event_type,
        'id': props.jp_props.id,
        'class_name': props.jp_props.class_name,
        'html_tag': props.jp_props.html_tag,
        'vue_type': props.jp_props.vue_type,
        'event_target': event.target.id,
        'input_type': props.jp_props.input_type,
        'checked': event.target.checked,
        'data': event.data,
        'value': event.target.value,
        'page_id': page_id,
        'websocket_id': websocket_id
    };
    if (props.jp_props.additional_properties) {
        for (let i = 0; i < props.jp_props.additional_properties.length; i++) {
            e[props.jp_props.additional_properties[i]] = event[props.jp_props.additional_properties[i]];
        }
    }
    if ((event instanceof Event) && (event.target.type == 'file')) {

        files_chosen[event.target.id] = event.target.files;
        var files = [];
        for (let i = 0; i < event.target.files.length; i++) {
            const fi = event.target.files[i];
            files.push({name: fi.name, size: fi.size, type: fi.type, lastModified: fi.lastModified});
        }
        e['files'] = files;
    }
    if (form_data) {
        e['form_data'] = form_data;
    } else {
        if (event.currentTarget)
            e['event_current_target'] = event.currentTarget.id;
    }
    if (aux) e['aux'] = aux;
    if (event instanceof KeyboardEvent) {
        // https://developer.mozilla.org/en-US/docs/Web/Events/keydown   keyup, keypress
        e['key_data'] = {
            altKey: event.altKey,
            ctrlKey: event.ctrlKey,
            shiftKey: event.shiftKey,
            metaKey: event.metaKey,
            code: event.code,
            key: event.key,
            location: event.location,
            repeat: event.repeat,
            locale: event.locale
        }
    }

    let modifiers = props.jp_props.event_modifiers[event.type];

    if (modifiers && modifiers.debounce) {
        let callNow = modifiers.debounce.immediate && !modifiers.debounce.timeout;
        clearTimeout(modifiers.debounce.timeout);
        let set_e = e;
        modifiers.debounce.timeout = setTimeout(function () {
                modifiers.debounce.timeout = undefined;
                if (!callNow) send_to_server(set_e, 'event', props.jp_props.debug);
            }
            , modifiers.debounce.value);
        if (callNow) send_to_server(set_e, 'event', props.jp_props.debug);

    } else if (modifiers && modifiers.throttle) {
        if (!modifiers.throttle.timeout) {
            let set_e = e;
            modifiers.throttle.timeout = setTimeout(function () {
                    send_to_server(set_e, 'event', props.jp_props.debug);
                    modifiers.throttle.timeout = undefined;
                }
                , modifiers.throttle.value);
        }
    } else if (props.jp_props.debounce && (event.type == 'input')) {
        clearTimeout(props.timeout);
        let set_e = e;
        props.timeout = setTimeout(function () {
                send_to_server(set_e, 'event', props.jp_props.debug);
            }
            , props.jp_props.debounce);
    } else {
        send_to_server(e, 'event', props.jp_props.debug);
    }

    // https://developer.mozilla.org/en-US/docs/Web/API/Element/scrollIntoView
    if (props.jp_props.scroll && (event.type == 'click')) {
        event.preventDefault();
        c = document.getElementById(props.jp_props.scroll_to);

        c.scrollIntoView({
            behavior: props.jp_props.scroll_option,    // Default is 'smooth'
            block: props.jp_props.block_option,
            inline: props.jp_props.inline_option,
        });

    }
}

function send_to_server(e, event_type, debug_flag) {
    if (debug_flag) {
        console.log('Sending message to server:');
        console.log({'type': event_type, 'event_data': e});
    }
    if (use_websockets) {
        if (web_socket_closed) {
            window.location.reload();
            return;
        }
        if (websocket_ready) {
            socket.send(JSON.stringify({'type': event_type, 'event_data': e}));
        } else {
            setTimeout(function () {
                socket.send(JSON.stringify({'type': event_type, 'event_data': e}));
            }, 1000);
        }
    } else {

        d = JSON.stringify({'type': 'event', 'event_data': e});
        $.ajax({
            type: "POST",
            url: "/zzz_justpy_ajax",
            data: JSON.stringify({'type': event_type, 'event_data': e}),
            success: function (msg) {
                if (msg.page_options.redirect) {
                    location.href = msg.page_options.redirect;
                }
                if (msg.page_options.open) {
                    window.open(msg.page_options.open, '_blank');
                }
                if (msg.page_options.display_url !== null)
                    window.history.pushState("", "", msg.page_options.display_url);
                document.title = msg.page_options.title;
                if (msg.page_options.favicon) {
                    var link = document.querySelector("link[rel*='icon']") || document.createElement('link');
                    link.type = 'image/x-icon';
                    link.rel = 'shortcut icon';
                    link.href = '{{ options.static_name + '/' }}' + msg.page_options.favicon;
                    document.getElementsByTagName('head')[0].appendChild(link);
                }
                if (msg) app1.justpyComponents = msg.data;
            },
            dataType: 'json'
        });
    }
}

// {% endraw %}