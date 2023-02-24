export default {
  template: `<q-knob>
      <q-icon :name="this.inner_icon" :size="this.size_icon" :color="this.color_icon" />
    </q-knob>`,
  props: {
    color_icon: String,
    inner_icon: String,
    size_icon: String,
  },
};
