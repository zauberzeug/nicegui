export default {
  template: `
    <q-expansion-item ref="qRef">
      <template v-for="(_, name) in nonDefaultSlots" :key="name" v-slot:[name]="slotProps">
        <slot :name="name" v-bind="slotProps || {}" />
      </template>
      <div class="nicegui-expansion-content">
        <slot></slot>
      </div>
    </q-expansion-item>
  `,
  computed: {
    nonDefaultSlots() {
      const { default: _, ...rest } = this.$slots;
      return rest;
    },
  },
};
