import { loadResource } from "../../static/utils/resources.js";

export default {
  template: `
    <div style="width: 100%">
      <textarea ref="myTextarea"></textarea>
    </div>
  `,
  props: {
    resource_path: String,
  },
  async mounted() {
    // Load CodeMirror resources and initialize it
    await this.$nextTick(); // NOTE: wait for window.path_prefix to be set
    await Promise.all([
      loadResource("https://cdnjs.cloudflare.com/ajax/libs/codemirror/6.65.7/codemirror.min.js"),
      loadResource("https://cdnjs.cloudflare.com/ajax/libs/codemirror/6.65.7/codemirror.min.css"),
      loadResource("https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.63.1/theme/dracula.min.css"),
      loadResource("https://cdnjs.cloudflare.com/ajax/libs/codemirror/6.65.7/mode/python/python.min.js"),
      loadResource("https://cdnjs.cloudflare.com/ajax/libs/codemirror/6.65.7/addon/edit/closebrackets.min.js"),
      loadResource("https://cdnjs.cloudflare.com/ajax/libs/codemirror/6.65.7/addon/fold/foldcode.min.js"),
      loadResource("https://cdnjs.cloudflare.com/ajax/libs/codemirror/6.65.7/addon/fold/foldgutter.min.css"),
      loadResource("https://cdnjs.cloudflare.com/ajax/libs/codemirror/6.65.7/addon/fold/foldgutter.min.js"),
    ]);
    // Initialize CodeMirror
    const myTextarea = this.$refs.myTextarea;
    const myCodeMirror = CodeMirror.fromTextArea(myTextarea, {
      language: "python",
      lineNumbers: true,
      theme: "dracula",
      autoCloseBrackets: true,
      indentWithTabs: true,
      foldGutter: false,
      gutters: ["CodeMirror-linenumbers", "CodeMirror-foldgutter"],
      extraKeys: {
        "Ctrl-.": function (cm) {
          // Shortcut for folding
          console.log("Folding!");
          cm.foldCode(cm.getCursor());
        },
      },
    });
    myCodeMirror.setGutterMarker(0, "CodeMirror-foldgutter", document.createTextNode("+"));
  },
};
