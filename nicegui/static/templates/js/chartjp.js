//{% raw %}


var cached_graph_def = {};
var tooltip_timeout = null;
// var tooltip_timeout_period = 100;
Vue.component('chart', {

    template:
        `<div v-bind:id="jp_props.id" :class="jp_props.classes"  :style="jp_props.style" ></div>`,
    methods: {
        evaluate_formatters(def) {
            if (Array.isArray(def)) {
                for (const element of def) {
                    this.evaluate_formatters(element);
                }
            } else if (typeof def == "object" && typeof def == "object") {
                for (const [key, value] of Object.entries(def)) {
                    if (key.toLowerCase().includes('formatter')) {
                        eval('def[key] = ' + def[value]);
                    }
                    this.evaluate_formatters(value);
                }
            }
        },
        graph_change() {
            cached_graph_def[this.$props.jp_props.id] = JSON.stringify(this.$props.jp_props.def);
            var container = this.$props.jp_props.id.toString();
            // Evaluate all properties that include 'formatter'
            this.evaluate_formatters(this.$props.jp_props.def);
            if (this.$props.jp_props.stock) {
                var c = Highcharts.stockChart(container, this.$props.jp_props.def);
            } else {
                var c = Highcharts.chart(container, this.$props.jp_props.def);
            }
            var id = this.$props.jp_props.id;
            var tooltip_timeout_period = this.$props.jp_props.tooltip_debounce;
            var props = this.$props.jp_props;
            cached_graph_def['chart' + container] = c;
            var update_dict = {};
            if (this.$props.jp_props.events.indexOf('tooltip') >= 0) {
                var point_array = [];
                update_dict.tooltip = {
                    useHTML: true,
                    shape: 'callout',
                    positioner: function (boxWidth, boxHeight, point) {
                        var yf = props.tooltip_y;  // 40 is default
                        var xf = props.tooltip_x;  // 40 is default
                        if (props.tooltip_fixed) return {
                            x: xf,
                            y: yf
                        };
                        return {
                            x: point.plotX + c.plotLeft + xf,
                            y: point.plotY + c.plotTop - yf
                        };
                    },
                    formatter: function (tooltip) {
                        if (this.point != null) {
                            // Tooltip not shared or split
                            var e = {
                                event_type: 'tooltip',
                                id: id,
                                x: this.point.x,
                                y: this.point.y,
                                z: this.point.z,
                                category: this.key,
                                color: this.point.color,
                                percentage: this.point.percentage,
                                total: this.point.total,
                                point_index: this.point.index,
                                series_name: this.series.name,
                                series_index: this.series.index,
                                page_id: page_id,
                                websocket_id: websocket_id
                            };

                        } else {
                            // Tooltip shared or split
                            for (let i = 0; i < this.points.length; i++) {
                                let point = {};
                                point.x = this.points[i].point.x; // Just .x instead of point.x returns the category
                                point.y = this.points[i].y;
                                point.z = this.points[i].z;
                                point.category = this.points[i].key;
                                point.color = this.points[i].color;
                                point.percentage = this.points[i].percentage;
                                point.total = this.points[i].total;
                                point.point_index = this.points[i].index;
                                point.series_name = this.points[i].series.name;
                                point.series_index = this.points[i].series.index;
                                point_array.push(point);
                            }
                            var e = {
                                event_type: 'tooltip',
                                x: this.x,
                                id: id,
                                points: point_array,
                                page_id: page_id,
                                websocket_id: websocket_id
                            };
                        }

                        if (use_websockets) {
                            // Wait tooltip_timeout_period before sending tooltip information to server.
                            // This allows new tooltip event delete old one if it arrives less than 100ms
                            // after the previous one. Basically, a debouncing of the tooltip event
                            clearTimeout(tooltip_timeout);
                            tooltip_timeout = setTimeout(function () {
                                    //socket.send(JSON.stringify({'type': 'event', 'event_data': e}));
                                    send_to_server(e, 'event');
                                }
                                , tooltip_timeout_period);
                        }
                        point_array = [];
                        if (tooltip.split) {
                            var return_array = [];
                            for (var i = 0; i < tooltip.chart.series.length + 1; i++) {
                                return_array.push('Loading...');
                            }
                            return return_array;
                        } else return 'Loading...';
                    },
                }
            }
            update_dict.plotOptions = {
                series: {
                    cursor: 'pointer',
                    events: {},
                    point: {
                        events: {}
                    }
                }
            };
            if (this.$props.jp_props.events.indexOf('point_click') >= 0) {
                update_dict.plotOptions.series.point.events.click = function (e) {
                    var p = {
                        event_type: 'point_click',
                        id: id,
                        x: e.point.x,
                        y: e.point.y,
                        z: e.point.z,
                        category: e.point.category,
                        color: e.point.color,
                        percentage: e.point.percentage,
                        total: e.point.total,
                        point_index: e.point.index,
                        type: e.type,
                        series_name: e.point.series.name,
                        series_index: e.point.series.index,
                        page_id: page_id,
                        websocket_id: websocket_id
                    };
                    send_to_server(p, 'event');
                }
            }

            if (this.$props.jp_props.events.indexOf('point_select') >= 0) {
                update_dict.plotOptions.series.point.events.select = function (e) {
                    var p = {
                        event_type: 'point_select',
                        id: id,
                        x: e.target.x,
                        y: e.target.y,
                        z: e.target.z,
                        accumulate: e.accumulate,
                        category: e.target.category,
                        color: e.target.color,
                        percentage: e.target.percentage,
                        total: e.target.total,
                        point_index: e.target.index,
                        type: e.type,
                        series_name: e.target.series.name,
                        series_index: e.target.series.index,
                        page_id: page_id,
                        websocket_id: websocket_id
                    };
                    var selectedPoints = this.series.chart.getSelectedPoints();
                    var selected_points = [];
                    for (let i = 0; i < selectedPoints.length; i++) {
                        let point = selectedPoints[i];
                        selected_points.push({
                            x: point.x,
                            y: point.y,
                            z: point.z,
                            category: point.category,
                            color: point.color,
                            percentage: point.percentage,
                            total: point.total,
                            point_index: point.index,
                            series_name: point.series.name,
                            series_index: point.series.index
                        })
                    }
                    p.selected_points = selected_points;
                    send_to_server(p, 'event');
                }
            }

            if (this.$props.jp_props.events.indexOf('point_unselect') >= 0) {
                update_dict.plotOptions.series.point.events.unselect = function (e) {
                    var p = {
                        event_type: 'point_unselect',
                        id: id,
                        x: e.target.x,
                        y: e.target.y,
                        z: e.target.z,
                        accumulate: e.accumulate,
                        category: e.target.category,
                        color: e.target.color,
                        percentage: e.target.percentage,
                        total: e.target.total,
                        point_index: e.target.index,
                        type: e.type,
                        series_name: e.target.series.name,
                        series_index: e.target.series.index,
                        page_id: page_id,
                        websocket_id: websocket_id
                    };
                    var selectedPoints = this.series.chart.getSelectedPoints();
                    var selected_points = [];
                    for (let i = 0; i < selectedPoints.length; i++) {
                        let point = selectedPoints[i];
                        selected_points.push({
                            x: point.x,
                            y: point.y,
                            z: point.z,
                            category: point.category,
                            color: point.color,
                            percentage: point.percentage,
                            total: point.total,
                            point_index: point.index,
                            series_name: point.series.name,
                            series_index: point.series.index
                        })
                    }
                    p.selected_points = selected_points;
                    send_to_server(p, 'event');
                }
            }

            if (this.$props.jp_props.events.indexOf('series_hide') >= 0) {
                update_dict.plotOptions.series.events.hide = function (e) {
                    var p = {
                        event_type: 'series_hide',
                        id: id,
                        color: e.target.color,
                        type: e.type,
                        series_name: e.target.name,
                        series_index: e.target.index,
                        page_id: page_id,
                        websocket_id: websocket_id
                    };
                    send_to_server(p, 'event');
                }
            }

            if (this.$props.jp_props.events.indexOf('series_show') >= 0) {
                update_dict.plotOptions.series.events.show = function (e) {
                    var p = {
                        event_type: 'series_show',
                        id: id,
                        color: e.target.color,
                        type: e.type,
                        series_name: e.target.name,
                        series_index: e.target.index,
                        page_id: page_id,
                        websocket_id: websocket_id
                    };
                    send_to_server(p, 'event');
                }

            }
            if (this.$props.jp_props.events.indexOf('series_click') >= 0) {
                update_dict.plotOptions.series.events.click = function (e) {
                    var p = {
                        event_type: 'series_click',
                        id: id,
                        type: e.type,
                        x: e.point.x,
                        y: e.point.y,
                        z: e.point.z,
                        category: e.point.category,
                        color: e.point.color,
                        percentage: e.point.percentage,
                        total: e.point.total,
                        point_index: e.point.index,
                        series_name: e.point.series.name,
                        series_index: e.point.series.index,
                        page_id: page_id,
                        websocket_id: websocket_id
                    };
                    send_to_server(p, 'event');
                }
            }

            if (this.$props.jp_props.events.indexOf('zoom_x') >= 0) {
                update_dict.xAxis = {
                    events: {}
                };
                update_dict.xAxis.events.setExtremes = function (e) {
                    var p = {
                        event_type: 'zoom_x',
                        id: id,
                        type: e.type,
                        min: e.min,
                        max: e.max,
                        page_id: page_id,
                        websocket_id: websocket_id
                    };
                    send_to_server(p, 'event');
                }
            }
            if (this.$props.jp_props.events.indexOf('zoom_y') >= 0) {
                update_dict.yAxis = {
                    events: {}
                };
                update_dict.yAxis.events.setExtremes = function (e) {
                    var p = {
                        event_type: 'zoom_y',
                        id: id,
                        type: e.type,
                        min: e.min,
                        max: e.max,
                        page_id: page_id,
                        websocket_id: websocket_id
                    };
                    send_to_server(p, 'event');
                }
            }

            c.update(update_dict);
        }
    },
    mounted() {
        this.graph_change();
    },
    updated() {
        const container = this.$props.jp_props.id.toString();
        const chart = cached_graph_def['chart' + container];
        if (!this.$props.jp_props.use_cache || (JSON.stringify(this.$props.jp_props.def) != cached_graph_def[this.$props.jp_props.id])) {
            cached_graph_def[this.$props.jp_props.id] = JSON.stringify(this.$props.jp_props.def);
            if (this.$props.jp_props.update_create) {
                this.graph_change();
            } else {
                chart.update(this.$props.jp_props.def, true, true, this.$props.jp_props.update_animation);
            }
        }
    },
    props: {
        jp_props: Object
    }
});

//   {% endraw %}

