export default {
  template: `<div><slot></slot></div>`,
  mounted() {
    if (!navigator.clipboard) this.$el.querySelector(".q-btn").style.display = "none";
  },
  props: {
    content: String,
  },
};
