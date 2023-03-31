export default {
  mounted() {
    this.add_classes(this.classes);
    this.add_style(this.style);
    this.add_props(this.props);
  },
  methods: {
    add_classes(classes) {
      document.querySelector(this.selector).classList.add(...classes);
    },
    remove_classes(classes) {
      document.querySelector(this.selector).classList.remove(...classes);
    },
    add_style(style) {
      Object.entries(style).forEach(([key, value]) => (document.querySelector(this.selector).style[key] = value));
    },
    remove_style(keys) {
      keys.forEach((key) => document.querySelector(this.selector).style.removeProperty(key));
    },
    add_props(props) {
      Object.entries(props).forEach(([key, value]) => document.querySelector(this.selector).setAttribute(key, value));
    },
    remove_props(keys) {
      keys.forEach((key) => document.querySelector(this.selector).removeAttribute(key));
    },
  },
  props: {
    selector: String,
    classes: Array,
    style: Object,
    props: Object,
  },
};
