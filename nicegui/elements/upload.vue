<template>
  <q-uploader :url="url" :label="file_picker_label" :auto-upload="auto_upload" :multiple="multiple" />
</template>

<script>
export default {
  data() {
    return {
      file: undefined,
    };
  },
  methods: {
    upload() {
      if (!this.file) return;
      const files = this.multiple ? this.file : [this.file];
      const args = files.map((file) => ({
        content: file,
        name: file.name,
        lastModified: file.lastModified / 1000,
        size: file.size,
        type: file.type,
      }));
      this.$emit("upload", args);
    },
    reset() {
      this.file = undefined;
    },
  },
  props: {
    multiple: Boolean,
    file_picker_label: String,
    auto_upload: Boolean,
    upload_button_icon: String,
    url: String,
  },
};
</script>

<style scoped></style>
