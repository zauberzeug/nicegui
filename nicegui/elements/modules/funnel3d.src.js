/**
 * @license Highcharts JS v10.3.2 (2022-11-28)
 *
 * Highcharts funnel module
 *
 * (c) 2010-2021 Kacper Madej
 *
 * License: www.highcharts.com/license
 */
(function (factory) {
    if (typeof module === 'object' && module.exports) {
        factory['default'] = factory;
        module.exports = factory;
    } else if (typeof define === 'function' && define.amd) {
        define('highcharts/modules/funnel3d', ['highcharts', 'highcharts/highcharts-3d', 'highcharts/modules/cylinder'], function (Highcharts) {
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
    _registerModule(_modules, 'Series/Funnel3D/Funnel3DComposition.js', [_modules['Core/Color/Color.js'], _modules['Core/Globals.js'], _modules['Core/Renderer/SVG/SVGRenderer3D.js'], _modules['Core/Utilities.js']], function (Color, H, SVGRenderer3D, U) {
        /* *
         *
         *  Highcharts funnel3d series module
         *
         *  (c) 2010-2021 Highsoft AS
         *
         *  Author: Kacper Madej
         *
         *  License: www.highcharts.com/license
         *
         *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
         *
         * */
        var color = Color.parse;
        var charts = H.charts;
        var error = U.error,
            extend = U.extend,
            merge = U.merge;
        /* *
         *
         *  Composition
         *
         * */
        var Funnel3DComposition;
        (function (Funnel3DComposition) {
            /* *
             *
             *  Functions
             *
             * */
            /* eslint-disable require-jsdoc, valid-jsdoc */
            function compose(SVGRendererClass) {
                SVGRenderer3D.compose(SVGRendererClass);
                wrapElement3D(SVGRendererClass.prototype.elements3d);
                wrapRenderer3D(SVGRendererClass);
            }
            Funnel3DComposition.compose = compose;
            function wrapElement3D(elements3d) {
                elements3d.funnel3d = merge(elements3d.cuboid, {
                    parts: [
                        'top', 'bottom',
                        'frontUpper', 'backUpper',
                        'frontLower', 'backLower',
                        'rightUpper', 'rightLower'
                    ],
                    mainParts: ['top', 'bottom'],
                    sideGroups: [
                        'upperGroup', 'lowerGroup'
                    ],
                    sideParts: {
                        upperGroup: ['frontUpper', 'backUpper', 'rightUpper'],
                        lowerGroup: ['frontLower', 'backLower', 'rightLower']
                    },
                    pathType: 'funnel3d',
                    // override opacity and color setters to control opacity
                    opacitySetter: function (opacity) {
                        var funnel3d = this,
                            parts = funnel3d.parts,
                            chart = H.charts[funnel3d.renderer.chartIndex],
                            filterId = 'group-opacity-' + opacity + '-' + chart.index;
                        // use default for top and bottom
                        funnel3d.parts = funnel3d.mainParts;
                        funnel3d.singleSetterForParts('opacity', opacity);
                        // restore
                        funnel3d.parts = parts;
                        if (!chart.renderer.filterId) {
                            chart.renderer.definition({
                                tagName: 'filter',
                                attributes: {
                                    id: filterId
                                },
                                children: [{
                                        tagName: 'feComponentTransfer',
                                        children: [{
                                                tagName: 'feFuncA',
                                                attributes: {
                                                    type: 'table',
                                                    tableValues: '0 ' + opacity
                                                }
                                            }]
                                    }]
                            });
                            funnel3d.sideGroups.forEach(function (groupName) {
                                funnel3d[groupName].attr({
                                    filter: 'url(#' + filterId + ')'
                                });
                            });
                            // styled mode
                            if (funnel3d.renderer.styledMode) {
                                chart.renderer.definition({
                                    tagName: 'style',
                                    textContent: '.highcharts-' + filterId +
                                        ' {filter:url(#' + filterId + ')}'
                                });
                                funnel3d.sideGroups.forEach(function (group) {
                                    group.addClass('highcharts-' + filterId);
                                });
                            }
                        }
                        return funnel3d;
                    },
                    fillSetter: function (fill) {
                        // extract alpha channel to use the opacitySetter
                        var funnel3d = this,
                            fillColor = color(fill),
                            alpha = fillColor.rgba[3],
                            partsWithColor = {
                                // standard color for top and bottom
                                top: color(fill).brighten(0.1).get(),
                                bottom: color(fill).brighten(-0.2).get()
                            };
                        if (alpha < 1) {
                            fillColor.rgba[3] = 1;
                            fillColor = fillColor.get('rgb');
                            // set opacity through the opacitySetter
                            funnel3d.attr({
                                opacity: alpha
                            });
                        }
                        else {
                            // use default for full opacity
                            fillColor = fill;
                        }
                        // add gradient for sides
                        if (!fillColor.linearGradient &&
                            !fillColor.radialGradient &&
                            funnel3d.gradientForSides) {
                            fillColor = {
                                linearGradient: { x1: 0, x2: 1, y1: 1, y2: 1 },
                                stops: [
                                    [0, color(fill).brighten(-0.2).get()],
                                    [0.5, fill],
                                    [1, color(fill).brighten(-0.2).get()]
                                ]
                            };
                        }
                        // gradient support
                        if (fillColor.linearGradient) {
                            // color in steps, as each gradient will generate a key
                            funnel3d.sideGroups.forEach(function (sideGroupName) {
                                var box = funnel3d[sideGroupName].gradientBox,
                                    gradient = fillColor.linearGradient,
                                    alteredGradient = merge(fillColor, {
                                        linearGradient: {
                                            x1: box.x + gradient.x1 * box.width,
                                            y1: box.y + gradient.y1 * box.height,
                                            x2: box.x + gradient.x2 * box.width,
                                            y2: box.y + gradient.y2 * box.height
                                        }
                                    });
                                funnel3d.sideParts[sideGroupName].forEach(function (partName) {
                                    partsWithColor[partName] = alteredGradient;
                                });
                            });
                        }
                        else {
                            merge(true, partsWithColor, {
                                frontUpper: fillColor,
                                backUpper: fillColor,
                                rightUpper: fillColor,
                                frontLower: fillColor,
                                backLower: fillColor,
                                rightLower: fillColor
                            });
                            if (fillColor.radialGradient) {
                                funnel3d.sideGroups.forEach(function (sideGroupName) {
                                    var gradBox = funnel3d[sideGroupName].gradientBox,
                                        centerX = gradBox.x + gradBox.width / 2,
                                        centerY = gradBox.y + gradBox.height / 2,
                                        diameter = Math.min(gradBox.width,
                                        gradBox.height);
                                    funnel3d.sideParts[sideGroupName].forEach(function (partName) {
                                        funnel3d[partName].setRadialReference([
                                            centerX, centerY, diameter
                                        ]);
                                    });
                                });
                            }
                        }
                        funnel3d.singleSetterForParts('fill', null, partsWithColor);
                        // fill for animation getter (#6776)
                        funnel3d.color = funnel3d.fill = fill;
                        // change gradientUnits to userSpaceOnUse for linearGradient
                        if (fillColor.linearGradient) {
                            [funnel3d.frontLower, funnel3d.frontUpper]
                                .forEach(function (part) {
                                var elem = part.element,
                                    grad = (elem &&
                                        funnel3d.renderer.gradients[elem.gradient]);
                                if (grad &&
                                    grad.attr('gradientUnits') !== 'userSpaceOnUse') {
                                    grad.attr({
                                        gradientUnits: 'userSpaceOnUse'
                                    });
                                }
                            });
                        }
                        return funnel3d;
                    },
                    adjustForGradient: function () {
                        var funnel3d = this,
                            bbox;
                        funnel3d.sideGroups.forEach(function (sideGroupName) {
                            // use common extremes for groups for matching gradients
                            var topLeftEdge = {
                                    x: Number.MAX_VALUE,
                                    y: Number.MAX_VALUE
                                },
                                bottomRightEdge = {
                                    x: -Number.MAX_VALUE,
                                    y: -Number.MAX_VALUE
                                };
                            // get extremes
                            funnel3d.sideParts[sideGroupName].forEach(function (partName) {
                                var part = funnel3d[partName];
                                bbox = part.getBBox(true);
                                topLeftEdge = {
                                    x: Math.min(topLeftEdge.x, bbox.x),
                                    y: Math.min(topLeftEdge.y, bbox.y)
                                };
                                bottomRightEdge = {
                                    x: Math.max(bottomRightEdge.x, bbox.x + bbox.width),
                                    y: Math.max(bottomRightEdge.y, bbox.y + bbox.height)
                                };
                            });
                            // store for color fillSetter
                            funnel3d[sideGroupName].gradientBox = {
                                x: topLeftEdge.x,
                                width: bottomRightEdge.x - topLeftEdge.x,
                                y: topLeftEdge.y,
                                height: bottomRightEdge.y - topLeftEdge.y
                            };
                        });
                    },
                    zIndexSetter: function () {
                        // this.added won't work, because zIndex is set after the prop
                        // is set, but before the graphic is really added
                        if (this.finishedOnAdd) {
                            this.adjustForGradient();
                        }
                        // run default
                        return this.renderer.Element.prototype.zIndexSetter.apply(this, arguments);
                    },
                    onAdd: function () {
                        this.adjustForGradient();
                        this.finishedOnAdd = true;
                    }
                });
            }
            function wrapRenderer3D(SVGRendererClass) {
                var rendererProto = SVGRendererClass.prototype;
                extend(rendererProto, {
                    funnel3d: function (shapeArgs) {
                        var renderer = this,
                            funnel3d = renderer.element3d('funnel3d',
                            shapeArgs),
                            styledMode = renderer.styledMode, 
                            // hide stroke for Firefox
                            strokeAttrs = {
                                'stroke-width': 1,
                                stroke: 'none'
                            };
                        // create groups for sides for oppacity setter
                        funnel3d.upperGroup = renderer.g('funnel3d-upper-group').attr({
                            zIndex: funnel3d.frontUpper.zIndex
                        }).add(funnel3d);
                        [
                            funnel3d.frontUpper,
                            funnel3d.backUpper,
                            funnel3d.rightUpper
                        ].forEach(function (upperElem) {
                            if (!styledMode) {
                                upperElem.attr(strokeAttrs);
                            }
                            upperElem.add(funnel3d.upperGroup);
                        });
                        funnel3d.lowerGroup = renderer.g('funnel3d-lower-group').attr({
                            zIndex: funnel3d.frontLower.zIndex
                        }).add(funnel3d);
                        [
                            funnel3d.frontLower,
                            funnel3d.backLower,
                            funnel3d.rightLower
                        ].forEach(function (lowerElem) {
                            if (!styledMode) {
                                lowerElem.attr(strokeAttrs);
                            }
                            lowerElem.add(funnel3d.lowerGroup);
                        });
                        funnel3d.gradientForSides = shapeArgs.gradientForSides;
                        return funnel3d;
                    },
                    /**
                     * Generates paths and zIndexes.
                     * @private
                     */
                    funnel3dPath: function (shapeArgs // @todo: Type it. It's an extended SVGAttributes.
                    ) {
                        // Check getCylinderEnd for better error message if
                        // the cylinder module is missing
                        if (!this.getCylinderEnd) {
                            error('A required Highcharts module is missing: cylinder.js', true, charts[this.chartIndex]);
                        }
                        var renderer = this,
                            chart = charts[renderer.chartIndex], 
                            // adjust angles for visible edges
                            // based on alpha, selected through visual tests
                            alphaCorrection = shapeArgs.alphaCorrection = 90 - Math.abs((chart.options.chart.options3d.alpha % 180) -
                                90), 
                            // set zIndexes of parts based on cubiod logic, for
                            // consistency
                            cuboidData = rendererProto.cuboidPath.call(renderer,
                            merge(shapeArgs, {
                                depth: shapeArgs.width,
                                width: (shapeArgs.width + shapeArgs.bottom.width) / 2
                            })),
                            isTopFirst = cuboidData.isTop,
                            isFrontFirst = !cuboidData.isFront,
                            hasMiddle = !!shapeArgs.middle, 
                            //
                            top = renderer.getCylinderEnd(chart,
                            merge(shapeArgs, {
                                x: shapeArgs.x - shapeArgs.width / 2,
                                z: shapeArgs.z - shapeArgs.width / 2,
                                alphaCorrection: alphaCorrection
                            })),
                            bottomWidth = shapeArgs.bottom.width,
                            bottomArgs = merge(shapeArgs, {
                                width: bottomWidth,
                                x: shapeArgs.x - bottomWidth / 2,
                                z: shapeArgs.z - bottomWidth / 2,
                                alphaCorrection: alphaCorrection
                            }),
                            bottom = renderer.getCylinderEnd(chart,
                            bottomArgs,
                            true), 
                            //
                            middleWidth = bottomWidth,
                            middleTopArgs = bottomArgs,
                            middleTop = bottom,
                            middleBottom = bottom,
                            ret, 
                            // masking for cylinders or a missing part of a side shape
                            useAlphaCorrection;
                        if (hasMiddle) {
                            middleWidth = shapeArgs.middle.width;
                            middleTopArgs = merge(shapeArgs, {
                                y: (shapeArgs.y +
                                    shapeArgs.middle.fraction * shapeArgs.height),
                                width: middleWidth,
                                x: shapeArgs.x - middleWidth / 2,
                                z: shapeArgs.z - middleWidth / 2
                            });
                            middleTop = renderer.getCylinderEnd(chart, middleTopArgs, false);
                            middleBottom = renderer.getCylinderEnd(chart, middleTopArgs, false);
                        }
                        ret = {
                            top: top,
                            bottom: bottom,
                            frontUpper: renderer.getCylinderFront(top, middleTop),
                            zIndexes: {
                                group: cuboidData.zIndexes.group,
                                top: isTopFirst !== 0 ? 0 : 3,
                                bottom: isTopFirst !== 1 ? 0 : 3,
                                frontUpper: isFrontFirst ? 2 : 1,
                                backUpper: isFrontFirst ? 1 : 2,
                                rightUpper: isFrontFirst ? 2 : 1
                            }
                        };
                        ret.backUpper = renderer.getCylinderBack(top, middleTop);
                        useAlphaCorrection = (Math.min(middleWidth, shapeArgs.width) /
                            Math.max(middleWidth, shapeArgs.width)) !== 1;
                        ret.rightUpper = renderer.getCylinderFront(renderer.getCylinderEnd(chart, merge(shapeArgs, {
                            x: shapeArgs.x - shapeArgs.width / 2,
                            z: shapeArgs.z - shapeArgs.width / 2,
                            alphaCorrection: useAlphaCorrection ?
                                -alphaCorrection : 0
                        }), false), renderer.getCylinderEnd(chart, merge(middleTopArgs, {
                            alphaCorrection: useAlphaCorrection ?
                                -alphaCorrection : 0
                        }), !hasMiddle));
                        if (hasMiddle) {
                            useAlphaCorrection = (Math.min(middleWidth, bottomWidth) /
                                Math.max(middleWidth, bottomWidth)) !== 1;
                            merge(true, ret, {
                                frontLower: renderer.getCylinderFront(middleBottom, bottom),
                                backLower: renderer.getCylinderBack(middleBottom, bottom),
                                rightLower: renderer.getCylinderFront(renderer.getCylinderEnd(chart, merge(bottomArgs, {
                                    alphaCorrection: useAlphaCorrection ?
                                        -alphaCorrection : 0
                                }), true), renderer.getCylinderEnd(chart, merge(middleTopArgs, {
                                    alphaCorrection: useAlphaCorrection ?
                                        -alphaCorrection : 0
                                }), false)),
                                zIndexes: {
                                    frontLower: isFrontFirst ? 2 : 1,
                                    backLower: isFrontFirst ? 1 : 2,
                                    rightLower: isFrontFirst ? 1 : 2
                                }
                            });
                        }
                        return ret;
                    }
                });
            }
        })(Funnel3DComposition || (Funnel3DComposition = {}));
        /* *
         *
         *  Default Export
         *
         * */

        return Funnel3DComposition;
    });
    _registerModule(_modules, 'Series/Funnel3D/Funnel3DPoint.js', [_modules['Core/Series/SeriesRegistry.js'], _modules['Core/Utilities.js']], function (SeriesRegistry, U) {
        /* *
         *
         *  Highcharts funnel3d series module
         *
         *  (c) 2010-2021 Highsoft AS
         *
         *  Author: Kacper Madej
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
        var extend = U.extend;
        /* *
         *
         *  Class
         *
         * */
        var Funnel3DPoint = /** @class */ (function (_super) {
                __extends(Funnel3DPoint, _super);
            function Funnel3DPoint() {
                /* *
                 *
                 *  Properties
                 *
                 * */
                var _this = _super !== null && _super.apply(this,
                    arguments) || this;
                _this.dlBoxRaw = void 0;
                _this.options = void 0;
                _this.series = void 0;
                _this.y = void 0;
                return _this;
            }
            return Funnel3DPoint;
        }(ColumnSeries.prototype.pointClass));
        extend(Funnel3DPoint.prototype, {
            shapeType: 'funnel3d'
        });
        /* *
         *
         *  Default Export
         *
         * */

        return Funnel3DPoint;
    });
    _registerModule(_modules, 'Series/Funnel3D/Funnel3DSeries.js', [_modules['Series/Funnel3D/Funnel3DComposition.js'], _modules['Series/Funnel3D/Funnel3DPoint.js'], _modules['Core/Globals.js'], _modules['Core/Math3D.js'], _modules['Core/Series/SeriesRegistry.js'], _modules['Core/Utilities.js']], function (Funnel3DComposition, Funnel3DPoint, H, Math3D, SeriesRegistry, U) {
        /* *
         *
         *  Highcharts funnel3d series module
         *
         *  (c) 2010-2021 Highsoft AS
         *
         *  Author: Kacper Madej
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
        var noop = H.noop;
        var perspective = Math3D.perspective;
        var Series = SeriesRegistry.series,
            ColumnSeries = SeriesRegistry.seriesTypes.column;
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
         * The funnel3d series type.
         *
         * @class
         * @name Highcharts.seriesTypes.funnel3d
         * @augments seriesTypes.column
         * @requires highcharts-3d
         * @requires modules/cylinder
         * @requires modules/funnel3d
         */
        var Funnel3DSeries = /** @class */ (function (_super) {
                __extends(Funnel3DSeries, _super);
            function Funnel3DSeries() {
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
                _this.options = void 0;
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
            /**
             * @private
             */
            Funnel3DSeries.prototype.alignDataLabel = function (point, _dataLabel, options) {
                var series = this,
                    dlBoxRaw = point.dlBoxRaw,
                    inverted = series.chart.inverted,
                    below = point.plotY > pick(series.translatedThreshold,
                    series.yAxis.len),
                    inside = pick(options.inside, !!series.options.stacking),
                    dlBox = {
                        x: dlBoxRaw.x,
                        y: dlBoxRaw.y,
                        height: 0
                    };
                options.align = pick(options.align, !inverted || inside ? 'center' : below ? 'right' : 'left');
                options.verticalAlign = pick(options.verticalAlign, inverted || inside ? 'middle' : below ? 'top' : 'bottom');
                if (options.verticalAlign !== 'top') {
                    dlBox.y += dlBoxRaw.bottom /
                        (options.verticalAlign === 'bottom' ? 1 : 2);
                }
                dlBox.width = series.getWidthAt(dlBox.y);
                if (series.options.reversed) {
                    dlBox.width = dlBoxRaw.fullWidth - dlBox.width;
                }
                if (inside) {
                    dlBox.x -= dlBox.width / 2;
                }
                else {
                    // swap for inside
                    if (options.align === 'left') {
                        options.align = 'right';
                        dlBox.x -= dlBox.width * 1.5;
                    }
                    else if (options.align === 'right') {
                        options.align = 'left';
                        dlBox.x += dlBox.width / 2;
                    }
                    else {
                        dlBox.x -= dlBox.width / 2;
                    }
                }
                point.dlBox = dlBox;
                ColumnSeries.prototype.alignDataLabel.apply(series, arguments);
            };
            /**
             * Override default axis options with series required options for axes.
             * @private
             */
            Funnel3DSeries.prototype.bindAxes = function () {
                Series.prototype.bindAxes.apply(this, arguments);
                extend(this.xAxis.options, {
                    gridLineWidth: 0,
                    lineWidth: 0,
                    title: void 0,
                    tickPositions: []
                });
                merge(true, this.yAxis.options, {
                    gridLineWidth: 0,
                    title: void 0,
                    labels: {
                        enabled: false
                    }
                });
            };
            /**
             * @private
             */
            Funnel3DSeries.prototype.translate = function () {
                Series.prototype.translate.apply(this, arguments);
                var sum = 0,
                    series = this,
                    chart = series.chart,
                    options = series.options,
                    reversed = options.reversed,
                    ignoreHiddenPoint = options.ignoreHiddenPoint,
                    plotWidth = chart.plotWidth,
                    plotHeight = chart.plotHeight,
                    cumulative = 0, // start at top
                    center = options.center,
                    centerX = relativeLength(center[0],
                    plotWidth),
                    centerY = relativeLength(center[1],
                    plotHeight),
                    width = relativeLength(options.width,
                    plotWidth),
                    tempWidth,
                    getWidthAt,
                    height = relativeLength(options.height,
                    plotHeight),
                    neckWidth = relativeLength(options.neckWidth,
                    plotWidth),
                    neckHeight = relativeLength(options.neckHeight,
                    plotHeight),
                    neckY = (centerY - height / 2) + height - neckHeight,
                    data = series.data,
                    fraction,
                    tooltipPos, 
                    //
                    y1,
                    y3,
                    y5, 
                    //
                    h,
                    shapeArgs; // @todo: Type it. It's an extended SVGAttributes.
                    // Return the width at a specific y coordinate
                    series.getWidthAt = getWidthAt = function (y) {
                        var top = (centerY - height / 2);
                    return (y > neckY || height === neckHeight) ?
                        neckWidth :
                        neckWidth + (width - neckWidth) *
                            (1 - (y - top) / (height - neckHeight));
                };
                // Expose
                series.center = [centerX, centerY, height];
                series.centerX = centerX;
                /*
                    * Individual point coordinate naming:
                    *
                    *  _________centerX,y1________
                    *  \                         /
                    *   \                       /
                    *    \                     /
                    *     \                   /
                    *      \                 /
                    *        ___centerX,y3___
                    *
                    * Additional for the base of the neck:
                    *
                    *       |               |
                    *       |               |
                    *       |               |
                    *        ___centerX,y5___
                    */
                // get the total sum
                data.forEach(function (point) {
                    if (!ignoreHiddenPoint || point.visible !== false) {
                        sum += point.y;
                    }
                });
                data.forEach(function (point) {
                    // set start and end positions
                    y5 = null;
                    fraction = sum ? point.y / sum : 0;
                    y1 = centerY - height / 2 + cumulative * height;
                    y3 = y1 + fraction * height;
                    tempWidth = getWidthAt(y1);
                    h = y3 - y1;
                    shapeArgs = {
                        // for fill setter
                        gradientForSides: pick(point.options.gradientForSides, options.gradientForSides),
                        x: centerX,
                        y: y1,
                        height: h,
                        width: tempWidth,
                        z: 1,
                        top: {
                            width: tempWidth
                        }
                    };
                    tempWidth = getWidthAt(y3);
                    shapeArgs.bottom = {
                        fraction: fraction,
                        width: tempWidth
                    };
                    // the entire point is within the neck
                    if (y1 >= neckY) {
                        shapeArgs.isCylinder = true;
                    }
                    else if (y3 > neckY) {
                        // the base of the neck
                        y5 = y3;
                        tempWidth = getWidthAt(neckY);
                        y3 = neckY;
                        shapeArgs.bottom.width = tempWidth;
                        shapeArgs.middle = {
                            fraction: h ? (neckY - y1) / h : 0,
                            width: tempWidth
                        };
                    }
                    if (reversed) {
                        shapeArgs.y = y1 = centerY + height / 2 -
                            (cumulative + fraction) * height;
                        if (shapeArgs.middle) {
                            shapeArgs.middle.fraction = 1 -
                                (h ? shapeArgs.middle.fraction : 0);
                        }
                        tempWidth = shapeArgs.width;
                        shapeArgs.width = shapeArgs.bottom.width;
                        shapeArgs.bottom.width = tempWidth;
                    }
                    point.shapeArgs = extend(point.shapeArgs, shapeArgs);
                    // for tooltips and data labels context
                    point.percentage = fraction * 100;
                    point.plotX = centerX;
                    if (reversed) {
                        point.plotY = centerY + height / 2 -
                            (cumulative + fraction / 2) * height;
                    }
                    else {
                        point.plotY = (y1 + (y5 || y3)) / 2;
                    }
                    // Placement of tooltips and data labels in 3D
                    tooltipPos = perspective([{
                            x: centerX,
                            y: point.plotY,
                            z: reversed ?
                                -(width - getWidthAt(point.plotY)) / 2 :
                                -(getWidthAt(point.plotY)) / 2
                        }], chart, true)[0];
                    point.tooltipPos = [tooltipPos.x, tooltipPos.y];
                    // base to be used when alignment options are known
                    point.dlBoxRaw = {
                        x: centerX,
                        width: getWidthAt(point.plotY),
                        y: y1,
                        bottom: shapeArgs.height || 0,
                        fullWidth: width
                    };
                    if (!ignoreHiddenPoint || point.visible !== false) {
                        cumulative += fraction;
                    }
                });
            };
            Funnel3DSeries.compose = Funnel3DComposition.compose;
            /**
             * A funnel3d is a 3d version of funnel series type. Funnel charts are
             * a type of chart often used to visualize stages in a sales project,
             * where the top are the initial stages with the most clients.
             *
             * It requires that the `highcharts-3d.js`, `cylinder.js` and
             * `funnel3d.js` module are loaded.
             *
             * @sample highcharts/demo/funnel3d/
             *         Funnel3d
             *
             * @extends      plotOptions.column
             * @excluding    allAreas, boostThreshold, colorAxis, compare, compareBase,
             *               dataSorting, boostBlending
             * @product      highcharts
             * @since        7.1.0
             * @requires     highcharts-3d
             * @requires     modules/cylinder
             * @requires     modules/funnel3d
             * @optionparent plotOptions.funnel3d
             */
            Funnel3DSeries.defaultOptions = merge(ColumnSeries.defaultOptions, {
                /** @ignore-option */
                center: ['50%', '50%'],
                /**
                 * The max width of the series compared to the width of the plot area,
                 * or the pixel width if it is a number.
                 *
                 * @type    {number|string}
                 * @sample  {highcharts} highcharts/demo/funnel3d/ Funnel3d demo
                 * @product highcharts
                 */
                width: '90%',
                /**
                 * The width of the neck, the lower part of the funnel. A number defines
                 * pixel width, a percentage string defines a percentage of the plot
                 * area width.
                 *
                 * @type    {number|string}
                 * @sample  {highcharts} highcharts/demo/funnel3d/ Funnel3d demo
                 * @product highcharts
                 */
                neckWidth: '30%',
                /**
                 * The height of the series. If it is a number it defines
                 * the pixel height, if it is a percentage string it is the percentage
                 * of the plot area height.
                 *
                 * @type    {number|string}
                 * @sample  {highcharts} highcharts/demo/funnel3d/ Funnel3d demo
                 * @product highcharts
                 */
                height: '100%',
                /**
                 * The height of the neck, the lower part of the funnel. A number
                 * defines pixel width, a percentage string defines a percentage
                 * of the plot area height.
                 *
                 * @type    {number|string}
                 * @sample  {highcharts} highcharts/demo/funnel3d/ Funnel3d demo
                 * @product highcharts
                 */
                neckHeight: '25%',
                /**
                 * A reversed funnel has the widest area down. A reversed funnel with
                 * no neck width and neck height is a pyramid.
                 *
                 * @product highcharts
                 */
                reversed: false,
                /**
                 * By deafult sides fill is set to a gradient through this option being
                 * set to `true`. Set to `false` to get solid color for the sides.
                 *
                 * @product highcharts
                 */
                gradientForSides: true,
                animation: false,
                edgeWidth: 0,
                colorByPoint: true,
                showInLegend: false,
                dataLabels: {
                    align: 'right',
                    crop: false,
                    inside: false,
                    overflow: 'allow'
                }
            });
            return Funnel3DSeries;
        }(ColumnSeries));
        extend(Funnel3DSeries.prototype, {
            pointClass: Funnel3DPoint,
            translate3dShapes: noop
        });
        SeriesRegistry.registerSeriesType('funnel3d', Funnel3DSeries);
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
         * A `funnel3d` series. If the [type](#series.funnel3d.type) option is
         * not specified, it is inherited from [chart.type](#chart.type).
         *
         * @sample {highcharts} highcharts/demo/funnel3d/
         *         Funnel3d demo
         *
         * @since     7.1.0
         * @extends   series.funnel,plotOptions.funnel3d
         * @excluding allAreas,boostThreshold,colorAxis,compare,compareBase
         * @product   highcharts
         * @requires  highcharts-3d
         * @requires  modules/cylinder
         * @requires  modules/funnel3d
         * @apioption series.funnel3d
         */
        /**
         * An array of data points for the series. For the `funnel3d` series
         * type, points can be given in the following ways:
         *
         * 1.  An array of numerical values. In this case, the numerical values
         * will be interpreted as `y` options. The `x` values will be automatically
         * calculated, either starting at 0 and incremented by 1, or from `pointStart`
         * and `pointInterval` given in the series options. If the axis has
         * categories, these will be used. Example:
         *
         *  ```js
         *  data: [0, 5, 3, 5]
         *  ```
         *
         * 2.  An array of objects with named values. The following snippet shows only a
         * few settings, see the complete options set below. If the total number of data
         * points exceeds the series' [turboThreshold](#series.funnel3d.turboThreshold),
         * this option is not available.
         *
         *  ```js
         *     data: [{
         *         y: 2,
         *         name: "Point2",
         *         color: "#00FF00"
         *     }, {
         *         y: 4,
         *         name: "Point1",
         *         color: "#FF00FF"
         *     }]
         *  ```
         *
         * @sample {highcharts} highcharts/chart/reflow-true/
         *         Numerical values
         * @sample {highcharts} highcharts/series/data-array-of-arrays/
         *         Arrays of numeric x and y
         * @sample {highcharts} highcharts/series/data-array-of-arrays-datetime/
         *         Arrays of datetime x and y
         * @sample {highcharts} highcharts/series/data-array-of-name-value/
         *         Arrays of point.name and y
         * @sample {highcharts} highcharts/series/data-array-of-objects/
         *         Config objects
         *
         * @type      {Array<number|Array<number>|*>}
         * @extends   series.column.data
         * @product   highcharts
         * @apioption series.funnel3d.data
         */
        /**
         * By deafult sides fill is set to a gradient through this option being
         * set to `true`. Set to `false` to get solid color for the sides.
         *
         * @type      {boolean}
         * @product   highcharts
         * @apioption series.funnel3d.data.gradientForSides
         */
        ''; // keeps doclets above in transpiled file

        return Funnel3DSeries;
    });
    _registerModule(_modules, 'masters/modules/funnel3d.src.js', [_modules['Core/Renderer/RendererRegistry.js'], _modules['Series/Funnel3D/Funnel3DSeries.js']], function (RendererRegistry, Funnel3DSeries) {

        Funnel3DSeries.compose(RendererRegistry.getRendererType());

        return Funnel3DSeries;
    });
}));