import { defineComponent, createElementBlock, openBlock, normalizeStyle, createElementVNode, toDisplayString } from "vue";
const _sfc_main = defineComponent({
  props: {
    title: String
  },
  emits: {
    change: (value) => true
  },
  data() {
    return {
      value: 0
    };
  },
  methods: {
    handle_click(event) {
      this.value += 1;
      this.$emit("change", this.value);
    },
    reset(event) {
      this.value = 0;
    }
  }
});
const _export_sfc = (sfc, props) => {
  const target = sfc.__vccOpts || sfc;
  for (const [key, val] of props) {
    target[key] = val;
  }
  return target;
};
function _sfc_render(_ctx, _cache, $props, $setup, $data, $options) {
  return openBlock(), createElementBlock("button", {
    onClick: _cache[0] || (_cache[0] = (...args) => _ctx.handle_click && _ctx.handle_click(...args)),
    style: normalizeStyle({ background: _ctx.value > 0 ? "#bf8" : "#eee", padding: "8px 16px", borderRadius: "4px" })
  }, [
    createElementVNode("strong", null, toDisplayString(_ctx.title) + ": " + toDisplayString(_ctx.value), 1)
  ], 4);
}
const CounterComposition = /* @__PURE__ */ _export_sfc(_sfc_main, [["render", _sfc_render]]);
export {
  CounterComposition as default
};
