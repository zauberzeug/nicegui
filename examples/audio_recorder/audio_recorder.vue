<template>
  <div>
    <button class="record-button" @mousedown="startRecording" @mouseup="stopRecording">Hold to Record</button>
    <audio ref="audioPlayer"></audio>
  </div>
</template>

<script>
export default {
  data() {
    return {
      isRecording: false,
      audioChunks: [],
      mediaRecorder: null,
      stream: null,
      audioURL: null,
      audioBlob: null,
    };
  },
  mounted() {
    this.requestMicrophonePermission();
  },
  watch: {
    audioBlob(newBlob, oldBlob) {
      if (newBlob && newBlob !== oldBlob) {
        this.emitBlob(); // Emit the blob when it's non-null and changes
      }
    },
  },
  methods: {
    async requestMicrophonePermission() {
      try {
        this.stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      } catch (error) {
        console.error("Error accessing microphone:", error);
      }
    },
    async startRecording() {
      try {
        if (!this.stream) {
          await this.requestMicrophonePermission();
        }
        this.audioChunks = [];
        this.mediaRecorder = new MediaRecorder(this.stream);
        this.mediaRecorder.addEventListener("dataavailable", (event) => {
          if (event.data.size > 0) {
            this.audioChunks.push(event.data);
          }
        });
        this.mediaRecorder.start();
        this.isRecording = true;
      } catch (error) {
        console.error("Error accessing microphone:", error);
      }
    },
    stopRecording() {
      if (this.isRecording) {
        this.mediaRecorder.addEventListener("stop", () => {
          this.isRecording = false;
          this.saveBlob();
          // this.playRecordedAudio();
        });
        this.mediaRecorder.stop();
      }
    },
    async playRecordedAudio() {
      this.audioURL = window.URL.createObjectURL(this.audioBlob);
      this.$refs.audioPlayer.src = this.audioURL;
      this.$refs.audioPlayer.play();
    },
    saveBlob() {
      this.audioBlob = new Blob(this.audioChunks, { type: "audio/wav" });
    },
    emitBlob() {
      const reader = new FileReader();
      reader.onload = () => {
        const base64Data = reader.result.split(",")[1]; // Extracting base64 data from the result
        this.$emit("audio_ready", { audioBlobBase64: base64Data });
      };
      reader.readAsDataURL(this.audioBlob);
    },
  },
};
</script>

<style scoped>
.record-button {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  background-color: red;
  color: white;
  border: 2px solid white;
  font-size: 16px;
  box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.3);
  transition: transform 0.2s, box-shadow 0.2s;
}

.record-button:active {
  transform: translateY(2px);
  box-shadow: 1px 1px 3px rgba(0, 0, 0, 0.3);
}
</style>
