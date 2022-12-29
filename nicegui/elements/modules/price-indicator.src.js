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
        define('highcharts/modules/price-indicator', ['highcharts', 'highcharts/modules/stock'], function (Highcharts) {
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
    _registerModule(_modules, 'Extensions/PriceIndication.js', [_modules['Core/Series/Series.js'], _modules['Core/Utilities.js']], function (Series, U) {
        /**
         * (c) 2009-2021 Sebastian Bochann
         *
         * Price indicator for Highcharts
         *
         * License: www.highcharts.com/license
         *
         *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
         */
        var addEvent = U.addEvent,
            isArray = U.isArray,
            merge = U.merge;
        /**
         * The line marks the last price from visible range of points.
         *
         * @sample {highstock} stock/indicators/last-visible-price
         *         Last visible price
         *
         * @declare   Highcharts.SeriesLastVisiblePriceOptionsObject
         * @product   highstock
         * @requires  modules/price-indicator
         * @apioption plotOptions.series.lastVisiblePrice
         */
        /**
         * Enable or disable the indicator.
         *
         * @type      {boolean}
         * @product   highstock
         * @default   false
         * @apioption plotOptions.series.lastVisiblePrice.enabled
         */
        /**
         * @declare   Highcharts.SeriesLastVisiblePriceLabelOptionsObject
         * @extends   yAxis.crosshair.label
         * @since     7.0.0
         * @apioption plotOptions.series.lastVisiblePrice.label
         */
        /**
         * @since     7.0.0
         * @apioption plotOptions.series.lastVisiblePrice.label.align
         */
        /**
         * @since     7.0.0
         * @apioption plotOptions.series.lastVisiblePrice.label.backgroundColor
         */
        /**
         * The border color for the `lastVisiblePrice` label.
         *
         * @type      {Highcharts.ColorType}
         * @since     7.0.0
         * @product   highstock
         * @apioption plotOptions.series.lastVisiblePrice.label.borderColor
         */
        /**
         * The border corner radius of the `lastVisiblePrice` label.
         *
         * @type      {number}
         * @default   3
         * @since     7.0.0
         * @product   highstock
         * @apioption plotOptions.series.lastVisiblePrice.label.borderRadius
        */
        /**
         * Flag to enable `lastVisiblePrice` label.
         *
         *
         * @type      {boolean}
         * @default   false
         * @since     7.0
         * @product   highstock
         * @apioption plotOptions.series.lastVisiblePrice.label.enabled
         */
        /**
         * A format string for the `lastVisiblePrice` label. Defaults to `{value}` for
         * numeric axes and `{value:%b %d, %Y}` for datetime axes.
         *
         * @type      {string}
         * @since     7.0
         * @product   highstock
         * @apioption plotOptions.series.lastVisiblePrice.label.format
        */
        /**
         * @since     7.0.0
         * @apioption plotOptions.series.lastVisiblePrice.label.formatter
         */
        /**
         * @since     7.0.0
         * @apioption plotOptions.series.lastVisiblePrice.label.padding
         */
        /**
         * @since     7.0.0
         * @apioption plotOptions.series.lastVisiblePrice.label.shape
         */
        /**
         * Text styles for the `lastVisiblePrice` label.
         *
         * @type      {Highcharts.CSSObject}
         * @default   {"color": "white", "fontWeight": "normal", "fontSize": "11px", "textAlign": "center"}
         * @since     7.0
         * @product   highstock
         * @apioption plotOptions.series.lastVisiblePrice.label.style
         */
        /**
         * The border width for the `lastVisiblePrice` label.
         *
         * @type      {number}
         * @default   0
         * @since     7.0
         * @product   highstock
         * @apioption plotOptions.series.lastVisiblePrice.label.borderWidth
        */
        /**
         * Padding inside the `lastVisiblePrice` label.
         *
         * @type      {number}
         * @default   8
         * @since     7.0
         * @product   highstock
         * @apioption plotOptions.series.lastVisiblePrice.label.padding
         */
        /**
         * The line marks the last price from all points.
         *
         * @sample {highstock} stock/indicators/last-price
         *         Last price
         *
         * @declare   Highcharts.SeriesLastPriceOptionsObject
         * @product   highstock
         * @requires  modules/price-indicator
         * @apioption plotOptions.series.lastPrice
         */
        /**
         * Enable or disable the indicator.
         *
         * @type      {boolean}
         * @product   highstock
         * @default   false
         * @apioption plotOptions.series.lastPrice.enabled
         */
        /**
         * @declare   Highcharts.SeriesLastPriceLabelOptionsObject
         * @extends   yAxis.crosshair.label
         * @since     7.0.0
         * @apioption plotOptions.series.lastPrice.label
         */
        /**
         * @since     7.0.0
         * @apioption plotOptions.series.lastPrice.label.align
         * */
        /**
         * @since     7.0.0
         * @apioption plotOptions.series.lastPrice.label.backgroundColor
         * */
        /**
         * The border color of `lastPrice` label.
         * @since     7.0.0
         * @apioption plotOptions.series.lastPrice.label.borderColor
         * */
        /**
         * The border radius of `lastPrice` label.
         * @since     7.0.0
         * @apioption plotOptions.series.lastPrice.label.borderRadius
         * */
        /**
         * The border width of `lastPrice` label.
         * @since     7.0.0
         * @apioption plotOptions.series.lastPrice.label.borderWidth
         * */
        /**
         * Flag to enable `lastPrice` label.
         * @since     7.0.0
         * @apioption plotOptions.series.lastPrice.label.enabled
         * */
        /**
         * A format string for the `lastPrice` label. Defaults to `{value}` for
         * numeric axes and `{value:%b %d, %Y}` for datetime axes.
         *
         * @type      {string}
         * @since     7.0
         * @product   highstock
         * @apioption plotOptions.series.lastPrice.label.format
        */
        /**
         * @since     7.0.0
         * @apioption plotOptions.series.lastPrice.label.formatter
         */
        /**
         * @since     7.0.0
         * @apioption plotOptions.series.lastPrice.label.padding
         */
        /**
         * @since     7.0.0
         * @apioption plotOptions.series.lastPrice.label.shape
         */
        /**
         * Text styles for the `lastPrice` label.
         *
         * @type      {Highcharts.CSSObject}
         * @default   {"color": "white", "fontWeight": "normal", "fontSize": "11px", "textAlign": "center"}
         * @since     7.0
         * @product   highstock
         * @apioption plotOptions.series.lastPrice.label.style
         */
        /**
         * The border width for the `lastPrice` label.
         *
         * @type      {number}
         * @default   0
         * @since     7.0
         * @product   highstock
         * @apioption plotOptions.series.lastPrice.label.borderWidth
        */
        /**
         * Padding inside the `lastPrice` label.
         *
         * @type      {number}
         * @default   8
         * @since     7.0
         * @product   highstock
         * @apioption plotOptions.series.lastPrice.label.padding
         */
        /**
         * The color of the line of last price.
         * By default, the line has the same color as the series.
         *
         * @type      {string}
         * @product   highstock
         * @apioption plotOptions.series.lastPrice.color
         *
         */
        /* eslint-disable no-invalid-this */
        addEvent(Series, 'afterRender', function () {
            var series = this,
                seriesOptions = series.options,
                pointRange = seriesOptions.pointRange,
                lastVisiblePrice = seriesOptions.lastVisiblePrice,
                lastPrice = seriesOptions.lastPrice;
            if ((lastVisiblePrice || lastPrice) &&
                seriesOptions.id !== 'highcharts-navigator-series') {
                var xAxis = series.xAxis,
                    yAxis = series.yAxis,
                    origOptions = yAxis.crosshair,
                    origGraphic = yAxis.cross,
                    origLabel = yAxis.crossLabel,
                    points = series.points,
                    yLength = series.yData.length,
                    pLength = points.length,
                    x = series.xData[series.xData.length - 1],
                    y = series.yData[yLength - 1],
                    lastPoint = void 0,
                    yValue = void 0,
                    crop = void 0;
                if (lastPrice && lastPrice.enabled) {
                    yAxis.crosshair = yAxis.options.crosshair = seriesOptions.lastPrice;
                    if (!series.chart.styledMode &&
                        yAxis.crosshair &&
                        yAxis.options.crosshair &&
                        seriesOptions.lastPrice) {
                        // Set the default color from the series, #14888.
                        yAxis.crosshair.color = yAxis.options.crosshair.color =
                            seriesOptions.lastPrice.color || series.color;
                    }
                    yAxis.cross = series.lastPrice;
                    yValue = isArray(y) ? y[3] : y;
                    yAxis.drawCrosshair(null, ({
                        x: x,
                        y: yValue,
                        plotX: xAxis.toPixels(x, true),
                        plotY: yAxis.toPixels(yValue, true)
                    }));
                    // Save price
                    if (series.yAxis.cross) {
                        series.lastPrice = series.yAxis.cross;
                        series.lastPrice.addClass('highcharts-color-' + series.colorIndex); // #15222
                        series.lastPrice.y = yValue;
                    }
                }
                if (lastVisiblePrice && lastVisiblePrice.enabled && pLength > 0) {
                    crop = (points[pLength - 1].x === x) || pointRange === null ? 1 : 2;
                    yAxis.crosshair = yAxis.options.crosshair = merge({
                        color: 'transparent' // line invisible by default
                    }, seriesOptions.lastVisiblePrice);
                    yAxis.cross = series.lastVisiblePrice;
                    lastPoint = points[pLength - crop];
                    if (series.crossLabel) {
                        series.crossLabel.destroy();
                    }
                    // Set to undefined to avoid collision with
                    // the yAxis crosshair #11480
                    // Delete the crossLabel each time the code is invoked, #13876.
                    delete yAxis.crossLabel;
                    // Save price
                    yAxis.drawCrosshair(null, lastPoint);
                    if (yAxis.cross) {
                        series.lastVisiblePrice = yAxis.cross;
                        if (typeof lastPoint.y === 'number') {
                            series.lastVisiblePrice.y = lastPoint.y;
                        }
                    }
                    series.crossLabel = yAxis.crossLabel;
                }
                // Restore crosshair:
                yAxis.crosshair = yAxis.options.crosshair = origOptions;
                yAxis.cross = origGraphic;
                yAxis.crossLabel = origLabel;
            }
        });

    });
    _registerModule(_modules, 'masters/modules/price-indicator.src.js', [], function () {


    });
}));