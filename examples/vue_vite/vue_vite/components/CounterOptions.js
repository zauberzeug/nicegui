import { defineComponent, ref, createElementBlock, openBlock, normalizeStyle, createElementVNode, toDisplayString } from "vue";
const _sfc_main = /* @__PURE__ */ defineComponent({
  __name: "CounterOptions",
  props: {
    title: {}
  },
  emits: ["change"],
  setup(__props, { expose: __expose, emit: __emit }) {
    const emit = __emit;
    const value = ref(0);
    function handle_click(event) {
      value.value += 1;
      emit("change", value.value);
    }
    function reset(event) {
      value.value = 0;
    }
    __expose({ reset });
    return (_ctx, _cache) => {
      return openBlock(), createElementBlock("button", {
        onClick: handle_click,
        style: normalizeStyle({ background: value.value > 0 ? "#bf8" : "#eee", padding: "8px 16px", borderRadius: "4px" })
      }, [
        createElementVNode("strong", null, toDisplayString(__props.title) + ": " + toDisplayString(value.value), 1)
      ], 4);
    };
  }
});
export {
  _sfc_main as default
};
