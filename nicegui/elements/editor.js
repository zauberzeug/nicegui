import DOMPurify from "dompurify";

export default {
  template: `
    <q-editor ref="qRef" v-model="inputValue">
      <template v-for="(_, slot) in $slots" v-slot:[slot]="slotProps">
        <slot :name="slot" v-bind="slotProps || {}" />
      </template>
    </q-editor>
  `,
  props: {
    value: String,
    sanitize: Boolean,
  },
  data() {
    return {
      inputValue: this.sanitizedValue(),
      emitting: true,
    };
  },
  beforeUnmount() {
    const element = mounted_app.elements[this.$el.id.slice(1)];
    if (element) element.props.value = this.inputValue;
  },
  watch: {
    value() {
      this.emitting = false;
      this.inputValue = this.sanitizedValue();
      this.$nextTick(() => (this.emitting = true));
    },
    inputValue(newValue) {
      if (!this.emitting) return;
      this.$emit("update:value", newValue);
    },
  },
  methods: {
    updateValue() {
      this.inputValue = this.sanitizedValue();
    },
    sanitizedValue() {
      return this.sanitize ? DOMPurify.sanitize(this.value ?? "") : this.value;
    },
  },
};
