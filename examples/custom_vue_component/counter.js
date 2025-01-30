// NOTE: Make sure to reload the browser with cache disabled after making changes to this file.
export default {
  template: `
    <button @click="handle_click" :style="{ background: value > 0 ? '#bf8' : '#eee', padding: '8px 16px', borderRadius: '4px' }">
      <strong>{{title}}: {{value}}</strong>
    </button>
  `,
  props: {
    title: String,
  },
  data() {
    return {
      value: 0,
    };
  },
  methods: {
    handle_click() {
      this.value += 1;
      this.$emit("change", this.value);
    },
    reset() {
      this.value = 0;
    },
  },
};
