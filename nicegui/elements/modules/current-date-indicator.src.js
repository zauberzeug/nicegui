/**
 * @license Highcharts Gantt JS v10.3.2 (2022-11-28)
 *
 * CurrentDateIndicator
 *
 * (c) 2010-2021 Lars A. V. Cabrera
 *
 * License: www.highcharts.com/license
 */
(function (factory) {
    if (typeof module === 'object' && module.exports) {
        factory['default'] = factory;
        module.exports = factory;
    } else if (typeof define === 'function' && define.amd) {
        define('highcharts/modules/current-date-indicator', ['highcharts'], function (Highcharts) {
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
    _registerModule(_modules, 'Extensions/CurrentDateIndication.js', [_modules['Core/Axis/Axis.js'], _modules['Core/Axis/PlotLineOrBand/PlotLineOrBand.js'], _modules['Core/Utilities.js']], function (Axis, PlotLineOrBand, U) {
        /* *
         *
         *  (c) 2016-2021 Highsoft AS
         *
         *  Author: Lars A. V. Cabrera
         *
         *  License: www.highcharts.com/license
         *
         *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
         *
         * */
        var addEvent = U.addEvent,
            merge = U.merge,
            wrap = U.wrap;
        /**
         * Show an indicator on the axis for the current date and time. Can be a
         * boolean or a configuration object similar to
         * [xAxis.plotLines](#xAxis.plotLines).
         *
         * @sample gantt/current-date-indicator/demo
         *         Current date indicator enabled
         * @sample gantt/current-date-indicator/object-config
         *         Current date indicator with custom options
         *
         * @declare   Highcharts.CurrentDateIndicatorOptions
         * @type      {boolean|CurrentDateIndicatorOptions}
         * @default   true
         * @extends   xAxis.plotLines
         * @excluding value
         * @product   gantt
         * @apioption xAxis.currentDateIndicator
         */
        var defaultOptions = {
                color: "#ccd6eb" /* Palette.highlightColor20 */,
                width: 2,
                /**
                 * @declare Highcharts.AxisCurrentDateIndicatorLabelOptions
                 */
                label: {
                    /**
                     * Format of the label. This options is passed as the fist argument to
                     * [dateFormat](/class-reference/Highcharts.Time#dateFormat) function.
                     *
                     * @type      {string}
                     * @default   %a, %b %d %Y, %H:%M
                     * @product   gantt
                     * @apioption xAxis.currentDateIndicator.label.format
                     */
                    format: '%a, %b %d %Y, %H:%M',
                    formatter: function (value, format) {
                        return this.axis.chart.time.dateFormat(format || '', value);
                },
                rotation: 0,
                /**
                 * @type {Highcharts.CSSObject}
                 */
                style: {
                    /** @internal */
                    fontSize: '10px'
                }
            }
        };
        /* eslint-disable no-invalid-this */
        addEvent(Axis, 'afterSetOptions', function () {
            var options = this.options,
                cdiOptions = options.currentDateIndicator;
            if (cdiOptions) {
                var plotLineOptions = typeof cdiOptions === 'object' ?
                        merge(defaultOptions,
                    cdiOptions) :
                        merge(defaultOptions);
                plotLineOptions.value = Date.now();
                plotLineOptions.className = 'highcharts-current-date-indicator';
                if (!options.plotLines) {
                    options.plotLines = [];
                }
                options.plotLines.push(plotLineOptions);
            }
        });
        addEvent(PlotLineOrBand, 'render', function () {
            // If the label already exists, update its text
            if (this.label) {
                this.label.attr({
                    text: this.getLabelText(this.options.label)
                });
            }
        });
        wrap(PlotLineOrBand.prototype, 'getLabelText', function (defaultMethod, defaultLabelOptions) {
            var options = this.options;
            if (options &&
                options.className &&
                options.className.indexOf('highcharts-current-date-indicator') !== -1 &&
                options.label &&
                typeof options.label.formatter === 'function') {
                options.value = Date.now();
                return options.label.formatter
                    .call(this, options.value, options.label.format);
            }
            return defaultMethod.call(this, defaultLabelOptions);
        });

    });
    _registerModule(_modules, 'masters/modules/current-date-indicator.src.js', [], function () {


    });
}));