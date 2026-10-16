export default {
  props: {
    url: String,
    mime_type: String,
  },
  methods: {
    async start() {
      if (this.recorder?.state === "recording") return;
      try {
        this.stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      } catch (error) {
        this.$emit("error", { name: error.name, message: error.message });
        return;
      }
      const chunks = [];
      this.recorder = new MediaRecorder(this.stream, this.mime_type ? { mimeType: this.mime_type } : {});
      this.recorder.ondataavailable = (event) => event.data.size && chunks.push(event.data);
      this.recorder.onstop = () => {
        this.stream.getTracks().forEach((track) => track.stop());
        const type = this.recorder.mimeType;
        const extension = type.split("/")[1]?.split(";")[0] || "bin";
        const form = new FormData();
        form.append("file", new Blob(chunks, { type }), `recording.${extension}`);
        fetch((this.url.startsWith("/") ? window.path_prefix : "") + this.url, { method: "POST", body: form });
      };
      this.recorder.start();
    },
    stop() {
      if (this.recorder?.state === "recording") this.recorder.stop();
    },
  },
  unmounted() {
    this.stop();
  },
};
