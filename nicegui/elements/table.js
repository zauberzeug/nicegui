import { convertDynamicProperties } from "../../static/utils/dynamic_properties.js";

export default {
  inheritAttrs: false,
  template: `
    <div>
      <q-table ref="qRef" v-bind="$attrs" :columns="convertedColumns">
        <template v-for="(_, slot) in forwardedSlots" v-slot:[slot]="slotProps">
          <slot :name="slot" v-bind="slotProps || {}" />
        </template>
      </q-table>
      <slot />
    </div>
  `,
  props: {
    columns: Array,
  },
  computed: {
    convertedColumns() {
      this.columns.forEach((column) => convertDynamicProperties(column, false));
      return this.columns;
    },
    forwardedSlots() {
      const { default: _default, ...nonDefaultSlots } = this.$slots;
      return nonDefaultSlots;
    },
  },
};
