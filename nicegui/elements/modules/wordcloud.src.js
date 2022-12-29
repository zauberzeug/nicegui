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
        define('highcharts/modules/wordcloud', ['highcharts'], function (Highcharts) {
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
    _registerModule(_modules, 'Series/Wordcloud/WordcloudPoint.js', [_modules['Core/Series/SeriesRegistry.js'], _modules['Core/Utilities.js']], function (SeriesRegistry, U) {
        /* *
         *
         *  Experimental Highcharts module which enables visualization of a word cloud.
         *
         *  (c) 2016-2021 Highsoft AS
         *  Authors: Jon Arild Nygard
         *
         *  License: www.highcharts.com/license
         *
         *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
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
        var WordcloudPoint = /** @class */ (function (_super) {
                __extends(WordcloudPoint, _super);
            function WordcloudPoint() {
                /* *
                 *
                 * Properties
                 *
                 * */
                var _this = _super !== null && _super.apply(this,
                    arguments) || this;
                _this.dimensions = void 0;
                _this.options = void 0;
                _this.polygon = void 0;
                _this.rect = void 0;
                _this.series = void 0;
                return _this;
            }
            /* *
             *
             * Functions
             *
             * */
            WordcloudPoint.prototype.isValid = function () {
                return true;
            };
            return WordcloudPoint;
        }(ColumnPoint));
        extend(WordcloudPoint.prototype, {
            weight: 1
        });
        /* *
         *
         *  Default Export
         *
         * */

        return WordcloudPoint;
    });
    _registerModule(_modules, 'Series/Wordcloud/WordcloudUtils.js', [_modules['Core/Globals.js'], _modules['Core/Utilities.js']], function (H, U) {
        /* *
         *
         *  Experimental Highcharts module which enables visualization of a word cloud.
         *
         *  (c) 2016-2021 Highsoft AS
         *  Authors: Jon Arild Nygard
         *
         *  License: www.highcharts.com/license
         *
         *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
         * */
        var deg2rad = H.deg2rad;
        var extend = U.extend,
            find = U.find,
            isNumber = U.isNumber,
            isObject = U.isObject,
            merge = U.merge;
        /* *
         *
         * Functions
         *
         * */
        /* eslint-disable valid-jsdoc */
        /**
         * Detects if there is a collision between two rectangles.
         *
         * @private
         * @function isRectanglesIntersecting
         *
         * @param {Highcharts.PolygonBoxObject} r1
         * First rectangle.
         *
         * @param {Highcharts.PolygonBoxObject} r2
         * Second rectangle.
         *
         * @return {boolean}
         * Returns true if the rectangles overlap.
         */
        function isRectanglesIntersecting(r1, r2) {
            return !(r2.left > r1.right ||
                r2.right < r1.left ||
                r2.top > r1.bottom ||
                r2.bottom < r1.top);
        }
        /**
         * Calculates the normals to a line between two points.
         *
         * @private
         * @function getNormals
         * @param {Highcharts.PolygonPointObject} p1
         *        Start point for the line. Array of x and y value.
         * @param {Highcharts.PolygonPointObject} p2
         *        End point for the line. Array of x and y value.
         * @return {Highcharts.PolygonObject}
         *         Returns the two normals in an array.
         */
        function getNormals(p1, p2) {
            var dx = p2[0] - p1[0], // x2 - x1
                dy = p2[1] - p1[1]; // y2 - y1
                return [
                    [-dy,
                dx],
                    [dy, -dx]
                ];
        }
        /**
         * @private
         */
        function getAxesFromPolygon(polygon) {
            var points,
                axes = polygon.axes || [];
            if (!axes.length) {
                axes = [];
                points = points = polygon.concat([polygon[0]]);
                points.reduce(function findAxis(p1, p2) {
                    var normals = getNormals(p1,
                        p2),
                        axis = normals[0]; // Use the left normal as axis.
                        // Check that the axis is unique.
                        if (!find(axes,
                        function (existing) {
                            return existing[0] === axis[0] &&
                                existing[1] === axis[1];
                    })) {
                        axes.push(axis);
                    }
                    // Return p2 to be used as p1 in next iteration.
                    return p2;
                });
                polygon.axes = axes;
            }
            return axes;
        }
        /**
         * Projects a polygon onto a coordinate.
         *
         * @private
         * @function project
         * @param {Highcharts.PolygonObject} polygon
         * Array of points in a polygon.
         * @param {Highcharts.PolygonPointObject} target
         * The coordinate of pr
         */
        function project(polygon, target) {
            var products = polygon.map(function (point) {
                    var ax = point[0],
                ay = point[1],
                bx = target[0],
                by = target[1];
                return ax * bx + ay * by;
            });
            return {
                min: Math.min.apply(this, products),
                max: Math.max.apply(this, products)
            };
        }
        /**
         * @private
         */
        function isPolygonsOverlappingOnAxis(axis, polygon1, polygon2) {
            var projection1 = project(polygon1,
                axis),
                projection2 = project(polygon2,
                axis),
                isOverlapping = !(projection2.min > projection1.max ||
                    projection2.max < projection1.min);
            return !isOverlapping;
        }
        /**
         * Checks whether two convex polygons are colliding by using the Separating
         * Axis Theorem.
         *
         * @private
         * @function isPolygonsColliding
         * @param {Highcharts.PolygonObject} polygon1
         *        First polygon.
         *
         * @param {Highcharts.PolygonObject} polygon2
         *        Second polygon.
         *
         * @return {boolean}
         *         Returns true if they are colliding, otherwise false.
         */
        function isPolygonsColliding(polygon1, polygon2) {
            // Get the axis from both polygons.
            var axes1 = getAxesFromPolygon(polygon1),
                axes2 = getAxesFromPolygon(polygon2),
                axes = axes1.concat(axes2),
                overlappingOnAllAxes = !find(axes,
                function (axis) { return isPolygonsOverlappingOnAxis(axis,
                polygon1,
                polygon2); });
            return overlappingOnAllAxes;
        }
        /**
         * Detects if a word collides with any previously placed words.
         *
         * @private
         * @function intersectsAnyWord
         *
         * @param {Highcharts.Point} point
         * Point which the word is connected to.
         *
         * @param {Array<Highcharts.Point>} points
         * Previously placed points to check against.
         *
         * @return {boolean}
         * Returns true if there is collision.
         */
        function intersectsAnyWord(point, points) {
            var intersects = false,
                rect = point.rect,
                polygon = point.polygon,
                lastCollidedWith = point.lastCollidedWith,
                isIntersecting = function (p) {
                    var result = isRectanglesIntersecting(rect,
                p.rect);
                if (result &&
                    (point.rotation % 90 || p.rotation % 90)) {
                    result = isPolygonsColliding(polygon, p.polygon);
                }
                return result;
            };
            // If the point has already intersected a different point, chances are
            // they are still intersecting. So as an enhancement we check this
            // first.
            if (lastCollidedWith) {
                intersects = isIntersecting(lastCollidedWith);
                // If they no longer intersects, remove the cache from the point.
                if (!intersects) {
                    delete point.lastCollidedWith;
                }
            }
            // If not already found, then check if we can find a point that is
            // intersecting.
            if (!intersects) {
                intersects = !!find(points, function (p) {
                    var result = isIntersecting(p);
                    if (result) {
                        point.lastCollidedWith = p;
                    }
                    return result;
                });
            }
            return intersects;
        }
        /**
         * Gives a set of cordinates for an Archimedian Spiral.
         *
         * @private
         * @function archimedeanSpiral
         *
         * @param {number} attempt
         * How far along the spiral we have traversed.
         *
         * @param {Highcharts.WordcloudSpiralParamsObject} [params]
         * Additional parameters.
         *
         * @return {boolean|Highcharts.PositionObject}
         * Resulting coordinates, x and y. False if the word should be dropped from
         * the visualization.
         */
        function archimedeanSpiral(attempt, params) {
            var field = params.field,
                result = false,
                maxDelta = (field.width * field.width) + (field.height * field.height),
                t = attempt * 0.8; // 0.2 * 4 = 0.8. Enlarging the spiral.
                // Emergency brake. TODO make spiralling logic more foolproof.
                if (attempt <= 10000) {
                    result = {
                        x: t * Math.cos(t),
                        y: t * Math.sin(t)
                    };
                if (!(Math.min(Math.abs(result.x), Math.abs(result.y)) < maxDelta)) {
                    result = false;
                }
            }
            return result;
        }
        /**
         * Gives a set of cordinates for an rectangular spiral.
         *
         * @private
         * @function squareSpiral
         *
         * @param {number} attempt
         * How far along the spiral we have traversed.
         *
         * @param {Highcharts.WordcloudSpiralParamsObject} [params]
         * Additional parameters.
         *
         * @return {boolean|Highcharts.PositionObject}
         * Resulting coordinates, x and y. False if the word should be dropped from
         * the visualization.
         */
        function squareSpiral(attempt, params) {
            var a = attempt * 4,
                k = Math.ceil((Math.sqrt(a) - 1) / 2),
                t = 2 * k + 1,
                m = Math.pow(t, 2),
                isBoolean = function (x) {
                    return typeof x === 'boolean';
            }, result = false;
            t -= 1;
            if (attempt <= 10000) {
                if (isBoolean(result) && a >= m - t) {
                    result = {
                        x: k - (m - a),
                        y: -k
                    };
                }
                m -= t;
                if (isBoolean(result) && a >= m - t) {
                    result = {
                        x: -k,
                        y: -k + (m - a)
                    };
                }
                m -= t;
                if (isBoolean(result)) {
                    if (a >= m - t) {
                        result = {
                            x: -k + (m - a),
                            y: k
                        };
                    }
                    else {
                        result = {
                            x: k,
                            y: k - (m - a - t)
                        };
                    }
                }
                result.x *= 5;
                result.y *= 5;
            }
            return result;
        }
        /**
         * Gives a set of cordinates for an rectangular spiral.
         *
         * @private
         * @function rectangularSpiral
         *
         * @param {number} attempt
         * How far along the spiral we have traversed.
         *
         * @param {Highcharts.WordcloudSpiralParamsObject} [params]
         * Additional parameters.
         *
         * @return {boolean|Higcharts.PositionObject}
         * Resulting coordinates, x and y. False if the word should be dropped from
         * the visualization.
         */
        function rectangularSpiral(attempt, params) {
            var result = squareSpiral(attempt,
                params),
                field = params.field;
            if (result) {
                result.x *= field.ratioX;
                result.y *= field.ratioY;
            }
            return result;
        }
        /**
         * @private
         * @function getRandomPosition
         *
         * @param {number} size
         * Random factor.
         *
         * @return {number}
         * Random position.
         */
        function getRandomPosition(size) {
            return Math.round((size * (Math.random() + 0.5)) / 2);
        }
        /**
         * Calculates the proper scale to fit the cloud inside the plotting area.
         *
         * @private
         * @function getScale
         *
         * @param {number} targetWidth
         * Width of target area.
         *
         * @param {number} targetHeight
         * Height of target area.
         *
         * @param {Object} field
         * The playing field.
         *
         * @param {Highcharts.Series} series
         * Series object.
         *
         * @return {number}
         * Returns the value to scale the playing field up to the size of the target
         * area.
         */
        function getScale(targetWidth, targetHeight, field) {
            var height = Math.max(Math.abs(field.top),
                Math.abs(field.bottom)) * 2,
                width = Math.max(Math.abs(field.left),
                Math.abs(field.right)) * 2,
                scaleX = width > 0 ? 1 / width * targetWidth : 1,
                scaleY = height > 0 ? 1 / height * targetHeight : 1;
            return Math.min(scaleX, scaleY);
        }
        /**
         * Calculates what is called the playing field. The field is the area which
         * all the words are allowed to be positioned within. The area is
         * proportioned to match the target aspect ratio.
         *
         * @private
         * @function getPlayingField
         *
         * @param {number} targetWidth
         * Width of the target area.
         *
         * @param {number} targetHeight
         * Height of the target area.
         *
         * @param {Array<Highcharts.Point>} data
         * Array of points.
         *
         * @param {Object} data.dimensions
         * The height and width of the word.
         *
         * @return {Object}
         * The width and height of the playing field.
         */
        function getPlayingField(targetWidth, targetHeight, data) {
            var info = data.reduce(function (obj,
                point) {
                    var dimensions = point.dimensions,
                x = Math.max(dimensions.width,
                dimensions.height);
                // Find largest height.
                obj.maxHeight = Math.max(obj.maxHeight, dimensions.height);
                // Find largest width.
                obj.maxWidth = Math.max(obj.maxWidth, dimensions.width);
                // Sum up the total maximum area of all the words.
                obj.area += x * x;
                return obj;
            }, {
                maxHeight: 0,
                maxWidth: 0,
                area: 0
            }), 
            /**
             * Use largest width, largest height, or root of total area to give
             * size to the playing field.
             */
            x = Math.max(info.maxHeight, // Have enough space for the tallest word
            info.maxWidth, // Have enough space for the broadest word
            // Adjust 15% to account for close packing of words
            Math.sqrt(info.area) * 0.85), ratioX = targetWidth > targetHeight ? targetWidth / targetHeight : 1, ratioY = targetHeight > targetWidth ? targetHeight / targetWidth : 1;
            return {
                width: x * ratioX,
                height: x * ratioY,
                ratioX: ratioX,
                ratioY: ratioY
            };
        }
        /**
         * Calculates a number of degrees to rotate, based upon a number of
         * orientations within a range from-to.
         *
         * @private
         * @function getRotation
         *
         * @param {number} [orientations]
         * Number of orientations.
         *
         * @param {number} [index]
         * Index of point, used to decide orientation.
         *
         * @param {number} [from]
         * The smallest degree of rotation.
         *
         * @param {number} [to]
         * The largest degree of rotation.
         *
         * @return {boolean|number}
         * Returns the resulting rotation for the word. Returns false if invalid
         * input parameters.
         */
        function getRotation(orientations, index, from, to) {
            var result = false, // Default to false
                range,
                intervals,
                orientation;
            // Check if we have valid input parameters.
            if (isNumber(orientations) &&
                isNumber(index) &&
                isNumber(from) &&
                isNumber(to) &&
                orientations > 0 &&
                index > -1 &&
                to > from) {
                range = to - from;
                intervals = range / (orientations - 1 || 1);
                orientation = index % orientations;
                result = from + (orientation * intervals);
            }
            return result;
        }
        /**
         * Calculates the spiral positions and store them in scope for quick access.
         *
         * @private
         * @function getSpiral
         *
         * @param {Function} fn
         * The spiral function.
         *
         * @param {Object} params
         * Additional parameters for the spiral.
         *
         * @return {Function}
         * Function with access to spiral positions.
         */
        function getSpiral(fn, params) {
            var length = 10000,
                i,
                arr = [];
            for (i = 1; i < length; i++) {
                // @todo unnecessary amount of precaclulation
                arr.push(fn(i, params));
            }
            return function (attempt) {
                return attempt <= length ? arr[attempt - 1] : false;
            };
        }
        /**
         * Detects if a word is placed outside the playing field.
         *
         * @private
         * @function outsidePlayingField
         *
         * @param {Highcharts.PolygonBoxObject} rect
         * The word box.
         *
         * @param {Highcharts.WordcloudFieldObject} field
         * The width and height of the playing field.
         *
         * @return {boolean}
         * Returns true if the word is placed outside the field.
         */
        function outsidePlayingField(rect, field) {
            var playingField = {
                    left: -(field.width / 2),
                    right: field.width / 2,
                    top: -(field.height / 2),
                    bottom: field.height / 2
                };
            return !(playingField.left < rect.left &&
                playingField.right > rect.right &&
                playingField.top < rect.top &&
                playingField.bottom > rect.bottom);
        }
        /**
         * @private
         */
        function movePolygon(deltaX, deltaY, polygon) {
            return polygon.map(function (point) {
                return [
                    point[0] + deltaX,
                    point[1] + deltaY
                ];
            });
        }
        /**
         * Check if a point intersects with previously placed words, or if it goes
         * outside the field boundaries. If a collision, then try to adjusts the
         * position.
         *
         * @private
         * @function intersectionTesting
         *
         * @param {Highcharts.Point} point
         * Point to test for intersections.
         *
         * @param {Highcharts.WordcloudTestOptionsObject} options
         * Options object.
         *
         * @return {boolean|Highcharts.PositionObject}
         * Returns an object with how much to correct the positions. Returns false
         * if the word should not be placed at all.
         */
        function intersectionTesting(point, options) {
            var placed = options.placed,
                field = options.field,
                rectangle = options.rectangle,
                polygon = options.polygon,
                spiral = options.spiral,
                attempt = 1,
                delta = {
                    x: 0,
                    y: 0
                }, 
                // Make a copy to update values during intersection testing.
                rect = point.rect = extend({},
                rectangle);
            point.polygon = polygon;
            point.rotation = options.rotation;
            /* while w intersects any previously placed words:
                do {
                move w a little bit along a spiral path
                } while any part of w is outside the playing field and
                        the spiral radius is still smallish */
            while (delta !== false &&
                (intersectsAnyWord(point, placed) ||
                    outsidePlayingField(rect, field))) {
                delta = spiral(attempt);
                if (isObject(delta)) {
                    // Update the DOMRect with new positions.
                    rect.left = rectangle.left + delta.x;
                    rect.right = rectangle.right + delta.x;
                    rect.top = rectangle.top + delta.y;
                    rect.bottom = rectangle.bottom + delta.y;
                    point.polygon = movePolygon(delta.x, delta.y, polygon);
                }
                attempt++;
            }
            return delta;
        }
        /**
         * Extends the playing field to have enough space to fit a given word.
         *
         * @private
         * @function extendPlayingField
         *
         * @param {Highcharts.WordcloudFieldObject} field
         * The width, height and ratios of a playing field.
         *
         * @param {Highcharts.PolygonBoxObject} rectangle
         * The bounding box of the word to add space for.
         *
         * @return {Highcharts.WordcloudFieldObject}
         * Returns the extended playing field with updated height and width.
         */
        function extendPlayingField(field, rectangle) {
            var height,
                width,
                ratioX,
                ratioY,
                x,
                extendWidth,
                extendHeight,
                result;
            if (isObject(field) && isObject(rectangle)) {
                height = (rectangle.bottom - rectangle.top);
                width = (rectangle.right - rectangle.left);
                ratioX = field.ratioX;
                ratioY = field.ratioY;
                // Use the same variable to extend both the height and width.
                x = ((width * ratioX) > (height * ratioY)) ? width : height;
                // Multiply variable with ratios to preserve aspect ratio.
                extendWidth = x * ratioX;
                extendHeight = x * ratioY;
                // Calculate the size of the new field after adding
                // space for the word.
                result = merge(field, {
                    // Add space on the left and right.
                    width: field.width + (extendWidth * 2),
                    // Add space on the top and bottom.
                    height: field.height + (extendHeight * 2)
                });
            }
            else {
                result = field;
            }
            // Return the new extended field.
            return result;
        }
        /**
         * If a rectangle is outside a give field, then the boundaries of the field
         * is adjusted accordingly. Modifies the field object which is passed as the
         * first parameter.
         *
         * @private
         * @function updateFieldBoundaries
         *
         * @param {Highcharts.WordcloudFieldObject} field
         * The bounding box of a playing field.
         *
         * @param {Highcharts.PolygonBoxObject} rectangle
         * The bounding box for a placed point.
         *
         * @return {Highcharts.WordcloudFieldObject}
         * Returns a modified field object.
         */
        function updateFieldBoundaries(field, rectangle) {
            // @todo improve type checking.
            if (!isNumber(field.left) || field.left > rectangle.left) {
                field.left = rectangle.left;
            }
            if (!isNumber(field.right) || field.right < rectangle.right) {
                field.right = rectangle.right;
            }
            if (!isNumber(field.top) || field.top > rectangle.top) {
                field.top = rectangle.top;
            }
            if (!isNumber(field.bottom) || field.bottom < rectangle.bottom) {
                field.bottom = rectangle.bottom;
            }
            return field;
        }
        /**
         * Alternative solution to correctFloat.
         * E.g Highcharts.correctFloat(123, 2) returns 120, when it should be 123.
         *
         * @private
         * @function correctFloat
         */
        function correctFloat(number, precision) {
            var p = isNumber(precision) ? precision : 14,
                magnitude = Math.pow(10,
                p);
            return Math.round(number * magnitude) / magnitude;
        }
        /**
         * @private
         */
        function getBoundingBoxFromPolygon(points) {
            return points.reduce(function (obj, point) {
                var x = point[0],
                    y = point[1];
                obj.left = Math.min(x, obj.left);
                obj.right = Math.max(x, obj.right);
                obj.bottom = Math.max(y, obj.bottom);
                obj.top = Math.min(y, obj.top);
                return obj;
            }, {
                left: Number.MAX_VALUE,
                right: -Number.MAX_VALUE,
                bottom: -Number.MAX_VALUE,
                top: Number.MAX_VALUE
            });
        }
        /**
         * @private
         */
        function getPolygon(x, y, width, height, rotation) {
            var origin = [x,
                y],
                left = x - (width / 2),
                right = x + (width / 2),
                top = y - (height / 2),
                bottom = y + (height / 2),
                polygon = [
                    [left,
                top],
                    [right,
                top],
                    [right,
                bottom],
                    [left,
                bottom]
                ];
            return polygon.map(function (point) {
                return rotate2DToPoint(point, origin, -rotation);
            });
        }
        /**
         * Rotates a point clockwise around the origin.
         *
         * @private
         * @function rotate2DToOrigin
         * @param {Highcharts.PolygonPointObject} point
         *        The x and y coordinates for the point.
         * @param {number} angle
         *        The angle of rotation.
         * @return {Highcharts.PolygonPointObject}
         *         The x and y coordinate for the rotated point.
         */
        function rotate2DToOrigin(point, angle) {
            var x = point[0],
                y = point[1],
                rad = deg2rad * -angle,
                cosAngle = Math.cos(rad),
                sinAngle = Math.sin(rad);
            return [
                correctFloat(x * cosAngle - y * sinAngle),
                correctFloat(x * sinAngle + y * cosAngle)
            ];
        }
        /**
         * Rotate a point clockwise around another point.
         *
         * @private
         * @function rotate2DToPoint
         * @param {Highcharts.PolygonPointObject} point
         *        The x and y coordinates for the point.
         * @param {Highcharts.PolygonPointObject} origin
         *        The point to rotate around.
         * @param {number} angle
         *        The angle of rotation.
         * @return {Highcharts.PolygonPointObject}
         *         The x and y coordinate for the rotated point.
         */
        function rotate2DToPoint(point, origin, angle) {
            var x = point[0] - origin[0],
                y = point[1] - origin[1],
                rotated = rotate2DToOrigin([x,
                y],
                angle);
            return [
                rotated[0] + origin[0],
                rotated[1] + origin[1]
            ];
        }
        /* *
         *
         * Default export
         *
         * */
        var WordcloudUtils = {
                archimedeanSpiral: archimedeanSpiral,
                extendPlayingField: extendPlayingField,
                getBoundingBoxFromPolygon: getBoundingBoxFromPolygon,
                getPlayingField: getPlayingField,
                getPolygon: getPolygon,
                getRandomPosition: getRandomPosition,
                getRotation: getRotation,
                getScale: getScale,
                getSpiral: getSpiral,
                intersectionTesting: intersectionTesting,
                isPolygonsColliding: isPolygonsColliding,
                isRectanglesIntersecting: isRectanglesIntersecting,
                rectangularSpiral: rectangularSpiral,
                rotate2DToOrigin: rotate2DToOrigin,
                rotate2DToPoint: rotate2DToPoint,
                squareSpiral: squareSpiral,
                updateFieldBoundaries: updateFieldBoundaries
            };

        return WordcloudUtils;
    });
    _registerModule(_modules, 'Series/Wordcloud/WordcloudSeries.js', [_modules['Series/DrawPointUtilities.js'], _modules['Core/Globals.js'], _modules['Core/Series/Series.js'], _modules['Core/Series/SeriesRegistry.js'], _modules['Core/Utilities.js'], _modules['Series/Wordcloud/WordcloudPoint.js'], _modules['Series/Wordcloud/WordcloudUtils.js']], function (DPU, H, Series, SeriesRegistry, U, WordcloudPoint, WordcloudUtils) {
        /* *
         *
         *  Experimental Highcharts module which enables visualization of a word cloud.
         *
         *  (c) 2016-2021 Highsoft AS
         *  Authors: Jon Arild Nygard
         *
         *  License: www.highcharts.com/license
         *
         *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
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
        var ColumnSeries = SeriesRegistry.seriesTypes.column;
        var extend = U.extend,
            isArray = U.isArray,
            isNumber = U.isNumber,
            isObject = U.isObject,
            merge = U.merge;
        var archimedeanSpiral = WordcloudUtils.archimedeanSpiral,
            extendPlayingField = WordcloudUtils.extendPlayingField,
            getBoundingBoxFromPolygon = WordcloudUtils.getBoundingBoxFromPolygon,
            getPlayingField = WordcloudUtils.getPlayingField,
            getPolygon = WordcloudUtils.getPolygon,
            getRandomPosition = WordcloudUtils.getRandomPosition,
            getRotation = WordcloudUtils.getRotation,
            getScale = WordcloudUtils.getScale,
            getSpiral = WordcloudUtils.getSpiral,
            intersectionTesting = WordcloudUtils.intersectionTesting,
            isPolygonsColliding = WordcloudUtils.isPolygonsColliding,
            rectangularSpiral = WordcloudUtils.rectangularSpiral,
            rotate2DToOrigin = WordcloudUtils.rotate2DToOrigin,
            rotate2DToPoint = WordcloudUtils.rotate2DToPoint,
            squareSpiral = WordcloudUtils.squareSpiral,
            updateFieldBoundaries = WordcloudUtils.updateFieldBoundaries;
        /* *
         *
         *  Class
         *
         * */
        /**
         * @private
         * @class
         * @name Highcharts.seriesTypes.wordcloud
         *
         * @augments Highcharts.Series
         */
        var WordcloudSeries = /** @class */ (function (_super) {
                __extends(WordcloudSeries, _super);
            function WordcloudSeries() {
                /* *
                 *
                 * Static properties
                 *
                 * */
                var _this = _super !== null && _super.apply(this,
                    arguments) || this;
                /* *
                 *
                 * Properties
                 *
                 * */
                _this.data = void 0;
                _this.options = void 0;
                _this.points = void 0;
                return _this;
            }
            /**
             *
             * Functions
             *
             */
            WordcloudSeries.prototype.bindAxes = function () {
                var wordcloudAxis = {
                        endOnTick: false,
                        gridLineWidth: 0,
                        lineWidth: 0,
                        maxPadding: 0,
                        startOnTick: false,
                        title: void 0,
                        tickPositions: []
                    };
                Series.prototype.bindAxes.call(this);
                extend(this.yAxis.options, wordcloudAxis);
                extend(this.xAxis.options, wordcloudAxis);
            };
            WordcloudSeries.prototype.pointAttribs = function (point, state) {
                var attribs = H.seriesTypes.column.prototype
                        .pointAttribs.call(this,
                    point,
                    state);
                delete attribs.stroke;
                delete attribs['stroke-width'];
                return attribs;
            };
            /**
             * Calculates the fontSize of a word based on its weight.
             *
             * @private
             * @function Highcharts.Series#deriveFontSize
             *
             * @param {number} [relativeWeight=0]
             * The weight of the word, on a scale 0-1.
             *
             * @param {number} [maxFontSize=1]
             * The maximum font size of a word.
             *
             * @param {number} [minFontSize=1]
             * The minimum font size of a word.
             *
             * @return {number}
             * Returns the resulting fontSize of a word. If minFontSize is larger then
             * maxFontSize the result will equal minFontSize.
             */
            WordcloudSeries.prototype.deriveFontSize = function (relativeWeight, maxFontSize, minFontSize) {
                var weight = isNumber(relativeWeight) ? relativeWeight : 0,
                    max = isNumber(maxFontSize) ? maxFontSize : 1,
                    min = isNumber(minFontSize) ? minFontSize : 1;
                return Math.floor(Math.max(min, weight * max));
            };
            WordcloudSeries.prototype.drawPoints = function () {
                var series = this,
                    hasRendered = series.hasRendered,
                    xAxis = series.xAxis,
                    yAxis = series.yAxis,
                    chart = series.chart,
                    group = series.group,
                    options = series.options,
                    animation = options.animation,
                    allowExtendPlayingField = options.allowExtendPlayingField,
                    renderer = chart.renderer,
                    testElement = renderer.text().add(group),
                    placed = [],
                    placementStrategy = series.placementStrategy[options.placementStrategy],
                    spiral,
                    rotation = options.rotation,
                    scale,
                    weights = series.points.map(function (p) {
                        return p.weight;
                }), maxWeight = Math.max.apply(null, weights), 
                // concat() prevents from sorting the original array.
                data = series.points.concat().sort(function (a, b) {
                    return b.weight - a.weight; // Sort descending
                }), field;
                // Reset the scale before finding the dimensions (#11993).
                // SVGGRaphicsElement.getBBox() (used in SVGElement.getBBox(boolean))
                // returns slightly different values for the same element depending on
                // whether it is rendered in a group which has already defined scale
                // (e.g. 6) or in the group without a scale (scale = 1).
                series.group.attr({
                    scaleX: 1,
                    scaleY: 1
                });
                // Get the dimensions for each word.
                // Used in calculating the playing field.
                data.forEach(function (point) {
                    var relativeWeight = 1 / maxWeight * point.weight,
                        fontSize = series.deriveFontSize(relativeWeight,
                        options.maxFontSize,
                        options.minFontSize),
                        css = extend({
                            fontSize: fontSize + 'px'
                        },
                        options.style),
                        bBox;
                    testElement.css(css).attr({
                        x: 0,
                        y: 0,
                        text: point.name
                    });
                    bBox = testElement.getBBox(true);
                    point.dimensions = {
                        height: bBox.height,
                        width: bBox.width
                    };
                });
                // Calculate the playing field.
                field = getPlayingField(xAxis.len, yAxis.len, data);
                spiral = getSpiral(series.spirals[options.spiral], {
                    field: field
                });
                // Draw all the points.
                data.forEach(function (point) {
                    var relativeWeight = 1 / maxWeight * point.weight,
                        fontSize = series.deriveFontSize(relativeWeight,
                        options.maxFontSize,
                        options.minFontSize),
                        css = extend({
                            fontSize: fontSize + 'px'
                        },
                        options.style),
                        placement = placementStrategy(point, {
                            data: data,
                            field: field,
                            placed: placed,
                            rotation: rotation
                        }),
                        attr = extend(series.pointAttribs(point, (point.selected && 'select')), {
                            align: 'center',
                            'alignment-baseline': 'middle',
                            'dominant-baseline': 'middle',
                            x: placement.x,
                            y: placement.y,
                            text: point.name,
                            rotation: isNumber(placement.rotation) ?
                                placement.rotation :
                                void 0
                        }),
                        polygon = getPolygon(placement.x,
                        placement.y,
                        point.dimensions.width,
                        point.dimensions.height,
                        placement.rotation),
                        rectangle = getBoundingBoxFromPolygon(polygon),
                        delta = intersectionTesting(point, {
                            rectangle: rectangle,
                            polygon: polygon,
                            field: field,
                            placed: placed,
                            spiral: spiral,
                            rotation: placement.rotation
                        }),
                        animate;
                    // If there is no space for the word, extend the playing field.
                    if (!delta && allowExtendPlayingField) {
                        // Extend the playing field to fit the word.
                        field = extendPlayingField(field, rectangle);
                        // Run intersection testing one more time to place the word.
                        delta = intersectionTesting(point, {
                            rectangle: rectangle,
                            polygon: polygon,
                            field: field,
                            placed: placed,
                            spiral: spiral,
                            rotation: placement.rotation
                        });
                    }
                    // Check if point was placed, if so delete it, otherwise place it
                    // on the correct positions.
                    if (isObject(delta)) {
                        attr.x = (attr.x || 0) + delta.x;
                        attr.y = (attr.y || 0) + delta.y;
                        rectangle.left += delta.x;
                        rectangle.right += delta.x;
                        rectangle.top += delta.y;
                        rectangle.bottom += delta.y;
                        field = updateFieldBoundaries(field, rectangle);
                        placed.push(point);
                        point.isNull = false;
                        point.isInside = true; // #15447
                    }
                    else {
                        point.isNull = true;
                    }
                    if (animation) {
                        // Animate to new positions
                        animate = {
                            x: attr.x,
                            y: attr.y
                        };
                        // Animate from center of chart
                        if (!hasRendered) {
                            attr.x = 0;
                            attr.y = 0;
                            // or animate from previous position
                        }
                        else {
                            delete attr.x;
                            delete attr.y;
                        }
                    }
                    DPU.draw(point, {
                        animatableAttribs: animate,
                        attribs: attr,
                        css: css,
                        group: group,
                        renderer: renderer,
                        shapeArgs: void 0,
                        shapeType: 'text'
                    });
                });
                // Destroy the element after use.
                testElement = testElement.destroy();
                // Scale the series group to fit within the plotArea.
                scale = getScale(xAxis.len, yAxis.len, field);
                series.group.attr({
                    scaleX: scale,
                    scaleY: scale
                });
            };
            WordcloudSeries.prototype.hasData = function () {
                var series = this;
                return (isObject(series) &&
                    series.visible === true &&
                    isArray(series.points) &&
                    series.points.length > 0);
            };
            WordcloudSeries.prototype.getPlotBox = function () {
                var series = this, chart = series.chart, inverted = chart.inverted, 
                    // Swap axes for inverted (#2339)
                    xAxis = series[(inverted ? 'yAxis' : 'xAxis')], yAxis = series[(inverted ? 'xAxis' : 'yAxis')], width = xAxis ? xAxis.len : chart.plotWidth, height = yAxis ? yAxis.len : chart.plotHeight, x = xAxis ? xAxis.left : chart.plotLeft, y = yAxis ? yAxis.top : chart.plotTop;
                return {
                    translateX: x + (width / 2),
                    translateY: y + (height / 2),
                    scaleX: 1,
                    scaleY: 1
                };
            };
            /**
             * A word cloud is a visualization of a set of words, where the size and
             * placement of a word is determined by how it is weighted.
             *
             * @sample highcharts/demo/wordcloud Word Cloud chart
             *
             * @extends      plotOptions.column
             * @excluding    allAreas, boostThreshold, clip, colorAxis, compare,
             *               compareBase, crisp, cropThreshold, dataGrouping,
             *               dataLabels, depth, dragDrop, edgeColor, findNearestPointBy,
             *               getExtremesFromAll, grouping, groupPadding, groupZPadding,
             *               joinBy, maxPointWidth, minPointLength, navigatorOptions,
             *               negativeColor, pointInterval, pointIntervalUnit,
             *               pointPadding, pointPlacement, pointRange, pointStart,
             *               pointWidth, pointStart, pointWidth, shadow, showCheckbox,
             *               showInNavigator, softThreshold, stacking, threshold,
             *               zoneAxis, zones, dataSorting, boostBlending
             * @product      highcharts
             * @since        6.0.0
             * @requires     modules/wordcloud
             * @optionparent plotOptions.wordcloud
             */
            WordcloudSeries.defaultOptions = merge(ColumnSeries.defaultOptions, {
                /**
                 * If there is no space for a word on the playing field, then this
                 * option will allow the playing field to be extended to fit the word.
                 * If false then the word will be dropped from the visualization.
                 *
                 * NB! This option is currently not decided to be published in the API,
                 * and is therefore marked as private.
                 *
                 * @ignore-option
                 */
                allowExtendPlayingField: true,
                animation: {
                    /** @internal */
                    duration: 500
                },
                borderWidth: 0,
                /**
                 * @ignore-option
                 */
                clip: false,
                colorByPoint: true,
                cropThreshold: Infinity,
                /**
                 * A threshold determining the minimum font size that can be applied to
                 * a word.
                 */
                minFontSize: 1,
                /**
                 * The word with the largest weight will have a font size equal to this
                 * value. The font size of a word is the ratio between its weight and
                 * the largest occuring weight, multiplied with the value of
                 * maxFontSize.
                 */
                maxFontSize: 25,
                /**
                 * This option decides which algorithm is used for placement, and
                 * rotation of a word. The choice of algorith is therefore a crucial
                 * part of the resulting layout of the wordcloud. It is possible for
                 * users to add their own custom placement strategies for use in word
                 * cloud. Read more about it in our
                 * [documentation](https://www.highcharts.com/docs/chart-and-series-types/word-cloud-series#custom-placement-strategies)
                 *
                 * @validvalue ["center", "random"]
                 */
                placementStrategy: 'center',
                /**
                 * Rotation options for the words in the wordcloud.
                 *
                 * @sample highcharts/plotoptions/wordcloud-rotation
                 *         Word cloud with rotation
                 */
                rotation: {
                    /**
                     * The smallest degree of rotation for a word.
                     */
                    from: 0,
                    /**
                     * The number of possible orientations for a word, within the range
                     * of `rotation.from` and `rotation.to`. Must be a number larger
                     * than 0.
                     */
                    orientations: 2,
                    /**
                     * The largest degree of rotation for a word.
                     */
                    to: 90
                },
                showInLegend: false,
                /**
                 * Spiral used for placing a word after the initial position
                 * experienced a collision with either another word or the borders.
                 * It is possible for users to add their own custom spiralling
                 * algorithms for use in word cloud. Read more about it in our
                 * [documentation](https://www.highcharts.com/docs/chart-and-series-types/word-cloud-series#custom-spiralling-algorithm)
                 *
                 * @validvalue ["archimedean", "rectangular", "square"]
                 */
                spiral: 'rectangular',
                /**
                 * CSS styles for the words.
                 *
                 * @type    {Highcharts.CSSObject}
                 * @default {"fontFamily":"sans-serif", "fontWeight": "900"}
                 */
                style: {
                    /** @ignore-option */
                    fontFamily: 'sans-serif',
                    /** @ignore-option */
                    fontWeight: '900',
                    /** @ignore-option */
                    whiteSpace: 'nowrap'
                },
                tooltip: {
                    followPointer: true,
                    pointFormat: '<span style="color:{point.color}">\u25CF</span> {series.name}: <b>{point.weight}</b><br/>'
                }
            });
            return WordcloudSeries;
        }(ColumnSeries));
        extend(WordcloudSeries.prototype, {
            animate: noop,
            animateDrilldown: noop,
            animateDrillupFrom: noop,
            pointClass: WordcloudPoint,
            setClip: noop,
            // Strategies used for deciding rotation and initial position of a word. To
            // implement a custom strategy, have a look at the function random for
            // example.
            placementStrategy: {
                random: function (point, options) {
                    var field = options.field,
                        r = options.rotation;
                    return {
                        x: getRandomPosition(field.width) - (field.width / 2),
                        y: getRandomPosition(field.height) - (field.height / 2),
                        rotation: getRotation(r.orientations, point.index, r.from, r.to)
                    };
                },
                center: function (point, options) {
                    var r = options.rotation;
                    return {
                        x: 0,
                        y: 0,
                        rotation: getRotation(r.orientations, point.index, r.from, r.to)
                    };
                }
            },
            pointArrayMap: ['weight'],
            // Spirals used for placing a word after the initial position experienced a
            // collision with either another word or the borders. To implement a custom
            // spiral, look at the function archimedeanSpiral for example.
            spirals: {
                'archimedean': archimedeanSpiral,
                'rectangular': rectangularSpiral,
                'square': squareSpiral
            },
            utils: {
                extendPlayingField: extendPlayingField,
                getRotation: getRotation,
                isPolygonsColliding: isPolygonsColliding,
                rotate2DToOrigin: rotate2DToOrigin,
                rotate2DToPoint: rotate2DToPoint
            }
        });
        SeriesRegistry.registerSeriesType('wordcloud', WordcloudSeries);
        /* *
         *
         * Export Default
         *
         * */
        /* *
         *
         * API Options
         *
         * */
        /**
         * A `wordcloud` series. If the [type](#series.wordcloud.type) option is not
         * specified, it is inherited from [chart.type](#chart.type).
         *
         * @extends   series,plotOptions.wordcloud
         * @exclude   dataSorting, boostThreshold, boostBlending
         * @product   highcharts
         * @requires  modules/wordcloud
         * @apioption series.wordcloud
         */
        /**
         * An array of data points for the series. For the `wordcloud` series type,
         * points can be given in the following ways:
         *
         * 1. An array of arrays with 2 values. In this case, the values correspond to
         *    `name,weight`.
         *    ```js
         *    data: [
         *        ['Lorem', 4],
         *        ['Ipsum', 1]
         *    ]
         *    ```
         *
         * 2. An array of objects with named values. The following snippet shows only a
         *    few settings, see the complete options set below. If the total number of
         *    data points exceeds the series'
         *    [turboThreshold](#series.arearange.turboThreshold), this option is not
         *    available.
         *    ```js
         *    data: [{
         *        name: "Lorem",
         *        weight: 4
         *    }, {
         *        name: "Ipsum",
         *        weight: 1
         *    }]
         *    ```
         *
         * @type      {Array<Array<string,number>|*>}
         * @extends   series.line.data
         * @excluding drilldown, marker, x, y
         * @product   highcharts
         * @apioption series.wordcloud.data
         */
        /**
         * The name decides the text for a word.
         *
         * @type      {string}
         * @since     6.0.0
         * @product   highcharts
         * @apioption series.wordcloud.data.name
         */
        /**
         * The weighting of a word. The weight decides the relative size of a word
         * compared to the rest of the collection.
         *
         * @type      {number}
         * @since     6.0.0
         * @product   highcharts
         * @apioption series.wordcloud.data.weight
         */
        ''; // detach doclets above

        return WordcloudSeries;
    });
    _registerModule(_modules, 'masters/modules/wordcloud.src.js', [], function () {


    });
}));