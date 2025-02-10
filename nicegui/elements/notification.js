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
        message: this.message,
        position: this.position,
        multiLine: this.multiLine,
        spinner: this.spinner,
        closeBtn: this.closeBtn,
        timeout: this.timeout,
        group: this.group,
        attrs: this.attrs,
        type: this.type,
        color: this.color,
        icon: this.icon,
        kwargs: this.kwargs,
        onDismiss: () => this.$emit("dismiss"),
      };
      return options;
    },
  },
  props: {
    message: String,
    position: String,
    multiLine: Boolean,
    spinner: Boolean,
    closeBtn: Object,
    timeout: Number,
    group: Boolean,
    attrs: Object,
    type: String,
    color: String,
    icon: String,
    kwargs: Object,
  },
};
