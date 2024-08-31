import SignaturePad from "signature_pad";

export default {
  template: "<canvas></canvas>",
  props: {
    options: Array,
  },
  mounted() {
    this.pad = new SignaturePad(this.$el, this.options);
  },
  methods: {
    clear() {
      this.pad.clear();
    },
  },
};
