/**
 * @license Highcharts JS v10.3.2 (2022-11-28)
 *
 * (c) 2016-2021 Highsoft AS
 * Authors: Jon Arild Nygard
 *
 * License: www.highcharts.com/license
 */
(function (factory) {
    if (typeof module === 'object' && module.exports) {
        factory['default'] = factory;
        module.exports = factory;
    } else if (typeof define === 'function' && define.amd) {
        define('highcharts/modules/sunburst', ['highcharts'], function (Highcharts) {
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
    _registerModule(_modules, 'Series/ColorMapComposition.js', [_modules['Core/Series/SeriesRegistry.js'], _modules['Core/Utilities.js']], function (SeriesRegistry, U) {
        /* *
         *
         *  (c) 2010-2021 Torstein Honsi
         *
         *  License: www.highcharts.com/license
         *
         *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
         *
         * */
        var columnProto = SeriesRegistry.seriesTypes.column.prototype;
        var addEvent = U.addEvent,
            defined = U.defined;
        /* *
         *
         *  Composition
         *
         * */
        var ColorMapComposition;
        (function (ColorMapComposition) {
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
            ColorMapComposition.pointMembers = {
                dataLabelOnNull: true,
                moveToTopOnHover: true,
                isValid: pointIsValid
            };
            ColorMapComposition.seriesMembers = {
                colorKey: 'value',
                axisTypes: ['xAxis', 'yAxis', 'colorAxis'],
                parallelArrays: ['x', 'y', 'value'],
                pointArrayMap: ['value'],
                trackerGroups: ['group', 'markerGroup', 'dataLabelsGroup'],
                colorAttribs: seriesColorAttribs,
                pointAttribs: columnProto.pointAttribs
            };
            /* *
             *
             *  Functions
             *
             * */
            /**
             * @private
             */
            function compose(SeriesClass) {
                var PointClass = SeriesClass.prototype.pointClass;
                if (composedClasses.indexOf(PointClass) === -1) {
                    composedClasses.push(PointClass);
                    addEvent(PointClass, 'afterSetState', onPointAfterSetState);
                }
                return SeriesClass;
            }
            ColorMapComposition.compose = compose;
            /**
             * Move points to the top of the z-index order when hovered.
             * @private
             */
            function onPointAfterSetState(e) {
                var point = this;
                if (point.moveToTopOnHover && point.graphic) {
                    point.graphic.attr({
                        zIndex: e && e.state === 'hover' ? 1 : 0
                    });
                }
            }
            /**
             * Color points have a value option that determines whether or not it is
             * a null point
             * @private
             */
            function pointIsValid() {
                return (this.value !== null &&
                    this.value !== Infinity &&
                    this.value !== -Infinity &&
                    // undefined is allowed, but NaN is not (#17279)
                    (this.value === void 0 || !isNaN(this.value)));
            }
            /**
             * Get the color attibutes to apply on the graphic
             * @private
             * @function Highcharts.colorMapSeriesMixin.colorAttribs
             * @param {Highcharts.Point} point
             * @return {Highcharts.SVGAttributes}
             *         The SVG attributes
             */
            function seriesColorAttribs(point) {
                var ret = {};
                if (defined(point.color) &&
                    (!point.state || point.state === 'normal') // #15746
                ) {
                    ret[this.colorProp || 'fill'] = point.color;
                }
                return ret;
            }
        })(ColorMapComposition || (ColorMapComposition = {}));
        /* *
         *
         *  Default Export
         *
         * */

        return ColorMapComposition;
    });
    _registerModule(_modules, 'Series/Treemap/TreemapAlgorithmGroup.js', [], function () {
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
        /* *
         *
         *  Class
         *
         * */
        var TreemapAlgorithmGroup = /** @class */ (function () {
                /* *
                 *
                 *  Constructor
                 *
                 * */
                function TreemapAlgorithmGroup(h, w, d, p) {
                    this.height = h;
                this.width = w;
                this.plot = p;
                this.direction = d;
                this.startDirection = d;
                this.total = 0;
                this.nW = 0;
                this.lW = 0;
                this.nH = 0;
                this.lH = 0;
                this.elArr = [];
                this.lP = {
                    total: 0,
                    lH: 0,
                    nH: 0,
                    lW: 0,
                    nW: 0,
                    nR: 0,
                    lR: 0,
                    aspectRatio: function (w, h) {
                        return Math.max((w / h), (h / w));
                    }
                };
            }
            /* *
             *
             *  Functions
             *
             * */
            /* eslint-disable valid-jsdoc */
            TreemapAlgorithmGroup.prototype.addElement = function (el) {
                this.lP.total = this.elArr[this.elArr.length - 1];
                this.total = this.total + el;
                if (this.direction === 0) {
                    // Calculate last point old aspect ratio
                    this.lW = this.nW;
                    this.lP.lH = this.lP.total / this.lW;
                    this.lP.lR = this.lP.aspectRatio(this.lW, this.lP.lH);
                    // Calculate last point new aspect ratio
                    this.nW = this.total / this.height;
                    this.lP.nH = this.lP.total / this.nW;
                    this.lP.nR = this.lP.aspectRatio(this.nW, this.lP.nH);
                }
                else {
                    // Calculate last point old aspect ratio
                    this.lH = this.nH;
                    this.lP.lW = this.lP.total / this.lH;
                    this.lP.lR = this.lP.aspectRatio(this.lP.lW, this.lH);
                    // Calculate last point new aspect ratio
                    this.nH = this.total / this.width;
                    this.lP.nW = this.lP.total / this.nH;
                    this.lP.nR = this.lP.aspectRatio(this.lP.nW, this.nH);
                }
                this.elArr.push(el);
            };
            TreemapAlgorithmGroup.prototype.reset = function () {
                this.nW = 0;
                this.lW = 0;
                this.elArr = [];
                this.total = 0;
            };
            return TreemapAlgorithmGroup;
        }());
        /* *
         *
         *  Default Export
         *
         * */

        return TreemapAlgorithmGroup;
    });
    _registerModule(_modules, 'Series/DrawPointUtilities.js', [_modules['Core/Utilities.js']], function (U) {
        /* *
         *
         *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
         *
         * */
        var isNumber = U.isNumber;
        /* *
         *
         *  Functions
         *
         * */
        /**
         * Handles the drawing of a component.
         * Can be used for any type of component that reserves the graphic property,
         * and provides a shouldDraw on its context.
         *
         * @private
         *
         * @todo add type checking.
         * @todo export this function to enable usage
         */
        function draw(point, params) {
            var animatableAttribs = params.animatableAttribs,
                onComplete = params.onComplete,
                css = params.css,
                renderer = params.renderer;
            var animation = (point.series && point.series.chart.hasRendered) ?
                    // Chart-level animation on updates
                    void 0 :
                    // Series-level animation on new points
                    (point.series &&
                        point.series.options.animation);
            var graphic = point.graphic;
            params.attribs = params.attribs || {};
            // Assigning class in dot notation does go well in IE8
            // eslint-disable-next-line dot-notation
            params.attribs['class'] = point.getClassName();
            if ((point.shouldDraw())) {
                if (!graphic) {
                    point.graphic = graphic = params.shapeType === 'text' ?
                        renderer.text() :
                        renderer[params.shapeType](params.shapeArgs || {});
                    graphic.add(params.group);
                }
                if (css) {
                    graphic.css(css);
                }
                graphic
                    .attr(params.attribs)
                    .animate(animatableAttribs, params.isNew ? false : animation, onComplete);
            }
            else if (graphic) {
                var destroy_1 = function () {
                        point.graphic = graphic = (graphic && graphic.destroy());
                    if (typeof onComplete === 'function') {
                        onComplete();
                    }
                };
                // animate only runs complete callback if something was animated.
                if (Object.keys(animatableAttribs).length) {
                    graphic.animate(animatableAttribs, void 0, function () { return destroy_1(); });
                }
                else {
                    destroy_1();
                }
            }
        }
        /* *
         *
         *  Default Export
         *
         * */
        var DrawPointUtilities = {
                draw: draw
            };

        return DrawPointUtilities;
    });
    _registerModule(_modules, 'Series/Treemap/TreemapPoint.js', [_modules['Series/DrawPointUtilities.js'], _modules['Core/Series/SeriesRegistry.js'], _modules['Core/Utilities.js']], function (DPU, SeriesRegistry, U) {
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
        var Point = SeriesRegistry.series.prototype.pointClass,
            _a = SeriesRegistry.seriesTypes,
            PiePoint = _a.pie.prototype.pointClass,
            ScatterPoint = _a.scatter.prototype.pointClass;
        var extend = U.extend,
            isNumber = U.isNumber,
            pick = U.pick;
        /* *
         *
         *  Class
         *
         * */
        var TreemapPoint = /** @class */ (function (_super) {
                __extends(TreemapPoint, _super);
            function TreemapPoint() {
                /* *
                 *
                 *  Properties
                 *
                 * */
                var _this = _super !== null && _super.apply(this,
                    arguments) || this;
                _this.name = void 0;
                _this.node = void 0;
                _this.options = void 0;
                _this.series = void 0;
                _this.shapeType = 'rect';
                _this.value = void 0;
                return _this;
                /* eslint-enable valid-jsdoc */
            }
            /* *
             *
             *  Functions
             *
             * */
            /* eslint-disable valid-jsdoc */
            TreemapPoint.prototype.draw = function (params) {
                DPU.draw(this, params);
            };
            TreemapPoint.prototype.getClassName = function () {
                var className = Point.prototype.getClassName.call(this),
                    series = this.series,
                    options = series.options;
                // Above the current level
                if (this.node.level <= series.nodeMap[series.rootNode].level) {
                    className += ' highcharts-above-level';
                }
                else if (!this.node.isLeaf &&
                    !pick(options.interactByLeaf, !options.allowTraversingTree)) {
                    className += ' highcharts-internal-node-interactive';
                }
                else if (!this.node.isLeaf) {
                    className += ' highcharts-internal-node';
                }
                return className;
            };
            /**
             * A tree point is valid if it has han id too, assume it may be a parent
             * item.
             *
             * @private
             * @function Highcharts.Point#isValid
             */
            TreemapPoint.prototype.isValid = function () {
                return Boolean(this.id || isNumber(this.value));
            };
            TreemapPoint.prototype.setState = function (state) {
                Point.prototype.setState.call(this, state);
                // Graphic does not exist when point is not visible.
                if (this.graphic) {
                    this.graphic.attr({
                        zIndex: state === 'hover' ? 1 : 0
                    });
                }
            };
            TreemapPoint.prototype.shouldDraw = function () {
                return isNumber(this.plotY) && this.y !== null;
            };
            return TreemapPoint;
        }(ScatterPoint));
        extend(TreemapPoint.prototype, {
            setVisible: PiePoint.prototype.setVisible
        });
        /* *
         *
         *  Default Export
         *
         * */

        return TreemapPoint;
    });
    _registerModule(_modules, 'Series/Treemap/TreemapUtilities.js', [_modules['Core/Utilities.js']], function (U) {
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
        /* *
         *
         *  Imports
         *
         * */
        var objectEach = U.objectEach;
        /* *
         *
         *  Namespace
         *
         * */
        var TreemapUtilities;
        (function (TreemapUtilities) {
            TreemapUtilities.AXIS_MAX = 100;
            /* eslint-disable no-invalid-this, valid-jsdoc */
            /**
             * @todo Similar to eachObject, this function is likely redundant
             */
            function isBoolean(x) {
                return typeof x === 'boolean';
            }
            TreemapUtilities.isBoolean = isBoolean;
            /**
             * @todo Similar to recursive, this function is likely redundant
             */
            function eachObject(list, func, context) {
                context = context || this;
                objectEach(list, function (val, key) {
                    func.call(context, val, key, list);
                });
            }
            TreemapUtilities.eachObject = eachObject;
            /**
             * @todo find correct name for this function.
             * @todo Similar to reduce, this function is likely redundant
             */
            function recursive(item, func, context) {
                if (context === void 0) { context = this; }
                var next;
                next = func.call(context, item);
                if (next !== false) {
                    recursive(next, func, context);
                }
            }
            TreemapUtilities.recursive = recursive;
        })(TreemapUtilities || (TreemapUtilities = {}));
        /* *
         *
         *  Default Export
         *
         * */

        return TreemapUtilities;
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
    _registerModule(_modules, 'Extensions/Breadcrumbs.js', [_modules['Core/Chart/Chart.js'], _modules['Core/Defaults.js'], _modules['Core/Globals.js'], _modules['Core/Utilities.js'], _modules['Core/FormatUtilities.js']], function (Chart, D, H, U, F) {
        /* *
         *
         *  Highcharts Breadcrumbs module
         *
         *  Authors: Grzegorz Blachlinski, Karol Kolodziej
         *
         *  License: www.highcharts.com/license
         *
         *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
         *
         * */
        var defaultOptions = D.defaultOptions;
        var format = F.format;
        var addEvent = U.addEvent,
            objectEach = U.objectEach,
            extend = U.extend,
            fireEvent = U.fireEvent,
            merge = U.merge,
            pick = U.pick,
            defined = U.defined,
            isString = U.isString;
        // Add language support.
        extend(defaultOptions.lang, 
        /**
         * @optionparent lang
         *
         * @private
         */
        {
            /**
             * @since 10.0.0
             * @product  highcharts
             *
             * @private
             */
            mainBreadcrumb: 'Main'
        });
        /**
         * The Breadcrumbs class
         *
         * @private
         * @class
         * @name Highcharts.Breadcrumbs
         *
         * @param {Highcharts.Chart} chart
         *        Chart object
         * @param {Highcharts.Options} userOptions
         *        User options
         */
        var Breadcrumbs = /** @class */ (function () {
                function Breadcrumbs(chart, userOptions) {
                    /* *
                     *
                     * Properties
                     *
                     * */
                    this.group = void 0;
                this.list = [];
                this.elementList = {};
                this.isDirty = true;
                this.level = 0;
                this.options = void 0;
                var chartOptions = merge(chart.options.drilldown &&
                        chart.options.drilldown.drillUpButton,
                    Breadcrumbs.defaultBreadcrumbsOptions,
                    chart.options.navigation && chart.options.navigation.breadcrumbs,
                    userOptions);
                this.chart = chart;
                this.options = chartOptions || {};
            }
            /**
             * Update Breadcrumbs properties, like level and list.
             *
             * @requires  modules/breadcrumbs
             *
             * @function Highcharts.Breadcrumbs#updateProperties
             * @param {Highcharts.Breadcrumbs} this
             *        Breadcrumbs class.
             */
            Breadcrumbs.prototype.updateProperties = function (list) {
                this.setList(list);
                this.setLevel();
                this.isDirty = true;
            };
            /**
             * Set breadcrumbs list.
             * @function Highcharts.Breadcrumbs#setList
             *
             * @requires  modules/breadcrumbs
             *
             * @param {Highcharts.Breadcrumbs} this
             *        Breadcrumbs class.
             * @param {Highcharts.BreadcrumbsOptions} list
             *        Breadcrumbs list.
             */
            Breadcrumbs.prototype.setList = function (list) {
                this.list = list;
            };
            /**
             * Calcule level on which chart currently is.
             *
             * @requires  modules/breadcrumbs
             *
             * @function Highcharts.Breadcrumbs#setLevel
             * @param {Highcharts.Breadcrumbs} this
             *        Breadcrumbs class.
             */
            Breadcrumbs.prototype.setLevel = function () {
                this.level = this.list.length && this.list.length - 1;
            };
            /**
             * Get Breadcrumbs level
             *
             * @requires  modules/breadcrumbs
             *
             * @function Highcharts.Breadcrumbs#getLevel
             * @param {Highcharts.Breadcrumbs} this
             *        Breadcrumbs class.
             */
            Breadcrumbs.prototype.getLevel = function () {
                return this.level;
            };
            /**
             * Default button text formatter.
             *
             * @requires  modules/breadcrumbs
             *
             * @function Highcharts.Breadcrumbs#getButtonText
             * @param {Highcharts.Breadcrumbs} this
             *        Breadcrumbs class.
             * @param {Highcharts.Breadcrumbs} breadcrumb
             *        Breadcrumb.
             * @return {string}
             *         Formatted text.
             */
            Breadcrumbs.prototype.getButtonText = function (breadcrumb) {
                var breadcrumbs = this,
                    chart = breadcrumbs.chart,
                    breadcrumbsOptions = breadcrumbs.options,
                    lang = chart.options.lang,
                    textFormat = pick(breadcrumbsOptions.format,
                    breadcrumbsOptions.showFullPath ?
                        '{level.name}' : '← {level.name}'),
                    defaultText = lang && pick(lang.drillUpText,
                    lang.mainBreadcrumb);
                var returnText = breadcrumbsOptions.formatter &&
                        breadcrumbsOptions.formatter(breadcrumb) ||
                        format(textFormat, { level: breadcrumb.levelOptions },
                    chart) || '';
                if (((isString(returnText) &&
                    !returnText.length) ||
                    returnText === '← ') &&
                    defined(defaultText)) {
                    returnText = !breadcrumbsOptions.showFullPath ?
                        '← ' + defaultText :
                        defaultText;
                }
                return returnText;
            };
            /**
             * Redraw.
             *
             * @requires  modules/breadcrums
             *
             * @function Highcharts.Breadcrumbs#redraw
             * @param {Highcharts.Breadcrumbs} this
             *        Breadcrumbs class.
             */
            Breadcrumbs.prototype.redraw = function () {
                if (this.isDirty) {
                    this.render();
                }
                if (this.group) {
                    this.group.align();
                }
                this.isDirty = false;
            };
            /**
             * Create a group, then draw breadcrumbs together with the separators.
             *
             * @requires  modules/breadcrumbs
             *
             * @function Highcharts.Breadcrumbs#render
             * @param {Highcharts.Breadcrumbs} this
             *        Breadcrumbs class.
             */
            Breadcrumbs.prototype.render = function () {
                var breadcrumbs = this,
                    chart = breadcrumbs.chart,
                    breadcrumbsOptions = breadcrumbs.options;
                // A main group for the breadcrumbs.
                if (!breadcrumbs.group && breadcrumbsOptions) {
                    breadcrumbs.group = chart.renderer
                        .g('breadcrumbs-group')
                        .addClass('highcharts-no-tooltip highcharts-breadcrumbs')
                        .attr({
                        zIndex: breadcrumbsOptions.zIndex
                    })
                        .add();
                }
                // Draw breadcrumbs.
                if (breadcrumbsOptions.showFullPath) {
                    this.renderFullPathButtons();
                }
                else {
                    this.renderSingleButton();
                }
                this.alignBreadcrumbsGroup();
            };
            /**
             * Draw breadcrumbs together with the separators.
             *
             * @requires  modules/breadcrumbs
             *
             * @function Highcharts.Breadcrumbs#renderFullPathButtons
             * @param {Highcharts.Breadcrumbs} this
             *        Breadcrumbs class.
             */
            Breadcrumbs.prototype.renderFullPathButtons = function () {
                // Make sure that only one type of button is visible.
                this.destroySingleButton();
                this.resetElementListState();
                this.updateListElements();
                this.destroyListElements();
            };
            /**
             * Render Single button - when showFullPath is not used. The button is
             * similar to the old drillUpButton
             *
             * @requires  modules/breadcrumbs
             *
             * @function Highcharts.Breadcrumbs#renderSingleButton
             * @param {Highcharts.Breadcrumbs} this Breadcrumbs class.
             */
            Breadcrumbs.prototype.renderSingleButton = function () {
                var breadcrumbs = this,
                    chart = breadcrumbs.chart,
                    list = breadcrumbs.list,
                    breadcrumbsOptions = breadcrumbs.options,
                    buttonSpacing = breadcrumbsOptions.buttonSpacing;
                // Make sure that only one type of button is visible.
                this.destroyListElements();
                // Draw breadcrumbs. Inital position for calculating the breadcrumbs
                // group.
                var posX = breadcrumbs.group ?
                        breadcrumbs.group.getBBox().width :
                        buttonSpacing,
                    posY = buttonSpacing;
                var previousBreadcrumb = list[list.length - 2];
                if (!chart.drillUpButton && (this.level > 0)) {
                    chart.drillUpButton = breadcrumbs.renderButton(previousBreadcrumb, posX, posY);
                }
                else if (chart.drillUpButton) {
                    if (this.level > 0) {
                        // Update button.
                        this.updateSingleButton();
                    }
                    else {
                        this.destroySingleButton();
                    }
                }
            };
            /**
             * Update group position based on align and it's width.
             *
             * @requires  modules/breadcrumbs
             *
             * @function Highcharts.Breadcrumbs#renderSingleButton
             * @param {Highcharts.Breadcrumbs} this
             *        Breadcrumbs class.
             */
            Breadcrumbs.prototype.alignBreadcrumbsGroup = function (xOffset) {
                var breadcrumbs = this;
                if (breadcrumbs.group) {
                    var breadcrumbsOptions = breadcrumbs.options,
                        buttonTheme = breadcrumbsOptions.buttonTheme,
                        positionOptions = breadcrumbsOptions.position,
                        alignTo = (breadcrumbsOptions.relativeTo === 'chart' ||
                            breadcrumbsOptions.relativeTo === 'spacingBox' ?
                            void 0 :
                            'scrollablePlotBox'),
                        bBox = breadcrumbs.group.getBBox(),
                        additionalSpace = 2 * (buttonTheme.padding || 0) +
                            breadcrumbsOptions.buttonSpacing;
                    // Store positionOptions
                    positionOptions.width = bBox.width + additionalSpace;
                    positionOptions.height = bBox.height + additionalSpace;
                    var newPositions = merge(positionOptions);
                    // Add x offset if specified.
                    if (xOffset) {
                        newPositions.x += xOffset;
                    }
                    if (breadcrumbs.options.rtl) {
                        newPositions.x += positionOptions.width;
                    }
                    newPositions.y = pick(newPositions.y, this.yOffset, 0);
                    breadcrumbs.group.align(newPositions, true, alignTo);
                }
            };
            /**
             * Render a button.
             *
             * @requires  modules/breadcrums
             *
             * @function Highcharts.Breadcrumbs#renderButton
             * @param {Highcharts.Breadcrumbs} this
             *        Breadcrumbs class.
             * @param {Highcharts.Breadcrumbs} breadcrumb
             *        Current breadcrumb
             * @param {Highcharts.Breadcrumbs} posX
             *        Initial horizontal position
             * @param {Highcharts.Breadcrumbs} posY
             *        Initial vertical position
             * @return {SVGElement|void}
             *        Returns the SVG button
             */
            Breadcrumbs.prototype.renderButton = function (breadcrumb, posX, posY) {
                var breadcrumbs = this,
                    chart = this.chart,
                    breadcrumbsOptions = breadcrumbs.options,
                    buttonTheme = merge(breadcrumbsOptions.buttonTheme);
                var button = chart.renderer
                        .button(breadcrumbs.getButtonText(breadcrumb),
                    posX,
                    posY,
                    function (e) {
                        // Extract events from button object and call
                        var buttonEvents = breadcrumbsOptions.events &&
                            breadcrumbsOptions.events.click;
                    var callDefaultEvent;
                    if (buttonEvents) {
                        callDefaultEvent = buttonEvents.call(breadcrumbs, e, breadcrumb);
                    }
                    // (difference in behaviour of showFullPath and drillUp)
                    if (callDefaultEvent !== false) {
                        // For single button we are not going to the button
                        // level, but the one level up
                        if (!breadcrumbsOptions.showFullPath) {
                            e.newLevel = breadcrumbs.level - 1;
                        }
                        else {
                            e.newLevel = breadcrumb.level;
                        }
                        fireEvent(breadcrumbs, 'up', e);
                    }
                }, buttonTheme)
                    .addClass('highcharts-breadcrumbs-button')
                    .add(breadcrumbs.group);
                if (!chart.styledMode) {
                    button.attr(breadcrumbsOptions.style);
                }
                return button;
            };
            /**
             * Render a separator.
             *
             * @requires  modules/breadcrums
             *
             * @function Highcharts.Breadcrumbs#renderSeparator
             * @param {Highcharts.Breadcrumbs} this
             *        Breadcrumbs class.
             * @param {Highcharts.Breadcrumbs} posX
             *        Initial horizontal position
             * @param {Highcharts.Breadcrumbs} posY
             *        Initial vertical position
             * @return {Highcharts.SVGElement}
             *        Returns the SVG button
             */
            Breadcrumbs.prototype.renderSeparator = function (posX, posY) {
                var breadcrumbs = this,
                    chart = this.chart,
                    breadcrumbsOptions = breadcrumbs.options,
                    separatorOptions = breadcrumbsOptions.separator;
                var separator = chart.renderer
                        .label(separatorOptions.text,
                    posX,
                    posY,
                    void 0,
                    void 0,
                    void 0,
                    false)
                        .addClass('highcharts-breadcrumbs-separator')
                        .add(breadcrumbs.group);
                if (!chart.styledMode) {
                    separator.css(separatorOptions.style);
                }
                return separator;
            };
            /**
             * Update.
             * @function Highcharts.Breadcrumbs#update
             *
             * @requires  modules/breadcrumbs
             *
             * @param {Highcharts.Breadcrumbs} this
             *        Breadcrumbs class.
             * @param {Highcharts.BreadcrumbsOptions} options
             *        Breadcrumbs class.
             * @param {boolean} redraw
             *        Redraw flag
             */
            Breadcrumbs.prototype.update = function (options) {
                merge(true, this.options, options);
                this.destroy();
                this.isDirty = true;
            };
            /**
             * Update button text when the showFullPath set to false.
             * @function Highcharts.Breadcrumbs#updateSingleButton
             *
             * @requires  modules/breadcrumbs
             *
             * @param {Highcharts.Breadcrumbs} this
             *        Breadcrumbs class.
             */
            Breadcrumbs.prototype.updateSingleButton = function () {
                var chart = this.chart,
                    currentBreadcrumb = this.list[this.level - 1];
                if (chart.drillUpButton) {
                    chart.drillUpButton.attr({
                        text: this.getButtonText(currentBreadcrumb)
                    });
                }
            };
            /**
             * Destroy the chosen breadcrumbs group
             *
             * @requires  modules/breadcrumbs
             *
             * @function Highcharts.Breadcrumbs#destroy
             * @param {Highcharts.Breadcrumbs} this
             *        Breadcrumbs class.
             */
            Breadcrumbs.prototype.destroy = function () {
                this.destroySingleButton();
                // Destroy elements one by one. It's necessary beacause
                // g().destroy() does not remove added HTML
                this.destroyListElements(true);
                // Then, destroy the group itself.
                if (this.group) {
                    this.group.destroy();
                }
                this.group = void 0;
            };
            /**
             * Destroy the elements' buttons and separators.
             *
             * @requires  modules/breadcrumbs
             *
             * @function Highcharts.Breadcrumbs#destroyListElements
             * @param {Highcharts.Breadcrumbs} this
             *        Breadcrumbs class.
             */
            Breadcrumbs.prototype.destroyListElements = function (force) {
                var elementList = this.elementList;
                objectEach(elementList, function (element, level) {
                    if (force ||
                        !elementList[level].updated) {
                        element = elementList[level];
                        element.button && element.button.destroy();
                        element.separator && element.separator.destroy();
                        delete element.button;
                        delete element.separator;
                        delete elementList[level];
                    }
                });
                if (force) {
                    this.elementList = {};
                }
            };
            /**
             * Destroy the single button if exists.
             *
             * @requires  modules/breadcrumbs
             *
             * @function Highcharts.Breadcrumbs#destroySingleButton
             * @param {Highcharts.Breadcrumbs} this
             *        Breadcrumbs class.
             */
            Breadcrumbs.prototype.destroySingleButton = function () {
                if (this.chart.drillUpButton) {
                    this.chart.drillUpButton.destroy();
                    this.chart.drillUpButton = void 0;
                }
            };
            /**
             * Reset state for all buttons in elementList.
             *
             * @requires  modules/breadcrumbs
             *
             * @function Highcharts.Breadcrumbs#resetElementListState
             * @param {Highcharts.Breadcrumbs} this
             *        Breadcrumbs class.
             */
            Breadcrumbs.prototype.resetElementListState = function () {
                objectEach(this.elementList, function (element) {
                    element.updated = false;
                });
            };
            /**
             * Update rendered elements inside the elementList.
             *
             * @requires  modules/breadcrumbs
             *
             * @function Highcharts.Breadcrumbs#updateListElements
             * @param {Highcharts.Breadcrumbs} this
             *        Breadcrumbs class.
             */
            Breadcrumbs.prototype.updateListElements = function () {
                var breadcrumbs = this,
                    elementList = breadcrumbs.elementList,
                    buttonSpacing = breadcrumbs.options.buttonSpacing,
                    list = breadcrumbs.list,
                    rtl = breadcrumbs.options.rtl,
                    rtlFactor = rtl ? -1 : 1,
                    updateXPosition = function (element,
                    spacing) {
                        return rtlFactor * element.getBBox().width +
                            rtlFactor * spacing;
                }, adjustToRTL = function (element, posX, posY) {
                    element.translate(posX - element.getBBox().width, posY);
                };
                // Inital position for calculating the breadcrumbs group.
                var posX = breadcrumbs.group ?
                        updateXPosition(breadcrumbs.group,
                    buttonSpacing) :
                        buttonSpacing,
                    posY = buttonSpacing,
                    currentBreadcrumb;
                list.forEach(function (breadcrumb, index) {
                    var isLast = index === list.length - 1;
                    var button,
                        separator;
                    if (elementList[breadcrumb.level]) {
                        currentBreadcrumb = elementList[breadcrumb.level];
                        button = currentBreadcrumb.button;
                        // Render a separator if it was not created before.
                        if (!currentBreadcrumb.separator &&
                            !isLast) {
                            // Add spacing for the next separator
                            posX += rtlFactor * buttonSpacing;
                            currentBreadcrumb.separator =
                                breadcrumbs.renderSeparator(posX, posY);
                            if (rtl) {
                                adjustToRTL(currentBreadcrumb.separator, posX, posY);
                            }
                            posX += updateXPosition(currentBreadcrumb.separator, buttonSpacing);
                        }
                        else if (currentBreadcrumb.separator &&
                            isLast) {
                            currentBreadcrumb.separator.destroy();
                            delete currentBreadcrumb.separator;
                        }
                        elementList[breadcrumb.level].updated = true;
                    }
                    else {
                        // Render a button.
                        button = breadcrumbs.renderButton(breadcrumb, posX, posY);
                        if (rtl) {
                            adjustToRTL(button, posX, posY);
                        }
                        posX += updateXPosition(button, buttonSpacing);
                        // Render a separator.
                        if (!isLast) {
                            separator = breadcrumbs.renderSeparator(posX, posY);
                            if (rtl) {
                                adjustToRTL(separator, posX, posY);
                            }
                            posX += updateXPosition(separator, buttonSpacing);
                        }
                        elementList[breadcrumb.level] = {
                            button: button,
                            separator: separator,
                            updated: true
                        };
                    }
                    if (button) {
                        button.setState(isLast ? 2 : 0);
                    }
                });
            };
            /**
             * Options for breadcrumbs. Breadcrumbs general options are defined in
             * `navigation.breadcrumbs`. Specific options for drilldown are set in
             * `drilldown.breadcrumbs` and for tree-like series traversing, in
             * `plotOptions[series].breadcrumbs`.
             *
             * @since 10.0.0
             * @product highcharts
             * @optionparent navigation.breadcrumbs
             */
            Breadcrumbs.defaultBreadcrumbsOptions = {
                /**
                 * A collection of attributes for the buttons. The object takes SVG
                 * attributes like `fill`, `stroke`, `stroke-width`, as well as `style`,
                 * a collection of CSS properties for the text.
                 *
                 * The object can also be extended with states, so you can set
                 * presentational options for `hover`, `select` or `disabled` button
                 * states.
                 *
                 * @sample {highcharts} highcharts/breadcrumbs/single-button
                 *         Themed, single button
                 *
                 * @type       {Highcharts.SVGAttributes}
                 * @since 10.0.0
                 * @product    highcharts
                 */
                buttonTheme: {
                    /** @ignore */
                    fill: 'none',
                    /** @ignore */
                    height: 18,
                    /** @ignore */
                    padding: 2,
                    /** @ignore */
                    'stroke-width': 0,
                    /** @ignore */
                    zIndex: 7,
                    /** @ignore */
                    states: {
                        select: {
                            fill: 'none'
                        }
                    },
                    style: {
                        color: "#335cad" /* Palette.highlightColor80 */
                    }
                },
                /**
                 * The default padding for each button and separator in each direction.
                 *
                 * @type      {number}
                 * @since 10.0.0
                 */
                buttonSpacing: 5,
                /**
                 * Fires when clicking on the breadcrumbs button. Two arguments are
                 * passed to the function. First breadcrumb button as an SVG element.
                 * Second is the breadcrumbs class, containing reference to the chart,
                 * series etc.
                 *
                 * ```js
                 * click: function(button, breadcrumbs) {
                 *   console.log(button);
                 * }
                 * ```
                 *
                 * Return false to stop default buttons click action.
                 *
                 * @type      {Highcharts.BreadcrumbsClickCallbackFunction}
                 * @since 10.0.0
                 * @apioption navigation.breadcrumbs.events.click
                 */
                /**
                 * When the breadcrumbs are floating, the plot area will not move to
                 * make space for it. By default, the chart will not make space for the
                 * buttons. This property won't work when positioned in the middle.
                 *
                 * @sample highcharts/breadcrumbs/single-button
                 *         Floating button
                 * @type      {boolean}
                 * @since 10.0.0
                 */
                floating: false,
                /**
                 * A format string for the breadcrumbs button. Variables are enclosed by
                 * curly brackets. Available values are passed in the declared point
                 * options.
                 *
                 * @type      {string|undefined}
                 * @since 10.0.0
                 * @default   undefined
                 * @sample {highcharts} highcharts/breadcrumbs/format Display custom
                 *          values in breadcrumb button.
                 */
                format: void 0,
                /**
                 * Callback function to format the breadcrumb text from scratch.
                 *
                 * @type      {Highcharts.BreadcrumbsFormatterCallbackFunction}
                 * @since 10.0.0
                 * @default   undefined
                 * @apioption navigation.breadcrumbs.formatter
                 */
                /**
                 * What box to align the button to. Can be either `plotBox` or
                 * `spacingBox`.
                 *
                 * @type       {Highcharts.ButtonRelativeToValue}
                 * @default    plotBox
                 * @since 10.0.0
                 * @product    highcharts highmaps
                 */
                relativeTo: 'plotBox',
                /**
                 * Whether to reverse the order of buttons. This is common in Arabic
                 * and Hebrew.
                 *
                 * @type       {boolean}
                 * @since 10.2.0
                 * @sample     {highcharts} highcharts/breadcrumbs/rtl
                 *             Breadcrumbs in RTL
                 */
                rtl: false,
                /**
                 * Positioning for the button row. The breadcrumbs buttons will be
                 * aligned properly for the default chart layout (title,  subtitle,
                 * legend, range selector) for the custom chart layout set the position
                 * properties.
                 * @type       {Highcharts.BreadcrumbsAlignOptions}
                 * @since 10.0.0
                 * @product    highcharts highmaps
                 * @sample     {highcharts} highcharts/breadcrumbs/single-button
                 *             Single, right aligned button
                 */
                position: {
                    /**
                     * Horizontal alignment of the breadcrumbs buttons.
                     *
                     * @type {Highcharts.AlignValue}
                     */
                    align: 'left',
                    /**
                     * Vertical alignment of the breadcrumbs buttons.
                     *
                     * @type {Highcharts.VerticalAlignValue}
                     */
                    verticalAlign: 'top',
                    /**
                     * The X offset of the breadcrumbs button group.
                     *
                     * @type {number}
                     */
                    x: 0,
                    /**
                     * The Y offset of the breadcrumbs button group. When `undefined`,
                     * and `floating` is `false`, the `y` position is adapted so that
                     * the breadcrumbs are rendered outside the target area.
                     *
                     * @type {number|undefined}
                     */
                    y: void 0
                },
                /**
                 * Options object for Breadcrumbs separator.
                 *
                 * @since 10.0.0
                 */
                separator: {
                    /**
                     * @type {string}
                     * @since 10.0.0
                     * @product highcharts
                     */
                    text: '/',
                    /**
                     * CSS styles for the breadcrumbs separator.
                     *
                     * In styled mode, the breadcrumbs separators are styled by the
                     * `.highcharts-separator` rule with its different states.
                     *  @type {Highcharts.CSSObject}
                     *  @since 10.0.0
                     */
                    style: {
                        color: "#666666" /* Palette.neutralColor60 */
                    }
                },
                /**
                 * Show full path or only a single button.
                 *
                 * @type      {boolean}
                 * @since 10.0.0
                 * @sample {highcharts} highcharts/breadcrumbs/single-button
                 *          Single, styled button
                 */
                showFullPath: true,
                /**
                 * CSS styles for all breadcrumbs.
                 *
                 * In styled mode, the breadcrumbs buttons are styled by the
                 * `.highcharts-breadcrumbs-buttons .highcharts-button` rule with its
                 * different states.
                 *  @type {Highcharts.SVGAttributes}
                 *  @since 10.0.0
                 */
                style: {},
                /**
                 * Whether to use HTML to render the breadcrumbs items texts.
                 *
                 * @type      {boolean}
                 * @since 10.0.0
                 */
                useHTML: false,
                /**
                 * The z index of the breadcrumbs group.
                 *
                 * @type      {number}
                 * @since 10.0.0
                 */
                zIndex: 7
            };
            return Breadcrumbs;
        }());
        /* eslint-disable no-invalid-this */
        if (!H.Breadcrumbs) {
            H.Breadcrumbs = Breadcrumbs;
            // Logic for making space for the buttons above the plot area
            addEvent(Chart, 'getMargins', function () {
                var breadcrumbs = this.breadcrumbs;
                if (breadcrumbs &&
                    !breadcrumbs.options.floating &&
                    breadcrumbs.level) {
                    var breadcrumbsOptions = breadcrumbs.options,
                        buttonTheme = breadcrumbsOptions.buttonTheme,
                        breadcrumbsHeight = ((buttonTheme.height || 0) +
                            2 * (buttonTheme.padding || 0) +
                            breadcrumbsOptions.buttonSpacing),
                        verticalAlign = breadcrumbsOptions.position.verticalAlign;
                    if (verticalAlign === 'bottom') {
                        this.marginBottom = (this.marginBottom || 0) + breadcrumbsHeight;
                        breadcrumbs.yOffset = breadcrumbsHeight;
                    }
                    else if (verticalAlign !== 'middle') {
                        this.plotTop += breadcrumbsHeight;
                        breadcrumbs.yOffset = -breadcrumbsHeight;
                    }
                    else {
                        breadcrumbs.yOffset = void 0;
                    }
                }
            });
            addEvent(Chart, 'redraw', function () {
                this.breadcrumbs && this.breadcrumbs.redraw();
            });
            // Remove resize/afterSetExtremes at chart destroy
            addEvent(Chart, 'destroy', function destroyEvents() {
                if (this.breadcrumbs) {
                    this.breadcrumbs.destroy();
                    this.breadcrumbs = void 0;
                }
            });
            // Shift the drillUpButton to make the space for resetZoomButton, #8095.
            addEvent(Chart, 'afterShowResetZoom', function () {
                var chart = this;
                if (chart.breadcrumbs) {
                    var bbox = chart.resetZoomButton &&
                            chart.resetZoomButton.getBBox(),
                        breadcrumbsOptions = chart.breadcrumbs.options;
                    if (bbox &&
                        breadcrumbsOptions.position.align === 'right' &&
                        breadcrumbsOptions.relativeTo === 'plotBox') {
                        chart.breadcrumbs.alignBreadcrumbsGroup(-bbox.width - breadcrumbsOptions.buttonSpacing);
                    }
                }
            });
            // After zooming out, shift the drillUpButton
            // to the previous position, #8095.
            addEvent(Chart, 'selection', function (event) {
                if (event.resetSelection === true &&
                    this.breadcrumbs) {
                    this.breadcrumbs.alignBreadcrumbsGroup();
                }
            });
        }
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
         * Callback function to react on button clicks.
         *
         * @callback Highcharts.BreadcrumbsClickCallbackFunction
         *
         * @param {Highcharts.Event} event
         * Event.
         *
         * @param {Highcharts.BreadcrumbOptions} options
         * Breadcrumb options.
         *
         * @param {global.Event} e
         * Event arguments.
         */
        /**
         * Callback function to format the breadcrumb text from scratch.
         *
         * @callback Highcharts.BreadcrumbsFormatterCallbackFunction
         *
         * @param {Highcharts.Event} event
         * Event.
         *
         * @param {Highcharts.BreadcrumbOptions} options
         * Breadcrumb options.
         *
         * @return {string}
         * Formatted text or false
         */
        /**
         * Options for the one breadcrumb.
         *
         * @interface Highcharts.BreadcrumbOptions
         */
        /**
         * Level connected to a specific breadcrumb.
         * @name Highcharts.BreadcrumbOptions#level
         * @type {number}
         */
        /**
         * Options for series or point connected to a specific breadcrumb.
         * @name Highcharts.BreadcrumbOptions#levelOptions
         * @type {SeriesOptions|PointOptionsObject}
         */
        /**
         * Options for aligning breadcrumbs group.
         *
         * @interface Highcharts.BreadcrumbsAlignOptions
         */
        /**
         * Align of a Breadcrumb group.
         * @default right
         * @name Highcharts.BreadcrumbsAlignOptions#align
         * @type {AlignValue}
         */
        /**
         * Vertical align of a Breadcrumb group.
         * @default top
         * @name Highcharts.BreadcrumbsAlignOptions#verticalAlign
         * @type {VerticalAlignValue}
         */
        /**
         * X offset of a Breadcrumbs group.
         * @name Highcharts.BreadcrumbsAlignOptions#x
         * @type {number}
         */
        /**
         * Y offset of a Breadcrumbs group.
         * @name Highcharts.BreadcrumbsAlignOptions#y
         * @type {number}
         */
        /**
         * Options for all breadcrumbs.
         *
         * @interface Highcharts.BreadcrumbsOptions
         */
        /**
         * Button theme.
         * @name Highcharts.BreadcrumbsOptions#buttonTheme
         * @type { SVGAttributes | undefined }
         */
        (''); // Keeps doclets above in JS file

        return Breadcrumbs;
    });
    _registerModule(_modules, 'Series/Treemap/TreemapComposition.js', [_modules['Core/Series/SeriesRegistry.js'], _modules['Series/Treemap/TreemapUtilities.js'], _modules['Core/Utilities.js']], function (SeriesRegistry, TreemapUtilities, U) {
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
        /* *
         *
         *  Imports
         *
         * */
        var Series = SeriesRegistry.series;
        var addEvent = U.addEvent,
            extend = U.extend;
        /* *
         *
         *  Composition
         *
         * */
        var treemapAxisDefaultValues = false;
        addEvent(Series, 'afterBindAxes', function () {
            // eslint-disable-next-line no-invalid-this
            var series = this,
                xAxis = series.xAxis,
                yAxis = series.yAxis,
                treeAxis;
            if (xAxis && yAxis) {
                if (series.is('treemap')) {
                    treeAxis = {
                        endOnTick: false,
                        gridLineWidth: 0,
                        lineWidth: 0,
                        min: 0,
                        // dataMin: 0,
                        minPadding: 0,
                        max: TreemapUtilities.AXIS_MAX,
                        // dataMax: TreemapUtilities.AXIS_MAX,
                        maxPadding: 0,
                        startOnTick: false,
                        title: void 0,
                        tickPositions: []
                    };
                    extend(yAxis.options, treeAxis);
                    extend(xAxis.options, treeAxis);
                    treemapAxisDefaultValues = true;
                }
                else if (treemapAxisDefaultValues) {
                    yAxis.setOptions(yAxis.userOptions);
                    xAxis.setOptions(xAxis.userOptions);
                    treemapAxisDefaultValues = false;
                }
            }
        });

    });
    _registerModule(_modules, 'Series/Treemap/TreemapNode.js', [], function () {
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
        *  Class
        *
        * */
        var TreemapNode = /** @class */ (function () {
                function TreemapNode() {
                    /* *
                    *
                    *  Properties
                    *
                    * */
                    this.childrenTotal = 0;
                this.visible = false;
            }
            /* *
            *
            *  Functions
            *
            * */
            TreemapNode.prototype.init = function (id, i, children, height, level, series, parent) {
                this.id = id;
                this.i = i;
                this.children = children;
                this.height = height;
                this.level = level;
                this.series = series;
                this.parent = parent;
                return this;
            };
            return TreemapNode;
        }());
        /* *
        *
        *  Default Export
        *
        * */

        return TreemapNode;
    });
    _registerModule(_modules, 'Series/Treemap/TreemapSeries.js', [_modules['Core/Color/Color.js'], _modules['Series/ColorMapComposition.js'], _modules['Core/Globals.js'], _modules['Core/Legend/LegendSymbol.js'], _modules['Core/Series/SeriesRegistry.js'], _modules['Series/Treemap/TreemapAlgorithmGroup.js'], _modules['Series/Treemap/TreemapPoint.js'], _modules['Series/Treemap/TreemapUtilities.js'], _modules['Series/TreeUtilities.js'], _modules['Extensions/Breadcrumbs.js'], _modules['Core/Utilities.js'], _modules['Series/Treemap/TreemapNode.js']], function (Color, ColorMapComposition, H, LegendSymbol, SeriesRegistry, TreemapAlgorithmGroup, TreemapPoint, TreemapUtilities, TU, Breadcrumbs, U, TreemapNode) {
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
        var Series = SeriesRegistry.series,
            _a = SeriesRegistry.seriesTypes,
            ColumnSeries = _a.column,
            HeatmapSeries = _a.heatmap,
            ScatterSeries = _a.scatter;
        var getColor = TU.getColor,
            getLevelOptions = TU.getLevelOptions,
            updateRootId = TU.updateRootId;
        var addEvent = U.addEvent,
            correctFloat = U.correctFloat,
            defined = U.defined,
            error = U.error,
            extend = U.extend,
            fireEvent = U.fireEvent,
            isArray = U.isArray,
            isNumber = U.isNumber,
            isObject = U.isObject,
            isString = U.isString,
            merge = U.merge,
            pick = U.pick,
            stableSort = U.stableSort;
        /* *
         *
         *  Class
         *
         * */
        /**
         * @private
         * @class
         * @name Highcharts.seriesTypes.treemap
         *
         * @augments Highcharts.Series
         */
        var TreemapSeries = /** @class */ (function (_super) {
                __extends(TreemapSeries, _super);
            function TreemapSeries() {
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
                _this.axisRatio = void 0;
                _this.data = void 0;
                _this.mapOptionsToLevel = void 0;
                _this.nodeMap = void 0;
                _this.nodeList = void 0;
                _this.options = void 0;
                _this.points = void 0;
                _this.rootNode = void 0;
                _this.tree = void 0;
                _this.level = void 0;
                return _this;
                /* eslint-enable valid-jsdoc */
            }
            /* *
             *
             *  Function
             *
             * */
            /* eslint-disable valid-jsdoc */
            TreemapSeries.prototype.algorithmCalcPoints = function (directionChange, last, group, childrenArea) {
                var pX,
                    pY,
                    pW,
                    pH,
                    gW = group.lW,
                    gH = group.lH,
                    plot = group.plot,
                    keep,
                    i = 0,
                    end = group.elArr.length - 1;
                if (last) {
                    gW = group.nW;
                    gH = group.nH;
                }
                else {
                    keep = group.elArr[group.elArr.length - 1];
                }
                group.elArr.forEach(function (p) {
                    if (last || (i < end)) {
                        if (group.direction === 0) {
                            pX = plot.x;
                            pY = plot.y;
                            pW = gW;
                            pH = p / pW;
                        }
                        else {
                            pX = plot.x;
                            pY = plot.y;
                            pH = gH;
                            pW = p / pH;
                        }
                        childrenArea.push({
                            x: pX,
                            y: pY,
                            width: pW,
                            height: correctFloat(pH)
                        });
                        if (group.direction === 0) {
                            plot.y = plot.y + pH;
                        }
                        else {
                            plot.x = plot.x + pW;
                        }
                    }
                    i = i + 1;
                });
                // Reset variables
                group.reset();
                if (group.direction === 0) {
                    group.width = group.width - gW;
                }
                else {
                    group.height = group.height - gH;
                }
                plot.y = plot.parent.y + (plot.parent.height - group.height);
                plot.x = plot.parent.x + (plot.parent.width - group.width);
                if (directionChange) {
                    group.direction = 1 - group.direction;
                }
                // If not last, then add uncalculated element
                if (!last) {
                    group.addElement(keep);
                }
            };
            TreemapSeries.prototype.algorithmFill = function (directionChange, parent, children) {
                var childrenArea = [],
                    pTot,
                    direction = parent.direction,
                    x = parent.x,
                    y = parent.y,
                    width = parent.width,
                    height = parent.height,
                    pX,
                    pY,
                    pW,
                    pH;
                children.forEach(function (child) {
                    pTot =
                        (parent.width * parent.height) * (child.val / parent.val);
                    pX = x;
                    pY = y;
                    if (direction === 0) {
                        pH = height;
                        pW = pTot / pH;
                        width = width - pW;
                        x = x + pW;
                    }
                    else {
                        pW = width;
                        pH = pTot / pW;
                        height = height - pH;
                        y = y + pH;
                    }
                    childrenArea.push({
                        x: pX,
                        y: pY,
                        width: pW,
                        height: pH
                    });
                    if (directionChange) {
                        direction = 1 - direction;
                    }
                });
                return childrenArea;
            };
            TreemapSeries.prototype.algorithmLowAspectRatio = function (directionChange, parent, children) {
                var childrenArea = [],
                    series = this,
                    pTot,
                    plot = {
                        x: parent.x,
                        y: parent.y,
                        parent: parent
                    },
                    direction = parent.direction,
                    i = 0,
                    end = children.length - 1,
                    group = new TreemapAlgorithmGroup(parent.height,
                    parent.width,
                    direction,
                    plot);
                // Loop through and calculate all areas
                children.forEach(function (child) {
                    pTot =
                        (parent.width * parent.height) * (child.val / parent.val);
                    group.addElement(pTot);
                    if (group.lP.nR > group.lP.lR) {
                        series.algorithmCalcPoints(directionChange, false, group, childrenArea, plot // @todo no supported
                        );
                    }
                    // If last child, then calculate all remaining areas
                    if (i === end) {
                        series.algorithmCalcPoints(directionChange, true, group, childrenArea, plot // @todo not supported
                        );
                    }
                    i = i + 1;
                });
                return childrenArea;
            };
            /**
             * Over the alignment method by setting z index.
             * @private
             */
            TreemapSeries.prototype.alignDataLabel = function (point, dataLabel, labelOptions) {
                var style = labelOptions.style;
                // #8160: Prevent the label from exceeding the point's
                // boundaries in treemaps by applying ellipsis overflow.
                // The issue was happening when datalabel's text contained a
                // long sequence of characters without a whitespace.
                if (style &&
                    !defined(style.textOverflow) &&
                    dataLabel.text &&
                    dataLabel.getBBox().width > dataLabel.text.textWidth) {
                    dataLabel.css({
                        textOverflow: 'ellipsis',
                        // unit (px) is required when useHTML is true
                        width: style.width += 'px'
                    });
                }
                ColumnSeries.prototype.alignDataLabel.apply(this, arguments);
                if (point.dataLabel) {
                    // point.node.zIndex could be undefined (#6956)
                    point.dataLabel.attr({ zIndex: (point.node.zIndex || 0) + 1 });
                }
            };
            /**
             * Recursive function which calculates the area for all children of a
             * node.
             *
             * @private
             * @function Highcharts.Series#calculateChildrenAreas
             *
             * @param {Object} node
             * The node which is parent to the children.
             *
             * @param {Object} area
             * The rectangular area of the parent.
             */
            TreemapSeries.prototype.calculateChildrenAreas = function (parent, area) {
                var series = this,
                    options = series.options,
                    mapOptionsToLevel = series.mapOptionsToLevel,
                    level = mapOptionsToLevel[parent.level + 1],
                    algorithm = pick((series[(level && level.layoutAlgorithm)] &&
                        level.layoutAlgorithm),
                    options.layoutAlgorithm),
                    alternate = options.alternateStartingDirection,
                    childrenValues = [],
                    children;
                // Collect all children which should be included
                children = parent.children.filter(function (n) {
                    return !n.ignore;
                });
                if (level && level.layoutStartingDirection) {
                    area.direction = level.layoutStartingDirection === 'vertical' ?
                        0 :
                        1;
                }
                childrenValues = series[algorithm](area, children);
                children.forEach(function (child, index) {
                    var values = childrenValues[index];
                    child.values = merge(values, {
                        val: child.childrenTotal,
                        direction: (alternate ? 1 - area.direction : area.direction)
                    });
                    child.pointValues = merge(values, {
                        x: (values.x / series.axisRatio),
                        // Flip y-values to avoid visual regression with csvCoord in
                        // Axis.translate at setPointValues. #12488
                        y: TreemapUtilities.AXIS_MAX - values.y - values.height,
                        width: (values.width / series.axisRatio)
                    });
                    // If node has children, then call method recursively
                    if (child.children.length) {
                        series.calculateChildrenAreas(child, child.values);
                    }
                });
            };
            /**
            * Create level list.
            *
            * @requires  modules/breadcrumbs
            *
            * @function TreemapSeries#createList
            * @param {TreemapSeries} this
            *        Treemap Series class.
            */
            TreemapSeries.prototype.createList = function (e) {
                var chart = this.chart,
                    breadcrumbs = chart.breadcrumbs,
                    list = [];
                if (breadcrumbs) {
                    var currentLevelNumber_1 = 0;
                    list.push({
                        level: currentLevelNumber_1,
                        levelOptions: chart.series[0]
                    });
                    var node = e.target.nodeMap[e.newRootId];
                    var extraNodes = [];
                    // When the root node is set and has parent,
                    // recreate the path from the node tree.
                    while (node.parent || node.parent === '') {
                        extraNodes.push(node);
                        node = e.target.nodeMap[node.parent];
                    }
                    extraNodes.reverse().forEach(function (node) {
                        list.push({
                            level: ++currentLevelNumber_1,
                            levelOptions: node
                        });
                    });
                    // If the list has only first element, we should clear it
                    if (list.length <= 1) {
                        list.length = 0;
                    }
                }
                return list;
            };
            /**
             * Extend drawDataLabels with logic to handle custom options related to
             * the treemap series:
             *
             * - Points which is not a leaf node, has dataLabels disabled by
             *   default.
             *
             * - Options set on series.levels is merged in.
             *
             * - Width of the dataLabel is set to match the width of the point
             *   shape.
             *
             * @private
             */
            TreemapSeries.prototype.drawDataLabels = function () {
                var series = this,
                    mapOptionsToLevel = series.mapOptionsToLevel,
                    points = series.points.filter(function (n) {
                        return n.node.visible;
                }), options, level;
                points.forEach(function (point) {
                    level = mapOptionsToLevel[point.node.level];
                    // Set options to new object to avoid problems with scope
                    options = { style: {} };
                    // If not a leaf, then label should be disabled as default
                    if (!point.node.isLeaf) {
                        options.enabled = false;
                    }
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
                });
                Series.prototype.drawDataLabels.call(this);
            };
            /**
             * Override drawPoints
             * @private
             */
            TreemapSeries.prototype.drawPoints = function (points) {
                if (points === void 0) { points = this.points; }
                var series = this,
                    chart = series.chart,
                    renderer = chart.renderer,
                    styledMode = chart.styledMode,
                    options = series.options,
                    shadow = styledMode ? {} : options.shadow,
                    borderRadius = options.borderRadius,
                    withinAnimationLimit = chart.pointCount < options.animationLimit,
                    allowTraversingTree = options.allowTraversingTree;
                points.forEach(function (point) {
                    var levelDynamic = point.node.levelDynamic,
                        animatableAttribs = {},
                        attribs = {},
                        css = {},
                        groupKey = 'level-group-' + point.node.level,
                        hasGraphic = !!point.graphic,
                        shouldAnimate = withinAnimationLimit && hasGraphic,
                        shapeArgs = point.shapeArgs;
                    // Don't bother with calculate styling if the point is not drawn
                    if (point.shouldDraw()) {
                        point.isInside = true;
                        if (borderRadius) {
                            attribs.r = borderRadius;
                        }
                        merge(true, // Extend object
                        // Which object to extend
                        shouldAnimate ? animatableAttribs : attribs, 
                        // Add shapeArgs to animate/attr if graphic exists
                        hasGraphic ? shapeArgs : {}, 
                        // Add style attribs if !styleMode
                        styledMode ?
                            {} :
                            series.pointAttribs(point, point.selected ? 'select' : void 0));
                        // In styled mode apply point.color. Use CSS, otherwise the
                        // fill used in the style sheet will take precedence over
                        // the fill attribute.
                        if (series.colorAttribs && styledMode) {
                            // Heatmap is loaded
                            extend(css, series.colorAttribs(point));
                        }
                        if (!series[groupKey]) {
                            series[groupKey] = renderer.g(groupKey)
                                .attr({
                                // @todo Set the zIndex based upon the number of
                                // levels, instead of using 1000
                                zIndex: 1000 - (levelDynamic || 0)
                            })
                                .add(series.group);
                            series[groupKey].survive = true;
                        }
                    }
                    // Draw the point
                    point.draw({
                        animatableAttribs: animatableAttribs,
                        attribs: attribs,
                        css: css,
                        group: series[groupKey],
                        renderer: renderer,
                        shadow: shadow,
                        shapeArgs: shapeArgs,
                        shapeType: point.shapeType
                    });
                    // If setRootNode is allowed, set a point cursor on clickables &
                    // add drillId to point
                    if (allowTraversingTree && point.graphic) {
                        point.drillId = options.interactByLeaf ?
                            series.drillToByLeaf(point) :
                            series.drillToByGroup(point);
                    }
                });
            };
            /**
             * Finds the drill id for a parent node. Returns false if point should
             * not have a click event.
             * @private
             */
            TreemapSeries.prototype.drillToByGroup = function (point) {
                var series = this,
                    drillId = false;
                if ((point.node.level - series.nodeMap[series.rootNode].level) ===
                    1 &&
                    !point.node.isLeaf) {
                    drillId = point.id;
                }
                return drillId;
            };
            /**
             * Finds the drill id for a leaf node. Returns false if point should not
             * have a click event
             * @private
             */
            TreemapSeries.prototype.drillToByLeaf = function (point) {
                var series = this,
                    drillId = false,
                    nodeParent;
                if ((point.node.parent !== series.rootNode) &&
                    point.node.isLeaf) {
                    nodeParent = point.node;
                    while (!drillId) {
                        nodeParent = series.nodeMap[nodeParent.parent];
                        if (nodeParent.parent === series.rootNode) {
                            drillId = nodeParent.id;
                        }
                    }
                }
                return drillId;
            };
            /**
             * @todo remove this function at a suitable version.
             * @private
             */
            TreemapSeries.prototype.drillToNode = function (id, redraw) {
                error(32, false, void 0, { 'treemap.drillToNode': 'use treemap.setRootNode' });
                this.setRootNode(id, redraw);
            };
            TreemapSeries.prototype.drillUp = function () {
                var series = this,
                    node = series.nodeMap[series.rootNode];
                if (node && isString(node.parent)) {
                    series.setRootNode(node.parent, true, { trigger: 'traverseUpButton' });
                }
            };
            TreemapSeries.prototype.getExtremes = function () {
                // Get the extremes from the value data
                var _a = Series.prototype.getExtremes
                        .call(this,
                    this.colorValueData),
                    dataMin = _a.dataMin,
                    dataMax = _a.dataMax;
                this.valueMin = dataMin;
                this.valueMax = dataMax;
                // Get the extremes from the y data
                return Series.prototype.getExtremes.call(this);
            };
            /**
             * Creates an object map from parent id to childrens index.
             *
             * @private
             * @function Highcharts.Series#getListOfParents
             *
             * @param {Highcharts.SeriesTreemapDataOptions} [data]
             *        List of points set in options.
             *
             * @param {Array<string>} [existingIds]
             *        List of all point ids.
             *
             * @return {Object}
             *         Map from parent id to children index in data.
             */
            TreemapSeries.prototype.getListOfParents = function (data, existingIds) {
                var arr = isArray(data) ? data : [],
                    ids = isArray(existingIds) ? existingIds : [],
                    listOfParents = arr.reduce(function (prev,
                    curr,
                    i) {
                        var parent = pick(curr.parent, '');
                    if (typeof prev[parent] === 'undefined') {
                        prev[parent] = [];
                    }
                    prev[parent].push(i);
                    return prev;
                }, {
                    '': [] // Root of tree
                });
                // If parent does not exist, hoist parent to root of tree.
                TreemapUtilities.eachObject(listOfParents, function (children, parent, list) {
                    if ((parent !== '') && (ids.indexOf(parent) === -1)) {
                        children.forEach(function (child) {
                            list[''].push(child);
                        });
                        delete list[parent];
                    }
                });
                return listOfParents;
            };
            /**
             * Creates a tree structured object from the series points.
             * @private
             */
            TreemapSeries.prototype.getTree = function () {
                var series = this,
                    allIds = this.data.map(function (d) {
                        return d.id;
                }), parentList = series.getListOfParents(this.data, allIds);
                series.nodeMap = {};
                series.nodeList = [];
                return series.buildTree('', -1, 0, parentList);
            };
            TreemapSeries.prototype.buildTree = function (id, index, level, list, parent) {
                var series = this,
                    children = [],
                    point = series.points[index],
                    height = 0,
                    node,
                    child;
                // Actions
                (list[id] || []).forEach(function (i) {
                    child = series.buildTree(series.points[i].id, i, level + 1, list, id);
                    height = Math.max(child.height + 1, height);
                    children.push(child);
                });
                node = new series.NodeClass().init(id, index, children, height, level, series, parent);
                children.forEach(function (child) {
                    child.parentNode = node;
                });
                series.nodeMap[node.id] = node;
                series.nodeList.push(node);
                if (point) {
                    point.node = node;
                    node.point = point;
                }
                return node;
            };
            /**
             * Define hasData function for non-cartesian series. Returns true if the
             * series has points at all.
             * @private
             */
            TreemapSeries.prototype.hasData = function () {
                return !!this.processedXData.length; // != 0
            };
            TreemapSeries.prototype.init = function (chart, options) {
                var series = this,
                    breadcrumbsOptions = merge(options.drillUpButton,
                    options.breadcrumbs);
                var setOptionsEvent;
                setOptionsEvent = addEvent(series, 'setOptions', function (event) {
                    var options = event.userOptions;
                    if (defined(options.allowDrillToNode) &&
                        !defined(options.allowTraversingTree)) {
                        options.allowTraversingTree = options.allowDrillToNode;
                        delete options.allowDrillToNode;
                    }
                    if (defined(options.drillUpButton) &&
                        !defined(options.traverseUpButton)) {
                        options.traverseUpButton = options.drillUpButton;
                        delete options.drillUpButton;
                    }
                });
                Series.prototype.init.call(series, chart, options);
                // Treemap's opacity is a different option from other series
                delete series.opacity;
                // Handle deprecated options.
                series.eventsToUnbind.push(setOptionsEvent);
                if (series.options.allowTraversingTree) {
                    series.eventsToUnbind.push(addEvent(series, 'click', series.onClickDrillToNode));
                    series.eventsToUnbind.push(addEvent(series, 'setRootNode', function (e) {
                        var chart = series.chart;
                        if (chart.breadcrumbs) {
                            // Create a list using the event after drilldown.
                            chart.breadcrumbs.updateProperties(series.createList(e));
                        }
                    }));
                    series.eventsToUnbind.push(addEvent(series, 'update', function (e, redraw) {
                        var breadcrumbs = this.chart.breadcrumbs;
                        if (breadcrumbs && e.options.breadcrumbs) {
                            breadcrumbs.update(e.options.breadcrumbs);
                        }
                    }));
                    series.eventsToUnbind.push(addEvent(series, 'destroy', function destroyEvents(e) {
                        var chart = this.chart;
                        if (chart.breadcrumbs) {
                            chart.breadcrumbs.destroy();
                            if (!e.keepEventsForUpdate) {
                                chart.breadcrumbs = void 0;
                            }
                        }
                    }));
                }
                if (!chart.breadcrumbs) {
                    chart.breadcrumbs = new Breadcrumbs(chart, breadcrumbsOptions);
                }
                series.eventsToUnbind.push(addEvent(chart.breadcrumbs, 'up', function (e) {
                    var drillUpsNumber = this.level - e.newLevel;
                    for (var i = 0; i < drillUpsNumber; i++) {
                        series.drillUp();
                    }
                }));
            };
            /**
             * Add drilling on the suitable points.
             * @private
             */
            TreemapSeries.prototype.onClickDrillToNode = function (event) {
                var series = this,
                    point = event.point,
                    drillId = point && point.drillId;
                // If a drill id is returned, add click event and cursor.
                if (isString(drillId)) {
                    point.setState(''); // Remove hover
                    series.setRootNode(drillId, true, { trigger: 'click' });
                }
            };
            /**
             * Get presentational attributes
             * @private
             */
            TreemapSeries.prototype.pointAttribs = function (point, state) {
                var series = this,
                    mapOptionsToLevel = (isObject(series.mapOptionsToLevel) ?
                        series.mapOptionsToLevel :
                        {}),
                    level = point && mapOptionsToLevel[point.node.level] || {},
                    options = this.options,
                    attr,
                    stateOptions = state && options.states && options.states[state] || {},
                    className = (point && point.getClassName()) || '',
                    opacity;
                // Set attributes by precedence. Point trumps level trumps series.
                // Stroke width uses pick because it can be 0.
                attr = {
                    'stroke': (point && point.borderColor) ||
                        level.borderColor ||
                        stateOptions.borderColor ||
                        options.borderColor,
                    'stroke-width': pick(point && point.borderWidth, level.borderWidth, stateOptions.borderWidth, options.borderWidth),
                    'dashstyle': (point && point.borderDashStyle) ||
                        level.borderDashStyle ||
                        stateOptions.borderDashStyle ||
                        options.borderDashStyle,
                    'fill': (point && point.color) || this.color
                };
                // Hide levels above the current view
                if (className.indexOf('highcharts-above-level') !== -1) {
                    attr.fill = 'none';
                    attr['stroke-width'] = 0;
                    // Nodes with children that accept interaction
                }
                else if (className.indexOf('highcharts-internal-node-interactive') !== -1) {
                    opacity = pick(stateOptions.opacity, options.opacity);
                    attr.fill = color(attr.fill).setOpacity(opacity).get();
                    attr.cursor = 'pointer';
                    // Hide nodes that have children
                }
                else if (className.indexOf('highcharts-internal-node') !== -1) {
                    attr.fill = 'none';
                }
                else if (state) {
                    // Brighten and hoist the hover nodes
                    attr.fill = color(attr.fill)
                        .brighten(stateOptions.brightness)
                        .get();
                }
                return attr;
            };
            /**
             * Set the node's color recursively, from the parent down.
             * @private
             */
            TreemapSeries.prototype.setColorRecursive = function (node, parentColor, colorIndex, index, siblings) {
                var series = this,
                    chart = series && series.chart,
                    colors = chart && chart.options && chart.options.colors,
                    colorInfo,
                    point;
                if (node) {
                    colorInfo = getColor(node, {
                        colors: colors,
                        index: index,
                        mapOptionsToLevel: series.mapOptionsToLevel,
                        parentColor: parentColor,
                        parentColorIndex: colorIndex,
                        series: series,
                        siblings: siblings
                    });
                    point = series.points[node.i];
                    if (point) {
                        point.color = colorInfo.color;
                        point.colorIndex = colorInfo.colorIndex;
                    }
                    // Do it all again with the children
                    (node.children || []).forEach(function (child, i) {
                        series.setColorRecursive(child, colorInfo.color, colorInfo.colorIndex, i, node.children.length);
                    });
                }
            };
            TreemapSeries.prototype.setPointValues = function () {
                var series = this;
                var points = series.points,
                    xAxis = series.xAxis,
                    yAxis = series.yAxis;
                var styledMode = series.chart.styledMode;
                // Get the crisp correction in classic mode. For this to work in
                // styled mode, we would need to first add the shape (without x,
                // y, width and height), then read the rendered stroke width
                // using point.graphic.strokeWidth(), then modify and apply the
                // shapeArgs. This applies also to column series, but the
                // downside is performance and code complexity.
                var getCrispCorrection = function (point) { return (styledMode ?
                        0 :
                        ((series.pointAttribs(point)['stroke-width'] || 0) % 2) / 2); };
                points.forEach(function (point) {
                    var _a = point.node,
                        values = _a.pointValues,
                        visible = _a.visible;
                    // Points which is ignored, have no values.
                    if (values && visible) {
                        var height = values.height,
                            width = values.width,
                            x = values.x,
                            y = values.y;
                        var crispCorr = getCrispCorrection(point);
                        var x1 = Math.round(xAxis.toPixels(x,
                            true)) - crispCorr;
                        var x2 = Math.round(xAxis.toPixels(x + width,
                            true)) - crispCorr;
                        var y1 = Math.round(yAxis.toPixels(y,
                            true)) - crispCorr;
                        var y2 = Math.round(yAxis.toPixels(y + height,
                            true)) - crispCorr;
                        // Set point values
                        var shapeArgs = {
                                x: Math.min(x1,
                            x2),
                                y: Math.min(y1,
                            y2),
                                width: Math.abs(x2 - x1),
                                height: Math.abs(y2 - y1)
                            };
                        point.plotX = shapeArgs.x + (shapeArgs.width / 2);
                        point.plotY = shapeArgs.y + (shapeArgs.height / 2);
                        point.shapeArgs = shapeArgs;
                    }
                    else {
                        // Reset visibility
                        delete point.plotX;
                        delete point.plotY;
                    }
                });
            };
            /**
             * Sets a new root node for the series.
             *
             * @private
             * @function Highcharts.Series#setRootNode
             *
             * @param {string} id
             * The id of the new root node.
             *
             * @param {boolean} [redraw=true]
             * Whether to redraw the chart or not.
             *
             * @param {Object} [eventArguments]
             * Arguments to be accessed in event handler.
             *
             * @param {string} [eventArguments.newRootId]
             * Id of the new root.
             *
             * @param {string} [eventArguments.previousRootId]
             * Id of the previous root.
             *
             * @param {boolean} [eventArguments.redraw]
             * Whether to redraw the chart after.
             *
             * @param {Object} [eventArguments.series]
             * The series to update the root of.
             *
             * @param {string} [eventArguments.trigger]
             * The action which triggered the event. Undefined if the setRootNode is
             * called directly.
             *
             * @emits Highcharts.Series#event:setRootNode
             */
            TreemapSeries.prototype.setRootNode = function (id, redraw, eventArguments) {
                var series = this,
                    eventArgs = extend({
                        newRootId: id,
                        previousRootId: series.rootNode,
                        redraw: pick(redraw,
                    true),
                        series: series
                    },
                    eventArguments);
                /**
                 * The default functionality of the setRootNode event.
                 *
                 * @private
                 * @param {Object} args The event arguments.
                 * @param {string} args.newRootId Id of the new root.
                 * @param {string} args.previousRootId Id of the previous root.
                 * @param {boolean} args.redraw Whether to redraw the chart after.
                 * @param {Object} args.series The series to update the root of.
                 * @param {string} [args.trigger=undefined] The action which
                 * triggered the event. Undefined if the setRootNode is called
                 * directly.
                     */
                var defaultFn = function (args) {
                        var series = args.series;
                    // Store previous and new root ids on the series.
                    series.idPreviousRoot = args.previousRootId;
                    series.rootNode = args.newRootId;
                    // Redraw the chart
                    series.isDirty = true; // Force redraw
                    if (args.redraw) {
                        series.chart.redraw();
                    }
                };
                // Fire setRootNode event.
                fireEvent(series, 'setRootNode', eventArgs, defaultFn);
            };
            /**
             * Workaround for `inactive` state. Since `series.opacity` option is
             * already reserved, don't use that state at all by disabling
             * `inactiveOtherPoints` and not inheriting states by points.
             * @private
             */
            TreemapSeries.prototype.setState = function (state) {
                this.options.inactiveOtherPoints = true;
                Series.prototype.setState.call(this, state, false);
                this.options.inactiveOtherPoints = false;
            };
            TreemapSeries.prototype.setTreeValues = function (tree) {
                var series = this,
                    options = series.options,
                    idRoot = series.rootNode,
                    mapIdToNode = series.nodeMap,
                    nodeRoot = mapIdToNode[idRoot],
                    levelIsConstant = (TreemapUtilities.isBoolean(options.levelIsConstant) ?
                        options.levelIsConstant :
                        true),
                    childrenTotal = 0,
                    children = [],
                    val,
                    point = series.points[tree.i];
                // First give the children some values
                tree.children.forEach(function (child) {
                    child = series.setTreeValues(child);
                    children.push(child);
                    if (!child.ignore) {
                        childrenTotal += child.val;
                    }
                });
                // Sort the children
                stableSort(children, function (a, b) {
                    return (a.sortIndex || 0) - (b.sortIndex || 0);
                });
                // Set the values
                val = pick(point && point.options.value, childrenTotal);
                if (point) {
                    point.value = val;
                }
                extend(tree, {
                    children: children,
                    childrenTotal: childrenTotal,
                    // Ignore this node if point is not visible
                    ignore: !(pick(point && point.visible, true) && (val > 0)),
                    isLeaf: tree.visible && !childrenTotal,
                    levelDynamic: (tree.level - (levelIsConstant ? 0 : nodeRoot.level)),
                    name: pick(point && point.name, ''),
                    sortIndex: pick(point && point.sortIndex, -val),
                    val: val
                });
                return tree;
            };
            TreemapSeries.prototype.sliceAndDice = function (parent, children) {
                return this.algorithmFill(true, parent, children);
            };
            TreemapSeries.prototype.squarified = function (parent, children) {
                return this.algorithmLowAspectRatio(true, parent, children);
            };
            TreemapSeries.prototype.strip = function (parent, children) {
                return this.algorithmLowAspectRatio(false, parent, children);
            };
            TreemapSeries.prototype.stripes = function (parent, children) {
                return this.algorithmFill(false, parent, children);
            };
            TreemapSeries.prototype.translate = function () {
                var series = this,
                    options = series.options, 
                    // NOTE: updateRootId modifies series.
                    rootId = updateRootId(series),
                    rootNode,
                    pointValues,
                    seriesArea,
                    tree,
                    val;
                // Call prototype function
                Series.prototype.translate.call(series);
                // @todo Only if series.isDirtyData is true
                tree = series.tree = series.getTree();
                rootNode = series.nodeMap[rootId];
                if (rootId !== '' &&
                    (!rootNode || !rootNode.children.length)) {
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
                // Parents of the root node is by default visible
                TreemapUtilities.recursive(series.nodeMap[series.rootNode], function (node) {
                    var next = false,
                        p = node.parent;
                    node.visible = true;
                    if (p || p === '') {
                        next = series.nodeMap[p];
                    }
                    return next;
                });
                // Children of the root node is by default visible
                TreemapUtilities.recursive(series.nodeMap[series.rootNode].children, function (children) {
                    var next = false;
                    children.forEach(function (child) {
                        child.visible = true;
                        if (child.children.length) {
                            next = (next || []).concat(child.children);
                        }
                    });
                    return next;
                });
                series.setTreeValues(tree);
                // Calculate plotting values.
                series.axisRatio = (series.xAxis.len / series.yAxis.len);
                series.nodeMap[''].pointValues = pointValues = {
                    x: 0,
                    y: 0,
                    width: TreemapUtilities.AXIS_MAX,
                    height: TreemapUtilities.AXIS_MAX
                };
                series.nodeMap[''].values = seriesArea = merge(pointValues, {
                    width: (pointValues.width * series.axisRatio),
                    direction: (options.layoutStartingDirection === 'vertical' ? 0 : 1),
                    val: tree.val
                });
                series.calculateChildrenAreas(tree, seriesArea);
                // Logic for point colors
                if (!series.colorAxis &&
                    !options.colorByPoint) {
                    series.setColorRecursive(series.tree);
                }
                // Update axis extremes according to the root node.
                if (options.allowTraversingTree) {
                    val = rootNode.pointValues;
                    series.xAxis.setExtremes(val.x, val.x + val.width, false);
                    series.yAxis.setExtremes(val.y, val.y + val.height, false);
                    series.xAxis.setScale();
                    series.yAxis.setScale();
                }
                // Assign values to points.
                series.setPointValues();
            };
            /**
             * A treemap displays hierarchical data using nested rectangles. The data
             * can be laid out in varying ways depending on options.
             *
             * @sample highcharts/demo/treemap-large-dataset/
             *         Treemap
             *
             * @extends      plotOptions.scatter
             * @excluding    cluster, connectEnds, connectNulls, dataSorting, dragDrop, jitter, marker
             * @product      highcharts
             * @requires     modules/treemap
             * @optionparent plotOptions.treemap
             */
            TreemapSeries.defaultOptions = merge(ScatterSeries.defaultOptions, {
                /**
                 * When enabled the user can click on a point which is a parent and
                 * zoom in on its children. Deprecated and replaced by
                 * [allowTraversingTree](#plotOptions.treemap.allowTraversingTree).
                 *
                 * @sample {highcharts} highcharts/plotoptions/treemap-allowdrilltonode/
                 *         Enabled
                 *
                 * @deprecated
                 * @type      {boolean}
                 * @default   false
                 * @since     4.1.0
                 * @product   highcharts
                 * @apioption plotOptions.treemap.allowDrillToNode
                 */
                /**
                 * When enabled the user can click on a point which is a parent and
                 * zoom in on its children.
                 *
                 * @sample {highcharts} highcharts/plotoptions/treemap-allowtraversingtree/
                 *         Enabled
                 *
                 * @since     7.0.3
                 * @product   highcharts
                 */
                allowTraversingTree: false,
                animationLimit: 250,
                /**
                 * The border radius for each treemap item.
                 */
                borderRadius: 0,
                /**
                 * Options for the breadcrumbs, the navigation at the top leading the
                 * way up through the traversed levels.
                 *
                 *
                 * @since 10.0.0
                 * @product   highcharts
                 * @extends   navigation.breadcrumbs
                 * @optionparent plotOptions.treemap.breadcrumbs
                 */
                /**
                 * When the series contains less points than the crop threshold, all
                 * points are drawn, event if the points fall outside the visible plot
                 * area at the current zoom. The advantage of drawing all points
                 * (including markers and columns), is that animation is performed on
                 * updates. On the other hand, when the series contains more points than
                 * the crop threshold, the series data is cropped to only contain points
                 * that fall within the plot area. The advantage of cropping away
                 * invisible points is to increase performance on large series.
                 *
                 * @type      {number}
                 * @default   300
                 * @since     4.1.0
                 * @product   highcharts
                 * @apioption plotOptions.treemap.cropThreshold
                 */
                /**
                 * Fires on a request for change of root node for the tree, before the
                 * update is made. An event object is passed to the function, containing
                 * additional properties `newRootId`, `previousRootId`, `redraw` and
                 * `trigger`.
                 *
                 * @sample {highcharts} highcharts/plotoptions/treemap-events-setrootnode/
                 *         Alert update information on setRootNode event.
                 *
                 * @type {Function}
                 * @default undefined
                 * @since 7.0.3
                 * @product highcharts
                 * @apioption plotOptions.treemap.events.setRootNode
                 */
                /**
                 * This option decides if the user can interact with the parent nodes
                 * or just the leaf nodes. When this option is undefined, it will be
                 * true by default. However when allowTraversingTree is true, then it
                 * will be false by default.
                 *
                 * @sample {highcharts} highcharts/plotoptions/treemap-interactbyleaf-false/
                 *         False
                 * @sample {highcharts} highcharts/plotoptions/treemap-interactbyleaf-true-and-allowtraversingtree/
                 *         InteractByLeaf and allowTraversingTree is true
                 *
                 * @type      {boolean}
                 * @since     4.1.2
                 * @product   highcharts
                 * @apioption plotOptions.treemap.interactByLeaf
                 */
                /**
                 * The sort index of the point inside the treemap level.
                 *
                 * @sample {highcharts} highcharts/plotoptions/treemap-sortindex/
                 *         Sort by years
                 *
                 * @type      {number}
                 * @since     4.1.10
                 * @product   highcharts
                 * @apioption plotOptions.treemap.sortIndex
                 */
                /**
                 * A series specific or series type specific color set to apply instead
                 * of the global [colors](#colors) when
                 * [colorByPoint](#plotOptions.treemap.colorByPoint) is true.
                 *
                 * @type      {Array<Highcharts.ColorString|Highcharts.GradientColorObject|Highcharts.PatternObject>}
                 * @since     3.0
                 * @product   highcharts
                 * @apioption plotOptions.treemap.colors
                 */
                /**
                 * Whether to display this series type or specific series item in the
                 * legend.
                 */
                showInLegend: false,
                /**
                 * @ignore-option
                 */
                marker: void 0,
                /**
                 * When using automatic point colors pulled from the `options.colors`
                 * collection, this option determines whether the chart should receive
                 * one color per series or one color per point.
                 *
                 * @see [series colors](#plotOptions.treemap.colors)
                 *
                 * @since     2.0
                 * @product   highcharts
                 * @apioption plotOptions.treemap.colorByPoint
                 */
                colorByPoint: false,
                /**
                 * @since 4.1.0
                 */
                dataLabels: {
                    defer: false,
                    enabled: true,
                    formatter: function () {
                        var point = this && this.point ?
                                this.point :
                                {},
                            name = isString(point.name) ? point.name : '';
                        return name;
                    },
                    inside: true,
                    verticalAlign: 'middle'
                },
                tooltip: {
                    headerFormat: '',
                    pointFormat: '<b>{point.name}</b>: {point.value}<br/>'
                },
                /**
                 * Whether to ignore hidden points when the layout algorithm runs.
                 * If `false`, hidden points will leave open spaces.
                 *
                 * @since 5.0.8
                 */
                ignoreHiddenPoint: true,
                /**
                 * This option decides which algorithm is used for setting position
                 * and dimensions of the points.
                 *
                 * @see [How to write your own algorithm](https://www.highcharts.com/docs/chart-and-series-types/treemap)
                 *
                 * @sample {highcharts} highcharts/plotoptions/treemap-layoutalgorithm-sliceanddice/
                 *         SliceAndDice by default
                 * @sample {highcharts} highcharts/plotoptions/treemap-layoutalgorithm-stripes/
                 *         Stripes
                 * @sample {highcharts} highcharts/plotoptions/treemap-layoutalgorithm-squarified/
                 *         Squarified
                 * @sample {highcharts} highcharts/plotoptions/treemap-layoutalgorithm-strip/
                 *         Strip
                 *
                 * @since      4.1.0
                 * @validvalue ["sliceAndDice", "stripes", "squarified", "strip"]
                 */
                layoutAlgorithm: 'sliceAndDice',
                /**
                 * Defines which direction the layout algorithm will start drawing.
                 *
                 * @since       4.1.0
                 * @validvalue ["vertical", "horizontal"]
                 */
                layoutStartingDirection: 'vertical',
                /**
                 * Enabling this option will make the treemap alternate the drawing
                 * direction between vertical and horizontal. The next levels starting
                 * direction will always be the opposite of the previous.
                 *
                 * @sample {highcharts} highcharts/plotoptions/treemap-alternatestartingdirection-true/
                 *         Enabled
                 *
                 * @since 4.1.0
                 */
                alternateStartingDirection: false,
                /**
                 * Used together with the levels and allowTraversingTree options. When
                 * set to false the first level visible to be level one, which is
                 * dynamic when traversing the tree. Otherwise the level will be the
                 * same as the tree structure.
                 *
                 * @since 4.1.0
                 */
                levelIsConstant: true,
                /**
                 * Options for the button appearing when traversing down in a treemap.
                 *
                 * Since v9.3.3 the `traverseUpButton` is replaced by `breadcrumbs`.
                 *
                 * @deprecated
                 */
                traverseUpButton: {
                    /**
                     * The position of the button.
                     */
                    position: {
                        /**
                         * Vertical alignment of the button.
                         *
                         * @type      {Highcharts.VerticalAlignValue}
                         * @default   top
                         * @product   highcharts
                         * @apioption plotOptions.treemap.traverseUpButton.position.verticalAlign
                         */
                        /**
                         * Horizontal alignment of the button.
                         *
                         * @type {Highcharts.AlignValue}
                         */
                        align: 'right',
                        /**
                         * Horizontal offset of the button.
                         */
                        x: -10,
                        /**
                         * Vertical offset of the button.
                         */
                        y: 10
                    }
                },
                /**
                 * Set options on specific levels. Takes precedence over series options,
                 * but not point options.
                 *
                 * @sample {highcharts} highcharts/plotoptions/treemap-levels/
                 *         Styling dataLabels and borders
                 * @sample {highcharts} highcharts/demo/treemap-with-levels/
                 *         Different layoutAlgorithm
                 *
                 * @type      {Array<*>}
                 * @since     4.1.0
                 * @product   highcharts
                 * @apioption plotOptions.treemap.levels
                 */
                /**
                 * Can set a `borderColor` on all points which lies on the same level.
                 *
                 * @type      {Highcharts.ColorString}
                 * @since     4.1.0
                 * @product   highcharts
                 * @apioption plotOptions.treemap.levels.borderColor
                 */
                /**
                 * Set the dash style of the border of all the point which lies on the
                 * level. See
                 * [plotOptions.scatter.dashStyle](#plotoptions.scatter.dashstyle)
                 * for possible options.
                 *
                 * @type      {Highcharts.DashStyleValue}
                 * @since     4.1.0
                 * @product   highcharts
                 * @apioption plotOptions.treemap.levels.borderDashStyle
                 */
                /**
                 * Can set the borderWidth on all points which lies on the same level.
                 *
                 * @type      {number}
                 * @since     4.1.0
                 * @product   highcharts
                 * @apioption plotOptions.treemap.levels.borderWidth
                 */
                /**
                 * Can set a color on all points which lies on the same level.
                 *
                 * @type      {Highcharts.ColorString|Highcharts.GradientColorObject|Highcharts.PatternObject}
                 * @since     4.1.0
                 * @product   highcharts
                 * @apioption plotOptions.treemap.levels.color
                 */
                /**
                 * A configuration object to define how the color of a child varies from
                 * the parent's color. The variation is distributed among the children
                 * of node. For example when setting brightness, the brightness change
                 * will range from the parent's original brightness on the first child,
                 * to the amount set in the `to` setting on the last node. This allows a
                 * gradient-like color scheme that sets children out from each other
                 * while highlighting the grouping on treemaps and sectors on sunburst
                 * charts.
                 *
                 * @sample highcharts/demo/sunburst/
                 *         Sunburst with color variation
                 *
                 * @since     6.0.0
                 * @product   highcharts
                 * @apioption plotOptions.treemap.levels.colorVariation
                 */
                /**
                 * The key of a color variation. Currently supports `brightness` only.
                 *
                 * @type       {string}
                 * @since      6.0.0
                 * @product    highcharts
                 * @validvalue ["brightness"]
                 * @apioption  plotOptions.treemap.levels.colorVariation.key
                 */
                /**
                 * The ending value of a color variation. The last sibling will receive
                 * this value.
                 *
                 * @type      {number}
                 * @since     6.0.0
                 * @product   highcharts
                 * @apioption plotOptions.treemap.levels.colorVariation.to
                 */
                /**
                 * Can set the options of dataLabels on each point which lies on the
                 * level.
                 * [plotOptions.treemap.dataLabels](#plotOptions.treemap.dataLabels) for
                 * possible values.
                 *
                 * @extends   plotOptions.treemap.dataLabels
                 * @since     4.1.0
                 * @product   highcharts
                 * @apioption plotOptions.treemap.levels.dataLabels
                 */
                /**
                 * Can set the layoutAlgorithm option on a specific level.
                 *
                 * @type       {string}
                 * @since      4.1.0
                 * @product    highcharts
                 * @validvalue ["sliceAndDice", "stripes", "squarified", "strip"]
                 * @apioption  plotOptions.treemap.levels.layoutAlgorithm
                 */
                /**
                 * Can set the layoutStartingDirection option on a specific level.
                 *
                 * @type       {string}
                 * @since      4.1.0
                 * @product    highcharts
                 * @validvalue ["vertical", "horizontal"]
                 * @apioption  plotOptions.treemap.levels.layoutStartingDirection
                 */
                /**
                 * Decides which level takes effect from the options set in the levels
                 * object.
                 *
                 * @sample {highcharts} highcharts/plotoptions/treemap-levels/
                 *         Styling of both levels
                 *
                 * @type      {number}
                 * @since     4.1.0
                 * @product   highcharts
                 * @apioption plotOptions.treemap.levels.level
                 */
                // Presentational options
                /**
                 * The color of the border surrounding each tree map item.
                 *
                 * @type {Highcharts.ColorString}
                 */
                borderColor: "#e6e6e6" /* Palette.neutralColor10 */,
                /**
                 * The width of the border surrounding each tree map item.
                 */
                borderWidth: 1,
                colorKey: 'colorValue',
                /**
                 * The opacity of a point in treemap. When a point has children, the
                 * visibility of the children is determined by the opacity.
                 *
                 * @since 4.2.4
                 */
                opacity: 0.15,
                /**
                 * A wrapper object for all the series options in specific states.
                 *
                 * @extends plotOptions.heatmap.states
                 */
                states: {
                    /**
                     * Options for the hovered series
                     *
                     * @extends   plotOptions.heatmap.states.hover
                     * @excluding halo
                     */
                    hover: {
                        /**
                         * The border color for the hovered state.
                         */
                        borderColor: "#999999" /* Palette.neutralColor40 */,
                        /**
                         * Brightness for the hovered point. Defaults to 0 if the
                         * heatmap series is loaded first, otherwise 0.1.
                         *
                         * @type    {number}
                         * @default undefined
                         */
                        brightness: HeatmapSeries ? 0 : 0.1,
                        /**
                         * @extends plotOptions.heatmap.states.hover.halo
                         */
                        halo: false,
                        /**
                         * The opacity of a point in treemap. When a point has children,
                         * the visibility of the children is determined by the opacity.
                         *
                         * @since 4.2.4
                         */
                        opacity: 0.75,
                        /**
                         * The shadow option for hovered state.
                         */
                        shadow: false
                    }
                }
            });
            return TreemapSeries;
        }(ScatterSeries));
        extend(TreemapSeries.prototype, {
            buildKDTree: noop,
            colorAttribs: ColorMapComposition.seriesMembers.colorAttribs,
            colorKey: 'colorValue',
            directTouch: true,
            drawLegendSymbol: LegendSymbol.drawRectangle,
            getExtremesFromAll: true,
            getSymbol: noop,
            optionalAxis: 'colorAxis',
            parallelArrays: ['x', 'y', 'value', 'colorValue'],
            pointArrayMap: ['value'],
            pointClass: TreemapPoint,
            NodeClass: TreemapNode,
            trackerGroups: ['group', 'dataLabelsGroup'],
            utils: {
                recursive: TreemapUtilities.recursive
            }
        });
        ColorMapComposition.compose(TreemapSeries);
        SeriesRegistry.registerSeriesType('treemap', TreemapSeries);
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
         * A `treemap` series. If the [type](#series.treemap.type) option is
         * not specified, it is inherited from [chart.type](#chart.type).
         *
         * @extends   series,plotOptions.treemap
         * @excluding dataParser, dataURL, stack, dataSorting
         * @product   highcharts
         * @requires  modules/treemap
         * @apioption series.treemap
         */
        /**
         * An array of data points for the series. For the `treemap` series
         * type, points can be given in the following ways:
         *
         * 1. An array of numerical values. In this case, the numerical values will be
         *    interpreted as `value` options. Example:
         *    ```js
         *    data: [0, 5, 3, 5]
         *    ```
         *
         * 2. An array of objects with named values. The following snippet shows only a
         *    few settings, see the complete options set below. If the total number of
         *    data points exceeds the series'
         *    [turboThreshold](#series.treemap.turboThreshold),
         *    this option is not available.
         *    ```js
         *      data: [{
         *        value: 9,
         *        name: "Point2",
         *        color: "#00FF00"
         *      }, {
         *        value: 6,
         *        name: "Point1",
         *        color: "#FF00FF"
         *      }]
         *    ```
         *
         * @sample {highcharts} highcharts/chart/reflow-true/
         *         Numerical values
         * @sample {highcharts} highcharts/series/data-array-of-objects/
         *         Config objects
         *
         * @type      {Array<number|null|*>}
         * @extends   series.heatmap.data
         * @excluding x, y, pointPadding
         * @product   highcharts
         * @apioption series.treemap.data
         */
        /**
         * The value of the point, resulting in a relative area of the point
         * in the treemap.
         *
         * @type      {number|null}
         * @product   highcharts
         * @apioption series.treemap.data.value
         */
        /**
         * Serves a purpose only if a `colorAxis` object is defined in the chart
         * options. This value will decide which color the point gets from the
         * scale of the colorAxis.
         *
         * @type      {number}
         * @since     4.1.0
         * @product   highcharts
         * @apioption series.treemap.data.colorValue
         */
        /**
         * Only for treemap. Use this option to build a tree structure. The
         * value should be the id of the point which is the parent. If no points
         * has a matching id, or this option is undefined, then the parent will
         * be set to the root.
         *
         * @sample {highcharts} highcharts/point/parent/
         *         Point parent
         * @sample {highcharts} highcharts/demo/treemap-with-levels/
         *         Example where parent id is not matching
         *
         * @type      {string}
         * @since     4.1.0
         * @product   highcharts
         * @apioption series.treemap.data.parent
         */
        ''; // adds doclets above to transpiled file

        return TreemapSeries;
    });
    _registerModule(_modules, 'Series/Sunburst/SunburstPoint.js', [_modules['Core/Series/SeriesRegistry.js'], _modules['Core/Utilities.js']], function (SeriesRegistry, U) {
        /* *
         *
         *  This module implements sunburst charts in Highcharts.
         *
         *  (c) 2016-2021 Highsoft AS
         *
         *  Authors: Jon Arild Nygard
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
        var Point = SeriesRegistry.series.prototype.pointClass,
            TreemapPoint = SeriesRegistry.seriesTypes.treemap.prototype.pointClass;
        var correctFloat = U.correctFloat,
            extend = U.extend;
        /* *
         *
         *  Class
         *
         * */
        var SunburstPoint = /** @class */ (function (_super) {
                __extends(SunburstPoint, _super);
            function SunburstPoint() {
                /* *
                 *
                 *  Properties
                 *
                 * */
                var _this = _super !== null && _super.apply(this,
                    arguments) || this;
                _this.node = void 0;
                _this.options = void 0;
                _this.series = void 0;
                _this.shapeExisting = void 0;
                _this.shapeType = void 0;
                return _this;
                /* eslint-enable valid-jsdoc */
            }
            /* *
             *
             *  Functions
             *
             * */
            /* eslint-disable valid-jsdoc */
            SunburstPoint.prototype.getDataLabelPath = function (label) {
                var renderer = this.series.chart.renderer,
                    shapeArgs = this.shapeExisting,
                    start = shapeArgs.start,
                    end = shapeArgs.end,
                    angle = start + (end - start) / 2, // arc middle value
                    upperHalf = angle < 0 &&
                        angle > -Math.PI ||
                        angle > Math.PI,
                    r = (shapeArgs.r + (label.options.distance || 0)),
                    moreThanHalf;
                // Check if point is a full circle
                if (start === -Math.PI / 2 &&
                    correctFloat(end) === correctFloat(Math.PI * 1.5)) {
                    start = -Math.PI + Math.PI / 360;
                    end = -Math.PI / 360;
                    upperHalf = true;
                }
                // Check if dataLabels should be render in the
                // upper half of the circle
                if (end - start > Math.PI) {
                    upperHalf = false;
                    moreThanHalf = true;
                }
                if (this.dataLabelPath) {
                    this.dataLabelPath = this.dataLabelPath.destroy();
                }
                // All times
                this.dataLabelPath = renderer
                    .arc({
                    open: true,
                    longArc: moreThanHalf ? 1 : 0
                })
                    .attr({
                    start: (upperHalf ? start : end),
                    end: (upperHalf ? end : start),
                    clockwise: +upperHalf,
                    x: shapeArgs.x,
                    y: shapeArgs.y,
                    r: (r + shapeArgs.innerR) / 2
                })
                    .add(renderer.defs);
                return this.dataLabelPath;
            };
            SunburstPoint.prototype.isValid = function () {
                return true;
            };
            return SunburstPoint;
        }(TreemapPoint));
        extend(SunburstPoint.prototype, {
            getClassName: Point.prototype.getClassName,
            haloPath: Point.prototype.haloPath,
            setState: Point.prototype.setState
        });
        /* *
         *
         *  Defaul Export
         *
         * */

        return SunburstPoint;
    });
    _registerModule(_modules, 'Series/Sunburst/SunburstUtilities.js', [_modules['Core/Series/SeriesRegistry.js'], _modules['Core/Utilities.js']], function (SeriesRegistry, U) {
        /* *
         *
         *  This module implements sunburst charts in Highcharts.
         *
         *  (c) 2016-2021 Highsoft AS
         *
         *  Authors: Jon Arild Nygard
         *
         *  License: www.highcharts.com/license
         *
         *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
         *
         * */
        var TreemapSeries = SeriesRegistry.seriesTypes.treemap;
        var isNumber = U.isNumber,
            isObject = U.isObject,
            merge = U.merge;
        /* *
         *
         *  Namespace
         *
         * */
        var SunburstUtilities;
        (function (SunburstUtilities) {
            /* *
             *
             *  Constants
             *
             * */
            SunburstUtilities.recursive = TreemapSeries.prototype.utils.recursive;
            /* *
             *
             *  Functions
             *
             * */
            /* eslint-disable valid-jsdoc */
            /**
             * @private
             * @function calculateLevelSizes
             *
             * @param {Object} levelOptions
             * Map of level to its options.
             *
             * @param {Highcharts.Dictionary<number>} params
             * Object containing number parameters `innerRadius` and `outerRadius`.
             *
             * @return {Highcharts.SunburstSeriesLevelsOptions|undefined}
             * Returns the modified options, or undefined.
             */
            function calculateLevelSizes(levelOptions, params) {
                var result,
                    p = isObject(params) ? params : {},
                    totalWeight = 0,
                    diffRadius,
                    levels,
                    levelsNotIncluded,
                    remainingSize,
                    from,
                    to;
                if (isObject(levelOptions)) {
                    result = merge({}, levelOptions);
                    from = isNumber(p.from) ? p.from : 0;
                    to = isNumber(p.to) ? p.to : 0;
                    levels = range(from, to);
                    levelsNotIncluded = Object.keys(result).filter(function (k) {
                        return levels.indexOf(+k) === -1;
                    });
                    diffRadius = remainingSize = isNumber(p.diffRadius) ?
                        p.diffRadius : 0;
                    // Convert percentage to pixels.
                    // Calculate the remaining size to divide between "weight" levels.
                    // Calculate total weight to use in convertion from weight to
                    // pixels.
                    levels.forEach(function (level) {
                        var options = result[level],
                            unit = options.levelSize.unit,
                            value = options.levelSize.value;
                        if (unit === 'weight') {
                            totalWeight += value;
                        }
                        else if (unit === 'percentage') {
                            options.levelSize = {
                                unit: 'pixels',
                                value: (value / 100) * diffRadius
                            };
                            remainingSize -= options.levelSize.value;
                        }
                        else if (unit === 'pixels') {
                            remainingSize -= value;
                        }
                    });
                    // Convert weight to pixels.
                    levels.forEach(function (level) {
                        var options = result[level],
                            weight;
                        if (options.levelSize.unit === 'weight') {
                            weight = options.levelSize.value;
                            result[level].levelSize = {
                                unit: 'pixels',
                                value: (weight / totalWeight) * remainingSize
                            };
                        }
                    });
                    // Set all levels not included in interval [from,to] to have 0
                    // pixels.
                    levelsNotIncluded.forEach(function (level) {
                        result[level].levelSize = {
                            value: 0,
                            unit: 'pixels'
                        };
                    });
                }
                return result;
            }
            SunburstUtilities.calculateLevelSizes = calculateLevelSizes;
            /**
             * @private
             */
            function getLevelFromAndTo(_a) {
                var level = _a.level,
                    height = _a.height;
                //  Never displays level below 1
                var from = level > 0 ? level : 1;
                var to = level + height;
                return { from: from, to: to };
            }
            SunburstUtilities.getLevelFromAndTo = getLevelFromAndTo;
            /**
             * TODO introduce step, which should default to 1.
             * @private
             */
            function range(from, to) {
                var result = [],
                    i;
                if (isNumber(from) && isNumber(to) && from <= to) {
                    for (i = from; i <= to; i++) {
                        result.push(i);
                    }
                }
                return result;
            }
            SunburstUtilities.range = range;
            /* eslint-enable valid-jsdoc */
        })(SunburstUtilities || (SunburstUtilities = {}));
        /* *
         *
         *  Default Export
         *
         * */

        return SunburstUtilities;
    });
    _registerModule(_modules, 'Series/Sunburst/SunburstNode.js', [_modules['Series/Treemap/TreemapNode.js']], function (TreemapNode) {
        /* *
         *
         *  (c) 2010-2022 Pawel Lysy
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
        var SunburstNode = /** @class */ (function (_super) {
                __extends(SunburstNode, _super);
            function SunburstNode() {
                return _super !== null && _super.apply(this, arguments) || this;
            }
            return SunburstNode;
        }(TreemapNode));

        return SunburstNode;
    });
    _registerModule(_modules, 'Series/Sunburst/SunburstSeries.js', [_modules['Series/CenteredUtilities.js'], _modules['Core/Globals.js'], _modules['Core/Series/SeriesRegistry.js'], _modules['Series/Sunburst/SunburstPoint.js'], _modules['Series/Sunburst/SunburstUtilities.js'], _modules['Series/TreeUtilities.js'], _modules['Core/Utilities.js'], _modules['Series/Sunburst/SunburstNode.js']], function (CU, H, SeriesRegistry, SunburstPoint, SunburstUtilities, TU, U, SunburstNode) {
        /* *
         *
         *  This module implements sunburst charts in Highcharts.
         *
         *  (c) 2016-2021 Highsoft AS
         *
         *  Authors: Jon Arild Nygard
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
        var getCenter = CU.getCenter,
            getStartAndEndRadians = CU.getStartAndEndRadians;
        var noop = H.noop;
        var Series = SeriesRegistry.series,
            _a = SeriesRegistry.seriesTypes,
            ColumnSeries = _a.column,
            TreemapSeries = _a.treemap;
        var getColor = TU.getColor,
            getLevelOptions = TU.getLevelOptions,
            setTreeValues = TU.setTreeValues,
            updateRootId = TU.updateRootId;
        var error = U.error,
            extend = U.extend,
            isNumber = U.isNumber,
            isObject = U.isObject,
            isString = U.isString,
            merge = U.merge,
            splat = U.splat;
        /* *
         *
         *  Constants
         *
         * */
        var rad2deg = 180 / Math.PI;
        /* *
         *
         *  Functions
         *
         * */
        // eslint-disable-next-line require-jsdoc
        function isBoolean(x) {
            return typeof x === 'boolean';
        }
        /**
         * Find a set of coordinates given a start coordinates, an angle, and a
         * distance.
         *
         * @private
         * @function getEndPoint
         *
         * @param {number} x
         *        Start coordinate x
         *
         * @param {number} y
         *        Start coordinate y
         *
         * @param {number} angle
         *        Angle in radians
         *
         * @param {number} distance
         *        Distance from start to end coordinates
         *
         * @return {Highcharts.SVGAttributes}
         *         Returns the end coordinates, x and y.
         */
        var getEndPoint = function getEndPoint(x,
            y,
            angle,
            distance) {
                return {
                    x: x + (Math.cos(angle) * distance),
                    y: y + (Math.sin(angle) * distance)
                };
        };
        // eslint-disable-next-line require-jsdoc
        function getDlOptions(params) {
            // Set options to new object to avoid problems with scope
            var point = params.point,
                shape = isObject(params.shapeArgs) ? params.shapeArgs : {},
                optionsPoint = (isObject(params.optionsPoint) ?
                    params.optionsPoint.dataLabels :
                    {}), 
                // The splat was used because levels dataLabels
                // options doesn't work as an array
                optionsLevel = splat(isObject(params.level) ?
                    params.level.dataLabels :
                    {})[0],
                options = merge({
                    style: {}
                },
                optionsLevel,
                optionsPoint),
                rotationRad,
                rotation,
                rotationMode = options.rotationMode;
            if (!isNumber(options.rotation)) {
                if (rotationMode === 'auto' || rotationMode === 'circular') {
                    if (point.innerArcLength < 1 &&
                        point.outerArcLength > shape.radius) {
                        rotationRad = 0;
                        // Trigger setTextPath function to get textOutline etc.
                        if (point.dataLabelPath && rotationMode === 'circular') {
                            options.textPath = {
                                enabled: true
                            };
                        }
                    }
                    else if (point.innerArcLength > 1 &&
                        point.outerArcLength > 1.5 * shape.radius) {
                        if (rotationMode === 'circular') {
                            options.textPath = {
                                enabled: true,
                                attributes: {
                                    dy: 5
                                }
                            };
                        }
                        else {
                            rotationMode = 'parallel';
                        }
                    }
                    else {
                        // Trigger the destroyTextPath function
                        if (point.dataLabel &&
                            point.dataLabel.textPath &&
                            rotationMode === 'circular') {
                            options.textPath = {
                                enabled: false
                            };
                        }
                        rotationMode = 'perpendicular';
                    }
                }
                if (rotationMode !== 'auto' && rotationMode !== 'circular') {
                    rotationRad = (shape.end -
                        (shape.end - shape.start) / 2);
                }
                if (rotationMode === 'parallel') {
                    options.style.width = Math.min(shape.radius * 2.5, (point.outerArcLength + point.innerArcLength) / 2);
                }
                else {
                    options.style.width = shape.radius;
                }
                if (rotationMode === 'perpendicular' &&
                    point.series.chart.renderer.fontMetrics(options.style.fontSize).h > point.outerArcLength) {
                    options.style.width = 1;
                }
                // Apply padding (#8515)
                options.style.width = Math.max(options.style.width - 2 * (options.padding || 0), 1);
                rotation = (rotationRad * rad2deg) % 180;
                if (rotationMode === 'parallel') {
                    rotation -= 90;
                }
                // Prevent text from rotating upside down
                if (rotation > 90) {
                    rotation -= 180;
                }
                else if (rotation < -90) {
                    rotation += 180;
                }
                options.rotation = rotation;
            }
            if (options.textPath) {
                if (point.shapeExisting.innerR === 0 &&
                    options.textPath.enabled) {
                    // Enable rotation to render text
                    options.rotation = 0;
                    // Center dataLabel - disable textPath
                    options.textPath.enabled = false;
                    // Setting width and padding
                    options.style.width = Math.max((point.shapeExisting.r * 2) -
                        2 * (options.padding || 0), 1);
                }
                else if (point.dlOptions &&
                    point.dlOptions.textPath &&
                    !point.dlOptions.textPath.enabled &&
                    (rotationMode === 'circular')) {
                    // Bring dataLabel back if was a center dataLabel
                    options.textPath.enabled = true;
                }
                if (options.textPath.enabled) {
                    // Enable rotation to render text
                    options.rotation = 0;
                    // Setting width and padding
                    options.style.width = Math.max((point.outerArcLength +
                        point.innerArcLength) / 2 -
                        2 * (options.padding || 0), 1);
                }
            }
            // NOTE: alignDataLabel positions the data label differntly when rotation is
            // 0. Avoiding this by setting rotation to a small number.
            if (options.rotation === 0) {
                options.rotation = 0.001;
            }
            return options;
        }
        // eslint-disable-next-line require-jsdoc
        function getAnimation(shape, params) {
            var point = params.point,
                radians = params.radians,
                innerR = params.innerR,
                idRoot = params.idRoot,
                idPreviousRoot = params.idPreviousRoot,
                shapeExisting = params.shapeExisting,
                shapeRoot = params.shapeRoot,
                shapePreviousRoot = params.shapePreviousRoot,
                visible = params.visible,
                from = {},
                to = {
                    end: shape.end,
                    start: shape.start,
                    innerR: shape.innerR,
                    r: shape.r,
                    x: shape.x,
                    y: shape.y
                };
            if (visible) {
                // Animate points in
                if (!point.graphic && shapePreviousRoot) {
                    if (idRoot === point.id) {
                        from = {
                            start: radians.start,
                            end: radians.end
                        };
                    }
                    else {
                        from = (shapePreviousRoot.end <= shape.start) ? {
                            start: radians.end,
                            end: radians.end
                        } : {
                            start: radians.start,
                            end: radians.start
                        };
                    }
                    // Animate from center and outwards.
                    from.innerR = from.r = innerR;
                }
            }
            else {
                // Animate points out
                if (point.graphic) {
                    if (idPreviousRoot === point.id) {
                        to = {
                            innerR: innerR,
                            r: innerR
                        };
                    }
                    else if (shapeRoot) {
                        to = (shapeRoot.end <= shapeExisting.start) ?
                            {
                                innerR: innerR,
                                r: innerR,
                                start: radians.end,
                                end: radians.end
                            } : {
                            innerR: innerR,
                            r: innerR,
                            start: radians.start,
                            end: radians.start
                        };
                    }
                }
            }
            return {
                from: from,
                to: to
            };
        }
        // eslint-disable-next-line require-jsdoc
        function getDrillId(point, idRoot, mapIdToNode) {
            var drillId,
                node = point.node,
                nodeRoot;
            if (!node.isLeaf) {
                // When it is the root node, the drillId should be set to parent.
                if (idRoot === point.id) {
                    nodeRoot = mapIdToNode[idRoot];
                    drillId = nodeRoot.parent;
                }
                else {
                    drillId = point.id;
                }
            }
            return drillId;
        }
        // eslint-disable-next-line require-jsdoc
        function cbSetTreeValuesBefore(node, options) {
            var mapIdToNode = options.mapIdToNode,
                parent = node.parent,
                nodeParent = parent ? mapIdToNode[parent] : void 0,
                series = options.series,
                chart = series.chart,
                points = series.points,
                point = points[node.i],
                colors = series.options.colors || chart && chart.options.colors,
                colorInfo = getColor(node, {
                    colors: colors,
                    colorIndex: series.colorIndex,
                    index: options.index,
                    mapOptionsToLevel: options.mapOptionsToLevel,
                    parentColor: nodeParent && nodeParent.color,
                    parentColorIndex: nodeParent && nodeParent.colorIndex,
                    series: options.series,
                    siblings: options.siblings
                });
            node.color = colorInfo.color;
            node.colorIndex = colorInfo.colorIndex;
            if (point) {
                point.color = node.color;
                point.colorIndex = node.colorIndex;
                // Set slicing on node, but avoid slicing the top node.
                node.sliced = (node.id !== options.idRoot) ? point.sliced : false;
            }
            return node;
        }
        /* *
         *
         *  Class
         *
         * */
        var SunburstSeries = /** @class */ (function (_super) {
                __extends(SunburstSeries, _super);
            function SunburstSeries() {
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
                _this.center = void 0;
                _this.data = void 0;
                _this.mapOptionsToLevel = void 0;
                _this.nodeMap = void 0;
                _this.options = void 0;
                _this.points = void 0;
                _this.shapeRoot = void 0;
                _this.startAndEndRadians = void 0;
                _this.tree = void 0;
                return _this;
                /* eslint-enable valid-jsdoc */
            }
            /* *
             *
             *  Functions
             *
             * */
            /* eslint-disable valid-jsdoc */
            SunburstSeries.prototype.alignDataLabel = function (_point, _dataLabel, labelOptions) {
                if (labelOptions.textPath && labelOptions.textPath.enabled) {
                    return;
                }
                return _super.prototype.alignDataLabel.apply(this, arguments);
            };
            /**
             * Animate the slices in. Similar to the animation of polar charts.
             * @private
             */
            SunburstSeries.prototype.animate = function (init) {
                var chart = this.chart,
                    center = [
                        chart.plotWidth / 2,
                        chart.plotHeight / 2
                    ],
                    plotLeft = chart.plotLeft,
                    plotTop = chart.plotTop,
                    attribs,
                    group = this.group;
                // Initialize the animation
                if (init) {
                    // Scale down the group and place it in the center
                    attribs = {
                        translateX: center[0] + plotLeft,
                        translateY: center[1] + plotTop,
                        scaleX: 0.001,
                        scaleY: 0.001,
                        rotation: 10,
                        opacity: 0.01
                    };
                    group.attr(attribs);
                    // Run the animation
                }
                else {
                    attribs = {
                        translateX: plotLeft,
                        translateY: plotTop,
                        scaleX: 1,
                        scaleY: 1,
                        rotation: 0,
                        opacity: 1
                    };
                    group.animate(attribs, this.options.animation);
                }
            };
            SunburstSeries.prototype.drawPoints = function () {
                var series = this,
                    mapOptionsToLevel = series.mapOptionsToLevel,
                    shapeRoot = series.shapeRoot,
                    group = series.group,
                    hasRendered = series.hasRendered,
                    idRoot = series.rootNode,
                    idPreviousRoot = series.idPreviousRoot,
                    nodeMap = series.nodeMap,
                    nodePreviousRoot = nodeMap[idPreviousRoot],
                    shapePreviousRoot = nodePreviousRoot && nodePreviousRoot.shapeArgs,
                    points = series.points,
                    radians = series.startAndEndRadians,
                    chart = series.chart,
                    optionsChart = chart && chart.options && chart.options.chart || {},
                    animation = (isBoolean(optionsChart.animation) ?
                        optionsChart.animation :
                        true),
                    positions = series.center,
                    center = {
                        x: positions[0],
                        y: positions[1]
                    },
                    innerR = positions[3] / 2,
                    renderer = series.chart.renderer,
                    animateLabels,
                    animateLabelsCalled = false,
                    addedHack = false,
                    hackDataLabelAnimation = !!(animation &&
                        hasRendered &&
                        idRoot !== idPreviousRoot &&
                        series.dataLabelsGroup);
                if (hackDataLabelAnimation) {
                    series.dataLabelsGroup.attr({ opacity: 0 });
                    animateLabels = function () {
                        var s = series;
                        animateLabelsCalled = true;
                        if (s.dataLabelsGroup) {
                            s.dataLabelsGroup.animate({
                                opacity: 1,
                                visibility: 'inherit'
                            });
                        }
                    };
                }
                points.forEach(function (point) {
                    var node = point.node,
                        level = mapOptionsToLevel[node.level],
                        shapeExisting = (point.shapeExisting || {}),
                        shape = node.shapeArgs || {},
                        animationInfo,
                        onComplete,
                        visible = !!(node.visible && node.shapeArgs);
                    if (hasRendered && animation) {
                        animationInfo = getAnimation(shape, {
                            center: center,
                            point: point,
                            radians: radians,
                            innerR: innerR,
                            idRoot: idRoot,
                            idPreviousRoot: idPreviousRoot,
                            shapeExisting: shapeExisting,
                            shapeRoot: shapeRoot,
                            shapePreviousRoot: shapePreviousRoot,
                            visible: visible
                        });
                    }
                    else {
                        // When animation is disabled, attr is called from animation.
                        animationInfo = {
                            to: shape,
                            from: {}
                        };
                    }
                    extend(point, {
                        shapeExisting: shape,
                        tooltipPos: [shape.plotX, shape.plotY],
                        drillId: getDrillId(point, idRoot, nodeMap),
                        name: '' + (point.name || point.id || point.index),
                        plotX: shape.plotX,
                        plotY: shape.plotY,
                        value: node.val,
                        isInside: visible,
                        isNull: !visible // used for dataLabels & point.draw
                    });
                    point.dlOptions = getDlOptions({
                        point: point,
                        level: level,
                        optionsPoint: point.options,
                        shapeArgs: shape
                    });
                    if (!addedHack && visible) {
                        addedHack = true;
                        onComplete = animateLabels;
                    }
                    point.draw({
                        animatableAttribs: animationInfo.to,
                        attribs: extend(animationInfo.from, (!chart.styledMode && series.pointAttribs(point, (point.selected && 'select')))),
                        onComplete: onComplete,
                        group: group,
                        renderer: renderer,
                        shapeType: 'arc',
                        shapeArgs: shape
                    });
                });
                // Draw data labels after points
                // TODO draw labels one by one to avoid addtional looping
                if (hackDataLabelAnimation && addedHack) {
                    series.hasRendered = false;
                    series.options.dataLabels.defer = true;
                    Series.prototype.drawDataLabels.call(series);
                    series.hasRendered = true;
                    // If animateLabels is called before labels were hidden, then call
                    // it again.
                    if (animateLabelsCalled) {
                        animateLabels();
                    }
                }
                else {
                    Series.prototype.drawDataLabels.call(series);
                }
            };
            /**
             * The layout algorithm for the levels.
             * @private
             */
            SunburstSeries.prototype.layoutAlgorithm = function (parent, children, options) {
                var startAngle = parent.start,
                    range = parent.end - startAngle,
                    total = parent.val,
                    x = parent.x,
                    y = parent.y,
                    radius = ((options &&
                        isObject(options.levelSize) &&
                        isNumber(options.levelSize.value)) ?
                        options.levelSize.value :
                        0),
                    innerRadius = parent.r,
                    outerRadius = innerRadius + radius,
                    slicedOffset = options && isNumber(options.slicedOffset) ?
                        options.slicedOffset :
                        0;
                return (children || []).reduce(function (arr, child) {
                    var percentage = (1 / total) * child.val,
                        radians = percentage * range,
                        radiansCenter = startAngle + (radians / 2),
                        offsetPosition = getEndPoint(x,
                        y,
                        radiansCenter,
                        slicedOffset),
                        values = {
                            x: child.sliced ? offsetPosition.x : x,
                            y: child.sliced ? offsetPosition.y : y,
                            innerR: innerRadius,
                            r: outerRadius,
                            radius: radius,
                            start: startAngle,
                            end: startAngle + radians
                        };
                    arr.push(values);
                    startAngle = values.end;
                    return arr;
                }, []);
            };
            /**
             * Set the shape arguments on the nodes. Recursive from root down.
             * @private
             */
            SunburstSeries.prototype.setShapeArgs = function (parent, parentValues, mapOptionsToLevel) {
                var childrenValues = [],
                    level = parent.level + 1,
                    options = mapOptionsToLevel[level], 
                    // Collect all children which should be included
                    children = parent.children.filter(function (n) {
                        return n.visible;
                }), twoPi = 6.28; // Two times Pi.
                childrenValues = this.layoutAlgorithm(parentValues, children, options);
                children.forEach(function (child, index) {
                    var values = childrenValues[index],
                        angle = values.start + ((values.end - values.start) / 2),
                        radius = values.innerR + ((values.r - values.innerR) / 2),
                        radians = (values.end - values.start),
                        isCircle = (values.innerR === 0 && radians > twoPi),
                        center = (isCircle ?
                            { x: values.x,
                        y: values.y } :
                            getEndPoint(values.x,
                        values.y,
                        angle,
                        radius)),
                        val = (child.val ?
                            (child.childrenTotal > child.val ?
                                child.childrenTotal :
                                child.val) :
                            child.childrenTotal);
                    // The inner arc length is a convenience for data label filters.
                    if (this.points[child.i]) {
                        this.points[child.i].innerArcLength = radians * values.innerR;
                        this.points[child.i].outerArcLength = radians * values.r;
                    }
                    child.shapeArgs = merge(values, {
                        plotX: center.x,
                        plotY: center.y + 4 * Math.abs(Math.cos(angle))
                    });
                    child.values = merge(values, {
                        val: val
                    });
                    // If node has children, then call method recursively
                    if (child.children.length) {
                        this.setShapeArgs(child, child.values, mapOptionsToLevel);
                    }
                }, this);
            };
            SunburstSeries.prototype.translate = function () {
                var series = this,
                    options = series.options,
                    positions = series.center = series.getCenter(),
                    radians = series.startAndEndRadians = getStartAndEndRadians(options.startAngle,
                    options.endAngle),
                    innerRadius = positions[3] / 2,
                    outerRadius = positions[2] / 2,
                    diffRadius = outerRadius - innerRadius, 
                    // NOTE: updateRootId modifies series.
                    rootId = updateRootId(series),
                    mapIdToNode = series.nodeMap,
                    mapOptionsToLevel,
                    idTop,
                    nodeRoot = mapIdToNode && mapIdToNode[rootId],
                    nodeTop,
                    tree,
                    values,
                    nodeIds = {};
                series.shapeRoot = nodeRoot && nodeRoot.shapeArgs;
                // Call prototype function
                Series.prototype.translate.call(series);
                // @todo Only if series.isDirtyData is true
                tree = series.tree = series.getTree();
                // Render traverseUpButton, after series.nodeMap i calculated.
                mapIdToNode = series.nodeMap;
                nodeRoot = mapIdToNode[rootId];
                idTop = isString(nodeRoot.parent) ? nodeRoot.parent : '';
                nodeTop = mapIdToNode[idTop];
                var _a = SunburstUtilities.getLevelFromAndTo(nodeRoot),
                    from = _a.from,
                    to = _a.to;
                mapOptionsToLevel = getLevelOptions({
                    from: from,
                    levels: series.options.levels,
                    to: to,
                    defaults: {
                        colorByPoint: options.colorByPoint,
                        dataLabels: options.dataLabels,
                        levelIsConstant: options.levelIsConstant,
                        levelSize: options.levelSize,
                        slicedOffset: options.slicedOffset
                    }
                });
                // NOTE consider doing calculateLevelSizes in a callback to
                // getLevelOptions
                mapOptionsToLevel = SunburstUtilities.calculateLevelSizes(mapOptionsToLevel, {
                    diffRadius: diffRadius,
                    from: from,
                    to: to
                });
                // TODO Try to combine setTreeValues & setColorRecursive to avoid
                //  unnecessary looping.
                setTreeValues(tree, {
                    before: cbSetTreeValuesBefore,
                    idRoot: rootId,
                    levelIsConstant: options.levelIsConstant,
                    mapOptionsToLevel: mapOptionsToLevel,
                    mapIdToNode: mapIdToNode,
                    points: series.points,
                    series: series
                });
                values = mapIdToNode[''].shapeArgs = {
                    end: radians.end,
                    r: innerRadius,
                    start: radians.start,
                    val: nodeRoot.val,
                    x: positions[0],
                    y: positions[1]
                };
                this.setShapeArgs(nodeTop, values, mapOptionsToLevel);
                // Set mapOptionsToLevel on series for use in drawPoints.
                series.mapOptionsToLevel = mapOptionsToLevel;
                // #10669 - verify if all nodes have unique ids
                series.data.forEach(function (child) {
                    if (nodeIds[child.id]) {
                        error(31, false, series.chart);
                    }
                    // map
                    nodeIds[child.id] = true;
                });
                // reset object
                nodeIds = {};
            };
            /**
             * A Sunburst displays hierarchical data, where a level in the hierarchy is
             * represented by a circle. The center represents the root node of the tree.
             * The visualization bears a resemblance to both treemap and pie charts.
             *
             * @sample highcharts/demo/sunburst
             *         Sunburst chart
             *
             * @extends      plotOptions.pie
             * @excluding    allAreas, clip, colorAxis, colorKey, compare, compareBase,
             *               dataGrouping, depth, dragDrop, endAngle, gapSize, gapUnit,
             *               ignoreHiddenPoint, innerSize, joinBy, legendType, linecap,
             *               minSize, navigatorOptions, pointRange
             * @product      highcharts
             * @requires     modules/sunburst.js
             * @optionparent plotOptions.sunburst
             *
             * @private
             */
            SunburstSeries.defaultOptions = merge(TreemapSeries.defaultOptions, {
                /**
                 * Options for the breadcrumbs, the navigation at the top leading the
                 * way up through the traversed levels.
                 *
                 * @since 10.0.0
                 * @product   highcharts
                 * @extends   navigation.breadcrumbs
                 * @optionparent plotOptions.sunburst.breadcrumbs
                 */
                /**
                 * Set options on specific levels. Takes precedence over series options,
                 * but not point options.
                 *
                 * @sample highcharts/demo/sunburst
                 *         Sunburst chart
                 *
                 * @type      {Array<*>}
                 * @apioption plotOptions.sunburst.levels
                 */
                /**
                 * Can set a `borderColor` on all points which lies on the same level.
                 *
                 * @type      {Highcharts.ColorString}
                 * @apioption plotOptions.sunburst.levels.borderColor
                 */
                /**
                 * Can set a `borderWidth` on all points which lies on the same level.
                 *
                 * @type      {number}
                 * @apioption plotOptions.sunburst.levels.borderWidth
                 */
                /**
                 * Can set a `borderDashStyle` on all points which lies on the same
                 * level.
                 *
                 * @type      {Highcharts.DashStyleValue}
                 * @apioption plotOptions.sunburst.levels.borderDashStyle
                 */
                /**
                 * Can set a `color` on all points which lies on the same level.
                 *
                 * @type      {Highcharts.ColorString|Highcharts.GradientColorObject|Highcharts.PatternObject}
                 * @apioption plotOptions.sunburst.levels.color
                 */
                /**
                 * Determines whether the chart should receive one color per point based
                 * on this level.
                 *
                 * @type      {boolean}
                 * @apioption plotOptions.sunburst.levels.colorByPoint
                 */
                /**
                 * Can set a `colorVariation` on all points which lies on the same
                 * level.
                 *
                 * @apioption plotOptions.sunburst.levels.colorVariation
                 */
                /**
                 * The key of a color variation. Currently supports `brightness` only.
                 *
                 * @type      {string}
                 * @apioption plotOptions.sunburst.levels.colorVariation.key
                 */
                /**
                 * The ending value of a color variation. The last sibling will receive
                 * this value.
                 *
                 * @type      {number}
                 * @apioption plotOptions.sunburst.levels.colorVariation.to
                 */
                /**
                 * Can set `dataLabels` on all points which lies on the same level.
                 *
                 * @extends   plotOptions.sunburst.dataLabels
                 * @apioption plotOptions.sunburst.levels.dataLabels
                 */
                /**
                 * Decides which level takes effect from the options set in the levels
                 * object.
                 *
                 * @sample highcharts/demo/sunburst
                 *         Sunburst chart
                 *
                 * @type      {number}
                 * @apioption plotOptions.sunburst.levels.level
                 */
                /**
                 * Can set a `levelSize` on all points which lies on the same level.
                 *
                 * @type      {Object}
                 * @apioption plotOptions.sunburst.levels.levelSize
                 */
                /**
                 * When enabled the user can click on a point which is a parent and
                 * zoom in on its children. Deprecated and replaced by
                 * [allowTraversingTree](#plotOptions.sunburst.allowTraversingTree).
                 *
                 * @deprecated
                 * @type      {boolean}
                 * @default   false
                 * @since     6.0.0
                 * @product   highcharts
                 * @apioption plotOptions.sunburst.allowDrillToNode
                 */
                /**
                 * When enabled the user can click on a point which is a parent and
                 * zoom in on its children.
                 *
                 * @type      {boolean}
                 * @default   false
                 * @since     7.0.3
                 * @product   highcharts
                 * @apioption plotOptions.sunburst.allowTraversingTree
                 */
                /**
                 * The center of the sunburst chart relative to the plot area. Can be
                 * percentages or pixel values.
                 *
                 * @sample {highcharts} highcharts/plotoptions/pie-center/
                 *         Centered at 100, 100
                 *
                 * @type    {Array<number|string>}
                 * @default ["50%", "50%"]
                 * @product highcharts
                 *
                 * @private
                 */
                center: ['50%', '50%'],
                colorByPoint: false,
                /**
                 * Disable inherited opacity from Treemap series.
                 *
                 * @ignore-option
                 *
                 * @private
                 */
                opacity: 1,
                /**
                 * @declare Highcharts.SeriesSunburstDataLabelsOptionsObject
                 *
                 * @private
                 */
                dataLabels: {
                    allowOverlap: true,
                    defer: true,
                    /**
                     * Decides how the data label will be rotated relative to the
                     * perimeter of the sunburst. Valid values are `auto`, `circular`,
                     * `parallel` and `perpendicular`. When `auto`, the best fit will be
                     * computed for the point. The `circular` option works similiar
                     * to `auto`, but uses the `textPath` feature - labels are curved,
                     * resulting in a better layout, however multiple lines and
                     * `textOutline` are not supported.
                     *
                     * The `rotation` option takes precedence over `rotationMode`.
                     *
                     * @type       {string}
                     * @sample {highcharts} highcharts/plotoptions/sunburst-datalabels-rotationmode-circular/
                     *         Circular rotation mode
                     * @validvalue ["auto", "perpendicular", "parallel", "circular"]
                     * @since      6.0.0
                     */
                    rotationMode: 'auto',
                    style: {
                        /** @internal */
                        textOverflow: 'ellipsis'
                    }
                },
                /**
                 * Which point to use as a root in the visualization.
                 *
                 * @type {string}
                 *
                 * @private
                 */
                rootId: void 0,
                /**
                 * Used together with the levels and `allowDrillToNode` options. When
                 * set to false the first level visible when drilling is considered
                 * to be level one. Otherwise the level will be the same as the tree
                 * structure.
                 *
                 * @private
                 */
                levelIsConstant: true,
                /**
                 * Determines the width of the ring per level.
                 *
                 * @sample {highcharts} highcharts/plotoptions/sunburst-levelsize/
                 *         Sunburst with various sizes per level
                 *
                 * @since 6.0.5
                 *
                 * @private
                 */
                levelSize: {
                    /**
                     * The value used for calculating the width of the ring. Its' affect
                     * is determined by `levelSize.unit`.
                     *
                     * @sample {highcharts} highcharts/plotoptions/sunburst-levelsize/
                     *         Sunburst with various sizes per level
                     */
                    value: 1,
                    /**
                     * How to interpret `levelSize.value`.
                     *
                     * - `percentage` gives a width relative to result of outer radius
                     *   minus inner radius.
                     *
                     * - `pixels` gives the ring a fixed width in pixels.
                     *
                     * - `weight` takes the remaining width after percentage and pixels,
                     *   and distributes it accross all "weighted" levels. The value
                     *   relative to the sum of all weights determines the width.
                     *
                     * @sample {highcharts} highcharts/plotoptions/sunburst-levelsize/
                     *         Sunburst with various sizes per level
                     *
                     * @validvalue ["percentage", "pixels", "weight"]
                     */
                    unit: 'weight'
                },
                /**
                 * Options for the button appearing when traversing down in a sunburst.
                 * Since v9.3.3 the `traverseUpButton` is replaced by `breadcrumbs`.
                 *
                 * @extends   plotOptions.treemap.traverseUpButton
                 * @since     6.0.0
                 * @deprecated
                 * @apioption plotOptions.sunburst.traverseUpButton
                 *
                 */
                /**
                 * If a point is sliced, moved out from the center, how many pixels
                 * should it be moved?.
                 *
                 * @sample highcharts/plotoptions/sunburst-sliced
                 *         Sliced sunburst
                 *
                 * @since 6.0.4
                 *
                 * @private
                 */
                slicedOffset: 10
            });
            return SunburstSeries;
        }(TreemapSeries));
        extend(SunburstSeries.prototype, {
            drawDataLabels: noop,
            getCenter: getCenter,
            // Mark that the sunburst is supported by the series on point feature.
            onPointSupported: true,
            pointAttribs: ColumnSeries.prototype.pointAttribs,
            pointClass: SunburstPoint,
            NodeClass: SunburstNode,
            utils: SunburstUtilities
        });
        SeriesRegistry.registerSeriesType('sunburst', SunburstSeries);
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
         * A `sunburst` series. If the [type](#series.sunburst.type) option is
         * not specified, it is inherited from [chart.type](#chart.type).
         *
         * @extends   series,plotOptions.sunburst
         * @excluding dataParser, dataURL, stack, dataSorting, boostThreshold,
         *            boostBlending
         * @product   highcharts
         * @requires  modules/sunburst.js
         * @apioption series.sunburst
         */
        /**
         * @type      {Array<number|null|*>}
         * @extends   series.treemap.data
         * @excluding x, y
         * @product   highcharts
         * @apioption series.sunburst.data
         */
        /**
         * @type      {Highcharts.SeriesSunburstDataLabelsOptionsObject|Array<Highcharts.SeriesSunburstDataLabelsOptionsObject>}
         * @product   highcharts
         * @apioption series.sunburst.data.dataLabels
         */
        /**
         * The value of the point, resulting in a relative area of the point
         * in the sunburst.
         *
         * @type      {number|null}
         * @since     6.0.0
         * @product   highcharts
         * @apioption series.sunburst.data.value
         */
        /**
         * Use this option to build a tree structure. The value should be the id of the
         * point which is the parent. If no points has a matching id, or this option is
         * undefined, then the parent will be set to the root.
         *
         * @type      {string}
         * @since     6.0.0
         * @product   highcharts
         * @apioption series.sunburst.data.parent
         */
        /**
          * Whether to display a slice offset from the center. When a sunburst point is
          * sliced, its children are also offset.
          *
          * @sample highcharts/plotoptions/sunburst-sliced
          *         Sliced sunburst
          *
          * @type      {boolean}
          * @default   false
          * @since     6.0.4
          * @product   highcharts
          * @apioption series.sunburst.data.sliced
          */
        ''; // detach doclets above

        return SunburstSeries;
    });
    _registerModule(_modules, 'masters/modules/sunburst.src.js', [], function () {


    });
}));