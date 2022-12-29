/**
 * @license Highstock JS v10.3.2 (2022-11-28)
 *
 * Advanced Highcharts Stock tools
 *
 * (c) 2010-2021 Highsoft AS
 * Author: Torstein Honsi
 *
 * License: www.highcharts.com/license
 */
(function (factory) {
    if (typeof module === 'object' && module.exports) {
        factory['default'] = factory;
        module.exports = factory;
    } else if (typeof define === 'function' && define.amd) {
        define('highcharts/modules/full-screen', ['highcharts'], function (Highcharts) {
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
    _registerModule(_modules, 'Extensions/Exporting/Fullscreen.js', [_modules['Core/Renderer/HTML/AST.js'], _modules['Core/Utilities.js']], function (AST, U) {
        /* *
         *
         *  (c) 2009-2021 Rafal Sebestjanski
         *
         *  Full screen for Highcharts
         *
         *  License: www.highcharts.com/license
         *
         *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
         *
         * */
        /**
         * The module allows user to enable display chart in full screen mode.
         * Used in StockTools too.
         * Based on default solutions in browsers.
         */
        /* *
         *
         *  Imports
         *
         * */
        var addEvent = U.addEvent,
            fireEvent = U.fireEvent;
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
        function onChartBeforeRender() {
            /**
             * @name Highcharts.Chart#fullscreen
             * @type {Highcharts.Fullscreen}
             * @requires modules/full-screen
             */
            this.fullscreen = new Fullscreen(this);
        }
        /* *
         *
         *  Class
         *
         * */
        /**
         * Handles displaying chart's container in the fullscreen mode.
         *
         * **Note**: Fullscreen is not supported on iPhone due to iOS limitations.
         *
         * @class
         * @name Highcharts.Fullscreen
         *
         * @requires modules/exporting
         */
        var Fullscreen = /** @class */ (function () {
                /* *
                 *
                 *  Constructors
                 *
                 * */
                function Fullscreen(chart) {
                    /**
                     * Chart managed by the fullscreen controller.
                     * @name Highcharts.Fullscreen#chart
                     * @type {Highcharts.Chart}
                     */
                    this.chart = chart;
                /**
                 * The flag is set to `true` when the chart is displayed in
                 * the fullscreen mode.
                 *
                 * @name Highcharts.Fullscreen#isOpen
                 * @type {boolean|undefined}
                 * @since 8.0.1
                 */
                this.isOpen = false;
                var container = chart.renderTo;
                // Hold event and methods available only for a current browser.
                if (!this.browserProps) {
                    if (typeof container.requestFullscreen === 'function') {
                        this.browserProps = {
                            fullscreenChange: 'fullscreenchange',
                            requestFullscreen: 'requestFullscreen',
                            exitFullscreen: 'exitFullscreen'
                        };
                    }
                    else if (container.mozRequestFullScreen) {
                        this.browserProps = {
                            fullscreenChange: 'mozfullscreenchange',
                            requestFullscreen: 'mozRequestFullScreen',
                            exitFullscreen: 'mozCancelFullScreen'
                        };
                    }
                    else if (container.webkitRequestFullScreen) {
                        this.browserProps = {
                            fullscreenChange: 'webkitfullscreenchange',
                            requestFullscreen: 'webkitRequestFullScreen',
                            exitFullscreen: 'webkitExitFullscreen'
                        };
                    }
                    else if (container.msRequestFullscreen) {
                        this.browserProps = {
                            fullscreenChange: 'MSFullscreenChange',
                            requestFullscreen: 'msRequestFullscreen',
                            exitFullscreen: 'msExitFullscreen'
                        };
                    }
                }
            }
            /* *
             *
             *  Static Functions
             *
             * */
            /**
             * Prepares the chart class to support fullscreen.
             *
             * @param {typeof_Highcharts.Chart} ChartClass
             * The chart class to decorate with fullscreen support.
             */
            Fullscreen.compose = function (ChartClass) {
                if (composedClasses.indexOf(ChartClass) === -1) {
                    composedClasses.push(ChartClass);
                    // Initialize fullscreen
                    addEvent(ChartClass, 'beforeRender', onChartBeforeRender);
                }
            };
            /* *
             *
             *  Functions
             *
             * */
            /**
             * Stops displaying the chart in fullscreen mode.
             * Exporting module required.
             *
             * @since       8.0.1
             *
             * @function    Highcharts.Fullscreen#close
             * @return      {void}
             * @requires    modules/full-screen
             */
            Fullscreen.prototype.close = function () {
                var fullscreen = this,
                    chart = fullscreen.chart,
                    optionsChart = chart.options.chart;
                fireEvent(chart, 'fullscreenClose', null, function () {
                    // Don't fire exitFullscreen() when user exited
                    // using 'Escape' button.
                    if (fullscreen.isOpen &&
                        fullscreen.browserProps &&
                        chart.container.ownerDocument instanceof Document) {
                        chart.container.ownerDocument[fullscreen.browserProps.exitFullscreen]();
                    }
                    // Unbind event as it's necessary only before exiting
                    // from fullscreen.
                    if (fullscreen.unbindFullscreenEvent) {
                        fullscreen.unbindFullscreenEvent = fullscreen
                            .unbindFullscreenEvent();
                    }
                    chart.setSize(fullscreen.origWidth, fullscreen.origHeight, false);
                    fullscreen.origWidth = void 0;
                    fullscreen.origHeight = void 0;
                    optionsChart.width = fullscreen.origWidthOption;
                    optionsChart.height = fullscreen.origHeightOption;
                    fullscreen.origWidthOption = void 0;
                    fullscreen.origHeightOption = void 0;
                    fullscreen.isOpen = false;
                    fullscreen.setButtonText();
                });
            };
            /**
             * Displays the chart in fullscreen mode.
             * When fired customly by user before exporting context button is created,
             * button's text will not be replaced - it's on the user side.
             * Exporting module required.
             *
             * @since       8.0.1
             *
             * @function Highcharts.Fullscreen#open
             * @return      {void}
             * @requires    modules/full-screen
             */
            Fullscreen.prototype.open = function () {
                var fullscreen = this,
                    chart = fullscreen.chart,
                    optionsChart = chart.options.chart;
                fireEvent(chart, 'fullscreenOpen', null, function () {
                    if (optionsChart) {
                        fullscreen.origWidthOption = optionsChart.width;
                        fullscreen.origHeightOption = optionsChart.height;
                    }
                    fullscreen.origWidth = chart.chartWidth;
                    fullscreen.origHeight = chart.chartHeight;
                    // Handle exitFullscreen() method when user clicks 'Escape' button.
                    if (fullscreen.browserProps) {
                        var unbindChange_1 = addEvent(chart.container.ownerDocument, // chart's document
                            fullscreen.browserProps.fullscreenChange,
                            function () {
                                // Handle lack of async of browser's
                                // fullScreenChange event.
                                if (fullscreen.isOpen) {
                                    fullscreen.isOpen = false;
                                fullscreen.close();
                            }
                            else {
                                chart.setSize(null, null, false);
                                fullscreen.isOpen = true;
                                fullscreen.setButtonText();
                            }
                        });
                        var unbindDestroy_1 = addEvent(chart, 'destroy',
                            unbindChange_1);
                        fullscreen.unbindFullscreenEvent = function () {
                            unbindChange_1();
                            unbindDestroy_1();
                        };
                        var promise = chart.renderTo[fullscreen.browserProps.requestFullscreen]();
                        if (promise) {
                            // No dot notation because of IE8 compatibility
                            promise['catch'](function () {
                                alert(// eslint-disable-line no-alert
                                'Full screen is not supported inside a frame.');
                            });
                        }
                    }
                });
            };
            /**
             * Replaces the exporting context button's text when toogling the
             * fullscreen mode.
             *
             * @private
             *
             * @since 8.0.1
             *
             * @requires modules/full-screen
             */
            Fullscreen.prototype.setButtonText = function () {
                var chart = this.chart,
                    exportDivElements = chart.exportDivElements,
                    exportingOptions = chart.options.exporting,
                    menuItems = (exportingOptions &&
                        exportingOptions.buttons &&
                        exportingOptions.buttons.contextButton.menuItems),
                    lang = chart.options.lang;
                if (exportingOptions &&
                    exportingOptions.menuItemDefinitions &&
                    lang &&
                    lang.exitFullscreen &&
                    lang.viewFullscreen &&
                    menuItems &&
                    exportDivElements) {
                    var exportDivElement = exportDivElements[menuItems.indexOf('viewFullscreen')];
                    if (exportDivElement) {
                        AST.setElementHTML(exportDivElement, !this.isOpen ?
                            (exportingOptions.menuItemDefinitions.viewFullscreen
                                .text ||
                                lang.viewFullscreen) : lang.exitFullscreen);
                    }
                }
            };
            /**
             * Toggles displaying the chart in fullscreen mode.
             * By default, when the exporting module is enabled, a context button with
             * a drop down menu in the upper right corner accesses this function.
             * Exporting module required.
             *
             * @since 8.0.1
             *
             * @sample      highcharts/members/chart-togglefullscreen/
             *              Toggle fullscreen mode from a HTML button
             *
             * @function Highcharts.Fullscreen#toggle
             * @requires    modules/full-screen
             */
            Fullscreen.prototype.toggle = function () {
                var fullscreen = this;
                if (!fullscreen.isOpen) {
                    fullscreen.open();
                }
                else {
                    fullscreen.close();
                }
            };
            return Fullscreen;
        }());
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
         * Gets fired when closing the fullscreen
         *
         * @callback Highcharts.FullScreenfullscreenCloseCallbackFunction
         *
         * @param {Highcharts.Chart} chart
         *        The chart on which the event occured.
         *
         * @param {global.Event} event
         *        The event that occured.
         */
        /**
         * Gets fired when opening the fullscreen
         *
         * @callback Highcharts.FullScreenfullscreenOpenCallbackFunction
         *
         * @param {Highcharts.Chart} chart
         *        The chart on which the event occured.
         *
         * @param {global.Event} event
         *        The event that occured.
         */
        (''); // keeps doclets above separated from following code
        /* *
         *
         *  API Options
         *
         * */
        /**
         * Fires when a fullscreen is closed through the context menu item,
         * or a fullscreen is closed on the `Escape` button click,
         * or the `Chart.fullscreen.close` method.
         *
         * @sample highcharts/chart/events-fullscreen
         *         Title size change on fullscreen open
         *
         * @type      {Highcharts.FullScreenfullscreenCloseCallbackFunction}
         * @since     10.1.0
         * @context   Highcharts.Chart
         * @requires  modules/full-screen
         * @apioption chart.events.fullscreenClose
         */
        /**
         * Fires when a fullscreen is opened through the context menu item,
         * or the `Chart.fullscreen.open` method.
         *
         * @sample highcharts/chart/events-fullscreen
         *         Title size change on fullscreen open
         *
         * @type      {Highcharts.FullScreenfullscreenOpenCallbackFunction}
         * @since     10.1.0
         * @context   Highcharts.Chart
         * @requires  modules/full-screen
         * @apioption chart.events.fullscreenOpen
         */
        (''); // keeps doclets above in transpiled file

        return Fullscreen;
    });
    _registerModule(_modules, 'masters/modules/full-screen.src.js', [_modules['Core/Globals.js'], _modules['Extensions/Exporting/Fullscreen.js']], function (Highcharts, Fullscreen) {

        var G = Highcharts;
        G.Fullscreen = Fullscreen;
        Fullscreen.compose(G.Chart);

    });
}));