export default {
  props: ["options"],
  template: `
      <q-select v-bind="$attrs" :options="filteredOptions" @filter="filterFn">
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
        const needle = val.toLocaleLowerCase();
        this.filteredOptions = this.initialOptions.filter((v) => v.label.toLocaleLowerCase().indexOf(needle) > -1);
      });
    },
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
