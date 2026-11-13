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
      // Prevent the page from smooth-scrolling when the table exits fullscreen;
      // Quasar restores the scroll position in exitFullscreen via nextTick and requestAnimationFrame,
      // so we remove the class in an animation frame requested after that one.
      if (isFullscreen) {
        document.documentElement.classList.add("nicegui-table-fullscreen");
      } else {
        this.$nextTick(() =>
          requestAnimationFrame(() => document.documentElement.classList.remove("nicegui-table-fullscreen"))
        );
      }
    },
  },
  unmounted() {
    this.setFullscreenClass(false);
  },
};
