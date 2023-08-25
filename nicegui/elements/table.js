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
        for (const attr in column) {
          if (attr.startsWith(":")) {
            try {
              column[attr.slice(1)] = new Function("return " + column[attr])();
              delete column[attr];
            } catch (e) {
              console.error(`Error while converting ${attr} attribute to function:`, e);
            }
          }
        }
        return column;
      });
    },
  },
};
