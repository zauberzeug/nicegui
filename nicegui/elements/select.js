export default {
  props: ["options"],
  template: `
    <q-select
      ref="qRef"
      :options="filteredOptions"
      @filter="filterFn"
      @popup-show="addClass"
      @popup-hide="removeClass"
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
      update(() => (this.filteredOptions = val ? this.findFilteredOptions() : this.initialOptions));
    },
    findFilteredOptions() {
      const needle = this.$el.querySelector("input[type=search]")?.value.toLocaleLowerCase();
      return needle
        ? this.initialOptions.filter((v) => String(v.label).toLocaleLowerCase().indexOf(needle) > -1)
        : this.initialOptions;
    },
    addClass() {
      // NOTE: prevent the page from scrolling when the select popup is closed (#5031)
      document.documentElement.classList.add("nicegui-select-popup-open");
    },
    async removeClass() {
      await this.$nextTick();
      document.documentElement.classList.remove("nicegui-select-popup-open");
    },
  },
  updated() {
    if (!this.$attrs.multiple) return;
    const newFilteredOptions = this.findFilteredOptions();
    if (newFilteredOptions.length !== this.filteredOptions.length) {
      this.filteredOptions = newFilteredOptions;
    }
  },
  unmounted() {
    this.removeClass();
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
