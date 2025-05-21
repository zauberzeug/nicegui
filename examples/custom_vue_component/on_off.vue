<template>
  <div>
    <button @click="handle_click" :class="{ active: value }">
      <strong>{{ title }}: {{ value ? "ON" : "OFF" }}</strong>
    </button>
  </div>
</template>

<script>
export default {
  props: {
    title: String,
  },
  data() {
    return {
      value: false,
    };
  },
  methods: {
    handle_click() {
      this.value = !this.value;
      this.$emit("change", this.value);
    },
    reset() {
      this.value = false;
    },
  },
};
</script>

<style scoped>
button {
  background-color: #eee;
  padding: 8px 16px;
  border-radius: 4px;
}

button.active {
  background-color: #fb8;
}
</style>
