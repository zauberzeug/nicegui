export default {
  template: "<span></span>",
  mounted() {
    for (const event of this.events) {
      document.addEventListener(event, (evt) => {
        // https://stackoverflow.com/a/36469636/3419103
        const ignored = ["input", "select", "button", "textarea"];
        const focus = document.activeElement;
        if (focus && ignored.includes(focus.tagName.toLowerCase())) return;
        if (evt.repeat && !this.repeating) return;
        this.$emit("key", {
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
  },
};
