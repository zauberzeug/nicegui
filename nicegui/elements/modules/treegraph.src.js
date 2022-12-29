/**
 * @license Highcharts JS v10.3.2 (2022-11-28)
 * Treegraph chart series type
 *
 *  (c) 2010-2022 Pawel Lysy Grzegorz Blachlinski
 *
 * License: www.highcharts.com/license
 */
(function (factory) {
    if (typeof module === 'object' && module.exports) {
        factory['default'] = factory;
        module.exports = factory;
    } else if (typeof define === 'function' && define.amd) {
        define('highcharts/modules/treegraph', ['highcharts', 'highcharts/modules/treemap'], function (Highcharts) {
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
    _registerModule(_modules, 'Series/PathUtilities.js', [], function () {
        /* *
         *
         *  (c) 2010-2022 Pawel Lysy
         *
         *  License: www.highcharts.com/license
         *
         *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
         *
         * */
        /* *
         *
         *  Functions
         *
         * */
        /**
         * General function to apply corner radius to a path
         * @private
         */
        function curvedPath(path, r) {
            var d = [];
            for (var i = 0; i < path.length; i++) {
                var x = path[i][1];
                var y = path[i][2];
                if (typeof x === 'number' && typeof y === 'number') {
                    // moveTo
                    if (i === 0) {
                        d.push(['M', x, y]);
                    }
                    else if (i === path.length - 1) {
                        d.push(['L', x, y]);
                        // curveTo
                    }
                    else if (r) {
                        var prevSeg = path[i - 1];
                        var nextSeg = path[i + 1];
                        if (prevSeg && nextSeg) {
                            var x1 = prevSeg[1],
                                y1 = prevSeg[2],
                                x2 = nextSeg[1],
                                y2 = nextSeg[2];
                            // Only apply to breaks
                            if (typeof x1 === 'number' &&
                                typeof x2 === 'number' &&
                                typeof y1 === 'number' &&
                                typeof y2 === 'number' &&
                                x1 !== x2 &&
                                y1 !== y2) {
                                var directionX = x1 < x2 ? 1 : -1,
                                    directionY = y1 < y2 ? 1 : -1;
                                d.push([
                                    'L',
                                    x - directionX * Math.min(Math.abs(x - x1), r),
                                    y - directionY * Math.min(Math.abs(y - y1), r)
                                ], [
                                    'C',
                                    x,
                                    y,
                                    x,
                                    y,
                                    x + directionX * Math.min(Math.abs(x - x2), r),
                                    y + directionY * Math.min(Math.abs(y - y2), r)
                                ]);
                            }
                        }
                        // lineTo
                    }
                    else {
                        d.push(['L', x, y]);
                    }
                }
            }
            return d;
        }
        var PathUtilities = {
                curvedPath: curvedPath
            };

        return PathUtilities;
    });
    _registerModule(_modules, 'Series/Treegraph/TreegraphNode.js', [_modules['Core/Series/SeriesRegistry.js']], function (SeriesRegistry) {
        /* *
         *
         *  (c) 2010-2022 Pawel Lysy Grzegorz Blachlinski
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
        var TreemapNode = SeriesRegistry.seriesTypes.treemap.prototype.NodeClass;
        /* *
         *
         *  Class
         *
         * */
        /**
         * @private
         * @class
         */
        var TreegraphNode = /** @class */ (function (_super) {
                __extends(TreegraphNode, _super);
            function TreegraphNode() {
                /* *
                 *
                 *  Properties
                 *
                 * */
                var _this = _super !== null && _super.apply(this,
                    arguments) || this;
                _this.mod = 0;
                _this.shift = 0;
                _this.change = 0;
                _this.children = [];
                _this.preX = 0;
                _this.hidden = false;
                _this.wasVisited = false;
                _this.collapsed = false;
                return _this;
            }
            /* *
             *
             *  Functions
             *
             * */
            /**
             * Get the next left node which is either first child or thread.
             *
             * @return {TreegraphNode|undefined}
             *         Next left node child or thread.
             */
            TreegraphNode.prototype.nextLeft = function () {
                return this.getLeftMostChild() || this.thread;
            };
            /**
             * Get the next right node which is either last child or thread.
             *
             * @return {TreegraphNode|undefined}
             *         Next right node child or thread.
             */
            TreegraphNode.prototype.nextRight = function () {
                return this.getRightMostChild() || this.thread;
            };
            /**
             * Return the left one of the greatest uncommon ancestors of a
             * leftInternal node and it's right neighbor.
             *
             * @param {TreegraphNode} leftIntNode
             * @param {TreegraphNode} defaultAncestor
             * @return {TreegraphNode}
             *         Left one of the greatest uncommon ancestors of a leftInternal
             *         node and it's right neighbor.
             *
             */
            TreegraphNode.prototype.getAncestor = function (leftIntNode, defaultAncestor) {
                var leftAnc = leftIntNode.ancestor;
                if (leftAnc.children[0] === this.children[0]) {
                    return leftIntNode.ancestor;
                }
                return defaultAncestor;
            };
            /**
             * Get node's first sibling, which is not hidden.
             *
             * @return {TreegraphNode|undefined}
             *         First sibling of the node which is not hidden or undefined, if it
             *         does not exists.
             */
            TreegraphNode.prototype.getLeftMostSibling = function () {
                var parent = this.getParent();
                if (parent) {
                    for (var _i = 0, _a = parent.children; _i < _a.length; _i++) {
                        var child = _a[_i];
                        if (child && child.point.visible) {
                            return child;
                        }
                    }
                }
            };
            /**
             * Check if the node is a leaf (if it has any children).
             *
             * @return {boolean}
             *         If the node has no visible children return true.
             */
            TreegraphNode.prototype.hasChildren = function () {
                var children = this.children;
                for (var i = 0; i < children.length; i++) {
                    if (children[i].point.visible) {
                        return true;
                    }
                }
                return false;
            };
            /**
             * Get node's left sibling (if it exists).
             *
             * @return {TreegraphNode|undefined}
             *         Left sibling of the node
             */
            TreegraphNode.prototype.getLeftSibling = function () {
                var parent = this.getParent();
                if (parent) {
                    var children = parent.children;
                    for (var i = this.relativeXPosition - 1; i >= 0; i--) {
                        if (children[i] && children[i].point.visible) {
                            return children[i];
                        }
                    }
                }
            };
            /**
             * Get the node's first child (if it exists).
             *
             * @return {TreegraphNode|undefined}
             *         Node's first child which isn't hidden.
             */
            TreegraphNode.prototype.getLeftMostChild = function () {
                var children = this.children;
                for (var i = 0; i < children.length; i++) {
                    if (children[i].point.visible) {
                        return children[i];
                    }
                }
            };
            /**
             * Get the node's last child (if it exists).
             *
             * @return {TreegraphNode|undefined}
             *         Node's last child which isn't hidden.
             */
            TreegraphNode.prototype.getRightMostChild = function () {
                var children = this.children;
                for (var i = children.length - 1; i >= 0; i--) {
                    if (children[i].point.visible) {
                        return children[i];
                    }
                }
            };
            /**
             * Get the parent of current node or return undefined for root of the
             * tree.
             *
             * @return {TreegraphNode|undefined}
             *         Node's parent or undefined for root.
             */
            TreegraphNode.prototype.getParent = function () {
                return this.parentNode;
            };
            /**
             * Get node's first child which is not hidden.
             *
             * @return {TreegraphNode|undefined}
             *         First child.
             */
            TreegraphNode.prototype.getFirstChild = function () {
                var children = this.children;
                for (var i = 0; i < children.length; i++) {
                    if (children[i].point.visible) {
                        return children[i];
                    }
                }
            };
            return TreegraphNode;
        }(TreemapNode));
        /* *
         *
         *  Default Export
         *
         * */

        return TreegraphNode;
    });
    _registerModule(_modules, 'Series/Treegraph/TreegraphPoint.js', [_modules['Core/Series/Point.js'], _modules['Core/Series/SeriesRegistry.js'], _modules['Core/Utilities.js']], function (Point, SeriesRegistry, U) {
        /* *
         *
         *  (c) 2010-2022 Pawel Lysy Grzegorz Blachlinski
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
        var TreemapPoint = SeriesRegistry.seriesTypes.treemap.prototype.pointClass;
        var addEvent = U.addEvent,
            fireEvent = U.fireEvent,
            merge = U.merge,
            pick = U.pick;
        /* *
         *
         *  Class
         *
         * */
        /**
         * @private
         * @class
         */
        var TreegraphPoint = /** @class */ (function (_super) {
                __extends(TreegraphPoint, _super);
            function TreegraphPoint() {
                /* *
                 *
                 *  Properties
                 *
                 * */
                var _this = _super !== null && _super.apply(this,
                    arguments) || this;
                _this.options = void 0;
                _this.isLink = false;
                _this.series = void 0;
                _this.node = void 0;
                _this.setState = Point.prototype.setState;
                return _this;
            }
            /* *
             *
             *  Functions
             *
             * */
            TreegraphPoint.prototype.draw = function () {
                _super.prototype.draw.apply(this, arguments);
                this.renderCollapseButton();
            };
            TreegraphPoint.prototype.renderCollapseButton = function () {
                var point = this,
                    series = point.series,
                    parentGroup = point.graphic && point.graphic.parentGroup,
                    levelOptions = series.mapOptionsToLevel[point.node.level || 0] || {},
                    btnOptions = merge(series.options.collapseButton,
                    levelOptions.collapseButton,
                    point.series.options.collapseButton),
                    width = btnOptions.width,
                    height = btnOptions.height,
                    shape = btnOptions.shape,
                    style = btnOptions.style,
                    padding = 2,
                    chart = this.series.chart;
                if (!point.shapeArgs) {
                    return;
                }
                this.collapseButtonOptions = btnOptions;
                if (!point.collapseButton) {
                    if (!point.node.children.length || !btnOptions.enabled) {
                        return;
                    }
                    var _a = this.getCollapseBtnPosition(btnOptions),
                        x = _a.x,
                        y = _a.y;
                    point.collapseButton = chart.renderer
                        .label(point.collapsed ? '+' : '-', x, y, shape)
                        .attr({
                        height: height - 2 * padding,
                        width: width - 2 * padding,
                        padding: padding,
                        fill: "#cccccc" /* Palette.neutralColor20 */,
                        rotation: chart.inverted ? 90 : 0,
                        rotationOriginX: width / 2,
                        rotationOriginY: height / 2,
                        stroke: "#333333" /* Palette.neutralColor80 */,
                        'stroke-width': 1,
                        'text-align': 'center',
                        align: 'center',
                        zIndex: 1
                    })
                        .addClass('highcharts-tracker')
                        .addClass('highcharts-collapse-button')
                        .removeClass('highcharts-no-tooltip')
                        .css(style || {})
                        .add(parentGroup);
                    point.collapseButton.element.point = point;
                    if (btnOptions.onlyOnHover && !point.collapsed) {
                        point.collapseButton.hide();
                    }
                }
                else {
                    if (!point.node.children.length || !btnOptions.enabled) {
                        point.collapseButton.destroy();
                        delete point.collapseButton;
                    }
                    else {
                        var _b = this.getCollapseBtnPosition(btnOptions),
                            x = _b.x,
                            y = _b.y;
                        point.collapseButton
                            .attr({
                            text: point.collapsed ? '+' : '-',
                            rotation: chart.inverted ? 90 : 0,
                            rotationOriginX: width / 2,
                            rotationOriginY: height / 2,
                            visibility: point.visible &&
                                (!btnOptions.onlyOnHover ||
                                    point.state === 'hover' ||
                                    point.collapsed) ?
                                'inherit' :
                                'hidden'
                        })
                            .animate({ x: x, y: y });
                    }
                }
            };
            TreegraphPoint.prototype.toggleCollapse = function (state) {
                this.collapsed = pick(state, !this.collapsed);
                fireEvent(this.series, 'toggleCollapse');
                this.series.redraw();
            };
            TreegraphPoint.prototype.shouldDraw = function () {
                return _super.prototype.shouldDraw.call(this) && this.visible;
            };
            TreegraphPoint.prototype.destroy = function () {
                if (this.collapseButton) {
                    this.collapseButton.destroy();
                    delete this.collapseButton;
                    this.collapseButton = void 0;
                }
                _super.prototype.destroy.apply(this, arguments);
            };
            TreegraphPoint.prototype.getCollapseBtnPosition = function (btnOptions) {
                var point = this,
                    chart = point.series.chart,
                    inverted = chart.inverted,
                    btnWidth = btnOptions.width,
                    btnHeight = btnOptions.height,
                    _a = point.shapeArgs || {},
                    _b = _a.x,
                    x = _b === void 0 ? 0 : _b,
                    _c = _a.y,
                    y = _c === void 0 ? 0 : _c,
                    _d = _a.width,
                    width = _d === void 0 ? 0 : _d,
                    _e = _a.height,
                    height = _e === void 0 ? 0 : _e;
                return {
                    x: x +
                        btnOptions.x +
                        (inverted ? -btnHeight * 0.3 : width + btnWidth * -0.3),
                    y: y + height / 2 - btnHeight / 2 + btnOptions.y
                };
            };
            return TreegraphPoint;
        }(TreemapPoint));
        addEvent(TreegraphPoint, 'mouseOut', function () {
            var btn = this.collapseButton,
                btnOptions = this.collapseButtonOptions;
            if (btn && btnOptions && btnOptions.onlyOnHover && !this.collapsed) {
                btn.hide();
            }
        });
        addEvent(TreegraphPoint, 'mouseOver', function () {
            if (this.collapseButton) {
                this.collapseButton.show();
            }
        });
        // Handle showing and hiding of the points
        addEvent(TreegraphPoint, 'click', function () {
            this.toggleCollapse();
        });
        /* *
         *
         *  Export Default
         *
         * */

        return TreegraphPoint;
    });
    _registerModule(_modules, 'Series/Treegraph/TreegraphLink.js', [_modules['Core/Series/Point.js'], _modules['Core/Utilities.js'], _modules['Core/Series/SeriesRegistry.js']], function (Point, U, SeriesRegistry) {
        /* *
         *
         *  (c) 2010-2022 Pawel Lysy Grzegorz Blachlinski
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
        var pick = U.pick,
            extend = U.extend;
        var ColumnPoint = SeriesRegistry.seriesTypes.column.prototype.pointClass;
        /* *
         *
         *  Class
         *
         * */
        /**
         * @private
         * @class
         */
        var LinkPoint = /** @class */ (function (_super) {
                __extends(LinkPoint, _super);
            function LinkPoint() {
                var _this = _super !== null && _super.apply(this,
                    arguments) || this;
                /* *
                *
                *  Class properties
                *
                * */
                _this.isLink = true;
                _this.node = {};
                _this.formatPrefix = 'link';
                _this.dataLabelOnNull = true;
                return _this;
            }
            /* *
             *
             *  Functions
             *
             * */
            LinkPoint.prototype.init = function (series, options, x, point) {
                var link = _super.prototype.init.apply(this,
                    arguments);
                this.formatPrefix = 'link';
                this.dataLabelOnNull = true;
                if (point) {
                    link.fromNode = point.node.parentNode.point;
                    link.visible = point.visible;
                    link.toNode = point;
                    this.id = link.toNode.id + '-' + link.fromNode.id;
                }
                return link;
            };
            LinkPoint.prototype.update = function (options, redraw, animation, runEvent) {
                var oldOptions = {
                        id: this.id,
                        formatPrefix: this.formatPrefix
                    };
                Point.prototype.update.call(this, options, this.isLink ? false : redraw, // Hold the redraw for nodes
                animation, runEvent);
                this.visible = this.toNode.visible;
                extend(this, oldOptions);
                if (pick(redraw, true)) {
                    this.series.chart.redraw(animation);
                }
            };
            return LinkPoint;
        }(ColumnPoint));
        /* *
         *
         *  Export Default
         *
         * */

        return LinkPoint;
    });
    _registerModule(_modules, 'Series/Treegraph/TreegraphLayout.js', [_modules['Series/Treegraph/TreegraphNode.js']], function (TreegraphNode) {
        /* *
         *
         *  (c) 2010-2022 Pawel Lysy Grzegorz Blachlinski
         *
         *  License: www.highcharts.com/license
         *
         *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
         *
         * */
        /* *
         *
         *  Class
         *
         * */
        /**
         * @private
         * @class
         */
        var TreegraphLayout = /** @class */ (function () {
                function TreegraphLayout() {
                }
                /* *
                 *
                 *  Functions
                 *
                 * */
                /**
                 * Create dummy node, which allows to manually set the level of the node.
                 *
                 * @param {TreegraphNode} parent
                 *        Parent node, to which the dummyNode should be connected.
                 * @param {TreegraphNode} child
                 *        Child node, which should be connected to dummyNode.
                 * @param {number} gapSize
                 *        Remainig gap size.
                 * @param {number} index
                 *        The index of the link.
                 *
                 * @return {TreegraphNode}
                 *         DummyNode as a parent of nodes, which column changes.
                 */
                TreegraphLayout.createDummyNode = function (parent, child, gapSize, index) {
                    // Initialise dummy node.
                    var dummyNode = new TreegraphNode();
                dummyNode.id = parent.id + '-' + gapSize;
                dummyNode.ancestor = parent;
                // Add connection from new node to the previous points.
                // First connection to itself.
                dummyNode.children.push(child);
                dummyNode.parent = parent.id;
                dummyNode.parentNode = parent;
                dummyNode.point = child.point;
                dummyNode.level = child.level - gapSize;
                dummyNode.relativeXPosition = child.relativeXPosition;
                dummyNode.visible = child.visible;
                // Then connection from parent to dummyNode.
                parent.children[child.relativeXPosition] = dummyNode;
                child.oldParentNode = parent;
                child.relativeXPosition = 0;
                // Then connection from child to dummyNode.
                child.parentNode = dummyNode;
                child.parent = dummyNode.id;
                return dummyNode;
            };
            /**
             * Walker algorithm of positioning the nodes in the treegraph improved by
             * Buchheim to run in the linear time. Basic algorithm consists of post
             * order traversal, which starts from going bottom up (first walk), and then
             * pre order traversal top to bottom (second walk) where adding all of the
             * modifiers is performed.
             * link to the paper: http://dirk.jivas.de/papers/buchheim02improving.pdf
             *
             * @param {TreegraphSeries} series the Treegraph series
             */
            TreegraphLayout.prototype.calculatePositions = function (series) {
                var treeLayout = this;
                var nodes = series.nodeList;
                this.resetValues(nodes);
                var root = series.tree;
                if (root) {
                    treeLayout.calculateRelativeX(root, 0);
                    treeLayout.beforeLayout(nodes);
                    treeLayout.firstWalk(root);
                    treeLayout.secondWalk(root, -root.preX);
                    treeLayout.afterLayout(nodes);
                }
            };
            /**
             * Create dummyNodes as parents for nodes, which column is changed.
             *
             * @param {Array<TreegraphNode>} nodes
             *        All of the nodes.
             */
            TreegraphLayout.prototype.beforeLayout = function (nodes) {
                for (var _i = 0, nodes_1 = nodes; _i < nodes_1.length; _i++) {
                    var node = nodes_1[_i];
                    var index = 0;
                    for (var _a = 0, _b = node.children; _a < _b.length; _a++) {
                        var child = _b[_a];
                        // Support for children placed in distant columns.
                        if (child && child.level - node.level > 1) {
                            // For further columns treat the nodes as a
                            // single parent-child pairs till the column is achieved.
                            var gapSize = child.level - node.level - 1;
                            // parent -> dummyNode -> child
                            while (gapSize > 0) {
                                child = TreegraphLayout.createDummyNode(node, child, gapSize, index);
                                gapSize--;
                            }
                        }
                        ++index;
                    }
                }
            };
            /**
             * Reset the caluclated values from the previous run.
             * @param {TreegraphNode[]} nodes all of the nodes.
             */
            TreegraphLayout.prototype.resetValues = function (nodes) {
                for (var _i = 0, nodes_2 = nodes; _i < nodes_2.length; _i++) {
                    var node = nodes_2[_i];
                    node.mod = 0;
                    node.ancestor = node;
                    node.shift = 0;
                    node.thread = void 0;
                    node.change = 0;
                    node.preX = 0;
                }
            };
            /**
             * Assigns the value to each node, which indicates, what is his sibling
             * number.
             *
             * @param {TreegraphNode} node
             *        Root node
             * @param {number} index
             *        Index to which the nodes position should be set
             */
            TreegraphLayout.prototype.calculateRelativeX = function (node, index) {
                var treeLayout = this,
                    children = node.children;
                for (var i = 0, iEnd = children.length; i < iEnd; ++i) {
                    treeLayout.calculateRelativeX(children[i], i);
                }
                node.relativeXPosition = index;
            };
            /**
             * Recursive post order traversal of the tree, where the initial position
             * of the nodes is calculated.
             *
             * @param {TreegraphNode} node
             *        The node for which the position should be calculated.
             */
            TreegraphLayout.prototype.firstWalk = function (node) {
                var treeLayout = this, 
                    // Arbitrary value used to position nodes in respect to each other.
                    siblingDistance = 1;
                var leftSibling;
                // If the node is a leaf, set it's position based on the left siblings.
                if (!node.hasChildren()) {
                    leftSibling = node.getLeftSibling();
                    if (leftSibling) {
                        node.preX = leftSibling.preX + siblingDistance;
                        node.mod = node.preX;
                    }
                    else {
                        node.preX = 0;
                    }
                }
                else {
                    // If the node has children, perform the recursive first walk for
                    // its children, and then calculate its shift in the apportion
                    // function (most crucial part part of the algorythm).
                    var defaultAncestor = node.getLeftMostChild();
                    for (var _i = 0, _a = node.children; _i < _a.length; _i++) {
                        var child = _a[_i];
                        treeLayout.firstWalk(child);
                        defaultAncestor = treeLayout.apportion(child, defaultAncestor);
                    }
                    treeLayout.executeShifts(node);
                    var leftChild = node.getLeftMostChild(),
                        rightChild = node.getRightMostChild(), 
                        // Set the position of the parent as a middle point of its
                        // children and move it by the value of the leftSibling (if it
                        // exists).
                        midPoint = (leftChild.preX + rightChild.preX) / 2;
                    leftSibling = node.getLeftSibling();
                    if (leftSibling) {
                        node.preX = leftSibling.preX + siblingDistance;
                        node.mod = node.preX - midPoint;
                    }
                    else {
                        node.preX = midPoint;
                    }
                }
            };
            /**
             * Pre order traversal of the tree, which sets the final xPosition of the
             * node as its preX value and sum of all if it's parents' modifiers.
             *
             * @param {TreegraphNode} node
             *        The node, for which the final position should be calculated.
             * @param {number} modSum
             *        The sum of modifiers of all of the parents.
             */
            TreegraphLayout.prototype.secondWalk = function (node, modSum) {
                var treeLayout = this;
                // When the chart is not inverted we want the tree to be positioned from
                // left to right with root node close to the chart border, this is why
                // x and y positions are switched.
                node.yPosition = node.preX + modSum;
                node.xPosition = node.level;
                for (var _i = 0, _a = node.children; _i < _a.length; _i++) {
                    var child = _a[_i];
                    treeLayout.secondWalk(child, modSum + node.mod);
                }
            };
            /**
             *  Shift all children of the current node from right to left.
             *
             * @param {TreegraphNode} node
             *        The parent node.
             */
            TreegraphLayout.prototype.executeShifts = function (node) {
                var shift = 0,
                    change = 0;
                for (var i = node.children.length - 1; i >= 0; i--) {
                    var childNode = node.children[i];
                    childNode.preX += shift;
                    childNode.mod += shift;
                    change += childNode.change;
                    shift += childNode.shift + change;
                }
            };
            /**
             * The core of the algorithm. The new subtree is combined with the previous
             * subtrees. Threads are used to traverse the inside and outside contours of
             * the left and right subtree up to the highest common level. The vertecies
             * are left(right)Int(Out)node where Int means internal and Out means
             * outernal. For summing up the modifiers along the contour we use the
             * `left(right)Int(Out)mod` variable. Whenever two nodes of the inside
             * contours are in conflict we comute the left one of the greatest uncommon
             * ancestors using the getAncestor function and we call the moveSubtree
             * method to shift the subtree and prepare the shifts of smaller subrtees.
             * Finally we add a new thread (if necessary) and we adjust ancestor of
             * right outernal node or defaultAncestor.
             *
             * @param {TreegraphNode} node
             * @param {TreegraphNode} defaultAncestor
             *        The default ancestor of the passed node.
             */
            TreegraphLayout.prototype.apportion = function (node, defaultAncestor) {
                var treeLayout = this,
                    leftSibling = node.getLeftSibling();
                if (leftSibling) {
                    var rightIntNode = node,
                        rightOutNode = node,
                        leftIntNode = leftSibling,
                        leftOutNode = rightIntNode.getLeftMostSibling(),
                        rightIntMod = rightIntNode.mod,
                        rightOutMod = rightOutNode.mod,
                        leftIntMod = leftIntNode.mod,
                        leftOutMod = leftOutNode.mod;
                    while (leftIntNode &&
                        leftIntNode.nextRight() &&
                        rightIntNode &&
                        rightIntNode.nextLeft()) {
                        leftIntNode = leftIntNode.nextRight();
                        leftOutNode = leftOutNode.nextLeft();
                        rightIntNode = rightIntNode.nextLeft();
                        rightOutNode = rightOutNode.nextRight();
                        rightOutNode.ancestor = node;
                        var siblingDistance = 1,
                            shift = leftIntNode.preX +
                                leftIntMod -
                                (rightIntNode.preX + rightIntMod) +
                                siblingDistance;
                        if (shift > 0) {
                            treeLayout.moveSubtree(node.getAncestor(leftIntNode, defaultAncestor), node, shift);
                            rightIntMod += shift;
                            rightOutMod += shift;
                        }
                        leftIntMod += leftIntNode.mod;
                        rightIntMod += rightIntNode.mod;
                        leftOutMod += leftOutNode.mod;
                        rightOutMod += rightOutNode.mod;
                    }
                    if (leftIntNode &&
                        leftIntNode.nextRight() &&
                        !rightOutNode.nextRight()) {
                        rightOutNode.thread = leftIntNode.nextRight();
                        rightOutNode.mod += leftIntMod - rightOutMod;
                    }
                    if (rightIntNode &&
                        rightIntNode.nextLeft() &&
                        !leftOutNode.nextLeft()) {
                        leftOutNode.thread = rightIntNode.nextLeft();
                        leftOutNode.mod += rightIntMod - leftOutMod;
                    }
                    defaultAncestor = node;
                }
                return defaultAncestor;
            };
            /**
             * Shifts the subtree from leftNode to rightNode.
             *
             * @param {TreegraphNode} leftNode
             * @param {TreegraphNode} rightNode
             * @param {number} shift
             *        The value, by which the subtree should be moved.
             */
            TreegraphLayout.prototype.moveSubtree = function (leftNode, rightNode, shift) {
                var subtrees = rightNode.relativeXPosition - leftNode.relativeXPosition;
                rightNode.change -= shift / subtrees;
                rightNode.shift += shift;
                rightNode.preX += shift;
                rightNode.mod += shift;
                leftNode.change += shift / subtrees;
            };
            /**
             * Clear values created in a beforeLayout.
             *
             * @param {TreegraphNode[]} nodes
             *        All of the nodes of the Treegraph Series.
             */
            TreegraphLayout.prototype.afterLayout = function (nodes) {
                for (var _i = 0, nodes_3 = nodes; _i < nodes_3.length; _i++) {
                    var node = nodes_3[_i];
                    if (node.oldParentNode) {
                        // Restore default connections
                        node.relativeXPosition = node.parentNode.relativeXPosition;
                        node.parent = node.oldParentNode.parent;
                        node.parentNode = node.oldParentNode;
                        // Delete dummyNode
                        delete node.oldParentNode.children[node.relativeXPosition];
                        node.oldParentNode.children[node.relativeXPosition] = node;
                        node.oldParentNode = void 0;
                    }
                }
            };
            return TreegraphLayout;
        }());
        /* *
         *
         *  Default Export
         *
         * */

        return TreegraphLayout;
    });
    _registerModule(_modules, 'Series/Treegraph/TreegraphSeriesDefaults.js', [], function () {
        /* *
         *
         *  (c) 2010-2022 Pawel Lysy Grzegorz Blachlinski
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
         * A treegraph series is a diagram, which shows a relation between ancestors
         * and descendants with a clear parent - child relation.
         * The best examples of the dataStructures, which best reflect this chart
         * are e.g. genealogy tree or directory structure.
         *
         * TODO change back the demo path
         * @sample highcharts/demo/treegraph-chart
         *         Treegraph Chart
         *
         * @extends      plotOptions.treemap
         * @excluding    layoutAlgorithm, dashStyle, linecap, lineWidth,
         *               negativeColor, threshold, zones, zoneAxis, colorAxis,
         *               colorKey, compare, dataGrouping, endAgle, gapSize, gapUnit,
         *               ignoreHiddenPoint, innerSize, joinBy, legendType, linecap,
         *               minSize, navigatorOptions, pointRange, allowTraversingTree,
         *               alternateStartingDirection, borderRadius, breadcrumbs,
         *               interactByLeaf, layoutStartingDirection, levelIsConstant,
         *               lineWidth, negativeColor, nodes, sortIndex, zoneAxis,
         *               zones
         *
         * @product      highcharts
         * @since 10.3.0
         * @requires     modules/treemap.js
         * @requires     modules/treegraph.js
         * @optionparent plotOptions.treegraph
         */
        var TreegraphSeriesDefaults = {
                /**
                 * Flips the positions of the nodes of a treegraph along the
                 * horizontal axis (vertical if chart is inverted).
                 *
                 * @sample highcharts/series-treegraph/reversed-nodes
                 *         Treegraph series with reversed nodes.
                 *
                 * @type    {boolean}
                 * @default false
                 * @product highcharts
                 * @since 10.3.0
                 */
                reversed: false,
                /**
                 * @extends   plotOptions.series.marker
                 * @excluding enabled,
            enabledThreshold
                 */
                marker: {
                    radius: 10,
                    lineWidth: 0,
                    symbol: 'circle',
                    fillOpacity: 1,
                    states: {}
                },
                link: {
                    /**
                     * Modifier of the shape of the curved link. Works best for
                     * values between 0 and 1,
            where 0 is a straight line,
            and 1 is
                     * a shape close to the default one.
                     *
                     * @type      {number}
                     * @default   0.5
                     * @product   highcharts
                     * @since 10.3.0
                     * @apioption series.treegraph.link.curveFactor
                     */
                    /**
                     * The color of the links between nodes.
                     *
                     * @type {Highcharts.ColorString}
                     * @private
                     */
                    color: "#666666" /* Palette.neutralColor60 */,
                    /**
                     * The line width of the links connecting nodes,
            in pixels.
                     * @type {number}
                     *
                     * @private
                     */
                    lineWidth: 1,
                    /**
                     * Radius for the rounded corners of the links between nodes.
                     * Works for `default` link type.
                     *
                     * @private
                     */
                    radius: 10,
                    cursor: 'default',
                    /**
                     * Type of the link shape.
                     *
                     * @sample   highcharts/series-treegraph/link-types
                     *           Different link types
                     *
                     * @type {'default' | 'curved' | 'straight'}
                     * @product highcharts
                     *
                     */
                    type: 'curved'
                },
                /**
                 * Options applied to collapse Button. The collape button is the
                 * small button which indicates,
            that the node is collapsable.
                 */
                collapseButton: {
                    /**
                     * Whether the button should be visible only when the node is
                     * hovered. When set to true,
            the button is hidden for nodes,
                     * which are not collapsed,
            and shown for the collapsed ones.
                     */
                    onlyOnHover: true,
                    /**
                     * Whether the button should be visible.
                     */
                    enabled: true,
                    /**
                     * Offset of the button in the x direction.
                     */
                    x: 0,
                    /**
                     * Offset of the button in the y direction.
                     */
                    y: 0,
                    /**
                     * Height of the button.
                     */
                    height: 10,
                    /**
                     * Width of the button.
                     */
                    width: 10,
                    /**
                     * The symbol of the collapse button.
                     */
                    shape: 'circle'
                    /**
                     * CSS styles for the collapse button.
                     *
                     * In styled mode,
            the collapse button style is given in the
                     * `.highcharts-collapse-button` class.
                     *
                     *
                     * @type      {Highcharts.CSSObject}
                     * @apioption series.treegraph.collapseButton.style
                     */
                },
                /**
                 * @extends plotOptions.series.tooltip
                 */
                tooltip: {
                    /**
                     * The HTML of the point's line in the tooltip. Variables are
                     * enclosed by curly brackets. Available variables are
                     * `point.id`,
            `point.fromNode.id`,
            `point.toNode.id`,
                     * `series.name`,
            `series.color` and other properties on the
                     * same form. Furthermore,
            This can also be overridden for each
                     * series,
            which makes it a good hook for displaying units. In
                     * styled mode,
            the dot is colored by a class name rather than
                     * the point color.
                     *
                     * @type {string}
                     * @since 10.3.0
                     * @product highcharts
                     */
                    linkFormat: '{point.fromNode.id} \u2192 {point.toNode.id}',
                    pointFormat: '{point.id}'
                    /**
                     * A callback function for formatting the HTML output for a
                     * single link in the tooltip. Like the `linkFormat` string,
                     * but with more flexibility.
                     *
                     * @type {Highcharts.FormatterCallbackFunction.<Highcharts.Point>}
                     * @apioption series.treegraph.tooltip.linkFormatter
                     *
                     */
                },
                /**
                 * Options for the data labels appearing on top of the nodes and
                 * links. For treegraph charts,
            data labels are visible for the
                 * nodes by default,
            but hidden for links. This is controlled by
                 * modifying the `nodeFormat`,
            and the `format` that applies to
                 * links and is an empty string by default.
                 *
                 * @declare Highcharts.SeriesTreegraphDataLabelsOptionsObject
                 */
                dataLabels: {
                    /**
                     * Options for a _link_ label text which should follow link
                     * connection. Border and background are disabled for a label
                     * that follows a path.
                     *
                     * **Note:** Only SVG-based renderer supports this option.
                     * Setting `useHTML` to true will disable this option.
                     *
                     * @sample highcharts/series-treegraph/link-text-path
                     *         Treegraph series with link text path dataLabels.
                     *
                     * @extends plotOptions.treegraph.dataLabels.linkTextPath
                     * @since 10.3.0
                     */
                    linkTextPath: {
                        attributes: {
                            startOffset: '50%'
                        }
                    },
                    enabled: true,
                    linkFormatter: function () { return ''; },
                    formatter: function () {
                        return this.point.id;
                }
            }
        };
        /* *
         *
         *  Default Export
         *
         * */

        return TreegraphSeriesDefaults;
    });
    _registerModule(_modules, 'Series/Treegraph/TreegraphSeries.js', [_modules['Series/PathUtilities.js'], _modules['Core/Series/SeriesRegistry.js'], _modules['Core/Renderer/SVG/SVGRenderer.js'], _modules['Series/Treegraph/TreegraphNode.js'], _modules['Series/Treegraph/TreegraphPoint.js'], _modules['Series/TreeUtilities.js'], _modules['Core/Utilities.js'], _modules['Series/Treegraph/TreegraphLink.js'], _modules['Series/Treegraph/TreegraphLayout.js'], _modules['Series/Treegraph/TreegraphSeriesDefaults.js']], function (PU, SeriesRegistry, SVGRenderer, TreegraphNode, TreegraphPoint, TU, U, TreegraphLink, TreegraphLayout, TreegraphSeriesDefaults) {
        /* *
         *
         *  (c) 2010-2022 Pawel Lysy Grzegorz Blachlinski
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
        var curvedPath = PU.curvedPath;
        var seriesProto = SeriesRegistry.series.prototype,
            _a = SeriesRegistry.seriesTypes,
            TreemapSeries = _a.treemap,
            ColumnSeries = _a.column;
        var symbols = SVGRenderer.prototype.symbols;
        var getLevelOptions = TU.getLevelOptions;
        var extend = U.extend,
            isArray = U.isArray,
            merge = U.merge,
            pick = U.pick,
            relativeLength = U.relativeLength;
        /* *
         *
         *  Class
         *
         * */
        /**
         * The Treegraph series type.
         *
         * @private
         * @class
         * @name Highcharts.seriesTypes.treegraph
         *
         * @augments Highcharts.Series
         */
        var TreegraphSeries = /** @class */ (function (_super) {
                __extends(TreegraphSeries, _super);
            function TreegraphSeries() {
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
                _this.layoutModifier = void 0;
                _this.nodeMap = void 0;
                _this.tree = void 0;
                _this.nodeList = [];
                _this.layoutAlgorythm = void 0;
                _this.links = [];
                _this.mapOptionsToLevel = void 0;
                return _this;
            }
            /* *
             *
             *  Functions
             *
             * */
            TreegraphSeries.prototype.init = function () {
                _super.prototype.init.apply(this, arguments);
                this.layoutAlgorythm = new TreegraphLayout();
            };
            /**
             * Calculate `a` and `b` parameters of linear transformation, where
             * `finalPosition = a * calculatedPosition + b`.
             *
             * @return {LayoutModifiers} `a` and `b` parameter for x and y direction.
             */
            TreegraphSeries.prototype.getLayoutModifiers = function () {
                var _this = this;
                var chart = this.chart,
                    series = this,
                    plotSizeX = chart.plotSizeX,
                    plotSizeY = chart.plotSizeY;
                var minX = Infinity,
                    maxX = -Infinity,
                    minY = Infinity,
                    maxY = -Infinity,
                    maxXSize = 0,
                    minXSize = 0,
                    maxYSize = 0,
                    minYSize = 0;
                this.points.forEach(function (point) {
                    var node = point.node,
                        level = series.mapOptionsToLevel[point.node.level] || {},
                        markerOptions = merge(_this.options.marker,
                        level.marker,
                        point.options.marker),
                        radius = relativeLength(markerOptions.radius || 0,
                        Math.min(plotSizeX,
                        plotSizeY)),
                        symbol = markerOptions.symbol,
                        nodeSizeY = (symbol === 'circle' || !markerOptions.height) ?
                            radius * 2 :
                            relativeLength(markerOptions.height,
                        plotSizeY),
                        nodeSizeX = symbol === 'circle' || !markerOptions.width ?
                            radius * 2 :
                            relativeLength(markerOptions.width,
                        plotSizeX);
                    node.nodeSizeX = nodeSizeX;
                    node.nodeSizeY = nodeSizeY;
                    var lineWidth;
                    if (node.xPosition <= minX) {
                        minX = node.xPosition;
                        lineWidth = markerOptions.lineWidth || 0;
                        minXSize = Math.max(nodeSizeX + lineWidth, minXSize);
                    }
                    if (node.xPosition >= maxX) {
                        maxX = node.xPosition;
                        lineWidth = markerOptions.lineWidth || 0;
                        maxXSize = Math.max(nodeSizeX + lineWidth, maxXSize);
                    }
                    if (node.yPosition <= minY) {
                        minY = node.yPosition;
                        lineWidth = markerOptions.lineWidth || 0;
                        minYSize = Math.max(nodeSizeY + lineWidth, minYSize);
                    }
                    if (node.yPosition >= maxY) {
                        maxY = node.yPosition;
                        lineWidth = markerOptions.lineWidth || 0;
                        maxYSize = Math.max(nodeSizeY + lineWidth, maxYSize);
                    }
                });
                // Calculate the values of linear transformation, which will later be
                // applied as `nodePosition = a * x + b` for each direction.
                var ay = maxY === minY ?
                        1 :
                        (plotSizeY - (minYSize + maxYSize) / 2) / (maxY - minY),
                    by = maxY === minY ? plotSizeY / 2 : -ay * minY + minYSize / 2,
                    ax = maxX === minX ?
                        1 :
                        (plotSizeX - (maxXSize + maxXSize) / 2) / (maxX - minX),
                    bx = maxX === minX ? plotSizeX / 2 : -ax * minX + minXSize / 2;
                return { ax: ax, bx: bx, ay: ay, by: by };
            };
            TreegraphSeries.prototype.getLinks = function () {
                var series = this;
                var links = [];
                this.data.forEach(function (point, index) {
                    var levelOptions = series.mapOptionsToLevel[point.node.level || 0] || {};
                    if (point.node.parent) {
                        var pointOptions = merge(levelOptions,
                            point.options);
                        if (!point.linkToParent || !point.linkToParent.update) {
                            var link = new series.LinkClass().init(series,
                                pointOptions,
                                void 0,
                                point);
                            point.linkToParent = link;
                        }
                        else {
                            point.linkToParent.update(pointOptions, false);
                        }
                        point.linkToParent.index = links.push(point.linkToParent) - 1;
                    }
                    else {
                        if (point.linkToParent) {
                            series.links.splice(point.linkToParent.index);
                            point.linkToParent.destroy();
                            delete point.linkToParent;
                        }
                    }
                });
                return links;
            };
            TreegraphSeries.prototype.buildTree = function (id, index, level, list, parent) {
                var point = this.points[index];
                level = (point && point.level) || level;
                return _super.prototype.buildTree.call(this, id, index, level, list, parent);
            };
            TreegraphSeries.prototype.markerAttribs = function () {
                // The super Series.markerAttribs returns { width: NaN, height: NaN },
                // so just disable this for now.
                return {};
            };
            TreegraphSeries.prototype.setCollapsedStatus = function (node, visibility) {
                var _this = this;
                var point = node.point;
                if (point) {
                    // Take the level options into account.
                    point.collapsed = pick(point.collapsed, (this.mapOptionsToLevel[node.level] || {}).collapsed);
                    point.visible = visibility;
                    visibility = visibility === false ? false : !point.collapsed;
                }
                node.children.forEach(function (childNode) {
                    _this.setCollapsedStatus(childNode, visibility);
                });
            };
            TreegraphSeries.prototype.drawTracker = function () {
                ColumnSeries.prototype.drawTracker.apply(this, arguments);
                ColumnSeries.prototype.drawTracker.call(this, this.links);
            };
            /**
             * Run pre-translation by generating the nodeColumns.
             * @private
             */
            TreegraphSeries.prototype.translate = function () {
                var _this = this;
                var series = this,
                    options = series.options;
                // NOTE: updateRootId modifies series.
                var rootId = TU.updateRootId(series),
                    rootNode;
                // Call prototype function
                seriesProto.translate.call(series);
                var tree = series.tree = series.getTree();
                rootNode = series.nodeMap[rootId];
                if (rootId !== '' && (!rootNode || !rootNode.children.length)) {
                    series.setRootNode('', false);
                    rootId = series.rootNode;
                    rootNode = series.nodeMap[rootId];
                }
                series.mapOptionsToLevel = getLevelOptions({
                    from: rootNode.level + 1,
                    levels: options.levels,
                    to: tree.height,
                    defaults: {
                        levelIsConstant: series.options.levelIsConstant,
                        colorByPoint: options.colorByPoint
                    }
                });
                this.setCollapsedStatus(tree, true);
                series.links = series.getLinks();
                series.setTreeValues(tree);
                this.layoutAlgorythm.calculatePositions(series);
                series.layoutModifier = this.getLayoutModifiers();
                this.points.forEach(function (point) {
                    _this.translateNode(point);
                });
                this.points.forEach(function (point) {
                    if (point.linkToParent) {
                        _this.translateLink(point.linkToParent);
                    }
                });
            };
            TreegraphSeries.prototype.translateLink = function (link) {
                var fromNode = link.fromNode,
                    toNode = link.toNode,
                    linkWidth = this.options.link.lineWidth,
                    crisp = (Math.round(linkWidth) % 2) / 2,
                    factor = pick(this.options.link.curveFactor, 0.5),
                    type = pick(link.options.link && link.options.link.type,
                    this.options.link.type);
                if (fromNode.shapeArgs && toNode.shapeArgs) {
                    var fromNodeWidth = (fromNode.shapeArgs.width || 0),
                        inverted = this.chart.inverted,
                        y1 = Math.floor((fromNode.shapeArgs.y || 0) +
                            (fromNode.shapeArgs.height || 0) / 2) + crisp,
                        y2 = Math.floor((toNode.shapeArgs.y || 0) +
                            (toNode.shapeArgs.height || 0) / 2) + crisp;
                    var x1 = Math.floor((fromNode.shapeArgs.x || 0) + fromNodeWidth) +
                            crisp,
                        x2 = Math.floor(toNode.shapeArgs.x || 0) + crisp;
                    if (inverted) {
                        x1 -= fromNodeWidth;
                        x2 += (toNode.shapeArgs.width || 0);
                    }
                    var diff = toNode.node.xPosition - fromNode.node.xPosition;
                    link.shapeType = 'path';
                    var fullWidth = Math.abs(x2 - x1) + fromNodeWidth,
                        width = (fullWidth / diff) - fromNodeWidth,
                        offset = width * factor * (inverted ? -1 : 1);
                    var xMiddle = Math.floor((x2 + x1) / 2) + crisp;
                    link.plotX = xMiddle;
                    link.plotY = y2;
                    if (type === 'straight') {
                        link.shapeArgs = {
                            d: [
                                ['M', x1, y1],
                                ['L', x1 + width * (inverted ? -1 : 1), y2],
                                ['L', x2, y2]
                            ]
                        };
                    }
                    else if (type === 'curved') {
                        link.shapeArgs = {
                            d: [
                                ['M', x1, y1],
                                [
                                    'C',
                                    x1 + offset,
                                    y1,
                                    x1 - offset + width * (inverted ? -1 : 1),
                                    y2,
                                    x1 + width * (inverted ? -1 : 1),
                                    y2
                                ],
                                ['L', x2, y2]
                            ]
                        };
                    }
                    else {
                        link.shapeArgs = {
                            d: curvedPath([
                                ['M', x1, y1],
                                ['L', x1 + width * (inverted ? -0.5 : 0.5), y1],
                                ['L', x1 + width * (inverted ? -0.5 : 0.5), y2],
                                ['L', x2, y2]
                            ], this.options.link.radius)
                        };
                    }
                    link.dlBox = {
                        x: (x1 + x2) / 2,
                        y: (y1 + y2) / 2,
                        height: linkWidth,
                        width: 0
                    };
                    link.tooltipPos = inverted ? [
                        (this.chart.plotSizeY || 0) - link.dlBox.y,
                        (this.chart.plotSizeX || 0) - link.dlBox.x
                    ] : [
                        link.dlBox.x,
                        link.dlBox.y
                    ];
                }
            };
            /**
             * Private method responsible for adjusting the dataLabel options for each
             * node-point individually.
             */
            TreegraphSeries.prototype.drawNodeLabels = function (points) {
                var series = this,
                    mapOptionsToLevel = series.mapOptionsToLevel;
                var options,
                    level;
                for (var _i = 0, points_1 = points; _i < points_1.length; _i++) {
                    var point = points_1[_i];
                    level = mapOptionsToLevel[point.node.level];
                    // Set options to new object to avoid problems with scope
                    options = { style: {} };
                    // If options for level exists, include them as well
                    if (level && level.dataLabels) {
                        options = merge(options, level.dataLabels);
                        series._hasPointLabels = true;
                    }
                    // Set dataLabel width to the width of the point shape.
                    if (point.shapeArgs) {
                        options.style.width = point.shapeArgs.width;
                        if (point.dataLabel) {
                            point.dataLabel.css({
                                width: point.shapeArgs.width + 'px'
                            });
                        }
                    }
                    // Merge custom options with point options
                    point.dlOptions = merge(options, point.options.dataLabels);
                }
                seriesProto.drawDataLabels.call(this, points);
            };
            /**
             * Treegraph has two separate collecions of nodes and lines,
             * render dataLabels for both sets.
             */
            TreegraphSeries.prototype.drawDataLabels = function () {
                if (this.options.dataLabels) {
                    if (!isArray(this.options.dataLabels)) {
                        this.options.dataLabels = [this.options.dataLabels];
                    }
                    // Render node labels.
                    this.drawNodeLabels(this.points);
                    // Render link labels.
                    seriesProto.drawDataLabels.call(this, this.links);
                }
            };
            TreegraphSeries.prototype.destroy = function () {
                // Links must also be destroyed.
                for (var _i = 0, _a = this.links; _i < _a.length; _i++) {
                    var link = _a[_i];
                    link.destroy();
                }
                return seriesProto.destroy.apply(this, arguments);
            };
            /**
             * Return the presentational attributes.
             * @private
             */
            TreegraphSeries.prototype.pointAttribs = function (point, state) {
                var series = this,
                    levelOptions = series.mapOptionsToLevel[point.node.level || 0] || {},
                    options = point.options,
                    stateOptions = (levelOptions.states &&
                        levelOptions.states[state]) ||
                        {};
                point.options.marker = merge(series.options.marker, levelOptions.marker, point.options.marker);
                var borderRadius = pick(stateOptions.borderRadius,
                    options.borderRadius,
                    levelOptions.borderRadius,
                    series.options.borderRadius),
                    linkColor = pick(stateOptions.link && stateOptions.link.color,
                    options.link && options.link.color,
                    levelOptions.link && levelOptions.link.color,
                    series.options.link && series.options.link.color),
                    linkLineWidth = pick(stateOptions.link && stateOptions.link.lineWidth,
                    options.link && options.link.lineWidth,
                    levelOptions.link && levelOptions.link.lineWidth,
                    series.options.link && series.options.link.lineWidth),
                    attribs = seriesProto.pointAttribs.call(series,
                    point,
                    state);
                if (point.isLink) {
                    attribs.stroke = linkColor;
                    attribs['stroke-width'] = linkLineWidth;
                    delete attribs.fill;
                }
                else {
                    if (borderRadius) {
                        attribs.r = borderRadius;
                    }
                }
                return attribs;
            };
            TreegraphSeries.prototype.drawPoints = function () {
                _super.prototype.drawPoints.apply(this, arguments);
                ColumnSeries.prototype.drawPoints.call(this, this.links);
            };
            /**
             * Run translation operations for one node.
             * @private
             */
            TreegraphSeries.prototype.translateNode = function (point) {
                var chart = this.chart,
                    node = point.node,
                    plotSizeY = chart.plotSizeY,
                    plotSizeX = chart.plotSizeX, 
                    // Get the layout modifiers which are common for all nodes.
                    _a = this.layoutModifier,
                    ax = _a.ax,
                    bx = _a.bx,
                    ay = _a.ay,
                    by = _a.by,
                    x = ax * node.xPosition + bx,
                    y = ay * node.yPosition + by,
                    level = this.mapOptionsToLevel[node.level] || {},
                    markerOptions = merge(this.options.marker,
                    level.marker,
                    point.options.marker),
                    symbol = markerOptions.symbol,
                    height = node.nodeSizeY,
                    width = node.nodeSizeX,
                    reversed = this.options.reversed,
                    nodeX = node.x = (chart.inverted ?
                        plotSizeX - width / 2 - x :
                        x - width / 2),
                    nodeY = node.y = (!reversed ?
                        plotSizeY - y - height / 2 :
                        y - height / 2);
                point.shapeType = 'path';
                point.plotX = nodeX;
                point.plotY = nodeY;
                point.shapeArgs = {
                    d: symbols[symbol || 'circle'](nodeX, nodeY, width, height),
                    x: nodeX,
                    y: nodeY,
                    width: width,
                    height: height,
                    cursor: !point.node.isLeaf ? 'pointer' : 'default'
                };
                // Set the anchor position for tooltip.
                point.tooltipPos = chart.inverted ?
                    [plotSizeY - nodeY - height / 2, plotSizeX - nodeX - width / 2] :
                    [nodeX + width / 2, nodeY];
            };
            TreegraphSeries.defaultOptions = merge(TreemapSeries.defaultOptions, TreegraphSeriesDefaults);
            return TreegraphSeries;
        }(TreemapSeries));
        extend(TreegraphSeries.prototype, {
            pointClass: TreegraphPoint,
            NodeClass: TreegraphNode,
            LinkClass: TreegraphLink
        });
        SeriesRegistry.registerSeriesType('treegraph', TreegraphSeries);
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
         * A `treegraph` series. If the [type](#series.treegraph.type)
         * option is not specified, it is inherited from [chart.type](#chart.type).
         *
         * @extends   series,plotOptions.treegraph
         * @exclude   allowDrillToNode, boostBlending, boostThreshold, curveFactor,
         * centerInCategory, connectEnds, connectNulls, colorAxis, colorKey,
         * dataSorting, dragDrop, findNearestPointBy, getExtremesFromAll, layout,
         * nodePadding,  pointInterval, pointIntervalUnit, pointPlacement, pointStart,
         * relativeXValue, softThreshold, stack, stacking, step,
         * traverseUpButton, xAxis, yAxis, zoneAxis, zones
         * @product   highcharts
         * @requires  modules/treemap.js
         * @requires  modules/treegraph.js
         * @apioption series.treegraph
         */
        /**
         * @extends   plotOptions.series.marker
         * @excluding enabled, enabledThreshold
         * @apioption series.treegraph.marker
         */
        /**
         * @type      {Highcharts.SeriesTreegraphDataLabelsOptionsObject|Array<Highcharts.SeriesTreegraphDataLabelsOptionsObject>}
         * @product   highcharts
         * @apioption series.treegraph.data.dataLabels
         */
        /**
         * @sample highcharts/series-treegraph/level-options
         *          Treegraph chart with level options applied
         *
         * @excluding layoutStartingDirection, layoutAlgorithm, colorVariation
         * @apioption series.treegraph.levels
         */
        /**
         * Set collapsed status for nodes level-wise.
         * @type {boolean}
         * @apioption series.treegraph.levels.collapsed
         */
        /**
         * An array of data points for the series. For the `treegraph` series type,
         * points can be given in the following ways:
         *
         * 1. The array of arrays, with `keys` property, which defines how the fields in
         *     array should be interpretated
         *    ```js
         *       keys: ['id', 'parent'],
         *       data: [
         *           ['Category1'],
         *           ['Category1', 'Category2']
         *       ]
         *
         * 2. An array of objects with named values. The following snippet shows only a
         *    few settings, see the complete options set below. If the total number of
         *    data points exceeds the
         *    series' [turboThreshold](#series.area.turboThreshold),
         *    this option is not available.
         *    The data of the treegraph series needs to be formatted in such a way, that
         *    there are no circular dependencies on the nodes
         *
         *  ```js
         *     data: [{
         *         id: 'Category1'
         *     }, {
         *         id: 'Category1',
         *         parent: 'Category2',
         *     }]
         *  ```
         *
         * @type      {Array<*>}
         * @extends   series.treemap.data
         * @product   highcharts
         * @excluding outgoing, weight, value
         * @apioption series.treegraph.data
         */
        /**
         * Options used for button, which toggles the collapse status of the node.
         *
         *
         * @apioption series.treegraph.data.collapseButton
         */
        /**
         * If point's children should be initially hidden
         *
         * @sample highcharts/series-treegraph/level-options
         *          Treegraph chart with initially hidden children
         *
         * @type {boolean}
         * @apioption series.treegraph.data.collapsed
         */
        ''; // gets doclets above into transpiled version

        return TreegraphSeries;
    });
    _registerModule(_modules, 'masters/modules/treegraph.src.js', [], function () {


    });
}));