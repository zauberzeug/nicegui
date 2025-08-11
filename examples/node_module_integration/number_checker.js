import isOdd from "is-odd/index.js";

export default {
  methods: {
    isOdd(number) {
      return isOdd(number);
    },
    isEven(number) {
      return !isOdd(number);
    },
  },
};
