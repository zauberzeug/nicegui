// import FullCalendar from "@fullcalendar/vue3";
// import FullCalendar from "../elements/lib/fullcalendar/index.global.js";
// import FullCalendar from "/index.global.min.js";
// import FullCalendar from "/_nicegui/1.4.0/libraries/f2236eb73ecd4b599de1d20d128079e5/index.global.min.js"; 
import FullCalendar from "/_nicegui/1.4.0/libraries/1f5b0e0b0b0b0b0b0b0b0b0b0b0b0b0b/index.global.min.js";
export default {
  template: "<div></div>",
  props: {
    options: Array,
  },
  mounted() {
    this.options.eventClick = (info) => this.$emit("click", { info });
    this.calendar = new FullCalendar.Calendar(this.$el, this.options);
    this.calendar.render();
  },
  methods: {
    update_calendar() {
      if (this.calendar) {
        this.calendar.setOption("events", this.options.events);
        this.calendar.render();
      }
    },
  },
};
