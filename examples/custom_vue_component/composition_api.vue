<script>
const { ref, onMounted } = Vue;

export default {
  setup() {
    // reactive state
    const count = ref(0);

    // functions that mutate state and trigger updates
    function increment() {
      count.value++;
    }

    // lifecycle hooks
    onMounted(() => {
      console.log(`The initial count is ${count.value}.`);
    });

    return { count, increment };
  },
};
</script>

<template>
  <button @click="increment">Count is: {{ count }}</button>
</template>
