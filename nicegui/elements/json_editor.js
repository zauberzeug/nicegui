import { JSONEditor } from "index";

export default {
  template: "<div></div>",
  mounted() {
    this.properties.onChange = (updatedContent, previousContent, { contentErrors, patchResult }) => {
      this.$emit("change", { content: updatedContent, errors: contentErrors });
    };
    this.properties.onSelect = (selection) => {
      this.$emit("select", { selection: selection });
    };
    this.editor = new JSONEditor({
      target: this.$el,
      props: this.properties,
    });
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
        this.editor.destroy();
      }
    },
    call_editor_method(name, arg) {
      if (this.editor) {
        if (arg === null) {
          return this.editor[name]();
        } else {
          this.arg = new Function("return " + arg)();
          return this.editor[name](this.arg);
        }
      }
    },
  },
  props: {
    properties: Object,
  },
};
