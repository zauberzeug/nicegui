export default {
  template: `
    <q-uploader
      ref="qRef"
      :url="computed_url"
    >
      <template v-for="(_, slot) in $slots" v-slot:[slot]="slotProps">
        <slot :name="slot" v-bind="slotProps || {}" />
      </template>
    </q-uploader>
  `,
  mounted() {
    setTimeout(() => this.compute_url(), 0); // NOTE: wait for window.path_prefix to be set in app.mounted()
  },
  updated() {
    this.compute_url();
  },
  methods: {
    compute_url() {
      this.computed_url = (this.url.startsWith("/") ? window.path_prefix : "") + this.url;
    },
  },
  props: {
    url: String,
  },
  data: function () {
    return {
      computed_url: this.url,
    };
  },
};
