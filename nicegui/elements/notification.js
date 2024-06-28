import { convertDynamicProperties } from "../../static/utils/dynamic_properties.js";

export default {
  mounted() {
    this.notification = Quasar.Notify.create(this.convertedOptions);
  },
  updated() {
    this.notification(this.convertedOptions);
  },
  methods: {
    dismiss() {
      this.notification();
    },
  },
  computed: {
    convertedOptions() {
      convertDynamicProperties(this.options, true);
      const options = {
        ...this.options,
        onDismiss: () => this.$emit("dismiss"),
      };
      return options;
    },
  },
  props: {
    options: Object,
  },
};
