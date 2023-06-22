export default {
  template: `
    <q-input v-bind="$attrs" v-model="inputValue" :shadow-text="shadowText" @keydown.tab="perform_autocomplete">
      <template v-for="(_, slot) in $slots" v-slot:[slot]="slotProps">
        <slot :name="slot" v-bind="slotProps || {}" />
      </template>
    </q-input>
  `,
  props: {
    autocomplete: Array,
    value: String,
  },
  data() {
    return {
      inputValue: this.value,
    };
  },
  watch: {
    inputValue(newValue) {
      this.$emit("update:value", newValue);
    },
  },
  computed: {
    shadowText() {
      if (!this.inputValue) return "";
      const matchingOption = this.autocomplete.find((option) =>
        option.toLowerCase().startsWith(this.inputValue.toLowerCase())
      );
      return matchingOption ? matchingOption.slice(this.inputValue.length) : "";
    },
  },
  methods: {
    perform_autocomplete(e) {
      if (this.shadowText) {
        this.inputValue += this.shadowText;
        e.preventDefault();
      }
    },
  },
};
