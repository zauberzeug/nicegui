/**
 * @license Highcharts JS v10.3.2 (2022-11-28)
 *
 * ColorAxis module
 *
 * (c) 2012-2021 Pawel Potaczek
 *
 * License: www.highcharts.com/license
 */
(function (factory) {
    if (typeof module === 'object' && module.exports) {
        factory['default'] = factory;
        module.exports = factory;
    } else if (typeof define === 'function' && define.amd) {
        define('highcharts/modules/color-axis', ['highcharts'], function (Highcharts) {
            factory(Highcharts);
            factory.Highcharts = Highcharts;
            return factory;
        });
    } else {
        factory(typeof Highcharts !== 'undefined' ? Highcharts : undefined);
    }
}(function (Highcharts) {
    'use strict';
    var _modules = Highcharts ? Highcharts._modules : {};
    function _registerModule(obj, path, args, fn) {
        if (!obj.hasOwnProperty(path)) {
            obj[path] = fn.apply(null, args);

            if (typeof CustomEvent === 'function') {
                window.dispatchEvent(
                    new CustomEvent(
                        'HighchartsModuleLoaded',
                        { detail: { path: path, module: obj[path] }
                    })
                );
            }
        }
    }
    _registerModule(_modules, 'Core/Axis/Color/ColorAxisComposition.js', [_modules['Core/Color/Color.js'], _modules['Core/Utilities.js']], function (Color, U) {
        /* *
         *
         *  (c) 2010-2021 Torstein Honsi
         *
         *  License: www.highcharts.com/license
         *
         *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
         *
         * */
        var color = Color.parse;
        var addEvent = U.addEvent,
            extend = U.extend,
            merge = U.merge,
            pick = U.pick,
            splat = U.splat;
        /* *
         *
         *  Composition
         *
         * */
        var ColorAxisComposition;
        (function (ColorAxisComposition) {
            /* *
             *
             *  Declarations
             *
             * */
            /* *
             *
             *  Constants
             *
             * */
            var composedClasses = [];
            /* *
             *
             *  Variables
             *
             * */
            var ColorAxisClass;
            /* *
             *
             *  Functions
             *
             * */
            /* eslint-disable valid-jsdoc */
            /**
             * @private
             */
            function compose(ColorAxisType, ChartClass, FxClass, LegendClass, SeriesClass) {
                if (!ColorAxisClass) {
                    ColorAxisClass = ColorAxisType;
                }
                if (composedClasses.indexOf(ChartClass) === -1) {
                    composedClasses.push(ChartClass);
                    var chartProto = ChartClass.prototype;
                    chartProto.collectionsWithUpdate.push('colorAxis');
                    chartProto.collectionsWithInit.colorAxis = [
                        chartProto.addColorAxis
                    ];
                    addEvent(ChartClass, 'afterGetAxes', onChartAfterGetAxes);
                    wrapChartCreateAxis(ChartClass);
                }
                if (composedClasses.indexOf(FxClass) === -1) {
                    composedClasses.push(FxClass);
                    var fxProto = FxClass.prototype;
                    fxProto.fillSetter = wrapFxFillSetter;
                    fxProto.strokeSetter = wrapFxStrokeSetter;
                }
                if (composedClasses.indexOf(LegendClass) === -1) {
                    composedClasses.push(LegendClass);
                    addEvent(LegendClass, 'afterGetAllItems', onLegendAfterGetAllItems);
                    addEvent(LegendClass, 'afterColorizeItem', onLegendAfterColorizeItem);
                    addEvent(LegendClass, 'afterUpdate', onLegendAfterUpdate);
                }
                if (composedClasses.indexOf(SeriesClass) === -1) {
                    composedClasses.push(SeriesClass);
                    extend(SeriesClass.prototype, {
                        optionalAxis: 'colorAxis',
                        translateColors: seriesTranslateColors
                    });
                    extend(SeriesClass.prototype.pointClass.prototype, {
                        setVisible: pointSetVisible
                    });
                    addEvent(SeriesClass, 'afterTranslate', onSeriesAfterTranslate);
                    addEvent(SeriesClass, 'bindAxes', onSeriesBindAxes);
                }
            }
            ColorAxisComposition.compose = compose;
            /**
             * Extend the chart getAxes method to also get the color axis.
             * @private
             */
            function onChartAfterGetAxes() {
                var _this = this;
                var options = this.options;
                this.colorAxis = [];
                if (options.colorAxis) {
                    options.colorAxis = splat(options.colorAxis);
                    options.colorAxis.forEach(function (axisOptions, i) {
                        axisOptions.index = i;
                        new ColorAxisClass(_this, axisOptions); // eslint-disable-line no-new
                    });
                }
            }
            /**
             * Add the color axis. This also removes the axis' own series to prevent
             * them from showing up individually.
             * @private
             */
            function onLegendAfterGetAllItems(e) {
                var _this = this;
                var colorAxes = this.chart.colorAxis || [],
                    destroyItem = function (item) {
                        var i = e.allItems.indexOf(item);
                    if (i !== -1) {
                        // #15436
                        _this.destroyItem(e.allItems[i]);
                        e.allItems.splice(i, 1);
                    }
                };
                var colorAxisItems = [],
                    options,
                    i;
                colorAxes.forEach(function (colorAxis) {
                    options = colorAxis.options;
                    if (options && options.showInLegend) {
                        // Data classes
                        if (options.dataClasses && options.visible) {
                            colorAxisItems = colorAxisItems.concat(colorAxis.getDataClassLegendSymbols());
                            // Gradient legend
                        }
                        else if (options.visible) {
                            // Add this axis on top
                            colorAxisItems.push(colorAxis);
                        }
                        // If dataClasses are defined or showInLegend option is not set
                        // to true, do not add color axis' series to legend.
                        colorAxis.series.forEach(function (series) {
                            if (!series.options.showInLegend || options.dataClasses) {
                                if (series.options.legendType === 'point') {
                                    series.points.forEach(function (point) {
                                        destroyItem(point);
                                    });
                                }
                                else {
                                    destroyItem(series);
                                }
                            }
                        });
                    }
                });
                i = colorAxisItems.length;
                while (i--) {
                    e.allItems.unshift(colorAxisItems[i]);
                }
            }
            /**
             * @private
             */
            function onLegendAfterColorizeItem(e) {
                if (e.visible && e.item.legendColor) {
                    e.item.legendItem.symbol.attr({
                        fill: e.item.legendColor
                    });
                }
            }
            /**
             * Updates in the legend need to be reflected in the color axis. (#6888)
             * @private
             */
            function onLegendAfterUpdate() {
                var colorAxes = this.chart.colorAxis;
                if (colorAxes) {
                    colorAxes.forEach(function (colorAxis) {
                        colorAxis.update({}, arguments[2]);
                    });
                }
            }
            /**
             * Calculate and set colors for points.
             * @private
             */
            function onSeriesAfterTranslate() {
                if (this.chart.colorAxis &&
                    this.chart.colorAxis.length ||
                    this.colorAttribs) {
                    this.translateColors();
                }
            }
            /**
             * Add colorAxis to series axisTypes.
             * @private
             */
            function onSeriesBindAxes() {
                var axisTypes = this.axisTypes;
                if (!axisTypes) {
                    this.axisTypes = ['colorAxis'];
                }
                else if (axisTypes.indexOf('colorAxis') === -1) {
                    axisTypes.push('colorAxis');
                }
            }
            /**
             * Set the visibility of a single point
             * @private
             * @function Highcharts.colorPointMixin.setVisible
             * @param {boolean} visible
             */
            function pointSetVisible(vis) {
                var point = this,
                    method = vis ? 'show' : 'hide';
                point.visible = point.options.visible = Boolean(vis);
                // Show and hide associated elements
                ['graphic', 'dataLabel'].forEach(function (key) {
                    if (point[key]) {
                        point[key][method]();
                    }
                });
                this.series.buildKDTree(); // rebuild kdtree #13195
            }
            ColorAxisComposition.pointSetVisible = pointSetVisible;
            /**
             * In choropleth maps, the color is a result of the value, so this needs
             * translation too
             * @private
             * @function Highcharts.colorSeriesMixin.translateColors
             */
            function seriesTranslateColors() {
                var series = this,
                    points = this.data.length ? this.data : this.points,
                    nullColor = this.options.nullColor,
                    colorAxis = this.colorAxis,
                    colorKey = this.colorKey;
                points.forEach(function (point) {
                    var value = point.getNestedProperty(colorKey),
                        color = point.options.color || (point.isNull || point.value === null ?
                            nullColor :
                            (colorAxis && typeof value !== 'undefined') ?
                                colorAxis.toColor(value,
                        point) :
                                point.color || series.color);
                    if (color && point.color !== color) {
                        point.color = color;
                        if (series.options.legendType === 'point' &&
                            point.legendItem &&
                            point.legendItem.label) {
                            series.chart.legend.colorizeItem(point, point.visible);
                        }
                    }
                });
            }
            /**
             * @private
             */
            function wrapChartCreateAxis(ChartClass) {
                var superCreateAxis = ChartClass.prototype.createAxis;
                ChartClass.prototype.createAxis = function (type, options) {
                    if (type !== 'colorAxis') {
                        return superCreateAxis.apply(this, arguments);
                    }
                    var axis = new ColorAxisClass(this,
                        merge(options.axis, {
                            index: this[type].length,
                            isX: false
                        }));
                    this.isDirtyLegend = true;
                    // Clear before 'bindAxes' (#11924)
                    this.axes.forEach(function (axis) {
                        axis.series = [];
                    });
                    this.series.forEach(function (series) {
                        series.bindAxes();
                        series.isDirtyData = true;
                    });
                    if (pick(options.redraw, true)) {
                        this.redraw(options.animation);
                    }
                    return axis;
                };
            }
            /**
             * Handle animation of the color attributes directly.
             * @private
             */
            function wrapFxFillSetter() {
                this.elem.attr('fill', color(this.start).tweenTo(color(this.end), this.pos), void 0, true);
            }
            /**
             * Handle animation of the color attributes directly.
             * @private
             */
            function wrapFxStrokeSetter() {
                this.elem.attr('stroke', color(this.start).tweenTo(color(this.end), this.pos), void 0, true);
            }
        })(ColorAxisComposition || (ColorAxisComposition = {}));
        /* *
         *
         *  Default Export
         *
         * */

        return ColorAxisComposition;
    });
    _registerModule(_modules, 'Core/Axis/Color/ColorAxisDefaults.js', [], function () {
        /* *
         *
         *  (c) 2010-2021 Torstein Honsi
         *
         *  License: www.highcharts.com/license
         *
         *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
         *
         * */
        /* *
         *
         *  API Options
         *
         * */
        /**
         * A color axis for series. Visually, the color
         * axis will appear as a gradient or as separate items inside the
         * legend, depending on whether the axis is scalar or based on data
         * classes.
         *
         * For supported color formats, see the
         * [docs article about colors](https://www.highcharts.com/docs/chart-design-and-style/colors).
         *
         * A scalar color axis is represented by a gradient. The colors either
         * range between the [minColor](#colorAxis.minColor) and the
         * [maxColor](#colorAxis.maxColor), or for more fine grained control the
         * colors can be defined in [stops](#colorAxis.stops). Often times, the
         * color axis needs to be adjusted to get the right color spread for the
         * data. In addition to stops, consider using a logarithmic
         * [axis type](#colorAxis.type), or setting [min](#colorAxis.min) and
         * [max](#colorAxis.max) to avoid the colors being determined by
         * outliers.
         *
         * When [dataClasses](#colorAxis.dataClasses) are used, the ranges are
         * subdivided into separate classes like categories based on their
         * values. This can be used for ranges between two values, but also for
         * a true category. However, when your data is categorized, it may be as
         * convenient to add each category to a separate series.
         *
         * Color axis does not work with: `sankey`, `sunburst`, `dependencywheel`,
         * `networkgraph`, `wordcloud`, `venn`, `gauge` and `solidgauge` series
         * types.
         *
         * Since v7.2.0 `colorAxis` can also be an array of options objects.
         *
         * See [the Axis object](/class-reference/Highcharts.Axis) for
         * programmatic access to the axis.
         *
         * @sample       {highcharts} highcharts/coloraxis/custom-color-key
         *               Column chart with color axis
         * @sample       {highcharts} highcharts/coloraxis/horizontal-layout
         *               Horizontal layout
         * @sample       {highmaps} maps/coloraxis/dataclasscolor
         *               With data classes
         * @sample       {highmaps} maps/coloraxis/mincolor-maxcolor
         *               Min color and max color
         *
         * @extends      xAxis
         * @excluding    alignTicks, allowDecimals, alternateGridColor, breaks,
         *               categories, crosshair, dateTimeLabelFormats, height, left,
         *               lineWidth, linkedTo, maxZoom, minRange, minTickInterval,
         *               offset, opposite, pane, plotBands, plotLines,
         *               reversedStacks, scrollbar, showEmpty, title, top, width,
         *               zoomEnabled
         * @product      highcharts highstock highmaps
         * @type         {*|Array<*>}
         * @optionparent colorAxis
         */
        var colorAxisDefaults = {
                /**
                 * Whether to allow decimals on the color axis.
                 * @type      {boolean}
                 * @default   true
                 * @product   highcharts highstock highmaps
                 * @apioption colorAxis.allowDecimals
                 */
                /**
                 * Determines how to set each data class' color if no individual
                 * color is set. The default value, `tween`, computes intermediate
                 * colors between `minColor` and `maxColor`. The other possible
                 * value, `category`, pulls colors from the global or chart specific
                 * [colors](#colors) array.
                 *
                 * @sample {highmaps} maps/coloraxis/dataclasscolor/
                 *         Category colors
                 *
                 * @type       {string}
                 * @default    tween
                 * @product    highcharts highstock highmaps
                 * @validvalue ["tween", "category"]
                 * @apioption  colorAxis.dataClassColor
                 */
                /**
                 * An array of data classes or ranges for the choropleth map. If
                 * none given, the color axis is scalar and values are distributed
                 * as a gradient between the minimum and maximum colors.
                 *
                 * @sample {highmaps} maps/demo/data-class-ranges/
                 *         Multiple ranges
                 *
                 * @sample {highmaps} maps/demo/data-class-two-ranges/
                 *         Two ranges
                 *
                 * @type      {Array<*>}
                 * @product   highcharts highstock highmaps
                 * @apioption colorAxis.dataClasses
                 */
                /**
                 * The layout of the color axis. Can be `'horizontal'` or `'vertical'`.
                 * If none given, the color axis has the same layout as the legend.
                 *
                 * @sample highcharts/coloraxis/horizontal-layout/
                 *         Horizontal color axis layout with vertical legend
                 *
                 * @type      {string|undefined}
                 * @since     7.2.0
                 * @product   highcharts highstock highmaps
                 * @apioption colorAxis.layout
                 */
                /**
                 * The color of each data class. If not set, the color is pulled
                 * from the global or chart-specific [colors](#colors) array. In
                 * styled mode, this option is ignored. Instead, use colors defined
                 * in CSS.
                 *
                 * @sample {highmaps} maps/demo/data-class-two-ranges/
                 *         Explicit colors
                 *
                 * @type      {Highcharts.ColorString|Highcharts.GradientColorObject|Highcharts.PatternObject}
                 * @product   highcharts highstock highmaps
                 * @apioption colorAxis.dataClasses.color
                 */
                /**
                 * The start of the value range that the data class represents,
                 * relating to the point value.
                 *
                 * The range of each `dataClass` is closed in both ends, but can be
                 * overridden by the next `dataClass`.
                 *
                 * @type      {number}
                 * @product   highcharts highstock highmaps
                 * @apioption colorAxis.dataClasses.from
                 */
                /**
                 * The name of the data class as it appears in the legend.
                 * If no name is given, it is automatically created based on the
                 * `from` and `to` values. For full programmatic control,
                 * [legend.labelFormatter](#legend.labelFormatter) can be used.
                 * In the formatter, `this.from` and `this.to` can be accessed.
                 *
                 * @sample {highmaps} maps/coloraxis/dataclasses-name/
                 *         Named data classes
                 *
                 * @sample {highmaps} maps/coloraxis/dataclasses-labelformatter/
                 *         Formatted data classes
                 *
                 * @type      {string}
                 * @product   highcharts highstock highmaps
                 * @apioption colorAxis.dataClasses.name
                 */
                /**
                 * The end of the value range that the data class represents,
                 * relating to the point value.
                 *
                 * The range of each `dataClass` is closed in both ends, but can be
                 * overridden by the next `dataClass`.
                 *
                 * @type      {number}
                 * @product   highcharts highstock highmaps
                 * @apioption colorAxis.dataClasses.to
                 */
                /** @ignore-option */
                lineWidth: 0,
                /**
                 * Padding of the min value relative to the length of the axis. A
                 * padding of 0.05 will make a 100px axis 5px longer.
                 *
                 * @product highcharts highstock highmaps
                 */
                minPadding: 0,
                /**
                 * The maximum value of the axis in terms of map point values. If
                 * `null`, the max value is automatically calculated. If the
                 * `endOnTick` option is true, the max value might be rounded up.
                 *
                 * @sample {highmaps} maps/coloraxis/gridlines/
                 *         Explicit min and max to reduce the effect of outliers
                 *
                 * @type      {number}
                 * @product   highcharts highstock highmaps
                 * @apioption colorAxis.max
                 */
                /**
                 * The minimum value of the axis in terms of map point values. If
                 * `null`, the min value is automatically calculated. If the
                 * `startOnTick` option is true, the min value might be rounded
                 * down.
                 *
                 * @sample {highmaps} maps/coloraxis/gridlines/
                 *         Explicit min and max to reduce the effect of outliers
                 *
                 * @type      {number}
                 * @product   highcharts highstock highmaps
                 * @apioption colorAxis.min
                 */
                /**
                 * Padding of the max value relative to the length of the axis. A
                 * padding of 0.05 will make a 100px axis 5px longer.
                 *
                 * @product highcharts highstock highmaps
                 */
                maxPadding: 0,
                /**
                 * Color of the grid lines extending from the axis across the
                 * gradient.
                 *
                 * @sample {highmaps} maps/coloraxis/gridlines/
                 *         Grid lines demonstrated
                 *
                 * @type      {Highcharts.ColorString|Highcharts.GradientColorObject|Highcharts.PatternObject}
                 * @default   #e6e6e6
                 * @product   highcharts highstock highmaps
                 * @apioption colorAxis.gridLineColor
                 */
                /**
                 * The width of the grid lines extending from the axis across the
                 * gradient of a scalar color axis.
                 *
                 * @sample {highmaps} maps/coloraxis/gridlines/
                 *         Grid lines demonstrated
                 *
                 * @product highcharts highstock highmaps
                 */
                gridLineWidth: 1,
                /**
                 * The interval of the tick marks in axis units. When `null`, the
                 * tick interval is computed to approximately follow the
                 * `tickPixelInterval`.
                 *
                 * @type      {number}
                 * @product   highcharts highstock highmaps
                 * @apioption colorAxis.tickInterval
                 */
                /**
                 * If [tickInterval](#colorAxis.tickInterval) is `null` this option
                 * sets the approximate pixel interval of the tick marks.
                 *
                 * @product highcharts highstock highmaps
                 */
                tickPixelInterval: 72,
                /**
                 * Whether to force the axis to start on a tick. Use this option
                 * with the `maxPadding` option to control the axis start.
                 *
                 * @product highcharts highstock highmaps
                 */
                startOnTick: true,
                /**
                 * Whether to force the axis to end on a tick. Use this option with
                 * the [maxPadding](#colorAxis.maxPadding) option to control the
                 * axis end.
                 *
                 * @product highcharts highstock highmaps
                 */
                endOnTick: true,
                /** @ignore */
                offset: 0,
                /**
                 * The triangular marker on a scalar color axis that points to the
                 * value of the hovered area. To disable the marker, set
                 * `marker: null`.
                 *
                 * @sample {highmaps} maps/coloraxis/marker/
                 *         Black marker
                 *
                 * @declare Highcharts.PointMarkerOptionsObject
                 * @product highcharts highstock highmaps
                 */
                marker: {
                    /**
                     * Animation for the marker as it moves between values. Set to
                     * `false` to disable animation. Defaults to `{ duration: 50 }`.
                     *
                     * @type    {boolean|Partial<Highcharts.AnimationOptionsObject>}
                     * @product highcharts highstock highmaps
                     */
                    animation: {
                        /** @internal */
                        duration: 50
                    },
                    /** @internal */
                    width: 0.01,
                    /**
                     * The color of the marker.
                     *
                     * @type    {Highcharts.ColorString|Highcharts.GradientColorObject|Highcharts.PatternObject}
                     * @product highcharts highstock highmaps
                     */
                    color: "#999999" /* Palette.neutralColor40 */
                },
                /**
                 * The axis labels show the number for each tick.
                 *
                 * For more live examples on label options, see [xAxis.labels in the
                 * Highcharts API.](/highcharts#xAxis.labels)
                 *
                 * @extends xAxis.labels
                 * @product highcharts highstock highmaps
                 */
                labels: {
                    /**
                     * How to handle overflowing labels on horizontal color axis. If set
                     * to `"allow"`, it will not be aligned at all. By default it
                     * `"justify"` labels inside the chart area. If there is room to
                     * move it, it will be aligned to the edge, else it will be removed.
                     *
                     * @validvalue ["allow", "justify"]
                     * @product    highcharts highstock highmaps
                     */
                    overflow: 'justify',
                    rotation: 0
                },
                /**
                 * The color to represent the minimum of the color axis. Unless
                 * [dataClasses](#colorAxis.dataClasses) or
                 * [stops](#colorAxis.stops) are set, the gradient starts at this
                 * value.
                 *
                 * If dataClasses are set, the color is based on minColor and
                 * maxColor unless a color is set for each data class, or the
                 * [dataClassColor](#colorAxis.dataClassColor) is set.
                 *
                 * @sample {highmaps} maps/coloraxis/mincolor-maxcolor/
                 *         Min and max colors on scalar (gradient) axis
                 * @sample {highmaps} maps/coloraxis/mincolor-maxcolor-dataclasses/
                 *         On data classes
                 *
                 * @type    {Highcharts.ColorString|Highcharts.GradientColorObject|Highcharts.PatternObject}
                 * @product highcharts highstock highmaps
                 */
                minColor: "#e6ebf5" /* Palette.highlightColor10 */,
                /**
                 * The color to represent the maximum of the color axis. Unless
                 * [dataClasses](#colorAxis.dataClasses) or
                 * [stops](#colorAxis.stops) are set, the gradient ends at this
                 * value.
                 *
                 * If dataClasses are set, the color is based on minColor and
                 * maxColor unless a color is set for each data class, or the
                 * [dataClassColor](#colorAxis.dataClassColor) is set.
                 *
                 * @sample {highmaps} maps/coloraxis/mincolor-maxcolor/
                 *         Min and max colors on scalar (gradient) axis
                 * @sample {highmaps} maps/coloraxis/mincolor-maxcolor-dataclasses/
                 *         On data classes
                 *
                 * @type    {Highcharts.ColorString|Highcharts.GradientColorObject|Highcharts.PatternObject}
                 * @product highcharts highstock highmaps
                 */
                maxColor: "#003399" /* Palette.highlightColor100 */,
                /**
                 * Color stops for the gradient of a scalar color axis. Use this in
                 * cases where a linear gradient between a `minColor` and `maxColor`
                 * is not sufficient. The stops is an array of tuples, where the
                 * first item is a float between 0 and 1 assigning the relative
                 * position in the gradient, and the second item is the color.
                 *
                 * @sample highcharts/coloraxis/coloraxis-stops/
                 *         Color axis stops
                 * @sample highcharts/coloraxis/color-key-with-stops/
                 *         Color axis stops with custom colorKey
                 * @sample {highmaps} maps/demo/heatmap/
                 *         Heatmap with three color stops
                 *
                 * @type      {Array<Array<number,Highcharts.ColorString>>}
                 * @product   highcharts highstock highmaps
                 * @apioption colorAxis.stops
                 */
                /**
                 * The pixel length of the main tick marks on the color axis.
                 */
                tickLength: 5,
                /**
                 * The type of interpolation to use for the color axis. Can be
                 * `linear` or `logarithmic`.
                 *
                 * @sample highcharts/coloraxis/logarithmic-with-emulate-negative-values/
                 *         Logarithmic color axis with extension to emulate negative
                 *         values
                 *
                 * @type      {Highcharts.ColorAxisTypeValue}
                 * @default   linear
                 * @product   highcharts highstock highmaps
                 * @apioption colorAxis.type
                 */
                /**
                 * Whether to reverse the axis so that the highest number is closest
                 * to the origin. Defaults to `false` in a horizontal legend and
                 * `true` in a vertical legend, where the smallest value starts on
                 * top.
                 *
                 * @type      {boolean}
                 * @product   highcharts highstock highmaps
                 * @apioption colorAxis.reversed
                 */
                /**
                 * @product   highcharts highstock highmaps
                 * @excluding afterBreaks, pointBreak, pointInBreak
                 * @apioption colorAxis.events
                 */
                /**
                 * Fires when the legend item belonging to the colorAxis is clicked.
                 * One parameter, `event`, is passed to the function.
                 *
                 * @type      {Function}
                 * @product   highcharts highstock highmaps
                 * @apioption colorAxis.events.legendItemClick
                 */
                /**
                 * Whether to display the colorAxis in the legend.
                 *
                 * @sample highcharts/coloraxis/hidden-coloraxis-with-3d-chart/
                 *         Hidden color axis with 3d chart
                 *
                 * @see [heatmap.showInLegend](#series.heatmap.showInLegend)
                 *
                 * @since   4.2.7
                 * @product highcharts highstock highmaps
                 */
                showInLegend: true
            };
        /* *
         *
         *  Default Export
         *
         * */

        return colorAxisDefaults;
    });
    _registerModule(_modules, 'Core/Axis/Color/ColorAxis.js', [_modules['Core/Axis/Axis.js'], _modules['Core/Color/Color.js'], _modules['Core/Axis/Color/ColorAxisComposition.js'], _modules['Core/Axis/Color/ColorAxisDefaults.js'], _modules['Core/Globals.js'], _modules['Core/Legend/LegendSymbol.js'], _modules['Core/Series/SeriesRegistry.js'], _modules['Core/Utilities.js']], function (Axis, Color, ColorAxisComposition, ColorAxisDefaults, H, LegendSymbol, SeriesRegistry, U) {
        /* *
         *
         *  (c) 2010-2021 Torstein Honsi
         *
         *  License: www.highcharts.com/license
         *
         *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
         *
         * */
        var __extends = (this && this.__extends) || (function () {
                var extendStatics = function (d,
            b) {
                    extendStatics = Object.setPrototypeOf ||
                        ({ __proto__: [] } instanceof Array && function (d,
            b) { d.__proto__ = b; }) ||
                        function (d,
            b) { for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p]; };
                return extendStatics(d, b);
            };
            return function (d, b) {
                extendStatics(d, b);
                function __() { this.constructor = d; }
                d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
            };
        })();
        var color = Color.parse;
        var noop = H.noop;
        var Series = SeriesRegistry.series;
        var extend = U.extend,
            isNumber = U.isNumber,
            merge = U.merge,
            pick = U.pick;
        /* *
         *
         *  Class
         *
         * */
        /* eslint-disable no-invalid-this, valid-jsdoc */
        /**
         * The ColorAxis object for inclusion in gradient legends.
         *
         * @class
         * @name Highcharts.ColorAxis
         * @augments Highcharts.Axis
         *
         * @param {Highcharts.Chart} chart
         * The related chart of the color axis.
         *
         * @param {Highcharts.ColorAxisOptions} userOptions
         * The color axis options for initialization.
         */
        var ColorAxis = /** @class */ (function (_super) {
                __extends(ColorAxis, _super);
            /* *
             *
             *  Constructors
             *
             * */
            /**
             * @private
             */
            function ColorAxis(chart, userOptions) {
                var _this = _super.call(this,
                    chart,
                    userOptions) || this;
                // Prevents unnecessary padding with `hc-more`
                _this.beforePadding = false;
                _this.chart = void 0;
                _this.coll = 'colorAxis';
                _this.dataClasses = void 0;
                _this.name = ''; // Prevents 'undefined' in legend in IE8
                _this.options = void 0;
                _this.stops = void 0;
                _this.visible = true;
                _this.init(chart, userOptions);
                return _this;
            }
            /* *
             *
             *  Static Functions
             *
             * */
            ColorAxis.compose = function (ChartClass, FxClass, LegendClass, SeriesClass) {
                ColorAxisComposition.compose(ColorAxis, ChartClass, FxClass, LegendClass, SeriesClass);
            };
            /* *
             *
             *  Functions
             *
             * */
            /**
             * Initializes the color axis.
             *
             * @function Highcharts.ColorAxis#init
             *
             * @param {Highcharts.Chart} chart
             * The related chart of the color axis.
             *
             * @param {Highcharts.ColorAxisOptions} userOptions
             * The color axis options for initialization.
             */
            ColorAxis.prototype.init = function (chart, userOptions) {
                var axis = this;
                var legend = chart.options.legend || {},
                    horiz = userOptions.layout ?
                        userOptions.layout !== 'vertical' :
                        legend.layout !== 'vertical',
                    visible = userOptions.visible;
                var options = merge(ColorAxis.defaultColorAxisOptions,
                    userOptions, {
                        showEmpty: false,
                        title: null,
                        visible: legend.enabled && visible !== false
                    });
                axis.coll = 'colorAxis';
                axis.side = userOptions.side || horiz ? 2 : 1;
                axis.reversed = userOptions.reversed || !horiz;
                axis.opposite = !horiz;
                _super.prototype.init.call(this, chart, options);
                // #16053: Restore the actual userOptions.visible so the color axis
                // doesnt stay hidden forever when hiding and showing legend
                axis.userOptions.visible = visible;
                // Base init() pushes it to the xAxis array, now pop it again
                // chart[this.isXAxis ? 'xAxis' : 'yAxis'].pop();
                // Prepare data classes
                if (userOptions.dataClasses) {
                    axis.initDataClasses(userOptions);
                }
                axis.initStops();
                // Override original axis properties
                axis.horiz = horiz;
                axis.zoomEnabled = false;
            };
            /**
             * @private
             */
            ColorAxis.prototype.initDataClasses = function (userOptions) {
                var axis = this,
                    chart = axis.chart,
                    legendItem = axis.legendItem = axis.legendItem || {},
                    len = userOptions.dataClasses.length,
                    options = axis.options;
                var dataClasses,
                    colorCounter = 0,
                    colorCount = chart.options.chart.colorCount;
                axis.dataClasses = dataClasses = [];
                legendItem.labels = [];
                (userOptions.dataClasses || []).forEach(function (dataClass, i) {
                    var colors;
                    dataClass = merge(dataClass);
                    dataClasses.push(dataClass);
                    if (!chart.styledMode && dataClass.color) {
                        return;
                    }
                    if (options.dataClassColor === 'category') {
                        if (!chart.styledMode) {
                            colors = chart.options.colors;
                            colorCount = colors.length;
                            dataClass.color = colors[colorCounter];
                        }
                        dataClass.colorIndex = colorCounter;
                        // increase and loop back to zero
                        colorCounter++;
                        if (colorCounter === colorCount) {
                            colorCounter = 0;
                        }
                    }
                    else {
                        dataClass.color = color(options.minColor).tweenTo(color(options.maxColor), len < 2 ? 0.5 : i / (len - 1) // #3219
                        );
                    }
                });
            };
            /**
             * Returns true if the series has points at all.
             *
             * @function Highcharts.ColorAxis#hasData
             *
             * @return {boolean}
             * True, if the series has points, otherwise false.
             */
            ColorAxis.prototype.hasData = function () {
                return !!(this.tickPositions || []).length;
            };
            /**
             * Override so that ticks are not added in data class axes (#6914)
             * @private
             */
            ColorAxis.prototype.setTickPositions = function () {
                if (!this.dataClasses) {
                    return _super.prototype.setTickPositions.call(this);
                }
            };
            /**
             * @private
             */
            ColorAxis.prototype.initStops = function () {
                var axis = this;
                axis.stops = axis.options.stops || [
                    [0, axis.options.minColor],
                    [1, axis.options.maxColor]
                ];
                axis.stops.forEach(function (stop) {
                    stop.color = color(stop[1]);
                });
            };
            /**
             * Extend the setOptions method to process extreme colors and color stops.
             * @private
             */
            ColorAxis.prototype.setOptions = function (userOptions) {
                var axis = this;
                _super.prototype.setOptions.call(this, userOptions);
                axis.options.crosshair = axis.options.marker;
            };
            /**
             * @private
             */
            ColorAxis.prototype.setAxisSize = function () {
                var axis = this;
                var symbol = axis.legendItem && axis.legendItem.symbol;
                var chart = axis.chart;
                var legendOptions = chart.options.legend || {};
                var x,
                    y,
                    width,
                    height;
                if (symbol) {
                    this.left = x = symbol.attr('x');
                    this.top = y = symbol.attr('y');
                    this.width = width = symbol.attr('width');
                    this.height = height = symbol.attr('height');
                    this.right = chart.chartWidth - x - width;
                    this.bottom = chart.chartHeight - y - height;
                    this.len = this.horiz ? width : height;
                    this.pos = this.horiz ? x : y;
                }
                else {
                    // Fake length for disabled legend to avoid tick issues
                    // and such (#5205)
                    this.len = (this.horiz ?
                        legendOptions.symbolWidth :
                        legendOptions.symbolHeight) || ColorAxis.defaultLegendLength;
                }
            };
            /**
             * @private
             */
            ColorAxis.prototype.normalizedValue = function (value) {
                var axis = this;
                if (axis.logarithmic) {
                    value = axis.logarithmic.log2lin(value);
                }
                return 1 - ((axis.max - value) /
                    ((axis.max - axis.min) || 1));
            };
            /**
             * Translate from a value to a color.
             * @private
             */
            ColorAxis.prototype.toColor = function (value, point) {
                var axis = this;
                var dataClasses = axis.dataClasses;
                var stops = axis.stops;
                var pos,
                    from,
                    to,
                    color,
                    dataClass,
                    i;
                if (dataClasses) {
                    i = dataClasses.length;
                    while (i--) {
                        dataClass = dataClasses[i];
                        from = dataClass.from;
                        to = dataClass.to;
                        if ((typeof from === 'undefined' || value >= from) &&
                            (typeof to === 'undefined' || value <= to)) {
                            color = dataClass.color;
                            if (point) {
                                point.dataClass = i;
                                point.colorIndex = dataClass.colorIndex;
                            }
                            break;
                        }
                    }
                }
                else {
                    pos = axis.normalizedValue(value);
                    i = stops.length;
                    while (i--) {
                        if (pos > stops[i][0]) {
                            break;
                        }
                    }
                    from = stops[i] || stops[i + 1];
                    to = stops[i + 1] || from;
                    // The position within the gradient
                    pos = 1 - (to[0] - pos) / ((to[0] - from[0]) || 1);
                    color = from.color.tweenTo(to.color, pos);
                }
                return color;
            };
            /**
             * Override the getOffset method to add the whole axis groups inside the
             * legend.
             * @private
             */
            ColorAxis.prototype.getOffset = function () {
                var axis = this;
                var group = axis.legendItem && axis.legendItem.group;
                var sideOffset = axis.chart.axisOffset[axis.side];
                if (group) {
                    // Hook for the getOffset method to add groups to this parent
                    // group
                    axis.axisParent = group;
                    // Call the base
                    _super.prototype.getOffset.call(this);
                    var legend_1 = this.chart.legend;
                    // Adds `maxLabelLength` needed for label padding corrections done
                    // by `render()` and `getMargins()` (#15551).
                    legend_1.allItems.forEach(function (item) {
                        if (item instanceof ColorAxis) {
                            item.drawLegendSymbol(legend_1, item);
                        }
                    });
                    legend_1.render();
                    this.chart.getMargins(true);
                    // First time only
                    if (!axis.added) {
                        axis.added = true;
                        axis.labelLeft = 0;
                        axis.labelRight = axis.width;
                    }
                    // Reset it to avoid color axis reserving space
                    axis.chart.axisOffset[axis.side] = sideOffset;
                }
            };
            /**
             * Create the color gradient.
             * @private
             */
            ColorAxis.prototype.setLegendColor = function () {
                var axis = this;
                var horiz = axis.horiz;
                var reversed = axis.reversed;
                var one = reversed ? 1 : 0;
                var zero = reversed ? 0 : 1;
                var grad = horiz ? [one, 0,
                    zero, 0] : [0,
                    zero, 0,
                    one]; // #3190
                    axis.legendColor = {
                        linearGradient: {
                            x1: grad[0],
                            y1: grad[1],
                            x2: grad[2],
                            y2: grad[3]
                        },
                        stops: axis.stops
                    };
            };
            /**
             * The color axis appears inside the legend and has its own legend symbol.
             * @private
             */
            ColorAxis.prototype.drawLegendSymbol = function (legend, item) {
                var axis = this,
                    legendItem = item.legendItem || {},
                    padding = legend.padding,
                    legendOptions = legend.options,
                    itemDistance = pick(legendOptions.itemDistance, 10),
                    horiz = axis.horiz,
                    width = pick(legendOptions.symbolWidth,
                    horiz ? ColorAxis.defaultLegendLength : 12),
                    height = pick(legendOptions.symbolHeight,
                    horiz ? 12 : ColorAxis.defaultLegendLength),
                    labelPadding = pick(
                    // @todo: This option is not documented, nor implemented when
                    // vertical
                    legendOptions.labelPadding,
                    horiz ? 16 : 30);
                this.setLegendColor();
                // Create the gradient
                if (!legendItem.symbol) {
                    legendItem.symbol = this.chart.renderer.rect(0, legend.baseline - 11, width, height).attr({
                        zIndex: 1
                    }).add(legendItem.group);
                }
                // Set how much space this legend item takes up
                legendItem.labelWidth = (width +
                    padding +
                    (horiz ?
                        itemDistance :
                        this.options.labels.x + this.maxLabelLength));
                legendItem.labelHeight = height + padding + (horiz ? labelPadding : 0);
            };
            /**
             * Fool the legend.
             * @private
             */
            ColorAxis.prototype.setState = function (state) {
                this.series.forEach(function (series) {
                    series.setState(state);
                });
            };
            /**
             * @private
             */
            ColorAxis.prototype.setVisible = function () {
            };
            /**
             * @private
             */
            ColorAxis.prototype.getSeriesExtremes = function () {
                var axis = this;
                var series = axis.series;
                var colorValArray,
                    colorKey,
                    colorValIndex,
                    pointArrayMap,
                    calculatedExtremes,
                    cSeries,
                    i = series.length,
                    yData,
                    j;
                this.dataMin = Infinity;
                this.dataMax = -Infinity;
                while (i--) { // x, y, value, other
                    cSeries = series[i];
                    colorKey = cSeries.colorKey = pick(cSeries.options.colorKey, cSeries.colorKey, cSeries.pointValKey, cSeries.zoneAxis, 'y');
                    pointArrayMap = cSeries.pointArrayMap;
                    calculatedExtremes = cSeries[colorKey + 'Min'] &&
                        cSeries[colorKey + 'Max'];
                    if (cSeries[colorKey + 'Data']) {
                        colorValArray = cSeries[colorKey + 'Data'];
                    }
                    else {
                        if (!pointArrayMap) {
                            colorValArray = cSeries.yData;
                        }
                        else {
                            colorValArray = [];
                            colorValIndex = pointArrayMap.indexOf(colorKey);
                            yData = cSeries.yData;
                            if (colorValIndex >= 0 && yData) {
                                for (j = 0; j < yData.length; j++) {
                                    colorValArray.push(pick(yData[j][colorValIndex], yData[j]));
                                }
                            }
                        }
                    }
                    // If color key extremes are already calculated, use them.
                    if (calculatedExtremes) {
                        cSeries.minColorValue = cSeries[colorKey + 'Min'];
                        cSeries.maxColorValue = cSeries[colorKey + 'Max'];
                    }
                    else {
                        var cExtremes = Series.prototype.getExtremes.call(cSeries,
                            colorValArray);
                        cSeries.minColorValue = cExtremes.dataMin;
                        cSeries.maxColorValue = cExtremes.dataMax;
                    }
                    if (typeof cSeries.minColorValue !== 'undefined') {
                        this.dataMin =
                            Math.min(this.dataMin, cSeries.minColorValue);
                        this.dataMax =
                            Math.max(this.dataMax, cSeries.maxColorValue);
                    }
                    if (!calculatedExtremes) {
                        Series.prototype.applyExtremes.call(cSeries);
                    }
                }
            };
            /**
             * Internal function to draw a crosshair.
             *
             * @function Highcharts.ColorAxis#drawCrosshair
             *
             * @param {Highcharts.PointerEventObject} [e]
             *        The event arguments from the modified pointer event, extended with
             *        `chartX` and `chartY`
             *
             * @param {Highcharts.Point} [point]
             *        The Point object if the crosshair snaps to points.
             *
             * @emits Highcharts.ColorAxis#event:afterDrawCrosshair
             * @emits Highcharts.ColorAxis#event:drawCrosshair
             */
            ColorAxis.prototype.drawCrosshair = function (e, point) {
                var axis = this,
                    legendItem = axis.legendItem || {},
                    plotX = point && point.plotX,
                    plotY = point && point.plotY,
                    axisPos = axis.pos,
                    axisLen = axis.len;
                var crossPos;
                if (point) {
                    crossPos = axis.toPixels(point.getNestedProperty(point.series.colorKey));
                    if (crossPos < axisPos) {
                        crossPos = axisPos - 2;
                    }
                    else if (crossPos > axisPos + axisLen) {
                        crossPos = axisPos + axisLen + 2;
                    }
                    point.plotX = crossPos;
                    point.plotY = axis.len - crossPos;
                    _super.prototype.drawCrosshair.call(this, e, point);
                    point.plotX = plotX;
                    point.plotY = plotY;
                    if (axis.cross &&
                        !axis.cross.addedToColorAxis &&
                        legendItem.group) {
                        axis.cross
                            .addClass('highcharts-coloraxis-marker')
                            .add(legendItem.group);
                        axis.cross.addedToColorAxis = true;
                        if (!axis.chart.styledMode &&
                            typeof axis.crosshair === 'object') {
                            axis.cross.attr({
                                fill: axis.crosshair.color
                            });
                        }
                    }
                }
            };
            /**
             * @private
             */
            ColorAxis.prototype.getPlotLinePath = function (options) {
                var axis = this,
                    left = axis.left,
                    pos = options.translatedValue,
                    top = axis.top;
                // crosshairs only
                return isNumber(pos) ? // pos can be 0 (#3969)
                    (axis.horiz ? [
                        ['M', pos - 4, top - 6],
                        ['L', pos + 4, top - 6],
                        ['L', pos, top],
                        ['Z']
                    ] : [
                        ['M', left, pos],
                        ['L', left - 6, pos + 6],
                        ['L', left - 6, pos - 6],
                        ['Z']
                    ]) :
                    _super.prototype.getPlotLinePath.call(this, options);
            };
            /**
             * Updates a color axis instance with a new set of options. The options are
             * merged with the existing options, so only new or altered options need to
             * be specified.
             *
             * @function Highcharts.ColorAxis#update
             *
             * @param {Highcharts.ColorAxisOptions} newOptions
             * The new options that will be merged in with existing options on the color
             * axis.
             *
             * @param {boolean} [redraw]
             * Whether to redraw the chart after the color axis is altered. If doing
             * more operations on the chart, it is a good idea to set redraw to `false`
             * and call {@link Highcharts.Chart#redraw} after.
             */
            ColorAxis.prototype.update = function (newOptions, redraw) {
                var axis = this,
                    chart = axis.chart,
                    legend = chart.legend;
                this.series.forEach(function (series) {
                    // Needed for Axis.update when choropleth colors change
                    series.isDirtyData = true;
                });
                // When updating data classes, destroy old items and make sure new
                // ones are created (#3207)
                if (newOptions.dataClasses && legend.allItems || axis.dataClasses) {
                    axis.destroyItems();
                }
                _super.prototype.update.call(this, newOptions, redraw);
                if (axis.legendItem && axis.legendItem.label) {
                    axis.setLegendColor();
                    legend.colorizeItem(this, true);
                }
            };
            /**
             * Destroy color axis legend items.
             * @private
             */
            ColorAxis.prototype.destroyItems = function () {
                var axis = this,
                    chart = axis.chart,
                    legendItem = axis.legendItem || {};
                if (legendItem.label) {
                    chart.legend.destroyItem(axis);
                }
                else if (legendItem.labels) {
                    for (var _i = 0, _a = legendItem.labels; _i < _a.length; _i++) {
                        var item = _a[_i];
                        chart.legend.destroyItem(item);
                    }
                }
                chart.isDirtyLegend = true;
            };
            //   Removing the whole axis (#14283)
            ColorAxis.prototype.destroy = function () {
                this.chart.isDirtyLegend = true;
                this.destroyItems();
                _super.prototype.destroy.apply(this, [].slice.call(arguments));
            };
            /**
             * Removes the color axis and the related legend item.
             *
             * @function Highcharts.ColorAxis#remove
             *
             * @param {boolean} [redraw=true]
             *        Whether to redraw the chart following the remove.
             */
            ColorAxis.prototype.remove = function (redraw) {
                this.destroyItems();
                _super.prototype.remove.call(this, redraw);
            };
            /**
             * Get the legend item symbols for data classes.
             * @private
             */
            ColorAxis.prototype.getDataClassLegendSymbols = function () {
                var axis = this,
                    chart = axis.chart,
                    legendItems = (axis.legendItem &&
                        axis.legendItem.labels ||
                        []),
                    legendOptions = chart.options.legend,
                    valueDecimals = pick(legendOptions.valueDecimals, -1),
                    valueSuffix = pick(legendOptions.valueSuffix, '');
                var getPointsInDataClass = function (i) {
                        return axis.series.reduce(function (points,
                    s) {
                            points.push.apply(points,
                    s.points.filter(function (point) {
                                return point.dataClass === i;
                        }));
                        return points;
                    }, []);
                };
                var name;
                if (!legendItems.length) {
                    axis.dataClasses.forEach(function (dataClass, i) {
                        var from = dataClass.from,
                            to = dataClass.to,
                            numberFormatter = chart.numberFormatter;
                        var vis = true;
                        // Assemble the default name. This can be overridden
                        // by legend.options.labelFormatter
                        name = '';
                        if (typeof from === 'undefined') {
                            name = '< ';
                        }
                        else if (typeof to === 'undefined') {
                            name = '> ';
                        }
                        if (typeof from !== 'undefined') {
                            name += numberFormatter(from, valueDecimals) + valueSuffix;
                        }
                        if (typeof from !== 'undefined' && typeof to !== 'undefined') {
                            name += ' - ';
                        }
                        if (typeof to !== 'undefined') {
                            name += numberFormatter(to, valueDecimals) + valueSuffix;
                        }
                        // Add a mock object to the legend items
                        legendItems.push(extend({
                            chart: chart,
                            name: name,
                            options: {},
                            drawLegendSymbol: LegendSymbol.drawRectangle,
                            visible: true,
                            isDataClass: true,
                            // Override setState to set either normal or inactive
                            // state to all points in this data class
                            setState: function (state) {
                                for (var _i = 0, _a = getPointsInDataClass(i); _i < _a.length; _i++) {
                                    var point = _a[_i];
                                    point.setState(state);
                                }
                            },
                            // Override setState to show or hide all points in this
                            // data class
                            setVisible: function () {
                                this.visible = vis = axis.visible = !vis;
                                for (var _i = 0, _a = getPointsInDataClass(i); _i < _a.length; _i++) {
                                    var point = _a[_i];
                                    point.setVisible(vis);
                                }
                                chart.legend.colorizeItem(this, vis);
                            }
                        }, dataClass));
                    });
                }
                return legendItems;
            };
            /* *
             *
             *  Static Properties
             *
             * */
            ColorAxis.defaultColorAxisOptions = ColorAxisDefaults;
            ColorAxis.defaultLegendLength = 200;
            /**
             * @private
             */
            ColorAxis.keepProps = [
                'legendItem'
            ];
            return ColorAxis;
        }(Axis));
        /* *
         *
         *  Registry
         *
         * */
        // Properties to preserve after destroy, for Axis.update (#5881, #6025).
        Array.prototype.push.apply(Axis.keepProps, ColorAxis.keepProps);
        /* *
         *
         *  Default Export
         *
         * */
        /* *
         *
         *  API Declarations
         *
         * */
        /**
         * Color axis types
         *
         * @typedef {"linear"|"logarithmic"} Highcharts.ColorAxisTypeValue
         */
        ''; // detach doclet above

        return ColorAxis;
    });
    _registerModule(_modules, 'masters/modules/coloraxis.src.js', [_modules['Core/Globals.js'], _modules['Core/Axis/Color/ColorAxis.js']], function (Highcharts, ColorAxis) {

        var G = Highcharts;
        G.ColorAxis = ColorAxis;
        ColorAxis.compose(G.Chart, G.Fx, G.Legend, G.Series);

    });
}));