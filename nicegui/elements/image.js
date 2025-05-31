export default {
  template: `
    <component
      :is="is_parallax ? 'q-parallax' : 'q-img'"
      ref="qRef"
      v-bind="$attrs"
      :src="computed_src"
    >
      <template v-for="(_, slot) in $slots" v-slot:[slot]="slotProps">
        <slot :name="slot" v-bind="slotProps || {}" />
      </template>
    </component>
  `,
  props: {
    src: String,
    t: String,
    is_parallax: {
      type: Boolean,
      default: false,
    },
  },
  data: function () {
    return {
      computed_src: undefined,
    };
  },
  mounted() {
    setTimeout(() => this.compute_src(), 0); // NOTE: wait for window.path_prefix to be set in app.mounted()
  },
  updated() {
    this.compute_src();
  },
  methods: {
    compute_src() {
      const suffix = this.t ? (this.src.includes("?") ? "&" : "?") + "_nicegui_t=" + this.t : "";
      this.computed_src = (this.src.startsWith("/") ? window.path_prefix : "") + this.src + suffix;
    },
  },
};
