import { JSONEditor, createAjvValidator } from "standalone";

export default {
  template: "<div></div>",
  mounted() {
    this.properties.onChange = (updatedContent, previousContent, { contentErrors, patchResult }) => {
      this.$emit("change", { content: updatedContent, errors: contentErrors });
    };
    this.properties.onSelect = (selection) => {
      this.$emit("select", { selection: selection });
    };

    this.checkValidation();
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
    checkValidation() {
      if (this.schema !== undefined) {
        this.properties.validator = createAjvValidator({ schema: this.schema, schemaDefinitions: {}, ajvOptions: {} });
      }
    },
    update_editor() {
      if (this.editor) {
        this.checkValidation();
        this.editor.updateProps(this.properties);
      }
    },
    destroyEditor() {
      if (this.editor) {
        this.editor.destroy();
      }
    },
    run_editor_method(name, ...args) {
      if (this.editor) {
        if (name.startsWith(":")) {
          name = name.slice(1);
          args = args.map((arg) => new Function(`return (${arg})`)());
        }
        return runMethod(this.editor, name, args);
      }
    },
  },
  props: {
    properties: Object,
    schema: Object,
  },
};
