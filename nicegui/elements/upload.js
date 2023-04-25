export default {
  template: `
    <q-uploader ref="uploader" :url="computed_url">
        <template v-for="(_, slot) in $slots" v-slot:[slot]="slotProps">
            <slot :name="slot" v-bind="slotProps || {}" />
        </template>
    </q-uploader>
  `,
  mounted() {
    setTimeout(() => {
      this.computed_url = (window.path_prefix || "") + this.url;
    }, 0); // NOTE: wait for window.path_prefix to be set in app.mounted()
  },
  methods: {
    reset() {
      this.$refs.uploader.reset();
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
