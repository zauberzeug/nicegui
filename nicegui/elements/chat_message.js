export default {
  template: `
    <q-chat-message v-bind="$attrs">
      <template v-for="(_, slot) in $slots" v-slot:[slot]="slotProps">
        <slot :name="slot" v-bind="slotProps || {}" />
      </template>
    </q-chat-message>
  `,
};
