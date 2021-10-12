Vue.component('hotkey', {
	template: `<span v-bind:id="jp_props.id" :class="jp_props.classes" :style="jp_props.style"></span>`,
	methods: {
		add_event_listener_to_parent() {
			const id = this.$props.jp_props.id.toString();
			const element = document.getElementById(id);
			const parent = element.parentNode;
			const key = this.$props.jp_props.options.key;
			const props = this.$props;
			parent.tabIndex = 0;
			parent.addEventListener('mouseover', function (e) {
				parent.focus();
			});
			parent.addEventListener('keydown', function (e) {
				if (parent === document.activeElement) {
					if (e.key === key) {
						send_to_server(
							{
								'event_type': 'onKeydown',
								'id': props.jp_props.id,
								'page_id': page_id,
								'websocket_id': websocket_id
							},
							'event'
						);
					}
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
