import { nipplejs } from "nicegui-joystick";

export default {
  template: "<div><div></div></div>",
  mounted() {
    const joystick = nipplejs.create({
      zone: this.$el.children[0],
      position: { left: "50%", top: "50%" },
      dynamicPage: true,
      ...this.options,
    });
    joystick.on("start", (e) => this.$emit("start", e));
    joystick.on("move", (_, data) => this.$emit("move", { data }));
    joystick.on("end", (e) => this.$emit("end", e));
  },
  props: {
    options: Object,
  },
};
