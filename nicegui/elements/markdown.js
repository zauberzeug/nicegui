export default {
  template: `<div></div>`,
  mounted() {
    this.ensure_codehilite_css();
    this.update(this.$el.innerHTML);
  },
  methods: {
    update(content) {
      this.$el.innerHTML = content;
      this.$el.querySelectorAll(".mermaid-pre").forEach((pre, i) => {
        const code = decodeHtml(pre.children[0].innerHTML);
        mermaid.render(`mermaid_${this.$el.id}_${i}`, code, (svg) => (pre.innerHTML = svg));
      });
    },
    ensure_codehilite_css() {
      if (!document.querySelector(`style[data-codehilite-css]`)) {
        const style = document.createElement("style");
        style.setAttribute("data-codehilite-css", "");
        style.innerHTML = this.codehilite_css;
        document.head.appendChild(style);
      }
    },
  },
  props: {
    codehilite_css: String,
  },
};

function decodeHtml(html) {
  const txt = document.createElement("textarea");
  txt.innerHTML = html;
  return txt.value;
}
