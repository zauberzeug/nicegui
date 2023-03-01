export default {
  mounted() {
    this.add_classes(this.classes);
    this.add_style(this.style);
    this.add_props(this.props);
  },
  methods: {
    add_classes(classes) {
      document.body.classList.add(...classes);
    },
    remove_classes(classes) {
      document.body.classList.remove(...classes);
    },
    add_style(style) {
      Object.entries(style).forEach(([key, value]) => (document.body.style[key] = value));
    },
    remove_style(keys) {
      keys.forEach((key) => document.body.style.removeProperty(key));
    },
    add_props(props) {
      Object.entries(props).forEach(([key, value]) => document.body.setAttribute(key, value));
    },
    remove_props(keys) {
      keys.forEach((key) => document.body.removeAttribute(key));
    },
  },
  props: {
    classes: Array,
    style: Object,
    props: Object,
  },
};
