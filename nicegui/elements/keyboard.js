Vue.component('keyboard', {
	template: `<span v-bind:id="jp_props.id" :class="jp_props.classes" :style="jp_props.style"></span>`,
	methods: {
		add_event_listeners() {
			const props = this.$props;
			const activeJSEvents = this.$props.jp_props.options.activeJSEvents;
			for (let i in activeJSEvents) {
				const event = activeJSEvents[i];
				document.addEventListener(event, function (evt) {
					const e = {
						event_type: 'keyboardEvent',
						id: props.jp_props.id,
						page_id: page_id,
						websocket_id: websocket_id
					};
					if (evt instanceof KeyboardEvent) {
						// https://developer.mozilla.org/en-US/docs/Web/Events/keydown   keyup, keypress
						e['key_data'] = {
							action: event,
							altKey: evt.altKey,
							ctrlKey: evt.ctrlKey,
							shiftKey: evt.shiftKey,
							metaKey: evt.metaKey,
							code: evt.code,
							key: evt.key,
							location: evt.location,
							repeat: evt.repeat,
							locale: evt.locale
						};
					}
					send_to_server(e, 'event', false);
				});
			}
		}
	},
	mounted() {
		this.add_event_listeners();
	},
	props: {
		jp_props: Object
	}
});
