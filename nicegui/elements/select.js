export default {
  props: ["options"],
  template: `
    <q-select
        v-bind="$attrs"
        :model-value="model"
        :options="options"
        @filter="filterFn"
        @input-value="setModel"
    >
        <template v-for="(_, slot) in $slots" v-slot:[slot]="slotProps">
            <slot :name="slot" v-bind="slotProps || {}" />
        </template>
    </q-select>
  `,
  setup(props) {
    const stringOptions = Vue.ref(props.options);
    const model = Vue.ref(null);
    const options = Vue.ref(stringOptions.value);
    const filterFn = (val, update, abort) => {
      update(() => {
        const needle = val.toLocaleLowerCase();
        options.value = stringOptions.value.filter((v) => v.label.toLocaleLowerCase().indexOf(needle) > -1);
      });
    };
    const setModel = (val) => (model.value = val);
    Vue.watch(
      () => props.options,
      (newVal) => {
        stringOptions.value = newVal;
        options.value = stringOptions.value;
      }
    );
    return {
      model,
      options,
      filterFn,
      setModel,
    };
  },
};
