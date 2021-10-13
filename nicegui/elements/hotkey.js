Vue.component('hotkey', {
	template: `<span v-bind:id="jp_props.id" :class="jp_props.classes" :style="jp_props.style"></span>`,
	methods: {
		add_event_listener_to_parent() {
			const id = this.$props.jp_props.id.toString();
			const element = document.getElementById(id);
			const parent = element.parentNode;
			const keys = this.$props.jp_props.options.keys;
			const props = this.$props;
			const map = keys.reduce((ac,a) => ({...ac,[a]:false}), {});
			const send_event = () => send_to_server(
				{
					'event_type': 'onKeydown',
					'id': props.jp_props.id,
					'page_id': page_id,
					'websocket_id': websocket_id
				},
				'event'
			);
			parent.tabIndex = 0;
			parent.addEventListener('mouseover', function (e) {
				parent.focus();
			});
			$(parent).keydown(function(e) {
					if (parent === document.activeElement && e.key in map) {
							map[e.key] = true;
							if (Object.values(map).every(Boolean)) {
									send_event()
							}
					}
			}).keyup(function(e) {
					if (e.key in map) {
							map[e.key] = false;
					}
			});
		}
	},
	mounted() {
		this.add_event_listener_to_parent();
	},
	props: {
		jp_props: Object
	}
});
