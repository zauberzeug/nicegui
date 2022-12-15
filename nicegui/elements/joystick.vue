<template>
  <div></div>
</template>

<script>
export default {
  mounted() {
    const joystick = nipplejs.create({
      zone: this.$el,
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
</script>

<style scoped>
:scope {
  background-color: AliceBlue;
  position: relative;
  width: 10em;
  height: 10em;
}
</style>
