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
      // Read files, send via bridge, then let QUploader finish cleanly
      return Promise.all(
        files.map(
          (file) =>
            new Promise((resolve) => {
              const reader = new FileReader();
              reader.onload = () => {
                const base64 = reader.result.split(",")[1];
                resolve({ name: file.name, type: file.type, data: base64 });
              };
              reader.readAsDataURL(file);
            })
        )
      ).then((fileDataArray) => {
        window.niceguiBridge.onUpload(JSON.stringify({ id: elementId, files: fileDataArray }));
        const qRef = this.$refs.qRef;
        if (qRef) {
          qRef.uploadedFiles = qRef.uploadedFiles.concat(files);
          files.forEach((f) => qRef.updateFileStatus(f, "uploaded"));
        }
        // Empty URL makes performUpload skip XHR and just decrement workingThreads
        return { url: "" };
      });
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
