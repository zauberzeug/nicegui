export default {
  mounted() {
    this.add_classes(this.classes);
    this.add_style(this.style);
    this.add_props(this.props);
  },
  methods: {
    add_classes(classes) {
      document.querySelectorAll(this.selector).forEach((e) => e.classList.add(...classes));
    },
    remove_classes(classes) {
      document.querySelectorAll(this.selector).forEach((e) => e.classList.remove(...classes));
    },
    add_style(style) {
      Object.entries(style).forEach(([key, val]) =>
        document.querySelectorAll(this.selector).forEach((e) => e.style.setProperty(key, val))
      );
    },
    remove_style(keys) {
      keys.forEach((key) => document.querySelectorAll(this.selector).forEach((e) => e.style.removeProperty(key)));
    },
    add_props(props) {
      Object.entries(props).forEach(([key, val]) =>
        document.querySelectorAll(this.selector).forEach((e) => e.setAttribute(key, val))
      );
    },
    remove_props(keys) {
      keys.forEach((key) => document.querySelectorAll(this.selector).forEach((e) => e.removeAttribute(key)));
    },
  },
  props: {
    selector: String,
    classes: Array,
    style: Object,
    props: Object,
  },
};
