/**
 * @license Highcharts JS v10.3.2 (2022-11-28)
 *
 * Arc diagram module
 *
 * (c) 2021 Piotr Madej
 *
 * License: www.highcharts.com/license
 */
(function (factory) {
    if (typeof module === 'object' && module.exports) {
        factory['default'] = factory;
        module.exports = factory;
    } else if (typeof define === 'function' && define.amd) {
        define('highcharts/modules/arc-diagram', ['highcharts', 'highcharts/modules/sankey'], function (Highcharts) {
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
    _registerModule(_modules, 'Series/ArcDiagram/ArcDiagramPoint.js', [_modules['Series/NodesComposition.js'], _modules['Core/Series/SeriesRegistry.js'], _modules['Core/Utilities.js']], function (NodesComposition, SeriesRegistry, U) {
        /* *
         *
         *  Arc diagram module
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
        var extend = U.extend;
        /* *
         *
         *  Class
         *
         * */
        var ArcDiagramPoint = /** @class */ (function (_super) {
                __extends(ArcDiagramPoint, _super);
            function ArcDiagramPoint() {
                /* *
                 *
                 *  Properties
                 *
                 * */
                var _this = _super !== null && _super.apply(this,
                    arguments) || this;
                _this.fromNode = void 0;
                _this.index = void 0;
                _this.linksFrom = void 0;
                _this.linksTo = void 0;
                _this.options = void 0;
                _this.series = void 0;
                _this.scale = void 0;
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
            ArcDiagramPoint.prototype.isValid = function () {
                // No null points here
                return true;
            };
            return ArcDiagramPoint;
        }(SankeyPoint));
        extend(ArcDiagramPoint.prototype, {
            setState: NodesComposition.setNodeState
        });
        /* *
         *
         *  Default Export
         *
         * */

        return ArcDiagramPoint;
    });
    _registerModule(_modules, 'Series/ArcDiagram/ArcDiagramSeries.js', [_modules['Series/ArcDiagram/ArcDiagramPoint.js'], _modules['Series/Sankey/SankeyColumnComposition.js'], _modules['Core/Series/Series.js'], _modules['Core/Series/SeriesRegistry.js'], _modules['Core/Renderer/SVG/SVGRenderer.js'], _modules['Core/Utilities.js']], function (ArcDiagramPoint, SankeyColumnComposition, Series, SeriesRegistry, SVGRenderer, U) {
        /* *
         *
         *  Arc diagram module
         *
         *  (c) 2021 Piotr Madej, Grzegorz Blachliński
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
        var __rest = (this && this.__rest) || function (s,
            e) {
                var t = {};
            for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p) && e.indexOf(p) < 0)
                t[p] = s[p];
            if (s != null && typeof Object.getOwnPropertySymbols === "function")
                for (var i = 0, p = Object.getOwnPropertySymbols(s); i < p.length; i++) {
                    if (e.indexOf(p[i]) < 0 && Object.prototype.propertyIsEnumerable.call(s, p[i]))
                        t[p[i]] = s[p[i]];
                }
            return t;
        };
        var symbols = SVGRenderer.prototype.symbols;
        var _a = SeriesRegistry.seriesTypes,
            ColumnSeries = _a.column,
            SankeySeries = _a.sankey;
        var extend = U.extend,
            merge = U.merge,
            pick = U.pick,
            relativeLength = U.relativeLength;
        /* *
         *
         *  Class
         *
         * */
        /**
         * @private
         * @class
         * @name Highcharts.seriesTypes.arcdiagram
         *
         * @augments Highcharts.seriesTypes.sankey
         */
        var ArcDiagramSeries = /** @class */ (function (_super) {
                __extends(ArcDiagramSeries, _super);
            function ArcDiagramSeries() {
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
            /**
             * Create node columns by analyzing the nodes and the relations between
             * incoming and outgoing links.
             * @private
             */
            ArcDiagramSeries.prototype.createNodeColumns = function () {
                var _this = this;
                var series = this,
                    chart = series.chart, 
                    // column needs casting, to much methods required at the same time
                    column = SankeyColumnComposition.compose([],
                    series);
                column.sankeyColumn.maxLength = chart.inverted ?
                    chart.plotHeight : chart.plotWidth;
                // Get the translation factor needed for each column to fill up the plot
                // height
                column.sankeyColumn.getTranslationFactor = function (series) {
                    var nodes = column.slice(),
                        minLinkWidth = _this.options.minLinkWidth || 0;
                    var skipPoint,
                        factor = 0,
                        i,
                        radius,
                        maxRadius = 0,
                        scale = 1,
                        additionalSpace = 0,
                        remainingWidth = (chart.plotSizeX || 0) -
                            (series.options.marker &&
                                series.options.marker.lineWidth || 0) -
                            (column.length - 1) *
                                series.nodePadding;
                    // Because the minLinkWidth option doesn't obey the direct
                    // translation, we need to run translation iteratively, check node
                    // heights, remove those nodes affected by minLinkWidth, check
                    // again, etc.
                    while (column.length) {
                        factor = remainingWidth / column.sankeyColumn.sum();
                        skipPoint = false;
                        i = column.length;
                        while (i--) {
                            radius = (column[i].getSum()) * factor * scale;
                            var plotArea = Math.min(chart.plotHeight,
                                chart.plotWidth);
                            if (radius > plotArea) {
                                scale = Math.min(plotArea / radius, scale);
                            }
                            else if (radius < minLinkWidth) {
                                column.splice(i, 1);
                                remainingWidth -= minLinkWidth;
                                radius = minLinkWidth;
                                skipPoint = true;
                            }
                            additionalSpace += radius * (1 - scale) / 2;
                            maxRadius = Math.max(maxRadius, radius);
                        }
                        if (!skipPoint) {
                            break;
                        }
                    }
                    // Re-insert original nodes
                    column.length = 0;
                    nodes.forEach(function (node) {
                        node.scale = scale;
                        column.push(node);
                    });
                    column.sankeyColumn.maxRadius = maxRadius;
                    column.sankeyColumn.scale = scale;
                    column.sankeyColumn.additionalSpace = additionalSpace;
                    return factor;
                };
                column.sankeyColumn.offset = function (node, factor) {
                    var equalNodes = node.series.options.equalNodes;
                    var offset = column.sankeyColumn.additionalSpace || 0,
                        totalNodeOffset,
                        nodePadding = series.nodePadding,
                        maxRadius = Math.min(chart.plotWidth,
                        chart.plotHeight, (column.sankeyColumn.maxLength || 0) /
                            series.nodes.length - nodePadding);
                    for (var i = 0; i < column.length; i++) {
                        var sum = column[i].getSum() *
                                (column.sankeyColumn.scale || 0);
                        var width = equalNodes ?
                                maxRadius :
                                Math.max(sum * factor,
                            series.options.minLinkWidth || 0);
                        if (sum) {
                            totalNodeOffset = width + nodePadding;
                        }
                        else {
                            // If node sum equals 0 nodePadding is missed #12453
                            totalNodeOffset = 0;
                        }
                        if (column[i] === node) {
                            return {
                                relativeLeft: offset + relativeLength(node.options.offset || 0, totalNodeOffset)
                            };
                        }
                        offset += totalNodeOffset;
                    }
                };
                // Add nodes directly to the column right after it's creation
                series.nodes.forEach(function (node) {
                    node.column = 0;
                    column.push(node);
                });
                return [column];
            };
            /**
             * Run translation operations for one link.
             * @private
             */
            ArcDiagramSeries.prototype.translateLink = function (point) {
                var _a,
                    _b;
                var series = this,
                    fromNode = point.fromNode,
                    toNode = point.toNode,
                    chart = this.chart,
                    translationFactor = series.translationFactor,
                    pointOptions = point.options,
                    seriesOptions = series.options,
                    linkWeight = pick(pointOptions.linkWeight,
                    seriesOptions.linkWeight,
                    Math.max((point.weight || 0) *
                        translationFactor *
                        fromNode.scale, (series.options.minLinkWidth || 0))),
                    centeredLinks = point.series.options.centeredLinks,
                    nodeTop = fromNode.nodeY;
                var getX = function (node,
                    fromOrTo) {
                        var linkLeft = ((node.offset(point,
                    fromOrTo) || 0) *
                            translationFactor);
                    var x = Math.min(node.nodeX + linkLeft, 
                        // Prevent links from spilling below the node (#12014)
                        node.nodeX + (node.shapeArgs && node.shapeArgs.height || 0) - linkWeight);
                    return x;
                };
                var fromX = centeredLinks ?
                        fromNode.nodeX +
                            ((fromNode.shapeArgs.height || 0) - linkWeight) / 2 :
                        getX(fromNode, 'linksFrom'),
                    toX = centeredLinks ? toNode.nodeX +
                        ((toNode.shapeArgs.height || 0) - linkWeight) / 2 :
                        getX(toNode, 'linksTo'),
                    bottom = nodeTop,
                    linkWidth = linkWeight;
                if (fromX > toX) {
                    _a = [toX, fromX], fromX = _a[0], toX = _a[1];
                }
                if (seriesOptions.reversed) {
                    _b = [toX, fromX], fromX = _b[0], toX = _b[1];
                    bottom = (chart.plotSizeY || 0) - bottom;
                    linkWidth = -linkWidth;
                }
                point.shapeType = 'path';
                point.linkBase = [
                    fromX,
                    fromX + linkWeight,
                    toX,
                    toX + linkWeight
                ];
                var linkRadius = ((toX + linkWeight - fromX) / Math.abs(toX + linkWeight - fromX)) * pick(seriesOptions.linkRadius,
                    Math.min(Math.abs(toX + linkWeight - fromX) / 2,
                    fromNode.nodeY - Math.abs(linkWeight)));
                point.shapeArgs = {
                    d: [
                        ['M', fromX, bottom],
                        [
                            'A',
                            (toX + linkWeight - fromX) / 2,
                            linkRadius,
                            0,
                            0,
                            1,
                            toX + linkWeight,
                            bottom
                        ],
                        ['L', toX, bottom],
                        [
                            'A',
                            (toX - fromX - linkWeight) / 2,
                            linkRadius - linkWeight,
                            0,
                            0,
                            0,
                            fromX + linkWeight,
                            bottom
                        ],
                        ['Z']
                    ]
                };
                point.dlBox = {
                    x: fromX + (toX - fromX) / 2,
                    y: bottom - linkRadius,
                    height: linkWeight,
                    width: 0
                };
                // And set the tooltip anchor in the middle
                point.tooltipPos = chart.inverted ? [
                    (chart.plotSizeY || 0) - point.dlBox.y - linkWeight / 2,
                    (chart.plotSizeX || 0) - point.dlBox.x
                ] : [
                    point.dlBox.x,
                    point.dlBox.y + linkWeight / 2
                ];
                // Pass test in drawPoints
                point.y = point.plotY = 1;
                point.x = point.plotX = 1;
                if (!point.color) {
                    point.color = fromNode.color;
                }
            };
            /**
             * Run translation operations for one node.
             * @private
             */
            ArcDiagramSeries.prototype.translateNode = function (node, column) {
                var series = this,
                    translationFactor = series.translationFactor,
                    chart = series.chart,
                    maxNodesLength = chart.inverted ?
                        chart.plotWidth : chart.plotHeight,
                    options = series.options,
                    maxRadius = Math.min(chart.plotWidth,
                    chart.plotHeight,
                    maxNodesLength / node.series.nodes.length - this.nodePadding),
                    sum = node.getSum() * (column.sankeyColumn.scale || 0),
                    equalNodes = options.equalNodes,
                    nodeHeight = equalNodes ?
                        maxRadius :
                        Math.max(sum * translationFactor,
                    this.options.minLinkWidth || 0),
                    crisp = Math.round(options.marker &&
                        options.marker.lineWidth || 0) % 2 / 2,
                    nodeOffset = column.sankeyColumn.offset(node,
                    translationFactor),
                    fromNodeLeft = Math.floor(pick(nodeOffset && nodeOffset.absoluteLeft, ((column.sankeyColumn.left(translationFactor) || 0) +
                        (nodeOffset && nodeOffset.relativeLeft || 0)))) + crisp,
                    markerOptions = merge(options.marker,
                    node.options.marker),
                    symbol = markerOptions.symbol,
                    markerRadius = markerOptions.radius,
                    top = parseInt(options.offset, 10) *
                        ((chart.inverted ?
                            chart.plotWidth : chart.plotHeight) - (Math.floor(this.colDistance * (node.column || 0) +
                            (markerOptions.lineWidth || 0) / 2) + crisp +
                            (column.sankeyColumn.scale || 0) *
                                (column.sankeyColumn.maxRadius || 0) / 2)) / 100;
                node.sum = sum;
                // If node sum is 0, don’t render the rect #12453
                if (sum) {
                    // Draw the node
                    node.nodeX = fromNodeLeft;
                    node.nodeY = top;
                    var x = fromNodeLeft,
                        width = node.options.width || options.width || nodeHeight,
                        height = node.options.height || options.height || nodeHeight;
                    var y = top;
                    if (options.reversed) {
                        y = (chart.plotSizeY || 0) - top;
                        if (chart.inverted) {
                            y = (chart.plotSizeY || 0) - top;
                        }
                    }
                    if (this.mapOptionsToLevel) {
                        // Calculate data label options for the point
                        node.dlOptions = SankeySeries.getDLOptions({
                            level: this.mapOptionsToLevel[node.level],
                            optionsPoint: node.options
                        });
                    }
                    // Pass test in drawPoints
                    node.plotX = 1;
                    node.plotY = 1;
                    // Set the anchor position for tooltips
                    node.tooltipPos = chart.inverted ? [
                        (chart.plotSizeY || 0) - y - height / 2,
                        (chart.plotSizeX || 0) - x - width / 2
                    ] : [
                        x + width / 2,
                        y + height / 2
                    ];
                    node.shapeType = 'path';
                    node.shapeArgs = {
                        d: symbols[symbol || 'circle'](x, y - (markerRadius || height) / 2, markerRadius || width, markerRadius || height),
                        width: markerRadius || width,
                        height: markerRadius || height
                    };
                    node.dlBox = {
                        x: x + width / 2,
                        y: y,
                        height: 0,
                        width: 0
                    };
                }
                else {
                    node.dlOptions = {
                        enabled: false
                    };
                }
            };
            // Networkgraph has two separate collecions of nodes and lines, render
            // dataLabels for both sets:
            ArcDiagramSeries.prototype.drawDataLabels = function () {
                if (this.options.dataLabels) {
                    var textPath = this.options.dataLabels.textPath;
                    // Render node labels:
                    ColumnSeries.prototype.drawDataLabels.call(this, this.nodes);
                    // Render link labels:
                    this.options.dataLabels.textPath =
                        this.options.dataLabels.linkTextPath;
                    ColumnSeries.prototype.drawDataLabels.call(this, this.data);
                    // Restore nodes
                    this.options.dataLabels.textPath = textPath;
                }
            };
            ArcDiagramSeries.prototype.pointAttribs = function (point, state) {
                if (point && point.isNode) {
                    var _a = Series.prototype.pointAttribs
                            .apply(this,
                        arguments),
                        opacity = _a.opacity,
                        attrs = __rest(_a,
                        ["opacity"]);
                    return attrs;
                }
                return _super.prototype.pointAttribs.apply(this, arguments);
            };
            ArcDiagramSeries.prototype.markerAttribs = function (point) {
                if (point.isNode) {
                    return _super.prototype.markerAttribs.apply(this, arguments);
                }
                return {};
            };
            /**
             *  Arc diagram series is a chart drawing style in which
             *  the vertices of the chart are positioned along a line
             *  on the Euclidean plane and the edges are drawn as a semicircle
             *  in one of the two half-planes delimited by the line,
             *  or as smooth curves formed by sequences of semicircles.
             *
             * @sample highcharts/demo/arc-diagram/
             *         Arc Diagram
             *
             * @extends      plotOptions.sankey
             * @since 10.0.0
             * @product      highcharts
             * @requires     modules/arc-diagram
             * @exclude      curveFactor, connectEnds, connectNulls, colorAxis, colorKey,
             *               dataSorting, dragDrop, getExtremesFromAll, nodePadding,
             *               centerInCategory, pointInterval, pointIntervalUnit,
             *               pointPlacement, pointStart, relativeXValue, softThreshold,
             *               stack, stacking, step, xAxis, yAxis
             * @optionparent plotOptions.arcdiagram
             */
            ArcDiagramSeries.defaultOptions = merge(SankeySeries.defaultOptions, {
                /**
                 * The option to center links rather than position them one after
                 * another
                 *
                 * @type    {boolean}
                 * @since 10.0.0
                 * @default false
                 * @product highcharts
                 */
                centeredLinks: false,
                /**
                 * The radius of the link arc. If not set, series renders a semi-circle
                 * between the nodes, except when overflowing the edge of the plot area,
                 * in which case an arc touching the edge is rendered. If `linkRadius`
                 * is set, an arc extending to the given value is rendered.
                 *
                 * @type    {number}
                 * @since 10.0.0
                 * @default undefined
                 * @product highcharts
                 * @apioption series.arcdiagram.linkRadius
                 */
                /**
                 * The offset of an arc diagram nodes column in relation to the
                 * `plotArea`. The offset equal to 50% places nodes in the center of a
                 * chart. By default the series is placed so that the biggest node is
                 * touching the bottom border of the `plotArea`.
                 *
                 * @type    {string}
                 * @since 10.0.0
                 * @default '100%'
                 * @product highcharts
                 * @apioption series.arcdiagram.offset
                 */
                offset: '100%',
                /**
                 * The global link weight. If not set, width is calculated per link,
                 * depending on the weight value.
                 *
                 * @type    {number}
                 * @since 10.0.0
                 * @default undefined
                 * @product highcharts
                 * @apioption series.arcdiagram.linkWeight
                 */
                /**
                 * Whether nodes with different values should have the same size. If set
                 * to true, all nodes are calculated based on the `nodePadding` and
                 * current `plotArea`. It is possible to override it using the
                 * `marker.radius` option.
                 *
                 * @type    {boolean}
                 * @since 10.0.0
                 * @default false
                 * @product highcharts
                 */
                equalNodes: false,
                /**
                 * Whether the series should be placed on the other side of the
                 * `plotArea`.
                 *
                 * @type    {boolean}
                 * @since 10.0.0
                 * @default false
                 * @product highcharts
                 */
                reversed: false,
                /**
                 * Options for the data labels appearing on top of the nodes and links.
                 * For arc diagram charts, data labels are visible for the nodes by
                 * default, but hidden for links. This is controlled by modifying the
                 * `nodeFormat`, and the `format` that applies to links and is an empty
                 * string by default.
                 *
                 * @declare Highcharts.SeriesArcDiagramDataLabelsOptionsObject
                 *
                 * @private
                 */
                dataLabels: {
                    /**
                     * Options for a _link_ label text which should follow link
                     * connection. Border and background are disabled for a label that
                     * follows a path.
                     *
                     * **Note:** Only SVG-based renderer supports this option. Setting
                     * `useHTML` to true will disable this option.
                     *
                     * @extends plotOptions.networkgraph.dataLabels.linkTextPath
                     * @since 10.0.0
                     */
                    linkTextPath: {
                        /**
                         * @type    {Highcharts.SVGAttributes}
                         * @default {"startOffset":"25%"}
                         */
                        attributes: {
                            /**
                             * @ignore-option
                             */
                            startOffset: '25%'
                        }
                    }
                },
                /**
                 * @extends   plotOptions.series.marker
                 * @excluding enabled, enabledThreshold, height, width
                 */
                marker: {
                    symbol: 'circle',
                    fillOpacity: 1,
                    lineWidth: 0,
                    states: {}
                }
            });
            return ArcDiagramSeries;
        }(SankeySeries));
        extend(ArcDiagramSeries.prototype, {
            orderNodes: false
        });
        ArcDiagramSeries.prototype.pointClass = ArcDiagramPoint;
        SeriesRegistry.registerSeriesType('arcdiagram', ArcDiagramSeries);
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
         * An `arcdiagram` series. If the [type](#series.arcdiagram.type)
         * option is not specified, it is inherited from [chart.type](#chart.type).
         *
         * @extends   series,plotOptions.arcdiagram
         * @exclude   dataSorting, boostThreshold, boostBlending, curveFactor,
         *            connectEnds, connectNulls, colorAxis, colorKey, dataSorting,
         *            dragDrop, getExtremesFromAll, nodePadding, centerInCategory,
         *            pointInterval, pointIntervalUnit, pointPlacement,
         *            pointStart, relativeXValue, softThreshold, stack,
         *            stacking, step, xAxis, yAxis
         * @product   highcharts
         * @requires  modules/sankey
         * @requires  modules/arc-diagram
         * @apioption series.arcdiagram
         */
        /**
         * @extends   plotOptions.series.marker
         * @excluding enabled, enabledThreshold, height, radius, width
         * @apioption series.arcdiagram.marker
         */
        /**
         * @type      {Highcharts.SeriesArcDiagramDataLabelsOptionsObject|Array<Highcharts.SeriesArcDiagramDataLabelsOptionsObject>}
         * @product   highcharts
         * @apioption series.arcdiagram.data.dataLabels
         */
        /**
         * A collection of options for the individual nodes. The nodes in an arc diagram
         * are auto-generated instances of `Highcharts.Point`, but options can be
         * applied here and linked by the `id`.
         *
         * @extends   series.sankey.nodes
         * @type      {Array<*>}
         * @product   highcharts
         * @excluding column, level
         * @apioption series.arcdiagram.nodes
         */
        /**
         * Individual data label for each node. The options are the same as the ones for
         * [series.arcdiagram.dataLabels](#series.arcdiagram.dataLabels).
         *
         * @type
         * {Highcharts.SeriesArcDiagramDataLabelsOptionsObject|Array<Highcharts.SeriesArcDiagramDataLabelsOptionsObject>}
         *
         * @apioption series.arcdiagram.nodes.dataLabels
         */
        /**
         * Individual data label for each node. The options are the same as the ones for
         * [series.arcdiagram.dataLabels](#series.arcdiagram.dataLabels).
         *
         * @type
         * {Highcharts.SeriesArcDiagramDataLabelsOptionsObject|Array<Highcharts.SeriesArcDiagramDataLabelsOptionsObject>}
         *
         */
        /**
         * An array of data points for the series. For the `arcdiagram` series type,
         * points can be given in the following way:
         *
         * An array of objects with named values. The following snippet shows only a few
         * settings, see the complete options set below. If the total number of data
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
         * @type      {Array<*>}
         * @extends   series.sankey.data
         * @product   highcharts
         * @excluding outgoing, dataLabels
         * @apioption series.arcdiagram.data
         */
        ''; // adds doclets above to the transpiled file

        return ArcDiagramSeries;
    });
    _registerModule(_modules, 'masters/modules/arc-diagram.src.js', [], function () {


    });
}));