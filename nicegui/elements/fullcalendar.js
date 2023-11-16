export default {
  template: "<div></div>",
  props: {
    options: Array,
    eventToAdd: Object
  },
  mounted() {
    this.options.eventClick = (info) => {
      console.log("hi2");
      this.$emit("click", { info: info });
    };

    this.calendar = new FullCalendar.Calendar(this.$el, this.options);
    this.calendar.render();
  },
  methods: {
    update_calendar() {
      if (this.calendar) {
        // this.calendar = new FullCalendar.Calendar(this.$el, this.options);
        // this.calendar.render()
        // this.calendar.addEvent(this.eventToAdd);
        this.calendar.render()
      }
    },
    add_event(eventToAdd) {
      if (this.calendar) {
        this.calendar.addEvent(eventToAdd);
        this.calendar.render() 
        console.log("hi");
      }
      
    }

  },
};