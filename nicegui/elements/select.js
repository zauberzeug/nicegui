export default {
  props: ["options"],
  template: `
    <q-select
      ref="qRef"
      v-bind="$attrs"
      :options="filteredOptions"
      @filter="filterFn"
    >
      <template v-for="(_, slot) in $slots" v-slot:[slot]="slotProps">
        <slot :name="slot" v-bind="slotProps || {}" />
      </template>
    </q-select>
  `,
  data() {
    return {
      initialOptions: this.options,
      filteredOptions: this.options,
    };
  },
  methods: {
    filterFn(val, update, abort) {
      update(() => {
        const needle = this.$attrs.multiple
          ? this.$el.querySelector("input[type=search]")?.value.toLocaleLowerCase()
          : val.toLocaleLowerCase()
        this.filteredOptions = this.findFilteredOptions(needle)
      });
    },
    findFilteredOptions(needle) {
      return needle
        ? this.initialOptions.filter((v) => String(v.label).toLocaleLowerCase().indexOf(needle) > -1)
        : this.initialOptions;
    },
  },
  updated() {
    if (this.$attrs.multiple) {
      const needle = this.$el.querySelector("input[type=search]")?.value.toLocaleLowerCase()
      const newFilteredOptions = this.findFilteredOptions(needle)
      if (newFilteredOptions.length !== this.filteredOptions.length) {
        this.filteredOptions = newFilteredOptions;
      }
    }
  },
  watch: {
    options: {
      handler(newOptions) {
        this.initialOptions = newOptions;
        this.filteredOptions = newOptions;
      },
      immediate: true,
    },
  },
};
