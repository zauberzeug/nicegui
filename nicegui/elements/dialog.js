export default {
  template: `
    <q-dialog
      v-bind="$attrs"
      @before-show="disableSmooth"
      @hide="enableSmooth"
    >
      <slot />
    </q-dialog>
  `,
  unmounted() {
    this.enableSmooth();
  },
  methods: {
    // NOTE: this is a workaround to prevent the page from scrolling when the dialog is closed (see https://github.com/zauberzeug/nicegui/issues/5031)
    disableSmooth() {
      const element = document.documentElement;
      this.__prevScrollBehavior = element.style.scrollBehavior;
      element.style.scrollBehavior = "auto";
    },
    enableSmooth() {
      const element = document.documentElement;
      if (this.__prevScrollBehavior !== undefined) {
        element.style.scrollBehavior = this.__prevScrollBehavior;
        this.__prevScrollBehavior = undefined;
      } else {
        element.style.removeProperty("scroll-behavior");
      }
    },
  },
};
