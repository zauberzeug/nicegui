import { convertDynamicProperties } from "../../static/utils/dynamic_properties.js";

export default {
  template: `
    <q-table
      ref="qRef"
      v-bind="$attrs"
      v-bind="columnsProp"
    >
      <template v-for="(_, slot) in $slots" v-slot:[slot]="slotProps">
        <slot :name="slot" v-bind="slotProps || {}" />
      </template>
    </q-table>
  `,
  props: {
    columns: [Array, String],
  },
  computed: {
    columnsProp() {
      if (this.columns === "none") {
        return {};
      }
      let convertedColumns = this.columns;
      convertedColumns.forEach((column) => convertDynamicProperties(column, false));
      return { columns: convertedColumns };
    },
  },
};
