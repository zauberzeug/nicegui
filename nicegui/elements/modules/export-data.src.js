/**
 * @license Highcharts JS v10.3.2 (2022-11-28)
 *
 * Exporting module
 *
 * (c) 2010-2021 Torstein Honsi
 *
 * License: www.highcharts.com/license
 */
(function (factory) {
    if (typeof module === 'object' && module.exports) {
        factory['default'] = factory;
        module.exports = factory;
    } else if (typeof define === 'function' && define.amd) {
        define('highcharts/modules/export-data', ['highcharts', 'highcharts/modules/exporting'], function (Highcharts) {
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
    _registerModule(_modules, 'Extensions/ExportData/ExportDataDefaults.js', [], function () {
        /* *
         *
         *  Experimental data export module for Highcharts
         *
         *  (c) 2010-2021 Torstein Honsi
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
         * @optionparent exporting
         * @private
         */
        var exporting = {
                /**
                 * Caption for the data table. Same as chart title by default. Set to
                 * `false` to disable.
                 *
                 * @sample highcharts/export-data/multilevel-table
                 *         Multiple table headers
                 *
                 * @type      {boolean|string}
                 * @since     6.0.4
                 * @requires  modules/export-data
                 * @apioption exporting.tableCaption
                 */
                /**
                 * Options for exporting data to CSV or ExCel,
            or displaying the data
                 * in a HTML table or a JavaScript structure.
                 *
                 * This module adds data export options to the export menu and provides
                 * functions like `Chart.getCSV`,
            `Chart.getTable`,
            `Chart.getDataRows`
                 * and `Chart.viewData`.
                 *
                 * The XLS converter is limited and only creates a HTML string that is
                 * passed for download,
            which works but creates a warning before
                 * opening. The workaround for this is to use a third party XLSX
                 * converter,
            as demonstrated in the sample below.
                 *
                 * @sample  highcharts/export-data/categorized/ Categorized data
                 * @sample  highcharts/export-data/stock-timeaxis/ Highcharts Stock time axis
                 * @sample  highcharts/export-data/xlsx/
                 *          Using a third party XLSX converter
                 *
                 * @since    6.0.0
                 * @requires modules/export-data
                 */
                csv: {
                    /**
                     *
                     * Options for annotations in the export-data table.
                     *
                     * @since 8.2.0
                     * @requires modules/export-data
                     * @requires modules/annotations
                     *
                     *
                     */
                    annotations: {
                        /**
                        * The way to mark the separator for annotations
                        * combined in one export-data table cell.
                        *
                        * @since 8.2.0
                        * @requires modules/annotations
                        */
                        itemDelimiter: '; ',
                        /**
                        * When several labels are assigned to a specific point,
                        * they will be displayed in one field in the table.
                        *
                        * @sample highcharts/export-data/join-annotations/
                        *         Concatenate point annotations with itemDelimiter set.
                        *
                        * @since 8.2.0
                        * @requires modules/annotations
                        */
                        join: false
                    },
                    /**
                     * Formatter callback for the column headers. Parameters are:
                     * - `item` - The series or axis object)
                     * - `key` -  The point key,
            for example y or z
                     * - `keyLength` - The amount of value keys for this item,
            for
                     *   example a range series has the keys `low` and `high` so the
                     *   key length is 2.
                     *
                     * If [useMultiLevelHeaders](#exporting.useMultiLevelHeaders) is
                     * true,
            columnHeaderFormatter by default returns an object with
                     * columnTitle and topLevelColumnTitle for each key. Columns with
                     * the same topLevelColumnTitle have their titles merged into a
                     * single cell with colspan for table/Excel export.
                     *
                     * If `useMultiLevelHeaders` is false,
            or for CSV export,
            it returns
                     * the series name,
            followed by the key if there is more than one
                     * key.
                     *
                     * For the axis it returns the axis title or "Category" or
                     * "DateTime" by default.
                     *
                     * Return `false` to use Highcharts' proposed header.
                     *
                     * @sample highcharts/export-data/multilevel-table
                     *         Multiple table headers
                     *
                     * @type {Function|null}
                     */
                    columnHeaderFormatter: null,
                    /**
                     * Which date format to use for exported dates on a datetime X axis.
                     * See `Highcharts.dateFormat`.
                     */
                    dateFormat: '%Y-%m-%d %H:%M:%S',
                    /**
                     * Which decimal point to use for exported CSV. Defaults to the same
                     * as the browser locale,
            typically `.` (English) or `,
            ` (German,
                     * French etc).
                     *
                     * @type  {string|null}
                     * @since 6.0.4
                     */
                    decimalPoint: null,
                    /**
                     * The item delimiter in the exported data. Use `;` for direct
                     * exporting to Excel. Defaults to a best guess based on the browser
                     * locale. If the locale _decimal point_ is `,
            `,
            the `itemDelimiter`
                     * defaults to `;`,
            otherwise the `itemDelimiter` defaults to `,
            `.
                     *
                     * @type {string|null}
                     */
                    itemDelimiter: null,
                    /**
                     * The line delimiter in the exported data,
            defaults to a newline.
                     */
                    lineDelimiter: '\n'
                },
                /**
                 * Show a HTML table below the chart with the chart's current data.
                 *
                 * @sample highcharts/export-data/showtable/
                 *         Show the table
                 * @sample highcharts/studies/exporting-table-html
                 *         Experiment with putting the table inside the subtitle to
                 *         allow exporting it.
                 *
                 * @since    6.0.0
                 * @requires modules/export-data
                 */
                showTable: false,
                /**
                 * Use multi level headers in data table. If [csv.columnHeaderFormatter
                 * ](#exporting.csv.columnHeaderFormatter) is defined,
            it has to return
                 * objects in order for multi level headers to work.
                 *
                 * @sample highcharts/export-data/multilevel-table
                 *         Multiple table headers
                 *
                 * @since    6.0.4
                 * @requires modules/export-data
                 */
                useMultiLevelHeaders: true,
                /**
                 * If using multi level table headers,
            use rowspans for headers that
                 * have only one level.
                 *
                 * @sample highcharts/export-data/multilevel-table
                 *         Multiple table headers
                 *
                 * @since    6.0.4
                 * @requires modules/export-data
                 */
                useRowspanHeaders: true
            };
        /**
         * @optionparent lang
         * @private
         */
        var lang = {
                /**
                 * The text for the menu item.
                 *
                 * @since    6.0.0
                 * @requires modules/export-data
                 */
                downloadCSV: 'Download CSV',
                /**
                 * The text for the menu item.
                 *
                 * @since    6.0.0
                 * @requires modules/export-data
                 */
                downloadXLS: 'Download XLS',
                /**
                 * The text for exported table.
                 *
                 * @since 8.1.0
                 * @requires modules/export-data
                 */
                exportData: {
                    /**
                     * The annotation column title.
                     */
                    annotationHeader: 'Annotations',
                    /**
                     * The category column title.
                     */
                    categoryHeader: 'Category',
                    /**
                     * The category column title when axis type set to "datetime".
                     */
                    categoryDatetimeHeader: 'DateTime'
                },
                /**
                 * The text for the menu item.
                 *
                 * @since    6.0.0
                 * @requires modules/export-data
                 */
                viewData: 'View data table',
                /**
                 * The text for the menu item.
                 *
                 * @since 8.2.0
                 * @requires modules/export-data
                 */
                hideData: 'Hide data table'
            };
        /* *
         *
         *  Default Export
         *
         * */
        var ExportDataDefaults = {
                exporting: exporting,
                lang: lang
            };
        /* *
         *
         *  API Options
         *
         * */
        /**
         * Callback that fires while exporting data. This allows the modification of
         * data rows before processed into the final format.
         *
         * @type      {Highcharts.ExportDataCallbackFunction}
         * @context   Highcharts.Chart
         * @requires  modules/export-data
         * @apioption chart.events.exportData
         */
        /**
         * When set to `false` will prevent the series data from being included in
         * any form of data export.
         *
         * Since version 6.0.0 until 7.1.0 the option was existing undocumented
         * as `includeInCSVExport`.
         *
         * @type      {boolean}
         * @since     7.1.0
         * @requires  modules/export-data
         * @apioption plotOptions.series.includeInDataExport
         */
        (''); // keep doclets above in JS file

        return ExportDataDefaults;
    });
    _registerModule(_modules, 'Extensions/DownloadURL.js', [_modules['Core/Globals.js']], function (Highcharts) {
        /* *
         *
         *  (c) 2015-2021 Oystein Moseng
         *
         *  License: www.highcharts.com/license
         *
         *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
         *
         *  Mixin for downloading content in the browser
         *
         * */
        var isSafari = Highcharts.isSafari;
        var win = Highcharts.win,
            doc = win.document,
            domurl = win.URL || win.webkitURL || win;
        /**
         * Convert base64 dataURL to Blob if supported, otherwise returns undefined.
         * @private
         * @function Highcharts.dataURLtoBlob
         * @param {string} dataURL
         *        URL to convert
         * @return {string|undefined}
         *         Blob
         */
        var dataURLtoBlob = Highcharts.dataURLtoBlob = function (dataURL) {
                var parts = dataURL
                    .replace(/filename=.*;/, '')
                    .match(/data:([^;]*)(;base64)?,([0-9A-Za-z+/]+)/);
            if (parts &&
                parts.length > 3 &&
                (win.atob) &&
                win.ArrayBuffer &&
                win.Uint8Array &&
                win.Blob &&
                (domurl.createObjectURL)) {
                // Try to convert data URL to Blob
                var binStr = win.atob(parts[3]),
                    buf = new win.ArrayBuffer(binStr.length),
                    binary = new win.Uint8Array(buf);
                for (var i = 0; i < binary.length; ++i) {
                    binary[i] = binStr.charCodeAt(i);
                }
                var blob = new win.Blob([binary], { 'type': parts[1] });
                return domurl.createObjectURL(blob);
            }
        };
        /**
         * Download a data URL in the browser. Can also take a blob as first param.
         *
         * @private
         * @function Highcharts.downloadURL
         * @param {string|global.URL} dataURL
         *        The dataURL/Blob to download
         * @param {string} filename
         *        The name of the resulting file (w/extension)
         * @return {void}
         */
        var downloadURL = Highcharts.downloadURL = function (dataURL,
            filename) {
                var nav = win.navigator,
            a = doc.createElement('a');
            // IE specific blob implementation
            // Don't use for normal dataURLs
            if (typeof dataURL !== 'string' &&
                !(dataURL instanceof String) &&
                nav.msSaveOrOpenBlob) {
                nav.msSaveOrOpenBlob(dataURL, filename);
                return;
            }
            dataURL = "".concat(dataURL);
            // Some browsers have limitations for data URL lengths. Try to convert to
            // Blob or fall back. Edge always needs that blob.
            var isOldEdgeBrowser = /Edge\/\d+/.test(nav.userAgent);
            // Safari on iOS needs Blob in order to download PDF
            var safariBlob = (isSafari &&
                    typeof dataURL === 'string' &&
                    dataURL.indexOf('data:application/pdf') === 0);
            if (safariBlob || isOldEdgeBrowser || dataURL.length > 2000000) {
                dataURL = dataURLtoBlob(dataURL) || '';
                if (!dataURL) {
                    throw new Error('Failed to convert to blob');
                }
            }
            // Try HTML5 download attr if supported
            if (typeof a.download !== 'undefined') {
                a.href = dataURL;
                a.download = filename; // HTML5 download attribute
                doc.body.appendChild(a);
                a.click();
                doc.body.removeChild(a);
            }
            else {
                // No download attr, just opening data URI
                try {
                    var windowRef = win.open(dataURL, 'chart');
                    if (typeof windowRef === 'undefined' || windowRef === null) {
                        throw new Error('Failed to open window');
                    }
                }
                catch (e) {
                    // window.open failed, trying location.href
                    win.location.href = dataURL;
                }
            }
        };
        var DownloadURL = {
                dataURLtoBlob: dataURLtoBlob,
                downloadURL: downloadURL
            };

        return DownloadURL;
    });
    _registerModule(_modules, 'Extensions/ExportData/ExportData.js', [_modules['Core/Renderer/HTML/AST.js'], _modules['Extensions/ExportData/ExportDataDefaults.js'], _modules['Core/Globals.js'], _modules['Core/Defaults.js'], _modules['Extensions/DownloadURL.js'], _modules['Core/Series/SeriesRegistry.js'], _modules['Core/Utilities.js']], function (AST, ExportDataDefaults, H, D, DownloadURL, SeriesRegistry, U) {
        /* *
         *
         *  Experimental data export module for Highcharts
         *
         *  (c) 2010-2021 Torstein Honsi
         *
         *  License: www.highcharts.com/license
         *
         *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
         *
         * */
        // @todo
        // - Set up systematic tests for all series types, paired with tests of the data
        //   module importing the same data.
        var __spreadArray = (this && this.__spreadArray) || function (to,
            from,
            pack) {
                if (pack || arguments.length === 2) for (var i = 0,
            l = from.length,
            ar; i < l; i++) {
                    if (ar || !(i in from)) {
                        if (!ar) ar = Array.prototype.slice.call(from, 0,
            i);
                    ar[i] = from[i];
                }
            }
            return to.concat(ar || Array.prototype.slice.call(from));
        };
        var doc = H.doc,
            win = H.win;
        var getOptions = D.getOptions,
            setOptions = D.setOptions;
        var downloadURL = DownloadURL.downloadURL;
        var SeriesClass = SeriesRegistry.series,
            _a = SeriesRegistry.seriesTypes,
            AreaRangeSeries = _a.arearange,
            GanttSeries = _a.gantt,
            MapSeries = _a.map,
            MapBubbleSeries = _a.mapbubble,
            TreemapSeries = _a.treemap;
        var addEvent = U.addEvent,
            defined = U.defined,
            extend = U.extend,
            find = U.find,
            fireEvent = U.fireEvent,
            isNumber = U.isNumber,
            pick = U.pick;
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
         * Generates a data URL of CSV for local download in the browser. This is the
         * default action for a click on the 'Download CSV' button.
         *
         * See {@link Highcharts.Chart#getCSV} to get the CSV data itself.
         *
         * @function Highcharts.Chart#downloadCSV
         *
         * @requires modules/exporting
         */
        function chartDownloadCSV() {
            var csv = this.getCSV(true);
            downloadURL(getBlobFromContent(csv, 'text/csv') ||
                'data:text/csv,\uFEFF' + encodeURIComponent(csv), this.getFilename() + '.csv');
        }
        /**
         * Generates a data URL of an XLS document for local download in the browser.
         * This is the default action for a click on the 'Download XLS' button.
         *
         * See {@link Highcharts.Chart#getTable} to get the table data itself.
         *
         * @function Highcharts.Chart#downloadXLS
         *
         * @requires modules/exporting
         */
        function chartDownloadXLS() {
            var uri = 'data:application/vnd.ms-excel;base64,', template = '<html xmlns:o="urn:schemas-microsoft-com:office:office" ' +
                    'xmlns:x="urn:schemas-microsoft-com:office:excel" ' +
                    'xmlns="http://www.w3.org/TR/REC-html40">' +
                    '<head><!--[if gte mso 9]><xml><x:ExcelWorkbook>' +
                    '<x:ExcelWorksheets><x:ExcelWorksheet>' +
                    '<x:Name>Ark1</x:Name>' +
                    '<x:WorksheetOptions><x:DisplayGridlines/></x:WorksheetOptions>' +
                    '</x:ExcelWorksheet></x:ExcelWorksheets></x:ExcelWorkbook>' +
                    '</xml><![endif]-->' +
                    '<style>td{border:none;font-family: Calibri, sans-serif;} ' +
                    '.number{mso-number-format:"0.00";} ' +
                    '.text{ mso-number-format:"\@";}</style>' +
                    '<meta name=ProgId content=Excel.Sheet>' +
                    '<meta charset=UTF-8>' +
                    '</head><body>' +
                    this.getTable(true) +
                    '</body></html>', base64 = function (s) {
                    return win.btoa(unescape(encodeURIComponent(s))); // #50
                };
            downloadURL(getBlobFromContent(template, 'application/vnd.ms-excel') ||
                uri + base64(template), this.getFilename() + '.xls');
        }
        /**
         * Export-data module required. Returns the current chart data as a CSV string.
         *
         * @function Highcharts.Chart#getCSV
         *
         * @param {boolean} [useLocalDecimalPoint]
         *        Whether to use the local decimal point as detected from the browser.
         *        This makes it easier to export data to Excel in the same locale as the
         *        user is.
         *
         * @return {string}
         *         CSV representation of the data
         */
        function chartGetCSV(useLocalDecimalPoint) {
            var csv = '';
            var rows = this.getDataRows(), csvOptions = this.options.exporting.csv, decimalPoint = pick(csvOptions.decimalPoint, csvOptions.itemDelimiter !== ',' && useLocalDecimalPoint ?
                    (1.1).toLocaleString()[1] :
                    '.'), 
                // use ';' for direct to Excel
                itemDelimiter = pick(csvOptions.itemDelimiter, decimalPoint === ',' ? ';' : ','), 
                // '\n' isn't working with the js csv data extraction
                lineDelimiter = csvOptions.lineDelimiter;
            // Transform the rows to CSV
            rows.forEach(function (row, i) {
                var val = '',
                    j = row.length;
                while (j--) {
                    val = row[j];
                    if (typeof val === 'string') {
                        val = '"' + val + '"';
                    }
                    if (typeof val === 'number') {
                        if (decimalPoint !== '.') {
                            val = val.toString().replace('.', decimalPoint);
                        }
                    }
                    row[j] = val;
                }
                // The first row is the header - it defines the number of columns.
                // Empty columns between not-empty cells are covered in the getDataRows
                // method.
                // Now add empty values only to the end of the row so all rows have
                // the same number of columns, #17186
                row.length = rows.length ? rows[0].length : 0;
                // Add the values
                csv += row.join(itemDelimiter);
                // Add the line delimiter
                if (i < rows.length - 1) {
                    csv += lineDelimiter;
                }
            });
            return csv;
        }
        /**
         * Export-data module required. Returns a two-dimensional array containing the
         * current chart data.
         *
         * @function Highcharts.Chart#getDataRows
         *
         * @param {boolean} [multiLevelHeaders]
         *        Use multilevel headers for the rows by default. Adds an extra row with
         *        top level headers. If a custom columnHeaderFormatter is defined, this
         *        can override the behavior.
         *
         * @return {Array<Array<(number|string)>>}
         *         The current chart data
         *
         * @emits Highcharts.Chart#event:exportData
         */
        function chartGetDataRows(multiLevelHeaders) {
            var hasParallelCoords = this.hasParallelCoordinates,
                time = this.time,
                csvOptions = ((this.options.exporting && this.options.exporting.csv) || {}),
                xAxes = this.xAxis,
                rows = {},
                rowArr = [],
                topLevelColumnTitles = [],
                columnTitles = [],
                langOptions = this.options.lang,
                exportDataOptions = langOptions.exportData,
                categoryHeader = exportDataOptions.categoryHeader,
                categoryDatetimeHeader = exportDataOptions.categoryDatetimeHeader, 
                // Options
                columnHeaderFormatter = function (item,
                key,
                keyLength) {
                    if (csvOptions.columnHeaderFormatter) {
                        var s = csvOptions.columnHeaderFormatter(item,
                key,
                keyLength);
                    if (s !== false) {
                        return s;
                    }
                }
                if (!item) {
                    return categoryHeader;
                }
                if (!(item instanceof SeriesClass)) {
                    return (item.options.title && item.options.title.text) ||
                        (item.dateTime ? categoryDatetimeHeader : categoryHeader);
                }
                if (multiLevelHeaders) {
                    return {
                        columnTitle: keyLength > 1 ?
                            key :
                            item.name,
                        topLevelColumnTitle: item.name
                    };
                }
                return item.name + (keyLength > 1 ? ' (' + key + ')' : '');
            }, 
            // Map the categories for value axes
            getCategoryAndDateTimeMap = function (series, pointArrayMap, pIdx) {
                var categoryMap = {},
                    dateTimeValueAxisMap = {};
                pointArrayMap.forEach(function (prop) {
                    var axisName = ((series.keyToAxis && series.keyToAxis[prop]) ||
                            prop) + 'Axis', 
                        // Points in parallel coordinates refers to all yAxis
                        // not only `series.yAxis`
                        axis = isNumber(pIdx) ?
                            series.chart[axisName][pIdx] :
                            series[axisName];
                    categoryMap[prop] = (axis && axis.categories) || [];
                    dateTimeValueAxisMap[prop] = (axis && axis.dateTime);
                });
                return {
                    categoryMap: categoryMap,
                    dateTimeValueAxisMap: dateTimeValueAxisMap
                };
            }, 
            // Create point array depends if xAxis is category
            // or point.name is defined #13293
            getPointArray = function (series, xAxis) {
                var namedPoints = series.data.filter(function (d) {
                        return (typeof d.y !== 'undefined') && d.name;
                });
                if (namedPoints.length &&
                    xAxis &&
                    !xAxis.categories &&
                    !series.keyToAxis) {
                    if (series.pointArrayMap) {
                        var pointArrayMapCheck = series.pointArrayMap
                                .filter(function (p) { return p === 'x'; });
                        if (pointArrayMapCheck.length) {
                            series.pointArrayMap.unshift('x');
                            return series.pointArrayMap;
                        }
                    }
                    return ['x', 'y'];
                }
                return series.pointArrayMap || ['y'];
            }, xAxisIndices = [];
            var xAxis,
                dataRows,
                columnTitleObj,
                i = 0, // Loop the series and index values
                x,
                xTitle;
            this.series.forEach(function (series) {
                var keys = series.options.keys,
                    xAxis = series.xAxis,
                    pointArrayMap = keys || getPointArray(series,
                    xAxis),
                    valueCount = pointArrayMap.length,
                    xTaken = !series.requireSorting && {},
                    xAxisIndex = xAxes.indexOf(xAxis);
                var categoryAndDatetimeMap = getCategoryAndDateTimeMap(series,
                    pointArrayMap),
                    mockSeries,
                    j;
                if (series.options.includeInDataExport !== false &&
                    !series.options.isInternal &&
                    series.visible !== false // #55
                ) {
                    // Build a lookup for X axis index and the position of the first
                    // series that belongs to that X axis. Includes -1 for non-axis
                    // series types like pies.
                    if (!find(xAxisIndices, function (index) {
                        return index[0] === xAxisIndex;
                    })) {
                        xAxisIndices.push([xAxisIndex, i]);
                    }
                    // Compute the column headers and top level headers, usually the
                    // same as series names
                    j = 0;
                    while (j < valueCount) {
                        columnTitleObj = columnHeaderFormatter(series, pointArrayMap[j], pointArrayMap.length);
                        columnTitles.push(columnTitleObj.columnTitle || columnTitleObj);
                        if (multiLevelHeaders) {
                            topLevelColumnTitles.push(columnTitleObj.topLevelColumnTitle ||
                                columnTitleObj);
                        }
                        j++;
                    }
                    mockSeries = {
                        chart: series.chart,
                        autoIncrement: series.autoIncrement,
                        options: series.options,
                        pointArrayMap: series.pointArrayMap,
                        index: series.index
                    };
                    // Export directly from options.data because we need the uncropped
                    // data (#7913), and we need to support Boost (#7026).
                    series.options.data.forEach(function eachData(options, pIdx) {
                        var mockPoint = { series: mockSeries };
                        var key,
                            prop,
                            val;
                        // In parallel coordinates chart, each data point is connected
                        // to a separate yAxis, conform this
                        if (hasParallelCoords) {
                            categoryAndDatetimeMap = getCategoryAndDateTimeMap(series, pointArrayMap, pIdx);
                        }
                        series.pointClass.prototype.applyOptions.apply(mockPoint, [options]);
                        key = mockPoint.x;
                        if (defined(rows[key]) &&
                            rows[key].seriesIndices.includes(mockSeries.index)) {
                            // find keys, which belong to actual series
                            var keysFromActualSeries = Object.keys(rows).filter(function (i) {
                                    return rows[i].seriesIndices.includes(mockSeries.index) &&
                                        key;
                            }), 
                            // find all properties, which start with actual key
                            existingKeys = keysFromActualSeries
                                .filter(function (propertyName) {
                                return propertyName.indexOf(String(key)) === 0;
                            });
                            key = key.toString() + ',' + existingKeys.length;
                        }
                        var name = series.data[pIdx] && series.data[pIdx].name;
                        j = 0;
                        // Pies, funnels, geo maps etc. use point name in X row
                        if (!xAxis ||
                            series.exportKey === 'name' ||
                            (!hasParallelCoords && xAxis && xAxis.hasNames) && name) {
                            key = name;
                        }
                        if (xTaken) {
                            if (xTaken[key]) {
                                key += '|' + pIdx;
                            }
                            xTaken[key] = true;
                        }
                        if (!rows[key]) {
                            // Generate the row
                            rows[key] = [];
                            // Contain the X values from one or more X axes
                            rows[key].xValues = [];
                        }
                        rows[key].x = mockPoint.x;
                        rows[key].name = name;
                        rows[key].xValues[xAxisIndex] = mockPoint.x;
                        if (!defined(rows[key].seriesIndices)) {
                            rows[key].seriesIndices = [];
                        }
                        rows[key].seriesIndices = __spreadArray(__spreadArray([], rows[key].seriesIndices, true), [
                            mockSeries.index
                        ], false);
                        while (j < valueCount) {
                            prop = pointArrayMap[j]; // y, z etc
                            val = mockPoint[prop];
                            rows[key][i + j] = pick(
                            // Y axis category if present
                            categoryAndDatetimeMap.categoryMap[prop][val], 
                            // datetime yAxis
                            categoryAndDatetimeMap.dateTimeValueAxisMap[prop] ?
                                time.dateFormat(csvOptions.dateFormat, val) :
                                null, 
                            // linear/log yAxis
                            val);
                            j++;
                        }
                    });
                    i = i + j;
                }
            });
            // Make a sortable array
            for (x in rows) {
                if (Object.hasOwnProperty.call(rows, x)) {
                    rowArr.push(rows[x]);
                }
            }
            var xAxisIndex,
                column;
            // Add computed column headers and top level headers to final row set
            dataRows = multiLevelHeaders ? [topLevelColumnTitles, columnTitles] :
                [columnTitles];
            i = xAxisIndices.length;
            while (i--) { // Start from end to splice in
                xAxisIndex = xAxisIndices[i][0];
                column = xAxisIndices[i][1];
                xAxis = xAxes[xAxisIndex];
                // Sort it by X values
                rowArr.sort(function (// eslint-disable-line no-loop-func
                a, b) {
                    return a.xValues[xAxisIndex] - b.xValues[xAxisIndex];
                });
                // Add header row
                xTitle = columnHeaderFormatter(xAxis);
                dataRows[0].splice(column, 0, xTitle);
                if (multiLevelHeaders && dataRows[1]) {
                    // If using multi level headers, we just added top level header.
                    // Also add for sub level
                    dataRows[1].splice(column, 0, xTitle);
                }
                // Add the category column
                rowArr.forEach(function (// eslint-disable-line no-loop-func
                row) {
                    var category = row.name;
                    if (xAxis && !defined(category)) {
                        if (xAxis.dateTime) {
                            if (row.x instanceof Date) {
                                row.x = row.x.getTime();
                            }
                            category = time.dateFormat(csvOptions.dateFormat, row.x);
                        }
                        else if (xAxis.categories) {
                            category = pick(xAxis.names[row.x], xAxis.categories[row.x], row.x);
                        }
                        else {
                            category = row.x;
                        }
                    }
                    // Add the X/date/category
                    row.splice(column, 0, category);
                });
            }
            dataRows = dataRows.concat(rowArr);
            fireEvent(this, 'exportData', { dataRows: dataRows });
            return dataRows;
        }
        /**
         * Export-data module required. Build a HTML table with the chart's current
         * data.
         *
         * @sample highcharts/export-data/viewdata/
         *         View the data from the export menu
         *
         * @function Highcharts.Chart#getTable
         *
         * @param {boolean} [useLocalDecimalPoint]
         *        Whether to use the local decimal point as detected from the browser.
         *        This makes it easier to export data to Excel in the same locale as the
         *        user is.
         *
         * @return {string}
         *         HTML representation of the data.
         *
         * @emits Highcharts.Chart#event:afterGetTable
         */
        function chartGetTable(useLocalDecimalPoint) {
            var serialize = function (node) {
                    if (!node.tagName || node.tagName === '#text') {
                        // Text node
                        return node.textContent || '';
                }
                var attributes = node.attributes;
                var html = "<".concat(node.tagName);
                if (attributes) {
                    Object.keys(attributes)
                        .forEach(function (key) {
                        var value = attributes[key];
                        html += " ".concat(key, "=\"").concat(value, "\"");
                    });
                }
                html += '>';
                html += node.textContent || '';
                (node.children || []).forEach(function (child) {
                    html += serialize(child);
                });
                html += "</".concat(node.tagName, ">");
                return html;
            };
            var tree = this.getTableAST(useLocalDecimalPoint);
            return serialize(tree);
        }
        /**
         * Get the AST of a HTML table representing the chart data.
         *
         * @private
         *
         * @function Highcharts.Chart#getTableAST
         *
         * @param {boolean} [useLocalDecimalPoint]
         *        Whether to use the local decimal point as detected from the browser.
         *        This makes it easier to export data to Excel in the same locale as the
         *        user is.
         *
         * @return {Highcharts.ASTNode}
         *         The abstract syntax tree
         */
        function chartGetTableAST(useLocalDecimalPoint) {
            var rowLength = 0;
            var treeChildren = [];
            var options = this.options,
                decimalPoint = useLocalDecimalPoint ? (1.1).toLocaleString()[1] : '.',
                useMultiLevelHeaders = pick(options.exporting.useMultiLevelHeaders,
                true),
                rows = this.getDataRows(useMultiLevelHeaders),
                topHeaders = useMultiLevelHeaders ? rows.shift() : null,
                subHeaders = rows.shift(), 
                // Compare two rows for equality
                isRowEqual = function (row1,
                row2) {
                    var i = row1.length;
                if (row2.length === i) {
                    while (i--) {
                        if (row1[i] !== row2[i]) {
                            return false;
                        }
                    }
                }
                else {
                    return false;
                }
                return true;
            }, 
            // Get table cell HTML from value
            getCellHTMLFromValue = function (tagName, classes, attributes, value) {
                var textContent = pick(value, ''), className = 'highcharts-text' + (classes ? ' ' + classes : '');
                // Convert to string if number
                if (typeof textContent === 'number') {
                    textContent = textContent.toString();
                    if (decimalPoint === ',') {
                        textContent = textContent.replace('.', decimalPoint);
                    }
                    className = 'highcharts-number';
                }
                else if (!value) {
                    className = 'highcharts-empty';
                }
                attributes = extend({ 'class': className }, attributes);
                return {
                    tagName: tagName,
                    attributes: attributes,
                    textContent: textContent
                };
            }, 
            // Get table header markup from row data
            getTableHeaderHTML = function (topheaders, subheaders, rowLength) {
                var theadChildren = [];
                var i = 0,
                    len = rowLength || subheaders && subheaders.length,
                    next,
                    cur,
                    curColspan = 0,
                    rowspan;
                // Clean up multiple table headers. Chart.getDataRows() returns two
                // levels of headers when using multilevel, not merged. We need to
                // merge identical headers, remove redundant headers, and keep it
                // all marked up nicely.
                if (useMultiLevelHeaders &&
                    topheaders &&
                    subheaders &&
                    !isRowEqual(topheaders, subheaders)) {
                    var trChildren = [];
                    for (; i < len; ++i) {
                        cur = topheaders[i];
                        next = topheaders[i + 1];
                        if (cur === next) {
                            ++curColspan;
                        }
                        else if (curColspan) {
                            // Ended colspan
                            // Add cur to HTML with colspan.
                            trChildren.push(getCellHTMLFromValue('th', 'highcharts-table-topheading', {
                                scope: 'col',
                                colspan: curColspan + 1
                            }, cur));
                            curColspan = 0;
                        }
                        else {
                            // Cur is standalone. If it is same as sublevel,
                            // remove sublevel and add just toplevel.
                            if (cur === subheaders[i]) {
                                if (options.exporting.useRowspanHeaders) {
                                    rowspan = 2;
                                    delete subheaders[i];
                                }
                                else {
                                    rowspan = 1;
                                    subheaders[i] = '';
                                }
                            }
                            else {
                                rowspan = 1;
                            }
                            var cell = getCellHTMLFromValue('th', 'highcharts-table-topheading', { scope: 'col' }, cur);
                            if (rowspan > 1 && cell.attributes) {
                                cell.attributes.valign = 'top';
                                cell.attributes.rowspan = rowspan;
                            }
                            trChildren.push(cell);
                        }
                    }
                    theadChildren.push({
                        tagName: 'tr',
                        children: trChildren
                    });
                }
                // Add the subheaders (the only headers if not using multilevels)
                if (subheaders) {
                    var trChildren = [];
                    for (i = 0, len = subheaders.length; i < len; ++i) {
                        if (typeof subheaders[i] !== 'undefined') {
                            trChildren.push(getCellHTMLFromValue('th', null, { scope: 'col' }, subheaders[i]));
                        }
                    }
                    theadChildren.push({
                        tagName: 'tr',
                        children: trChildren
                    });
                }
                return {
                    tagName: 'thead',
                    children: theadChildren
                };
            };
            // Add table caption
            if (options.exporting.tableCaption !== false) {
                treeChildren.push({
                    tagName: 'caption',
                    attributes: {
                        'class': 'highcharts-table-caption'
                    },
                    textContent: pick(options.exporting.tableCaption, (options.title.text ?
                        options.title.text :
                        'Chart'))
                });
            }
            // Find longest row
            for (var i = 0, len = rows.length; i < len; ++i) {
                if (rows[i].length > rowLength) {
                    rowLength = rows[i].length;
                }
            }
            // Add header
            treeChildren.push(getTableHeaderHTML(topHeaders, subHeaders, Math.max(rowLength, subHeaders.length)));
            // Transform the rows to HTML
            var trs = [];
            rows.forEach(function (row) {
                var trChildren = [];
                for (var j = 0; j < rowLength; j++) {
                    // Make first column a header too. Especially important for
                    // category axes, but also might make sense for datetime? Should
                    // await user feedback on this.
                    trChildren.push(getCellHTMLFromValue(j ? 'td' : 'th', null, j ? {} : { scope: 'row' }, row[j]));
                }
                trs.push({
                    tagName: 'tr',
                    children: trChildren
                });
            });
            treeChildren.push({
                tagName: 'tbody',
                children: trs
            });
            var e = {
                    tree: {
                        tagName: 'table',
                        id: "highcharts-data-table-".concat(this.index),
                        children: treeChildren
                    }
                };
            fireEvent(this, 'aftergetTableAST', e);
            return e.tree;
        }
        /**
         * Export-data module required. Hide the data table when visible.
         *
         * @function Highcharts.Chart#hideData
         */
        function chartHideData() {
            this.toggleDataTable(false);
        }
        /**
         * @private
         */
        function chartToggleDataTable(show) {
            show = pick(show, !this.isDataTableVisible);
            // Create the div
            var createContainer = show && !this.dataTableDiv;
            if (createContainer) {
                this.dataTableDiv = doc.createElement('div');
                this.dataTableDiv.className = 'highcharts-data-table';
                // Insert after the chart container
                this.renderTo.parentNode.insertBefore(this.dataTableDiv, this.renderTo.nextSibling);
            }
            // Toggle the visibility
            if (this.dataTableDiv) {
                var style = this.dataTableDiv.style,
                    oldDisplay = style.display;
                style.display = show ? 'block' : 'none';
                // Generate the data table
                if (show) {
                    this.dataTableDiv.innerHTML = AST.emptyHTML;
                    var ast = new AST([this.getTableAST()]);
                    ast.addToDOM(this.dataTableDiv);
                    fireEvent(this, 'afterViewData', {
                        element: this.dataTableDiv,
                        wasHidden: createContainer || oldDisplay !== style.display
                    });
                }
            }
            // Set the flag
            this.isDataTableVisible = show;
            // Change the menu item text
            var exportDivElements = this.exportDivElements,
                options = this.options.exporting,
                menuItems = options &&
                    options.buttons &&
                    options.buttons.contextButton.menuItems,
                lang = this.options.lang;
            if (options &&
                options.menuItemDefinitions &&
                lang &&
                lang.viewData &&
                lang.hideData &&
                menuItems &&
                exportDivElements) {
                var exportDivElement = exportDivElements[menuItems.indexOf('viewData')];
                if (exportDivElement) {
                    AST.setElementHTML(exportDivElement, this.isDataTableVisible ? lang.hideData : lang.viewData);
                }
            }
        }
        /**
         * Export-data module required. View the data in a table below the chart.
         *
         * @function Highcharts.Chart#viewData
         *
         * @emits Highcharts.Chart#event:afterViewData
         */
        function chartViewData() {
            this.toggleDataTable(true);
        }
        /**
         * @private
         */
        function compose(ChartClass) {
            if (composedClasses.indexOf(ChartClass) === -1) {
                composedClasses.push(ChartClass);
                // Add an event listener to handle the showTable option
                addEvent(ChartClass, 'afterViewData', onChartAfterViewData);
                addEvent(ChartClass, 'render', onChartRenderer);
                var chartProto = ChartClass.prototype;
                chartProto.downloadCSV = chartDownloadCSV;
                chartProto.downloadXLS = chartDownloadXLS;
                chartProto.getCSV = chartGetCSV;
                chartProto.getDataRows = chartGetDataRows;
                chartProto.getTable = chartGetTable;
                chartProto.getTableAST = chartGetTableAST;
                chartProto.hideData = chartHideData;
                chartProto.toggleDataTable = chartToggleDataTable;
                chartProto.viewData = chartViewData;
            }
            if (composedClasses.indexOf(setOptions) === -1) {
                composedClasses.push(setOptions);
                var exportingOptions = getOptions().exporting;
                // Add "Download CSV" to the exporting menu.
                // @todo consider move to defaults
                if (exportingOptions) {
                    extend(exportingOptions.menuItemDefinitions, {
                        downloadCSV: {
                            textKey: 'downloadCSV',
                            onclick: function () {
                                this.downloadCSV();
                            }
                        },
                        downloadXLS: {
                            textKey: 'downloadXLS',
                            onclick: function () {
                                this.downloadXLS();
                            }
                        },
                        viewData: {
                            textKey: 'viewData',
                            onclick: function () {
                                this.toggleDataTable();
                            }
                        }
                    });
                    if (exportingOptions.buttons &&
                        exportingOptions.buttons.contextButton.menuItems) {
                        exportingOptions.buttons.contextButton.menuItems.push('separator', 'downloadCSV', 'downloadXLS', 'viewData');
                    }
                }
                setOptions(ExportDataDefaults);
            }
            if (AreaRangeSeries && composedClasses.indexOf(AreaRangeSeries) === -1) {
                composedClasses.push(AreaRangeSeries);
                AreaRangeSeries.prototype.keyToAxis = {
                    low: 'y',
                    high: 'y'
                };
            }
            if (GanttSeries && composedClasses.indexOf(GanttSeries) === -1) {
                composedClasses.push(GanttSeries);
                GanttSeries.prototype.keyToAxis = {
                    start: 'x',
                    end: 'x'
                };
            }
            if (MapSeries && composedClasses.indexOf(MapSeries) === -1) {
                composedClasses.push(MapSeries);
                MapSeries.prototype.exportKey = 'name';
            }
            if (MapBubbleSeries && composedClasses.indexOf(MapBubbleSeries) === -1) {
                composedClasses.push(MapBubbleSeries);
                MapBubbleSeries.prototype.exportKey = 'name';
            }
            if (TreemapSeries && composedClasses.indexOf(TreemapSeries) === -1) {
                composedClasses.push(TreemapSeries);
                TreemapSeries.prototype.exportKey = 'name';
            }
        }
        /**
         * Get a blob object from content, if blob is supported
         *
         * @private
         * @param {string} content
         *        The content to create the blob from.
         * @param {string} type
         *        The type of the content.
         * @return {string|undefined}
         *         The blob object, or undefined if not supported.
         */
        function getBlobFromContent(content, type) {
            var nav = win.navigator,
                webKit = (nav.userAgent.indexOf('WebKit') > -1 &&
                    nav.userAgent.indexOf('Chrome') < 0),
                domurl = win.URL || win.webkitURL || win;
            try {
                // MS specific
                if ((nav.msSaveOrOpenBlob) && win.MSBlobBuilder) {
                    var blob = new win.MSBlobBuilder();
                    blob.append(content);
                    return blob.getBlob('image/svg+xml');
                }
                // Safari requires data URI since it doesn't allow navigation to blob
                // URLs.
                if (!webKit) {
                    return domurl.createObjectURL(new win.Blob(['\uFEFF' + content], // #7084
                    { type: type }));
                }
            }
            catch (e) {
                // Ignore
            }
        }
        /**
         * @private
         */
        function onChartAfterViewData() {
            var chart = this,
                dataTableDiv = chart.dataTableDiv,
                row = document.querySelectorAll('thead')[0].querySelectorAll('tr')[0],
                getCellValue = function (tr,
                index) {
                    return tr.children[index].textContent;
            }, comparer = function (index, ascending) {
                return function (a, b) {
                    var sort = function (v1,
                        v2) { return (v1 !== '' && v2 !== '' && !isNaN(v1) && !isNaN(v2) ?
                            v1 - v2 :
                            v1.toString().localeCompare(v2)); };
                    return sort(getCellValue(ascending ? a : b, index), getCellValue(ascending ? b : a, index));
                };
            };
            if (dataTableDiv) {
                row.childNodes.forEach(function (th) {
                    var table = th.closest('table');
                    th.addEventListener('click', function () {
                        var rows = __spreadArray([],
                            dataTableDiv.querySelectorAll('tr:not(thead tr)'),
                            true),
                            headers = __spreadArray([],
                            th.parentNode.children,
                            true);
                        rows.sort(comparer(headers.indexOf(th), chart.ascendingOrderInTable =
                            !chart.ascendingOrderInTable)).forEach(function (tr) {
                            table.appendChild(tr);
                        });
                        headers.forEach(function (th) {
                            ['highcharts-sort-ascending', 'highcharts-sort-descending']
                                .forEach(function (className) {
                                if (th.classList.contains(className)) {
                                    th.classList.remove(className);
                                }
                            });
                        });
                        th.classList.add(chart.ascendingOrderInTable ?
                            'highcharts-sort-ascending' :
                            'highcharts-sort-descending');
                    });
                });
            }
        }
        /**
         * Handle the showTable option
         * @private
         */
        function onChartRenderer() {
            if (this.options &&
                this.options.exporting &&
                this.options.exporting.showTable &&
                !this.options.chart.forExport) {
                this.viewData();
            }
        }
        /* *
         *
         *  Default Export
         *
         * */
        var ExportData = {
                compose: compose
            };
        /* *
         *
         *  API Declarations
         *
         * */
        /**
         * Function callback to execute while data rows are processed for exporting.
         * This allows the modification of data rows before processed into the final
         * format.
         *
         * @callback Highcharts.ExportDataCallbackFunction
         * @extends Highcharts.EventCallbackFunction<Highcharts.Chart>
         *
         * @param {Highcharts.Chart} this
         * Chart context where the event occured.
         *
         * @param {Highcharts.ExportDataEventObject} event
         * Event object with data rows that can be modified.
         */
        /**
         * Contains information about the export data event.
         *
         * @interface Highcharts.ExportDataEventObject
         */ /**
        * Contains the data rows for the current export task and can be modified.
        * @name Highcharts.ExportDataEventObject#dataRows
        * @type {Array<Array<string>>}
        */
        (''); // keeps doclets above in JS file

        return ExportData;
    });
    _registerModule(_modules, 'masters/modules/export-data.src.js', [_modules['Core/Globals.js'], _modules['Extensions/ExportData/ExportData.js']], function (Highcharts, ExportData) {

        var G = Highcharts;
        ExportData.compose(G.Chart);

    });
}));