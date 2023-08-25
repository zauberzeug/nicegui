import { convertDynamicProperties } from "../../static/utils/dynamic_properties.js";

export default {
  template: `
    <q-table
      ref="qRef"
      v-bind="$attrs"
      :columns="convertedColumns"
    >
      <template v-for="(_, slot) in $slots" v-slot:[slot]="slotProps">
        <slot :name="slot" v-bind="slotProps || {}" />
      </template>
    </q-table>
  `,
  props: {
    columns: Array,
  },
  computed: {
    convertedColumns() {
      this.columns.forEach((column) => convertDynamicProperties(column, false));
      return this.columns;
    },
  },
};
