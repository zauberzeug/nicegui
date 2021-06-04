(function() {
    var a, b, c, d, e, f, g;
    a = jQuery, e = "highcharts-themes", g = {}, b = {
        base: ["#dd7722", "#2288cc", "#dd3322", "#22aa99", "#bb4488", "#ddaa00", "#6655cc", "#99aa00"],
        pastel: ["#E6645C", "#55A9DC", "#886DB3", "#6CC080"],
        steel: ["#484D59", "#aaaaaa", "#4295F3"],
        future: ["#E6645C", "#55A9DC", "#886DB3", "#6CC080"]
    }, c = {
        base: {
            enabled: !0,
            lineWidth: 1,
            radius: 2,
            fillColor: "#FFFFFF",
            lineColor: null,
            symbol: "circle",
            states: {
                hover: {
                    enabled: !1,
                    radius: 1,
                    lineWidth: 5
                }
            }
        },
        pastel: {
            enabled: !0,
            lineWidth: 3,
            radius: 5,
            fillColor: null,
            lineColor: "#FFFFFF",
            symbol: "circle",
            states: {
                hover: {
                    lineWidth: 5,
                    radius: 7
                }
            }
        },
        steel: {
            enabled: !0,
            lineWidth: 2,
            radius: 5,
            fillColor: "#FFFFFF",
            lineColor: null,
            symbol: "circle",
            states: {
                hover: {
                    lineWidth: 3,
                    radius: 6
                }
            }
        },
        future: {
            enabled: !0,
            lineWidth: 8,
            radius: 5,
            fillColor: null,
            lineColor: "rgba(0, 0, 0, 0.15)",
            symbol: "circle",
            states: {
                hover: {
                    lineWidth: 0,
                    radius: 10
                }
            }
        }
    }, g.pastel = {
        colors: b.pastel,
        plotOptions: {
            line: {
                lineWidth: 3,
                marker: c.pastel
            },
            bar: {
                pointWidth: 1
            },
            column: {
                pointWidth: 1
            },
            scatter: {
                marker: c.pastel
            }
        }
    }, g.steel = {
        colors: b.steel,
        plotOptions: {
            line: {
                marker: c.steel
            },
            bar: {
                pointWidth: 1
            },
            column: {
                pointWidth: 1
            },
            scatter: {
                marker: c.steel
            }
        }
    }, g.future = {
        colors: b.future,
        plotOptions: {
            line: {
                marker: c.future
            },
            bar: {
                pointWidth: 1
            },
            column: {
                pointWidth: 1
            },
            scatter: {
                marker: c.future
            }
        }
    }, g._defaults = {
        chart: {
            style: {
                fontFamily: "Helvetica",
                fontWeight: "normal"
            }
        },
        xAxis: {
            lineColor: "#ccc"
        },
        yAxis: {
            gridLineColor: "#e0e0e0"
        },
        credits: !1,
        legend: {
            borderRadius: 0,
            borderWidth: 0,
            align: "center",
            x: 15
        }
    };
    for (d in g) f = g[d], "_defaults" !== d && a.extend(!0, f, g._defaults);
    a.fn[e] = Highcharts.themes = g, Highcharts.setTheme = function(a) {
        var b;
        return (b = null != Highcharts[a]) ? Highcharts.setOptions(b) : console.warn("Found no such theme.")
    }
}).call(this);