export default {
  template: `
    <q-input
      ref="qRef"
      v-bind="$attrs"
      v-model="inputValue"
      :shadow-text="shadowText"
      @keydown.tab="perform_autocomplete"
      :list="id + '-datalist'"
    >
      <template v-for="(_, slot) in $slots" v-slot:[slot]="slotProps">
        <slot :name="slot" v-bind="slotProps || {}" />
      </template>
    </q-input>
    <datalist v-if="withDatalist" :id="id + '-datalist'">
      <option v-for="option in this._autocomplete" :value="option"></option>
    </datalist>
  `,
  props: {
    _autocomplete: Array,
    value: String,
    id: String,
  },
  data() {
    return {
      inputValue: this.value,
      emitting: true,
    };
  },
  beforeUnmount() {
    mounted_app.elements[this.$props.id.slice(1)].props.value = this.inputValue;
  },
  watch: {
    value(newValue) {
      this.emitting = false;
      this.inputValue = newValue;
      this.$nextTick(() => (this.emitting = true));
    },
    inputValue(newValue) {
      if (!this.emitting) return;
      this.$emit("update:value", newValue);
    },
  },
  computed: {
    shadowText() {
      if (!this.inputValue) return "";
      const matchingOption = this._autocomplete.find((option) =>
        option.toLowerCase().startsWith(this.inputValue.toLowerCase()),
      );
      return matchingOption ? matchingOption.slice(this.inputValue.length) : "";
    },
    withDatalist() {
      const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
      return isMobile && this._autocomplete && this._autocomplete.length > 0;
    },
  },
  methods: {
    updateValue() {
      this.inputValue = this.value;
    },
    perform_autocomplete(e) {
      if (this.shadowText) {
        this.inputValue += this.shadowText;
        e.preventDefault();
      }
    },
  },
};
