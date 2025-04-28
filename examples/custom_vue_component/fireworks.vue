<template>
  <div id="fireworks"></div>
</template>

<script>
import { Fireworks } from "https://esm.run/fireworks-js";

export default {
  props: {
    gravity: {
      type: Number,
      default: 1.4,
    },
    opacity: {
      type: Number,
      default: 0.4,
    },
    autoresize: {
      type: Boolean,
      default: true,
    },
    acceleration: {
      type: Number,
      default: 1.0,
    },
  },
  watch: {
    gravity() {
      this.updateOptions();
    },
    opacity() {
      this.updateOptions();
    },
    acceleration() {
      this.updateOptions();
    },
  },
  methods: {
    startFireworks() {
      if (this.fireworks) {
        this.stopFireworks();
      }
      const options = {
        gravity: this.gravity,
        opacity: this.opacity,
        autoresize: this.autoresize,
        acceleration: this.acceleration,
      };
      this.fireworks = new Fireworks(this.$el, options);
      this.fireworks.start();
    },
    stopFireworks() {
      if (this.fireworks) {
        this.fireworks.stop(true);
        this.fireworks = null;
      }
    },
    updateOptions() {
      if (this.fireworks) {
        this.fireworks.updateOptions({
          gravity: this.gravity,
          opacity: this.opacity,
          autoresize: this.autoresize,
          acceleration: this.acceleration,
        });
      }
    },
  },
};
</script>
