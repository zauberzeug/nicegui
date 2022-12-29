/**
 * @license Highstock JS v10.3.2 (2022-11-28)
 *
 * Drag-panes module
 *
 * (c) 2010-2021 Highsoft AS
 * Author: Kacper Madej
 *
 * License: www.highcharts.com/license
 */
(function (factory) {
    if (typeof module === 'object' && module.exports) {
        factory['default'] = factory;
        module.exports = factory;
    } else if (typeof define === 'function' && define.amd) {
        define('highcharts/modules/drag-panes', ['highcharts', 'highcharts/modules/stock'], function (Highcharts) {
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
    _registerModule(_modules, 'Extensions/DragPanes.js', [_modules['Core/Globals.js'], _modules['Core/Axis/Axis.js'], _modules['Core/Axis/AxisDefaults.js'], _modules['Core/Pointer.js'], _modules['Core/Utilities.js']], function (H, Axis, AxisDefaults, Pointer, U) {
        /* *
         *
         *  Plugin for resizing axes / panes in a chart.
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
        var hasTouch = H.hasTouch;
        var addEvent = U.addEvent,
            clamp = U.clamp,
            isNumber = U.isNumber,
            merge = U.merge,
            objectEach = U.objectEach,
            relativeLength = U.relativeLength,
            wrap = U.wrap;
        /* *
         *
         *  Class
         *
         * */
        /* eslint-disable no-invalid-this, valid-jsdoc */
        /**
         * The AxisResizer class.
         *
         * @private
         * @class
         * @name Highcharts.AxisResizer
         *
         * @param {Highcharts.Axis} axis
         *        Main axis for the AxisResizer.
         */
        var AxisResizer = /** @class */ (function () {
                function AxisResizer(axis) {
                    /* eslint-enable no-invalid-this */
                    this.axis = void 0;
                this.controlLine = void 0;
                this.lastPos = void 0;
                this.options = void 0;
                this.init(axis);
            }
            /**
             * Initialize the AxisResizer object.
             *
             * @function Highcharts.AxisResizer#init
             *
             * @param {Highcharts.Axis} axis
             *        Main axis for the AxisResizer.
             */
            AxisResizer.prototype.init = function (axis, update) {
                this.axis = axis;
                this.options = axis.options.resize;
                this.render();
                if (!update) {
                    // Add mouse events.
                    this.addMouseEvents();
                }
            };
            /**
             * Render the AxisResizer
             *
             * @function Highcharts.AxisResizer#render
             */
            AxisResizer.prototype.render = function () {
                var resizer = this,
                    axis = resizer.axis,
                    chart = axis.chart,
                    options = resizer.options,
                    x = options.x || 0,
                    y = options.y, 
                    // Normalize control line position according to the plot area
                    pos = clamp(axis.top + axis.height + y,
                    chart.plotTop,
                    chart.plotTop + chart.plotHeight),
                    attr = {},
                    lineWidth;
                if (!chart.styledMode) {
                    attr = {
                        cursor: options.cursor,
                        stroke: options.lineColor,
                        'stroke-width': options.lineWidth,
                        dashstyle: options.lineDashStyle
                    };
                }
                // Register current position for future reference.
                resizer.lastPos = pos - y;
                if (!resizer.controlLine) {
                    resizer.controlLine = chart.renderer.path()
                        .addClass('highcharts-axis-resizer');
                }
                // Add to axisGroup after axis update, because the group is recreated
                // Do .add() before path is calculated because strokeWidth() needs it.
                resizer.controlLine.add(axis.axisGroup);
                lineWidth = chart.styledMode ?
                    resizer.controlLine.strokeWidth() :
                    options.lineWidth;
                attr.d = chart.renderer.crispLine([
                    ['M', axis.left + x, pos],
                    ['L', axis.left + axis.width + x, pos]
                ], lineWidth);
                resizer.controlLine.attr(attr);
            };
            /**
             * Set up the mouse and touch events for the control line.
             *
             * @function Highcharts.AxisResizer#addMouseEvents
             */
            AxisResizer.prototype.addMouseEvents = function () {
                var resizer = this,
                    ctrlLineElem = resizer.controlLine.element,
                    container = resizer.axis.chart.container,
                    eventsToUnbind = [],
                    mouseMoveHandler,
                    mouseUpHandler,
                    mouseDownHandler;
                // Create mouse events' handlers.
                // Make them as separate functions to enable wrapping them:
                resizer.mouseMoveHandler = mouseMoveHandler = function (e) {
                    resizer.onMouseMove(e);
                };
                resizer.mouseUpHandler = mouseUpHandler = function (e) {
                    resizer.onMouseUp(e);
                };
                resizer.mouseDownHandler = mouseDownHandler = function (e) {
                    resizer.onMouseDown(e);
                };
                // Add mouse move and mouseup events. These are bind to doc/container,
                // because resizer.grabbed flag is stored in mousedown events.
                eventsToUnbind.push(addEvent(container, 'mousemove', mouseMoveHandler), addEvent(container.ownerDocument, 'mouseup', mouseUpHandler), addEvent(ctrlLineElem, 'mousedown', mouseDownHandler));
                // Touch events.
                if (hasTouch) {
                    eventsToUnbind.push(addEvent(container, 'touchmove', mouseMoveHandler), addEvent(container.ownerDocument, 'touchend', mouseUpHandler), addEvent(ctrlLineElem, 'touchstart', mouseDownHandler));
                }
                resizer.eventsToUnbind = eventsToUnbind;
            };
            /**
             * Mouse move event based on x/y mouse position.
             *
             * @function Highcharts.AxisResizer#onMouseMove
             *
             * @param {Highcharts.PointerEventObject} e
             *        Mouse event.
             */
            AxisResizer.prototype.onMouseMove = function (e) {
                /*
                 * In iOS, a mousemove event with e.pageX === 0 is fired when holding
                 * the finger down in the center of the scrollbar. This should
                 * be ignored. Borrowed from Navigator.
                 */
                if (!e.touches || e.touches[0].pageX !== 0) {
                    // Drag the control line
                    if (this.grabbed) {
                        this.hasDragged = true;
                        this.updateAxes(this.axis.chart.pointer.normalize(e).chartY -
                            this.options.y);
                    }
                }
            };
            /**
             * Mouse up event based on x/y mouse position.
             *
             * @function Highcharts.AxisResizer#onMouseUp
             *
             * @param {Highcharts.PointerEventObject} e
             *        Mouse event.
             */
            AxisResizer.prototype.onMouseUp = function (e) {
                if (this.hasDragged) {
                    this.updateAxes(this.axis.chart.pointer.normalize(e).chartY -
                        this.options.y);
                }
                // Restore runPointActions.
                this.grabbed = this.hasDragged = this.axis.chart.activeResizer =
                    null;
            };
            /**
             * Mousedown on a control line.
             * Will store necessary information for drag&drop.
             *
             * @function Highcharts.AxisResizer#onMouseDown
             */
            AxisResizer.prototype.onMouseDown = function (e) {
                // Clear all hover effects.
                this.axis.chart.pointer.reset(false, 0);
                // Disable runPointActions.
                this.grabbed = this.axis.chart.activeResizer = true;
            };
            /**
             * Update all connected axes after a change of control line position
             *
             * @function Highcharts.AxisResizer#updateAxes
             *
             * @param {number} chartY
             */
            AxisResizer.prototype.updateAxes = function (chartY) {
                var resizer = this,
                    chart = resizer.axis.chart,
                    axes = resizer.options.controlledAxis,
                    nextAxes = axes.next.length === 0 ?
                        [chart.yAxis.indexOf(resizer.axis) + 1] : axes.next, 
                    // Main axis is included in the prev array by default
                    prevAxes = [resizer.axis].concat(axes.prev), 
                    // prev and next configs
                    axesConfigs = [],
                    stopDrag = false,
                    plotTop = chart.plotTop,
                    plotHeight = chart.plotHeight,
                    plotBottom = plotTop + plotHeight,
                    yDelta,
                    calculatePercent = function (value) {
                        return value * 100 / plotHeight + '%';
                }, normalize = function (val, min, max) {
                    return Math.round(clamp(val, min, max));
                };
                // Normalize chartY to plot area limits
                chartY = clamp(chartY, plotTop, plotBottom);
                yDelta = chartY - resizer.lastPos;
                // Update on changes of at least 1 pixel in the desired direction
                if (yDelta * yDelta < 1) {
                    return;
                }
                // First gather info how axes should behave
                [prevAxes, nextAxes].forEach(function (axesGroup, isNext) {
                    axesGroup.forEach(function (axisInfo, i) {
                        // Axes given as array index, axis object or axis id
                        var axis = isNumber(axisInfo) ?
                                // If it's a number - it's an index
                                chart.yAxis[axisInfo] :
                                (
                                // If it's first elem. in first group
                                (!isNext && !i) ?
                                    // then it's an Axis object
                                    axisInfo :
                                    // else it should be an id
                                    chart.get(axisInfo)),
                            axisOptions = axis && axis.options,
                            optionsToUpdate = {},
                            hDelta = 0,
                            height,
                            top,
                            minLength,
                            maxLength;
                        // Skip if axis is not found
                        // or it is navigator's yAxis (#7732)
                        if (!axisOptions ||
                            axisOptions.id === 'navigator-y-axis') {
                            return;
                        }
                        top = axis.top;
                        minLength = Math.round(relativeLength(axisOptions.minLength, plotHeight));
                        maxLength = Math.round(relativeLength(axisOptions.maxLength, plotHeight));
                        if (isNext) {
                            // Try to change height first. yDelta could had changed
                            yDelta = chartY - resizer.lastPos;
                            // Normalize height to option limits
                            height = normalize(axis.len - yDelta, minLength, maxLength);
                            // Adjust top, so the axis looks like shrinked from top
                            top = axis.top + yDelta;
                            // Check for plot area limits
                            if (top + height > plotBottom) {
                                hDelta = plotBottom - height - top;
                                chartY += hDelta;
                                top += hDelta;
                            }
                            // Fit to plot - when overflowing on top
                            if (top < plotTop) {
                                top = plotTop;
                                if (top + height > plotBottom) {
                                    height = plotHeight;
                                }
                            }
                            // If next axis meets min length, stop dragging:
                            if (height === minLength) {
                                stopDrag = true;
                            }
                            axesConfigs.push({
                                axis: axis,
                                options: {
                                    top: calculatePercent(top - plotTop),
                                    height: calculatePercent(height)
                                }
                            });
                        }
                        else {
                            // Normalize height to option limits
                            height = normalize(chartY - top, minLength, maxLength);
                            // If prev axis meets max length, stop dragging:
                            if (height === maxLength) {
                                stopDrag = true;
                            }
                            // Check axis size limits
                            chartY = top + height;
                            axesConfigs.push({
                                axis: axis,
                                options: {
                                    height: calculatePercent(height)
                                }
                            });
                        }
                        optionsToUpdate.height = height;
                    });
                });
                // If we hit the min/maxLength with dragging, don't do anything:
                if (!stopDrag) {
                    // Now update axes:
                    axesConfigs.forEach(function (config) {
                        config.axis.update(config.options, false);
                    });
                    chart.redraw(false);
                }
            };
            /**
             * Destroy AxisResizer. Clear outside references, clear events,
             * destroy elements, nullify properties.
             *
             * @function Highcharts.AxisResizer#destroy
             */
            AxisResizer.prototype.destroy = function () {
                var resizer = this,
                    axis = resizer.axis;
                // Clear resizer in axis
                delete axis.resizer;
                // Clear control line events
                if (this.eventsToUnbind) {
                    this.eventsToUnbind.forEach(function (unbind) {
                        unbind();
                    });
                }
                // Destroy AxisResizer elements
                resizer.controlLine.destroy();
                // Nullify properties
                objectEach(resizer, function (val, key) {
                    resizer[key] = null;
                });
            };
            // Default options for AxisResizer.
            AxisResizer.resizerOptions = {
                /**
                 * Minimal size of a resizable axis. Could be set as a percent
                 * of plot area or pixel size.
                 *
                 * @sample {highstock} stock/yaxis/resize-min-max-length
                 *         minLength and maxLength
                 *
                 * @type      {number|string}
                 * @product   highstock
                 * @requires  modules/drag-panes
                 * @apioption yAxis.minLength
                 */
                minLength: '10%',
                /**
                 * Maximal size of a resizable axis. Could be set as a percent
                 * of plot area or pixel size.
                 *
                 * @sample {highstock} stock/yaxis/resize-min-max-length
                 *         minLength and maxLength
                 *
                 * @type      {number|string}
                 * @product   highstock
                 * @requires  modules/drag-panes
                 * @apioption yAxis.maxLength
                 */
                maxLength: '100%',
                /**
                 * Options for axis resizing. It adds a thick line between panes which
                 * the user can drag in order to resize the panes.
                 *
                 * @sample {highstock} stock/demo/candlestick-and-volume
                 *         Axis resizing enabled
                 *
                 * @product      highstock
                 * @requires     modules/drag-panes
                 * @optionparent yAxis.resize
                 */
                resize: {
                    /**
                     * Contains two arrays of axes that are controlled by control line
                     * of the axis.
                     *
                     * @requires modules/drag-panes
                     */
                    controlledAxis: {
                        /**
                         * Array of axes that should move out of the way of resizing
                         * being done for the current axis. If not set, the next axis
                         * will be used.
                         *
                         * @sample {highstock} stock/yaxis/multiple-resizers
                         *         Three panes with resizers
                         * @sample {highstock} stock/yaxis/resize-multiple-axes
                         *         One resizer controlling multiple axes
                         *
                         * @type     {Array<number|string>}
                         * @default  []
                         * @requires modules/drag-panes
                         */
                        next: [],
                        /**
                         * Array of axes that should move with the current axis
                         * while resizing.
                         *
                         * @sample {highstock} stock/yaxis/multiple-resizers
                         *         Three panes with resizers
                         * @sample {highstock} stock/yaxis/resize-multiple-axes
                         *         One resizer controlling multiple axes
                         *
                         * @type     {Array<number|string>}
                         * @default  []
                         * @requires modules/drag-panes
                         */
                        prev: []
                    },
                    /**
                     * Enable or disable resize by drag for the axis.
                     *
                     * @sample {highstock} stock/demo/candlestick-and-volume
                     *         Enabled resizer
                     *
                     * @requires modules/drag-panes
                     */
                    enabled: false,
                    /**
                     * Cursor style for the control line.
                     *
                     * In styled mode use class `highcharts-axis-resizer` instead.
                     *
                     * @requires modules/drag-panes
                     */
                    cursor: 'ns-resize',
                    /**
                     * Color of the control line.
                     *
                     * In styled mode use class `highcharts-axis-resizer` instead.
                     *
                     * @sample {highstock} stock/yaxis/styled-resizer
                     *         Styled resizer
                     *
                     * @type     {Highcharts.ColorString}
                     * @requires modules/drag-panes
                     */
                    lineColor: "#cccccc" /* Palette.neutralColor20 */,
                    /**
                     * Dash style of the control line.
                     *
                     * In styled mode use class `highcharts-axis-resizer` instead.
                     *
                     * @see For supported options check [dashStyle](#plotOptions.series.dashStyle)
                     *
                     * @sample {highstock} stock/yaxis/styled-resizer
                     *         Styled resizer
                     *
                     * @requires modules/drag-panes
                     */
                    lineDashStyle: 'Solid',
                    /**
                     * Width of the control line.
                     *
                     * In styled mode use class `highcharts-axis-resizer` instead.
                     *
                     * @sample {highstock} stock/yaxis/styled-resizer
                     *         Styled resizer
                     *
                     * @requires modules/drag-panes
                     */
                    lineWidth: 4,
                    /**
                     * Horizontal offset of the control line.
                     *
                     * @sample {highstock} stock/yaxis/styled-resizer
                     *         Styled resizer
                     *
                     * @requires modules/drag-panes
                     */
                    x: 0,
                    /**
                     * Vertical offset of the control line.
                     *
                     * @sample {highstock} stock/yaxis/styled-resizer
                     *         Styled resizer
                     *
                     * @requires modules/drag-panes
                     */
                    y: 0
                }
            };
            return AxisResizer;
        }());
        // Keep resizer reference on axis update
        Axis.keepProps.push('resizer');
        /* eslint-disable no-invalid-this */
        // Add new AxisResizer, update or remove it
        addEvent(Axis, 'afterRender', function () {
            var axis = this,
                resizer = axis.resizer,
                resizerOptions = axis.options.resize,
                enabled;
            if (resizerOptions) {
                enabled = resizerOptions.enabled !== false;
                if (resizer) {
                    // Resizer present and enabled
                    if (enabled) {
                        // Update options
                        resizer.init(axis, true);
                        // Resizer present, but disabled
                    }
                    else {
                        // Destroy the resizer
                        resizer.destroy();
                    }
                }
                else {
                    // Resizer not present and enabled
                    if (enabled) {
                        // Add new resizer
                        axis.resizer = new AxisResizer(axis);
                    }
                    // Resizer not present and disabled, so do nothing
                }
            }
        });
        // Clear resizer on axis remove.
        addEvent(Axis, 'destroy', function (e) {
            if (!e.keepEvents && this.resizer) {
                this.resizer.destroy();
            }
        });
        // Prevent any hover effects while dragging a control line of AxisResizer.
        wrap(Pointer.prototype, 'runPointActions', function (proceed) {
            if (!this.chart.activeResizer) {
                proceed.apply(this, Array.prototype.slice.call(arguments, 1));
            }
        });
        // Prevent default drag action detection while dragging a control line of
        // AxisResizer. (#7563)
        wrap(Pointer.prototype, 'drag', function (proceed) {
            if (!this.chart.activeResizer) {
                proceed.apply(this, Array.prototype.slice.call(arguments, 1));
            }
        });
        merge(true, AxisDefaults.defaultYAxisOptions, AxisResizer.resizerOptions);
        H.AxisResizer = AxisResizer;

        return H.AxisResizer;
    });
    _registerModule(_modules, 'masters/modules/drag-panes.src.js', [], function () {


    });
}));