<template>
    <button @click="handle_click">
      <strong>{{title}}: {{value}}</strong>
    </button>
  </template>
  
  <script>
    export default {
      data() {
        return {
          value: 0
        }
      },
      methods: {
        handle_click() {
          this.value += 1;
          this.$emit("change", this.value);
        },
        reset() {
          this.value = 0
        },
        dummy() {}
      },
      props: {
        title: String
      }
    }
  </script>