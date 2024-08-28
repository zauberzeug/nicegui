export default {
  template: `
    <div></div>
  `,
  props: {
    conf: Object,
  },
  watch: {
    conf(newConf) {
      this.updateConf(newConf);
    },
  },
  methods: {
    updateConf(conf) {
      this.line.update(conf);
    },
  },
  data() {
    return {
      linePromise: new Promise((resolve) => {
        this.resolveLine = resolve;
      }),
  },
  async mounted() {
    this.line = new Zeitline.Timeline(this.conf);
    this.line.render();
    this.resolveLine(this.line);
  },
};
