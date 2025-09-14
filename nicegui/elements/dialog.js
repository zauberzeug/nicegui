export default {
  template: `
    <q-dialog @show="addClass" @hide="removeClass">
      <slot />
    </q-dialog>
  `,
  methods: {
    addClass() {
      // NOTE: prevent the page from scrolling when the dialog is closed (#5031)
      document.documentElement.classList.add("nicegui-dialog-open");
    },
    removeClass() {
      document.documentElement.classList.remove("nicegui-dialog-open");
    },
  },
  unmounted() {
    this.removeClass();
  },
};
