export default {
  template: `<div></div>`,
  async mounted() {},
  data() {
    return {};
  },
  methods: {
    update(content) {
      this.$el.innerHTML = content;
    },
  },
};
