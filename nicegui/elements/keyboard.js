export default {
  mounted() {
    for (const event of this.events) {
      document.addEventListener(event, (evt) => {
        // https://github.com/zauberzeug/nicegui/issues/4290
        if (!(evt instanceof KeyboardEvent)) return;

        // https://stackoverflow.com/a/36469636/3419103
        const focus = document.activeElement;
        if (focus && this.ignore.includes(focus.tagName.toLowerCase())) return;

        if (evt.repeat && !this.repeating) return;

        this.$emit("key", {
          event: evt,
          action: event,
          altKey: evt.altKey,
          ctrlKey: evt.ctrlKey,
          shiftKey: evt.shiftKey,
          metaKey: evt.metaKey,
          code: evt.code,
          key: evt.key,
          location: evt.location,
          repeat: evt.repeat,
          locale: evt.locale,
        });
      });
    }
  },
  props: {
    events: Array,
    repeating: Boolean,
    ignore: Array,
  },
};
