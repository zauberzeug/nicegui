/**
 * @license Highcharts JS v10.3.2 (2022-11-28)
 *
 * Sankey diagram module
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
        define('highcharts/modules/sankey', ['highcharts'], function (Highcharts) {
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
    _registerModule(_modules, 'Series/NodesComposition.js', [_modules['Core/Series/SeriesRegistry.js'], _modules['Core/Utilities.js']], function (SeriesRegistry, U) {
        /* *
         *
         *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
         *
         * */
        var _a = SeriesRegistry.series,
            seriesProto = _a.prototype,
            pointProto = _a.prototype.pointClass.prototype;
        var defined = U.defined,
            extend = U.extend,
            find = U.find,
            merge = U.merge,
            pick = U.pick;
        /* *
         *
         *  Composition
         *
         * */
        var NodesComposition;
        (function (NodesComposition) {
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
             *  Functions
             *
             * */
            /**
             * @private
             */
            function compose(PointClass, SeriesClass) {
                if (composedClasses.indexOf(PointClass) === -1) {
                    composedClasses.push(PointClass);
                    var pointProto_1 = PointClass.prototype;
                    pointProto_1.setNodeState = setNodeState;
                    pointProto_1.setState = setNodeState;
                    pointProto_1.update = updateNode;
                }
                if (composedClasses.indexOf(SeriesClass) === -1) {
                    composedClasses.push(SeriesClass);
                    var seriesProto_1 = SeriesClass.prototype;
                    seriesProto_1.destroy = destroy;
                    seriesProto_1.setData = setData;
                }
                return SeriesClass;
            }
            NodesComposition.compose = compose;
            /**
             * Create a single node that holds information on incoming and outgoing
             * links.
             * @private
             */
            function createNode(id) {
                var PointClass = this.pointClass,
                    findById = function (nodes,
                    id) { return find(nodes,
                    function (node) { return node.id === id; }); };
                var node = findById(this.nodes,
                    id),
                    options;
                if (!node) {
                    options = this.options.nodes && findById(this.options.nodes, id);
                    var newNode_1 = (new PointClass()).init(this,
                        extend({
                            className: 'highcharts-node',
                            isNode: true,
                            id: id,
                            y: 1 // Pass isNull test
                        },
                        options));
                    newNode_1.linksTo = [];
                    newNode_1.linksFrom = [];
                    /**
                     * Return the largest sum of either the incoming or outgoing links.
                     * @private
                     */
                    newNode_1.getSum = function () {
                        var sumTo = 0,
                            sumFrom = 0;
                        newNode_1.linksTo.forEach(function (link) {
                            sumTo += link.weight || 0;
                        });
                        newNode_1.linksFrom.forEach(function (link) {
                            sumFrom += link.weight || 0;
                        });
                        return Math.max(sumTo, sumFrom);
                    };
                    /**
                     * Get the offset in weight values of a point/link.
                     * @private
                     */
                    newNode_1.offset = function (point, coll) {
                        var offset = 0;
                        for (var i = 0; i < newNode_1[coll].length; i++) {
                            if (newNode_1[coll][i] === point) {
                                return offset;
                            }
                            offset += newNode_1[coll][i].weight;
                        }
                    };
                    // Return true if the node has a shape, otherwise all links are
                    // outgoing.
                    newNode_1.hasShape = function () {
                        var outgoing = 0;
                        newNode_1.linksTo.forEach(function (link) {
                            if (link.outgoing) {
                                outgoing++;
                            }
                        });
                        return (!newNode_1.linksTo.length ||
                            outgoing !== newNode_1.linksTo.length);
                    };
                    newNode_1.index = this.nodes.push(newNode_1) - 1;
                    node = newNode_1;
                }
                node.formatPrefix = 'node';
                // for use in formats
                node.name = node.name || node.options.id || '';
                // Mass is used in networkgraph:
                node.mass = pick(
                // Node:
                node.options.mass, node.options.marker && node.options.marker.radius, 
                // Series:
                this.options.marker && this.options.marker.radius, 
                // Default:
                4);
                return node;
            }
            NodesComposition.createNode = createNode;
            /**
             * Destroy alll nodes and links.
             * @private
             */
            function destroy() {
                // Nodes must also be destroyed (#8682, #9300)
                this.data = []
                    .concat(this.points || [], this.nodes);
                return seriesProto.destroy.apply(this, arguments);
            }
            NodesComposition.destroy = destroy;
            /**
             * Extend generatePoints by adding the nodes, which are Point objects but
             * pushed to the this.nodes array.
             * @private
             */
            function generatePoints() {
                var _this = this;
                var chart = this.chart,
                    nodeLookup = {};
                seriesProto.generatePoints.call(this);
                if (!this.nodes) {
                    this.nodes = []; // List of Point-like node items
                }
                this.colorCounter = 0;
                // Reset links from previous run
                this.nodes.forEach(function (node) {
                    node.linksFrom.length = 0;
                    node.linksTo.length = 0;
                    node.level = node.options.level;
                });
                // Create the node list and set up links
                this.points.forEach(function (point) {
                    if (defined(point.from)) {
                        if (!nodeLookup[point.from]) {
                            nodeLookup[point.from] = _this.createNode(point.from);
                        }
                        nodeLookup[point.from].linksFrom.push(point);
                        point.fromNode = nodeLookup[point.from];
                        // Point color defaults to the fromNode's color
                        if (chart.styledMode) {
                            point.colorIndex = pick(point.options.colorIndex, nodeLookup[point.from].colorIndex);
                        }
                        else {
                            point.color =
                                point.options.color || nodeLookup[point.from].color;
                        }
                    }
                    if (defined(point.to)) {
                        if (!nodeLookup[point.to]) {
                            nodeLookup[point.to] = _this.createNode(point.to);
                        }
                        nodeLookup[point.to].linksTo.push(point);
                        point.toNode = nodeLookup[point.to];
                    }
                    point.name = point.name || point.id; // for use in formats
                }, this);
                // Store lookup table for later use
                this.nodeLookup = nodeLookup;
            }
            NodesComposition.generatePoints = generatePoints;
            /**
             * Destroy all nodes on setting new data
             * @private
             */
            function setData() {
                if (this.nodes) {
                    this.nodes.forEach(function (node) {
                        node.destroy();
                    });
                    this.nodes.length = 0;
                }
                seriesProto.setData.apply(this, arguments);
            }
            /**
             * When hovering node, highlight all connected links. When hovering a link,
             * highlight all connected nodes.
             * @private
             */
            function setNodeState(state) {
                var args = arguments,
                    others = this.isNode ? this.linksTo.concat(this.linksFrom) :
                        [this.fromNode,
                    this.toNode];
                if (state !== 'select') {
                    others.forEach(function (linkOrNode) {
                        if (linkOrNode && linkOrNode.series) {
                            pointProto.setState.apply(linkOrNode, args);
                            if (!linkOrNode.isNode) {
                                if (linkOrNode.fromNode.graphic) {
                                    pointProto.setState.apply(linkOrNode.fromNode, args);
                                }
                                if (linkOrNode.toNode && linkOrNode.toNode.graphic) {
                                    pointProto.setState.apply(linkOrNode.toNode, args);
                                }
                            }
                        }
                    });
                }
                pointProto.setState.apply(this, args);
            }
            NodesComposition.setNodeState = setNodeState;
            /**
             * When updating a node, don't update `series.options.data`, but
             * `series.options.nodes`
             * @private
             */
            function updateNode(options, redraw, animation, runEvent) {
                var _this = this;
                var nodes = this.series.options.nodes,
                    data = this.series.options.data,
                    dataLength = data && data.length || 0,
                    linkConfig = data && data[this.index];
                pointProto.update.call(this, options, this.isNode ? false : redraw, // Hold the redraw for nodes
                animation, runEvent);
                if (this.isNode) {
                    // this.index refers to `series.nodes`, not `options.nodes` array
                    var nodeIndex = (nodes || [])
                            .reduce(// Array.findIndex needs a polyfill
                        function (prevIndex,
                        n,
                        index) {
                            return (_this.id === n.id ? index : prevIndex);
                    }, -1), 
                    // Merge old config with new config. New config is stored in
                    // options.data, because of default logic in point.update()
                    nodeConfig = merge(nodes && nodes[nodeIndex] || {}, data && data[this.index] || {});
                    // Restore link config
                    if (data) {
                        if (linkConfig) {
                            data[this.index] = linkConfig;
                        }
                        else {
                            // Remove node from config if there's more nodes than links
                            data.length = dataLength;
                        }
                    }
                    // Set node config
                    if (nodes) {
                        if (nodeIndex >= 0) {
                            nodes[nodeIndex] = nodeConfig;
                        }
                        else {
                            nodes.push(nodeConfig);
                        }
                    }
                    else {
                        this.series.options.nodes = [nodeConfig];
                    }
                    if (pick(redraw, true)) {
                        this.series.chart.redraw(animation);
                    }
                }
            }
            NodesComposition.updateNode = updateNode;
        })(NodesComposition || (NodesComposition = {}));
        /* *
         *
         *  Default Export
         *
         * */

        return NodesComposition;
    });
    _registerModule(_modules, 'Series/Sankey/SankeyPoint.js', [_modules['Core/Series/Point.js'], _modules['Core/Series/SeriesRegistry.js'], _modules['Core/Utilities.js']], function (Point, SeriesRegistry, U) {
        /* *
         *
         *  Sankey diagram module
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
        var ColumnSeries = SeriesRegistry.seriesTypes.column;
        var defined = U.defined;
        /* *
         *
         *  Class
         *
         * */
        var SankeyPoint = /** @class */ (function (_super) {
                __extends(SankeyPoint, _super);
            function SankeyPoint() {
                /* *
                 *
                 *  Properties
                 *
                 * */
                var _this = _super !== null && _super.apply(this,
                    arguments) || this;
                _this.className = void 0;
                _this.fromNode = void 0;
                _this.level = void 0;
                _this.linkBase = void 0;
                _this.linksFrom = void 0;
                _this.linksTo = void 0;
                _this.mass = void 0;
                _this.nodeX = void 0;
                _this.nodeY = void 0;
                _this.options = void 0;
                _this.series = void 0;
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
             * @private
             */
            SankeyPoint.prototype.applyOptions = function (options, x) {
                Point.prototype.applyOptions.call(this, options, x);
                // Treat point.level as a synonym of point.column
                if (defined(this.options.level)) {
                    this.options.column = this.column = this.options.level;
                }
                return this;
            };
            /**
             * @private
             */
            SankeyPoint.prototype.getClassName = function () {
                return (this.isNode ? 'highcharts-node ' : 'highcharts-link ') +
                    Point.prototype.getClassName.call(this);
            };
            /**
             * If there are incoming links, place it to the right of the
             * highest order column that links to this one.
             *
             * @private
             */
            SankeyPoint.prototype.getFromNode = function () {
                var node = this;
                var fromColumn = -1,
                    fromNode;
                for (var i = 0; i < node.linksTo.length; i++) {
                    var point = node.linksTo[i];
                    if (point.fromNode.column > fromColumn &&
                        point.fromNode !== node // #16080
                    ) {
                        fromNode = point.fromNode;
                        fromColumn = fromNode.column;
                    }
                }
                return { fromNode: fromNode, fromColumn: fromColumn };
            };
            /**
             * Calculate node.column if it's not set by user
             * @private
             */
            SankeyPoint.prototype.setNodeColumn = function () {
                var node = this;
                if (!defined(node.options.column)) {
                    // No links to this node, place it left
                    if (node.linksTo.length === 0) {
                        node.column = 0;
                    }
                    else {
                        node.column = node.getFromNode().fromColumn + 1;
                    }
                }
            };
            /**
             * @private
             */
            SankeyPoint.prototype.isValid = function () {
                return this.isNode || typeof this.weight === 'number';
            };
            return SankeyPoint;
        }(ColumnSeries.prototype.pointClass));
        /* *
         *
         *  Default Export
         *
         * */

        return SankeyPoint;
    });
    _registerModule(_modules, 'Series/Sankey/SankeySeriesDefaults.js', [], function () {
        /* *
         *
         *  Sankey diagram module
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
         * A sankey diagram is a type of flow diagram, in which the width of the
         * link between two nodes is shown proportionally to the flow quantity.
         *
         * @sample highcharts/demo/sankey-diagram/
         *         Sankey diagram
         * @sample highcharts/plotoptions/sankey-inverted/
         *         Inverted sankey diagram
         * @sample highcharts/plotoptions/sankey-outgoing
         *         Sankey diagram with outgoing links
         *
         * @extends      plotOptions.column
         * @since        6.0.0
         * @product      highcharts
         * @excluding    animationLimit, boostThreshold, borderRadius,
         *               crisp, cropThreshold, colorAxis, colorKey, depth, dragDrop,
         *               edgeColor, edgeWidth, findNearestPointBy, grouping,
         *               groupPadding, groupZPadding, maxPointWidth, negativeColor,
         *               pointInterval, pointIntervalUnit, pointPadding,
         *               pointPlacement, pointRange, pointStart, pointWidth,
         *               shadow, softThreshold, stacking, threshold, zoneAxis,
         *               zones, minPointLength, dataSorting, boostBlending
         * @requires     modules/sankey
         * @optionparent plotOptions.sankey
         *
         * @private
         */
        var SankeySeriesDefaults = {
                borderWidth: 0,
                colorByPoint: true,
                /**
                 * Higher numbers makes the links in a sankey diagram or dependency
                 * wheelrender more curved. A `curveFactor` of 0 makes the lines
                 * straight.
                 *
                 * @private
                 */
                curveFactor: 0.33,
                /**
                 * Options for the data labels appearing on top of the nodes and links.
                 * For sankey charts,
            data labels are visible for the nodes by default,
                 * but hidden for links. This is controlled by modifying the
                 * `nodeFormat`,
            and the `format` that applies to links and is an empty
                 * string by default.
                 *
                 * @declare Highcharts.SeriesSankeyDataLabelsOptionsObject
                 *
                 * @private
                 */
                dataLabels: {
                    enabled: true,
                    backgroundColor: 'none',
                    crop: false,
                    /**
                     * The
                     * [format string](https://www.highcharts.com/docs/chart-concepts/labels-and-string-formatting)
                     * specifying what to show for _nodes_ in the sankey diagram. By
                     * default the `nodeFormatter` returns `{point.name}`.
                     *
                     * @sample highcharts/plotoptions/sankey-link-datalabels/
                     *         Node and link data labels
                     *
                     * @type {string}
                     */
                    nodeFormat: void 0,
                    // eslint-disable-next-line valid-jsdoc
                    /**
                     * Callback to format data labels for _nodes_ in the sankey diagram.
                     * The `nodeFormat` option takes precedence over the
                     * `nodeFormatter`.
                     *
                     * @type  {Highcharts.SeriesSankeyDataLabelsFormatterCallbackFunction}
                     * @since 6.0.2
                     */
                    nodeFormatter: function () {
                        return this.point.name;
                },
                format: void 0,
                // eslint-disable-next-line valid-jsdoc
                /**
                 * @type {Highcharts.SeriesSankeyDataLabelsFormatterCallbackFunction}
                 */
                formatter: function () {
                    return;
                },
                inside: true
            },
            /**
             * @ignore-option
             *
             * @private
             */
            inactiveOtherPoints: true,
            /**
             * Set options on specific levels. Takes precedence over series options,
             * but not node and link options.
             *
             * @sample highcharts/demo/sunburst
             *         Sunburst chart
             *
             * @type      {Array<*>}
             * @since     7.1.0
             * @apioption plotOptions.sankey.levels
             */
            /**
             * Can set `borderColor` on all nodes which lay on the same level.
             *
             * @type      {Highcharts.ColorString}
             * @apioption plotOptions.sankey.levels.borderColor
             */
            /**
             * Can set `borderWidth` on all nodes which lay on the same level.
             *
             * @type      {number}
             * @apioption plotOptions.sankey.levels.borderWidth
             */
            /**
             * Can set `color` on all nodes which lay on the same level.
             *
             * @type      {Highcharts.ColorString|Highcharts.GradientColorObject|Highcharts.PatternObject}
             * @apioption plotOptions.sankey.levels.color
             */
            /**
             * Can set `colorByPoint` on all nodes which lay on the same level.
             *
             * @type      {boolean}
             * @default   true
             * @apioption plotOptions.sankey.levels.colorByPoint
             */
            /**
             * Can set `dataLabels` on all points which lay on the same level.
             *
             * @extends   plotOptions.sankey.dataLabels
             * @apioption plotOptions.sankey.levels.dataLabels
             */
            /**
             * Decides which level takes effect from the options set in the levels
             * object.
             *
             * @type      {number}
             * @apioption plotOptions.sankey.levels.level
             */
            /**
             * Can set `linkOpacity` on all points which lay on the same level.
             *
             * @type      {number}
             * @default   0.5
             * @apioption plotOptions.sankey.levels.linkOpacity
             */
            /**
             * Can set `states` on all nodes and points which lay on the same level.
             *
             * @extends   plotOptions.sankey.states
             * @apioption plotOptions.sankey.levels.states
             */
            /**
             * Opacity for the links between nodes in the sankey diagram.
             *
             * @private
             */
            linkOpacity: 0.5,
            /**
             * Opacity for the nodes in the sankey diagram.
             *
             * @private
             */
            opacity: 1,
            /**
             * The minimal width for a line of a sankey. By default,
             * 0 values are not shown.
             *
             * @sample highcharts/plotoptions/sankey-minlinkwidth
             *         Sankey diagram with minimal link height
             *
             * @type      {number}
             * @since     7.1.3
             * @default   0
             * @apioption plotOptions.sankey.minLinkWidth
             *
             * @private
             */
            minLinkWidth: 0,
            /**
             * The pixel width of each node in a sankey diagram or dependency wheel,
             * or the height in case the chart is inverted.
             *
             * @private
             */
            nodeWidth: 20,
            /**
             * The padding between nodes in a sankey diagram or dependency wheel, in
             * pixels.
             *
             * If the number of nodes is so great that it is possible to lay them
             * out within the plot area with the given `nodePadding`, they will be
             * rendered with a smaller padding as a strategy to avoid overflow.
             *
             * @private
             */
            nodePadding: 10,
            showInLegend: false,
            states: {
                hover: {
                    /**
                     * Opacity for the links between nodes in the sankey diagram in
                     * hover mode.
                     */
                    linkOpacity: 1,
                    /**
                     * Opacity for the nodes in the sankey diagram in hover mode.
                     */
                    opacity: 1
                },
                /**
                 * The opposite state of a hover for a single point node/link.
                 *
                 * @declare Highcharts.SeriesStatesInactiveOptionsObject
                 */
                inactive: {
                    /**
                     * Opacity for the links between nodes in the sankey diagram in
                     * inactive mode.
                     */
                    linkOpacity: 0.1,
                    /**
                     * Opacity of the nodes in the sankey diagram in inactive mode.
                     */
                    opacity: 0.1,
                    /**
                     * Animation when not hovering over the marker.
                     *
                     * @type      {boolean|Partial<Highcharts.AnimationOptionsObject>}
                     * @apioption plotOptions.series.states.inactive.animation
                     */
                    animation: {
                        /** @internal */
                        duration: 50
                    }
                }
            },
            tooltip: {
                /**
                 * A callback for defining the format for _nodes_ in the chart's
                 * tooltip, as opposed to links.
                 *
                 * @type      {Highcharts.FormatterCallbackFunction<Highcharts.SankeyNodeObject>}
                 * @since     6.0.2
                 * @apioption plotOptions.sankey.tooltip.nodeFormatter
                 */
                /**
                 * Whether the tooltip should follow the pointer or stay fixed on
                 * the item.
                 */
                followPointer: true,
                headerFormat: '<span style="font-size: 10px">{series.name}</span><br/>',
                pointFormat: '{point.fromNode.name} \u2192 {point.toNode.name}: <b>{point.weight}</b><br/>',
                /**
                 * The
                 * [format string](https://www.highcharts.com/docs/chart-concepts/labels-and-string-formatting)
                 * specifying what to show for _nodes_ in tooltip of a diagram
                 * series, as opposed to links.
                 */
                nodeFormat: '{point.name}: <b>{point.sum}</b><br/>'
            }
        };
        /**
         * A `sankey` series. If the [type](#series.sankey.type) option is not
         * specified, it is inherited from [chart.type](#chart.type).
         *
         * @extends   series,plotOptions.sankey
         * @excluding animationLimit, boostBlending, boostThreshold, borderColor,
         *            borderRadius, borderWidth, crisp, cropThreshold, dataParser,
         *            dataURL, depth, dragDrop, edgeColor, edgeWidth,
         *            findNearestPointBy, getExtremesFromAll, grouping, groupPadding,
         *            groupZPadding, label, maxPointWidth, negativeColor, pointInterval,
         *            pointIntervalUnit, pointPadding, pointPlacement, pointRange,
         *            pointStart, pointWidth, shadow, softThreshold, stacking,
         *            threshold, zoneAxis, zones, dataSorting
         * @product   highcharts
         * @requires  modules/sankey
         * @apioption series.sankey
         */
        /**
         * A collection of options for the individual nodes. The nodes in a sankey
         * diagram are auto-generated instances of `Highcharts.Point`, but options can
         * be applied here and linked by the `id`.
         *
         * @sample highcharts/css/sankey/
         *         Sankey diagram with node options
         *
         * @declare   Highcharts.SeriesSankeyNodesOptionsObject
         * @type      {Array<*>}
         * @product   highcharts
         * @apioption series.sankey.nodes
         */
        /**
         * The id of the auto-generated node, refering to the `from` or `to` setting of
         * the link.
         *
         * @type      {string}
         * @product   highcharts
         * @apioption series.sankey.nodes.id
         */
        /**
         * The color of the auto generated node.
         *
         * @type      {Highcharts.ColorString|Highcharts.GradientColorObject|Highcharts.PatternObject}
         * @product   highcharts
         * @apioption series.sankey.nodes.color
         */
        /**
         * The color index of the auto generated node, especially for use in styled
         * mode.
         *
         * @type      {number}
         * @product   highcharts
         * @apioption series.sankey.nodes.colorIndex
         */
        /**
         * An optional column index of where to place the node. The default behaviour is
         * to place it next to the preceding node. Note that this option name is
         * counter intuitive in inverted charts, like for example an organization chart
         * rendered top down. In this case the "columns" are horizontal.
         *
         * @sample highcharts/plotoptions/sankey-node-column/
         *         Specified node column
         *
         * @type      {number}
         * @since     6.0.5
         * @product   highcharts
         * @apioption series.sankey.nodes.column
         */
        /**
         * Individual data label for each node. The options are the same as
         * the ones for [series.sankey.dataLabels](#series.sankey.dataLabels).
         *
         * @extends   plotOptions.sankey.dataLabels
         * @apioption series.sankey.nodes.dataLabels
         */
        /**
         * An optional level index of where to place the node. The default behaviour is
         * to place it next to the preceding node. Alias of `nodes.column`, but in
         * inverted sankeys and org charts, the levels are laid out as rows.
         *
         * @type      {number}
         * @since     7.1.0
         * @product   highcharts
         * @apioption series.sankey.nodes.level
         */
        /**
         * The name to display for the node in data labels and tooltips. Use this when
         * the name is different from the `id`. Where the id must be unique for each
         * node, this is not necessary for the name.
         *
         * @sample highcharts/css/sankey/
         *         Sankey diagram with node options
         *
         * @type      {string}
         * @product   highcharts
         * @apioption series.sankey.nodes.name
         */
        /**
         * This option is deprecated, use
         * [offsetHorizontal](#series.sankey.nodes.offsetHorizontal) and
         * [offsetVertical](#series.sankey.nodes.offsetVertical) instead.
         *
         * In a horizontal layout, the vertical offset of a node in terms of weight.
         * Positive values shift the node downwards, negative shift it upwards. In a
         * vertical layout, like organization chart, the offset is horizontal.
         *
         * If a percantage string is given, the node is offset by the percentage of the
         * node size plus `nodePadding`.
         *
         * @deprecated
         * @type      {number|string}
         * @default   0
         * @since     6.0.5
         * @product   highcharts
         * @apioption series.sankey.nodes.offset
         */
        /**
         * The horizontal offset of a node. Positive values shift the node right,
         * negative shift it left.
         *
         * If a percantage string is given, the node is offset by the percentage of the
         * node size.
         *
         * @sample highcharts/plotoptions/sankey-node-column/
         *         Specified node offset
         *
         * @type      {number|string}
         * @since 9.3.0
         * @product   highcharts
         * @apioption series.sankey.nodes.offsetHorizontal
         */
        /**
         * The vertical offset of a node. Positive values shift the node down,
         * negative shift it up.
         *
         * If a percantage string is given, the node is offset by the percentage of the
         * node size.
         *
         * @sample highcharts/plotoptions/sankey-node-column/
         *         Specified node offset
         *
         * @type      {number|string}
         * @since 9.3.0
         * @product   highcharts
         * @apioption series.sankey.nodes.offsetVertical
         */
        /**
         * An array of data points for the series. For the `sankey` series type,
         * points can be given in the following way:
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
         *  When you provide the data as tuples, the keys option has to be set as well.
         *
         *  ```js
         *     keys: ['from', 'to', 'weight'],
         *     data: [
         *         ['Category1', 'Category2', 2],
         *         ['Category1', 'Category3', 5]
         *     ]
         *  ```
         *
         * @sample {highcharts} highcharts/series/data-array-of-objects/
         *         Config objects
         *
         * @declare   Highcharts.SeriesSankeyPointOptionsObject
         * @type      {Array<*>|Array<Array<(string|number)>>}
         * @extends   series.line.data
         * @excluding dragDrop, drilldown, marker, x, y
         * @product   highcharts
         * @apioption series.sankey.data
         */
        /**
         * The color for the individual _link_. By default, the link color is the same
         * as the node it extends from. The `series.fillOpacity` option also applies to
         * the points, so when setting a specific link color, consider setting the
         * `fillOpacity` to 1.
         *
         * @type      {Highcharts.ColorString|Highcharts.GradientColorObject|Highcharts.PatternObject}
         * @product   highcharts
         * @apioption series.sankey.data.color
         */
        /**
         * @type      {Highcharts.SeriesSankeyDataLabelsOptionsObject|Array<Highcharts.SeriesSankeyDataLabelsOptionsObject>}
         * @product   highcharts
         * @apioption series.sankey.data.dataLabels
         */
        /**
         * The node that the link runs from.
         *
         * @type      {string}
         * @product   highcharts
         * @apioption series.sankey.data.from
         */
        /**
         * The node that the link runs to.
         *
         * @type      {string}
         * @product   highcharts
         * @apioption series.sankey.data.to
         */
        /**
         * Whether the link goes out of the system.
         *
         * @sample highcharts/plotoptions/sankey-outgoing
         *         Sankey chart with outgoing links
         *
         * @type      {boolean}
         * @default   false
         * @product   highcharts
         * @apioption series.sankey.data.outgoing
         */
        /**
         * The weight of the link.
         *
         * @type      {number|null}
         * @product   highcharts
         * @apioption series.sankey.data.weight
         */
        ''; // adds doclets above to transpiled file
        /* *
         *
         *  Default Export
         *
         * */

        return SankeySeriesDefaults;
    });
    _registerModule(_modules, 'Series/Sankey/SankeyColumnComposition.js', [_modules['Core/Utilities.js']], function (U) {
        var defined = U.defined,
            relativeLength = U.relativeLength;
        var SankeyColumnComposition;
        (function (SankeyColumnComposition) {
            /* *
             *
             *  Declarations
             *
             * */
            /**
             * SankeyColumn Composition
             * @private
             * @function Highcharts.SankeyColumn#compose
             *
             * @param {Array<SankeyPoint>} points
             * The array of nodes
             * @param {SankeySeries} series
             * Series connected to column
             * @return {ArrayComposition} SankeyColumnArray
             */
            function compose(points, series) {
                var sankeyColumnArray = points;
                sankeyColumnArray.sankeyColumn =
                    new SankeyColumnAdditions(sankeyColumnArray, series);
                return sankeyColumnArray;
            }
            SankeyColumnComposition.compose = compose;
            /* *
             *
             *  Classes
             *
             * */
            var SankeyColumnAdditions = /** @class */ (function () {
                    function SankeyColumnAdditions(points, series) {
                        this.points = points;
                    this.series = series;
                }
                /**
                 * Calculate translation factor used in column and nodes distribution
                 * @private
                 * @function Highcharts.SankeyColumn#getTranslationFactor
                 *
                 * @param {SankeySeries} series
                 * The Series
                 * @return {number} TranslationFactor
                 * Translation Factor
                 */
                SankeyColumnAdditions.prototype.getTranslationFactor = function (series) {
                    var column = this.points,
                        nodes = column.slice(),
                        chart = series.chart,
                        minLinkWidth = series.options.minLinkWidth || 0;
                    var skipPoint,
                        factor = 0,
                        i,
                        remainingHeight = ((chart.plotSizeY || 0) -
                            (series.options.borderWidth || 0) -
                            (column.length - 1) * series.nodePadding);
                    // Because the minLinkWidth option doesn't obey the direct
                    // translation, we need to run translation iteratively, check
                    // node heights, remove those nodes affected by minLinkWidth,
                    // check again, etc.
                    while (column.length) {
                        factor = remainingHeight / column.sankeyColumn.sum();
                        skipPoint = false;
                        i = column.length;
                        while (i--) {
                            if (column[i].getSum() * factor < minLinkWidth) {
                                column.splice(i, 1);
                                remainingHeight -= minLinkWidth;
                                skipPoint = true;
                            }
                        }
                        if (!skipPoint) {
                            break;
                        }
                    }
                    // Re-insert original nodes
                    column.length = 0;
                    nodes.forEach(function (node) {
                        column.push(node);
                    });
                    return factor;
                };
                /**
                 * Get the top position of the column in pixels
                 * @private
                 * @function Highcharts.SankeyColumn#top
                 *
                 * @param {number} factor
                 * The Translation Factor
                 * @return {number} top
                 * The top position of the column
                 */
                SankeyColumnAdditions.prototype.top = function (factor) {
                    var series = this.series;
                    var nodePadding = series.nodePadding;
                    var height = this.points.reduce(function (height,
                        node) {
                            if (height > 0) {
                                height += nodePadding;
                        }
                        var nodeHeight = Math.max(node.getSum() * factor,
                            series.options.minLinkWidth || 0);
                        height += nodeHeight;
                        return height;
                    }, 0);
                    return ((series.chart.plotSizeY || 0) - height) / 2;
                };
                /**
                 * Get the left position of the column in pixels
                 * @private
                 * @function Highcharts.SankeyColumn#top
                 *
                 * @param {number} factor
                 * The Translation Factor
                 * @return {number} left
                 * The left position of the column
                 */
                SankeyColumnAdditions.prototype.left = function (factor) {
                    var series = this.series,
                        chart = series.chart,
                        equalNodes = series.options.equalNodes;
                    var maxNodesLength = chart.inverted ?
                            chart.plotHeight : chart.plotWidth,
                        nodePadding = series.nodePadding;
                    var width = this.points.reduce(function (width,
                        node) {
                            if (width > 0) {
                                width += nodePadding;
                        }
                        var nodeWidth = equalNodes ?
                                maxNodesLength / node.series.nodes.length - nodePadding :
                                Math.max(node.getSum() * factor,
                            series.options.minLinkWidth || 0);
                        width += nodeWidth;
                        return width;
                    }, 0);
                    return ((chart.plotSizeX || 0) - Math.round(width)) / 2;
                };
                /**
                 * Calculate sum of all nodes inside specific column
                 * @private
                 * @function Highcharts.SankeyColumn#sum
                 *
                 * @param {ArrayComposition} this
                 * Sankey Column Array
                 *
                 * @return {number} sum
                 * Sum of all nodes inside column
                 */
                SankeyColumnAdditions.prototype.sum = function () {
                    return this.points.reduce(function (sum, node) {
                        return sum + node.getSum();
                    }, 0);
                };
                /**
                 * Get the offset in pixels of a node inside the column
                 * @private
                 * @function Highcharts.SankeyColumn#offset
                 *
                 * @param {SankeyPoint} node
                 * Sankey node
                 * @param {number} factor
                 * Translation Factor
                 * @return {number} offset
                 * Offset of a node inside column
                 */
                SankeyColumnAdditions.prototype.offset = function (node, factor) {
                    var column = this.points,
                        series = this.series,
                        nodePadding = series.nodePadding;
                    var offset = 0,
                        totalNodeOffset;
                    if (series.is('organization') && node.hangsFrom) {
                        return {
                            absoluteTop: node.hangsFrom.nodeY
                        };
                    }
                    for (var i = 0; i < column.length; i++) {
                        var sum = column[i].getSum();
                        var height = Math.max(sum * factor,
                            series.options.minLinkWidth || 0);
                        var directionOffset = node.options[series.chart.inverted ?
                                'offsetHorizontal' :
                                'offsetVertical'],
                            optionOffset = node.options.offset || 0;
                        if (sum) {
                            totalNodeOffset = height + nodePadding;
                        }
                        else {
                            // If node sum equals 0 nodePadding is missed #12453
                            totalNodeOffset = 0;
                        }
                        if (column[i] === node) {
                            return {
                                relativeTop: offset + (defined(directionOffset) ?
                                    // directionOffset is a percent
                                    // of the node height
                                    relativeLength(directionOffset, height) :
                                    relativeLength(optionOffset, totalNodeOffset))
                            };
                        }
                        offset += totalNodeOffset;
                    }
                };
                return SankeyColumnAdditions;
            }());
            SankeyColumnComposition.SankeyColumnAdditions = SankeyColumnAdditions;
        })(SankeyColumnComposition || (SankeyColumnComposition = {}));

        return SankeyColumnComposition;
    });
    _registerModule(_modules, 'Series/TreeUtilities.js', [_modules['Core/Color/Color.js'], _modules['Core/Utilities.js']], function (Color, U) {
        /* *
         *
         *  (c) 2014-2021 Highsoft AS
         *
         *  Authors: Jon Arild Nygard / Oystein Moseng
         *
         *  License: www.highcharts.com/license
         *
         *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
         *
         * */
        var extend = U.extend,
            isArray = U.isArray,
            isNumber = U.isNumber,
            isObject = U.isObject,
            merge = U.merge,
            pick = U.pick;
        /* *
         *
         *  Functions
         *
         * */
        /* eslint-disable valid-jsdoc */
        /**
         * @private
         */
        function getColor(node, options) {
            var index = options.index,
                mapOptionsToLevel = options.mapOptionsToLevel,
                parentColor = options.parentColor,
                parentColorIndex = options.parentColorIndex,
                series = options.series,
                colors = options.colors,
                siblings = options.siblings,
                points = series.points,
                chartOptionsChart = series.chart.options.chart;
            var getColorByPoint,
                point,
                level,
                colorByPoint,
                colorIndexByPoint,
                color,
                colorIndex;
            /**
             * @private
             */
            var variateColor = function (color) {
                    var colorVariation = level && level.colorVariation;
                if (colorVariation &&
                    colorVariation.key === 'brightness' &&
                    index &&
                    siblings) {
                    return Color.parse(color).brighten(colorVariation.to * (index / siblings)).get();
                }
                return color;
            };
            if (node) {
                point = points[node.i];
                level = mapOptionsToLevel[node.level] || {};
                getColorByPoint = point && level.colorByPoint;
                if (getColorByPoint) {
                    colorIndexByPoint = point.index % (colors ?
                        colors.length :
                        chartOptionsChart.colorCount);
                    colorByPoint = colors && colors[colorIndexByPoint];
                }
                // Select either point color, level color or inherited color.
                if (!series.chart.styledMode) {
                    color = pick(point && point.options.color, level && level.color, colorByPoint, parentColor && variateColor(parentColor), series.color);
                }
                colorIndex = pick(point && point.options.colorIndex, level && level.colorIndex, colorIndexByPoint, parentColorIndex, options.colorIndex);
            }
            return {
                color: color,
                colorIndex: colorIndex
            };
        }
        /**
         * Creates a map from level number to its given options.
         *
         * @private
         *
         * @param {Object} params
         * Object containing parameters.
         * - `defaults` Object containing default options. The default options are
         *   merged with the userOptions to get the final options for a specific
         *   level.
         * - `from` The lowest level number.
         * - `levels` User options from series.levels.
         * - `to` The highest level number.
         *
         * @return {Highcharts.Dictionary<object>|null}
         * Returns a map from level number to its given options.
         */
        function getLevelOptions(params) {
            var result = {},
                defaults,
                converted,
                i,
                from,
                to,
                levels;
            if (isObject(params)) {
                from = isNumber(params.from) ? params.from : 1;
                levels = params.levels;
                converted = {};
                defaults = isObject(params.defaults) ? params.defaults : {};
                if (isArray(levels)) {
                    converted = levels.reduce(function (obj, item) {
                        var level,
                            levelIsConstant,
                            options;
                        if (isObject(item) && isNumber(item.level)) {
                            options = merge({}, item);
                            levelIsConstant = pick(options.levelIsConstant, defaults.levelIsConstant);
                            // Delete redundant properties.
                            delete options.levelIsConstant;
                            delete options.level;
                            // Calculate which level these options apply to.
                            level = item.level + (levelIsConstant ? 0 : from - 1);
                            if (isObject(obj[level])) {
                                merge(true, obj[level], options); // #16329
                            }
                            else {
                                obj[level] = options;
                            }
                        }
                        return obj;
                    }, {});
                }
                to = isNumber(params.to) ? params.to : 1;
                for (i = 0; i <= to; i++) {
                    result[i] = merge({}, defaults, isObject(converted[i]) ? converted[i] : {});
                }
            }
            return result;
        }
        /**
         * @private
         * @todo Combine buildTree and buildNode with setTreeValues
         * @todo Remove logic from Treemap and make it utilize this mixin.
         */
        function setTreeValues(tree, options) {
            var before = options.before,
                idRoot = options.idRoot,
                mapIdToNode = options.mapIdToNode,
                nodeRoot = mapIdToNode[idRoot],
                levelIsConstant = (options.levelIsConstant !== false),
                points = options.points,
                point = points[tree.i],
                optionsPoint = point && point.options || {},
                children = [];
            var childrenTotal = 0;
            tree.levelDynamic = tree.level - (levelIsConstant ? 0 : nodeRoot.level);
            tree.name = pick(point && point.name, '');
            tree.visible = (idRoot === tree.id ||
                options.visible === true);
            if (typeof before === 'function') {
                tree = before(tree, options);
            }
            // First give the children some values
            tree.children.forEach(function (child, i) {
                var newOptions = extend({},
                    options);
                extend(newOptions, {
                    index: i,
                    siblings: tree.children.length,
                    visible: tree.visible
                });
                child = setTreeValues(child, newOptions);
                children.push(child);
                if (child.visible) {
                    childrenTotal += child.val;
                }
            });
            // Set the values
            var value = pick(optionsPoint.value,
                childrenTotal);
            tree.visible = value >= 0 && (childrenTotal > 0 || tree.visible);
            tree.children = children;
            tree.childrenTotal = childrenTotal;
            tree.isLeaf = tree.visible && !childrenTotal;
            tree.val = value;
            return tree;
        }
        /**
         * Update the rootId property on the series. Also makes sure that it is
         * accessible to exporting.
         *
         * @private
         *
         * @param {Object} series
         * The series to operate on.
         *
         * @return {string}
         * Returns the resulting rootId after update.
         */
        function updateRootId(series) {
            var rootId,
                options;
            if (isObject(series)) {
                // Get the series options.
                options = isObject(series.options) ? series.options : {};
                // Calculate the rootId.
                rootId = pick(series.rootNode, options.rootId, '');
                // Set rootId on series.userOptions to pick it up in exporting.
                if (isObject(series.userOptions)) {
                    series.userOptions.rootId = rootId;
                }
                // Set rootId on series to pick it up on next update.
                series.rootNode = rootId;
            }
            return rootId;
        }
        /* *
         *
         *  Default Export
         *
         * */
        var TreeUtilities = {
                getColor: getColor,
                getLevelOptions: getLevelOptions,
                setTreeValues: setTreeValues,
                updateRootId: updateRootId
            };

        return TreeUtilities;
    });
    _registerModule(_modules, 'Series/Sankey/SankeySeries.js', [_modules['Core/Color/Color.js'], _modules['Core/Globals.js'], _modules['Series/NodesComposition.js'], _modules['Series/Sankey/SankeyPoint.js'], _modules['Series/Sankey/SankeySeriesDefaults.js'], _modules['Core/Series/SeriesRegistry.js'], _modules['Series/Sankey/SankeyColumnComposition.js'], _modules['Series/TreeUtilities.js'], _modules['Core/Utilities.js']], function (Color, H, NodesComposition, SankeyPoint, SankeySeriesDefaults, SeriesRegistry, SankeyColumnComposition, TU, U) {
        /* *
         *
         *  Sankey diagram module
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
        var Series = SeriesRegistry.series,
            ColumnSeries = SeriesRegistry.seriesTypes.column;
        var getLevelOptions = TU.getLevelOptions;
        var defined = U.defined,
            extend = U.extend,
            isObject = U.isObject,
            merge = U.merge,
            pick = U.pick,
            relativeLength = U.relativeLength,
            stableSort = U.stableSort;
        /* *
         *
         *  Class
         *
         * */
        /**
         * @private
         * @class
         * @name Highcharts.seriesTypes.sankey
         *
         * @augments Highcharts.Series
         */
        var SankeySeries = /** @class */ (function (_super) {
                __extends(SankeySeries, _super);
            function SankeySeries() {
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
                _this.colDistance = void 0;
                _this.data = void 0;
                _this.group = void 0;
                _this.nodeLookup = void 0;
                _this.nodePadding = void 0;
                _this.nodes = void 0;
                _this.nodeWidth = void 0;
                _this.options = void 0;
                _this.points = void 0;
                _this.translationFactor = void 0;
                return _this;
                /* eslint-enable valid-jsdoc */
            }
            /* *
             *
             *  Static Functions
             *
             * */
            // eslint-disable-next-line valid-jsdoc
            /**
             * @private
             */
            SankeySeries.getDLOptions = function (params) {
                var optionsPoint = (isObject(params.optionsPoint) ?
                        params.optionsPoint.dataLabels :
                        {}),
                    optionsLevel = (isObject(params.level) ?
                        params.level.dataLabels :
                        {}),
                    options = merge({
                        style: {}
                    },
                    optionsLevel,
                    optionsPoint);
                return options;
            };
            /* *
             *
             *  Functions
             *
             * */
            /* eslint-disable valid-jsdoc */
            /**
             * Create node columns by analyzing the nodes and the relations between
             * incoming and outgoing links.
             * @private
             */
            SankeySeries.prototype.createNodeColumns = function () {
                var columns = [];
                this.nodes.forEach(function (node) {
                    node.setNodeColumn();
                    if (!columns[node.column]) {
                        columns[node.column] =
                            SankeyColumnComposition.compose([], this);
                    }
                    columns[node.column].push(node);
                }, this);
                // Fill in empty columns (#8865)
                for (var i = 0; i < columns.length; i++) {
                    if (typeof columns[i] === 'undefined') {
                        columns[i] =
                            SankeyColumnComposition.compose([], this);
                    }
                }
                return columns;
            };
            /**
             * Order the nodes, starting with the root node(s). (#9818)
             * @private
             */
            SankeySeries.prototype.order = function (node, level) {
                var series = this;
                // Prevents circular recursion:
                if (typeof node.level === 'undefined') {
                    node.level = level;
                    node.linksFrom.forEach(function (link) {
                        if (link.toNode) {
                            series.order(link.toNode, level + 1);
                        }
                    });
                }
            };
            /**
             * Extend generatePoints by adding the nodes, which are Point objects
             * but pushed to the this.nodes array.
             * @private
             */
            SankeySeries.prototype.generatePoints = function () {
                NodesComposition.generatePoints.apply(this, arguments);
                var series = this;
                if (this.orderNodes) {
                    this.nodes
                        // Identify the root node(s)
                        .filter(function (node) {
                        return node.linksTo.length === 0;
                    })
                        // Start by the root node(s) and recursively set the level
                        // on all following nodes.
                        .forEach(function (node) {
                        series.order(node, 0);
                    });
                    stableSort(this.nodes, function (a, b) {
                        return a.level - b.level;
                    });
                }
            };
            /**
             * Overridable function to get node padding, overridden in dependency
             * wheel series type.
             * @private
             */
            SankeySeries.prototype.getNodePadding = function () {
                var nodePadding = this.options.nodePadding || 0;
                // If the number of columns is so great that they will overflow with
                // the given nodePadding, we sacrifice the padding in order to
                // render all nodes within the plot area (#11917).
                if (this.nodeColumns) {
                    var maxLength = this.nodeColumns.reduce(function (acc,
                        col) { return Math.max(acc,
                        col.length); }, 0);
                    if (maxLength * nodePadding > this.chart.plotSizeY) {
                        nodePadding = this.chart.plotSizeY / maxLength;
                    }
                }
                return nodePadding;
            };
            /**
             * Define hasData function for non-cartesian series.
             * @private
             * @return {boolean}
             *         Returns true if the series has points at all.
             */
            SankeySeries.prototype.hasData = function () {
                return !!this.processedXData.length; // != 0
            };
            /**
             * Return the presentational attributes.
             * @private
             */
            SankeySeries.prototype.pointAttribs = function (point, state) {
                if (!point) {
                    return {};
                }
                var series = this,
                    level = point.isNode ? point.level : point.fromNode.level,
                    levelOptions = series.mapOptionsToLevel[level || 0] || {},
                    options = point.options,
                    stateOptions = (levelOptions.states && levelOptions.states[state || '']) || {},
                    values = [
                        'colorByPoint',
                        'borderColor',
                        'borderWidth',
                        'linkOpacity',
                        'opacity'
                    ].reduce(function (obj,
                    key) {
                        obj[key] = pick(stateOptions[key],
                    options[key],
                    levelOptions[key],
                    series.options[key]);
                    return obj;
                }, {}), color = pick(stateOptions.color, options.color, values.colorByPoint ? point.color : levelOptions.color);
                // Node attributes
                if (point.isNode) {
                    return {
                        fill: color,
                        stroke: values.borderColor,
                        'stroke-width': values.borderWidth,
                        opacity: values.opacity
                    };
                }
                // Link attributes
                return {
                    fill: Color.parse(color).setOpacity(values.linkOpacity).get()
                };
            };
            SankeySeries.prototype.drawTracker = function () {
                ColumnSeries.prototype.drawTracker.call(this, this.points);
                ColumnSeries.prototype.drawTracker.call(this, this.nodes);
            };
            SankeySeries.prototype.drawPoints = function () {
                ColumnSeries.prototype.drawPoints.call(this, this.points);
                ColumnSeries.prototype.drawPoints.call(this, this.nodes);
            };
            SankeySeries.prototype.drawDataLabels = function () {
                ColumnSeries.prototype.drawDataLabels.call(this, this.points);
                ColumnSeries.prototype.drawDataLabels.call(this, this.nodes);
            };
            /**
             * Run pre-translation by generating the nodeColumns.
             * @private
             */
            SankeySeries.prototype.translate = function () {
                if (!this.processedXData) {
                    this.processData();
                }
                this.generatePoints();
                this.nodeColumns = this.createNodeColumns();
                this.nodeWidth = relativeLength(this.options.nodeWidth, this.chart.plotSizeX);
                var series = this,
                    chart = this.chart,
                    options = this.options,
                    nodeWidth = this.nodeWidth,
                    nodeColumns = this.nodeColumns;
                this.nodePadding = this.getNodePadding();
                // Find out how much space is needed. Base it on the translation
                // factor of the most spaceous column.
                this.translationFactor = nodeColumns.reduce(function (translationFactor, column) { return Math.min(translationFactor, column.sankeyColumn.getTranslationFactor(series)); }, Infinity);
                this.colDistance =
                    (chart.plotSizeX - nodeWidth -
                        options.borderWidth) / Math.max(1, nodeColumns.length - 1);
                // Calculate level options used in sankey and organization
                series.mapOptionsToLevel = getLevelOptions({
                    // NOTE: if support for allowTraversingTree is added, then from
                    // should be the level of the root node.
                    from: 1,
                    levels: options.levels,
                    to: nodeColumns.length - 1,
                    defaults: {
                        borderColor: options.borderColor,
                        borderRadius: options.borderRadius,
                        borderWidth: options.borderWidth,
                        color: series.color,
                        colorByPoint: options.colorByPoint,
                        // NOTE: if support for allowTraversingTree is added, then
                        // levelIsConstant should be optional.
                        levelIsConstant: true,
                        linkColor: options.linkColor,
                        linkLineWidth: options.linkLineWidth,
                        linkOpacity: options.linkOpacity,
                        states: options.states
                    }
                });
                // First translate all nodes so we can use them when drawing links
                nodeColumns.forEach(function (column) {
                    column.forEach(function (node) {
                        series.translateNode(node, column);
                    });
                }, this);
                // Then translate links
                this.nodes.forEach(function (node) {
                    // Translate the links from this node
                    node.linksFrom.forEach(function (linkPoint) {
                        // If weight is 0 - don't render the link path #12453,
                        // render null points (for organization chart)
                        if ((linkPoint.weight || linkPoint.isNull) && linkPoint.to) {
                            series.translateLink(linkPoint);
                            linkPoint.allowShadow = false;
                        }
                    });
                });
            };
            /**
             * Run translation operations for one link.
             * @private
             */
            SankeySeries.prototype.translateLink = function (point) {
                var getY = function (node,
                    fromOrTo) {
                        var linkTop = (node.offset(point,
                    fromOrTo) *
                            translationFactor);
                    var y = Math.min(node.nodeY + linkTop, 
                        // Prevent links from spilling below the node (#12014)
                        node.nodeY + (node.shapeArgs && node.shapeArgs.height || 0) - linkHeight);
                    return y;
                };
                var fromNode = point.fromNode, toNode = point.toNode, chart = this.chart, translationFactor = this.translationFactor, linkHeight = Math.max(point.weight * translationFactor, this.options.minLinkWidth), options = this.options, curvy = ((chart.inverted ? -this.colDistance : this.colDistance) *
                        options.curveFactor), fromY = getY(fromNode, 'linksFrom'), toY = getY(toNode, 'linksTo'), nodeLeft = fromNode.nodeX, nodeW = this.nodeWidth, right = toNode.nodeX, outgoing = point.outgoing, straight = right > nodeLeft + nodeW;
                if (chart.inverted) {
                    fromY = chart.plotSizeY - fromY;
                    toY = (chart.plotSizeY || 0) - toY;
                    nodeW = -nodeW;
                    linkHeight = -linkHeight;
                    straight = nodeLeft > right;
                }
                point.shapeType = 'path';
                point.linkBase = [
                    fromY,
                    fromY + linkHeight,
                    toY,
                    toY + linkHeight
                ];
                // Links going from left to right
                if (straight && typeof toY === 'number') {
                    point.shapeArgs = {
                        d: [
                            ['M', nodeLeft + nodeW, fromY],
                            [
                                'C',
                                nodeLeft + nodeW + curvy,
                                fromY,
                                right - curvy,
                                toY,
                                right,
                                toY
                            ],
                            ['L', right + (outgoing ? nodeW : 0), toY + linkHeight / 2],
                            ['L', right, toY + linkHeight],
                            [
                                'C',
                                right - curvy,
                                toY + linkHeight,
                                nodeLeft + nodeW + curvy,
                                fromY + linkHeight,
                                nodeLeft + nodeW, fromY + linkHeight
                            ],
                            ['Z']
                        ]
                    };
                    // Experimental: Circular links pointing backwards. In
                    // v6.1.0 this breaks the rendering completely, so even
                    // this experimental rendering is an improvement. #8218.
                    // @todo
                    // - Make room for the link in the layout
                    // - Automatically determine if the link should go up or
                    //   down.
                }
                else if (typeof toY === 'number') {
                    var bend = 20,
                        vDist = chart.plotHeight - fromY - linkHeight,
                        x1 = right - bend - linkHeight,
                        x2 = right - bend,
                        x3 = right,
                        x4 = nodeLeft + nodeW,
                        x5 = x4 + bend,
                        x6 = x5 + linkHeight,
                        fy1 = fromY,
                        fy2 = fromY + linkHeight,
                        fy3 = fy2 + bend,
                        y4 = fy3 + vDist,
                        y5 = y4 + bend,
                        y6 = y5 + linkHeight,
                        ty1 = toY,
                        ty2 = ty1 + linkHeight,
                        ty3 = ty2 + bend,
                        cfy1 = fy2 - linkHeight * 0.7,
                        cy2 = y5 + linkHeight * 0.7,
                        cty1 = ty2 - linkHeight * 0.7,
                        cx1 = x3 - linkHeight * 0.7,
                        cx2 = x4 + linkHeight * 0.7;
                    point.shapeArgs = {
                        d: [
                            ['M', x4, fy1],
                            ['C', cx2, fy1, x6, cfy1, x6, fy3],
                            ['L', x6, y4],
                            ['C', x6, cy2, cx2, y6, x4, y6],
                            ['L', x3, y6],
                            ['C', cx1, y6, x1, cy2, x1, y4],
                            ['L', x1, ty3],
                            ['C', x1, cty1, cx1, ty1, x3, ty1],
                            ['L', x3, ty2],
                            ['C', x2, ty2, x2, ty2, x2, ty3],
                            ['L', x2, y4],
                            ['C', x2, y5, x2, y5, x3, y5],
                            ['L', x4, y5],
                            ['C', x5, y5, x5, y5, x5, y4],
                            ['L', x5, fy3],
                            ['C', x5, fy2, x5, fy2, x4, fy2],
                            ['Z']
                        ]
                    };
                }
                // Place data labels in the middle
                point.dlBox = {
                    x: nodeLeft + (right - nodeLeft + nodeW) / 2,
                    y: fromY + (toY - fromY) / 2,
                    height: linkHeight,
                    width: 0
                };
                // And set the tooltip anchor in the middle
                point.tooltipPos = chart.inverted ? [
                    chart.plotSizeY - point.dlBox.y - linkHeight / 2,
                    chart.plotSizeX - point.dlBox.x
                ] : [
                    point.dlBox.x,
                    point.dlBox.y + linkHeight / 2
                ];
                // Pass test in drawPoints. plotX/Y needs to be defined for dataLabels.
                // #15863
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
            SankeySeries.prototype.translateNode = function (node, column) {
                var translationFactor = this.translationFactor,
                    chart = this.chart,
                    options = this.options,
                    sum = node.getSum(),
                    nodeHeight = Math.max(Math.round(sum * translationFactor),
                    this.options.minLinkWidth),
                    nodeWidth = Math.round(this.nodeWidth),
                    crisp = Math.round(options.borderWidth) % 2 / 2,
                    nodeOffset = column.sankeyColumn.offset(node,
                    translationFactor),
                    fromNodeTop = Math.floor(pick(nodeOffset.absoluteTop, (column.sankeyColumn.top(translationFactor) +
                        nodeOffset.relativeTop))) + crisp,
                    left = Math.floor(this.colDistance * node.column +
                        options.borderWidth / 2) + relativeLength(node.options.offsetHorizontal || 0,
                    nodeWidth) +
                        crisp,
                    nodeLeft = chart.inverted ?
                        chart.plotSizeX - left :
                        left;
                node.sum = sum;
                // If node sum is 0, don't render the rect #12453
                if (sum) {
                    // Draw the node
                    node.shapeType = 'rect';
                    node.nodeX = nodeLeft;
                    node.nodeY = fromNodeTop;
                    var x = nodeLeft,
                        y = fromNodeTop,
                        width = node.options.width || options.width || nodeWidth,
                        height = node.options.height || options.height || nodeHeight;
                    if (chart.inverted) {
                        x = nodeLeft - nodeWidth;
                        y = chart.plotSizeY - fromNodeTop - nodeHeight;
                        width = node.options.height || options.height || nodeWidth;
                        height = node.options.width || options.width || nodeHeight;
                    }
                    // Calculate data label options for the point
                    node.dlOptions = SankeySeries.getDLOptions({
                        level: this.mapOptionsToLevel[node.level],
                        optionsPoint: node.options
                    });
                    // Pass test in drawPoints
                    node.plotX = 1;
                    node.plotY = 1;
                    // Set the anchor position for tooltips
                    node.tooltipPos = chart.inverted ? [
                        chart.plotSizeY - y - height / 2,
                        chart.plotSizeX - x - width / 2
                    ] : [
                        x + width / 2,
                        y + height / 2
                    ];
                    node.shapeArgs = {
                        x: x,
                        y: y,
                        width: width,
                        height: height,
                        display: node.hasShape() ? '' : 'none'
                    };
                }
                else {
                    node.dlOptions = {
                        enabled: false
                    };
                }
            };
            SankeySeries.defaultOptions = merge(ColumnSeries.defaultOptions, SankeySeriesDefaults);
            return SankeySeries;
        }(ColumnSeries));
        NodesComposition.compose(SankeyPoint, SankeySeries);
        extend(SankeySeries.prototype, {
            animate: Series.prototype.animate,
            // Create a single node that holds information on incoming and outgoing
            // links.
            createNode: NodesComposition.createNode,
            forceDL: true,
            invertible: true,
            isCartesian: false,
            orderNodes: true,
            noSharedTooltip: true,
            pointArrayMap: ['from', 'to', 'weight'],
            pointClass: SankeyPoint,
            searchPoint: H.noop
        });
        SeriesRegistry.registerSeriesType('sankey', SankeySeries);
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
         * A node in a sankey diagram.
         *
         * @interface Highcharts.SankeyNodeObject
         * @extends Highcharts.Point
         * @product highcharts
         */ /**
        * The color of the auto generated node.
        *
        * @name Highcharts.SankeyNodeObject#color
        * @type {Highcharts.ColorString|Highcharts.GradientColorObject|Highcharts.PatternObject}
        */ /**
        * The color index of the auto generated node, especially for use in styled
        * mode.
        *
        * @name Highcharts.SankeyNodeObject#colorIndex
        * @type {number}
        */ /**
        * An optional column index of where to place the node. The default behaviour is
        * to place it next to the preceding node.
        *
        * @see {@link https://jsfiddle.net/gh/get/library/pure/highcharts/highcharts/tree/master/samples/highcharts/plotoptions/sankey-node-column/|Highcharts-Demo:}
        *      Specified node column
        *
        * @name Highcharts.SankeyNodeObject#column
        * @type {number}
        * @since 6.0.5
        */ /**
        * The id of the auto-generated node, refering to the `from` or `to` setting of
        * the link.
        *
        * @name Highcharts.SankeyNodeObject#id
        * @type {string}
        */ /**
        * The name to display for the node in data labels and tooltips. Use this when
        * the name is different from the `id`. Where the id must be unique for each
        * node, this is not necessary for the name.
        *
        * @see {@link https://jsfiddle.net/gh/get/library/pure/highcharts/highcharts/tree/master/samples/highcharts/css/sankey/|Highcharts-Demo:}
        *         Sankey diagram with node options
        *
        * @name Highcharts.SankeyNodeObject#name
        * @type {string}
        * @product highcharts
        */ /**
        * This option is deprecated, use
        * {@link Highcharts.SankeyNodeObject#offsetHorizontal} and
        * {@link Highcharts.SankeyNodeObject#offsetVertical} instead.
        *
        * The vertical offset of a node in terms of weight. Positive values shift the
        * node downwards, negative shift it upwards.
        *
        * If a percantage string is given, the node is offset by the percentage of the
        * node size plus `nodePadding`.
        *
        * @see {@link https://jsfiddle.net/gh/get/library/pure/highcharts/highcharts/tree/master/samples/highcharts/plotoptions/sankey-node-column/|Highcharts-Demo:}
        *         Specified node offset
        *
        * @deprecated
        * @name Highcharts.SankeyNodeObject#offset
        * @type {number|string}
        * @default 0
        * @since 6.0.5
        */ /**
        * The horizontal offset of a node. Positive values shift the node right,
        * negative shift it left.
        *
        * If a percantage string is given, the node is offset by the percentage of the
        * node size.
        *
        * @see {@link https://jsfiddle.net/gh/get/library/pure/highcharts/highcharts/tree/master/samples/highcharts/plotoptions/sankey-node-column/|Highcharts-Demo:}
        *         Specified node offset
        *
        * @name Highcharts.SankeyNodeObject#offsetHorizontal
        * @type {number|string}
        * @since 9.3.0
        */ /**
        * The vertical offset of a node. Positive values shift the node down,
        * negative shift it up.
        *
        * If a percantage string is given, the node is offset by the percentage of the
        * node size.
        *
        * @see {@link https://jsfiddle.net/gh/get/library/pure/highcharts/highcharts/tree/master/samples/highcharts/plotoptions/sankey-node-column/|Highcharts-Demo:}
        *         Specified node offset
        *
        * @name Highcharts.SankeyNodeObject#offsetVertical
        * @type {number|string}
        * @since 9.3.0
        */
        /**
         * Formatter callback function.
         *
         * @callback Highcharts.SeriesSankeyDataLabelsFormatterCallbackFunction
         *
         * @param {Highcharts.SeriesSankeyDataLabelsFormatterContextObject|Highcharts.PointLabelObject} this
         *        Data label context to format
         *
         * @return {string|undefined}
         *         Formatted data label text
         */
        /**
         * Context for the node formatter function.
         *
         * @interface Highcharts.SeriesSankeyDataLabelsFormatterContextObject
         * @extends Highcharts.PointLabelObject
         */ /**
        * The node object. The node name, if defined, is available through
        * `this.point.name`.
        * @name Highcharts.SeriesSankeyDataLabelsFormatterContextObject#point
        * @type {Highcharts.SankeyNodeObject}
        */
        ''; // detach doclets above

        return SankeySeries;
    });
    _registerModule(_modules, 'masters/modules/sankey.src.js', [], function () {


    });
}));