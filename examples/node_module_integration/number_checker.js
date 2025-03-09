export default {
  async mounted() {
    await import("is-odd");
  },
  methods: {
    isOdd(number) {
      return isOdd(number);
    },
    isEven(number) {
      return !isOdd(number);
    },
  },
};
