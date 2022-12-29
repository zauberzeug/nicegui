/**
 * @license Highcharts JS v10.3.2 (2022-11-28)
 *
 * Highcharts cylinder module
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
        define('highcharts/modules/cylinder', ['highcharts', 'highcharts/highcharts-3d'], function (Highcharts) {
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
    _registerModule(_modules, 'Series/Cylinder/CylinderPoint.js', [_modules['Core/Series/SeriesRegistry.js'], _modules['Core/Utilities.js']], function (SeriesRegistry, U) {
        /* *
         *
         *  Highcharts cylinder - a 3D series
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
        var ColumnPoint = SeriesRegistry.seriesTypes.column.prototype.pointClass;
        var extend = U.extend;
        /* *
         *
         *  Class
         *
         * */
        var CylinderPoint = /** @class */ (function (_super) {
                __extends(CylinderPoint, _super);
            function CylinderPoint() {
                /* *
                 *
                 *  Properties
                 *
                 * */
                var _this = _super !== null && _super.apply(this,
                    arguments) || this;
                _this.options = void 0;
                _this.series = void 0;
                return _this;
            }
            return CylinderPoint;
        }(ColumnPoint));
        extend(CylinderPoint.prototype, {
            shapeType: 'cylinder'
        });
        /* *
         *
         *  Default Export
         *
         * */

        return CylinderPoint;
    });
    _registerModule(_modules, 'Series/Cylinder/CylinderComposition.js', [_modules['Core/Color/Color.js'], _modules['Core/Globals.js'], _modules['Core/Math3D.js'], _modules['Core/Renderer/RendererRegistry.js'], _modules['Core/Utilities.js']], function (Color, H, Math3D, RendererRegistry, U) {
        /* *
         *
         *  Highcharts cylinder - a 3D series
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
        var charts = H.charts,
            deg2rad = H.deg2rad;
        var perspective = Math3D.perspective;
        var merge = U.merge,
            pick = U.pick;
        /* *
         *
         *  Composition
         *
         * */
        var rendererProto = RendererRegistry.getRendererType().prototype,
            cuboidPath = rendererProto.cuboidPath;
        // Check if a path is simplified. The simplified path contains only lineTo
        // segments, whereas non-simplified contain curves.
        var isSimplified = function (path) {
                return !path.some(function (seg) { return seg[0] === 'C'; });
        };
        // cylinder extends cuboid
        var cylinderMethods = merge(rendererProto.elements3d.cuboid, {
                parts: ['top', 'bottom', 'front', 'back'],
                pathType: 'cylinder',
                fillSetter: function (fill) {
                    this.singleSetterForParts('fill', null, {
                        front: fill,
                        back: fill,
                        top: color(fill).brighten(0.1).get(),
                        bottom: color(fill).brighten(-0.1).get()
                    });
                // fill for animation getter (#6776)
                this.color = this.fill = fill;
                return this;
            }
        });
        rendererProto.elements3d.cylinder = cylinderMethods;
        rendererProto.cylinder = function (shapeArgs) {
            return this.element3d('cylinder', shapeArgs);
        };
        // Generates paths and zIndexes.
        rendererProto.cylinderPath = function (shapeArgs) {
            var renderer = this,
                chart = charts[renderer.chartIndex], 
                // decide zIndexes of parts based on cubiod logic, for consistency.
                cuboidData = cuboidPath.call(renderer,
                shapeArgs),
                isTopFirst = !cuboidData.isTop,
                isFronFirst = !cuboidData.isFront,
                top = renderer.getCylinderEnd(chart,
                shapeArgs),
                bottom = renderer.getCylinderEnd(chart,
                shapeArgs,
                true);
            return {
                front: renderer.getCylinderFront(top, bottom),
                back: renderer.getCylinderBack(top, bottom),
                top: top,
                bottom: bottom,
                zIndexes: {
                    top: isTopFirst ? 3 : 0,
                    bottom: isTopFirst ? 0 : 3,
                    front: isFronFirst ? 2 : 1,
                    back: isFronFirst ? 1 : 2,
                    group: cuboidData.zIndexes.group
                }
            };
        };
        // Returns cylinder Front path
        rendererProto.getCylinderFront = function (topPath, bottomPath) {
            var path = topPath.slice(0, 3);
            if (isSimplified(bottomPath)) {
                var move = bottomPath[0];
                if (move[0] === 'M') {
                    path.push(bottomPath[2]);
                    path.push(bottomPath[1]);
                    path.push(['L', move[1], move[2]]);
                }
            }
            else {
                var move = bottomPath[0],
                    curve1 = bottomPath[1],
                    curve2 = bottomPath[2];
                if (move[0] === 'M' && curve1[0] === 'C' && curve2[0] === 'C') {
                    path.push(['L', curve2[5], curve2[6]]);
                    path.push([
                        'C',
                        curve2[3],
                        curve2[4],
                        curve2[1],
                        curve2[2],
                        curve1[5],
                        curve1[6]
                    ]);
                    path.push([
                        'C',
                        curve1[3],
                        curve1[4],
                        curve1[1],
                        curve1[2],
                        move[1],
                        move[2]
                    ]);
                }
            }
            path.push(['Z']);
            return path;
        };
        // Returns cylinder Back path
        rendererProto.getCylinderBack = function (topPath, bottomPath) {
            var path = [];
            if (isSimplified(topPath)) {
                var move = topPath[0],
                    line2 = topPath[2];
                if (move[0] === 'M' && line2[0] === 'L') {
                    path.push(['M', line2[1], line2[2]]);
                    path.push(topPath[3]);
                    // End at start
                    path.push(['L', move[1], move[2]]);
                }
            }
            else {
                if (topPath[2][0] === 'C') {
                    path.push(['M', topPath[2][5], topPath[2][6]]);
                }
                path.push(topPath[3], topPath[4]);
            }
            if (isSimplified(bottomPath)) {
                var move = bottomPath[0];
                if (move[0] === 'M') {
                    path.push(['L', move[1], move[2]]);
                    path.push(bottomPath[3]);
                    path.push(bottomPath[2]);
                }
            }
            else {
                var curve2 = bottomPath[2],
                    curve3 = bottomPath[3],
                    curve4 = bottomPath[4];
                if (curve2[0] === 'C' && curve3[0] === 'C' && curve4[0] === 'C') {
                    path.push(['L', curve4[5], curve4[6]]);
                    path.push([
                        'C',
                        curve4[3],
                        curve4[4],
                        curve4[1],
                        curve4[2],
                        curve3[5],
                        curve3[6]
                    ]);
                    path.push([
                        'C',
                        curve3[3],
                        curve3[4],
                        curve3[1],
                        curve3[2],
                        curve2[5],
                        curve2[6]
                    ]);
                }
            }
            path.push(['Z']);
            return path;
        };
        // Retruns cylinder path for top or bottom
        rendererProto.getCylinderEnd = function (chart, shapeArgs, isBottom) {
            var _a = shapeArgs.width,
                width = _a === void 0 ? 0 : _a,
                _b = shapeArgs.height,
                height = _b === void 0 ? 0 : _b,
                _c = shapeArgs.alphaCorrection,
                alphaCorrection = _c === void 0 ? 0 : _c;
            // A half of the smaller one out of width or depth (optional, because
            // there's no depth for a funnel that reuses the code)
            var depth = pick(shapeArgs.depth,
                width, 0),
                radius = Math.min(width,
                depth) / 2, 
                // Approximated longest diameter
                angleOffset = deg2rad * (chart.options.chart.options3d.beta - 90 +
                    alphaCorrection), 
                // Could be top or bottom of the cylinder
                y = (shapeArgs.y || 0) + (isBottom ? height : 0), 
                // Use cubic Bezier curve to draw a cricle in x,z (y is constant).
                // More math. at spencermortensen.com/articles/bezier-circle/
                c = 0.5519 * radius,
                centerX = width / 2 + (shapeArgs.x || 0),
                centerZ = depth / 2 + (shapeArgs.z || 0), 
                // points could be generated in a loop, but readability will plummet
                points = [{
                        x: 0,
                        y: y,
                        z: radius
                    }, {
                        x: c,
                        y: y,
                        z: radius
                    }, {
                        x: radius,
                        y: y,
                        z: c
                    }, {
                        x: radius,
                        y: y,
                        z: 0
                    }, {
                        x: radius,
                        y: y,
                        z: -c
                    }, {
                        x: c,
                        y: y,
                        z: -radius
                    }, {
                        x: 0,
                        y: y,
                        z: -radius
                    }, {
                        x: -c,
                        y: y,
                        z: -radius
                    }, {
                        x: -radius,
                        y: y,
                        z: -c
                    }, {
                        x: -radius,
                        y: y,
                        z: 0
                    }, {
                        x: -radius,
                        y: y,
                        z: c
                    }, {
                        x: -c,
                        y: y,
                        z: radius
                    }, {
                        x: 0,
                        y: y,
                        z: radius
                    }],
                cosTheta = Math.cos(angleOffset),
                sinTheta = Math.sin(angleOffset),
                perspectivePoints,
                path,
                x,
                z;
            // rotete to match chart's beta and translate to the shape center
            points.forEach(function (point, i) {
                x = point.x;
                z = point.z;
                // x′ = (x * cosθ − z * sinθ) + centerX
                // z′ = (z * cosθ + x * sinθ) + centerZ
                points[i].x = (x * cosTheta - z * sinTheta) + centerX;
                points[i].z = (z * cosTheta + x * sinTheta) + centerZ;
            });
            perspectivePoints = perspective(points, chart, true);
            // check for sub-pixel curve issue, compare front and back edges
            if (Math.abs(perspectivePoints[3].y - perspectivePoints[9].y) < 2.5 &&
                Math.abs(perspectivePoints[0].y - perspectivePoints[6].y) < 2.5) {
                // use simplied shape
                path = this.toLinePath([
                    perspectivePoints[0],
                    perspectivePoints[3],
                    perspectivePoints[6],
                    perspectivePoints[9]
                ], true);
            }
            else {
                // or default curved path to imitate ellipse (2D circle)
                path = this.getCurvedPath(perspectivePoints);
            }
            return path;
        };
        // Returns curved path in format of:
        // [ M, x, y, ...[C, cp1x, cp2y, cp2x, cp2y, epx, epy]*n_times ]
        // (cp - control point, ep - end point)
        rendererProto.getCurvedPath = function (points) {
            var path = [['M',
                points[0].x,
                points[0].y]],
                limit = points.length - 2,
                i;
            for (i = 1; i < limit; i += 3) {
                path.push([
                    'C',
                    points[i].x, points[i].y,
                    points[i + 1].x, points[i + 1].y,
                    points[i + 2].x, points[i + 2].y
                ]);
            }
            return path;
        };

    });
    _registerModule(_modules, 'Series/Cylinder/CylinderSeries.js', [_modules['Series/Cylinder/CylinderPoint.js'], _modules['Core/Series/SeriesRegistry.js'], _modules['Core/Utilities.js']], function (CylinderPoint, SeriesRegistry, U) {
        /* *
         *
         *  Highcharts cylinder - a 3D series
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
        var extend = U.extend,
            merge = U.merge;
        /* *
         *
         *  Class
         *
         * */
        /**
         * The cylinder series type.
         *
         * @requires module:highcharts-3d
         * @requires module:modules/cylinder
         *
         * @private
         * @class
         * @name Highcharts.seriesTypes.cylinder
         *
         * @augments Highcharts.Series
         */
        var CylinderSeries = /** @class */ (function (_super) {
                __extends(CylinderSeries, _super);
            function CylinderSeries() {
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
                return _this;
            }
            /**
             * A cylinder graph is a variation of a 3d column graph. The cylinder graph
             * features cylindrical points.
             *
             * @sample {highcharts} highcharts/demo/cylinder/
             *         Cylinder graph
             *
             * @extends      plotOptions.column
             * @since        7.0.0
             * @product      highcharts
             * @excluding    allAreas, boostThreshold, colorAxis, compare, compareBase,
             *               dragDrop, boostBlending
             * @requires     modules/cylinder
             * @optionparent plotOptions.cylinder
             */
            CylinderSeries.defaultOptions = merge(ColumnSeries.defaultOptions);
            return CylinderSeries;
        }(ColumnSeries));
        extend(CylinderSeries.prototype, {
            pointClass: CylinderPoint
        });
        SeriesRegistry.registerSeriesType('cylinder', CylinderSeries);
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
         * A `cylinder` series. If the [type](#series.cylinder.type) option is not
         * specified, it is inherited from [chart.type](#chart.type).
         *
         * @extends   series,plotOptions.cylinder
         * @since     7.0.0
         * @product   highcharts
         * @excluding allAreas, boostThreshold, colorAxis, compare, compareBase,
         *            boostBlending
         * @requires  modules/cylinder
         * @apioption series.cylinder
         */
        /**
         * An array of data points for the series. For the `cylinder` series type,
         * points can be given in the following ways:
         *
         * 1. An array of numerical values. In this case, the numerical values will be
         *    interpreted as `y` options. The `x` values will be automatically
         *    calculated, either starting at 0 and incremented by 1, or from
         *    `pointStart` and `pointInterval` given in the series options. If the axis
         *    has categories, these will be used. Example:
         *    ```js
         *    data: [0, 5, 3, 5]
         *    ```
         *
         * 2. An array of arrays with 2 values. In this case, the values correspond to
         *    `x,y`. If the first value is a string, it is applied as the name of the
         *    point, and the `x` value is inferred.
         *    ```js
         *    data: [
         *        [0, 0],
         *        [1, 8],
         *        [2, 9]
         *    ]
         *    ```
         *
         * 3. An array of objects with named values. The following snippet shows only a
         *    few settings, see the complete options set below. If the total number of
         *    data points exceeds the series'
         *    [turboThreshold](#series.cylinder.turboThreshold), this option is not
         *    available.
         *
         *    ```js
         *    data: [{
         *        x: 1,
         *        y: 2,
         *        name: "Point2",
         *        color: "#00FF00"
         *    }, {
         *        x: 1,
         *        y: 4,
         *        name: "Point1",
         *        color: "#FF00FF"
         *    }]
         *    ```
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
         * @type      {Array<number|Array<(number|string),(number|null)>|null|*>}
         * @extends   series.column.data
         * @product   highcharts highstock
         * @apioption series.cylinder.data
         */
        ''; // keeps doclets above in the transpiled file

        return CylinderSeries;
    });
    _registerModule(_modules, 'masters/modules/cylinder.src.js', [], function () {


    });
}));