import isOdd from "is-odd";

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
