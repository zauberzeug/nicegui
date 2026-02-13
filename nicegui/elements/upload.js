export default {
  template: `
    <q-uploader
      ref="qRef"
      :url="computed_url"
      :factory="factoryFn"
    >
      <template v-for="(_, slot) in $slots" v-slot:[slot]="slotProps">
        <slot :name="slot" v-bind="slotProps || {}" />
      </template>
    </q-uploader>
  `,
  mounted() {
    setTimeout(() => this.compute_url(), 0); // NOTE: wait for window.path_prefix to be set in app.mounted()
  },
  updated() {
    this.compute_url();
  },
  methods: {
    compute_url() {
      this.computed_url = (this.url.startsWith("/") ? window.path_prefix : "") + this.url;
    },
    factoryFn(files) {
      // Pyodide mode: read files client-side and send via bridge instead of HTTP POST
      if (!window.niceguiBridge || !window.niceguiBridge.onUpload) return { url: this.computed_url };
      const elementId = this.$el.id?.replace(/^c/, "");
      if (!elementId) return { url: this.computed_url };
      const promises = files.map(
        (file) =>
          new Promise((resolve) => {
            const reader = new FileReader();
            reader.onload = () => {
              const base64 = reader.result.split(",")[1];
              resolve({ name: file.name, type: file.type, data: base64 });
            };
            reader.readAsDataURL(file);
          })
      );
      // Handle the upload via the bridge, then reset the uploader
      Promise.all(promises).then((fileDataArray) => {
        const msg = JSON.stringify({ id: elementId, files: fileDataArray });
        window.niceguiBridge.onUpload(msg);
        setTimeout(() => this.$refs.qRef?.reset(), 100);
      });
      // Return a never-resolving Promise to prevent QUploader from sending an XHR POST
      return new Promise(() => {});
    },
  },
  props: {
    url: String,
  },
  data: function () {
    return {
      computed_url: this.url,
    };
  },
};
