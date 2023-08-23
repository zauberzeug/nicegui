import { JSONEditor } from "index";

export default {
  template: "<div></div>",
  mounted() {
    setTimeout(() => {
      this.properties.onChange = (updatedContent, previousContent, { contentErrors, patchResult }) => {
        this.$emit("change", { content: updatedContent, errors: contentErrors });
      };
      this.properties.onSelect = (selection) => {
        if (selection.type === "text") {
          this.$emit("select_text", { main: selection.main, ranges: selection.ranges, type: selection.type });
        } else {
          this.$emit("select_json", { edit: selection.edit, path: selection.path, type: selection.type });
        }
      };
      this.editor = new JSONEditor({
        target: this.$el,
        props: this.properties,
      });
    }, 0); // NOTE: wait for window.path_prefix to be set in app.mounted()
  },
  beforeDestroy() {
    this.destroyEditor();
  },
  beforeUnmount() {
    this.destroyEditor();
  },
  methods: {
    update_editor() {
      if (this.editor) {
        this.editor.updateProps(this.properties);
      }
    },
    destroyEditor() {
      if (this.editor) {
        this.editor.dispose();
      }
    },
  },
  props: {
    properties: Object,
  },
};
