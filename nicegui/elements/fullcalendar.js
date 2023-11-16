export default {
  template: "<div></div>",
  props: {
    eventsData: Array,
  },
  mounted() {
    this.calendar = new FullCalendar.Calendar(this.$el, {
      initialView: "timeGridWeek",
      slotMinTime: "05:00:00",
      slotMaxTime: "22:00:00",
      allDaySlot: false,
      timeZone: "local",
      height: "auto",
      events: this.eventsData,
      eventClick: function(info) {
          alert('Event: ' + info.event.title);
          this.$emit("click", {"click":info});
        
      }
    });

    this.calendar.render();
  },
  methods: {
  },
};
