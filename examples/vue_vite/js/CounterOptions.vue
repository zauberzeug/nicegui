<script setup lang="ts">
import { ref, defineProps, defineEmits, defineExpose } from "vue";

const props = defineProps<{
  title: string;
}>();

const emit = defineEmits<{
  change: [value: number];
}>();

const value = ref(0);

function handle_click(event: Event) {
  value.value += 1;
  emit("change", value.value);
}

function reset(event: Event) {
  value.value = 0;
}

defineExpose({ reset });
</script>

<template>
  <button
    @click="handle_click"
    :style="{ background: value > 0 ? '#bf8' : '#eee', padding: '8px 16px', borderRadius: '4px' }"
  >
    <strong>{{ title }}: {{ value }}</strong>
  </button>
</template>
