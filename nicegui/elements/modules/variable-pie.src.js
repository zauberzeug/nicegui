/**
 * @license Highcharts JS v10.3.2 (2022-11-28)
 *
 * Variable Pie module for Highcharts
 *
 * (c) 2010-2021 Grzegorz Blachliński
 *
 * License: www.highcharts.com/license
 */
(function (factory) {
    if (typeof module === 'object' && module.exports) {
        factory['default'] = factory;
        module.exports = factory;
    } else if (typeof define === 'function' && define.amd) {
        define('highcharts/modules/variable-pie', ['highcharts'], function (Highcharts) {
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
    _registerModule(_modules, 'Series/VariablePie/VariablePieSeries.js', [_modules['Core/Series/SeriesRegistry.js'], _modules['Core/Utilities.js']], function (SeriesRegistry, U) {
        /* *
         *
         *  Variable Pie module for Highcharts
         *
         *  (c) 2010-2021 Grzegorz Blachliński
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
        var PieSeries = SeriesRegistry.seriesTypes.pie;
        var arrayMax = U.arrayMax,
            arrayMin = U.arrayMin,
            clamp = U.clamp,
            extend = U.extend,
            fireEvent = U.fireEvent,
            merge = U.merge,
            pick = U.pick;
        /* *
         *
         *  Class
         *
         * */
        /**
         * The variablepie series type.
         *
         * @private
         * @class
         * @name Highcharts.seriesTypes.variablepie
         *
         * @augments Highcharts.Series
         */
        var VariablePieSeries = /** @class */ (function (_super) {
                __extends(VariablePieSeries, _super);
            function VariablePieSeries() {
                /* *
                 *
                 *  Static Properties
                 *
                 * */
                var _this = _super !== null && _super.apply(this,
                    arguments) || this;
                /* *
                 *
                 *  Properties
                 *
                 * */
                _this.data = void 0;
                _this.options = void 0;
                _this.points = void 0;
                _this.radii = void 0;
                return _this;
                /* eslint-enable valid-jsdoc */
            }
            /* *
             *
             *  Functions
             *
             * */
            /* eslint-disable valid-jsdoc */
            /**
             * Before standard translate method for pie chart it is needed to calculate
             * min/max radius of each pie slice based on its Z value.
             * @private
             */
            VariablePieSeries.prototype.calculateExtremes = function () {
                var series = this,
                    chart = series.chart,
                    plotWidth = chart.plotWidth,
                    plotHeight = chart.plotHeight,
                    seriesOptions = series.options,
                    slicingRoom = 2 * (seriesOptions.slicedOffset || 0),
                    zMin,
                    zMax,
                    zData = series.zData,
                    smallestSize = Math.min(plotWidth,
                    plotHeight) - slicingRoom, 
                    // Min and max size of pie slice:
                    extremes = {}, 
                    // In pie charts size of a pie is changed to make space for
                    // dataLabels, then series.center is changing.
                    positions = series.center || series.getCenter();
                ['minPointSize', 'maxPointSize'].forEach(function (prop) {
                    var length = seriesOptions[prop],
                        isPercent = /%$/.test(length);
                    length = parseInt(length, 10);
                    extremes[prop] = isPercent ?
                        smallestSize * length / 100 :
                        length * 2; // Because it should be radius, not diameter.
                });
                series.minPxSize = positions[3] + extremes.minPointSize;
                series.maxPxSize = clamp(positions[2], positions[3] + extremes.minPointSize, extremes.maxPointSize);
                if (zData.length) {
                    zMin = pick(seriesOptions.zMin, arrayMin(zData.filter(series.zValEval)));
                    zMax = pick(seriesOptions.zMax, arrayMax(zData.filter(series.zValEval)));
                    this.getRadii(zMin, zMax, series.minPxSize, series.maxPxSize);
                }
            };
            /**
             * Finding radius of series points based on their Z value and min/max Z
             * value for all series.
             *
             * @private
             * @function Highcharts.Series#getRadii
             *
             * @param {number} zMin
             * Min threshold for Z value. If point's Z value is smaller that zMin, point
             * will have the smallest possible radius.
             *
             * @param {number} zMax
             * Max threshold for Z value. If point's Z value is bigger that zMax, point
             * will have the biggest possible radius.
             *
             * @param {number} minSize
             * Minimal pixel size possible for radius.
             *
             * @param {numbner} maxSize
             * Minimal pixel size possible for radius.
             */
            VariablePieSeries.prototype.getRadii = function (zMin, zMax, minSize, maxSize) {
                var i = 0,
                    pos,
                    zData = this.zData,
                    len = zData.length,
                    radii = [],
                    options = this.options,
                    sizeByArea = options.sizeBy !== 'radius',
                    zRange = zMax - zMin,
                    value,
                    radius;
                // Calculate radius for all pie slice's based on their Z values
                for (i; i < len; i++) {
                    // if zData[i] is null/undefined/string we need to take zMin for
                    // smallest radius.
                    value = this.zValEval(zData[i]) ? zData[i] : zMin;
                    if (value <= zMin) {
                        radius = minSize / 2;
                    }
                    else if (value >= zMax) {
                        radius = maxSize / 2;
                    }
                    else {
                        // Relative size, a number between 0 and 1
                        pos = zRange > 0 ? (value - zMin) / zRange : 0.5;
                        if (sizeByArea) {
                            pos = Math.sqrt(pos);
                        }
                        radius = Math.ceil(minSize + pos * (maxSize - minSize)) / 2;
                    }
                    radii.push(radius);
                }
                this.radii = radii;
            };
            /**
             * It is needed to null series.center on chart redraw. Probably good idea
             * will be to add this option in directly in pie series.
             * @private
             */
            VariablePieSeries.prototype.redraw = function () {
                this.center = null;
                _super.prototype.redraw.apply(this, arguments);
            };
            /**
             * Extend translate by updating radius for each pie slice instead of using
             * one global radius.
             * @private
             */
            VariablePieSeries.prototype.translate = function (positions) {
                this.generatePoints();
                var series = this,
                    cumulative = 0,
                    precision = 1000, // issue #172
                    options = series.options,
                    slicedOffset = options.slicedOffset,
                    connectorOffset = slicedOffset + (options.borderWidth || 0),
                    finalConnectorOffset,
                    start,
                    end,
                    angle,
                    startAngle = options.startAngle || 0,
                    startAngleRad = Math.PI / 180 * (startAngle - 90),
                    endAngleRad = Math.PI / 180 * (pick(options.endAngle,
                    startAngle + 360) - 90),
                    circ = endAngleRad - startAngleRad, // 2 * Math.PI,
                    points = series.points, 
                    // the x component of the radius vector for a given point
                    radiusX,
                    radiusY,
                    labelDistance = options.dataLabels.distance,
                    ignoreHiddenPoint = options.ignoreHiddenPoint,
                    i,
                    len = points.length,
                    point,
                    pointRadii,
                    pointRadiusX,
                    pointRadiusY;
                series.startAngleRad = startAngleRad;
                series.endAngleRad = endAngleRad;
                // Use calculateExtremes to get series.radii array.
                series.calculateExtremes();
                // Get positions - either an integer or a percentage string must be
                // given. If positions are passed as a parameter, we're in a
                // recursive loop for adjusting space for data labels.
                if (!positions) {
                    series.center = positions = series.getCenter();
                }
                // Calculate the geometry for each point
                for (i = 0; i < len; i++) {
                    point = points[i];
                    pointRadii = series.radii[i];
                    // Used for distance calculation for specific point.
                    point.labelDistance = pick(point.options.dataLabels &&
                        point.options.dataLabels.distance, labelDistance);
                    // Saved for later dataLabels distance calculation.
                    series.maxLabelDistance = Math.max(series.maxLabelDistance || 0, point.labelDistance);
                    // set start and end angle
                    start = startAngleRad + (cumulative * circ);
                    if (!ignoreHiddenPoint || point.visible) {
                        cumulative += point.percentage / 100;
                    }
                    end = startAngleRad + (cumulative * circ);
                    // set the shape
                    point.shapeType = 'arc';
                    point.shapeArgs = {
                        x: positions[0],
                        y: positions[1],
                        r: pointRadii,
                        innerR: positions[3] / 2,
                        start: Math.round(start * precision) / precision,
                        end: Math.round(end * precision) / precision
                    };
                    // The angle must stay within -90 and 270 (#2645)
                    angle = (end + start) / 2;
                    if (angle > 1.5 * Math.PI) {
                        angle -= 2 * Math.PI;
                    }
                    else if (angle < -Math.PI / 2) {
                        angle += 2 * Math.PI;
                    }
                    // Center for the sliced out slice
                    point.slicedTranslation = {
                        translateX: Math.round(Math.cos(angle) * slicedOffset),
                        translateY: Math.round(Math.sin(angle) * slicedOffset)
                    };
                    // set the anchor point for tooltips
                    radiusX = Math.cos(angle) * positions[2] / 2;
                    radiusY = Math.sin(angle) * positions[2] / 2;
                    pointRadiusX = Math.cos(angle) * pointRadii;
                    pointRadiusY = Math.sin(angle) * pointRadii;
                    point.tooltipPos = [
                        positions[0] + radiusX * 0.7,
                        positions[1] + radiusY * 0.7
                    ];
                    point.half = angle < -Math.PI / 2 || angle > Math.PI / 2 ?
                        1 :
                        0;
                    point.angle = angle;
                    // Set the anchor point for data labels. Use point.labelDistance
                    // instead of labelDistance // #1174
                    // finalConnectorOffset - not override connectorOffset value.
                    finalConnectorOffset = Math.min(connectorOffset, point.labelDistance / 5); // #1678
                    point.labelPosition = {
                        natural: {
                            // initial position of the data label - it's utilized
                            // for finding the final position for the label
                            x: positions[0] + pointRadiusX +
                                Math.cos(angle) * point.labelDistance,
                            y: positions[1] + pointRadiusY +
                                Math.sin(angle) * point.labelDistance
                        },
                        'final': {
                        // used for generating connector path -
                        // initialized later in drawDataLabels function
                        // x: undefined,
                        // y: undefined
                        },
                        // left - pie on the left side of the data label
                        // right - pie on the right side of the data label
                        alignment: point.half ? 'right' : 'left',
                        connectorPosition: {
                            breakAt: {
                                x: positions[0] + pointRadiusX +
                                    Math.cos(angle) * finalConnectorOffset,
                                y: positions[1] + pointRadiusY +
                                    Math.sin(angle) * finalConnectorOffset
                            },
                            touchingSliceAt: {
                                x: positions[0] + pointRadiusX,
                                y: positions[1] + pointRadiusY
                            }
                        }
                    };
                }
                fireEvent(series, 'afterTranslate');
            };
            /**
             * For arrayMin and arrayMax calculations array shouldn't have
             * null/undefined/string values. In this case it is needed to check if
             * points Z value is a Number.
             * @private
             */
            VariablePieSeries.prototype.zValEval = function (zVal) {
                if (typeof zVal === 'number' && !isNaN(zVal)) {
                    return true;
                }
                return null;
            };
            /**
             * A variable pie series is a two dimensional series type, where each point
             * renders an Y and Z value.  Each point is drawn as a pie slice where the
             * size (arc) of the slice relates to the Y value and the radius of pie
             * slice relates to the Z value.
             *
             * @sample {highcharts} highcharts/demo/variable-radius-pie/
             *         Variable-radius pie chart
             *
             * @extends      plotOptions.pie
             * @excluding    dragDrop
             * @since        6.0.0
             * @product      highcharts
             * @requires     modules/variable-pie.js
             * @optionparent plotOptions.variablepie
             */
            VariablePieSeries.defaultOptions = merge(PieSeries.defaultOptions, {
                /**
                 * The minimum size of the points' radius related to chart's `plotArea`.
                 * If a number is set, it applies in pixels.
                 *
                 * @sample {highcharts} highcharts/variable-radius-pie/min-max-point-size/
                 *         Example of minPointSize and maxPointSize
                 * @sample {highcharts} highcharts/variable-radius-pie/min-point-size-100/
                 *         minPointSize set to 100
                 *
                 * @type  {number|string}
                 * @since 6.0.0
                 */
                minPointSize: '10%',
                /**
                 * The maximum size of the points' radius related to chart's `plotArea`.
                 * If a number is set, it applies in pixels.
                 *
                 * @sample {highcharts} highcharts/variable-radius-pie/min-max-point-size/
                 *         Example of minPointSize and maxPointSize
                 *
                 * @type  {number|string}
                 * @since 6.0.0
                 */
                maxPointSize: '100%',
                /**
                 * The minimum possible z value for the point's radius calculation. If
                 * the point's Z value is smaller than zMin, the slice will be drawn
                 * according to the zMin value.
                 *
                 * @sample {highcharts} highcharts/variable-radius-pie/zmin-5/
                 *         zMin set to 5, smaller z values are treated as 5
                 * @sample {highcharts} highcharts/variable-radius-pie/zmin-zmax/
                 *         Series limited by both zMin and zMax
                 *
                 * @type  {number}
                 * @since 6.0.0
                 */
                zMin: void 0,
                /**
                 * The maximum possible z value for the point's radius calculation. If
                 * the point's Z value is bigger than zMax, the slice will be drawn
                 * according to the zMax value
                 *
                 * @sample {highcharts} highcharts/variable-radius-pie/zmin-zmax/
                 *         Series limited by both zMin and zMax
                 *
                 * @type  {number}
                 * @since 6.0.0
                 */
                zMax: void 0,
                /**
                 * Whether the pie slice's value should be represented by the area or
                 * the radius of the slice. Can be either `area` or `radius`. The
                 * default, `area`, corresponds best to the human perception of the size
                 * of each pie slice.
                 *
                 * @sample {highcharts} highcharts/variable-radius-pie/sizeby/
                 *         Difference between area and radius sizeBy
                 *
                 * @type  {Highcharts.VariablePieSizeByValue}
                 * @since 6.0.0
                 */
                sizeBy: 'area',
                tooltip: {
                    pointFormat: '<span style="color:{point.color}">\u25CF</span> {series.name}<br/>Value: {point.y}<br/>Size: {point.z}<br/>'
                }
            });
            return VariablePieSeries;
        }(PieSeries));
        extend(VariablePieSeries.prototype, {
            pointArrayMap: ['y', 'z'],
            parallelArrays: ['x', 'y', 'z']
        });
        SeriesRegistry.registerSeriesType('variablepie', VariablePieSeries);
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
         * @typedef {"area"|"radius"} Highcharts.VariablePieSizeByValue
         */
        ''; // detach doclets above
        /* *
         *
         *  API Options
         *
         * */
        /**
         * A `variablepie` series. If the [type](#series.variablepie.type) option is not
         * specified, it is inherited from [chart.type](#chart.type).
         *
         * @extends   series,plotOptions.variablepie
         * @excluding dataParser, dataURL, stack, xAxis, yAxis, dataSorting,
         *            boostThreshold, boostBlending
         * @product   highcharts
         * @requires  modules/variable-pie.js
         * @apioption series.variablepie
         */
        /**
         * An array of data points for the series. For the `variablepie` series type,
         * points can be given in the following ways:
         *
         * 1. An array of arrays with 2 values. In this case, the numerical values will
         *    be interpreted as `y, z` options. Example:
         *    ```js
         *    data: [
         *        [40, 75],
         *        [50, 50],
         *        [60, 40]
         *    ]
         *    ```
         *
         * 2. An array of objects with named values. The following snippet shows only a
         *    few settings, see the complete options set below. If the total number of
         *    data points exceeds the series'
         *    [turboThreshold](#series.variablepie.turboThreshold), this option is not
         *    available.
         *    ```js
         *    data: [{
         *        y: 1,
         *        z: 4,
         *        name: "Point2",
         *        color: "#00FF00"
         *    }, {
         *        y: 7,
         *        z: 10,
         *        name: "Point1",
         *        color: "#FF00FF"
         *    }]
         *    ```
         *
         * @sample {highcharts} highcharts/series/data-array-of-arrays/
         *         Arrays of numeric x and y
         * @sample {highcharts} highcharts/series/data-array-of-arrays-datetime/
         *         Arrays of datetime x and y
         * @sample {highcharts} highcharts/series/data-array-of-name-value/
         *         Arrays of point.name and y
         * @sample {highcharts} highcharts/series/data-array-of-objects/
         *         Config objects
         *
         * @type      {Array<Array<(number|string),number>|*>}
         * @extends   series.pie.data
         * @excluding marker, x
         * @product   highcharts
         * @apioption series.variablepie.data
         */
        ''; // adds doclets above to transpiled file

        return VariablePieSeries;
    });
    _registerModule(_modules, 'masters/modules/variable-pie.src.js', [], function () {


    });
}));