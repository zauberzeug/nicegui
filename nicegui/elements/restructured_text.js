export default {
  template: `<div></div>`,
  methods: {
    update(content) {
      this.$el.innerHTML = content;
    },
  },
};
