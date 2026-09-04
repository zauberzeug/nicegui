import { loadResource } from "../../static/utils/resources.js";

export default {
  template: "<div></div>",
  props: {
    options: Array,
    resourcePath: String,
    resourcePath: String,
  },
  async mounted() {
    await this.$nextTick(); // wait for window.path_prefix to be set
    await loadResource(window.path_prefix + `${this.resourcePath}/index.global.min.js`);
    await this.$nextTick(); // wait for window.path_prefix to be set
    await loadResource(window.path_prefix + `${this.resourcePath}/index.global.min.js`);
    this.options.eventClick = (info) => this.$emit("click", { info });

const eventsOpt = this.options.events;
    if (eventsOpt === "__fetch__" || typeof eventsOpt === "function") {
      this.options.events = (fetchInfo, successCallback, failureCallback) => {
        const request_id = ++this._next_request_id;
        this._pending_fetches[request_id] = { success: successCallback, failure: failureCallback };
        this.$emit("fetch-events", {
          request_id,
          start: fetchInfo.startStr,
          end: fetchInfo.endStr,
          start_value: fetchInfo.start.valueOf(),
          end_value: fetchInfo.end.valueOf(),
          time_zone: fetchInfo.timeZone,
        });
      };
    }

    this.calendar = new FullCalendar.Calendar(this.$el, this.options);
    this.calendar.render();
  },
  methods: {
    update_calendar() {
      if (this.calendar) {
        if (this.options.events !== "__fetch__") {
          this.calendar.setOption("events", this.options.events);
        }
        this.calendar.refetchEvents();
      }
    },
    on_events_fetched(request_id, events) {
      const pending = this._pending_fetches && this._pending_fetches[request_id];
      if (pending) {
        pending.success(events || []);
        delete this._pending_fetches[request_id];
      }
    },
    on_events_failed(request_id, error) {
      const pending = this._pending_fetches && this._pending_fetches[request_id];
      if (pending) {
        pending.failure(error || new Error("fetch failed"));
        delete this._pending_fetches[request_id];
      }
    },
  },
  created() {
    this._pending_fetches = {};
    this._next_request_id = 0;
  },
};
