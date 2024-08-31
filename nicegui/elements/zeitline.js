export default {
  template: `
    <div></div>
  `,
  props: {
    conf: Object,
    resource_path: String,
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
      })
    }
  },
  async mounted() {
    await this.$nextTick(); // NOTE: wait for window.path_prefix to be set
    this.ZL = await import(window.path_prefix + `${this.resource_path}/zeitline.bundle.min.js`);
    const ZL = this.ZL;
    this.line = new ZL.Timeline(this.conf);
    this.line.render();
    this.resolveLine(this.line);
  },
};
