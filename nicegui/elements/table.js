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
      return this.columns.map((column) => {
        const convertedColumn = { ...column };
        for (const attr in convertedColumn) {
          if (attr.startsWith(":")) {
            try {
              convertedColumn[attr.slice(1)] = new Function("return " + convertedColumn[attr])();
              delete convertedColumn[attr];
            } catch (e) {
              console.error(`Error while converting ${attr} attribute to function:`, e);
            }
          }
        }
        return convertedColumn;
      });
    },
  },
};
