export default {
  props: {
    url: String,
    mime_type: String,
  },
  methods: {
    async start() {
      if (this.session) return;
      const session = (this.session = { cancelled: false });
      let stream;
      try {
        stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        if (session.cancelled) return stream.getTracks().forEach((track) => track.stop());
        const recorder = new MediaRecorder(stream, this.mime_type ? { mimeType: this.mime_type } : {});
        const chunks = [];
        recorder.ondataavailable = (event) => event.data.size && chunks.push(event.data);
        recorder.onstop = () => {
          stream.getTracks().forEach((track) => track.stop());
          if (!session.discard) this.upload(new Blob(chunks, { type: recorder.mimeType }));
        };
        recorder.start();
        session.recorder = recorder;
      } catch (error) {
        stream?.getTracks().forEach((track) => track.stop());
        if (this.session === session) this.session = null;
        this.$emit("error", { name: error.name, message: error.message });
      }
    },
    stop(discard = false) {
      const session = this.session;
      if (!session) return;
      this.session = null;
      session.cancelled = true;
      session.discard = discard;
      session.recorder?.stop();
    },
    async upload(blob) {
      const extension = blob.type.split("/")[1]?.split(";")[0] || "bin";
      const form = new FormData();
      form.append("file", blob, `recording.${extension}`);
      try {
        const url = (this.url.startsWith("/") ? window.path_prefix : "") + this.url;
        const response = await fetch(url, { method: "POST", body: form });
        if (!response.ok) throw new Error(`Upload failed with status ${response.status}`);
      } catch (error) {
        this.$emit("error", { name: "UploadError", message: error.message });
      }
    },
  },
  unmounted() {
    this.stop(true);
  },
};
