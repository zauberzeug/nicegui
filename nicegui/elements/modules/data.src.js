/**
 * @license Highcharts JS v10.3.2 (2022-11-28)
 *
 * Data module
 *
 * (c) 2012-2021 Torstein Honsi
 *
 * License: www.highcharts.com/license
 */
(function (factory) {
    if (typeof module === 'object' && module.exports) {
        factory['default'] = factory;
        module.exports = factory;
    } else if (typeof define === 'function' && define.amd) {
        define('highcharts/modules/data', ['highcharts'], function (Highcharts) {
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
    _registerModule(_modules, 'Core/HttpUtilities.js', [_modules['Core/Globals.js'], _modules['Core/Utilities.js']], function (G, U) {
        /* *
         *
         *  (c) 2010-2021 Christer Vasseng, Torstein Honsi
         *
         *  License: www.highcharts.com/license
         *
         *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
         *
         * */
        var doc = G.doc;
        var createElement = U.createElement,
            discardElement = U.discardElement,
            merge = U.merge,
            objectEach = U.objectEach;
        /* *
         *
         *  Functions
         *
         * */
        /**
         * Perform an Ajax call.
         *
         * @function Highcharts.ajax
         *
         * @param {Highcharts.AjaxSettingsObject} settings
         *        The Ajax settings to use.
         *
         * @return {false|undefined}
         *         Returns false, if error occured.
         */
        function ajax(settings) {
            var headers = {
                    json: 'application/json',
                    xml: 'application/xml',
                    text: 'text/plain',
                    octet: 'application/octet-stream'
                },
                r = new XMLHttpRequest();
            /**
             * Private error handler.
             * @private
             * @param {XMLHttpRequest} xhr
             * Internal request object.
             * @param {string|Error} err
             * Occured error.
             */
            function handleError(xhr, err) {
                if (settings.error) {
                    settings.error(xhr, err);
                }
                else {
                    // @todo Maybe emit a highcharts error event here
                }
            }
            if (!settings.url) {
                return false;
            }
            r.open((settings.type || 'get').toUpperCase(), settings.url, true);
            if (!settings.headers || !settings.headers['Content-Type']) {
                r.setRequestHeader('Content-Type', headers[settings.dataType || 'json'] || headers.text);
            }
            objectEach(settings.headers, function (val, key) {
                r.setRequestHeader(key, val);
            });
            if (settings.responseType) {
                r.responseType = settings.responseType;
            }
            // @todo lacking timeout handling
            r.onreadystatechange = function () {
                var res;
                if (r.readyState === 4) {
                    if (r.status === 200) {
                        if (settings.responseType !== 'blob') {
                            res = r.responseText;
                            if (settings.dataType === 'json') {
                                try {
                                    res = JSON.parse(res);
                                }
                                catch (e) {
                                    if (e instanceof Error) {
                                        return handleError(r, e);
                                    }
                                }
                            }
                        }
                        return settings.success && settings.success(res, r);
                    }
                    handleError(r, r.responseText);
                }
            };
            if (settings.data && typeof settings.data !== 'string') {
                settings.data = JSON.stringify(settings.data);
            }
            r.send(settings.data);
        }
        /**
         * Get a JSON resource over XHR, also supporting CORS without preflight.
         *
         * @function Highcharts.getJSON
         * @param {string} url
         *        The URL to load.
         * @param {Function} success
         *        The success callback. For error handling, use the `Highcharts.ajax`
         *        function instead.
         */
        function getJSON(url, success) {
            HttpUtilities.ajax({
                url: url,
                success: success,
                dataType: 'json',
                headers: {
                    // Override the Content-Type to avoid preflight problems with CORS
                    // in the Highcharts demos
                    'Content-Type': 'text/plain'
                }
            });
        }
        /**
         * The post utility
         *
         * @private
         * @function Highcharts.post
         *
         * @param {string} url
         * Post URL
         *
         * @param {Object} data
         * Post data
         *
         * @param {Highcharts.Dictionary<string>} [formAttributes]
         * Additional attributes for the post request
         */
        function post(url, data, formAttributes) {
            // create the form
            var form = createElement('form',
                merge({
                    method: 'post',
                    action: url,
                    enctype: 'multipart/form-data'
                },
                formAttributes), {
                    display: 'none'
                },
                doc.body);
            // add the data
            objectEach(data, function (val, name) {
                createElement('input', {
                    type: 'hidden',
                    name: name,
                    value: val
                }, void 0, form);
            });
            // submit
            form.submit();
            // clean up
            discardElement(form);
        }
        /* *
         *
         *  Default Export
         *
         * */
        var HttpUtilities = {
                ajax: ajax,
                getJSON: getJSON,
                post: post
            };
        /* *
         *
         *  API Declarations
         *
         * */
        /**
         * @interface Highcharts.AjaxSettingsObject
         */ /**
        * The payload to send.
        *
        * @name Highcharts.AjaxSettingsObject#data
        * @type {string|Highcharts.Dictionary<any>|undefined}
        */ /**
        * The data type expected.
        * @name Highcharts.AjaxSettingsObject#dataType
        * @type {"json"|"xml"|"text"|"octet"|undefined}
        */ /**
        * Function to call on error.
        * @name Highcharts.AjaxSettingsObject#error
        * @type {Function|undefined}
        */ /**
        * The headers; keyed on header name.
        * @name Highcharts.AjaxSettingsObject#headers
        * @type {Highcharts.Dictionary<string>|undefined}
        */ /**
        * Function to call on success.
        * @name Highcharts.AjaxSettingsObject#success
        * @type {Function|undefined}
        */ /**
        * The HTTP method to use. For example GET or POST.
        * @name Highcharts.AjaxSettingsObject#type
        * @type {string|undefined}
        */ /**
        * The URL to call.
        * @name Highcharts.AjaxSettingsObject#url
        * @type {string}
        */
        (''); // keeps doclets above in JS file

        return HttpUtilities;
    });
    _registerModule(_modules, 'Extensions/Data.js', [_modules['Core/Chart/Chart.js'], _modules['Core/Defaults.js'], _modules['Core/Globals.js'], _modules['Core/HttpUtilities.js'], _modules['Core/Series/Point.js'], _modules['Core/Series/SeriesRegistry.js'], _modules['Core/Utilities.js']], function (Chart, D, G, HU, Point, SeriesRegistry, U) {
        /* *
         *
         *  Data module
         *
         *  (c) 2012-2021 Torstein Honsi
         *
         *  License: www.highcharts.com/license
         *
         *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
         *
         * */
        var getOptions = D.getOptions;
        var doc = G.doc;
        var ajax = HU.ajax;
        var seriesTypes = SeriesRegistry.seriesTypes;
        var addEvent = U.addEvent,
            defined = U.defined,
            extend = U.extend,
            fireEvent = U.fireEvent,
            isNumber = U.isNumber,
            merge = U.merge,
            objectEach = U.objectEach,
            pick = U.pick,
            splat = U.splat;
        /* *
         *
         *  Functions
         *
         * */
        /**
         * @private
         */
        function getFreeIndexes(numberOfColumns, seriesBuilders) {
            var freeIndexes = [],
                freeIndexValues = [];
            var s,
                i,
                referencedIndexes;
            // Add all columns as free
            for (i = 0; i < numberOfColumns; i = i + 1) {
                freeIndexes.push(true);
            }
            // Loop all defined builders and remove their referenced columns
            for (s = 0; s < seriesBuilders.length; s = s + 1) {
                referencedIndexes = seriesBuilders[s].getReferencedColumnIndexes();
                for (i = 0; i < referencedIndexes.length; i = i + 1) {
                    freeIndexes[referencedIndexes[i]] = false;
                }
            }
            // Collect the values for the free indexes
            for (i = 0; i < freeIndexes.length; i = i + 1) {
                if (freeIndexes[i]) {
                    freeIndexValues.push(i);
                }
            }
            return freeIndexValues;
        }
        function hasURLOption(options) {
            return Boolean(options &&
                (options.rowsURL || options.csvURL || options.columnsURL));
        }
        /* *
         *
         *  Class
         *
         * */
        /**
         * The Data class
         *
         * @requires module:modules/data
         *
         * @class
         * @name Highcharts.Data
         *
         * @param {Highcharts.DataOptions} dataOptions
         *
         * @param {Highcharts.Options} [chartOptions]
         *
         * @param {Highcharts.Chart} [chart]
         */
        var Data = /** @class */ (function () {
                /* *
                 *
                 *  Constructors
                 *
                 * */
                function Data(dataOptions, chartOptions, chart) {
                    if (chartOptions === void 0) { chartOptions = {}; }
                    this.rowsToColumns = Data.rowsToColumns; // backwards compatibility
                    /**
                     * A collection of available date formats, extendable from the outside to
                     * support custom date formats.
                     *
                     * @name Highcharts.Data#dateFormats
                     * @type {Highcharts.Dictionary<Highcharts.DataDateFormatObject>}
                     */
                    this.dateFormats = {
                        'YYYY/mm/dd': {
                            regex: /^([0-9]{4})[\-\/\.]([0-9]{1,2})[\-\/\.]([0-9]{1,2})$/,
                            parser: function (match) {
                                return (match ?
                                    Date.UTC(+match[1], match[2] - 1, +match[3]) :
                                    NaN);
                        }
                    },
                    'dd/mm/YYYY': {
                        regex: /^([0-9]{1,2})[\-\/\.]([0-9]{1,2})[\-\/\.]([0-9]{4})$/,
                        parser: function (match) {
                            return (match ?
                                Date.UTC(+match[3], match[2] - 1, +match[1]) :
                                NaN);
                        },
                        alternative: 'mm/dd/YYYY' // different format with the same regex
                    },
                    'mm/dd/YYYY': {
                        regex: /^([0-9]{1,2})[\-\/\.]([0-9]{1,2})[\-\/\.]([0-9]{4})$/,
                        parser: function (match) {
                            return (match ?
                                Date.UTC(+match[3], match[1] - 1, +match[2]) :
                                NaN);
                        }
                    },
                    'dd/mm/YY': {
                        regex: /^([0-9]{1,2})[\-\/\.]([0-9]{1,2})[\-\/\.]([0-9]{2})$/,
                        parser: function (match) {
                            if (!match) {
                                return NaN;
                            }
                            var d = new Date();
                            var year = +match[3];
                            if (year > (d.getFullYear() - 2000)) {
                                year += 1900;
                            }
                            else {
                                year += 2000;
                            }
                            return Date.UTC(year, match[2] - 1, +match[1]);
                        },
                        alternative: 'mm/dd/YY' // different format with the same regex
                    },
                    'mm/dd/YY': {
                        regex: /^([0-9]{1,2})[\-\/\.]([0-9]{1,2})[\-\/\.]([0-9]{2})$/,
                        parser: function (match) {
                            return (match ?
                                Date.UTC(+match[3] + 2000, match[1] - 1, +match[2]) :
                                NaN);
                        }
                    }
                };
                this.chart = chart;
                this.chartOptions = chartOptions;
                this.options = dataOptions;
                this.rawColumns = [];
                this.init(dataOptions, chartOptions, chart);
            }
            /* *
             *
             *  Static Properties
             *
             * */
            /**
             * Creates a data object to parse data for a chart.
             *
             * @function Highcharts.data
             */
            Data.data = function (dataOptions, chartOptions, chart) {
                if (chartOptions === void 0) { chartOptions = {}; }
                return new Data(dataOptions, chartOptions, chart);
            };
            /**
             * Reorganize rows into columns.
             *
             * @function Highcharts.Data.rowsToColumns
             */
            Data.rowsToColumns = function (rows) {
                var row,
                    rowsLength,
                    col,
                    colsLength,
                    columns;
                if (rows) {
                    columns = [];
                    rowsLength = rows.length;
                    for (row = 0; row < rowsLength; row++) {
                        colsLength = rows[row].length;
                        for (col = 0; col < colsLength; col++) {
                            if (!columns[col]) {
                                columns[col] = [];
                            }
                            columns[col][row] = rows[row][col];
                        }
                    }
                }
                return columns;
            };
            /* *
             *
             *  Functions
             *
             * */
            /**
             * Initialize the Data object with the given options
             *
             * @private
             * @function Highcharts.Data#init
             */
            Data.prototype.init = function (dataOptions, chartOptions, chart) {
                var decimalPoint = dataOptions.decimalPoint,
                    hasData;
                if (chartOptions) {
                    this.chartOptions = chartOptions;
                }
                if (chart) {
                    this.chart = chart;
                }
                if (decimalPoint !== '.' && decimalPoint !== ',') {
                    decimalPoint = void 0;
                }
                this.options = dataOptions;
                this.columns = (dataOptions.columns ||
                    this.rowsToColumns(dataOptions.rows) ||
                    []);
                this.firstRowAsNames = pick(dataOptions.firstRowAsNames, this.firstRowAsNames, true);
                this.decimalRegex = (decimalPoint &&
                    new RegExp('^(-?[0-9]+)' + decimalPoint + '([0-9]+)$'));
                // Always stop old polling when we have new options
                if (this.liveDataTimeout !== void 0) {
                    clearTimeout(this.liveDataTimeout);
                }
                // This is a two-dimensional array holding the raw, trimmed string
                // values with the same organisation as the columns array. It makes it
                // possible for example to revert from interpreted timestamps to
                // string-based categories.
                this.rawColumns = [];
                // No need to parse or interpret anything
                if (this.columns.length) {
                    this.dataFound();
                    hasData = !hasURLOption(dataOptions);
                }
                if (!hasData) {
                    // Fetch live data
                    hasData = this.fetchLiveData();
                }
                if (!hasData) {
                    // Parse a CSV string if options.csv is given. The parseCSV function
                    // returns a columns array, if it has no length, we have no data
                    hasData = Boolean(this.parseCSV().length);
                }
                if (!hasData) {
                    // Parse a HTML table if options.table is given
                    hasData = Boolean(this.parseTable().length);
                }
                if (!hasData) {
                    // Parse a Google Spreadsheet
                    hasData = this.parseGoogleSpreadsheet();
                }
                if (!hasData && dataOptions.afterComplete) {
                    dataOptions.afterComplete();
                }
            };
            /**
             * Get the column distribution. For example, a line series takes a single
             * column for Y values. A range series takes two columns for low and high
             * values respectively, and an OHLC series takes four columns.
             *
             * @function Highcharts.Data#getColumnDistribution
             */
            Data.prototype.getColumnDistribution = function () {
                var chartOptions = this.chartOptions,
                    options = this.options,
                    xColumns = [],
                    getValueCount = function (type) {
                        return (seriesTypes[type || 'line'].prototype.pointArrayMap || [0]).length;
                }, getPointArrayMap = function (type) {
                    return seriesTypes[type || 'line'].prototype.pointArrayMap;
                }, globalType = (chartOptions &&
                    chartOptions.chart &&
                    chartOptions.chart.type), individualCounts = [], seriesBuilders = [], 
                // If no series mapping is defined, check if the series array is
                // defined with types.
                seriesMapping = ((options && options.seriesMapping) ||
                    (chartOptions &&
                        chartOptions.series &&
                        chartOptions.series.map(function () {
                            return { x: 0 };
                        })) ||
                    []);
                var seriesIndex = 0,
                    i;
                ((chartOptions && chartOptions.series) || []).forEach(function (series) {
                    individualCounts.push(getValueCount(series.type || globalType));
                });
                // Collect the x-column indexes from seriesMapping
                seriesMapping.forEach(function (mapping) {
                    xColumns.push(mapping.x || 0);
                });
                // If there are no defined series with x-columns, use the first column
                // as x column
                if (xColumns.length === 0) {
                    xColumns.push(0);
                }
                // Loop all seriesMappings and constructs SeriesBuilders from
                // the mapping options.
                seriesMapping.forEach(function (mapping) {
                    var builder = new SeriesBuilder(),
                        numberOfValueColumnsNeeded = individualCounts[seriesIndex] ||
                            getValueCount(globalType),
                        seriesArr = (chartOptions && chartOptions.series) || [],
                        series = seriesArr[seriesIndex] || {},
                        defaultPointArrayMap = getPointArrayMap(series.type || globalType),
                        pointArrayMap = defaultPointArrayMap || ['y'];
                    if (
                    // User-defined x.mapping
                    defined(mapping.x) ||
                        // All non cartesian don't need 'x'
                        series.isCartesian ||
                        // Except pie series:
                        !defaultPointArrayMap) {
                        // Add an x reader from the x property or from an undefined
                        // column if the property is not set. It will then be auto
                        // populated later.
                        builder.addColumnReader(mapping.x, 'x');
                    }
                    // Add all column mappings
                    objectEach(mapping, function (val, name) {
                        if (name !== 'x') {
                            builder.addColumnReader(val, name);
                        }
                    });
                    // Add missing columns
                    for (i = 0; i < numberOfValueColumnsNeeded; i++) {
                        if (!builder.hasReader(pointArrayMap[i])) {
                            // Create and add a column reader for the next free column
                            // index
                            builder.addColumnReader(void 0, pointArrayMap[i]);
                        }
                    }
                    seriesBuilders.push(builder);
                    seriesIndex++;
                });
                var globalPointArrayMap = getPointArrayMap(globalType);
                if (typeof globalPointArrayMap === 'undefined') {
                    globalPointArrayMap = ['y'];
                }
                this.valueCount = {
                    global: getValueCount(globalType),
                    xColumns: xColumns,
                    individual: individualCounts,
                    seriesBuilders: seriesBuilders,
                    globalPointArrayMap: globalPointArrayMap
                };
            };
            /**
             * When the data is parsed into columns, either by CSV, table, GS or direct
             * input, continue with other operations.
             *
             * @private
             * @function Highcharts.Data#dataFound
             */
            Data.prototype.dataFound = function () {
                if (this.options.switchRowsAndColumns) {
                    this.columns = this.rowsToColumns(this.columns);
                }
                // Interpret the info about series and columns
                this.getColumnDistribution();
                // Interpret the values into right types
                this.parseTypes();
                // Handle columns if a handleColumns callback is given
                if (this.parsed() !== false) {
                    // Complete if a complete callback is given
                    this.complete();
                }
            };
            /**
             * Parse a CSV input string
             *
             * @function Highcharts.Data#parseCSV
             */
            Data.prototype.parseCSV = function (inOptions) {
                var self = this, columns = this.columns = [], options = inOptions || this.options, startColumn = (typeof options.startColumn !== 'undefined' &&
                        options.startColumn) ? options.startColumn : 0, endColumn = options.endColumn || Number.MAX_VALUE, dataTypes = [], 
                    // We count potential delimiters in the prepass, and use the
                    // result as the basis of half-intelligent guesses.
                    potDelimiters = {
                        ',': 0,
                        ';': 0,
                        '\t': 0
                    };
                var csv = options.csv,
                    startRow = (typeof options.startRow !== 'undefined' && options.startRow ?
                        options.startRow :
                        0),
                    endRow = options.endRow || Number.MAX_VALUE,
                    itemDelimiter,
                    lines, 
                    // activeRowNo = 0,
                    rowIt = 0;
                /*
                    This implementation is quite verbose. It will be shortened once
                    it's stable and passes all the test.

                    It's also not written with speed in mind, instead everything is
                    very seggregated, and there a several redundant loops.
                    This is to make it easier to stabilize the code initially.

                    We do a pre-pass on the first 4 rows to make some intelligent
                    guesses on the set. Guessed delimiters are in this pass counted.

                    Auto detecting delimiters
                        - If we meet a quoted string, the next symbol afterwards
                          (that's not \s, \t) is the delimiter
                        - If we meet a date, the next symbol afterwards is the delimiter

                    Date formats
                        - If we meet a column with date formats, check all of them to
                          see if one of the potential months crossing 12. If it does,
                          we now know the format

                    It would make things easier to guess the delimiter before
                    doing the actual parsing.

                    General rules:
                        - Quoting is allowed, e.g: "Col 1",123,321
                        - Quoting is optional, e.g.: Col1,123,321
                        - Doubble quoting is escaping, e.g. "Col ""Hello world""",123
                        - Spaces are considered part of the data: Col1 ,123
                        - New line is always the row delimiter
                        - Potential column delimiters are , ; \t
                        - First row may optionally contain headers
                        - The last row may or may not have a row delimiter
                        - Comments are optionally supported, in which case the comment
                          must start at the first column, and the rest of the line will
                          be ignored
                */
                /**
                 * Parse a single row.
                 * @private
                 */
                function parseRow(columnStr, rowNumber, noAdd, callbacks) {
                    var i = 0, c = '', cl = '', cn = '', token = '', actualColumn = 0, column = 0;
                    /**
                     * @private
                     */
                    function read(j) {
                        c = columnStr[j];
                        cl = columnStr[j - 1];
                        cn = columnStr[j + 1];
                    }
                    /**
                     * @private
                     */
                    function pushType(type) {
                        if (dataTypes.length < column + 1) {
                            dataTypes.push([type]);
                        }
                        if (dataTypes[column][dataTypes[column].length - 1] !== type) {
                            dataTypes[column].push(type);
                        }
                    }
                    /**
                     * @private
                     */
                    function push() {
                        if (startColumn > actualColumn || actualColumn > endColumn) {
                            // Skip this column, but increment the column count (#7272)
                            ++actualColumn;
                            token = '';
                            return;
                        }
                        if (!isNaN(parseFloat(token)) && isFinite(token)) {
                            token = parseFloat(token);
                            pushType('number');
                        }
                        else if (!isNaN(Date.parse(token))) {
                            token = token.replace(/\//g, '-');
                            pushType('date');
                        }
                        else {
                            pushType('string');
                        }
                        if (columns.length < column + 1) {
                            columns.push([]);
                        }
                        if (!noAdd) {
                            // Don't push - if there's a varrying amount of columns
                            // for each row, pushing will skew everything down n slots
                            columns[column][rowNumber] = token;
                        }
                        token = '';
                        ++column;
                        ++actualColumn;
                    }
                    if (!columnStr.trim().length) {
                        return;
                    }
                    if (columnStr.trim()[0] === '#') {
                        return;
                    }
                    for (; i < columnStr.length; i++) {
                        read(i);
                        if (c === '"') {
                            read(++i);
                            while (i < columnStr.length) {
                                if (c === '"' && cl !== '"' && cn !== '"') {
                                    break;
                                }
                                if (c !== '"' || (c === '"' && cl !== '"')) {
                                    token += c;
                                }
                                read(++i);
                            }
                            // Perform "plugin" handling
                        }
                        else if (callbacks && callbacks[c]) {
                            if (callbacks[c](c, token)) {
                                push();
                            }
                            // Delimiter - push current token
                        }
                        else if (c === itemDelimiter) {
                            push();
                            // Actual column data
                        }
                        else {
                            token += c;
                        }
                    }
                    push();
                }
                /**
                 * Attempt to guess the delimiter. We do a separate parse pass here
                 * because we need to count potential delimiters softly without making
                 * any assumptions.
                 * @private
                 */
                function guessDelimiter(lines) {
                    var points = 0,
                        commas = 0,
                        guessed = false;
                    lines.some(function (columnStr, i) {
                        var inStr = false,
                            c,
                            cn,
                            cl,
                            token = '';
                        // We should be able to detect dateformats within 13 rows
                        if (i > 13) {
                            return true;
                        }
                        for (var j = 0; j < columnStr.length; j++) {
                            c = columnStr[j];
                            cn = columnStr[j + 1];
                            cl = columnStr[j - 1];
                            if (c === '#') {
                                // Skip the rest of the line - it's a comment
                                return;
                            }
                            if (c === '"') {
                                if (inStr) {
                                    if (cl !== '"' && cn !== '"') {
                                        while (cn === ' ' && j < columnStr.length) {
                                            cn = columnStr[++j];
                                        }
                                        // After parsing a string, the next non-blank
                                        // should be a delimiter if the CSV is properly
                                        // formed.
                                        if (typeof potDelimiters[cn] !== 'undefined') {
                                            potDelimiters[cn]++;
                                        }
                                        inStr = false;
                                    }
                                }
                                else {
                                    inStr = true;
                                }
                            }
                            else if (typeof potDelimiters[c] !== 'undefined') {
                                token = token.trim();
                                if (!isNaN(Date.parse(token))) {
                                    potDelimiters[c]++;
                                }
                                else if (isNaN(token) ||
                                    !isFinite(token)) {
                                    potDelimiters[c]++;
                                }
                                token = '';
                            }
                            else {
                                token += c;
                            }
                            if (c === ',') {
                                commas++;
                            }
                            if (c === '.') {
                                points++;
                            }
                        }
                    });
                    // Count the potential delimiters.
                    // This could be improved by checking if the number of delimiters
                    // equals the number of columns - 1
                    if (potDelimiters[';'] > potDelimiters[',']) {
                        guessed = ';';
                    }
                    else if (potDelimiters[','] > potDelimiters[';']) {
                        guessed = ',';
                    }
                    else {
                        // No good guess could be made..
                        guessed = ',';
                    }
                    // Try to deduce the decimal point if it's not explicitly set.
                    // If both commas or points is > 0 there is likely an issue
                    if (!options.decimalPoint) {
                        if (points > commas) {
                            options.decimalPoint = '.';
                        }
                        else {
                            options.decimalPoint = ',';
                        }
                        // Apply a new decimal regex based on the presumed decimal sep.
                        self.decimalRegex = new RegExp('^(-?[0-9]+)' +
                            options.decimalPoint +
                            '([0-9]+)$');
                    }
                    return guessed;
                }
                /**
                 * Tries to guess the date format
                 *  - Check if either month candidate exceeds 12
                 *  - Check if year is missing (use current year)
                 *  - Check if a shortened year format is used (e.g. 1/1/99)
                 *  - If no guess can be made, the user must be prompted
                 * data is the data to deduce a format based on
                 * @private
                 */
                function deduceDateFormat(data, limit) {
                    var format = 'YYYY/mm/dd',
                        stable = [],
                        max = [];
                    var thing,
                        guessedFormat = [],
                        calculatedFormat,
                        i = 0,
                        madeDeduction = false, 
                        // candidates = {},
                        j;
                    if (!limit || limit > data.length) {
                        limit = data.length;
                    }
                    for (; i < limit; i++) {
                        if (typeof data[i] !== 'undefined' &&
                            data[i] && data[i].length) {
                            thing = data[i]
                                .trim()
                                .replace(/\//g, ' ')
                                .replace(/\-/g, ' ')
                                .replace(/\./g, ' ')
                                .split(' ');
                            guessedFormat = [
                                '',
                                '',
                                ''
                            ];
                            for (j = 0; j < thing.length; j++) {
                                if (j < guessedFormat.length) {
                                    thing[j] = parseInt(thing[j], 10);
                                    if (thing[j]) {
                                        max[j] = (!max[j] || max[j] < thing[j]) ?
                                            thing[j] :
                                            max[j];
                                        if (typeof stable[j] !== 'undefined') {
                                            if (stable[j] !== thing[j]) {
                                                stable[j] = false;
                                            }
                                        }
                                        else {
                                            stable[j] = thing[j];
                                        }
                                        if (thing[j] > 31) {
                                            if (thing[j] < 100) {
                                                guessedFormat[j] = 'YY';
                                            }
                                            else {
                                                guessedFormat[j] = 'YYYY';
                                            }
                                            // madeDeduction = true;
                                        }
                                        else if (thing[j] > 12 &&
                                            thing[j] <= 31) {
                                            guessedFormat[j] = 'dd';
                                            madeDeduction = true;
                                        }
                                        else if (!guessedFormat[j].length) {
                                            guessedFormat[j] = 'mm';
                                        }
                                    }
                                }
                            }
                        }
                    }
                    if (madeDeduction) {
                        // This handles a few edge cases with hard to guess dates
                        for (j = 0; j < stable.length; j++) {
                            if (stable[j] !== false) {
                                if (max[j] > 12 &&
                                    guessedFormat[j] !== 'YY' &&
                                    guessedFormat[j] !== 'YYYY') {
                                    guessedFormat[j] = 'YY';
                                }
                            }
                            else if (max[j] > 12 && guessedFormat[j] === 'mm') {
                                guessedFormat[j] = 'dd';
                            }
                        }
                        // If the middle one is dd, and the last one is dd,
                        // the last should likely be year.
                        if (guessedFormat.length === 3 &&
                            guessedFormat[1] === 'dd' &&
                            guessedFormat[2] === 'dd') {
                            guessedFormat[2] = 'YY';
                        }
                        calculatedFormat = guessedFormat.join('/');
                        // If the caculated format is not valid, we need to present an
                        // error.
                        if (!(options.dateFormats || self.dateFormats)[calculatedFormat]) {
                            // This should emit an event instead
                            fireEvent('deduceDateFailed');
                            return format;
                        }
                        return calculatedFormat;
                    }
                    return format;
                }
                /**
                 * @todo
                 * Figure out the best axis types for the data
                 * - If the first column is a number, we're good
                 * - If the first column is a date, set to date/time
                 * - If the first column is a string, set to categories
                 * @private
                 */
                function deduceAxisTypes() {
                }
                if (csv && options.beforeParse) {
                    csv = options.beforeParse.call(this, csv);
                }
                if (csv) {
                    lines = csv
                        .replace(/\r\n/g, '\n') // Unix
                        .replace(/\r/g, '\n') // Mac
                        .split(options.lineDelimiter || '\n');
                    if (!startRow || startRow < 0) {
                        startRow = 0;
                    }
                    if (!endRow || endRow >= lines.length) {
                        endRow = lines.length - 1;
                    }
                    if (options.itemDelimiter) {
                        itemDelimiter = options.itemDelimiter;
                    }
                    else {
                        itemDelimiter = null;
                        itemDelimiter = guessDelimiter(lines);
                    }
                    var offset = 0;
                    for (rowIt = startRow; rowIt <= endRow; rowIt++) {
                        if (lines[rowIt][0] === '#') {
                            offset++;
                        }
                        else {
                            parseRow(lines[rowIt], rowIt - startRow - offset);
                        }
                    }
                    // //Make sure that there's header columns for everything
                    // columns.forEach(function (col) {
                    // });
                    deduceAxisTypes();
                    if ((!options.columnTypes || options.columnTypes.length === 0) &&
                        dataTypes.length &&
                        dataTypes[0].length &&
                        dataTypes[0][1] === 'date' &&
                        !options.dateFormat) {
                        options.dateFormat = deduceDateFormat(columns[0]);
                    }
                    // lines.forEach(function (line, rowNo) {
                    //    let trimmed = self.trim(line),
                    //        isComment = trimmed.indexOf('#') === 0,
                    //        isBlank = trimmed === '',
                    //        items;
                    //    if (
                    //        rowNo >= startRow &&
                    //        rowNo <= endRow &&
                    //        !isComment && !isBlank
                    //    ) {
                    //        items = line.split(itemDelimiter);
                    //        items.forEach(function (item, colNo) {
                    //            if (colNo >= startColumn && colNo <= endColumn) {
                    //                if (!columns[colNo - startColumn]) {
                    //                    columns[colNo - startColumn] = [];
                    //                }
                    //                columns[colNo - startColumn][activeRowNo] = item;
                    //            }
                    //        });
                    //        activeRowNo += 1;
                    //    }
                    // });
                    //
                    this.dataFound();
                }
                return columns;
            };
            /**
             * Parse a HTML table
             *
             * @function Highcharts.Data#parseTable
             */
            Data.prototype.parseTable = function () {
                var options = this.options,
                    columns = this.columns || [],
                    startRow = options.startRow || 0,
                    endRow = options.endRow || Number.MAX_VALUE,
                    startColumn = options.startColumn || 0,
                    endColumn = options.endColumn || Number.MAX_VALUE;
                if (options.table) {
                    var table = options.table;
                    if (typeof table === 'string') {
                        table = doc.getElementById(table);
                    }
                    [].forEach.call(table.getElementsByTagName('tr'), function (tr, rowNo) {
                        if (rowNo >= startRow && rowNo <= endRow) {
                            [].forEach.call(tr.children, function (item, colNo) {
                                var row = columns[colNo - startColumn];
                                var i = 1;
                                if ((item.tagName === 'TD' ||
                                    item.tagName === 'TH') &&
                                    colNo >= startColumn &&
                                    colNo <= endColumn) {
                                    if (!columns[colNo - startColumn]) {
                                        columns[colNo - startColumn] = [];
                                    }
                                    columns[colNo - startColumn][rowNo - startRow] = item.innerHTML;
                                    // Loop over all previous indices and make sure
                                    // they are nulls, not undefined.
                                    while (rowNo - startRow >= i &&
                                        row[rowNo - startRow - i] === void 0) {
                                        row[rowNo - startRow - i] = null;
                                        i++;
                                    }
                                }
                            });
                        }
                    });
                    this.dataFound(); // continue
                }
                return columns;
            };
            /**
             * Fetch or refetch live data
             *
             * @function Highcharts.Data#fetchLiveData
             *
             * @return {boolean}
             *         The URLs that were tried can be found in the options
             */
            Data.prototype.fetchLiveData = function () {
                var data = this,
                    chart = this.chart,
                    options = this.options,
                    maxRetries = 3,
                    pollingEnabled = options.enablePolling,
                    originalOptions = merge(options);
                var currentRetries = 0,
                    updateIntervalMs = (options.dataRefreshRate || 2) * 1000;
                if (!hasURLOption(options)) {
                    return false;
                }
                // Do not allow polling more than once a second
                if (updateIntervalMs < 1000) {
                    updateIntervalMs = 1000;
                }
                delete options.csvURL;
                delete options.rowsURL;
                delete options.columnsURL;
                /**
                 * @private
                 */
                function performFetch(initialFetch) {
                    /**
                     * Helper function for doing the data fetch + polling.
                     * @private
                     */
                    function request(url, done, tp) {
                        if (!url ||
                            !/^(http|\/|\.\/|\.\.\/)/.test(url)) {
                            if (url && options.error) {
                                options.error('Invalid URL');
                            }
                            return false;
                        }
                        if (initialFetch) {
                            clearTimeout(data.liveDataTimeout);
                            chart.liveDataURL = url;
                        }
                        /**
                         * @private
                         */
                        function poll() {
                            // Poll
                            if (pollingEnabled && chart.liveDataURL === url) {
                                // We need to stop doing this if the URL has changed
                                data.liveDataTimeout =
                                    setTimeout(performFetch, updateIntervalMs);
                            }
                        }
                        ajax({
                            url: url,
                            dataType: tp || 'json',
                            success: function (res) {
                                if (chart && chart.series) {
                                    done(res);
                                }
                                poll();
                            },
                            error: function (xhr, text) {
                                if (++currentRetries < maxRetries) {
                                    poll();
                                }
                                return options.error && options.error(text, xhr);
                            }
                        });
                        return true;
                    }
                    if (!request(originalOptions.csvURL, function (res) {
                        chart.update({
                            data: {
                                csv: res
                            }
                        });
                    }, 'text')) {
                        if (!request(originalOptions.rowsURL, function (res) {
                            chart.update({
                                data: {
                                    rows: res
                                }
                            });
                        })) {
                            request(originalOptions.columnsURL, function (res) {
                                chart.update({
                                    data: {
                                        columns: res
                                    }
                                });
                            });
                        }
                    }
                }
                performFetch(true);
                return hasURLOption(options);
            };
            /**
             * Parse a Google spreadsheet.
             *
             * @function Highcharts.Data#parseGoogleSpreadsheet
             *
             * @return {boolean}
             *         Always returns false, because it is an intermediate fetch.
             */
            Data.prototype.parseGoogleSpreadsheet = function () {
                var data = this,
                    options = this.options,
                    googleSpreadsheetKey = options.googleSpreadsheetKey,
                    chart = this.chart,
                    refreshRate = Math.max((options.dataRefreshRate || 2) * 1000, 4000);
                /**
                 * Form the `values` field after range settings, unless the
                 * googleSpreadsheetRange option is set.
                 */
                var getRange = function () {
                        if (options.googleSpreadsheetRange) {
                            return options.googleSpreadsheetRange;
                    }
                    var alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
                    var start = (alphabet.charAt(options.startColumn || 0) || 'A') +
                            ((options.startRow || 0) + 1);
                    var end = alphabet.charAt(pick(options.endColumn, -1)) || 'ZZ';
                    if (defined(options.endRow)) {
                        end += options.endRow + 1;
                    }
                    return "" + start + ":".concat(end);
                };
                /**
                 * Fetch the actual spreadsheet using XMLHttpRequest.
                 * @private
                 */
                function fetchSheet(fn) {
                    var url = [
                            'https://sheets.googleapis.com/v4/spreadsheets',
                            googleSpreadsheetKey,
                            'values',
                            getRange(),
                            '?alt=json&' +
                                'majorDimension=COLUMNS&' +
                                'valueRenderOption=UNFORMATTED_VALUE&' +
                                'dateTimeRenderOption=FORMATTED_STRING&' +
                                'key=' + options.googleAPIKey
                        ].join('/');
                    ajax({
                        url: url,
                        dataType: 'json',
                        success: function (json) {
                            fn(json);
                            if (options.enablePolling) {
                                data.liveDataTimeout = setTimeout(function () {
                                    fetchSheet(fn);
                                }, refreshRate);
                            }
                        },
                        error: function (xhr, text) {
                            return options.error && options.error(text, xhr);
                        }
                    });
                }
                if (googleSpreadsheetKey) {
                    delete options.googleSpreadsheetKey;
                    fetchSheet(function (json) {
                        // Prepare the data from the spreadsheat
                        var columns = json.values;
                        if (!columns || columns.length === 0) {
                            return false;
                        }
                        // Find the maximum row count in order to extend shorter columns
                        var rowCount = columns.reduce(function (rowCount,
                            column) { return Math.max(rowCount,
                            column.length); }, 0);
                        // Insert null for empty spreadsheet cells (#5298)
                        columns.forEach(function (column) {
                            for (var i = 0; i < rowCount; i++) {
                                if (typeof column[i] === 'undefined') {
                                    column[i] = null;
                                }
                            }
                        });
                        if (chart && chart.series) {
                            chart.update({
                                data: {
                                    columns: columns
                                }
                            });
                        }
                        else { // #8245
                            data.columns = columns;
                            data.dataFound();
                        }
                    });
                }
                // This is an intermediate fetch, so always return false.
                return false;
            };
            /**
             * Trim a string from whitespaces.
             *
             * @function Highcharts.Data#trim
             *
             * @param {string} str
             *        String to trim
             *
             * @param {boolean} [inside=false]
             *        Remove all spaces between numbers.
             *
             * @return {string}
             *         Trimed string
             */
            Data.prototype.trim = function (str, inside) {
                if (typeof str === 'string') {
                    str = str.replace(/^\s+|\s+$/g, '');
                    // Clear white space insdie the string, like thousands separators
                    if (inside && /^[0-9\s]+$/.test(str)) {
                        str = str.replace(/\s/g, '');
                    }
                    if (this.decimalRegex) {
                        str = str.replace(this.decimalRegex, '$1.$2');
                    }
                }
                return str;
            };
            /**
             * Parse numeric cells in to number types and date types in to true dates.
             *
             * @function Highcharts.Data#parseTypes
             */
            Data.prototype.parseTypes = function () {
                var columns = this.columns || [];
                var col = columns.length;
                while (col--) {
                    this.parseColumn(columns[col], col);
                }
            };
            /**
             * Parse a single column. Set properties like .isDatetime and .isNumeric.
             *
             * @function Highcharts.Data#parseColumn
             *
             * @param {Array<Highcharts.DataValueType>} column
             *        Column to parse
             *
             * @param {number} col
             *        Column index
             */
            Data.prototype.parseColumn = function (column, col) {
                var rawColumns = this.rawColumns,
                    columns = this.columns,
                    firstRowAsNames = this.firstRowAsNames,
                    isXColumn = this.valueCount.xColumns.indexOf(col) !== -1,
                    backup = [],
                    chartOptions = this.chartOptions,
                    columnTypes = this.options.columnTypes || [],
                    columnType = columnTypes[col],
                    forceCategory = isXColumn && ((chartOptions &&
                        chartOptions.xAxis &&
                        splat(chartOptions.xAxis)[0].type === 'category') || columnType === 'string'),
                    columnHasName = defined(column.name);
                var row = column.length,
                    val,
                    floatVal,
                    trimVal,
                    trimInsideVal,
                    dateVal,
                    diff,
                    descending;
                if (!rawColumns[col]) {
                    rawColumns[col] = [];
                }
                while (row--) {
                    val = backup[row] || column[row];
                    trimVal = this.trim(val);
                    trimInsideVal = this.trim(val, true);
                    floatVal = parseFloat(trimInsideVal);
                    // Set it the first time
                    if (typeof rawColumns[col][row] === 'undefined') {
                        rawColumns[col][row] = trimVal;
                    }
                    // Disable number or date parsing by setting the X axis type to
                    // category
                    if (forceCategory ||
                        (row === 0 && firstRowAsNames && !columnHasName)) {
                        column[row] = '' + trimVal;
                    }
                    else if (+trimInsideVal === floatVal) { // is numeric
                        column[row] = floatVal;
                        // If the number is greater than milliseconds in a year, assume
                        // datetime
                        if (floatVal > 365 * 24 * 3600 * 1000 &&
                            columnType !== 'float') {
                            column.isDatetime = true;
                        }
                        else {
                            column.isNumeric = true;
                        }
                        if (typeof column[row + 1] !== 'undefined') {
                            descending = floatVal > column[row + 1];
                        }
                        // String, continue to determine if it is a date string or really a
                        // string
                    }
                    else {
                        if (trimVal && trimVal.length) {
                            dateVal = this.parseDate(val);
                        }
                        // Only allow parsing of dates if this column is an x-column
                        if (isXColumn && isNumber(dateVal) && columnType !== 'float') {
                            backup[row] = val;
                            column[row] = dateVal;
                            column.isDatetime = true;
                            // Check if the dates are uniformly descending or ascending.
                            // If they are not, chances are that they are a different
                            // time format, so check for alternative.
                            if (typeof column[row + 1] !== 'undefined') {
                                diff = dateVal > column[row + 1];
                                if (diff !== descending &&
                                    typeof descending !== 'undefined') {
                                    if (this.alternativeFormat) {
                                        this.dateFormat = this.alternativeFormat;
                                        row = column.length;
                                        this.alternativeFormat =
                                            this.dateFormats[this.dateFormat]
                                                .alternative;
                                    }
                                    else {
                                        column.unsorted = true;
                                    }
                                }
                                descending = diff;
                            }
                        }
                        else { // string
                            column[row] = trimVal === '' ? null : trimVal;
                            if (row !== 0 &&
                                (column.isDatetime ||
                                    column.isNumeric)) {
                                column.mixed = true;
                            }
                        }
                    }
                }
                // If strings are intermixed with numbers or dates in a parsed column,
                // it is an indication that parsing went wrong or the data was not
                // intended to display as numbers or dates and parsing is too
                // aggressive. Fall back to categories. Demonstrated in the
                // highcharts/demo/column-drilldown sample.
                if (isXColumn && column.mixed) {
                    columns[col] = rawColumns[col];
                }
                // If the 0 column is date or number and descending, reverse all
                // columns.
                if (isXColumn && descending && this.options.sort) {
                    for (col = 0; col < columns.length; col++) {
                        columns[col].reverse();
                        if (firstRowAsNames) {
                            columns[col].unshift(columns[col].pop());
                        }
                    }
                }
            };
            /**
             * Parse a date and return it as a number. Overridable through
             * `options.parseDate`.
             *
             * @function Highcharts.Data#parseDate
             */
            Data.prototype.parseDate = function (val) {
                var parseDate = this.options.parseDate;
                var ret,
                    key,
                    format,
                    dateFormat = this.options.dateFormat || this.dateFormat,
                    match;
                if (parseDate) {
                    ret = parseDate(val);
                }
                else if (typeof val === 'string') {
                    // Auto-detect the date format the first time
                    if (!dateFormat) {
                        for (key in this.dateFormats) { // eslint-disable-line guard-for-in
                            format = this.dateFormats[key];
                            match = val.match(format.regex);
                            if (match) {
                                this.dateFormat = dateFormat = key;
                                this.alternativeFormat = format.alternative;
                                ret = format.parser(match);
                                break;
                            }
                        }
                        // Next time, use the one previously found
                    }
                    else {
                        format = this.dateFormats[dateFormat];
                        if (!format) {
                            // The selected format is invalid
                            format = this.dateFormats['YYYY/mm/dd'];
                        }
                        match = val.match(format.regex);
                        if (match) {
                            ret = format.parser(match);
                        }
                    }
                    // Fall back to Date.parse
                    if (!match) {
                        if (val.match(/:.+(GMT|UTC|[Z+-])/)) {
                            val = val
                                .replace(/\s*(?:GMT|UTC)?([+-])(\d\d)(\d\d)$/, '$1$2:$3')
                                .replace(/(?:\s+|GMT|UTC)([+-])/, '$1')
                                .replace(/(\d)\s*(?:GMT|UTC|Z)$/, '$1+00:00');
                        }
                        match = Date.parse(val);
                        // External tools like Date.js and MooTools extend Date object
                        // and return a date.
                        if (typeof match === 'object' &&
                            match !== null &&
                            match.getTime) {
                            ret = (match.getTime() -
                                match.getTimezoneOffset() *
                                    60000);
                            // Timestamp
                        }
                        else if (isNumber(match)) {
                            ret = match - (new Date(match)).getTimezoneOffset() * 60000;
                        }
                    }
                }
                return ret;
            };
            /**
             * Get the parsed data in a form that we can apply directly to the
             * `series.data` config. Array positions can be mapped using the
             * `series.keys` option.
             *
             * @example
             * const data = Highcharts.data({
             *   csv: document.getElementById('data').innerHTML
             * }).getData();
             *
             * @function Highcharts.Data#getData
             *
             * @return {Array<Array<(number|string)>>|undefined} Data rows
             */
            Data.prototype.getData = function () {
                if (this.columns) {
                    return this.rowsToColumns(this.columns).slice(1);
                }
            };
            /**
             * A hook for working directly on the parsed columns
             *
             * @function Highcharts.Data#parsed
             */
            Data.prototype.parsed = function () {
                if (this.options.parsed) {
                    return this.options.parsed.call(this, this.columns);
                }
            };
            /**
             * If a complete callback function is provided in the options, interpret the
             * columns into a Highcharts options object.
             *
             * @function Highcharts.Data#complete
             */
            Data.prototype.complete = function () {
                var columns = this.columns,
                    xColumns = [],
                    options = this.options,
                    allSeriesBuilders = [];
                var type,
                    series,
                    data,
                    i,
                    j,
                    r,
                    seriesIndex,
                    chartOptions,
                    builder,
                    freeIndexes,
                    typeCol,
                    index;
                xColumns.length = columns.length;
                if (options.complete || options.afterComplete) {
                    // Get the names and shift the top row
                    if (this.firstRowAsNames) {
                        for (i = 0; i < columns.length; i++) {
                            var curCol = columns[i];
                            if (!defined(curCol.name)) {
                                curCol.name = pick(curCol.shift(), '').toString();
                            }
                        }
                    }
                    // Use the next columns for series
                    series = [];
                    freeIndexes = getFreeIndexes(columns.length, this.valueCount.seriesBuilders);
                    // Populate defined series
                    for (seriesIndex = 0; seriesIndex < this.valueCount.seriesBuilders.length; seriesIndex++) {
                        builder = this.valueCount.seriesBuilders[seriesIndex];
                        // If the builder can be populated with remaining columns, then
                        // add it to allBuilders
                        if (builder.populateColumns(freeIndexes)) {
                            allSeriesBuilders.push(builder);
                        }
                    }
                    // Populate dynamic series
                    while (freeIndexes.length > 0) {
                        builder = new SeriesBuilder();
                        builder.addColumnReader(0, 'x');
                        // Mark index as used (not free)
                        index = freeIndexes.indexOf(0);
                        if (index !== -1) {
                            freeIndexes.splice(index, 1);
                        }
                        for (i = 0; i < this.valueCount.global; i++) {
                            // Create and add a column reader for the next free column
                            // index
                            builder.addColumnReader(void 0, this.valueCount.globalPointArrayMap[i]);
                        }
                        // If the builder can be populated with remaining columns, then
                        // add it to allBuilders
                        if (builder.populateColumns(freeIndexes)) {
                            allSeriesBuilders.push(builder);
                        }
                    }
                    // Get the data-type from the first series x column
                    if (allSeriesBuilders.length > 0 &&
                        allSeriesBuilders[0].readers.length > 0) {
                        typeCol = columns[allSeriesBuilders[0].readers[0].columnIndex];
                        if (typeof typeCol !== 'undefined') {
                            if (typeCol.isDatetime) {
                                type = 'datetime';
                            }
                            else if (!typeCol.isNumeric) {
                                type = 'category';
                            }
                        }
                    }
                    // Axis type is category, then the "x" column should be called
                    // "name"
                    if (type === 'category') {
                        for (seriesIndex = 0; seriesIndex < allSeriesBuilders.length; seriesIndex++) {
                            builder = allSeriesBuilders[seriesIndex];
                            for (r = 0; r < builder.readers.length; r++) {
                                if (builder.readers[r].configName === 'x') {
                                    builder.readers[r].configName = 'name';
                                }
                            }
                        }
                    }
                    // Read data for all builders
                    for (seriesIndex = 0; seriesIndex < allSeriesBuilders.length; seriesIndex++) {
                        builder = allSeriesBuilders[seriesIndex];
                        // Iterate down the cells of each column and add data to the
                        // series
                        data = [];
                        for (j = 0; j < columns[0].length; j++) {
                            data[j] = builder.read(columns, j);
                        }
                        // Add the series
                        series[seriesIndex] = {
                            data: data
                        };
                        if (builder.name) {
                            series[seriesIndex].name = builder.name;
                        }
                        if (type === 'category') {
                            series[seriesIndex].turboThreshold = 0;
                        }
                    }
                    // Do the callback
                    chartOptions = {
                        series: series
                    };
                    if (type) {
                        chartOptions.xAxis = {
                            type: type
                        };
                        if (type === 'category') {
                            chartOptions.xAxis.uniqueNames = false;
                        }
                    }
                    if (options.complete) {
                        options.complete(chartOptions);
                    }
                    // The afterComplete hook is used internally to avoid conflict with
                    // the externally available complete option.
                    if (options.afterComplete) {
                        options.afterComplete(chartOptions);
                    }
                }
            };
            /**
             * Updates the chart with new data options.
             *
             * @function Highcharts.Data#update
             *
             * @param {Highcharts.DataOptions} options
             *
             * @param {boolean} [redraw=true]
             */
            Data.prototype.update = function (options, redraw) {
                var chart = this.chart,
                    chartOptions = chart.options;
                if (options) {
                    // Set the complete handler
                    options.afterComplete = function (dataOptions) {
                        // Avoid setting axis options unless the type changes. Running
                        // Axis.update will cause the whole structure to be destroyed
                        // and rebuilt, and animation is lost.
                        if (dataOptions) {
                            if (dataOptions.xAxis &&
                                chart.xAxis[0] &&
                                dataOptions.xAxis.type ===
                                    chart.xAxis[0].options.type) {
                                delete dataOptions.xAxis;
                            }
                            // @todo looks not right:
                            chart.update(dataOptions, redraw, true);
                        }
                    };
                    // Apply it
                    merge(true, chartOptions.data, options);
                    // Reset columns if fetching spreadsheet, to force a re-fetch
                    if (chartOptions.data && chartOptions.data.googleSpreadsheetKey &&
                        !options.columns) {
                        delete chartOptions.data.columns;
                    }
                    this.init(chartOptions.data);
                }
            };
            return Data;
        }());
        // Extend Chart.init so that the Chart constructor accepts a new configuration
        // option group, data.
        addEvent(Chart, 'init', function (e) {
            var chart = this,
                callback = e.args[1],
                defaultDataOptions = getOptions().data;
            var userOptions = (e.args[0] || {});
            if ((defaultDataOptions || userOptions && userOptions.data) &&
                !chart.hasDataDef) {
                chart.hasDataDef = true;
                /**
                 * The data parser for this chart.
                 *
                 * @name Highcharts.Chart#data
                 * @type {Highcharts.Data|undefined}
                 */
                var dataOptions = merge(defaultDataOptions,
                    userOptions.data);
                chart.data = new Data(extend(dataOptions, {
                    afterComplete: function (dataOptions) {
                        var i,
                            series;
                        // Merge series configs
                        if (Object.hasOwnProperty.call(userOptions, 'series')) {
                            if (typeof userOptions.series === 'object') {
                                i = Math.max(userOptions.series.length, dataOptions && dataOptions.series ?
                                    dataOptions.series.length :
                                    0);
                                while (i--) {
                                    series = userOptions.series[i] || {};
                                    userOptions.series[i] = merge(series, dataOptions && dataOptions.series ?
                                        dataOptions.series[i] :
                                        {});
                                }
                            }
                            else { // Allow merging in dataOptions.series (#2856)
                                delete userOptions.series;
                            }
                        }
                        // Do the merge
                        userOptions = merge(dataOptions, userOptions);
                        // Run chart.init again
                        chart.init(userOptions, callback);
                    }
                }), userOptions, chart);
                e.preventDefault();
            }
        });
        /**
         * Creates a new SeriesBuilder. A SeriesBuilder consists of a number
         * of ColumnReaders that reads columns and give them a name.
         * Ex: A series builder can be constructed to read column 3 as 'x' and
         * column 7 and 8 as 'y1' and 'y2'.
         * The output would then be points/rows of the form {x: 11, y1: 22, y2: 33}
         *
         * The name of the builder is taken from the second column. In the above
         * example it would be the column with index 7.
         *
         * @private
         * @class
         * @name SeriesBuilder
         */
        var SeriesBuilder = /** @class */ (function () {
                function SeriesBuilder() {
                    /* eslint-disable no-invalid-this */
                    this.readers = [];
                this.pointIsArray = true;
            }
            /**
             * Populates readers with column indexes. A reader can be added without
             * a specific index and for those readers the index is taken sequentially
             * from the free columns (this is handled by the ColumnCursor instance).
             *
             * @function SeriesBuilder#populateColumns
             */
            SeriesBuilder.prototype.populateColumns = function (freeIndexes) {
                var builder = this;
                var enoughColumns = true;
                // Loop each reader and give it an index if its missing.
                // The freeIndexes.shift() will return undefined if there
                // are no more columns.
                builder.readers.forEach(function (reader) {
                    if (typeof reader.columnIndex === 'undefined') {
                        reader.columnIndex = freeIndexes.shift();
                    }
                });
                // Now, all readers should have columns mapped. If not
                // then return false to signal that this series should
                // not be added.
                builder.readers.forEach(function (reader) {
                    if (typeof reader.columnIndex === 'undefined') {
                        enoughColumns = false;
                    }
                });
                return enoughColumns;
            };
            /**
             * Reads a row from the dataset and returns a point or array depending
             * on the names of the readers.
             *
             * @function SeriesBuilder#read<T>
             */
            SeriesBuilder.prototype.read = function (columns, rowIndex) {
                var builder = this,
                    pointIsArray = builder.pointIsArray,
                    point = pointIsArray ? [] : {};
                var columnIndexes;
                // Loop each reader and ask it to read its value.
                // Then, build an array or point based on the readers names.
                builder.readers.forEach(function (reader) {
                    var value = columns[reader.columnIndex][rowIndex];
                    if (pointIsArray) {
                        point.push(value);
                    }
                    else {
                        if (reader.configName.indexOf('.') > 0) {
                            // Handle nested property names
                            Point.prototype.setNestedProperty(point, value, reader.configName);
                        }
                        else {
                            point[reader.configName] = value;
                        }
                    }
                });
                // The name comes from the first column (excluding the x column)
                if (typeof this.name === 'undefined' && builder.readers.length >= 2) {
                    columnIndexes = builder.getReferencedColumnIndexes();
                    if (columnIndexes.length >= 2) {
                        // remove the first one (x col)
                        columnIndexes.shift();
                        // Sort the remaining
                        columnIndexes.sort(function (a, b) {
                            return a - b;
                        });
                        // Now use the lowest index as name column
                        this.name = columns[columnIndexes.shift()].name;
                    }
                }
                return point;
            };
            /**
             * Creates and adds ColumnReader from the given columnIndex and configName.
             * ColumnIndex can be undefined and in that case the reader will be given
             * an index when columns are populated.
             *
             * @function SeriesBuilder#addColumnReader
             */
            SeriesBuilder.prototype.addColumnReader = function (columnIndex, configName) {
                this.readers.push({
                    columnIndex: columnIndex,
                    configName: configName
                });
                if (!(configName === 'x' ||
                    configName === 'y' ||
                    typeof configName === 'undefined')) {
                    this.pointIsArray = false;
                }
            };
            /**
             * Returns an array of column indexes that the builder will use when
             * reading data.
             *
             * @function SeriesBuilder#getReferencedColumnIndexes
             */
            SeriesBuilder.prototype.getReferencedColumnIndexes = function () {
                var referencedColumnIndexes = [];
                var i,
                    columnReader;
                for (i = 0; i < this.readers.length; i = i + 1) {
                    columnReader = this.readers[i];
                    if (typeof columnReader.columnIndex !== 'undefined') {
                        referencedColumnIndexes.push(columnReader.columnIndex);
                    }
                }
                return referencedColumnIndexes;
            };
            /**
             * Returns true if the builder has a reader for the given configName.
             *
             * @function SeriesBuider#hasReader
             */
            SeriesBuilder.prototype.hasReader = function (configName) {
                var i,
                    columnReader;
                for (i = 0; i < this.readers.length; i = i + 1) {
                    columnReader = this.readers[i];
                    if (columnReader.configName === configName) {
                        return true;
                    }
                }
                // Else return undefined
            };
            return SeriesBuilder;
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
         * Callback function to modify the CSV before parsing it by the data module.
         *
         * @callback Highcharts.DataBeforeParseCallbackFunction
         *
         * @param {string} csv
         *        The CSV to modify.
         *
         * @return {string}
         *         The CSV to parse.
         */
        /**
         * Callback function that gets called after parsing data.
         *
         * @callback Highcharts.DataCompleteCallbackFunction
         *
         * @param {Highcharts.Options} chartOptions
         *        The chart options that were used.
         */
        /**
         * Callback function that returns the correspondig Date object to a match.
         *
         * @callback Highcharts.DataDateFormatCallbackFunction
         *
         * @param {Array<number>} match
         *
         * @return {number}
         */
        /**
         * Structure for alternative date formats to parse.
         *
         * @interface Highcharts.DataDateFormatObject
         */ /**
        * @name Highcharts.DataDateFormatObject#alternative
        * @type {string|undefined}
        */ /**
        * @name Highcharts.DataDateFormatObject#parser
        * @type {Highcharts.DataDateFormatCallbackFunction}
        */ /**
        * @name Highcharts.DataDateFormatObject#regex
        * @type {global.RegExp}
        */
        /**
         * Possible types for a data item in a column or row.
         *
         * @typedef {number|string|null} Highcharts.DataValueType
         */
        /**
         * Callback function to parse string representations of dates into
         * JavaScript timestamps (milliseconds since 1.1.1970).
         *
         * @callback Highcharts.DataParseDateCallbackFunction
         *
         * @param {string} dateValue
         *
         * @return {number}
         *         Timestamp (milliseconds since 1.1.1970) as integer for Date class.
         */
        /**
         * Callback function to access the parsed columns, the two-dimentional
         * input data array directly, before they are interpreted into series
         * data and categories.
         *
         * @callback Highcharts.DataParsedCallbackFunction
         *
         * @param {Array<Array<*>>} columns
         *        The parsed columns by the data module.
         *
         * @return {boolean|undefined}
         *         Return `false` to stop completion, or call `this.complete()` to
         *         continue async.
         */
        /* *
         *
         *  API Options
         *
         * */
        /**
         * The Data module provides a simplified interface for adding data to
         * a chart from sources like CVS, HTML tables or grid views. See also
         * the [tutorial article on the Data module](
         * https://www.highcharts.com/docs/working-with-data/data-module).
         *
         * It requires the `modules/data.js` file to be loaded.
         *
         * Please note that the default way of adding data in Highcharts, without
         * the need of a module, is through the [series._type_.data](#series.line.data)
         * option.
         *
         * @sample {highcharts} highcharts/demo/column-parsed/
         *         HTML table
         * @sample {highcharts} highcharts/data/csv/
         *         CSV
         *
         * @since     4.0
         * @requires  modules/data
         * @apioption data
         */
        /**
         * A callback function to modify the CSV before parsing it. Return the modified
         * string.
         *
         * @sample {highcharts} highcharts/demo/line-ajax/
         *         Modify CSV before parse
         *
         * @type      {Highcharts.DataBeforeParseCallbackFunction}
         * @since     6.1
         * @apioption data.beforeParse
         */
        /**
         * A two-dimensional array representing the input data on tabular form.
         * This input can be used when the data is already parsed, for example
         * from a grid view component. Each cell can be a string or number.
         * If not switchRowsAndColumns is set, the columns are interpreted as
         * series.
         *
         * @see [data.rows](#data.rows)
         *
         * @sample {highcharts} highcharts/data/columns/
         *         Columns
         *
         * @type      {Array<Array<Highcharts.DataValueType>>}
         * @since     4.0
         * @apioption data.columns
         */
        /**
         * The callback that is evaluated when the data is finished loading,
         * optionally from an external source, and parsed. The first argument
         * passed is a finished chart options object, containing the series.
         * These options can be extended with additional options and passed
         * directly to the chart constructor.
         *
         * @see [data.parsed](#data.parsed)
         *
         * @sample {highcharts} highcharts/data/complete/
         *         Modify data on complete
         *
         * @type      {Highcharts.DataCompleteCallbackFunction}
         * @since     4.0
         * @apioption data.complete
         */
        /**
         * A comma delimited string to be parsed. Related options are [startRow](
         * #data.startRow), [endRow](#data.endRow), [startColumn](#data.startColumn)
         * and [endColumn](#data.endColumn) to delimit what part of the table
         * is used. The [lineDelimiter](#data.lineDelimiter) and [itemDelimiter](
         * #data.itemDelimiter) options define the CSV delimiter formats.
         *
         * The built-in CSV parser doesn't support all flavours of CSV, so in
         * some cases it may be necessary to use an external CSV parser. See
         * [this example](https://jsfiddle.net/highcharts/u59176h4/) of parsing
         * CSV through the MIT licensed [Papa Parse](http://papaparse.com/)
         * library.
         *
         * @sample {highcharts} highcharts/data/csv/
         *         Data from CSV
         *
         * @type      {string}
         * @since     4.0
         * @apioption data.csv
         */
        /**
         * Which of the predefined date formats in Date.prototype.dateFormats
         * to use to parse date values. Defaults to a best guess based on what
         * format gives valid and ordered dates. Valid options include: `YYYY/mm/dd`,
         * `dd/mm/YYYY`, `mm/dd/YYYY`, `dd/mm/YY`, `mm/dd/YY`.
         *
         * @see [data.parseDate](#data.parseDate)
         *
         * @sample {highcharts} highcharts/data/dateformat-auto/
         *         Best guess date format
         *
         * @type       {string}
         * @since      4.0
         * @validvalue ["YYYY/mm/dd", "dd/mm/YYYY", "mm/dd/YYYY", "dd/mm/YYYY",
         *             "dd/mm/YY", "mm/dd/YY"]
         * @apioption  data.dateFormat
         */
        /**
         * The decimal point used for parsing numbers in the CSV.
         *
         * If both this and data.delimiter is set to `undefined`, the parser will
         * attempt to deduce the decimal point automatically.
         *
         * @sample {highcharts} highcharts/data/delimiters/
         *         Comma as decimal point
         *
         * @type      {string}
         * @default   .
         * @since     4.1.0
         * @apioption data.decimalPoint
         */
        /**
         * In tabular input data, the last column (indexed by 0) to use. Defaults
         * to the last column containing data.
         *
         * @sample {highcharts} highcharts/data/start-end/
         *         Limited data
         *
         * @type      {number}
         * @since     4.0
         * @apioption data.endColumn
         */
        /**
         * In tabular input data, the last row (indexed by 0) to use. Defaults
         * to the last row containing data.
         *
         * @sample {highcharts} highcharts/data/start-end/
         *         Limited data
         *
         * @type      {number}
         * @since     4.0.4
         * @apioption data.endRow
         */
        /**
         * Whether to use the first row in the data set as series names.
         *
         * @sample {highcharts} highcharts/data/start-end/
         *         Don't get series names from the CSV
         * @sample {highstock} highcharts/data/start-end/
         *         Don't get series names from the CSV
         *
         * @type      {boolean}
         * @default   true
         * @since     4.1.0
         * @product   highcharts highstock gantt
         * @apioption data.firstRowAsNames
         */
        /**
         * The Google Spreadsheet API key required for access generated at [API Services
         * / Credentials](https://console.cloud.google.com/apis/credentials). See a
         * comprehensive tutorial for setting up the key at the
         * [Hands-On Data Visualization](https://handsondataviz.org/google-sheets-api-key.html)
         * book website.
         *
         * @sample {highcharts} highcharts/data/google-spreadsheet/
         *         Load a Google Spreadsheet
         *
         * @type      {string}
         * @since     9.2.2
         * @apioption data.googleAPIKey
         */
        /**
         * The key or `spreadsheetId` value for a Google Spreadsheet to load. See
         * [developers.google.com](https://developers.google.com/sheets/api/guides/concepts)
         * for how to find the `spreadsheetId`.
         *
         * In order for Google Sheets to load, a valid [googleAPIKey](#data.googleAPIKey)
         * must also be given.
         *
         * @sample {highcharts} highcharts/data/google-spreadsheet/
         *         Load a Google Spreadsheet
         *
         * @type      {string}
         * @since     4.0
         * @apioption data.googleSpreadsheetKey
         */
        /**
         * The Google Spreadsheet `range` to use in combination with
         * [googleSpreadsheetKey](#data.googleSpreadsheetKey). See
         * [developers.google.com](https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/get)
         * for details.
         *
         * If given, it takes precedence over `startColumn`, `endColumn`, `startRow` and
         * `endRow`.
         *
         * @example
         * googleSpreadsheetRange: 'Fruit Consumption' // Load a named worksheet
         * googleSpreadsheetRange: 'A:Z' // Load columns A to Z
         *
         * @sample {highcharts} highcharts/data/google-spreadsheet/
         *         Load a Google Spreadsheet
         *
         * @type      {string|undefined}
         * @since     9.2.2
         * @apioption data.googleSpreadsheetRange
         */
        /**
         * No longer works since v9.2.2, that uses Google Sheets API v4. Instead, use
         * the [googleSpreadsheetRange](#data.googleSpreadsheetRange) option to load a
         * specific sheet.
         *
         * @deprecated
         * @type      {string}
         * @since     4.0
         * @apioption data.googleSpreadsheetWorksheet
         */
        /**
         * Item or cell delimiter for parsing CSV. Defaults to the tab character
         * `\t` if a tab character is found in the CSV string, if not it defaults
         * to `,`.
         *
         * If this is set to false or undefined, the parser will attempt to deduce
         * the delimiter automatically.
         *
         * @sample {highcharts} highcharts/data/delimiters/
         *         Delimiters
         *
         * @type      {string}
         * @since     4.0
         * @apioption data.itemDelimiter
         */
        /**
         * Line delimiter for parsing CSV.
         *
         * @sample {highcharts} highcharts/data/delimiters/
         *         Delimiters
         *
         * @type      {string}
         * @default   \n
         * @since     4.0
         * @apioption data.lineDelimiter
         */
        /**
         * A callback function to access the parsed columns, the two-dimentional
         * input data array directly, before they are interpreted into series
         * data and categories. Return `false` to stop completion, or call
         * `this.complete()` to continue async.
         *
         * @see [data.complete](#data.complete)
         *
         * @sample {highcharts} highcharts/data/parsed/
         *         Modify data after parse
         *
         * @type      {Highcharts.DataParsedCallbackFunction}
         * @since     4.0
         * @apioption data.parsed
         */
        /**
         * A callback function to parse string representations of dates into
         * JavaScript timestamps. Should return an integer timestamp on success.
         *
         * @see [dateFormat](#data.dateFormat)
         *
         * @type      {Highcharts.DataParseDateCallbackFunction}
         * @since     4.0
         * @apioption data.parseDate
         */
        /**
         * The same as the columns input option, but defining rows intead of
         * columns.
         *
         * @see [data.columns](#data.columns)
         *
         * @sample {highcharts} highcharts/data/rows/
         *         Data in rows
         *
         * @type      {Array<Array<Highcharts.DataValueType>>}
         * @since     4.0
         * @apioption data.rows
         */
        /**
         * An array containing dictionaries for each series. A dictionary exists of
         * Point property names as the key and the CSV column index as the value.
         *
         * @sample {highcharts} highcharts/data/seriesmapping-label/
         *         Label from data set
         *
         * @type      {Array<Highcharts.Dictionary<number>>}
         * @since     4.0.4
         * @apioption data.seriesMapping
         */
        /**
         * In tabular input data, the first column (indexed by 0) to use.
         *
         * @sample {highcharts} highcharts/data/start-end/
         *         Limited data
         *
         * @type      {number}
         * @default   0
         * @since     4.0
         * @apioption data.startColumn
         */
        /**
         * In tabular input data, the first row (indexed by 0) to use.
         *
         * @sample {highcharts} highcharts/data/start-end/
         *         Limited data
         *
         * @type      {number}
         * @default   0
         * @since     4.0
         * @apioption data.startRow
         */
        /**
         * Switch rows and columns of the input data, so that `this.columns`
         * effectively becomes the rows of the data set, and the rows are interpreted
         * as series.
         *
         * @sample {highcharts} highcharts/data/switchrowsandcolumns/
         *         Switch rows and columns
         *
         * @type      {boolean}
         * @default   false
         * @since     4.0
         * @apioption data.switchRowsAndColumns
         */
        /**
         * An HTML table or the id of such to be parsed as input data. Related
         * options are `startRow`, `endRow`, `startColumn` and `endColumn` to
         * delimit what part of the table is used.
         *
         * @sample {highcharts} highcharts/demo/column-parsed/
         *         Parsed table
         *
         * @type      {string|global.HTMLElement}
         * @since     4.0
         * @apioption data.table
         */
        /**
         * An URL to a remote CSV dataset. Will be fetched when the chart is created
         * using Ajax.
         *
         * @sample highcharts/data/livedata-columns
         *         Categorized bar chart with CSV and live polling
         * @sample highcharts/data/livedata-csv
         *         Time based line chart with CSV and live polling
         *
         * @type      {string}
         * @apioption data.csvURL
         */
        /**
         * A URL to a remote JSON dataset, structured as a row array.
         * Will be fetched when the chart is created using Ajax.
         *
         * @sample highcharts/data/livedata-rows
         *         Rows with live polling
         *
         * @type      {string}
         * @apioption data.rowsURL
         */
        /**
         * A URL to a remote JSON dataset, structured as a column array.
         * Will be fetched when the chart is created using Ajax.
         *
         * @sample highcharts/data/livedata-columns
         *         Columns with live polling
         *
         * @type      {string}
         * @apioption data.columnsURL
         */
        /**
         * Sets the refresh rate for data polling when importing remote dataset by
         * setting [data.csvURL](data.csvURL), [data.rowsURL](data.rowsURL),
         * [data.columnsURL](data.columnsURL), or
         * [data.googleSpreadsheetKey](data.googleSpreadsheetKey).
         *
         * Note that polling must be enabled by setting
         * [data.enablePolling](data.enablePolling) to true.
         *
         * The value is the number of seconds between pollings.
         * It cannot be set to less than 1 second.
         *
         * @sample highcharts/demo/live-data
         *         Live data with user set refresh rate
         *
         * @default   1
         * @type      {number}
         * @apioption data.dataRefreshRate
         */
        /**
         * Enables automatic refetching of remote datasets every _n_ seconds (defined by
         * setting [data.dataRefreshRate](data.dataRefreshRate)).
         *
         * Only works when either [data.csvURL](data.csvURL),
         * [data.rowsURL](data.rowsURL), [data.columnsURL](data.columnsURL), or
         * [data.googleSpreadsheetKey](data.googleSpreadsheetKey).
         *
         * @sample highcharts/demo/live-data
         *         Live data
         * @sample highcharts/data/livedata-columns
         *         Categorized bar chart with CSV and live polling
         *
         * @type      {boolean}
         * @default   false
         * @apioption data.enablePolling
         */
        (''); // keeps doclets above in JS file

        return Data;
    });
    _registerModule(_modules, 'masters/modules/data.src.js', [_modules['Core/Globals.js'], _modules['Core/HttpUtilities.js'], _modules['Extensions/Data.js']], function (Highcharts, HttpUtilities, Data) {

        var G = Highcharts;
        // Functions
        G.ajax = HttpUtilities.ajax;
        G.data = Data.data;
        G.getJSON = HttpUtilities.getJSON;
        G.post = HttpUtilities.post;
        // Classes
        G.Data = Data;
        G.HttpUtilities = HttpUtilities;

    });
}));