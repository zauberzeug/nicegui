export default {
  template: "<div></div>",
  mounted() {
    this.map = L.map(this.$el);
    L.tileLayer("http://{s}.tile.osm.org/{z}/{x}/{y}.png").addTo(this.map);
  },
  methods: {
    set_location(latitude, longitude) {
      this.target = L.latLng(latitude, longitude);
      this.map.setView(this.target, 9);
      if (this.marker) {
        this.map.removeLayer(this.marker);
      }
      this.marker = L.marker(this.target);
      this.marker.addTo(this.map);
    },
  },
};
