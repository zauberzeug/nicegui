export default {
  template: `<Teleport :to="to" :key="key"><slot></slot></Teleport>`,
  props: {
    to: String,
  },
  data() {
    return {
      key: 0,
    };
  },
  methods: {
    forceUpdate() {
      this.key++;
    },
  },
};
