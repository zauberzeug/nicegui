// fullcalendar.js
import FullCalendar from './lib/fullcalendar/index.global.min.js';
export default {
    template: "<div></div>",
    props: {
      eventsData: Array,
      elementId: String,
    },
    mounted() {
      this.renderFullCalendar();
    },
    methods: {
      renderFullCalendar() {
        var calendarEl = this.$el;
  
        if (calendarEl) {
          window.calendarInstance = new FullCalendar.Calendar(calendarEl, {
            initialView: 'timeGridWeek',
            slotMinTime: "05:00:00",
            slotMaxTime: "22:00:00",
            allDaySlot: false,
            timeZone: 'local',
            height: 'auto',
            events: this.eventsData,
          });
  
          window.calendarInstance.render();
        }
      },
    },
  };