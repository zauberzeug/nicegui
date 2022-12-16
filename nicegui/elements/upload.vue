<template>
  <div>
    <q-file :label="file_picker_label" v-model="file" :multiple="multiple" />
    <q-btn :icon="upload_button_icon" @click="upload" size="sm" round color="primary" />
  </div>
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
    upload_button_icon: String,
  },
};
</script>

<style scoped></style>
