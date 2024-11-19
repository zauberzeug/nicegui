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
    run_editor_method(name, ...args) {
      if (this.editor) {
        if (name.startsWith(":")) {
          name = name.slice(1);
          args = args.map((arg) => new Function(`return (${arg})`)());
        }
        return runMethod(this.editor, name, args);
      }
    },
    add_validation(schema) {
      if (this.editor) {
        try {
          const validator = createAjvValidator({ schema: schema, schemaDefinitions: {}, ajvOptions: {} });
          this.editor.updateProps({ ...this.props, validator: validator });
          return true;
        } catch (err) {
          console.log("Failed to create JSONSchema Validator");
          return false;
        }
      }
    },
  },
  props: {
    properties: Object,
  },
};
