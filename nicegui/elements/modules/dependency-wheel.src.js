/**
 * @license Highcharts JS v10.3.2 (2022-11-28)
 *
 * Dependency wheel module
 *
 * (c) 2010-2021 Torstein Honsi
 *
 * License: www.highcharts.com/license
 */
(function (factory) {
    if (typeof module === 'object' && module.exports) {
        factory['default'] = factory;
        module.exports = factory;
    } else if (typeof define === 'function' && define.amd) {
        define('highcharts/modules/dependency-wheel', ['highcharts', 'highcharts/modules/sankey'], function (Highcharts) {
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
    _registerModule(_modules, 'Series/DependencyWheel/DependencyWheelPoint.js', [_modules['Core/Series/SeriesRegistry.js'], _modules['Core/Utilities.js']], function (SeriesRegistry, U) {
        /* *
         *
         *  Dependency wheel module
         *
         *  (c) 2018-2021 Torstein Honsi
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
        var SankeyPoint = SeriesRegistry.seriesTypes.sankey.prototype.pointClass;
        var wrap = U.wrap;
        /* *
         *
         *  Class
         *
         * */
        var DependencyWheelPoint = /** @class */ (function (_super) {
                __extends(DependencyWheelPoint, _super);
            function DependencyWheelPoint() {
                /* *
                 *
                 *  Properties
                 *
                 * */
                var _this = _super !== null && _super.apply(this,
                    arguments) || this;
                _this.angle = void 0;
                _this.fromNode = void 0;
                _this.index = void 0;
                _this.linksFrom = void 0;
                _this.linksTo = void 0;
                _this.options = void 0;
                _this.series = void 0;
                _this.shapeArgs = void 0;
                _this.toNode = void 0;
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
             * Return a text path that the data label uses.
             * @private
             */
            DependencyWheelPoint.prototype.getDataLabelPath = function (label) {
                var _this = this;
                var renderer = this.series.chart.renderer,
                    shapeArgs = this.shapeArgs,
                    upperHalf = this.angle < 0 || this.angle > Math.PI,
                    start = shapeArgs.start || 0,
                    end = shapeArgs.end || 0;
                // First time
                if (!this.dataLabelPath) {
                    // Destroy the path with the label
                    wrap(label, 'destroy', function (proceed) {
                        if (_this.dataLabelPath) {
                            _this.dataLabelPath = _this.dataLabelPath.destroy();
                        }
                        return proceed.call(label);
                    });
                    // Subsequent times
                }
                else {
                    this.dataLabelPath = this.dataLabelPath.destroy();
                    delete this.dataLabelPath;
                }
                // All times
                this.dataLabelPath = renderer
                    .arc({
                    open: true,
                    longArc: Math.abs(Math.abs(start) - Math.abs(end)) < Math.PI ? 0 : 1
                })
                    .attr({
                    x: shapeArgs.x,
                    y: shapeArgs.y,
                    r: (shapeArgs.r +
                        (this.dataLabel.options.distance || 0)),
                    start: (upperHalf ? start : end),
                    end: (upperHalf ? end : start),
                    clockwise: +upperHalf
                })
                    .add(renderer.defs);
                return this.dataLabelPath;
            };
            DependencyWheelPoint.prototype.isValid = function () {
                // No null points here
                return true;
            };
            return DependencyWheelPoint;
        }(SankeyPoint));
        /* *
         *
         *  Default Export
         *
         * */

        return DependencyWheelPoint;
    });
    _registerModule(_modules, 'Series/DependencyWheel/DependencyWheelSeriesDefaults.js', [], function () {
        /* *
         *
         *  Dependency wheel module
         *
         *  (c) 2018-2021 Torstein Honsi
         *
         *  License: www.highcharts.com/license
         *
         *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
         *
         * */
        /* *
         *
         *  Constants
         *
         * */
        /**
         * A dependency wheel chart is a type of flow diagram, where all nodes are laid
         * out in a circle, and the flow between the are drawn as link bands.
         *
         * @sample highcharts/demo/dependency-wheel/
         *         Dependency wheel
         *
         * @extends      plotOptions.sankey
         * @exclude      dataSorting
         * @since        7.1.0
         * @product      highcharts
         * @requires     modules/dependency-wheel
         * @optionparent plotOptions.dependencywheel
         */
        var DependencyWheelSeriesDefaults = {
                /**
                 * Distance between the data label and the center of the node.
                 *
                 * @type      {number}
                 * @default   0
                 * @apioption plotOptions.dependencywheel.dataLabels.distance
                 */
                /**
                 * A format string for data labels of the links between nodes. Available
                 * variables are the same as for `formatter`.
                 *
                 * @see [nodeFormat](#nodeFormat) for formatting node labels
                 *
                 * @apioption plotOptions.dependencywheel.dataLabels.format
                 */
                /**
                 * Callback to format data labels of the links between nodes. The `format`
                 * option takes precedence over the `formatter` option.
                 *
                 * @see [nodeFormatter](#nodeFormatter) for formatting node labels
                 *
                 * @apioption plotOptions.dependencywheel.dataLabels.formatter
                 */
                /**
                 * The format string specifying what to show for nodes in the sankey
                 * diagram. By default the nodeFormatter returns `{point.name}`. Available
                 * variables are the same as for `nodeFormatter`.
                 *
                 * @apioption plotOptions.dependencywheel.dataLabels.nodeFormat
                 */
                /**
                 * Callback to format data labels of nodes in the dependency wheel. The
                 * `nodeFormat` option takes precedence over the `nodeFormatter` option.
                 *
                 * @apioption plotOptions.dependencywheel.dataLabels.nodeFormatter
                 */
                /**
                 * Size of the wheel in pixel or percent relative to the canvas space.
                 *
                 * @type      {number|string}
                 * @default   100%
                 * @apioption plotOptions.dependencywheel.size
                 */
                /**
                 * The center of the wheel relative to the plot area. Can be
                 * percentages or pixel values. The default behaviour is to
                 * center the wheel inside the plot area.
                 *
                 * @type    {Array<number|string|null>}
                 * @default [null,
            null]
                 * @product highcharts
                 */
                center: [null,
            null],
                curveFactor: 0.6,
                /**
                 * The start angle of the dependency wheel,
            in degrees where 0 is up.
                 */
                startAngle: 0,
                dataLabels: {
                    textPath: {
                        /**
                         * Enable or disable `textPath` option for link's or marker's data
                         * labels.
                         *
                         * @type      {boolean}
                         * @default   false
                         * @since     7.1.0
                         * @apioption plotOptions.series.dataLabels.textPath.enabled
                         */
                        enabled: false,
                        attributes: {
                            /**
                            * Text path shift along its y-axis.
                            *
                            * @type      {Highcharts.SVGAttributes}
                            * @default   5
                            * @since     7.1.0
                            * @apioption plotOptions.dependencywheel.dataLabels.textPath.attributes.dy
                            */
                            dy: 5
                        }
                    }
                }
            };
        /* *
         *
         *  Default Export
         *
         * */
        /* *
         *
         *  API Options
         *
         * */
        /**
         * A `dependencywheel` series. If the [type](#series.dependencywheel.type)
         * option is not specified, it is inherited from [chart.type](#chart.type).
         *
         * @extends   series,plotOptions.dependencywheel
         * @exclude   dataSorting
         * @product   highcharts
         * @requires  modules/sankey
         * @requires  modules/dependency-wheel
         * @apioption series.dependencywheel
         */
        /**
         * A collection of options for the individual nodes. The nodes in a dependency
         * diagram are auto-generated instances of `Highcharts.Point`, but options can
         * be applied here and linked by the `id`.
         *
         * @extends   series.sankey.nodes
         * @type      {Array<*>}
         * @product   highcharts
         * @excluding offset
         * @apioption series.dependencywheel.nodes
         */
        /**
         * An array of data points for the series. For the `dependencywheel` series
         * type, points can be given in the following way:
         *
         * An array of objects with named values. The following snippet shows only a
         * few settings, see the complete options set below. If the total number of data
         * points exceeds the series' [turboThreshold](#series.area.turboThreshold),
         * this option is not available.
         *
         *  ```js
         *     data: [{
         *         from: 'Category1',
         *         to: 'Category2',
         *         weight: 2
         *     }, {
         *         from: 'Category1',
         *         to: 'Category3',
         *         weight: 5
         *     }]
         *  ```
         *
         * @type      {Array<Array<string,string,number>|*>}
         * @extends   series.sankey.data
         * @product   highcharts
         * @excluding outgoing, dataLabels
         * @apioption series.dependencywheel.data
         */
        /**
         * Individual data label for each node. The options are the same as
         * the ones for [series.dependencywheel.dataLabels](#series.dependencywheel.dataLabels).
         *
         * @apioption series.dependencywheel.nodes.dataLabels
         */
        ''; // adds doclets above to the transpiled file

        return DependencyWheelSeriesDefaults;
    });
    _registerModule(_modules, 'Series/DependencyWheel/DependencyWheelSeries.js', [_modules['Core/Animation/AnimationUtilities.js'], _modules['Series/DependencyWheel/DependencyWheelPoint.js'], _modules['Series/DependencyWheel/DependencyWheelSeriesDefaults.js'], _modules['Core/Globals.js'], _modules['Series/Sankey/SankeyColumnComposition.js'], _modules['Core/Series/SeriesRegistry.js'], _modules['Core/Utilities.js']], function (A, DependencyWheelPoint, DependencyWheelSeriesDefaults, H, SankeyColumnComposition, SeriesRegistry, U) {
        /* *
         *
         *  Dependency wheel module
         *
         *  (c) 2018-2021 Torstein Honsi
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
        var animObject = A.animObject;
        var deg2rad = H.deg2rad;
        var _a = SeriesRegistry.seriesTypes,
            PieSeries = _a.pie,
            SankeySeries = _a.sankey;
        var extend = U.extend,
            merge = U.merge;
        /* *
         *
         *  Class
         *
         * */
        /**
         * @private
         * @class
         * @name Highcharts.seriesTypes.dependencywheel
         *
         * @augments Highcharts.seriesTypes.sankey
         */
        var DependencyWheelSeries = /** @class */ (function (_super) {
                __extends(DependencyWheelSeries, _super);
            function DependencyWheelSeries() {
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
                _this.nodeColumns = void 0;
                _this.nodes = void 0;
                _this.points = void 0;
                return _this;
                /* eslint-enable valid-jsdoc */
            }
            /* *
             *
             *  Functions
             *
             * */
            /* eslint-disable valid-jsdoc */
            DependencyWheelSeries.prototype.animate = function (init) {
                if (!init) {
                    var duration = animObject(this.options.animation).duration,
                        step_1 = (duration / 2) / this.nodes.length;
                    this.nodes.forEach(function (point, i) {
                        var graphic = point.graphic;
                        if (graphic) {
                            graphic.attr({ opacity: 0 });
                            setTimeout(function () {
                                if (point.graphic) {
                                    point.graphic.animate({ opacity: 1 }, { duration: step_1 });
                                }
                            }, step_1 * i);
                        }
                    }, this);
                    this.points.forEach(function (point) {
                        var graphic = point.graphic;
                        if (!point.isNode && graphic) {
                            graphic.attr({ opacity: 0 })
                                .animate({
                                opacity: 1
                            }, this.options.animation);
                        }
                    }, this);
                }
            };
            DependencyWheelSeries.prototype.createNode = function (id) {
                var node = SankeySeries.prototype.createNode.call(this,
                    id);
                /**
                 * Return the sum of incoming and outgoing links.
                 * @private
                 */
                node.getSum = function () {
                    return node.linksFrom
                        .concat(node.linksTo)
                        .reduce(function (acc, link) {
                        return acc + link.weight;
                    }, 0);
                };
                /**
                 * Get the offset in weight values of a point/link.
                 * @private
                 */
                node.offset = function (point) {
                    var offset = 0,
                        i,
                        links = node.linksFrom.concat(node.linksTo),
                        sliced;
                    /**
                     * @private
                     */
                    function otherNode(link) {
                        if (link.fromNode === node) {
                            return link.toNode;
                        }
                        return link.fromNode;
                    }
                    // Sort and slice the links to avoid links going out of each
                    // node crossing each other.
                    links.sort(function (a, b) {
                        return otherNode(a).index - otherNode(b).index;
                    });
                    for (i = 0; i < links.length; i++) {
                        if (otherNode(links[i]).index > node.index) {
                            links = links.slice(0, i).reverse().concat(links.slice(i).reverse());
                            sliced = true;
                            break;
                        }
                    }
                    if (!sliced) {
                        links.reverse();
                    }
                    for (i = 0; i < links.length; i++) {
                        if (links[i] === point) {
                            return offset;
                        }
                        offset += links[i].weight;
                    }
                };
                return node;
            };
            /**
             * Dependency wheel has only one column, it runs along the perimeter.
             * @private
             */
            DependencyWheelSeries.prototype.createNodeColumns = function () {
                var columns = [SankeyColumnComposition.compose([],
                    this)];
                this.nodes.forEach(function (node) {
                    node.column = 0;
                    columns[0].push(node);
                });
                return columns;
            };
            /**
             * Translate from vertical pixels to perimeter.
             * @private
             */
            DependencyWheelSeries.prototype.getNodePadding = function () {
                return this.options.nodePadding / Math.PI;
            };
            /**
             * @private
             * @todo Override the refactored sankey translateLink and translateNode
             * functions instead of the whole translate function.
             */
            DependencyWheelSeries.prototype.translate = function () {
                var options = this.options,
                    factor = 2 * Math.PI /
                        (this.chart.plotHeight + this.getNodePadding()),
                    center = this.getCenter(),
                    startAngle = (options.startAngle - 90) * deg2rad;
                SankeySeries.prototype.translate.call(this);
                this.nodeColumns[0].forEach(function (node) {
                    // Don't render the nodes if sum is 0 #12453
                    if (node.sum) {
                        var shapeArgs = node.shapeArgs,
                            centerX_1 = center[0],
                            centerY_1 = center[1],
                            r = center[2] / 2,
                            innerR_1 = r - options.nodeWidth,
                            start = startAngle + factor * (shapeArgs.y || 0),
                            end = startAngle +
                                factor * ((shapeArgs.y || 0) + (shapeArgs.height || 0));
                        // Middle angle
                        node.angle = start + (end - start) / 2;
                        node.shapeType = 'arc';
                        node.shapeArgs = {
                            x: centerX_1,
                            y: centerY_1,
                            r: r,
                            innerR: innerR_1,
                            start: start,
                            end: end
                        };
                        node.dlBox = {
                            x: centerX_1 + Math.cos((start + end) / 2) * (r + innerR_1) / 2,
                            y: centerY_1 + Math.sin((start + end) / 2) * (r + innerR_1) / 2,
                            width: 1,
                            height: 1
                        };
                        // Draw the links from this node
                        node.linksFrom.forEach(function (point) {
                            if (point.linkBase) {
                                var distance_1;
                                var corners = point.linkBase.map(function (top,
                                    i) {
                                        var angle = factor * top,
                                    x = Math.cos(startAngle + angle) * (innerR_1 + 1),
                                    y = Math.sin(startAngle + angle) * (innerR_1 + 1),
                                    curveFactor = options.curveFactor || 0;
                                    // The distance between the from and to node
                                    // along the perimeter. This affect how curved
                                    // the link is, so that links between neighbours
                                    // don't extend too far towards the center.
                                    distance_1 = Math.abs(point.linkBase[3 - i] * factor - angle);
                                    if (distance_1 > Math.PI) {
                                        distance_1 = 2 * Math.PI - distance_1;
                                    }
                                    distance_1 = distance_1 * innerR_1;
                                    if (distance_1 < innerR_1) {
                                        curveFactor *= (distance_1 / innerR_1);
                                    }
                                    return {
                                        x: centerX_1 + x,
                                        y: centerY_1 + y,
                                        cpX: centerX_1 + (1 - curveFactor) * x,
                                        cpY: centerY_1 + (1 - curveFactor) * y
                                    };
                                });
                                point.shapeArgs = {
                                    d: [[
                                            'M',
                                            corners[0].x, corners[0].y
                                        ], [
                                            'A',
                                            innerR_1, innerR_1,
                                            0,
                                            0,
                                            1,
                                            corners[1].x, corners[1].y
                                        ], [
                                            'C',
                                            corners[1].cpX, corners[1].cpY,
                                            corners[2].cpX, corners[2].cpY,
                                            corners[2].x, corners[2].y
                                        ], [
                                            'A',
                                            innerR_1, innerR_1,
                                            0,
                                            0,
                                            1,
                                            corners[3].x, corners[3].y
                                        ], [
                                            'C',
                                            corners[3].cpX, corners[3].cpY,
                                            corners[0].cpX, corners[0].cpY,
                                            corners[0].x, corners[0].y
                                        ]]
                                };
                            }
                        });
                    }
                });
            };
            DependencyWheelSeries.defaultOptions = merge(SankeySeries.defaultOptions, DependencyWheelSeriesDefaults);
            return DependencyWheelSeries;
        }(SankeySeries));
        extend(DependencyWheelSeries.prototype, {
            orderNodes: false,
            getCenter: PieSeries.prototype.getCenter
        });
        DependencyWheelSeries.prototype.pointClass = DependencyWheelPoint;
        SeriesRegistry.registerSeriesType('dependencywheel', DependencyWheelSeries);
        /* *
         *
         *  Default Export
         *
         * */

        return DependencyWheelSeries;
    });
    _registerModule(_modules, 'masters/modules/dependency-wheel.src.js', [], function () {


    });
}));