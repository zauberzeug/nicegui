<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  props: {
    title: String,
  },
  emits: {
    change: (value: number) => true,
  },
  data() {
    return {
      value: 0,
    };
  },
  methods: {
    handle_click(event: Event) {
      this.value += 1;
      this.$emit("change", this.value);
    },
    reset(event: Event) {
      this.value = 0;
    }
  }
});
</script>

<template>
  <button @click="handle_click" :style="{ background: value > 0 ? '#bf8' : '#eee', padding: '8px 16px', borderRadius: '4px' }">
    <strong>{{title}}: {{value}}</strong>
  </button>
</template>
