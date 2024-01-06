export default {
  template: `
    <q-card v-bind="$attrs">
      <template v-for="(_, slot) in $slots" v-slot:[slot]="slotProps">
        <div>
          <slot :name="slot" v-bind="slotProps || {}" />
        </div>
      </template>
    </q-card>
  `,
};
