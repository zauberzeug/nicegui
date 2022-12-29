/**
 * @license Highcharts JS v10.3.2 (2022-11-28)
 *
 * (c) 2017-2021 Highsoft AS
 * Authors: Jon Arild Nygard
 *
 * License: www.highcharts.com/license
 */
(function (factory) {
    if (typeof module === 'object' && module.exports) {
        factory['default'] = factory;
        module.exports = factory;
    } else if (typeof define === 'function' && define.amd) {
        define('highcharts/modules/venn', ['highcharts'], function (Highcharts) {
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
    _registerModule(_modules, 'Core/Geometry/GeometryUtilities.js', [], function () {
        /* *
         *
         *  (c) 2010-2021 Highsoft AS
         *
         *  License: www.highcharts.com/license
         *
         *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
         *
         * */
        /* *
         *
         *  Namespace
         *
         * */
        var GeometryUtilities;
        (function (GeometryUtilities) {
            /* *
             *
             *  Functions
             *
             * */
            /**
             * Calculates the center between a list of points.
             *
             * @private
             *
             * @param {Array<Highcharts.PositionObject>} points
             * A list of points to calculate the center of.
             *
             * @return {Highcharts.PositionObject}
             * Calculated center
             */
            function getCenterOfPoints(points) {
                var sum = points.reduce(function (sum,
                    point) {
                        sum.x += point.x;
                    sum.y += point.y;
                    return sum;
                }, { x: 0, y: 0 });
                return {
                    x: sum.x / points.length,
                    y: sum.y / points.length
                };
            }
            GeometryUtilities.getCenterOfPoints = getCenterOfPoints;
            /**
             * Calculates the distance between two points based on their x and y
             * coordinates.
             *
             * @private
             *
             * @param {Highcharts.PositionObject} p1
             * The x and y coordinates of the first point.
             *
             * @param {Highcharts.PositionObject} p2
             * The x and y coordinates of the second point.
             *
             * @return {number}
             * Returns the distance between the points.
             */
            function getDistanceBetweenPoints(p1, p2) {
                return Math.sqrt(Math.pow(p2.x - p1.x, 2) + Math.pow(p2.y - p1.y, 2));
            }
            GeometryUtilities.getDistanceBetweenPoints = getDistanceBetweenPoints;
            /**
             * Calculates the angle between two points.
             * @todo add unit tests.
             * @private
             * @param {Highcharts.PositionObject} p1 The first point.
             * @param {Highcharts.PositionObject} p2 The second point.
             * @return {number} Returns the angle in radians.
             */
            function getAngleBetweenPoints(p1, p2) {
                return Math.atan2(p2.x - p1.x, p2.y - p1.y);
            }
            GeometryUtilities.getAngleBetweenPoints = getAngleBetweenPoints;
        })(GeometryUtilities || (GeometryUtilities = {}));
        /* *
         *
         *  Default Export
         *
         * */

        return GeometryUtilities;
    });
    _registerModule(_modules, 'Core/Geometry/CircleUtilities.js', [_modules['Core/Geometry/GeometryUtilities.js']], function (Geometry) {
        /* *
         *
         *  (c) 2010-2021 Highsoft AS
         *
         *  License: www.highcharts.com/license
         *
         *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
         *
         * */
        var getAngleBetweenPoints = Geometry.getAngleBetweenPoints,
            getCenterOfPoints = Geometry.getCenterOfPoints,
            getDistanceBetweenPoints = Geometry.getDistanceBetweenPoints;
        /* *
         *
         *  Namespace
         *
         * */
        var CircleUtilities;
        (function (CircleUtilities) {
            /* *
             *
             *  Functions
             *
             * */
            /**
             * @private
             *
             * @param {number} x
             * Number to round
             *
             * @param {number} decimals
             * Number of decimals to round to
             *
             * @return {number}
             * Rounded number
             */
            function round(x, decimals) {
                var a = Math.pow(10,
                    decimals);
                return Math.round(x * a) / a;
            }
            CircleUtilities.round = round;
            /**
             * Calculates the area of a circle based on its radius.
             *
             * @private
             *
             * @param {number} r
             * The radius of the circle.
             *
             * @return {number}
             * Returns the area of the circle.
             */
            function getAreaOfCircle(r) {
                if (r <= 0) {
                    throw new Error('radius of circle must be a positive number.');
                }
                return Math.PI * r * r;
            }
            CircleUtilities.getAreaOfCircle = getAreaOfCircle;
            /**
             * Calculates the area of a circular segment based on the radius of the
             * circle and the height of the segment.
             *
             * @see http://mathworld.wolfram.com/CircularSegment.html
             *
             * @private
             *
             * @param {number} r
             * The radius of the circle.
             *
             * @param {number} h
             * The height of the circular segment.
             *
             * @return {number}
             * Returns the area of the circular segment.
             */
            function getCircularSegmentArea(r, h) {
                return (r * r * Math.acos(1 - h / r) -
                    (r - h) * Math.sqrt(h * (2 * r - h)));
            }
            CircleUtilities.getCircularSegmentArea = getCircularSegmentArea;
            /**
             * Calculates the area of overlap between two circles based on their
             * radiuses and the distance between them.
             *
             * @see http://mathworld.wolfram.com/Circle-CircleIntersection.html
             *
             * @private
             *
             * @param {number} r1
             * Radius of the first circle.
             *
             * @param {number} r2
             * Radius of the second circle.
             *
             * @param {number} d
             * The distance between the two circles.
             *
             * @return {number}
             * Returns the area of overlap between the two circles.
             */
            function getOverlapBetweenCircles(r1, r2, d) {
                var overlap = 0;
                // If the distance is larger than the sum of the radiuses then the
                // circles does not overlap.
                if (d < r1 + r2) {
                    if (d <= Math.abs(r2 - r1)) {
                        // If the circles are completely overlapping, then the overlap
                        // equals the area of the smallest circle.
                        overlap = getAreaOfCircle(r1 < r2 ? r1 : r2);
                    }
                    else {
                        // Height of first triangle segment.
                        var d1 = (r1 * r1 - r2 * r2 + d * d) / (2 * d), 
                            // Height of second triangle segment.
                            d2 = d - d1;
                        overlap = (getCircularSegmentArea(r1, r1 - d1) +
                            getCircularSegmentArea(r2, r2 - d2));
                    }
                    // Round the result to two decimals.
                    overlap = round(overlap, 14);
                }
                return overlap;
            }
            CircleUtilities.getOverlapBetweenCircles = getOverlapBetweenCircles;
            /**
             * Calculates the intersection points of two circles.
             *
             * NOTE: does not handle floating errors well.
             *
             * @private
             *
             * @param {Highcharts.CircleObject} c1
             * The first circle.
             *
             * @param {Highcharts.CircleObject} c2
             * The second sircle.
             *
             * @return {Array<Highcharts.PositionObject>}
             * Returns the resulting intersection points.
             */
            function getCircleCircleIntersection(c1, c2) {
                var d = getDistanceBetweenPoints(c1,
                    c2),
                    r1 = c1.r,
                    r2 = c2.r;
                var points = [];
                if (d < r1 + r2 && d > Math.abs(r1 - r2)) {
                    // If the circles are overlapping, but not completely overlapping,
                    // then it exists intersecting points.
                    var r1Square = r1 * r1,
                        r2Square = r2 * r2, 
                        // d^2 - r^2 + R^2 / 2d
                        x = (r1Square - r2Square + d * d) / (2 * d), 
                        // y^2 = R^2 - x^2
                        y = Math.sqrt(r1Square - x * x),
                        x1 = c1.x,
                        x2 = c2.x,
                        y1 = c1.y,
                        y2 = c2.y,
                        x0 = x1 + x * (x2 - x1) / d,
                        y0 = y1 + x * (y2 - y1) / d,
                        rx = -(y2 - y1) * (y / d),
                        ry = -(x2 - x1) * (y / d);
                    points = [
                        { x: round(x0 + rx, 14), y: round(y0 - ry, 14) },
                        { x: round(x0 - rx, 14), y: round(y0 + ry, 14) }
                    ];
                }
                return points;
            }
            CircleUtilities.getCircleCircleIntersection = getCircleCircleIntersection;
            /**
             * Calculates all the intersection points for between a list of circles.
             *
             * @private
             *
             * @param {Array<Highcharts.CircleObject>} circles
             * The circles to calculate the points from.
             *
             * @return {Array<Highcharts.GeometryObject>}
             * Returns a list of intersection points.
             */
            function getCirclesIntersectionPoints(circles) {
                return circles.reduce(function (points, c1, i, arr) {
                    var additional = arr
                            .slice(i + 1)
                            .reduce(function (points,
                        c2,
                        j,
                        arr) {
                            var indexes = [i,
                        j + i + 1];
                        return points.concat(getCircleCircleIntersection(c1, c2).map(function (p) {
                            p.indexes = indexes;
                            return p;
                        }));
                    }, []);
                    return points.concat(additional);
                }, []);
            }
            CircleUtilities.getCirclesIntersectionPoints = getCirclesIntersectionPoints;
            /**
             * Tests whether the first circle is completely overlapping the second
             * circle.
             *
             * @private
             *
             * @param {Highcharts.CircleObject} circle1
             * The first circle.
             *
             * @param {Highcharts.CircleObject} circle2
             * The The second circle.
             *
             * @return {boolean}
             * Returns true if circle1 is completely overlapping circle2, false if not.
             */
            function isCircle1CompletelyOverlappingCircle2(circle1, circle2) {
                return getDistanceBetweenPoints(circle1, circle2) + circle2.r < circle1.r + 1e-10;
            }
            CircleUtilities.isCircle1CompletelyOverlappingCircle2 = isCircle1CompletelyOverlappingCircle2;
            /**
             * Tests whether a point lies within a given circle.
             * @private
             * @param {Highcharts.PositionObject} point
             * The point to test for.
             *
             * @param {Highcharts.CircleObject} circle
             * The circle to test if the point is within.
             *
             * @return {boolean}
             * Returns true if the point is inside, false if outside.
             */
            function isPointInsideCircle(point, circle) {
                return getDistanceBetweenPoints(point, circle) <= circle.r + 1e-10;
            }
            CircleUtilities.isPointInsideCircle = isPointInsideCircle;
            /**
             * Tests whether a point lies within a set of circles.
             *
             * @private
             *
             * @param {Highcharts.PositionObject} point
             * The point to test.
             *
             * @param {Array<Highcharts.CircleObject>} circles
             * The list of circles to test against.
             *
             * @return {boolean}
             * Returns true if the point is inside all the circles, false if not.
             */
            function isPointInsideAllCircles(point, circles) {
                return !circles.some(function (circle) {
                    return !isPointInsideCircle(point, circle);
                });
            }
            CircleUtilities.isPointInsideAllCircles = isPointInsideAllCircles;
            /**
             * Tests whether a point lies outside a set of circles.
             *
             * TODO: add unit tests.
             *
             * @private
             *
             * @param {Highcharts.PositionObject} point
             * The point to test.
             *
             * @param {Array<Highcharts.CircleObject>} circles
             * The list of circles to test against.
             *
             * @return {boolean}
             * Returns true if the point is outside all the circles, false if not.
             */
            function isPointOutsideAllCircles(point, circles) {
                return !circles.some(function (circle) {
                    return isPointInsideCircle(point, circle);
                });
            }
            CircleUtilities.isPointOutsideAllCircles = isPointOutsideAllCircles;
            /**
             * Calculates the points for the polygon of the intersection area between
             * a set of circles.
             *
             * @private
             *
             * @param {Array<Highcharts.CircleObject>} circles
             * List of circles to calculate polygon of.
             *
             * @return {Array<Highcharts.GeometryObject>}
             * Return list of points in the intersection polygon.
             */
            function getCirclesIntersectionPolygon(circles) {
                return getCirclesIntersectionPoints(circles)
                    .filter(function (p) {
                    return isPointInsideAllCircles(p, circles);
                });
            }
            CircleUtilities.getCirclesIntersectionPolygon = getCirclesIntersectionPolygon;
            /**
             * Calculate the path for the area of overlap between a set of circles.
             *
             * @todo handle cases with only 1 or 0 arcs.
             *
             * @private
             *
             * @param {Array<Highcharts.CircleObject>} circles
             * List of circles to calculate area of.
             *
             * @return {Highcharts.GeometryIntersectionObject|undefined}
             * Returns the path for the area of overlap. Returns an empty string if
             * there are no intersection between all the circles.
             */
            function getAreaOfIntersectionBetweenCircles(circles) {
                var intersectionPoints = getCirclesIntersectionPolygon(circles),
                    result;
                if (intersectionPoints.length > 1) {
                    // Calculate the center of the intersection points.
                    var center_1 = getCenterOfPoints(intersectionPoints);
                    intersectionPoints = intersectionPoints
                        // Calculate the angle between the center and the points.
                        .map(function (p) {
                        p.angle = getAngleBetweenPoints(center_1, p);
                        return p;
                    })
                        // Sort the points by the angle to the center.
                        .sort(function (a, b) {
                        return b.angle - a.angle;
                    });
                    var startPoint = intersectionPoints[intersectionPoints.length - 1];
                    var arcs = intersectionPoints
                            .reduce(function (data,
                        p1) {
                            var startPoint = data.startPoint,
                        midPoint = getCenterOfPoints([startPoint,
                        p1]);
                        // Calculate the arc from the intersection points and their
                        // circles.
                        var arc = p1.indexes
                                // Filter out circles that are not included in both
                                // intersection points.
                                .filter(function (index) {
                                return startPoint.indexes.indexOf(index) > -1;
                        })
                            // Iterate the circles of the intersection points and
                            // calculate arcs.
                            .reduce(function (arc, index) {
                            var circle = circles[index],
                                angle1 = getAngleBetweenPoints(circle,
                                p1),
                                angle2 = getAngleBetweenPoints(circle,
                                startPoint),
                                angleDiff = angle2 - angle1 +
                                    (angle2 < angle1 ? 2 * Math.PI : 0),
                                angle = angle2 - angleDiff / 2;
                            var width = getDistanceBetweenPoints(midPoint, {
                                    x: circle.x + circle.r * Math.sin(angle),
                                    y: circle.y + circle.r * Math.cos(angle)
                                });
                            var r = circle.r;
                            // Width can sometimes become to large due to
                            // floating point errors
                            if (width > r * 2) {
                                width = r * 2;
                            }
                            // Get the arc with the smallest width.
                            if (!arc || arc.width > width) {
                                arc = {
                                    r: r,
                                    largeArc: width > r ? 1 : 0,
                                    width: width,
                                    x: p1.x,
                                    y: p1.y
                                };
                            }
                            // Return the chosen arc.
                            return arc;
                        }, null);
                        // If we find an arc then add it to the list and update p2.
                        if (arc) {
                            var r = arc.r;
                            data.arcs.push(['A', r, r, 0, arc.largeArc, 1, arc.x, arc.y]);
                            data.startPoint = p1;
                        }
                        return data;
                    }, {
                        startPoint: startPoint,
                        arcs: []
                    }).arcs;
                    if (arcs.length === 0) {
                        // empty
                    }
                    else if (arcs.length === 1) {
                        // empty
                    }
                    else {
                        arcs.unshift(['M', startPoint.x, startPoint.y]);
                        result = {
                            center: center_1,
                            d: arcs
                        };
                    }
                }
                return result;
            }
            CircleUtilities.getAreaOfIntersectionBetweenCircles = getAreaOfIntersectionBetweenCircles;
        })(CircleUtilities || (CircleUtilities = {}));
        /* *
         *
         *  Default Export
         *
         * */

        return CircleUtilities;
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
    _registerModule(_modules, 'Series/Venn/VennPoint.js', [_modules['Core/Series/SeriesRegistry.js'], _modules['Core/Utilities.js']], function (SeriesRegistry, U) {
        /* *
         *
         *  Experimental Highcharts module which enables visualization of a Venn
         *  diagram.
         *
         *  (c) 2016-2021 Highsoft AS
         *  Authors: Jon Arild Nygard
         *
         *  Layout algorithm by Ben Frederickson:
         *  https://www.benfrederickson.com/better-venn-diagrams/
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
        var ScatterPoint = SeriesRegistry.seriesTypes.scatter.prototype.pointClass;
        var extend = U.extend,
            isNumber = U.isNumber;
        /* *
         *
         *  Class
         *
         * */
        var VennPoint = /** @class */ (function (_super) {
                __extends(VennPoint, _super);
            function VennPoint() {
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
                /* eslint-enable valid-jsdoc */
            }
            /* *
             *
             *  Functions
             *
             * */
            /* eslint-disable valid-jsdoc */
            VennPoint.prototype.isValid = function () {
                return isNumber(this.value);
            };
            VennPoint.prototype.shouldDraw = function () {
                // Only draw points with single sets.
                return !!this.shapeArgs;
            };
            return VennPoint;
        }(ScatterPoint));
        /* *
         *
         *  Default Export
         *
         * */

        return VennPoint;
    });
    _registerModule(_modules, 'Series/Venn/VennUtils.js', [_modules['Core/Geometry/CircleUtilities.js'], _modules['Core/Geometry/GeometryUtilities.js'], _modules['Core/Utilities.js']], function (CU, GU, U) {
        /* *
         *
         *  Experimental Highcharts module which enables visualization of a Venn
         *  diagram.
         *
         *  (c) 2016-2021 Highsoft AS
         *  Authors: Jon Arild Nygard
         *
         *  Layout algorithm by Ben Frederickson:
         *  https://www.benfrederickson.com/better-venn-diagrams/
         *
         *  License: www.highcharts.com/license
         *
         *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
         *
         * */
        var getAreaOfCircle = CU.getAreaOfCircle,
            getCircleCircleIntersection = CU.getCircleCircleIntersection,
            getOverlapBetweenCirclesByDistance = CU.getOverlapBetweenCircles,
            isPointInsideAllCircles = CU.isPointInsideAllCircles,
            isPointInsideCircle = CU.isPointInsideCircle,
            isPointOutsideAllCircles = CU.isPointOutsideAllCircles;
        var getDistanceBetweenPoints = GU.getDistanceBetweenPoints;
        var extend = U.extend,
            isArray = U.isArray,
            isNumber = U.isNumber,
            isObject = U.isObject,
            isString = U.isString;
        /* *
         *
         *  Functions
         *
         * */
        /* eslint-disable valid-jsdoc */
        /**
         * Takes an array of relations and adds the properties `totalOverlap` and
         * `overlapping` to each set. The property `totalOverlap` is the sum of
         * value for each relation where this set is included. The property
         * `overlapping` is a map of how much this set is overlapping another set.
         * NOTE: This algorithm ignores relations consisting of more than 2 sets.
         * @private
         * @param {Array<Highcharts.VennRelationObject>} relations
         * The list of relations that should be sorted.
         * @return {Array<Highcharts.VennRelationObject>}
         * Returns the modified input relations with added properties `totalOverlap`
         * and `overlapping`.
         */
        function addOverlapToSets(relations) {
            // Calculate the amount of overlap per set.
            var mapOfIdToProps = relations
                    // Filter out relations consisting of 2 sets.
                    .filter(function (relation) { return (relation.sets.length === 2); })
                    // Sum up the amount of overlap for each set.
                    .reduce(function (map,
                relation) {
                    relation.sets.forEach(function (set,
                i,
                arr) {
                        if (!isObject(map[set])) {
                            map[set] = {
                                overlapping: {},
                                totalOverlap: 0
                            };
                    }
                    map[set].totalOverlap += relation.value;
                    map[set].overlapping[arr[1 - i]] = relation.value;
                });
                return map;
            }, {});
            relations
                // Filter out single sets
                .filter(isSet)
                // Extend the set with the calculated properties.
                .forEach(function (set) {
                var properties = mapOfIdToProps[set.sets[0]];
                extend(set, properties);
            });
            // Returns the modified relations.
            return relations;
        }
        /**
         * Finds the root of a given function. The root is the input value needed
         * for a function to return 0.
         *
         * See https://en.wikipedia.org/wiki/Bisection_method#Algorithm
         *
         * TODO: Add unit tests.
         *
         * @param {Function} f
         * The function to find the root of.
         * @param {number} a
         * The lowest number in the search range.
         * @param {number} b
         * The highest number in the search range.
         * @param {number} [tolerance=1e-10]
         * The allowed difference between the returned value and root.
         * @param {number} [maxIterations=100]
         * The maximum iterations allowed.
         * @return {number}
         * Root number.
         */
        function bisect(f, a, b, tolerance, maxIterations) {
            var fA = f(a),
                fB = f(b),
                nMax = maxIterations || 100,
                tol = tolerance || 1e-10,
                delta = b - a,
                n = 1,
                x,
                fX;
            if (a >= b) {
                throw new Error('a must be smaller than b.');
            }
            else if (fA * fB > 0) {
                throw new Error('f(a) and f(b) must have opposite signs.');
            }
            if (fA === 0) {
                x = a;
            }
            else if (fB === 0) {
                x = b;
            }
            else {
                while (n++ <= nMax && fX !== 0 && delta > tol) {
                    delta = (b - a) / 2;
                    x = a + delta;
                    fX = f(x);
                    // Update low and high for next search interval.
                    if (fA * fX > 0) {
                        a = x;
                    }
                    else {
                        b = x;
                    }
                }
            }
            return x;
        }
        /**
         * @private
         */
        function getCentroid(simplex) {
            var arr = simplex.slice(0, -1),
                length = arr.length,
                result = [],
                sum = function (data,
                point) {
                    data.sum += point[data.i];
                return data;
            };
            for (var i = 0; i < length; i++) {
                result[i] = arr.reduce(sum, { sum: 0, i: i }).sum / length;
            }
            return result;
        }
        /**
         * Uses the bisection method to make a best guess of the ideal distance
         * between two circles too get the desired overlap.
         * Currently there is no known formula to calculate the distance from the
         * area of overlap, which makes the bisection method preferred.
         * @private
         * @param {number} r1
         * Radius of the first circle.
         * @param {number} r2
         * Radiues of the second circle.
         * @param {number} overlap
         * The wanted overlap between the two circles.
         * @return {number}
         * Returns the distance needed to get the wanted overlap between the two
         * circles.
         */
        function getDistanceBetweenCirclesByOverlap(r1, r2, overlap) {
            var maxDistance = r1 + r2,
                distance;
            if (overlap <= 0) {
                // If overlap is below or equal to zero, then there is no overlap.
                distance = maxDistance;
            }
            else if (getAreaOfCircle(r1 < r2 ? r1 : r2) <= overlap) {
                // When area of overlap is larger than the area of the smallest
                // circle, then it is completely overlapping.
                distance = 0;
            }
            else {
                distance = bisect(function (x) {
                    var actualOverlap = getOverlapBetweenCirclesByDistance(r1,
                        r2,
                        x);
                    // Return the differance between wanted and actual overlap.
                    return overlap - actualOverlap;
                }, 0, maxDistance);
            }
            return distance;
        }
        /**
         * Finds the available width for a label, by taking the label position and
         * finding the largest distance, which is inside all internal circles, and
         * outside all external circles.
         *
         * @private
         * @param {Highcharts.PositionObject} pos
         * The x and y coordinate of the label.
         * @param {Array<Highcharts.CircleObject>} internal
         * Internal circles.
         * @param {Array<Highcharts.CircleObject>} external
         * External circles.
         * @return {number}
         * Returns available width for the label.
         */
        function getLabelWidth(pos, internal, external) {
            var radius = internal.reduce(function (min,
                circle) { return Math.min(circle.r,
                min); },
                Infinity), 
                // Filter out external circles that are completely overlapping.
                filteredExternals = external.filter(function (circle) {
                    return !isPointInsideCircle(pos,
                circle);
            });
            var findDistance = function (maxDistance,
                direction) {
                    return bisect(function (x) {
                        var testPos = {
                            x: pos.x + (direction * x),
                            y: pos.y
                        },
                isValid = (isPointInsideAllCircles(testPos,
                internal) &&
                            isPointOutsideAllCircles(testPos,
                filteredExternals));
                    // If the position is valid, then we want to move towards the
                    // max distance. If not, then we want to  away from the max
                    // distance.
                    return -(maxDistance - x) + (isValid ? 0 : Number.MAX_VALUE);
                }, 0, maxDistance);
            };
            // Find the smallest distance of left and right.
            return Math.min(findDistance(radius, -1), findDistance(radius, 1)) * 2;
        }
        /**
         * Calculates a margin for a point based on the iternal and external
         * circles. The margin describes if the point is well placed within the
         * internal circles, and away from the external.
         * @private
         * @todo add unit tests.
         * @param {Highcharts.PositionObject} point
         * The point to evaluate.
         * @param {Array<Highcharts.CircleObject>} internal
         * The internal circles.
         * @param {Array<Highcharts.CircleObject>} external
         * The external circles.
         * @return {number}
         * Returns the margin.
         */
        function getMarginFromCircles(point, internal, external) {
            var margin = internal.reduce(function (margin,
                circle) {
                    var m = circle.r - getDistanceBetweenPoints(point,
                circle);
                return (m <= margin) ? m : margin;
            }, Number.MAX_VALUE);
            margin = external.reduce(function (margin, circle) {
                var m = getDistanceBetweenPoints(point,
                    circle) - circle.r;
                return (m <= margin) ? m : margin;
            }, margin);
            return margin;
        }
        /**
         * Calculates the area of overlap between a list of circles.
         * @private
         * @todo add support for calculating overlap between more than 2 circles.
         * @param {Array<Highcharts.CircleObject>} circles
         * List of circles with their given positions.
         * @return {number}
         * Returns the area of overlap between all the circles.
         */
        function getOverlapBetweenCircles(circles) {
            var overlap = 0;
            // When there is only two circles we can find the overlap by using their
            // radiuses and the distance between them.
            if (circles.length === 2) {
                var circle1 = circles[0];
                var circle2 = circles[1];
                overlap = getOverlapBetweenCirclesByDistance(circle1.r, circle2.r, getDistanceBetweenPoints(circle1, circle2));
            }
            return overlap;
        }
        // eslint-disable-next-line require-jsdoc
        function isSet(x) {
            return isArray(x.sets) && x.sets.length === 1;
        }
        // eslint-disable-next-line require-jsdoc
        function isValidRelation(x) {
            var map = {};
            return (isObject(x) &&
                (isNumber(x.value) && x.value > -1) &&
                (isArray(x.sets) && x.sets.length > 0) &&
                !x.sets.some(function (set) {
                    var invalid = false;
                    if (!map[set] && isString(set)) {
                        map[set] = true;
                    }
                    else {
                        invalid = true;
                    }
                    return invalid;
                }));
        }
        // eslint-disable-next-line require-jsdoc
        function isValidSet(x) {
            return (isValidRelation(x) && isSet(x) && x.value > 0);
        }
        /**
         * Uses a greedy approach to position all the sets. Works well with a small
         * number of sets, and are in these cases a good choice aesthetically.
         * @private
         * @param {Array<object>} relations List of the overlap between two or more
         * sets, or the size of a single set.
         * @return {Array<object>} List of circles and their calculated positions.
         */
        function layoutGreedyVenn(relations) {
            var positionedSets = [],
                mapOfIdToCircles = {};
            // Define a circle for each set.
            relations
                .filter(function (relation) {
                return relation.sets.length === 1;
            }).forEach(function (relation) {
                mapOfIdToCircles[relation.sets[0]] = relation.circle = {
                    x: Number.MAX_VALUE,
                    y: Number.MAX_VALUE,
                    r: Math.sqrt(relation.value / Math.PI)
                };
            });
            /**
             * Takes a set and updates the position, and add the set to the list of
             * positioned sets.
             * @private
             * @param {Object} set
             * The set to add to its final position.
             * @param {Object} coordinates
             * The coordinates to position the set at.
             */
            var positionSet = function positionSet(set,
                coordinates) {
                    var circle = set.circle;
                circle.x = coordinates.x;
                circle.y = coordinates.y;
                positionedSets.push(set);
            };
            // Find overlap between sets. Ignore relations with more then 2 sets.
            addOverlapToSets(relations);
            // Sort sets by the sum of their size from large to small.
            var sortedByOverlap = relations
                    .filter(isSet)
                    .sort(sortByTotalOverlap);
            // Position the most overlapped set at 0,0.
            positionSet(sortedByOverlap.shift(), { x: 0, y: 0 });
            var relationsWithTwoSets = relations.filter(function (x) {
                    return x.sets.length === 2;
            });
            // Iterate and position the remaining sets.
            sortedByOverlap.forEach(function (set) {
                var circle = set.circle,
                    radius = circle.r,
                    overlapping = set.overlapping;
                var bestPosition = positionedSets.reduce(function (best,
                    positionedSet,
                    i) {
                        var positionedCircle = positionedSet.circle,
                    overlap = overlapping[positionedSet.sets[0]];
                    // Calculate the distance between the sets to get the
                    // correct overlap
                    var distance = getDistanceBetweenCirclesByOverlap(radius,
                        positionedCircle.r,
                        overlap);
                    // Create a list of possible coordinates calculated from
                    // distance.
                    var possibleCoordinates = [
                            { x: positionedCircle.x + distance,
                        y: positionedCircle.y },
                            { x: positionedCircle.x - distance,
                        y: positionedCircle.y },
                            { x: positionedCircle.x,
                        y: positionedCircle.y + distance },
                            { x: positionedCircle.x,
                        y: positionedCircle.y - distance }
                        ];
                    // If there are more circles overlapping, then add the
                    // intersection points as possible positions.
                    positionedSets.slice(i + 1).forEach(function (positionedSet2) {
                        var positionedCircle2 = positionedSet2.circle,
                            overlap2 = overlapping[positionedSet2.sets[0]],
                            distance2 = getDistanceBetweenCirclesByOverlap(radius,
                            positionedCircle2.r,
                            overlap2);
                        // Add intersections to list of coordinates.
                        possibleCoordinates = possibleCoordinates.concat(getCircleCircleIntersection({
                            x: positionedCircle.x,
                            y: positionedCircle.y,
                            r: distance
                        }, {
                            x: positionedCircle2.x,
                            y: positionedCircle2.y,
                            r: distance2
                        }));
                    });
                    // Iterate all suggested coordinates and find the best one.
                    possibleCoordinates.forEach(function (coordinates) {
                        circle.x = coordinates.x;
                        circle.y = coordinates.y;
                        // Calculate loss for the suggested coordinates.
                        var currentLoss = loss(mapOfIdToCircles,
                            relationsWithTwoSets);
                        // If the loss is better, then use these new coordinates
                        if (currentLoss < best.loss) {
                            best.loss = currentLoss;
                            best.coordinates = coordinates;
                        }
                    });
                    // Return resulting coordinates.
                    return best;
                }, {
                    loss: Number.MAX_VALUE,
                    coordinates: void 0
                });
                // Add the set to its final position.
                positionSet(set, bestPosition.coordinates);
            });
            // Return the positions of each set.
            return mapOfIdToCircles;
        }
        /**
         * Calculates the difference between the desired overlap and the actual
         * overlap between two circles.
         * @private
         * @param {Dictionary<Highcharts.CircleObject>} mapOfIdToCircle
         * Map from id to circle.
         * @param {Array<Highcharts.VennRelationObject>} relations
         * List of relations to calculate the loss of.
         * @return {number}
         * Returns the loss between positions of the circles for the given
         * relations.
         */
        function loss(mapOfIdToCircle, relations) {
            var precision = 10e10;
            // Iterate all the relations and calculate their individual loss.
            return relations.reduce(function (totalLoss, relation) {
                var loss = 0;
                if (relation.sets.length > 1) {
                    var wantedOverlap = relation.value;
                    // Calculate the actual overlap between the sets.
                    var actualOverlap = getOverlapBetweenCircles(
                        // Get the circles for the given sets.
                        relation.sets.map(function (set) {
                            return mapOfIdToCircle[set];
                    }));
                    var diff = wantedOverlap - actualOverlap;
                    loss = Math.round((diff * diff) * precision) / precision;
                }
                // Add calculated loss to the sum.
                return totalLoss + loss;
            }, 0);
        }
        /**
         * Finds an optimal position for a given point.
         * @todo add unit tests.
         * @todo add constraints to optimize the algorithm.
         * @private
         * @param {Highcharts.NelderMeadTestFunction} fn
         *        The function to test a point.
         * @param {Highcharts.NelderMeadPointArray} initial
         *        The initial point to optimize.
         * @return {Highcharts.NelderMeadPointArray}
         *         Returns the opimized position of a point.
         */
        function nelderMead(fn, initial) {
            var maxIterations = 100,
                sortByFx = function (a,
                b) {
                    return a.fx - b.fx;
            }, pRef = 1, // Reflection parameter
            pExp = 2, // Expansion parameter
            pCon = -0.5, // Contraction parameter
            pOCon = pCon * pRef, // Outwards contraction parameter
            pShrink = 0.5; // Shrink parameter
            /**
             * @private
             */
            var weightedSum = function (weight1,
                v1,
                weight2,
                v2) { return v1.map(function (x,
                i) { return weight1 * x + weight2 * v2[i]; }); };
            /**
             * @private
             */
            var getSimplex = function (initial) {
                    var n = initial.length,
                simplex = new Array(n + 1);
                // Initial point to the simplex.
                simplex[0] = initial;
                simplex[0].fx = fn(initial);
                // Create a set of extra points based on the initial.
                for (var i = 0; i < n; ++i) {
                    var point = initial.slice();
                    point[i] = point[i] ? point[i] * 1.05 : 0.001;
                    point.fx = fn(point);
                    simplex[i + 1] = point;
                }
                return simplex;
            };
            var updateSimplex = function (simplex,
                point) {
                    point.fx = fn(point);
                simplex[simplex.length - 1] = point;
                return simplex;
            };
            var shrinkSimplex = function (simplex) {
                    var best = simplex[0];
                return simplex.map(function (point) {
                    var p = weightedSum(1 - pShrink,
                        best,
                        pShrink,
                        point);
                    p.fx = fn(p);
                    return p;
                });
            };
            var getPoint = function (centroid,
                worst,
                a,
                b) {
                    var point = weightedSum(a,
                centroid,
                b,
                worst);
                point.fx = fn(point);
                return point;
            };
            // Create a simplex
            var simplex = getSimplex(initial);
            // Iterate from 0 to max iterations
            for (var i = 0; i < maxIterations; i++) {
                // Sort the simplex
                simplex.sort(sortByFx);
                // Create a centroid from the simplex
                var worst = simplex[simplex.length - 1];
                var centroid = getCentroid(simplex);
                // Calculate the reflected point.
                var reflected = getPoint(centroid,
                    worst, 1 + pRef, -pRef);
                if (reflected.fx < simplex[0].fx) {
                    // If reflected point is the best, then possibly expand.
                    var expanded = getPoint(centroid,
                        worst, 1 + pExp, -pExp);
                    simplex = updateSimplex(simplex, (expanded.fx < reflected.fx) ? expanded : reflected);
                }
                else if (reflected.fx >= simplex[simplex.length - 2].fx) {
                    // If the reflected point is worse than the second worse, then
                    // contract.
                    var contracted = void 0;
                    if (reflected.fx > worst.fx) {
                        // If the reflected is worse than the worst point, do a
                        // contraction
                        contracted = getPoint(centroid, worst, 1 + pCon, -pCon);
                        if (contracted.fx < worst.fx) {
                            simplex = updateSimplex(simplex, contracted);
                        }
                        else {
                            simplex = shrinkSimplex(simplex);
                        }
                    }
                    else {
                        // Otherwise do an outwards contraction
                        contracted = getPoint(centroid, worst, 1 - pOCon, pOCon);
                        if (contracted.fx < reflected.fx) {
                            simplex = updateSimplex(simplex, contracted);
                        }
                        else {
                            simplex = shrinkSimplex(simplex);
                        }
                    }
                }
                else {
                    simplex = updateSimplex(simplex, reflected);
                }
            }
            return simplex[0];
        }
        /**
         * Prepares the venn data so that it is usable for the layout function.
         * Filter out sets, or intersections that includes sets, that are missing in
         * the data or has (value < 1). Adds missing relations between sets in the
         * data as value = 0.
         * @private
         * @param {Array<object>} data The raw input data.
         * @return {Array<object>} Returns an array of valid venn data.
         */
        function processVennData(data) {
            var d = isArray(data) ? data : [];
            var validSets = d
                    .reduce(function (arr,
                x) {
                    // Check if x is a valid set, and that it is not an duplicate.
                    if (isValidSet(x) && arr.indexOf(x.sets[0]) === -1) {
                        arr.push(x.sets[0]);
                }
                return arr;
            }, [])
                .sort();
            var mapOfIdToRelation = d.reduce(function (mapOfIdToRelation,
                relation) {
                    if (isValidRelation(relation) &&
                        !relation.sets.some(function (set) {
                            return validSets.indexOf(set) === -1;
                    })) {
                    mapOfIdToRelation[relation.sets.sort().join()] =
                        relation;
                }
                return mapOfIdToRelation;
            }, {});
            validSets.reduce(function (combinations, set, i, arr) {
                var remaining = arr.slice(i + 1);
                remaining.forEach(function (set2) {
                    combinations.push(set + ',' + set2);
                });
                return combinations;
            }, []).forEach(function (combination) {
                if (!mapOfIdToRelation[combination]) {
                    var obj = {
                            sets: combination.split(','),
                            value: 0
                        };
                    mapOfIdToRelation[combination] = obj;
                }
            });
            // Transform map into array.
            return Object
                .keys(mapOfIdToRelation)
                .map(function (id) {
                return mapOfIdToRelation[id];
            });
        }
        /**
         * Takes two sets and finds the one with the largest total overlap.
         * @private
         * @param {Object} a
         * The first set to compare.
         * @param {Object} b
         * The second set to compare.
         * @return {number}
         * Returns 0 if a and b are equal, <0 if a is greater, >0 if b is greater.
         */
        function sortByTotalOverlap(a, b) {
            return b.totalOverlap - a.totalOverlap;
        }
        /* *
         *
         *  Default Export
         *
         * */
        var VennUtils = {
                geometry: GU,
                geometryCircles: CU,
                addOverlapToSets: addOverlapToSets,
                getCentroid: getCentroid,
                getDistanceBetweenCirclesByOverlap: getDistanceBetweenCirclesByOverlap,
                getLabelWidth: getLabelWidth,
                getMarginFromCircles: getMarginFromCircles,
                isSet: isSet,
                layoutGreedyVenn: layoutGreedyVenn,
                loss: loss,
                nelderMead: nelderMead,
                processVennData: processVennData,
                sortByTotalOverlap: sortByTotalOverlap
            };

        return VennUtils;
    });
    _registerModule(_modules, 'Series/Venn/VennSeries.js', [_modules['Core/Animation/AnimationUtilities.js'], _modules['Core/Color/Color.js'], _modules['Core/Geometry/CircleUtilities.js'], _modules['Series/DrawPointUtilities.js'], _modules['Core/Geometry/GeometryUtilities.js'], _modules['Core/Series/SeriesRegistry.js'], _modules['Series/Venn/VennPoint.js'], _modules['Series/Venn/VennUtils.js'], _modules['Core/Legend/LegendSymbol.js'], _modules['Core/Utilities.js']], function (A, Color, CU, DPU, GU, SeriesRegistry, VennPoint, VennUtils, LegendSymbol, U) {
        /* *
         *
         *  Experimental Highcharts module which enables visualization of a Venn
         *  diagram.
         *
         *  (c) 2016-2021 Highsoft AS
         *  Authors: Jon Arild Nygard
         *
         *  Layout algorithm by Ben Frederickson:
         *  https://www.benfrederickson.com/better-venn-diagrams/
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
        var color = Color.parse;
        var getAreaOfIntersectionBetweenCircles = CU.getAreaOfIntersectionBetweenCircles,
            getCirclesIntersectionPolygon = CU.getCirclesIntersectionPolygon,
            isCircle1CompletelyOverlappingCircle2 = CU.isCircle1CompletelyOverlappingCircle2,
            isPointInsideAllCircles = CU.isPointInsideAllCircles,
            isPointOutsideAllCircles = CU.isPointOutsideAllCircles;
        var getCenterOfPoints = GU.getCenterOfPoints;
        var ScatterSeries = SeriesRegistry.seriesTypes.scatter;
        var addEvent = U.addEvent,
            extend = U.extend,
            isArray = U.isArray,
            isNumber = U.isNumber,
            isObject = U.isObject,
            isString = U.isString,
            merge = U.merge;
        /* *
         *
         *  Class
         *
         * */
        /**
         * @private
         * @class
         * @name Highcharts.seriesTypes.venn
         *
         * @augments Highcharts.Series
         */
        var VennSeries = /** @class */ (function (_super) {
                __extends(VennSeries, _super);
            function VennSeries() {
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
                _this.mapOfIdToRelation = void 0;
                _this.options = void 0;
                _this.points = void 0;
                return _this;
                /* eslint-enable valid-jsdoc */
            }
            /* *
             *
             *  Static Functions
             *
             * */
            /**
             * Finds the optimal label position by looking for a position that has a low
             * distance from the internal circles, and as large possible distane to the
             * external circles.
             * @private
             * @todo Optimize the intial position.
             * @todo Add unit tests.
             * @param {Array<Highcharts.CircleObject>} internal
             * Internal circles.
             * @param {Array<Highcharts.CircleObject>} external
             * External circles.
             * @return {Highcharts.PositionObject}
             * Returns the found position.
             */
            VennSeries.getLabelPosition = function (internal, external) {
                // Get the best label position within the internal circles.
                var best = internal.reduce(function (best,
                    circle) {
                        var d = circle.r / 2;
                    // Give a set of points with the circle to evaluate as the best
                    // label position.
                    return [
                        { x: circle.x, y: circle.y },
                        { x: circle.x + d, y: circle.y },
                        { x: circle.x - d, y: circle.y },
                        { x: circle.x, y: circle.y + d },
                        { x: circle.x, y: circle.y - d }
                    ]
                        // Iterate the given points and return the one with the
                        // largest margin.
                        .reduce(function (best, point) {
                        var margin = VennUtils.getMarginFromCircles(point,
                            internal,
                            external);
                        // If the margin better than the current best, then
                        // update sbest.
                        if (best.margin < margin) {
                            best.point = point;
                            best.margin = margin;
                        }
                        return best;
                    }, best);
                }, {
                    point: void 0,
                    margin: -Number.MAX_VALUE
                }).point;
                // Use nelder mead to optimize the initial label position.
                var optimal = VennUtils.nelderMead(function (p) {
                        return -(VennUtils.getMarginFromCircles({ x: p[0],
                    y: p[1] },
                    internal,
                    external));
                }, [best.x, best.y]);
                // Update best to be the point which was found to have the best margin.
                best = {
                    x: optimal[0],
                    y: optimal[1]
                };
                if (!(isPointInsideAllCircles(best, internal) &&
                    isPointOutsideAllCircles(best, external))) {
                    // If point was either outside one of the internal, or inside one of
                    // the external, then it was invalid and should use a fallback.
                    if (internal.length > 1) {
                        best = getCenterOfPoints(getCirclesIntersectionPolygon(internal));
                    }
                    else {
                        best = {
                            x: internal[0].x,
                            y: internal[0].y
                        };
                    }
                }
                // Return the best point.
                return best;
            };
            /**
             * Calulates data label values for a given relations object.
             *
             * @private
             * @todo add unit tests
             * @param {Highcharts.VennRelationObject} relation A relations object.
             * @param {Array<Highcharts.VennRelationObject>} setRelations The list of
             * relations that is a set.
             * @return {Highcharts.VennLabelValuesObject}
             * Returns an object containing position and width of the label.
             */
            VennSeries.getLabelValues = function (relation, setRelations) {
                var sets = relation.sets;
                // Create a list of internal and external circles.
                var data = setRelations.reduce(function (data,
                    set) {
                        // If the set exists in this relation, then it is internal,
                        // otherwise it will be external.
                        var isInternal = sets.indexOf(set.sets[0]) > -1;
                    var property = isInternal ? 'internal' : 'external';
                    // Add the circle to the list.
                    data[property].push(set.circle);
                    return data;
                }, {
                    internal: [],
                    external: []
                });
                // Filter out external circles that are completely overlapping all
                // internal
                data.external = data.external.filter(function (externalCircle) {
                    return data.internal.some(function (internalCircle) {
                        return !isCircle1CompletelyOverlappingCircle2(externalCircle, internalCircle);
                    });
                });
                // Calulate the label position.
                var position = VennSeries.getLabelPosition(data.internal,
                    data.external);
                // Calculate the label width
                var width = VennUtils.getLabelWidth(position,
                    data.internal,
                    data.external);
                return {
                    position: position,
                    width: width
                };
            };
            /**
             * Calculates the positions, and the label values of all the sets in the
             * venn diagram.
             *
             * @private
             * @todo Add support for constrained MDS.
             * @param {Array<Highchats.VennRelationObject>} relations
             * List of the overlap between two or more sets, or the size of a single
             * sset.
             * @return {Highcharts.Dictionary<*>}
             * List of circles and their calculated positions.
             */
            VennSeries.layout = function (relations) {
                var mapOfIdToShape = {};
                var mapOfIdToLabelValues = {};
                // Calculate best initial positions by using greedy layout.
                if (relations.length > 0) {
                    var mapOfIdToCircles_1 = VennUtils.layoutGreedyVenn(relations);
                    var setRelations_1 = relations.filter(VennUtils.isSet);
                    relations.forEach(function (relation) {
                        var sets = relation.sets;
                        var id = sets.join();
                        // Get shape from map of circles, or calculate intersection.
                        var shape = VennUtils.isSet(relation) ?
                                mapOfIdToCircles_1[id] :
                                getAreaOfIntersectionBetweenCircles(sets.map(function (set) { return mapOfIdToCircles_1[set]; }));
                        // Calculate label values if the set has a shape
                        if (shape) {
                            mapOfIdToShape[id] = shape;
                            mapOfIdToLabelValues[id] = VennSeries.getLabelValues(relation, setRelations_1);
                        }
                    });
                }
                return { mapOfIdToShape: mapOfIdToShape, mapOfIdToLabelValues: mapOfIdToLabelValues };
            };
            /**
             * Calculates the proper scale to fit the cloud inside the plotting area.
             * @private
             * @todo add unit test
             * @param {number} targetWidth
             * Width of target area.
             * @param {number} targetHeight
             * Height of target area.
             * @param {Highcharts.PolygonBoxObject} field
             * The playing field.
             * @return {Highcharts.Dictionary<number>}
             * Returns the value to scale the playing field up to the size of the target
             * area, and center of x and y.
             */
            VennSeries.getScale = function (targetWidth, targetHeight, field) {
                var height = field.bottom - field.top, // top is smaller than bottom
                    width = field.right - field.left,
                    scaleX = width > 0 ? 1 / width * targetWidth : 1,
                    scaleY = height > 0 ? 1 / height * targetHeight : 1,
                    adjustX = (field.right + field.left) / 2,
                    adjustY = (field.top + field.bottom) / 2,
                    scale = Math.min(scaleX,
                    scaleY);
                return {
                    scale: scale,
                    centerX: targetWidth / 2 - adjustX * scale,
                    centerY: targetHeight / 2 - adjustY * scale
                };
            };
            /**
             * If a circle is outside a give field, then the boundaries of the field is
             * adjusted accordingly. Modifies the field object which is passed as the
             * first parameter.
             * @private
             * @todo NOTE: Copied from wordcloud, can probably be unified.
             * @param {Highcharts.PolygonBoxObject} field
             * The bounding box of a playing field.
             * @param {Highcharts.CircleObject} circle
             * The bounding box for a placed point.
             * @return {Highcharts.PolygonBoxObject}
             * Returns a modified field object.
             */
            VennSeries.updateFieldBoundaries = function (field, circle) {
                var left = circle.x - circle.r,
                    right = circle.x + circle.r,
                    bottom = circle.y + circle.r,
                    top = circle.y - circle.r;
                // TODO improve type checking.
                if (!isNumber(field.left) || field.left > left) {
                    field.left = left;
                }
                if (!isNumber(field.right) || field.right < right) {
                    field.right = right;
                }
                if (!isNumber(field.top) || field.top > top) {
                    field.top = top;
                }
                if (!isNumber(field.bottom) || field.bottom < bottom) {
                    field.bottom = bottom;
                }
                return field;
            };
            /* *
             *
             *  Functions
             *
             * */
            /* eslint-disable valid-jsdoc */
            VennSeries.prototype.animate = function (init) {
                if (!init) {
                    var series = this,
                        animOptions_1 = animObject(series.options.animation);
                    series.points.forEach(function (point) {
                        var args = point.shapeArgs;
                        if (point.graphic && args) {
                            var attr = {},
                                animate = {};
                            if (args.d) {
                                // If shape is a path, then animate opacity.
                                attr.opacity = 0.001;
                            }
                            else {
                                // If shape is a circle, then animate radius.
                                attr.r = 0;
                                animate.r = args.r;
                            }
                            point.graphic
                                .attr(attr)
                                .animate(animate, animOptions_1);
                            // If shape is path, then fade it in after the circles
                            // animation
                            if (args.d) {
                                setTimeout(function () {
                                    if (point && point.graphic) {
                                        point.graphic.animate({
                                            opacity: 1
                                        });
                                    }
                                }, animOptions_1.duration);
                            }
                        }
                    }, series);
                }
            };
            /**
             * Draw the graphics for each point.
             * @private
             */
            VennSeries.prototype.drawPoints = function () {
                var series = this, 
                    // Series properties
                    chart = series.chart,
                    group = series.group,
                    points = series.points || [], 
                    // Chart properties
                    renderer = chart.renderer;
                // Iterate all points and calculate and draw their graphics.
                points.forEach(function (point) {
                    var attribs = {
                            zIndex: isArray(point.sets) ? point.sets.length : 0
                        },
                        shapeArgs = point.shapeArgs;
                    // Add point attribs
                    if (!chart.styledMode) {
                        extend(attribs, series.pointAttribs(point, point.state));
                    }
                    // Draw the point graphic.
                    DPU.draw(point, {
                        isNew: !point.graphic,
                        animatableAttribs: shapeArgs,
                        attribs: attribs,
                        group: group,
                        renderer: renderer,
                        shapeType: shapeArgs && shapeArgs.d ? 'path' : 'circle'
                    });
                });
            };
            VennSeries.prototype.init = function () {
                ScatterSeries.prototype.init.apply(this, arguments);
                // Venn's opacity is a different option from other series
                delete this.opacity;
            };
            /**
             * Calculates the style attributes for a point. The attributes can vary
             * depending on the state of the point.
             * @private
             * @param {Highcharts.Point} point
             * The point which will get the resulting attributes.
             * @param {string} [state]
             * The state of the point.
             * @return {Highcharts.SVGAttributes}
             * Returns the calculated attributes.
             */
            VennSeries.prototype.pointAttribs = function (point, state) {
                var series = this,
                    seriesOptions = series.options || {},
                    pointOptions = point && point.options || {},
                    stateOptions = (state && seriesOptions.states[state]) || {},
                    options = merge(seriesOptions, { color: point && point.color },
                    pointOptions,
                    stateOptions);
                // Return resulting values for the attributes.
                return {
                    'fill': color(options.color)
                        .brighten(options.brightness)
                        .get(),
                    // Set opacity directly to the SVG element, not to pattern #14372.
                    opacity: options.opacity,
                    'stroke': options.borderColor,
                    'stroke-width': options.borderWidth,
                    'dashstyle': options.borderDashStyle
                };
            };
            VennSeries.prototype.translate = function () {
                var chart = this.chart;
                this.processedXData = this.xData;
                this.generatePoints();
                // Process the data before passing it into the layout function.
                var relations = VennUtils.processVennData(this.options.data);
                // Calculate the positions of each circle.
                var _a = VennSeries.layout(relations),
                    mapOfIdToShape = _a.mapOfIdToShape,
                    mapOfIdToLabelValues = _a.mapOfIdToLabelValues;
                // Calculate the scale, and center of the plot area.
                var field = Object.keys(mapOfIdToShape)
                        .filter(function (key) {
                        var shape = mapOfIdToShape[key];
                    return shape && isNumber(shape.r);
                })
                    .reduce(function (field, key) {
                    return VennSeries.updateFieldBoundaries(field, mapOfIdToShape[key]);
                }, { top: 0, bottom: 0, left: 0, right: 0 }), scaling = VennSeries.getScale(chart.plotWidth, chart.plotHeight, field), scale = scaling.scale, centerX = scaling.centerX, centerY = scaling.centerY;
                // Iterate all points and calculate and draw their graphics.
                this.points.forEach(function (point) {
                    var sets = isArray(point.sets) ? point.sets : [],
                        id = sets.join(),
                        shape = mapOfIdToShape[id],
                        shapeArgs,
                        dataLabelValues = mapOfIdToLabelValues[id] || {},
                        dataLabelWidth = dataLabelValues.width,
                        dataLabelPosition = dataLabelValues.position,
                        dlOptions = point.options && point.options.dataLabels;
                    if (shape) {
                        if (shape.r) {
                            shapeArgs = {
                                x: centerX + shape.x * scale,
                                y: centerY + shape.y * scale,
                                r: shape.r * scale
                            };
                        }
                        else if (shape.d) {
                            var d = shape.d;
                            d.forEach(function (seg) {
                                if (seg[0] === 'M') {
                                    seg[1] = centerX + seg[1] * scale;
                                    seg[2] = centerY + seg[2] * scale;
                                }
                                else if (seg[0] === 'A') {
                                    seg[1] = seg[1] * scale;
                                    seg[2] = seg[2] * scale;
                                    seg[6] = centerX + seg[6] * scale;
                                    seg[7] = centerY + seg[7] * scale;
                                }
                            });
                            shapeArgs = { d: d };
                        }
                        // Scale the position for the data label.
                        if (dataLabelPosition) {
                            dataLabelPosition.x = centerX + dataLabelPosition.x * scale;
                            dataLabelPosition.y = centerY + dataLabelPosition.y * scale;
                        }
                        else {
                            dataLabelPosition = {};
                        }
                        if (isNumber(dataLabelWidth)) {
                            dataLabelWidth = Math.round(dataLabelWidth * scale);
                        }
                    }
                    point.shapeArgs = shapeArgs;
                    // Placement for the data labels
                    if (dataLabelPosition && shapeArgs) {
                        point.plotX = dataLabelPosition.x;
                        point.plotY = dataLabelPosition.y;
                    }
                    // Add width for the data label
                    if (dataLabelWidth && shapeArgs) {
                        point.dlOptions = merge(true, {
                            style: {
                                width: dataLabelWidth
                            }
                        }, isObject(dlOptions, true) ? dlOptions : void 0);
                    }
                    // Set name for usage in tooltip and in data label.
                    point.name = point.options.name || sets.join('∩');
                });
            };
            /**
             * A Venn diagram displays all possible logical relations between a
             * collection of different sets. The sets are represented by circles, and
             * the relation between the sets are displayed by the overlap or lack of
             * overlap between them. The venn diagram is a special case of Euler
             * diagrams, which can also be displayed by this series type.
             *
             * @sample {highcharts} highcharts/demo/venn-diagram/
             *         Venn diagram
             * @sample {highcharts} highcharts/demo/euler-diagram/
             *         Euler diagram
             * @sample {highcharts} highcharts/series-venn/point-legend/
             *         Venn diagram with a legend
             *
             * @extends      plotOptions.scatter
             * @excluding    connectEnds, connectNulls, cropThreshold, dragDrop,
             *               findNearestPointBy, getExtremesFromAll, jitter, label,
             *               linecap, lineWidth, linkedTo, marker, negativeColor,
             *               pointInterval, pointIntervalUnit, pointPlacement,
             *               pointStart, softThreshold, stacking, steps, threshold,
             *               xAxis, yAxis, zoneAxis, zones, dataSorting, boostThreshold,
             *               boostBlending
             * @product      highcharts
             * @requires     modules/venn
             * @optionparent plotOptions.venn
             */
            VennSeries.defaultOptions = merge(ScatterSeries.defaultOptions, {
                borderColor: "#cccccc" /* Palette.neutralColor20 */,
                borderDashStyle: 'solid',
                borderWidth: 1,
                brighten: 0,
                clip: false,
                colorByPoint: true,
                dataLabels: {
                    enabled: true,
                    verticalAlign: 'middle',
                    formatter: function () {
                        return this.point.name;
                    }
                },
                /**
                 * @ignore-option
                 * @private
                 */
                inactiveOtherPoints: true,
                /**
                 * @ignore-option
                 * @private
                 */
                marker: false,
                opacity: 0.75,
                showInLegend: false,
                /**
                 * @ignore-option
                 *
                 * @private
                 */
                legendType: 'point',
                states: {
                    /**
                     * @excluding halo
                     */
                    hover: {
                        opacity: 1,
                        borderColor: "#333333" /* Palette.neutralColor80 */
                    },
                    /**
                     * @excluding halo
                     */
                    select: {
                        color: "#cccccc" /* Palette.neutralColor20 */,
                        borderColor: "#000000" /* Palette.neutralColor100 */,
                        animation: false
                    },
                    inactive: {
                        opacity: 0.075
                    }
                },
                tooltip: {
                    pointFormat: '{point.name}: {point.value}'
                }
            });
            return VennSeries;
        }(ScatterSeries));
        extend(VennSeries.prototype, {
            axisTypes: [],
            directTouch: true,
            drawLegendSymbol: LegendSymbol.drawRectangle,
            isCartesian: false,
            pointArrayMap: ['value'],
            pointClass: VennPoint,
            utils: VennUtils
        });
        SeriesRegistry.registerSeriesType('venn', VennSeries);
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
         * A `venn` series. If the [type](#series.venn.type) option is
         * not specified, it is inherited from [chart.type](#chart.type).
         *
         * @extends   series,plotOptions.venn
         * @excluding connectEnds, connectNulls, cropThreshold, dataParser, dataURL,
         *            findNearestPointBy, getExtremesFromAll, label, linecap, lineWidth,
         *            linkedTo, marker, negativeColor, pointInterval, pointIntervalUnit,
         *            pointPlacement, pointStart, softThreshold, stack, stacking, steps,
         *            threshold, xAxis, yAxis, zoneAxis, zones, dataSorting,
         *            boostThreshold, boostBlending
         * @product   highcharts
         * @requires  modules/venn
         * @apioption series.venn
         */
        /**
         * @type      {Array<*>}
         * @extends   series.scatter.data
         * @excluding marker, x, y
         * @product   highcharts
         * @apioption series.venn.data
         */
        /**
         * The name of the point. Used in data labels and tooltip. If name is not
         * defined then it will default to the joined values in
         * [sets](#series.venn.sets).
         *
         * @sample {highcharts} highcharts/demo/venn-diagram/
         *         Venn diagram
         * @sample {highcharts} highcharts/demo/euler-diagram/
         *         Euler diagram
         *
         * @type      {number}
         * @since     7.0.0
         * @product   highcharts
         * @apioption series.venn.data.name
         */
        /**
         * The value of the point, resulting in a relative area of the circle, or area
         * of overlap between two sets in the venn or euler diagram.
         *
         * @sample {highcharts} highcharts/demo/venn-diagram/
         *         Venn diagram
         * @sample {highcharts} highcharts/demo/euler-diagram/
         *         Euler diagram
         *
         * @type      {number}
         * @since     7.0.0
         * @product   highcharts
         * @apioption series.venn.data.value
         */
        /**
         * The set or sets the options will be applied to. If a single entry is defined,
         * then it will create a new set. If more than one entry is defined, then it
         * will define the overlap between the sets in the array.
         *
         * @sample {highcharts} highcharts/demo/venn-diagram/
         *         Venn diagram
         * @sample {highcharts} highcharts/demo/euler-diagram/
         *         Euler diagram
         *
         * @type      {Array<string>}
         * @since     7.0.0
         * @product   highcharts
         * @apioption series.venn.data.sets
         */
        /**
         * @excluding halo
         * @apioption series.venn.states.hover
         */
        /**
         * @excluding halo
         * @apioption series.venn.states.select
         */
        ''; // detach doclets above
        /* eslint-disable no-invalid-this */
        // Modify final series options.
        addEvent(VennSeries, 'afterSetOptions', function (e) {
            var options = e.options,
                states = options.states;
            if (this.is('venn')) {
                // Explicitly disable all halo options.
                Object.keys(states).forEach(function (state) {
                    states[state].halo = false;
                });
            }
        });

        return VennSeries;
    });
    _registerModule(_modules, 'masters/modules/venn.src.js', [], function () {


    });
}));