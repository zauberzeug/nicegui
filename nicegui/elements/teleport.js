export default {
  template: `<Teleport v-if="isLoaded" :to="to" :key="key"><slot></slot></Teleport>`,
  props: {
    to: String,
  },
  mounted() {
    this.isLoaded = true;
  },
  data() {
    return {
      key: 0,
      isLoaded: false,
    };
  },
  methods: {
    update() {
      this.key++;
    },
  },
};
