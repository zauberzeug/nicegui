import { convertDynamicProperties } from "../../static/utils/dynamic_properties.js";

export default {
  template: `
    <q-table ref="qRef" :columns="convertedColumns" @fullscreen="setFullscreenClass">
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
  methods: {
    setFullscreenClass(isFullscreen) {
      // NOTE: prevent the page from smooth-scrolling when the table exits fullscreen;
      // Quasar uses setTimeout(() => el.scrollIntoView()) in exitFullscreen,
      // so we need a setTimeout to remove the class after that scroll completes.
      if (isFullscreen) {
        document.documentElement.classList.add("nicegui-table-fullscreen");
      } else {
        setTimeout(() => document.documentElement.classList.remove("nicegui-table-fullscreen"));
      }
    },
  },
  unmounted() {
    this.setFullscreenClass(false);
  },
};
