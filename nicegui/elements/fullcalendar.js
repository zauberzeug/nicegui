export default {
  template: "<div></div>",
  props: {
    options: Array,
    // eventToAdd: Object
  },
  mounted() {
    this.options.eventClick = (info) => {
      this.$emit("click", { info: info });
    };

    this.calendar = new FullCalendar.Calendar(this.$el, this.options);
    this.calendar.render();
  },
  methods: {
    update_calendar() {
      if (this.calendar) {   
        this.calendar.setOption('events', this.options.events)
        this.calendar.render();
          }
    },



  },
};