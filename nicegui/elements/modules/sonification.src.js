/**
 * @license Highcharts JS v10.3.2 (2022-11-28)
 *
 * Sonification module
 *
 * (c) 2012-2021 Øystein Moseng
 *
 * License: www.highcharts.com/license
 */
(function (factory) {
    if (typeof module === 'object' && module.exports) {
        factory['default'] = factory;
        module.exports = factory;
    } else if (typeof define === 'function' && define.amd) {
        define('highcharts/modules/sonification', ['highcharts'], function (Highcharts) {
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
    _registerModule(_modules, 'Extensions/Sonification/MusicalFrequencies.js', [], function () {
        /* *
         *
         *  (c) 2009-2021 Øystein Moseng
         *
         *  List of musical frequencies from C0 to C8.
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
        var frequencies = [
                16.351597831287414,
                17.323914436054505,
                18.354047994837977,
                19.445436482630058,
                20.601722307054366,
                21.826764464562746,
                23.12465141947715,
                24.499714748859326,
                25.956543598746574,
                27.5,
                29.13523509488062,
                30.86770632850775,
                32.70319566257483,
                34.64782887210901,
                36.70809598967594,
                38.890872965260115,
                41.20344461410875,
                43.653528929125486,
                46.2493028389543,
                48.999429497718666,
                51.91308719749314,
                55,
                58.27047018976124,
                61.7354126570155,
                65.40639132514966,
                69.29565774421802,
                73.41619197935188,
                77.78174593052023,
                82.4068892282175,
                87.30705785825097,
                92.4986056779086,
                97.99885899543733,
                103.82617439498628,
                110,
                116.54094037952248,
                123.47082531403103,
                130.8127826502993,
                138.59131548843604,
                146.8323839587038,
                155.56349186104046,
                164.81377845643496,
                174.61411571650194,
                184.9972113558172,
                195.99771799087463,
                207.65234878997256,
                220,
                233.08188075904496,
                246.94165062806206,
                261.6255653005986,
                277.1826309768721,
                293.6647679174076,
                311.1269837220809,
                329.6275569128699,
                349.2282314330039,
                369.9944227116344,
                391.99543598174927,
                415.3046975799451,
                440,
                466.1637615180899,
                493.8833012561241,
                523.2511306011972,
                554.3652619537442,
                587.3295358348151,
                622.2539674441618,
                659.2551138257398,
                698.4564628660078,
                739.9888454232688,
                783.9908719634985,
                830.6093951598903,
                880,
                932.3275230361799,
                987.7666025122483,
                1046.5022612023945,
                1108.7305239074883,
                1174.6590716696303,
                1244.5079348883237,
                1318.5102276514797,
                1396.9129257320155,
                1479.9776908465376,
                1567.981743926997,
                1661.2187903197805,
                1760,
                1864.6550460723597,
                1975.533205024496,
                2093.004522404789,
                2217.4610478149766,
                2349.31814333926,
                2489.0158697766474,
                2637.02045530296,
                2793.825851464031,
                2959.955381693075,
                3135.9634878539946,
                3322.437580639561,
                3520,
                3729.3100921447194,
                3951.066410048992,
                4186.009044809578 // C8
            ];
        /* *
         *
         *  Default export
         *
         * */

        return frequencies;
    });
    _registerModule(_modules, 'Extensions/Sonification/SignalHandler.js', [], function () {
        /* *
         *
         *  (c) 2009-2021 Øystein Moseng
         *
         *  Utility functions for sonification.
         *
         *  License: www.highcharts.com/license
         *
         *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
         *
         * */
        /* eslint-disable no-invalid-this, valid-jsdoc */
        /* *
         *
         *  Class
         *
         * */
        /**
         * The SignalHandler class. Stores signal callbacks (event handlers), and
         * provides an interface to register them, and emit signals. The word "event" is
         * not used to avoid confusion with TimelineEvents.
         *
         * @requires module:modules/sonification
         *
         * @private
         * @class
         * @name Highcharts.SignalHandler
         *
         * @param {Array<string>} supportedSignals
         *        List of supported signal names.
         */
        var SignalHandler = /** @class */ (function () {
                /* *
                 *
                 *  Constructors
                 *
                 * */
                function SignalHandler(supportedSignals) {
                    /* *
                     *
                     *  Properties
                     *
                     * */
                    this.signals = void 0;
                this.supportedSignals = void 0;
                this.init(supportedSignals || []);
            }
            /* *
             *
             * Functions
             *
             * */
            SignalHandler.prototype.init = function (supportedSignals) {
                this.supportedSignals = supportedSignals;
                this.signals = {};
            };
            /**
             * Register a set of signal callbacks with this SignalHandler.
             * Multiple signal callbacks can be registered for the same signal.
             * @private
             * @param {Highcharts.Dictionary<(Function|undefined)>} signals
             * An object that contains a mapping from the signal name to the callbacks.
             * Only supported events are considered.
             */
            SignalHandler.prototype.registerSignalCallbacks = function (signals) {
                var signalHandler = this;
                signalHandler.supportedSignals.forEach(function (supportedSignal) {
                    var signal = signals[supportedSignal];
                    if (signal) {
                        (signalHandler.signals[supportedSignal] =
                            signalHandler.signals[supportedSignal] || []).push(signal);
                    }
                });
            };
            /**
             * Clear signal callbacks, optionally by name.
             * @private
             * @param {Array<string>} [signalNames]
             * A list of signal names to clear. If not supplied, all signal callbacks
             * are removed.
             */
            SignalHandler.prototype.clearSignalCallbacks = function (signalNames) {
                var signalHandler = this;
                if (signalNames) {
                    signalNames.forEach(function (signalName) {
                        if (signalHandler.signals[signalName]) {
                            delete signalHandler.signals[signalName];
                        }
                    });
                }
                else {
                    signalHandler.signals = {};
                }
            };
            /**
             * Emit a signal. Does nothing if the signal does not exist, or has no
             * registered callbacks.
             * @private
             * @param {string} signalName
             * Name of signal to emit.
             * @param {*} [data]
             * Data to pass to the callback.
             */
            SignalHandler.prototype.emitSignal = function (signalName, data) {
                var retval;
                if (this.signals[signalName]) {
                    this.signals[signalName].forEach(function (handler) {
                        var result = handler(data);
                        retval = typeof result !== 'undefined' ? result : retval;
                    });
                }
                return retval;
            };
            return SignalHandler;
        }());
        /* *
         *
         * Default Export
         *
         * */

        return SignalHandler;
    });
    _registerModule(_modules, 'Extensions/Sonification/SonificationUtilities.js', [_modules['Extensions/Sonification/MusicalFrequencies.js'], _modules['Extensions/Sonification/SignalHandler.js'], _modules['Core/Utilities.js']], function (MusicalFrequencies, SignalHandler, U) {
        /* *
         *
         *  (c) 2009-2021 Øystein Moseng
         *
         *  Utility functions for sonification.
         *
         *  License: www.highcharts.com/license
         *
         *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
         *
         * */
        var clamp = U.clamp,
            merge = U.merge;
        /* eslint-disable no-invalid-this, valid-jsdoc */
        /* *
         *
         *  Constants
         *
         * */
        var SonificationUtilities = {
                // List of musical frequencies from C0 to C8
                musicalFrequencies: MusicalFrequencies,
                // SignalHandler class
                SignalHandler: SignalHandler,
                getExtremesForInstrumentProps: getExtremesForInstrumentProps,
                /**
                 * Get a musical scale by specifying the semitones from 1-12 to include.
                 *  1: C, 2: C#, 3: D, 4: D#, 5: E, 6: F,
                 *  7: F#, 8: G, 9: G#, 10: A, 11: Bb, 12: B
                 * @private
                 * @param {Array<number>} semitones
                 * Array of semitones from 1-12 to include in the scale. Duplicate entries
                 * are ignored.
                 * @return {Array<number>}
                 * Array of frequencies from C0 to C8 that are included in this scale.
                 */
                getMusicalScale: function (semitones) {
                    return MusicalFrequencies.filter(function (freq,
            i) {
                        var interval = i % 12 + 1;
                    return semitones.some(function (allowedInterval) {
                        return allowedInterval === interval;
                    });
                });
            },
            /**
             * Calculate the extreme values in a chart for a data prop.
             * @private
             * @param {Highcharts.Chart} chart
             * The chart
             * @param {string} prop
             * The data prop to find extremes for
             * @return {Highcharts.RangeObject}
             * Object with min and max properties
             */
            calculateDataExtremes: function (chart, prop) {
                return chart.series.reduce(function (extremes, series) {
                    // We use cropped points rather than series.data here, to allow
                    // users to zoom in for better fidelity.
                    series.points.forEach(function (point) {
                        var val = typeof point[prop] !== 'undefined' ?
                                point[prop] : point.options[prop];
                        extremes.min = Math.min(extremes.min, val);
                        extremes.max = Math.max(extremes.max, val);
                    });
                    return extremes;
                }, {
                    min: Infinity,
                    max: -Infinity
                });
            },
            /**
             * Translate a value on a virtual axis. Creates a new, virtual, axis with a
             * min and max, and maps the relative value onto this axis.
             * @private
             * @param {number} value
             * The relative data value to translate.
             * @param {Highcharts.RangeObject} DataExtremesObject
             * The possible extremes for this value.
             * @param {Object} limits
             * Limits for the virtual axis.
             * @param {boolean} [invert]
             * Invert the virtual axis.
             * @return {number}
             * The value mapped to the virtual axis.
             */
            virtualAxisTranslate: function (value, dataExtremes, limits, invert) {
                var lenValueAxis = dataExtremes.max - dataExtremes.min,
                    lenVirtualAxis = Math.abs(limits.max - limits.min),
                    valueDelta = invert ?
                        dataExtremes.max - value :
                        value - dataExtremes.min,
                    virtualValueDelta = lenVirtualAxis * valueDelta / lenValueAxis,
                    virtualAxisValue = limits.min + virtualValueDelta;
                return lenValueAxis > 0 ?
                    clamp(virtualAxisValue, limits.min, limits.max) :
                    limits.min;
            }
        };
        /* *
         *
         *  Functions
         *
         * */
        /**
         * Calculate value extremes for used instrument data properties on a chart.
         * @private
         * @param {Highcharts.Chart} chart
         * The chart to calculate extremes from.
         * @param {Array<Highcharts.PointInstrumentObject>} [instruments]
         * Additional instrument definitions to inspect for data props used, in
         * addition to the instruments defined in the chart options.
         * @param {Highcharts.Dictionary<Highcharts.RangeObject>} [dataExtremes]
         * Predefined extremes for each data prop.
         * @return {Highcharts.Dictionary<Highcharts.RangeObject>}
         * New extremes with data properties mapped to min/max objects.
         */
        function getExtremesForInstrumentProps(chart, instruments, dataExtremes) {
            var defaultInstrumentDef = (chart.options.sonification &&
                    chart.options.sonification.defaultInstrumentOptions),
                optionDefToInstrDef = function (optionDef) { return ({
                    instrumentMapping: optionDef.mapping
                }); };
            var allInstrumentDefinitions = (instruments || []).slice(0);
            if (defaultInstrumentDef) {
                allInstrumentDefinitions.push(optionDefToInstrDef(defaultInstrumentDef));
            }
            chart.series.forEach(function (series) {
                var instrOptions = (series.options.sonification &&
                        series.options.sonification.instruments);
                if (instrOptions) {
                    allInstrumentDefinitions = allInstrumentDefinitions.concat(instrOptions.map(optionDefToInstrDef));
                }
            });
            return (allInstrumentDefinitions).reduce(function (newExtremes, instrumentDefinition) {
                Object.keys(instrumentDefinition.instrumentMapping || {}).forEach(function (instrumentParameter) {
                    var value = instrumentDefinition.instrumentMapping[instrumentParameter];
                    if (typeof value === 'string' && !newExtremes[value]) {
                        // This instrument parameter is mapped to a data prop. If we
                        // don't have predefined data extremes, find them.
                        newExtremes[value] = SonificationUtilities
                            .calculateDataExtremes(chart, value);
                    }
                });
                return newExtremes;
            }, merge(dataExtremes));
        }
        /* *
         *
         *  Default export
         *
         * */

        return SonificationUtilities;
    });
    _registerModule(_modules, 'Extensions/Sonification/Options.js', [], function () {
        /* *
         *
         *  (c) 2009-2021 Øystein Moseng
         *
         *  Default options for sonification.
         *
         *  License: www.highcharts.com/license
         *
         *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
         *
         * */
        /* *
         *
         * Constants
         *
         * */
        // Experimental, disabled by default, not exposed in API
        var options = {
                sonification: {
                    enabled: false,
                    duration: 2500,
                    afterSeriesWait: 700,
                    masterVolume: 1,
                    order: 'sequential',
                    defaultInstrumentOptions: {
                        instrument: 'sineMusical',
                        // Start at G4 note, end at C6
                        minFrequency: 392,
                        maxFrequency: 1046,
                        mapping: {
                            pointPlayTime: 'x',
                            duration: 200,
                            frequency: 'y'
                        }
                    }
                }
            };
        /* *
         *
         * Default Export
         *
         * */

        return options;
    });
    _registerModule(_modules, 'Extensions/Sonification/Sonification.js', [_modules['Core/Defaults.js'], _modules['Core/Utilities.js'], _modules['Extensions/Sonification/SonificationUtilities.js'], _modules['Extensions/Sonification/Options.js']], function (D, U, SU, sonificationOptions) {
        /* *
         *
         *  (c) 2009-2021 Øystein Moseng
         *
         *  Sonification module for Highcharts
         *
         *  License: www.highcharts.com/license
         *
         *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
         *
         * */
        /* *
         *
         *  Imports
         *
         * */
        var defaultOptions = D.defaultOptions;
        var merge = U.merge;
        /* *
         *
         *  Functions
         *
         * */
        // Expose on the Highcharts object
        // Add default options
        merge(true, defaultOptions, sonificationOptions);
        var Sonification = {
                fadeOutDuration: 20,
                // Classes and functions
                utilities: SU
            };
        /* *
         *
         *  Default Export
         *
         * */
        /**
         * Global classes and objects related to sonification.
         *
         * @requires module:modules/sonification
         *
         * @name Highcharts.sonification
         * @type {Highcharts.SonificationObject}
         */
        /**
         * Global classes and objects related to sonification.
         *
         * @requires module:modules/sonification
         *
         * @interface Highcharts.SonificationObject
         */ /**
        * Note fade-out-time in milliseconds. Most notes are faded out quickly by
        * default if there is time. This is to avoid abrupt stops which will cause
        * perceived clicks.
        * @name Highcharts.SonificationObject#fadeOutDuration
        * @type {number}
        */ /**
        * Utility functions.
        * @name Highcharts.SonificationObject#utilities
        * @private
        * @type {Object}
        */ /**
        * The Instrument class.
        * @name Highcharts.SonificationObject#Instrument
        * @type {Function}
        */ /**
        * Predefined instruments, given as an object with a map between the instrument
        * name and the Highcharts.Instrument object.
        * @name Highcharts.SonificationObject#instruments
        * @type {Object}
        */ /**
        * The Earcon class.
        * @name Highcharts.SonificationObject#Earcon
        * @type {Function}
        */ /**
        * The TimelineEvent class.
        * @private
        * @name Highcharts.SonificationObject#TimelineEvent
        * @type {Function}
        */ /**
        * The TimelinePath class.
        * @private
        * @name Highcharts.SonificationObject#TimelinePath
        * @type {Function}
        */ /**
        * The Timeline class.
        * @private
        * @name Highcharts.SonificationObject#Timeline
        * @type {Function}
        */
        (''); // detach doclets above

        return Sonification;
    });
    _registerModule(_modules, 'Extensions/Sonification/Instrument.js', [_modules['Core/Globals.js'], _modules['Extensions/Sonification/Sonification.js'], _modules['Extensions/Sonification/SonificationUtilities.js'], _modules['Core/Utilities.js']], function (H, Sonification, SU, U) {
        /* *
         *
         *  (c) 2009-2021 Øystein Moseng
         *
         *  Instrument class for sonification module.
         *
         *  License: www.highcharts.com/license
         *
         *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
         *
         * */
        /* *
         *
         *  Imports
         *
         * */
        var win = H.win;
        var error = U.error,
            merge = U.merge,
            pick = U.pick,
            uniqueKey = U.uniqueKey;
        /* eslint-disable no-invalid-this, valid-jsdoc */
        /* *
         *
         *  Class
         *
         * */
        /**
         * The Instrument class. Instrument objects represent an instrument capable of
         * playing a certain pitch for a specified duration.
         *
         * @sample highcharts/sonification/instrument/
         *         Using Instruments directly
         * @sample highcharts/sonification/instrument-advanced/
         *         Using callbacks for instrument parameters
         *
         * @requires module:modules/sonification
         *
         * @class
         * @name Highcharts.Instrument
         *
         * @param {Highcharts.InstrumentOptionsObject} options
         *        Options for the instrument instance.
         */
        var Instrument = /** @class */ (function () {
                /* *
                 *
                 *  Constructor
                 *
                 * */
                function Instrument(options) {
                    this.id = void 0;
                this.masterVolume = void 0;
                this.options = void 0;
                this.playCallbackTimers = void 0;
                this.init(options);
            }
            /* *
            *
            *  Functions
            *
            * */
            Instrument.prototype.init = function (options) {
                if (!this.initAudioContext()) {
                    error(29);
                    return;
                }
                this.options = merge(Instrument.defaultOptions, options);
                this.id = this.options.id = options && options.id || uniqueKey();
                this.masterVolume = this.options.masterVolume || 0;
                // Init the audio nodes
                var ctx = Instrument.audioContext, 
                    // Note: Destination node can be overridden by setting
                    // Highcharts.sonification.Instrument.prototype.destinationNode.
                    // This allows for inserting an additional chain of nodes after
                    // the default processing.
                    destination = this.destinationNode || ctx.destination;
                this.gainNode = ctx.createGain();
                this.setGain(0);
                this.panNode = ctx.createStereoPanner && ctx.createStereoPanner();
                if (this.panNode) {
                    this.setPan(0);
                    this.gainNode.connect(this.panNode);
                    this.panNode.connect(destination);
                }
                else {
                    this.gainNode.connect(destination);
                }
                // Oscillator initialization
                if (this.options.type === 'oscillator') {
                    this.initOscillator(this.options.oscillator);
                }
                // Init timer list
                this.playCallbackTimers = [];
            };
            /**
             * Return a copy of an instrument. Only one instrument instance can play at
             * a time, so use this to get a new copy of the instrument that can play
             * alongside it. The new instrument copy will receive a new ID unless one is
             * supplied in options.
             *
             * @function Highcharts.Instrument#copy
             *
             * @param {Highcharts.InstrumentOptionsObject} [options]
             *        Options to merge in for the copy.
             *
             * @return {Highcharts.Instrument}
             *         A new Instrument instance with the same options.
             */
            Instrument.prototype.copy = function (options) {
                return new Instrument(merge(this.options, { id: null }, options));
            };
            /**
             * Init the audio context, if we do not have one.
             * @private
             * @return {boolean} True if successful, false if not.
             */
            Instrument.prototype.initAudioContext = function () {
                var Context = win.AudioContext || win.webkitAudioContext,
                    hasOldContext = !!Instrument.audioContext;
                if (Context) {
                    Instrument.audioContext = Instrument.audioContext || new Context();
                    if (!hasOldContext &&
                        Instrument.audioContext &&
                        Instrument.audioContext.state === 'running') {
                        Instrument.audioContext.suspend(); // Pause until we need it
                    }
                    return !!(Instrument.audioContext &&
                        (Instrument.audioContext.createOscillator) &&
                        (Instrument.audioContext.createGain));
                }
                return false;
            };
            /**
             * Init an oscillator instrument.
             * @private
             * @param {Highcharts.OscillatorOptionsObject} oscillatorOptions
             * The oscillator options passed to Highcharts.Instrument#init.
             */
            Instrument.prototype.initOscillator = function (options) {
                var ctx = Instrument.audioContext;
                this.oscillator = ctx.createOscillator();
                this.oscillator.type = options.waveformShape;
                this.oscillator.connect(this.gainNode);
                this.oscillatorStarted = false;
            };
            /**
             * Set pan position.
             * @private
             * @param {number} panValue
             * The pan position to set for the instrument.
             */
            Instrument.prototype.setPan = function (panValue) {
                if (this.panNode) {
                    this.panNode.pan.setValueAtTime(panValue, Instrument.audioContext.currentTime);
                }
            };
            /**
             * Set gain level. A maximum of 1.2 is allowed before we emit a warning. The
             * actual volume is not set above this level regardless of input. This
             * function also handles the Instrument's master volume.
             * @private
             * @param {number} gainValue
             * The gain level to set for the instrument.
             * @param {number} [rampTime=0]
             * Gradually change the gain level, time given in milliseconds.
             */
            Instrument.prototype.setGain = function (gainValue, rampTime) {
                var gainNode = this.gainNode;
                var newVal = gainValue * this.masterVolume;
                if (gainNode) {
                    if (newVal > 1.2) {
                        console.warn(// eslint-disable-line
                        'Highcharts sonification warning: ' +
                            'Volume of instrument set too high.');
                        newVal = 1.2;
                    }
                    if (rampTime) {
                        gainNode.gain.setValueAtTime(gainNode.gain.value, Instrument.audioContext.currentTime);
                        gainNode.gain.linearRampToValueAtTime(newVal, Instrument.audioContext.currentTime + rampTime / 1000);
                    }
                    else {
                        gainNode.gain.setValueAtTime(newVal, Instrument.audioContext.currentTime);
                    }
                }
            };
            /**
             * Cancel ongoing gain ramps.
             * @private
             */
            Instrument.prototype.cancelGainRamp = function () {
                if (this.gainNode) {
                    this.gainNode.gain.cancelScheduledValues(0);
                }
            };
            /**
             * Set the master volume multiplier of the instrument after creation.
             * @param {number} volumeMultiplier
             * The gain level to set for the instrument.
             */
            Instrument.prototype.setMasterVolume = function (volumeMultiplier) {
                this.masterVolume = volumeMultiplier || 0;
            };
            /**
             * Get the closest valid frequency for this instrument.
             * @private
             * @param {number} frequency
             * The target frequency.
             * @param {number} [min]
             * Minimum frequency to return.
             * @param {number} [max]
             * Maximum frequency to return.
             * @return {number}
             * The closest valid frequency to the input frequency.
             */
            Instrument.prototype.getValidFrequency = function (frequency, min, max) {
                var validFrequencies = this.options.allowedFrequencies,
                    maximum = pick(max,
                    Infinity),
                    minimum = pick(min, -Infinity);
                return !validFrequencies || !validFrequencies.length ?
                    // No valid frequencies for this instrument, return the target
                    frequency :
                    // Use the valid frequencies and return the closest match
                    validFrequencies.reduce(function (acc, cur) {
                        // Find the closest allowed value
                        return Math.abs(cur - frequency) < Math.abs(acc - frequency) &&
                            cur < maximum && cur > minimum ?
                            cur : acc;
                    }, Infinity);
            };
            /**
             * Clear existing play callback timers.
             * @private
             */
            Instrument.prototype.clearPlayCallbackTimers = function () {
                this.playCallbackTimers.forEach(function (timer) {
                    clearInterval(timer);
                });
                this.playCallbackTimers = [];
            };
            /**
             * Set the current frequency being played by the instrument. The closest
             * valid frequency between the frequency limits is used.
             * @param {number} frequency
             * The frequency to set.
             * @param {Highcharts.Dictionary<number>} [frequencyLimits]
             * Object with maxFrequency and minFrequency
             */
            Instrument.prototype.setFrequency = function (frequency, frequencyLimits) {
                var limits = frequencyLimits || {},
                    validFrequency = this.getValidFrequency(frequency,
                    limits.min,
                    limits.max);
                if (this.options.type === 'oscillator') {
                    this.oscillatorPlay(validFrequency);
                }
            };
            /**
             * Play oscillator instrument.
             * @private
             * @param {number} frequency
             * The frequency to play.
             */
            Instrument.prototype.oscillatorPlay = function (frequency) {
                if (!this.oscillatorStarted) {
                    this.oscillator.start();
                    this.oscillatorStarted = true;
                }
                this.oscillator.frequency.setValueAtTime(frequency, Instrument.audioContext.currentTime);
            };
            /**
             * Prepare instrument before playing. Resumes the audio context and starts
             * the oscillator.
             * @private
             */
            Instrument.prototype.preparePlay = function () {
                this.setGain(0.001);
                if (Instrument.audioContext.state === 'suspended') {
                    Instrument.audioContext.resume();
                }
                if (this.oscillator && !this.oscillatorStarted) {
                    this.oscillator.start();
                    this.oscillatorStarted = true;
                }
            };
            /**
             * Play the instrument according to options.
             *
             * @sample highcharts/sonification/instrument/
             *         Using Instruments directly
             * @sample highcharts/sonification/instrument-advanced/
             *         Using callbacks for instrument parameters
             *
             * @function Highcharts.Instrument#play
             *
             * @param {Highcharts.InstrumentPlayOptionsObject} options
             *        Options for the playback of the instrument.
             *
             */
            Instrument.prototype.play = function (options) {
                var instrument = this,
                    duration = options.duration || 0, 
                    // Set a value, or if it is a function, set it continously as a
                    // timer. Pass in the value/function to set, the setter function,
                    // and any additional data to pass through to the setter function.
                    setOrStartTimer = function (value,
                    setter,
                    setterData) {
                        var target = options.duration,
                    callbackInterval = instrument.options.playCallbackInterval;
                    var currentDurationIx = 0;
                    if (typeof value === 'function') {
                        var timer_1 = setInterval(function () {
                                currentDurationIx++;
                            var curTime = (currentDurationIx *
                                    callbackInterval / target);
                            if (curTime >= 1) {
                                instrument[setter](value(1), setterData);
                                clearInterval(timer_1);
                            }
                            else {
                                instrument[setter](value(curTime), setterData);
                            }
                        }, callbackInterval);
                        instrument.playCallbackTimers.push(timer_1);
                    }
                    else {
                        instrument[setter](value, setterData);
                    }
                };
                if (!instrument.id) {
                    // No audio support - do nothing
                    return;
                }
                // If the AudioContext is suspended we have to resume it before playing
                if (Instrument.audioContext.state === 'suspended' ||
                    this.oscillator && !this.oscillatorStarted) {
                    instrument.preparePlay();
                    // Try again in 10ms
                    setTimeout(function () {
                        instrument.play(options);
                    }, 10);
                    return;
                }
                // Clear any existing play timers
                if (instrument.playCallbackTimers.length) {
                    instrument.clearPlayCallbackTimers();
                }
                // Clear any gain ramps
                instrument.cancelGainRamp();
                // Clear stop oscillator timer
                if (instrument.stopOscillatorTimeout) {
                    clearTimeout(instrument.stopOscillatorTimeout);
                    delete instrument.stopOscillatorTimeout;
                }
                // If a note is playing right now, clear the stop timeout, and call the
                // callback.
                if (instrument.stopTimeout) {
                    clearTimeout(instrument.stopTimeout);
                    delete instrument.stopTimeout;
                    if (instrument.stopCallback) {
                        // We have a callback for the play we are interrupting. We do
                        // not allow this callback to start a new play, because that
                        // leads to chaos. We pass in 'cancelled' to indicate that this
                        // note did not finish, but still stopped.
                        instrument._play = instrument.play;
                        instrument.play = function () { };
                        instrument.stopCallback('cancelled');
                        instrument.play = instrument._play;
                    }
                }
                // Stop the note without fadeOut if the duration is too short to hear
                // the note otherwise.
                var immediate = duration < Sonification.fadeOutDuration + 20;
                // Stop the instrument after the duration of the note
                instrument.stopCallback = options.onEnd;
                var onStop = function () {
                        delete instrument.stopTimeout;
                    instrument.stop(immediate);
                };
                if (duration) {
                    instrument.stopTimeout = setTimeout(onStop, immediate ? duration :
                        duration - Sonification.fadeOutDuration);
                    // Play the note
                    setOrStartTimer(options.frequency, 'setFrequency', {
                        minFrequency: options.minFrequency,
                        maxFrequency: options.maxFrequency
                    });
                    // Set the volume and panning
                    setOrStartTimer(pick(options.volume, 1), 'setGain', 4); // Slight ramp
                    setOrStartTimer(pick(options.pan, 0), 'setPan');
                }
                else {
                    // No note duration, so just stop immediately
                    onStop();
                }
            };
            /**
             * Mute an instrument that is playing. If the instrument is not currently
             * playing, this function does nothing.
             *
             * @function Highcharts.Instrument#mute
             */
            Instrument.prototype.mute = function () {
                this.setGain(0.0001, Sonification.fadeOutDuration * 0.8);
            };
            /**
             * Stop the instrument playing.
             *
             * @function Highcharts.Instrument#stop
             *
             * @param {boolean} immediately
             *        Whether to do the stop immediately or fade out.
             *
             * @param {Function} [onStopped]
             *        Callback function to be called when the stop is completed.
             *
             * @param {*} [callbackData]
             *        Data to send to the onEnd callback functions.
             *
             */
            Instrument.prototype.stop = function (immediately, onStopped, callbackData) {
                var instr = this,
                    reset = function () {
                        // Remove timeout reference
                        if (instr.stopOscillatorTimeout) {
                            delete instr.stopOscillatorTimeout;
                    }
                    if (instr.oscillator &&
                        instr.options.oscillator) {
                        // The oscillator may have stopped in the meantime here, so
                        // allow this function to fail if so.
                        try {
                            instr.oscillator.stop();
                        }
                        catch (e) {
                            // silent error
                        }
                        if (instr.gainNode) {
                            instr.oscillator.disconnect(instr.gainNode);
                        }
                        // We need a new oscillator in order to restart it
                        instr.initOscillator(instr.options.oscillator);
                    }
                    // Done stopping, call the callback from the stop
                    if (onStopped) {
                        onStopped(callbackData);
                    }
                    // Call the callback for the play we finished
                    if (instr.stopCallback) {
                        instr.stopCallback(callbackData);
                    }
                };
                // Clear any existing timers
                if (instr.playCallbackTimers.length) {
                    instr.clearPlayCallbackTimers();
                }
                if (instr.stopTimeout) {
                    clearTimeout(instr.stopTimeout);
                }
                if (immediately) {
                    instr.setGain(0);
                    reset();
                }
                else {
                    instr.mute();
                    // Stop the oscillator after the mute fade-out has finished
                    instr.stopOscillatorTimeout =
                        setTimeout(reset, Sonification.fadeOutDuration + 100);
                }
            };
            // Default options for Instrument constructor
            Instrument.defaultOptions = {
                type: 'oscillator',
                playCallbackInterval: 20,
                masterVolume: 1,
                oscillator: {
                    waveformShape: 'sine'
                }
            };
            Instrument.definitions = {};
            return Instrument;
        }());
        /* *
         *
         *  Class Prototype
         *
         * */
        // ['sine', 'square', 'triangle', 'sawtooth'].forEach(function (
        ['sine', 'square', 'triangle', 'sawtooth'].forEach(function (waveform) {
            // Add basic instruments
            Instrument.definitions[waveform] = new Instrument({
                oscillator: { waveformShape: waveform }
            });
            // Add musical instruments
            Instrument.definitions[waveform + 'Musical'] = new Instrument({
                allowedFrequencies: SU.musicalFrequencies,
                oscillator: { waveformShape: waveform }
            });
            // Add scaled instruments
            Instrument.definitions[waveform + 'Major'] = new Instrument({
                allowedFrequencies: SU.getMusicalScale([1, 3, 5, 6, 8, 10, 12]),
                oscillator: { waveformShape: waveform }
            });
        });
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
         * A set of options for the Instrument class.
         *
         * @requires module:modules/sonification
         *
         * @interface Highcharts.InstrumentOptionsObject
         */ /**
        * The type of instrument. Currently only `oscillator` is supported. Defaults
        * to `oscillator`.
        * @name Highcharts.InstrumentOptionsObject#type
        * @type {string|undefined}
        */ /**
        * The unique ID of the instrument. Generated if not supplied.
        * @name Highcharts.InstrumentOptionsObject#id
        * @type {string|undefined}
        */ /**
        * The master volume multiplier to apply to the instrument, regardless of other
        * volume changes. Defaults to 1.
        * @name Highcharts.InstrumentPlayOptionsObject#masterVolume
        * @type {number|undefined}
        */ /**
        * When using functions to determine frequency or other parameters during
        * playback, this options specifies how often to call the callback functions.
        * Number given in milliseconds. Defaults to 20.
        * @name Highcharts.InstrumentOptionsObject#playCallbackInterval
        * @type {number|undefined}
        */ /**
        * A list of allowed frequencies for this instrument. If trying to play a
        * frequency not on this list, the closest frequency will be used. Set to `null`
        * to allow all frequencies to be used. Defaults to `null`.
        * @name Highcharts.InstrumentOptionsObject#allowedFrequencies
        * @type {Array<number>|undefined}
        */ /**
        * Options specific to oscillator instruments.
        * @name Highcharts.InstrumentOptionsObject#oscillator
        * @type {Highcharts.OscillatorOptionsObject|undefined}
        */
        /**
         * Options for playing an instrument.
         *
         * @requires module:modules/sonification
         *
         * @interface Highcharts.InstrumentPlayOptionsObject
         */ /**
        * The frequency of the note to play. Can be a fixed number, or a function. The
        * function receives one argument: the relative time of the note playing (0
        * being the start, and 1 being the end of the note). It should return the
        * frequency number for each point in time. The poll interval of this function
        * is specified by the Instrument.playCallbackInterval option.
        * @name Highcharts.InstrumentPlayOptionsObject#frequency
        * @type {number|Function}
        */ /**
        * The duration of the note in milliseconds.
        * @name Highcharts.InstrumentPlayOptionsObject#duration
        * @type {number}
        */ /**
        * The minimum frequency to allow. If the instrument has a set of allowed
        * frequencies, the closest frequency is used by default. Use this option to
        * stop too low frequencies from being used.
        * @name Highcharts.InstrumentPlayOptionsObject#minFrequency
        * @type {number|undefined}
        */ /**
        * The maximum frequency to allow. If the instrument has a set of allowed
        * frequencies, the closest frequency is used by default. Use this option to
        * stop too high frequencies from being used.
        * @name Highcharts.InstrumentPlayOptionsObject#maxFrequency
        * @type {number|undefined}
        */ /**
        * The volume of the instrument. Can be a fixed number between 0 and 1, or a
        * function. The function receives one argument: the relative time of the note
        * playing (0 being the start, and 1 being the end of the note). It should
        * return the volume for each point in time. The poll interval of this function
        * is specified by the Instrument.playCallbackInterval option. Defaults to 1.
        * @name Highcharts.InstrumentPlayOptionsObject#volume
        * @type {number|Function|undefined}
        */ /**
        * The panning of the instrument. Can be a fixed number between -1 and 1, or a
        * function. The function receives one argument: the relative time of the note
        * playing (0 being the start, and 1 being the end of the note). It should
        * return the panning value for each point in time. The poll interval of this
        * function is specified by the Instrument.playCallbackInterval option.
        * Defaults to 0.
        * @name Highcharts.InstrumentPlayOptionsObject#pan
        * @type {number|Function|undefined}
        */ /**
        * Callback function to be called when the play is completed.
        * @name Highcharts.InstrumentPlayOptionsObject#onEnd
        * @type {Function|undefined}
        */
        /**
         * @requires module:modules/sonification
         *
         * @interface Highcharts.OscillatorOptionsObject
         */ /**
        * The waveform shape to use for oscillator instruments. Defaults to `sine`.
        * @name Highcharts.OscillatorOptionsObject#waveformShape
        * @type {string|undefined}
        */
        (''); // keeps doclets above in JS file

        return Instrument;
    });
    _registerModule(_modules, 'Extensions/Sonification/Earcon.js', [_modules['Extensions/Sonification/Instrument.js'], _modules['Core/Utilities.js']], function (Instrument, U) {
        /* *
         *
         *  (c) 2009-2021 Øystein Moseng
         *
         *  Earcons for the sonification module in Highcharts.
         *
         *  License: www.highcharts.com/license
         *
         *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
         *
         * */
        var error = U.error,
            merge = U.merge,
            pick = U.pick,
            uniqueKey = U.uniqueKey;
        /* *
         *
         *  Class
         *
         * */
        /* eslint-disable no-invalid-this, valid-jsdoc */
        /**
         * The Earcon class. Earcon objects represent a certain sound consisting of
         * one or more instruments playing a predefined sound.
         *
         * @sample highcharts/sonification/earcon/
         *         Using earcons directly
         *
         * @requires module:modules/sonification
         *
         * @class
         * @name Highcharts.Earcon
         *
         * @param {Highcharts.EarconOptionsObject} options
         *        Options for the Earcon instance.
         */
        var Earcon = /** @class */ (function () {
                /* *
                 *
                 *  Constructor
                 *
                 * */
                function Earcon(options) {
                    /* *
                     *
                     *  Properties
                     *
                     * */
                    this.id = void 0;
                this.instrumentsPlaying = void 0;
                this.options = void 0;
                this.init(options || {});
            }
            /* *
             *
             *  Functions
             *
             * */
            Earcon.prototype.init = function (options) {
                this.options = options;
                if (!this.options.id) {
                    this.options.id = this.id = uniqueKey();
                }
                this.instrumentsPlaying = {};
            };
            /**
             * Play the earcon, optionally overriding init options.
             *
             * @sample highcharts/sonification/earcon/
             *         Using earcons directly
             *
             * @function Highcharts.Earcon#sonify
             *
             * @param {Highcharts.EarconOptionsObject} options
             * Override existing options.
             */
            Earcon.prototype.sonify = function (options) {
                var playOptions = merge(this.options,
                    options), 
                    // Find master volume/pan settings
                    masterVolume = pick(playOptions.volume, 1),
                    masterPan = playOptions.pan,
                    earcon = this,
                    playOnEnd = options && options.onEnd,
                    masterOnEnd = earcon.options.onEnd;
                // Go through the instruments and play them
                playOptions.instruments.forEach(function (opts) {
                    var instrument = typeof opts.instrument === 'string' ?
                            Instrument.definitions[opts.instrument] : opts.instrument,
                        instrumentOpts = merge(opts.playOptions);
                    var instrOnEnd,
                        instrumentCopy,
                        copyId = '';
                    if (instrument && (instrument.play)) {
                        if (opts.playOptions) {
                            instrumentOpts.pan = pick(masterPan, instrumentOpts.pan);
                            // Handle onEnd
                            instrOnEnd = instrumentOpts.onEnd;
                            instrumentOpts.onEnd = function () {
                                delete earcon.instrumentsPlaying[copyId];
                                if (instrOnEnd) {
                                    instrOnEnd.apply(this, arguments);
                                }
                                if (!Object.keys(earcon.instrumentsPlaying).length) {
                                    if (playOnEnd) {
                                        playOnEnd.apply(this, arguments);
                                    }
                                    if (masterOnEnd) {
                                        masterOnEnd.apply(this, arguments);
                                    }
                                }
                            };
                            // Play the instrument. Use a copy so we can play multiple
                            // at the same time.
                            instrumentCopy = instrument.copy();
                            instrumentCopy.setMasterVolume(masterVolume);
                            copyId = instrumentCopy.id;
                            earcon.instrumentsPlaying[copyId] = instrumentCopy;
                            instrumentCopy.play(instrumentOpts);
                        }
                    }
                    else {
                        error(30);
                    }
                });
            };
            /**
             * Cancel any current sonification of the Earcon. Calls onEnd functions.
             *
             * @function Highcharts.Earcon#cancelSonify
             *
             * @param {boolean} [fadeOut=false]
             *        Whether or not to fade out as we stop. If false, the earcon is
             *        cancelled synchronously.
             */
            Earcon.prototype.cancelSonify = function (fadeOut) {
                var playing = this.instrumentsPlaying,
                    instrIds = playing && Object.keys(playing);
                if (instrIds && instrIds.length) {
                    instrIds.forEach(function (instr) {
                        playing[instr].stop(!fadeOut, null, 'cancelled');
                    });
                    this.instrumentsPlaying = {};
                }
            };
            return Earcon;
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
         * Define an Instrument and the options for playing it.
         *
         * @requires module:modules/sonification
         *
         * @interface Highcharts.EarconInstrument
         */ /**
        * An instrument instance or the name of the instrument in the
        * Highcharts.sonification.instruments map.
        * @name Highcharts.EarconInstrument#instrument
        * @type {string|Highcharts.Instrument}
        */ /**
        * The options to pass to Instrument.play.
        * @name Highcharts.EarconInstrument#playOptions
        * @type {Highcharts.InstrumentPlayOptionsObject}
        */
        /**
         * Options for an Earcon.
         *
         * @requires module:modules/sonification
         *
         * @interface Highcharts.EarconOptionsObject
         */ /**
        * The instruments and their options defining this earcon.
        * @name Highcharts.EarconOptionsObject#instruments
        * @type {Array<Highcharts.EarconInstrument>}
        */ /**
        * The unique ID of the Earcon. Generated if not supplied.
        * @name Highcharts.EarconOptionsObject#id
        * @type {string|undefined}
        */ /**
        * Global panning of all instruments. Overrides all panning on individual
        * instruments. Can be a number between -1 and 1.
        * @name Highcharts.EarconOptionsObject#pan
        * @type {number|undefined}
        */ /**
        * Master volume for all instruments. Volume settings on individual instruments
        * can still be used for relative volume between the instruments. This setting
        * does not affect volumes set by functions in individual instruments. Can be a
        * number between 0 and 1. Defaults to 1.
        * @name Highcharts.EarconOptionsObject#volume
        * @type {number|undefined}
        */ /**
        * Callback function to call when earcon has finished playing.
        * @name Highcharts.EarconOptionsObject#onEnd
        * @type {Function|undefined}
        */
        (''); // detach doclets above

        return Earcon;
    });
    _registerModule(_modules, 'Extensions/Sonification/Timeline.js', [_modules['Extensions/Sonification/Sonification.js'], _modules['Core/Utilities.js'], _modules['Extensions/Sonification/SonificationUtilities.js']], function (Sonification, U, SU) {
        /* *
         *
         *  (c) 2009-2021 Øystein Moseng
         *
         *  TimelineEvent class definition.
         *
         *  License: www.highcharts.com/license
         *
         *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
         *
         * */
        var merge = U.merge,
            splat = U.splat;
        /**
         * Internal types.
         * @private
         */
        /* eslint-disable no-invalid-this, valid-jsdoc */
        /* *
         *
         *  Class
         *
         * */
        /**
         * The Timeline class. Represents a sonification timeline with a list of
         * timeline paths with events to play at certain times relative to each other.
         *
         * @requires module:modules/sonification
         *
         * @private
         * @class
         * @name Highcharts.Timeline
         *
         * @param {Highcharts.TimelineOptionsObject} options
         *        Options for the Timeline.
         */
        var Timeline = /** @class */ (function () {
                /* *
                 *
                 *  Constructor
                 *
                 * */
                function Timeline(options) {
                    /* *
                     *
                     *  Properties
                     *
                     * */
                    this.cursor = void 0;
                this.options = void 0;
                this.paths = void 0;
                this.pathsPlaying = void 0;
                this.signalHandler = void 0;
                this.init(options || {});
            }
            /* *
             *
             *  Functions
             *
             * */
            Timeline.prototype.init = function (options) {
                this.options = options;
                this.cursor = 0;
                this.paths = options.paths || [];
                this.pathsPlaying = {};
                this.signalHandler = new SU.SignalHandler(['playOnEnd', 'masterOnEnd', 'onPathStart', 'onPathEnd']);
                this.signalHandler.registerSignalCallbacks(merge(options, { masterOnEnd: options.onEnd }));
            };
            /**
             * Play the timeline forwards from cursor.
             * @private
             * @param {Function} [onEnd]
             * Callback to call when play finished. Does not override other onEnd
             * callbacks.
             */
            Timeline.prototype.play = function (onEnd) {
                this.pause();
                this.signalHandler.clearSignalCallbacks(['playOnEnd']);
                this.signalHandler.registerSignalCallbacks({ playOnEnd: onEnd });
                this.playPaths(1);
            };
            /**
             * Play the timeline backwards from cursor.
             * @private
             * @param {Function} onEnd
             * Callback to call when play finished. Does not override other onEnd
             * callbacks.
             */
            Timeline.prototype.rewind = function (onEnd) {
                this.pause();
                this.signalHandler.clearSignalCallbacks(['playOnEnd']);
                this.signalHandler.registerSignalCallbacks({ playOnEnd: onEnd });
                this.playPaths(-1);
            };
            /**
             * Play the timeline in the specified direction.
             * @private
             * @param {number} direction
             * Direction to play in. 1 for forwards, -1 for backwards.
             */
            Timeline.prototype.playPaths = function (direction) {
                var timeline = this,
                    signalHandler = timeline.signalHandler;
                if (!timeline.paths.length) {
                    var emptySignal = {
                            cancelled: false
                        };
                    signalHandler.emitSignal('playOnEnd', emptySignal);
                    signalHandler.emitSignal('masterOnEnd', emptySignal);
                    return;
                }
                var curPaths = splat(this.paths[this.cursor]),
                    nextPaths = this.paths[this.cursor + direction], 
                    // Play a path
                    playPath = function (path) {
                        // Emit signal and set playing state
                        signalHandler.emitSignal('onPathStart',
                    path);
                    timeline.pathsPlaying[path.id] = path;
                    // Do the play
                    path[direction > 0 ? 'play' : 'rewind'](function (callbackData) {
                        // Play ended callback
                        // Data to pass to signal callbacks
                        var cancelled = callbackData && callbackData.cancelled,
                            signalData = {
                                path: path,
                                cancelled: cancelled
                            };
                        // Clear state and send signal
                        delete timeline.pathsPlaying[path.id];
                        signalHandler.emitSignal('onPathEnd', signalData);
                        // Handle next paths
                        var pathsEnded = 0;
                        pathsEnded++;
                        if (pathsEnded >= curPaths.length) {
                            // We finished all of the current paths for cursor.
                            if (nextPaths && !cancelled) {
                                // We have more paths, move cursor along
                                timeline.cursor += direction;
                                // Reset upcoming path cursors before playing
                                splat(nextPaths).forEach(function (nextPath) {
                                    nextPath[direction > 0 ?
                                        'resetCursor' : 'resetCursorEnd']();
                                });
                                // Play next
                                timeline.playPaths(direction);
                            }
                            else {
                                // If it is the last path in this direction,
                                // call onEnd
                                signalHandler.emitSignal('playOnEnd', signalData);
                                signalHandler.emitSignal('masterOnEnd', signalData);
                            }
                        }
                    });
                };
                // Go through the paths under cursor and play them
                curPaths.forEach(function (path) {
                    if (path) {
                        // Store reference to timeline
                        path.timeline = timeline;
                        // Leave a timeout to let notes fade out before next play
                        setTimeout(function () {
                            playPath(path);
                        }, Sonification.fadeOutDuration);
                    }
                });
            };
            /**
             * Stop the playing of the timeline. Cancels all current sounds, but does
             * not affect the cursor.
             * @private
             * @param {boolean} [fadeOut=false]
             * Whether or not to fade out as we stop. If false, the timeline is
             * cancelled synchronously.
             */
            Timeline.prototype.pause = function (fadeOut) {
                var timeline = this;
                // Cancel currently playing events
                Object.keys(timeline.pathsPlaying).forEach(function (id) {
                    if (timeline.pathsPlaying[id]) {
                        timeline.pathsPlaying[id].pause(fadeOut);
                    }
                });
                timeline.pathsPlaying = {};
            };
            /**
             * Reset the cursor to the beginning of the timeline.
             * @private
             */
            Timeline.prototype.resetCursor = function () {
                this.paths.forEach(function (paths) {
                    splat(paths).forEach(function (path) {
                        path.resetCursor();
                    });
                });
                this.cursor = 0;
            };
            /**
             * Reset the cursor to the end of the timeline.
             * @private
             */
            Timeline.prototype.resetCursorEnd = function () {
                this.paths.forEach(function (paths) {
                    splat(paths).forEach(function (path) {
                        path.resetCursorEnd();
                    });
                });
                this.cursor = this.paths.length - 1;
            };
            /**
             * Set the current TimelineEvent under the cursor. If multiple paths are
             * being played at the same time, this function only affects a single path
             * (the one that contains the eventId that is passed in).
             * @private
             * @param {string} eventId
             * The ID of the timeline event to set as current.
             * @return {boolean}
             * True if the cursor was set, false if no TimelineEvent was found for
             * this ID.
             */
            Timeline.prototype.setCursor = function (eventId) {
                return this.paths.some(function (paths) {
                    return splat(paths).some(function (path) {
                        return path.setCursor(eventId);
                    });
                });
            };
            /**
             * Get the current TimelineEvents under the cursors. This function will
             * return the event under the cursor for each currently playing path, as an
             * object where the path ID is mapped to the TimelineEvent under that
             * path's cursor.
             * @private
             * @return {Highcharts.Dictionary<Highcharts.TimelineEvent>}
             * The TimelineEvents under each path's cursors.
             */
            Timeline.prototype.getCursor = function () {
                return this.getCurrentPlayingPaths().reduce(function (acc, cur) {
                    acc[cur.id] = cur.getCursor();
                    return acc;
                }, {});
            };
            /**
             * Check if timeline is reset or at start.
             * @private
             * @return {boolean}
             * True if timeline is at the beginning.
             */
            Timeline.prototype.atStart = function () {
                if (this.cursor) {
                    return false;
                }
                return !splat(this.paths[0]).some(function (path) {
                    return path.cursor;
                });
            };
            /**
             * Get the current TimelinePaths being played.
             * @private
             * @return {Array<Highcharts.TimelinePath>}
             * The TimelinePaths currently being played.
             */
            Timeline.prototype.getCurrentPlayingPaths = function () {
                if (!this.paths.length) {
                    return [];
                }
                return splat(this.paths[this.cursor]);
            };
            return Timeline;
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
         * A set of options for the Timeline class.
         *
         * @requires module:modules/sonification
         *
         * @private
         * @interface Highcharts.TimelineOptionsObject
         */ /**
        * List of TimelinePaths to play. Multiple paths can be grouped together and
        * played simultaneously by supplying an array of paths in place of a single
        * path.
        * @name Highcharts.TimelineOptionsObject#paths
        * @type {Array<(Highcharts.TimelinePath|Array<Highcharts.TimelinePath>)>}
        */ /**
        * Callback function to call before a path plays.
        * @name Highcharts.TimelineOptionsObject#onPathStart
        * @type {Function|undefined}
        */ /**
        * Callback function to call after a path has stopped playing.
        * @name Highcharts.TimelineOptionsObject#onPathEnd
        * @type {Function|undefined}
        */ /**
        * Callback called when the whole path is finished.
        * @name Highcharts.TimelineOptionsObject#onEnd
        * @type {Function|undefined}
        */
        (''); // detach doclets above

        return Timeline;
    });
    _registerModule(_modules, 'Extensions/Sonification/TimelineEvent.js', [_modules['Core/Utilities.js']], function (U) {
        /* *
         *
         *  (c) 2009-2021 Øystein Moseng
         *
         *  TimelineEvent class definition.
         *
         *  License: www.highcharts.com/license
         *
         *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
         *
         * */
        var merge = U.merge,
            uniqueKey = U.uniqueKey;
        /* eslint-disable no-invalid-this, valid-jsdoc */
        /* *
         *
         *  Class
         *
         * */
        /**
         * The TimelineEvent class. Represents a sound event on a timeline.
         *
         * @requires module:modules/sonification
         *
         * @private
         * @class
         * @name Highcharts.TimelineEvent
         *
         * @param {Highcharts.TimelineEventOptionsObject} options
         * Options for the TimelineEvent.
         */
        var TimelineEvent = /** @class */ (function () {
                /* *
                 *
                 *  Constructor
                 *
                 * */
                function TimelineEvent(options) {
                    /* *
                     *
                     *  Properties
                     *
                     * */
                    this.id = void 0;
                this.options = void 0;
                this.time = void 0;
                this.init(options);
            }
            /* *
             *
             *  Functions
             *
             * */
            TimelineEvent.prototype.init = function (options) {
                this.options = options;
                this.time = options.time || 0;
                this.id = this.options.id = options.id || uniqueKey();
            };
            /**
             * Play the event. Does not take the TimelineEvent.time option into account,
             * and plays the event immediately.
             *
             * @function Highcharts.TimelineEvent#play
             *
             * @param {Highcharts.TimelineEventOptionsObject} [options]
             *        Options to pass in to the eventObject when playing it.
             *
             */
            TimelineEvent.prototype.play = function (options) {
                var eventObject = this.options.eventObject,
                    masterOnEnd = this.options.onEnd,
                    playOnEnd = options && options.onEnd,
                    playOptionsOnEnd = this.options.playOptions &&
                        this.options.playOptions.onEnd,
                    playOptions = merge(this.options.playOptions,
                    options);
                if (eventObject && eventObject.sonify) {
                    // If we have multiple onEnds defined, use all
                    playOptions.onEnd = masterOnEnd || playOnEnd || playOptionsOnEnd ?
                        function () {
                            var args = arguments;
                            [masterOnEnd, playOnEnd, playOptionsOnEnd].forEach(function (onEnd) {
                                if (onEnd) {
                                    onEnd.apply(this, args);
                                }
                            });
                        } : void 0;
                    eventObject.sonify(playOptions);
                }
                else {
                    if (playOnEnd) {
                        playOnEnd();
                    }
                    if (masterOnEnd) {
                        masterOnEnd();
                    }
                }
            };
            /**
             * Cancel the sonification of this event. Does nothing if the event is not
             * currently sonifying.
             *
             * @function Highcharts.TimelineEvent#cancel
             *
             * @param {boolean} [fadeOut=false]
             *        Whether or not to fade out as we stop. If false, the event is
             *        cancelled synchronously.
             */
            TimelineEvent.prototype.cancel = function (fadeOut) {
                var eventObject = this.options.eventObject;
                if (eventObject) {
                    eventObject.cancelSonify(fadeOut);
                }
            };
            return TimelineEvent;
        }());
        /* *
         *
         *  Default export
         *
         * */
        /* *
         *
         *  API Declarations
         *
         * */
        /**
         * A set of options for the TimelineEvent class.
         *
         * @requires module:modules/sonification
         *
         * @private
         * @interface Highcharts.TimelineEventOptionsObject
         */ /**
        * The object we want to sonify when playing the TimelineEvent. Can be any
        * object that implements the `sonify` and `cancelSonify` functions. If this is
        * not supplied, the TimelineEvent is considered a silent event, and the onEnd
        * event is immediately called.
        * @name Highcharts.TimelineEventOptionsObject#eventObject
        * @type {*}
        */ /**
        * Options to pass on to the eventObject when playing it.
        * @name Highcharts.TimelineEventOptionsObject#playOptions
        * @type {object|undefined}
        */ /**
        * The time at which we want this event to play (in milliseconds offset). This
        * is not used for the TimelineEvent.play function, but rather intended as a
        * property to decide when to call TimelineEvent.play. Defaults to 0.
        * @name Highcharts.TimelineEventOptionsObject#time
        * @type {number|undefined}
        */ /**
        * Unique ID for the event. Generated automatically if not supplied.
        * @name Highcharts.TimelineEventOptionsObject#id
        * @type {string|undefined}
        */ /**
        * Callback called when the play has finished.
        * @name Highcharts.TimelineEventOptionsObject#onEnd
        * @type {Function|undefined}
        */
        (''); // detach doclets above

        return TimelineEvent;
    });
    _registerModule(_modules, 'Extensions/Sonification/TimelinePath.js', [_modules['Extensions/Sonification/TimelineEvent.js'], _modules['Extensions/Sonification/SonificationUtilities.js'], _modules['Core/Utilities.js']], function (TimelineEvent, SU, U) {
        /* *
         *
         *  (c) 2009-2021 Øystein Moseng
         *
         *  TimelineEvent class definition.
         *
         *  License: www.highcharts.com/license
         *
         *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
         *
         * */
        var merge = U.merge,
            uniqueKey = U.uniqueKey;
        /* *
         *
         *  Class
         *
         * */
        /* eslint-disable no-invalid-this, valid-jsdoc */
        /**
         * The TimelinePath class. Represents a track on a timeline with a list of
         * sound events to play at certain times relative to each other.
         *
         * @requires module:modules/sonification
         *
         * @private
         * @class
         * @name Highcharts.TimelinePath
         *
         * @param {Highcharts.TimelinePathOptionsObject} options
         *        Options for the TimelinePath.
         */
        var TimelinePath = /** @class */ (function () {
                /* *
                 *
                 *  Constructors
                 *
                 * */
                function TimelinePath(options) {
                    /* *
                    *
                    *  Properties
                    *
                    * */
                    this.cursor = void 0;
                this.events = void 0;
                this.eventIdMap = void 0;
                this.eventsPlaying = void 0;
                this.id = void 0;
                this.options = void 0;
                this.signalHandler = void 0;
                this.init(options);
            }
            /* *
             *
             *  Functions
             *
             * */
            TimelinePath.prototype.init = function (options) {
                this.options = options;
                this.id = this.options.id = options.id || uniqueKey();
                this.cursor = 0;
                this.eventsPlaying = {};
                // Handle silent wait, otherwise use events from options
                this.events = options.silentWait ?
                    [
                        new TimelineEvent({ time: 0 }),
                        new TimelineEvent({ time: options.silentWait })
                    ] :
                    this.options.events;
                // Reference optionally provided by the user that indicates the intended
                // duration of the path. Unused by TimelinePath itself.
                this.targetDuration = options.targetDuration || options.silentWait;
                // We need to sort our events by time
                this.sortEvents();
                // Get map from event ID to index
                this.updateEventIdMap();
                // Signal events to fire
                this.signalHandler = new SU.SignalHandler([
                    'playOnEnd', 'masterOnEnd', 'onStart', 'onEventStart', 'onEventEnd'
                ]);
                this.signalHandler.registerSignalCallbacks(merge(options, { masterOnEnd: options.onEnd }));
            };
            /**
             * Sort the internal event list by time.
             * @private
             */
            TimelinePath.prototype.sortEvents = function () {
                this.events = this.events.sort(function (a, b) {
                    return a.time - b.time;
                });
            };
            /**
             * Update the internal eventId to index map.
             * @private
             */
            TimelinePath.prototype.updateEventIdMap = function () {
                this.eventIdMap = this.events.reduce(function (acc, cur, i) {
                    acc[cur.id] = i;
                    return acc;
                }, {});
            };
            /**
             * Add events to the path. Should not be done while the path is playing.
             * The new events are inserted according to their time property.
             * @private
             * @param {Array<Highcharts.TimelineEvent>} newEvents
             * The new timeline events to add.
             */
            TimelinePath.prototype.addTimelineEvents = function (newEvents) {
                this.events = this.events.concat(newEvents);
                this.sortEvents(); // Sort events by time
                this.updateEventIdMap(); // Update the event ID to index map
            };
            /**
             * Get the current TimelineEvent under the cursor.
             * @private
             * @return {Highcharts.TimelineEvent} The current timeline event.
             */
            TimelinePath.prototype.getCursor = function () {
                return this.events[this.cursor];
            };
            /**
             * Set the current TimelineEvent under the cursor.
             * @private
             * @param {string} eventId
             * The ID of the timeline event to set as current.
             * @return {boolean}
             * True if there is an event with this ID in the path. False otherwise.
             */
            TimelinePath.prototype.setCursor = function (eventId) {
                var ix = this.eventIdMap[eventId];
                if (typeof ix !== 'undefined') {
                    this.cursor = ix;
                    return true;
                }
                return false;
            };
            /**
             * Play the timeline from the current cursor.
             * @private
             * @param {Function} onEnd
             * Callback to call when play finished. Does not override other onEnd
             * callbacks.
             */
            TimelinePath.prototype.play = function (onEnd) {
                this.pause();
                this.signalHandler.emitSignal('onStart');
                this.signalHandler.clearSignalCallbacks(['playOnEnd']);
                this.signalHandler.registerSignalCallbacks({ playOnEnd: onEnd });
                this.playEvents(1);
            };
            /**
             * Play the timeline backwards from the current cursor.
             * @private
             * @param {Function} onEnd
             * Callback to call when play finished. Does not override other onEnd
             * callbacks.
             */
            TimelinePath.prototype.rewind = function (onEnd) {
                this.pause();
                this.signalHandler.emitSignal('onStart');
                this.signalHandler.clearSignalCallbacks(['playOnEnd']);
                this.signalHandler.registerSignalCallbacks({ playOnEnd: onEnd });
                this.playEvents(-1);
            };
            /**
             * Reset the cursor to the beginning.
             * @private
             */
            TimelinePath.prototype.resetCursor = function () {
                this.cursor = 0;
            };
            /**
             * Reset the cursor to the end.
             * @private
             */
            TimelinePath.prototype.resetCursorEnd = function () {
                this.cursor = this.events.length - 1;
            };
            /**
             * Cancel current playing. Leaves the cursor intact.
             * @private
             * @param {boolean} [fadeOut=false]
             * Whether or not to fade out as we stop. If false, the path is cancelled
             * synchronously.
             */
            TimelinePath.prototype.pause = function (fadeOut) {
                var timelinePath = this;
                // Cancel next scheduled play
                clearTimeout(timelinePath.nextScheduledPlay);
                // Cancel currently playing events
                Object.keys(timelinePath.eventsPlaying).forEach(function (id) {
                    if (timelinePath.eventsPlaying[id]) {
                        timelinePath.eventsPlaying[id].cancel(fadeOut);
                    }
                });
                timelinePath.eventsPlaying = {};
            };
            /**
             * Play the events, starting from current cursor, and going in specified
             * direction.
             * @private
             * @param {number} direction
             * The direction to play, 1 for forwards and -1 for backwards.
             */
            TimelinePath.prototype.playEvents = function (direction) {
                var timelinePath = this,
                    curEvent = timelinePath.events[this.cursor],
                    nextEvent = timelinePath.events[this.cursor + direction],
                    onEnd = function (signalData) {
                        timelinePath.signalHandler.emitSignal('masterOnEnd',
                    signalData);
                    timelinePath.signalHandler.emitSignal('playOnEnd', signalData);
                };
                var timeDiff;
                // Store reference to path on event
                curEvent.timelinePath = timelinePath;
                // Emit event, cancel if returns false
                if (timelinePath.signalHandler.emitSignal('onEventStart', curEvent) === false) {
                    onEnd({
                        event: curEvent,
                        cancelled: true
                    });
                    return;
                }
                // Play the current event
                timelinePath.eventsPlaying[curEvent.id] = curEvent;
                curEvent.play({
                    onEnd: function (cancelled) {
                        var signalData = {
                                event: curEvent,
                                cancelled: !!cancelled
                            };
                        // Keep track of currently playing events for cancelling
                        delete timelinePath.eventsPlaying[curEvent.id];
                        // Handle onEventEnd
                        timelinePath.signalHandler.emitSignal('onEventEnd', signalData);
                        // Reached end of path?
                        if (!nextEvent) {
                            onEnd(signalData);
                        }
                    }
                });
                // Schedule next
                if (nextEvent) {
                    timeDiff = Math.abs(nextEvent.time - curEvent.time);
                    if (timeDiff < 1) {
                        // Play immediately
                        timelinePath.cursor += direction;
                        timelinePath.playEvents(direction);
                    }
                    else {
                        // Schedule after the difference in ms
                        this.nextScheduledPlay = setTimeout(function () {
                            timelinePath.cursor += direction;
                            timelinePath.playEvents(direction);
                        }, timeDiff);
                    }
                }
            };
            return TimelinePath;
        }());
        /* *
         *
         *  Default export
         *
         * */
        /* *
         *
         *  API Declarations
         *
         * */
        /**
         * A set of options for the TimelinePath class.
         *
         * @requires module:modules/
         *
         * @private
         * @interface Highcharts.TimelinePathOptionsObject
         */ /**
        * List of TimelineEvents to play on this track.
        * @name Highcharts.TimelinePathOptionsObject#events
        * @type {Array<Highcharts.TimelineEvent>}
        */ /**
        * If this option is supplied, this path ignores all events and just waits for
        * the specified number of milliseconds before calling onEnd.
        * @name Highcharts.TimelinePathOptionsObject#silentWait
        * @type {number|undefined}
        */ /**
        * Unique ID for this timeline path. Automatically generated if not supplied.
        * @name Highcharts.TimelinePathOptionsObject#id
        * @type {string|undefined}
        */ /**
        * Callback called before the path starts playing.
        * @name Highcharts.TimelinePathOptionsObject#onStart
        * @type {Function|undefined}
        */ /**
        * Callback function to call before an event plays.
        * @name Highcharts.TimelinePathOptionsObject#onEventStart
        * @type {Function|undefined}
        */ /**
        * Callback function to call after an event has stopped playing.
        * @name Highcharts.TimelinePathOptionsObject#onEventEnd
        * @type {Function|undefined}
        */ /**
        * Callback called when the whole path is finished.
        * @name Highcharts.TimelinePathOptionsObject#onEnd
        * @type {Function|undefined}
        */
        (''); // detach doclets above

        return TimelinePath;
    });
    _registerModule(_modules, 'Extensions/Sonification/SeriesSonify.js', [_modules['Extensions/Sonification/Earcon.js'], _modules['Extensions/Sonification/Instrument.js'], _modules['Core/Series/Point.js'], _modules['Extensions/Sonification/SonificationUtilities.js'], _modules['Extensions/Sonification/Timeline.js'], _modules['Extensions/Sonification/TimelineEvent.js'], _modules['Extensions/Sonification/TimelinePath.js'], _modules['Core/Utilities.js']], function (Earcon, Instrument, Point, SU, Timeline, TimelineEvent, TimelinePath, U) {
        /* *
         *
         *  (c) 2009-2021 Øystein Moseng
         *
         *  Sonification functions for chart/series.
         *
         *  License: www.highcharts.com/license
         *
         *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
         *
         * */
        var getExtremesForInstrumentProps = SU.getExtremesForInstrumentProps,
            virtualAxisTranslate = SU.virtualAxisTranslate;
        var extend = U.extend,
            find = U.find,
            isArray = U.isArray,
            merge = U.merge,
            objectEach = U.objectEach,
            pick = U.pick;
        /* *
         *
         *  Compositions
         *
         * */
        var SeriesSonify;
        (function (SeriesSonify) {
            /* *
             *
             *  Declarations
             *
             * */
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
            /* eslint-disable valid-jsdoc */
            /**
             * @private
             */
            function compose(SeriesClass) {
                if (composedClasses.indexOf(SeriesClass) === -1) {
                    composedClasses.push(SeriesClass);
                    var seriesProto = SeriesClass.prototype;
                    extend(seriesProto, {
                        sonify: sonify
                    });
                }
                return SeriesClass;
            }
            SeriesSonify.compose = compose;
            /**
             * Utility function to apply a master volume to a list of instrument
             * options.
             * @private
             * @param {Array<Highcharts.PointInstrumentObject>} instruments
             * The instrument options. Only options with Instrument object instances
             * will be affected.
             * @param {number} masterVolume
             * The master volume multiplier to apply to the instruments.
             * @return {Array<Highcharts.PointInstrumentObject>}
             * Array of instrument options.
             */
            function applyMasterVolumeToInstruments(instruments, masterVolume) {
                instruments.forEach(function (instrOpts) {
                    var instr = instrOpts.instrument;
                    if (typeof instr !== 'string') {
                        instr.setMasterVolume(masterVolume);
                    }
                });
                return instruments;
            }
            /**
             * Utility function to assemble options for creating a TimelinePath from a
             * series when sonifying an entire chart.
             * @private
             * @param {Highcharts.Series} series
             * The series to return options for.
             * @param {Highcharts.RangeObject} dataExtremes
             * Pre-calculated data extremes for the chart.
             * @param {Highcharts.SonificationOptions} chartSonifyOptions
             * Options passed in to chart.sonify.
             * @return {Partial<Highcharts.SonifySeriesOptionsObject>}
             * Options for buildTimelinePathFromSeries.
             */
            function buildChartSonifySeriesOptions(series, dataExtremes, chartSonifyOptions) {
                var additionalSeriesOptions = chartSonifyOptions.seriesOptions || {},
                    sonification = series.chart.options.sonification,
                    pointPlayTime = (sonification &&
                        sonification.defaultInstrumentOptions &&
                        sonification.defaultInstrumentOptions.mapping &&
                        sonification.defaultInstrumentOptions.mapping.pointPlayTime ||
                        'x'),
                    configOptions = chartOptionsToSonifySeriesOptions(series);
                return merge(
                // Options from chart configuration
                configOptions, 
                // Options passed in
                {
                    // Calculated dataExtremes for chart
                    dataExtremes: dataExtremes,
                    // We need to get timeExtremes for each series. We pass this
                    // in when building the TimelinePath objects to avoid
                    // calculating twice.
                    timeExtremes: getTimeExtremes(series, pointPlayTime),
                    // Some options we just pass on
                    instruments: (chartSonifyOptions.instruments || configOptions.instruments),
                    onStart: (chartSonifyOptions.onSeriesStart || configOptions.onStart),
                    onEnd: chartSonifyOptions.onSeriesEnd || configOptions.onEnd,
                    earcons: chartSonifyOptions.earcons || configOptions.earcons,
                    masterVolume: pick(chartSonifyOptions.masterVolume, configOptions.masterVolume)
                }, 
                // Merge in the specific series options by ID if any are passed in
                isArray(additionalSeriesOptions) ? (find(additionalSeriesOptions, function (optEntry) {
                    return optEntry.id === pick(series.id, series.options.id);
                }) || {}) : additionalSeriesOptions, {
                    // Forced options
                    pointPlayTime: pointPlayTime
                });
            }
            SeriesSonify.buildChartSonifySeriesOptions = buildChartSonifySeriesOptions;
            /**
             * Create a TimelinePath from a series. Takes the same options as
             * seriesSonify. To intuitively allow multiple series to play simultaneously
             * we make copies of the instruments for each series.
             * @private
             * @param {Highcharts.Series} series
             * The series to build from.
             * @param {Highcharts.SonifySeriesOptionsObject} options
             * The options for building the TimelinePath.
             * @return {Highcharts.TimelinePath}
             * A timeline path with events.
             */
            function buildTimelinePathFromSeries(series, options) {
                // options.timeExtremes is internal and used so that the calculations
                // from chart.sonify can be reused.
                var timeExtremes = options.timeExtremes || getTimeExtremes(series,
                    options.pointPlayTime), 
                    // Compute any data extremes that aren't defined yet
                    dataExtremes = getExtremesForInstrumentProps(series.chart,
                    options.instruments,
                    options.dataExtremes),
                    minimumSeriesDurationMs = 10, 
                    // Get the duration of the final note
                    finalNoteDuration = getFinalNoteDuration(series,
                    options.instruments,
                    dataExtremes), 
                    // Get time offset for a point, relative to duration
                    pointToTime = function (point) {
                        return virtualAxisTranslate(getPointTimeValue(point,
                    options.pointPlayTime),
                    timeExtremes, {
                            min: 0,
                            max: Math.max(options.duration - finalNoteDuration,
                    minimumSeriesDurationMs)
                        });
                }, masterVolume = pick(options.masterVolume, 1), 
                // Make copies of the instruments used for this series, to allow
                // multiple series with the same instrument to play together
                instrumentCopies = makeInstrumentCopies(options.instruments), instruments = applyMasterVolumeToInstruments(instrumentCopies, masterVolume), 
                // Go through the points, convert to events, optionally add Earcons
                timelineEvents = series.points.reduce(function (events, point) {
                    var earcons = getPointEarcons(point,
                        options.earcons || []),
                        time = pointToTime(point);
                    return events.concat(
                    // Event object for point
                    new TimelineEvent({
                        eventObject: point,
                        time: time,
                        id: point.id,
                        playOptions: {
                            instruments: instruments,
                            dataExtremes: dataExtremes,
                            masterVolume: masterVolume
                        }
                    }), 
                    // Earcons
                    earcons.map(function (earcon) {
                        return new TimelineEvent({
                            eventObject: earcon,
                            time: time,
                            playOptions: {
                                volume: masterVolume
                            }
                        });
                    }));
                }, []);
                // Build the timeline path
                return new TimelinePath({
                    events: timelineEvents,
                    onStart: function () {
                        if (options.onStart) {
                            options.onStart(series);
                        }
                    },
                    onEventStart: function (event) {
                        var eventObject = event.options && event.options.eventObject;
                        if (eventObject instanceof Point) {
                            // Check for hidden series
                            if (!eventObject.series.visible &&
                                !eventObject.series.chart.series.some(function (series) {
                                    return series.visible;
                                })) {
                                // We have no visible series, stop the path.
                                event.timelinePath.timeline.pause();
                                event.timelinePath.timeline.resetCursor();
                                return false;
                            }
                            // Emit onPointStart
                            if (options.onPointStart) {
                                options.onPointStart(event, eventObject);
                            }
                        }
                    },
                    onEventEnd: function (eventData) {
                        var eventObject = (eventData.event &&
                                eventData.event.options &&
                                eventData.event.options.eventObject);
                        if (eventObject instanceof Point && options.onPointEnd) {
                            options.onPointEnd(eventData.event, eventObject);
                        }
                    },
                    onEnd: function () {
                        if (options.onEnd) {
                            options.onEnd(series);
                        }
                    },
                    targetDuration: options.duration
                });
            }
            SeriesSonify.buildTimelinePathFromSeries = buildTimelinePathFromSeries;
            /**
             * Utility function to translate between options set in chart configuration
             * and a SonifySeriesOptionsObject.
             * @private
             * @param {Highcharts.Series} series
             * The series to get options for.
             * @return {Highcharts.SonifySeriesOptionsObject}
             * Options for chart/series.sonify()
             */
            function chartOptionsToSonifySeriesOptions(series) {
                var seriesOpts = series.options.sonification ||
                        {},
                    chartOpts = series.chart.options.sonification ||
                        {},
                    chartEvents = chartOpts.events ||
                        {},
                    seriesEvents = seriesOpts.events ||
                        {};
                return {
                    onEnd: seriesEvents.onSeriesEnd || chartEvents.onSeriesEnd,
                    onStart: seriesEvents.onSeriesStart || chartEvents.onSeriesStart,
                    onPointEnd: seriesEvents.onPointEnd || chartEvents.onPointEnd,
                    onPointStart: seriesEvents.onPointStart || chartEvents.onPointStart,
                    pointPlayTime: (chartOpts.defaultInstrumentOptions &&
                        chartOpts.defaultInstrumentOptions.mapping &&
                        chartOpts.defaultInstrumentOptions.mapping.pointPlayTime),
                    masterVolume: chartOpts.masterVolume,
                    // Deals with chart-level defaults
                    instruments: getSeriesInstrumentOptions(series),
                    earcons: seriesOpts.earcons || chartOpts.earcons
                };
            }
            /**
             * Utility function to find the duration of the final note in a series.
             * @private
             * @param {Highcharts.Series} series The data series to calculate on.
             * @param {Array<Highcharts.PointInstrumentObject>} instruments The instrument options for this series.
             * @param {Highcharts.Dictionary<Highcharts.RangeObject>} dataExtremes Value extremes for the data series props.
             * @return {number} The duration of the final note in milliseconds.
             */
            function getFinalNoteDuration(series, instruments, dataExtremes) {
                var finalPoint = series.points[series.points.length - 1];
                return instruments.reduce(function (duration, instrument) {
                    var mapping = instrument.instrumentMapping.duration;
                    var instrumentDuration;
                    if (typeof mapping === 'string') {
                        instrumentDuration = 0; // Ignore, no easy way to map this
                    }
                    else if (typeof mapping === 'function') {
                        instrumentDuration = mapping(finalPoint, dataExtremes);
                    }
                    else {
                        instrumentDuration = mapping;
                    }
                    return Math.max(duration, instrumentDuration);
                }, 0);
            }
            /**
             * Get earcons for the point if there are any.
             * @private
             * @param {Highcharts.Point} point
             * The point to find earcons for.
             * @param {Array<Highcharts.EarconConfiguration>} earconDefinitions
             * Earcons to check.
             * @return {Array<Highcharts.Earcon>}
             * Array of earcons to be played with this point.
             */
            function getPointEarcons(point, earconDefinitions) {
                return earconDefinitions.reduce(function (earcons, earconDefinition) {
                    var earcon = earconDefinition.earcon;
                    var cond;
                    if (earconDefinition.condition) {
                        // We have a condition. This overrides onPoint
                        cond = earconDefinition.condition(point);
                        if (cond instanceof Earcon) {
                            // Condition returned an earcon
                            earcons.push(cond);
                        }
                        else if (cond) {
                            // Condition returned true
                            earcons.push(earcon);
                        }
                    }
                    else if (earconDefinition.onPoint &&
                        point.id === earconDefinition.onPoint) {
                        // We have earcon onPoint
                        earcons.push(earcon);
                    }
                    return earcons;
                }, []);
            }
            /**
             * Get the relative time value of a point.
             * @private
             * @param {Highcharts.Point} point
             * The point.
             * @param {Function|string} timeProp
             * The time axis data prop or the time function.
             * @return {number}
             * The time value.
             */
            function getPointTimeValue(point, timeProp) {
                return typeof timeProp === 'function' ?
                    timeProp(point) :
                    pick(point[timeProp], point.options[timeProp]);
            }
            /**
             * @private
             * @param {Highcharts.Series} series
             * The series to get options for.
             * @param {Highcharts.SonifySeriesOptionsObject} options
             * Options to merge with user options on series/chart and default options.
             * @return {Array<Highcharts.PointInstrumentObject>}
             * The merged options.
             */
            function getSeriesInstrumentOptions(series, options) {
                if (options && options.instruments) {
                    return options.instruments;
                }
                var defaultInstrOpts = (series.chart.options.sonification &&
                        series.chart.options.sonification.defaultInstrumentOptions ||
                        {}),
                    seriesInstrOpts = (series.options.sonification &&
                        series.options.sonification.instruments ||
                        [{}]),
                    removeNullsFromObject = function (obj) {
                        objectEach(obj,
                    function (val,
                    key) {
                            if (val === null) {
                                delete obj[key];
                        }
                    });
                };
                // Convert series options to PointInstrumentObjects and merge with
                // default options
                return (seriesInstrOpts).map(function (optionSet) {
                    // Allow setting option to null to use default
                    removeNullsFromObject(optionSet.mapping || {});
                    removeNullsFromObject(optionSet);
                    return {
                        instrument: optionSet.instrument || defaultInstrOpts.instrument,
                        instrumentOptions: merge(defaultInstrOpts, optionSet, {
                            // Instrument options are lifted to root in the API options
                            // object, so merge all in order to avoid missing any. But
                            // remove the following which are not instrumentOptions:
                            mapping: void 0,
                            instrument: void 0
                        }),
                        instrumentMapping: merge(defaultInstrOpts.mapping, optionSet.mapping)
                    };
                });
            }
            /**
             * @private
             * @param {Highcharts.Series} series
             * The series to get options for.
             * @param {Highcharts.SonifySeriesOptionsObject} options
             * Options to merge with user options on series/chart and default options.
             * @return {Highcharts.SonifySeriesOptionsObject}
             * The merged options.
             */
            function getSeriesSonifyOptions(series, options) {
                var chartOpts = series.chart.options.sonification,
                    seriesOpts = series.options.sonification;
                return merge({
                    duration: ((seriesOpts && seriesOpts.duration) ||
                        (chartOpts && chartOpts.duration))
                }, chartOptionsToSonifySeriesOptions(series), options);
            }
            /**
             * Get the time extremes of this series. This is handled outside of the
             * dataExtremes, as we always want to just sonify the visible points, and we
             * always want the extremes to be the extremes of the visible points.
             * @private
             * @param {Highcharts.Series} series
             * The series to compute on.
             * @param {Function|string} timeProp
             * The time axis data prop or the time function.
             * @return {Highcharts.RangeObject}
             * Object with min/max extremes for the time values.
             */
            function getTimeExtremes(series, timeProp) {
                // Compute the extremes from the visible points.
                return series.points.reduce(function (acc, point) {
                    var value = getPointTimeValue(point,
                        timeProp);
                    acc.min = Math.min(acc.min, value);
                    acc.max = Math.max(acc.max, value);
                    return acc;
                }, {
                    min: Infinity,
                    max: -Infinity
                });
            }
            /**
             * Utility function to get a new list of instrument options where all the
             * instrument references are copies.
             * @private
             * @param {Array<Highcharts.PointInstrumentObject>} instruments
             * The instrument options.
             * @return {Array<Highcharts.PointInstrumentObject>}
             * Array of copied instrument options.
             */
            function makeInstrumentCopies(instruments) {
                return instruments.map(function (instrumentDef) {
                    var instrument = instrumentDef.instrument,
                        copy = (typeof instrument === 'string' ?
                            Instrument.definitions[instrument] :
                            instrument).copy();
                    return merge(instrumentDef, { instrument: copy });
                });
            }
            /**
             * Sonify a series.
             *
             * @sample highcharts/sonification/series-basic/
             *         Click on series to sonify
             * @sample highcharts/sonification/series-earcon/
             *         Series with earcon
             * @sample highcharts/sonification/point-play-time/
             *         Play y-axis by time
             * @sample highcharts/sonification/earcon-on-point/
             *         Earcon set on point
             *
             * @requires module:modules/sonification
             *
             * @function Highcharts.Series#sonify
             *
             * @param {Highcharts.SonifySeriesOptionsObject} [options]
             * The options for sonifying this series. If not provided, uses options set
             * on chart and series.
             */
            function sonify(options) {
                var mergedOptions = getSeriesSonifyOptions(this,
                    options),
                    timelinePath = buildTimelinePathFromSeries(this,
                    mergedOptions),
                    chartSonification = this.chart.sonification;
                if (chartSonification) {
                    // Only one timeline can play at a time. If we want multiple series
                    // playing at the same time, use chart.sonify.
                    if (chartSonification.timeline) {
                        chartSonification.timeline.pause();
                    }
                    // Store reference to duration
                    chartSonification.duration = mergedOptions.duration;
                    // Create new timeline for this series, and play it.
                    chartSonification.timeline = new Timeline({
                        paths: [timelinePath]
                    });
                    chartSonification.timeline.play();
                }
            }
        })(SeriesSonify || (SeriesSonify = {}));
        /* *
         *
         *  Default Export
         *
         * */

        return SeriesSonify;
    });
    _registerModule(_modules, 'Extensions/Sonification/ChartSonify.js', [_modules['Extensions/Sonification/Earcon.js'], _modules['Core/Series/Point.js'], _modules['Extensions/Sonification/SeriesSonify.js'], _modules['Extensions/Sonification/SonificationUtilities.js'], _modules['Extensions/Sonification/Timeline.js'], _modules['Extensions/Sonification/TimelineEvent.js'], _modules['Extensions/Sonification/TimelinePath.js'], _modules['Core/Utilities.js']], function (Earcon, Point, SeriesSonify, SU, Timeline, TimelineEvent, TimelinePath, U) {
        /* *
         *
         *  (c) 2009-2021 Øystein Moseng
         *
         *  Sonification functions for chart/series.
         *
         *  License: www.highcharts.com/license
         *
         *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
         *
         * */
        var getExtremesForInstrumentProps = SU.getExtremesForInstrumentProps,
            virtualAxisTranslate = SU.virtualAxisTranslate;
        var addEvent = U.addEvent,
            extend = U.extend,
            merge = U.merge,
            pick = U.pick,
            splat = U.splat;
        /* *
         *
         *  Functions
         *
         * */
        /* eslint-disable valid-jsdoc */
        /**
         * Utility function to normalize the ordering of timeline paths when sonifying
         * a chart.
         * @private
         * @param {string|Array<string|Highcharts.Earcon|Array<string|Highcharts.Earcon>>} orderOptions
         * Order options for the sonification.
         * @param {Highcharts.Chart} chart
         * The chart we are sonifying.
         * @param {Function} seriesOptionsCallback
         * A function that takes a series as argument, and returns the series options
         * for that series to be used with buildTimelinePathFromSeries.
         * @return {Array<object|Array<object|Highcharts.TimelinePath>>}
         * If order is sequential, we return an array of objects to create series paths
         * from. If order is simultaneous we return an array of an array with the same.
         * If there is a custom order, we return an array of arrays of either objects
         * (for series) or TimelinePaths (for earcons and delays).
         */
        function buildPathOrder(orderOptions, chart, seriesOptionsCallback) {
            var order;
            if (orderOptions === 'sequential' || orderOptions === 'simultaneous') {
                // Just add the series from the chart
                order = chart.series.reduce(function (seriesList, series) {
                    if (series.visible &&
                        (series.options.sonification &&
                            series.options.sonification.enabled) !== false) {
                        seriesList.push({
                            series: series,
                            seriesOptions: seriesOptionsCallback(series)
                        });
                    }
                    return seriesList;
                }, []);
                // If order is simultaneous, group all series together
                if (orderOptions === 'simultaneous') {
                    order = [order];
                }
            }
            else {
                // We have a specific order, and potentially custom items - like
                // earcons or silent waits.
                order = orderOptions.reduce(function (orderList, orderDef) {
                    // Return set of items to play simultaneously. Could be only one.
                    var simulItems = splat(orderDef).reduce(function (items,
                        item) {
                            var itemObject;
                        // Is this item a series ID?
                        if (typeof item === 'string') {
                            var series = chart.get(item);
                            if (series.visible) {
                                itemObject = {
                                    series: series,
                                    seriesOptions: seriesOptionsCallback(series)
                                };
                            }
                            // Is it an earcon? If so, just create the path.
                        }
                        else if (item instanceof Earcon) {
                            // Path with a single event
                            itemObject = new TimelinePath({
                                events: [new TimelineEvent({
                                        eventObject: item
                                    })]
                            });
                        }
                        // Is this item a silent wait? If so, just create the path.
                        if (item.silentWait) {
                            itemObject = new TimelinePath({
                                silentWait: item.silentWait
                            });
                        }
                        // Add to items to play simultaneously
                        if (itemObject) {
                            items.push(itemObject);
                        }
                        return items;
                    }, []);
                    // Add to order list
                    if (simulItems.length) {
                        orderList.push(simulItems);
                    }
                    return orderList;
                }, []);
            }
            return order;
        }
        /**
         * Utility function to add a silent wait after all series.
         * @private
         * @param {Array<object|Array<object|TimelinePath>>} order
         * The order of items.
         * @param {number} wait
         * The wait in milliseconds to add.
         * @return {Array<object|Array<object|TimelinePath>>}
         * The order with waits inserted.
         */
        function addAfterSeriesWaits(order, wait) {
            if (!wait) {
                return order;
            }
            return order.reduce(function (newOrder, orderDef, i) {
                var simultaneousPaths = splat(orderDef);
                newOrder.push(simultaneousPaths);
                // Go through the simultaneous paths and see if there is a series there
                if (i < order.length - 1 && // Do not add wait after last series
                    simultaneousPaths.some(function (item) {
                        return item.series;
                    })) {
                    // We have a series, meaning we should add a wait after these
                    // paths have finished.
                    newOrder.push(new TimelinePath({
                        silentWait: wait
                    }));
                }
                return newOrder;
            }, []);
        }
        /**
         * Utility function to find the total amout of wait time in the TimelinePaths.
         * @private
         * @param {Array<object|Array<object|TimelinePath>>} order
         * The order of TimelinePaths/items.
         * @return {number}
         * The total time in ms spent on wait paths between playing.
         */
        function getWaitTime(order) {
            return order.reduce(function (waitTime, orderDef) {
                var def = splat(orderDef);
                return waitTime + (def.length === 1 &&
                    def[0].options &&
                    def[0].options.silentWait || 0);
            }, 0);
        }
        /**
         * Utility function to ensure simultaneous paths have start/end events at the
         * same time, to sync them.
         * @private
         * @param {Array<Highcharts.TimelinePath>} paths
         * The paths to sync.
         */
        function syncSimultaneousPaths(paths) {
            // Find the extremes for these paths
            var extremes = paths.reduce(function (extremes,
                path) {
                    var events = path.events;
                if (events && events.length) {
                    extremes.min = Math.min(events[0].time, extremes.min);
                    extremes.max = Math.max(events[events.length - 1].time, extremes.max);
                }
                return extremes;
            }, {
                min: Infinity,
                max: -Infinity
            });
            // Go through the paths and add events to make them fit the same timespan
            paths.forEach(function (path) {
                var events = path.events,
                    hasEvents = events && events.length,
                    eventsToAdd = [];
                if (!(hasEvents && events[0].time <= extremes.min)) {
                    eventsToAdd.push(new TimelineEvent({
                        time: extremes.min
                    }));
                }
                if (!(hasEvents && events[events.length - 1].time >= extremes.max)) {
                    eventsToAdd.push(new TimelineEvent({
                        time: extremes.max
                    }));
                }
                if (eventsToAdd.length) {
                    path.addTimelineEvents(eventsToAdd);
                }
            });
        }
        /**
         * Utility function to find the total duration span for all simul path sets
         * that include series.
         * @private
         * @param {Array<object|Array<object|Highcharts.TimelinePath>>} order
         * The order of TimelinePaths/items.
         * @return {number}
         * The total time value span difference for all series.
         */
        function getSimulPathDurationTotal(order) {
            return order.reduce(function (durationTotal, orderDef) {
                return durationTotal + splat(orderDef).reduce(function (maxPathDuration, item) {
                    var timeExtremes = (item.series &&
                            item.seriesOptions &&
                            item.seriesOptions.timeExtremes);
                    return timeExtremes ?
                        Math.max(maxPathDuration, timeExtremes.max - timeExtremes.min) : maxPathDuration;
                }, 0);
            }, 0);
        }
        /**
         * Function to calculate the duration in ms for a series.
         * @private
         * @param {number} seriesValueDuration
         * The duration of the series in value difference.
         * @param {number} totalValueDuration
         * The total duration of all (non simultaneous) series in value difference.
         * @param {number} totalDurationMs
         * The desired total duration for all series in milliseconds.
         * @return {number}
         * The duration for the series in milliseconds.
         */
        function getSeriesDurationMs(seriesValueDuration, totalValueDuration, totalDurationMs) {
            // A series spanning the whole chart would get the full duration.
            return virtualAxisTranslate(seriesValueDuration, { min: 0, max: totalValueDuration }, { min: 0, max: totalDurationMs });
        }
        /**
         * Convert series building objects into paths and return a new list of
         * TimelinePaths.
         * @private
         * @param {Array<object|Array<object|Highcharts.TimelinePath>>} order
         * The order list.
         * @param {number} duration
         * Total duration to aim for in milliseconds.
         * @return {Array<Array<Highcharts.TimelinePath>>}
         * Array of TimelinePath objects to play.
         */
        function buildPathsFromOrder(order, duration) {
            // Find time used for waits (custom or after series), and subtract it from
            // available duration.
            var totalAvailableDurationMs = Math.max(duration - getWaitTime(order), 0), 
                // Add up simultaneous path durations to find total value span duration
                // of everything
                totalUsedDuration = getSimulPathDurationTotal(order);
            // Go through the order list and convert the items
            return order.reduce(function (allPaths, orderDef) {
                var simultaneousPaths = splat(orderDef).reduce(function (simulPaths,
                    item) {
                        if (item instanceof TimelinePath) {
                            // This item is already a path object
                            simulPaths.push(item);
                    }
                    else if (item.series) {
                        // We have a series.
                        // We need to set the duration of the series
                        item.seriesOptions.duration =
                            item.seriesOptions.duration || getSeriesDurationMs(item.seriesOptions.timeExtremes.max -
                                item.seriesOptions.timeExtremes.min, totalUsedDuration, totalAvailableDurationMs);
                        // Add the path
                        simulPaths.push(SeriesSonify.buildTimelinePathFromSeries(item.series, item.seriesOptions));
                    }
                    return simulPaths;
                }, []);
                // Add in the simultaneous paths
                allPaths.push(simultaneousPaths);
                return allPaths;
            }, []);
        }
        /**
         * @private
         * @param {Highcharts.Chart} chart The chart to get options for.
         * @param {Highcharts.SonificationOptions} options
         *  Options to merge with user options on chart and default options.
         * @return {Highcharts.SonificationOptions} The merged options.
         */
        function getChartSonifyOptions(chart, options) {
            var chartOpts = chart.options.sonification || {};
            return merge({
                duration: chartOpts.duration,
                afterSeriesWait: chartOpts.afterSeriesWait,
                pointPlayTime: (chartOpts.defaultInstrumentOptions &&
                    chartOpts.defaultInstrumentOptions.mapping &&
                    chartOpts.defaultInstrumentOptions.mapping.pointPlayTime),
                order: chartOpts.order,
                onSeriesStart: (chartOpts.events && chartOpts.events.onSeriesStart),
                onSeriesEnd: (chartOpts.events && chartOpts.events.onSeriesEnd),
                onEnd: (chartOpts.events && chartOpts.events.onEnd)
            }, options);
        }
        /**
         * Sonify a chart.
         *
         * @sample highcharts/sonification/chart-sequential/
         *         Sonify a basic chart
         * @sample highcharts/sonification/chart-simultaneous/
         *         Sonify series simultaneously
         * @sample highcharts/sonification/chart-custom-order/
         *         Custom defined order of series
         * @sample highcharts/sonification/chart-earcon/
         *         Earcons on chart
         * @sample highcharts/sonification/chart-events/
         *         Sonification events on chart
         *
         * @requires module:modules/sonification
         *
         * @function Highcharts.Chart#sonify
         *
         * @param {Highcharts.SonificationOptions} [options]
         * The options for sonifying this chart. If not provided,
         * uses options set on chart and series.
         */
        function chartSonify(options) {
            var opts = getChartSonifyOptions(this,
                options);
            // Only one timeline can play at a time.
            if (this.sonification.timeline) {
                this.sonification.timeline.pause();
            }
            // Store reference to duration
            this.sonification.duration = opts.duration;
            // Calculate data extremes for the props used
            var dataExtremes = getExtremesForInstrumentProps(this,
                opts.instruments,
                opts.dataExtremes);
            // Figure out ordering of series and custom paths
            var order = buildPathOrder(opts.order,
                this,
                function (series) {
                    return SeriesSonify.buildChartSonifySeriesOptions(series,
                dataExtremes,
                opts);
            });
            // Add waits after simultaneous paths with series in them.
            order = addAfterSeriesWaits(order, opts.afterSeriesWait || 0);
            // We now have a list of either TimelinePath objects or series that need to
            // be converted to TimelinePath objects. Convert everything to paths.
            var paths = buildPathsFromOrder(order,
                opts.duration);
            // Sync simultaneous paths
            paths.forEach(function (simultaneousPaths) {
                syncSimultaneousPaths(simultaneousPaths);
            });
            // We have a set of paths. Create the timeline, and play it.
            this.sonification.timeline = new Timeline({
                paths: paths,
                onEnd: opts.onEnd
            });
            this.sonification.timeline.play();
        }
        /**
         * Get a list of the points currently under cursor.
         *
         * @requires module:modules/sonification
         *
         * @function Highcharts.Chart#getCurrentSonifyPoints
         *
         * @return {Array<Highcharts.Point>}
         *         The points currently under the cursor.
         */
        function getCurrentPoints() {
            var cursorObj;
            if (this.sonification.timeline) {
                cursorObj = this.sonification.timeline.getCursor(); // Cursor per pathID
                return Object.keys(cursorObj).map(function (path) {
                    // Get the event objects under cursor for each path
                    return cursorObj[path].options.eventObject;
                }).filter(function (eventObj) {
                    // Return the events that are points
                    return eventObj instanceof Point;
                });
            }
            return [];
        }
        /**
         * Set the cursor to a point or set of points in different series.
         *
         * @requires module:modules/sonification
         *
         * @function Highcharts.Chart#setSonifyCursor
         *
         * @param {Highcharts.Point|Array<Highcharts.Point>} points
         *        The point or points to set the cursor to. If setting multiple points
         *        under the cursor, the points have to be in different series that are
         *        being played simultaneously.
         */
        function setCursor(points) {
            var timeline = this.sonification.timeline;
            if (timeline) {
                splat(points).forEach(function (point) {
                    // We created the events with the ID of the points, which makes
                    // this easy. Just call setCursor for each ID.
                    timeline.setCursor(point.id);
                });
            }
        }
        /**
         * Pause the running sonification.
         *
         * @requires module:modules/sonification
         *
         * @function Highcharts.Chart#pauseSonify
         *
         * @param {boolean} [fadeOut=true]
         *        Fade out as we pause to avoid clicks.
         *
         * @return {void}
         */
        function pause(fadeOut) {
            if (this.sonification.timeline) {
                this.sonification.timeline.pause(pick(fadeOut, true));
            }
            else if (this.sonification.currentlyPlayingPoint) {
                this.sonification.currentlyPlayingPoint.cancelSonify(fadeOut);
            }
        }
        /**
         * Resume the currently running sonification. Requires series.sonify or
         * chart.sonify to have been played at some point earlier.
         *
         * @requires module:modules/sonification
         *
         * @function Highcharts.Chart#resumeSonify
         *
         * @param {Function} onEnd
         *        Callback to call when play finished.
         *
         * @return {void}
         */
        function resume(onEnd) {
            if (this.sonification.timeline) {
                this.sonification.timeline.play(onEnd);
            }
        }
        /**
         * Play backwards from cursor. Requires series.sonify or chart.sonify to have
         * been played at some point earlier.
         *
         * @requires module:modules/sonification
         *
         * @function Highcharts.Chart#rewindSonify
         *
         * @param {Function} onEnd
         *        Callback to call when play finished.
         *
         * @return {void}
         */
        function rewind(onEnd) {
            if (this.sonification.timeline) {
                this.sonification.timeline.rewind(onEnd);
            }
        }
        /**
         * Cancel current sonification and reset cursor.
         *
         * @requires module:modules/sonification
         *
         * @function Highcharts.Chart#cancelSonify
         *
         * @param {boolean} [fadeOut=true]
         *        Fade out as we pause to avoid clicks.
         *
         * @return {void}
         */
        function cancel(fadeOut) {
            this.pauseSonify(fadeOut);
            this.resetSonifyCursor();
        }
        /**
         * Reset cursor to start. Requires series.sonify or chart.sonify to have been
         * played at some point earlier.
         *
         * @requires module:modules/sonification
         *
         * @function Highcharts.Chart#resetSonifyCursor
         *
         * @return {void}
         */
        function resetCursor() {
            if (this.sonification.timeline) {
                this.sonification.timeline.resetCursor();
            }
        }
        /**
         * Reset cursor to end. Requires series.sonify or chart.sonify to have been
         * played at some point earlier.
         *
         * @requires module:modules/sonification
         *
         * @function Highcharts.Chart#resetSonifyCursorEnd
         *
         * @return {void}
         */
        function resetCursorEnd() {
            if (this.sonification.timeline) {
                this.sonification.timeline.resetCursorEnd();
            }
        }
        var composedClasses = [];
        /**
         * @private
         * @todo move to composition namespace with all functions
         */
        function compose(ChartClass) {
            if (composedClasses.indexOf(ChartClass) === -1) {
                composedClasses.push(ChartClass);
                var chartProto = ChartClass.prototype;
                extend(chartProto, {
                    sonify: chartSonify,
                    pauseSonify: pause,
                    resumeSonify: resume,
                    rewindSonify: rewind,
                    cancelSonify: cancel,
                    getCurrentSonifyPoints: getCurrentPoints,
                    setSonifyCursor: setCursor,
                    resetSonifyCursor: resetCursor,
                    resetSonifyCursorEnd: resetCursorEnd
                });
                // Prepare charts for sonification on init
                addEvent(ChartClass, 'init', function () {
                    this.sonification = {};
                });
                // Update with chart/series/point updates
                addEvent(ChartClass, 'update', function (e) {
                    var newOptions = e.options.sonification;
                    if (newOptions) {
                        merge(true, this.options.sonification, newOptions);
                    }
                });
            }
            return ChartClass;
        }
        /* *
         *
         *  Default Export
         *
         * */
        var ChartSonify = {
                chartSonify: chartSonify,
                compose: compose,
                pause: pause,
                resume: resume,
                rewind: rewind,
                cancel: cancel,
                getCurrentPoints: getCurrentPoints,
                setCursor: setCursor,
                resetCursor: resetCursor,
                resetCursorEnd: resetCursorEnd
            };
        /* *
         *
         *  API Declarations
         *
         * */
        /**
         * An Earcon configuration, specifying an Earcon and when to play it.
         *
         * @requires module:modules/sonification
         *
         * @interface Highcharts.EarconConfiguration
         */ /**
        * An Earcon instance.
        * @name Highcharts.EarconConfiguration#earcon
        * @type {Highcharts.Earcon}
        */ /**
        * The ID of the point to play the Earcon on.
        * @name Highcharts.EarconConfiguration#onPoint
        * @type {string|undefined}
        */ /**
        * A function to determine whether or not to play this earcon on a point. The
        * function is called for every point, receiving that point as parameter. It
        * should return either a boolean indicating whether or not to play the earcon,
        * or a new Earcon instance - in which case the new Earcon will be played.
        * @name Highcharts.EarconConfiguration#condition
        * @type {Function|undefined}
        */
        /**
         * Options for sonifying a chart.
         *
         * @requires module:modules/sonification
         *
         * @interface Highcharts.SonificationOptions
         */ /**
        * Duration for sonifying the entire chart. The duration is distributed across
        * the different series intelligently, but does not take earcons into account.
        * It is also possible to set the duration explicitly per series, using
        * `seriesOptions`. Note that points may continue to play after the duration has
        * passed, but no new points will start playing.
        * @name Highcharts.SonificationOptions#duration
        * @type {number}
        */ /**
        * Define the order to play the series in. This can be given as a string, or an
        * array specifying a custom ordering. If given as a string, valid values are
        * `sequential` - where each series is played in order - or `simultaneous`,
        * where all series are played at once. For custom ordering, supply an array as
        * the order. Each element in the array can be either a string with a series ID,
        * an Earcon object, or an object with a numeric `silentWait` property
        * designating a number of milliseconds to wait before continuing. Each element
        * of the array will be played in order. To play elements simultaneously, group
        * the elements in an array.
        * @name Highcharts.SonificationOptions#order
        * @type {string|Array<string|Highcharts.Earcon|Array<string|Highcharts.Earcon>>}
        */ /**
        * The axis to use for when to play the points. Can be a string with a data
        * property (e.g. `x`), or a function. If it is a function, this function
        * receives the point as argument, and should return a numeric value. The points
        * with the lowest numeric values are then played first, and the time between
        * points will be proportional to the distance between the numeric values. This
        * option cannot be overridden per series.
        * @name Highcharts.SonificationOptions#pointPlayTime
        * @type {string|Function}
        */ /**
        * Milliseconds of silent waiting to add between series. Note that waiting time
        * is considered part of the sonify duration.
        * @name Highcharts.SonificationOptions#afterSeriesWait
        * @type {number|undefined}
        */ /**
        * Options as given to `series.sonify` to override options per series. If the
        * option is supplied as an array of options objects, the `id` property of the
        * object should correspond to the series' id. If the option is supplied as a
        * single object, the options apply to all series.
        * @name Highcharts.SonificationOptions#seriesOptions
        * @type {Object|Array<object>|undefined}
        */ /**
        * The instrument definitions for the points in this chart.
        * @name Highcharts.SonificationOptions#instruments
        * @type {Array<Highcharts.PointInstrumentObject>|undefined}
        */ /**
        * Earcons to add to the chart. Note that earcons can also be added per series
        * using `seriesOptions`.
        * @name Highcharts.SonificationOptions#earcons
        * @type {Array<Highcharts.EarconConfiguration>|undefined}
        */ /**
        * Optionally provide the minimum/maximum data values for the points. If this is
        * not supplied, it is calculated from all points in the chart on demand. This
        * option is supplied in the following format, as a map of point data properties
        * to objects with min/max values:
        *  ```js
        *      dataExtremes: {
        *          y: {
        *              min: 0,
        *              max: 100
        *          },
        *          z: {
        *              min: -10,
        *              max: 10
        *          }
        *          // Properties used and not provided are calculated on demand
        *      }
        *  ```
        * @name Highcharts.SonificationOptions#dataExtremes
        * @type {Highcharts.Dictionary<Highcharts.RangeObject>|undefined}
        */ /**
        * Callback before a series is played.
        * @name Highcharts.SonificationOptions#onSeriesStart
        * @type {Function|undefined}
        */ /**
        * Callback after a series has finished playing.
        * @name Highcharts.SonificationOptions#onSeriesEnd
        * @type {Function|undefined}
        */ /**
        * Callback after the chart has played.
        * @name Highcharts.SonificationOptions#onEnd
        * @type {Function|undefined}
        */
        /**
         * Options for sonifying a series.
         *
         * @requires module:modules/sonification
         *
         * @interface Highcharts.SonifySeriesOptionsObject
         */ /**
        * The duration for playing the points. Note that points might continue to play
        * after the duration has passed, but no new points will start playing.
        * @name Highcharts.SonifySeriesOptionsObject#duration
        * @type {number}
        */ /**
        * The axis to use for when to play the points. Can be a string with a data
        * property (e.g. `x`), or a function. If it is a function, this function
        * receives the point as argument, and should return a numeric value. The points
        * with the lowest numeric values are then played first, and the time between
        * points will be proportional to the distance between the numeric values.
        * @name Highcharts.SonifySeriesOptionsObject#pointPlayTime
        * @type {string|Function}
        */ /**
        * The instrument definitions for the points in this series.
        * @name Highcharts.SonifySeriesOptionsObject#instruments
        * @type {Array<Highcharts.PointInstrumentObject>}
        */ /**
        * Earcons to add to the series.
        * @name Highcharts.SonifySeriesOptionsObject#earcons
        * @type {Array<Highcharts.EarconConfiguration>|undefined}
        */ /**
        * Optionally provide the minimum/maximum data values for the points. If this is
        * not supplied, it is calculated from all points in the chart on demand. This
        * option is supplied in the following format, as a map of point data properties
        * to objects with min/max values:
        * ```js
        *     dataExtremes: {
        *         y: {
        *             min: 0,
        *             max: 100
        *         },
        *         z: {
        *             min: -10,
        *             max: 10
        *         }
        *         // Properties used and not provided are calculated on demand
        *     }
        * ```
        * @name Highcharts.SonifySeriesOptionsObject#dataExtremes
        * @type {Highcharts.Dictionary<Highcharts.RangeObject>|undefined}
        */ /**
        * Callback before a point is played.
        * @name Highcharts.SonifySeriesOptionsObject#onPointStart
        * @type {Function|undefined}
        */ /**
        * Callback after a point has finished playing.
        * @name Highcharts.SonifySeriesOptionsObject#onPointEnd
        * @type {Function|undefined}
        */ /**
        * Callback after the series has played.
        * @name Highcharts.SonifySeriesOptionsObject#onEnd
        * @type {Function|undefined}
        */
        ''; // detach doclets above

        return ChartSonify;
    });
    _registerModule(_modules, 'Extensions/Sonification/PointSonify.js', [_modules['Extensions/Sonification/Instrument.js'], _modules['Core/Utilities.js'], _modules['Extensions/Sonification/SonificationUtilities.js']], function (Instrument, U, SU) {
        /* *
         *
         *  (c) 2009-2021 Øystein Moseng
         *
         *  Code for sonifying single points.
         *
         *  License: www.highcharts.com/license
         *
         *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
         *
         * */
        var error = U.error,
            merge = U.merge,
            pick = U.pick;
        /* *
         *
         *  Constants
         *
         * */
        var composedClasses = [];
        // Defaults for the instrument options
        // NOTE: Also change defaults in Highcharts.PointInstrumentOptionsObject if
        //       making changes here.
        var defaultInstrumentOptions = {
                minDuration: 20,
                maxDuration: 2000,
                minVolume: 0.1,
                maxVolume: 1,
                minPan: -1,
                maxPan: 1,
                minFrequency: 220,
                maxFrequency: 2200
            };
        /* eslint-disable valid-jsdoc */
        /* *
         *
         *  Composition
         *
         * */
        /**
         * @private
         */
        var PointSonify;
        (function (PointSonify) {
            /* *
             *
             * Declarations
             *
             * */
            /* *
             *
             *  Functions
             *
             * */
            /**
             * Extends the axis with ordinal support.
             *
             * @private
             *
             * @param PointClass
             * Point class to extend.
             */
            function compose(PointClass) {
                if (composedClasses.indexOf(PointClass) === -1) {
                    composedClasses.push(PointClass);
                    var pointProto = PointClass.prototype;
                    pointProto.sonify = pointSonify;
                    pointProto.cancelSonify = pointCancelSonify;
                }
                return PointClass;
            }
            PointSonify.compose = compose;
            /**
             * Sonify a single point.
             *
             * @sample highcharts/sonification/point-basic/
             *         Click on points to sonify
             * @sample highcharts/sonification/point-advanced/
             *         Sonify bubbles
             *
             * @requires module:modules/sonification
             *
             * @function Highcharts.Point#sonify
             *
             * @param {Highcharts.PointSonifyOptionsObject} options
             * Options for the sonification of the point.
             */
            function pointSonify(options) {
                var point = this,
                    chart = point.series.chart,
                    masterVolume = pick(options.masterVolume,
                    chart.options.sonification &&
                        chart.options.sonification.masterVolume),
                    dataExtremes = options.dataExtremes || {}, 
                    // Get the value to pass to instrument.play from the mapping value
                    // passed in.
                    getMappingValue = function (value,
                    makeFunction,
                    allowedExtremes) {
                        // Function. Return new function if we try to use callback,
                        // otherwise call it now and return result.
                        if (typeof value === 'function') {
                            return makeFunction ?
                                function (time) {
                                    return value(point,
                    dataExtremes,
                    time);
                            } :
                            value(point, dataExtremes);
                    }
                    // String, this is a data prop. Potentially with negative
                    // polarity.
                    if (typeof value === 'string') {
                        var hasInvertedPolarity = value.charAt(0) === '-';
                        var dataProp = hasInvertedPolarity ?
                                value.slice(1) : value;
                        var pointValue = pick(point[dataProp],
                            point.options[dataProp]);
                        // Find data extremes if we don't have them
                        dataExtremes[dataProp] = dataExtremes[dataProp] ||
                            SU.calculateDataExtremes(point.series.chart, dataProp);
                        // Find the value
                        return SU.virtualAxisTranslate(pointValue, dataExtremes[dataProp], allowedExtremes, hasInvertedPolarity);
                    }
                    // Fixed number or something else weird, just use that
                    return value;
                };
                // Register playing point on chart
                chart.sonification.currentlyPlayingPoint = point;
                // Keep track of instruments playing
                point.sonification = point.sonification || {};
                point.sonification.instrumentsPlaying =
                    point.sonification.instrumentsPlaying || {};
                // Register signal handler for the point
                var signalHandler = point.sonification.signalHandler =
                        point.sonification.signalHandler ||
                            new SU.SignalHandler(['onEnd']);
                signalHandler.clearSignalCallbacks();
                signalHandler.registerSignalCallbacks({ onEnd: options.onEnd });
                // If we have a null point or invisible point, just return
                if (point.isNull || !point.visible || !point.series.visible) {
                    signalHandler.emitSignal('onEnd');
                    return;
                }
                // Go through instruments and play them
                options.instruments.forEach(function (instrumentDefinition) {
                    var instrument = (typeof instrumentDefinition.instrument === 'string') ?
                            Instrument.definitions[instrumentDefinition.instrument] :
                            instrumentDefinition.instrument,
                        mapping = instrumentDefinition.instrumentMapping || {},
                        extremes = merge(defaultInstrumentOptions,
                        instrumentDefinition.instrumentOptions),
                        id = instrument.id,
                        onEnd = function (cancelled) {
                            // Instrument on end
                            if (instrumentDefinition.onEnd) {
                                instrumentDefinition.onEnd.apply(this,
                        arguments);
                        }
                        // Remove currently playing point reference on chart
                        if (chart.sonification &&
                            chart.sonification.currentlyPlayingPoint) {
                            delete chart.sonification.currentlyPlayingPoint;
                        }
                        // Remove reference from instruments playing
                        if (point.sonification &&
                            point.sonification.instrumentsPlaying) {
                            delete point.sonification.instrumentsPlaying[id];
                            // This was the last instrument?
                            if (!Object.keys(point.sonification.instrumentsPlaying).length) {
                                signalHandler.emitSignal('onEnd', cancelled);
                            }
                        }
                    };
                    // Play the note on the instrument
                    if (instrument && instrument.play) {
                        if (typeof masterVolume !== 'undefined') {
                            instrument.setMasterVolume(masterVolume);
                        }
                        point.sonification.instrumentsPlaying[instrument.id] =
                            instrument;
                        instrument.play({
                            frequency: getMappingValue(mapping.frequency, true, {
                                min: extremes.minFrequency,
                                max: extremes.maxFrequency
                            }),
                            duration: getMappingValue(mapping.duration, false, { min: extremes.minDuration, max: extremes.maxDuration }),
                            pan: getMappingValue(mapping.pan, true, { min: extremes.minPan, max: extremes.maxPan }),
                            volume: getMappingValue(mapping.volume, true, { min: extremes.minVolume, max: extremes.maxVolume }),
                            onEnd: onEnd,
                            minFrequency: extremes.minFrequency,
                            maxFrequency: extremes.maxFrequency
                        });
                    }
                    else {
                        error(30);
                    }
                });
            }
            /**
             * Cancel sonification of a point. Calls onEnd functions.
             *
             * @requires module:modules/sonification
             *
             * @function Highcharts.Point#cancelSonify
             *
             * @param {boolean} [fadeOut=false]
             *        Whether or not to fade out as we stop. If false, the points are
             *        cancelled synchronously.
             *
             */
            function pointCancelSonify(fadeOut) {
                var playing = (this.sonification && this.sonification.instrumentsPlaying),
                    instrIds = playing && Object.keys(playing);
                if (instrIds && instrIds.length) {
                    instrIds.forEach(function (instr) {
                        playing[instr].stop(!fadeOut, null, 'cancelled');
                    });
                    this.sonification.instrumentsPlaying = {};
                    this.sonification.signalHandler.emitSignal('onEnd', 'cancelled');
                }
            }
        })(PointSonify || (PointSonify = {}));
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
         * Define the parameter mapping for an instrument.
         *
         * @requires module:modules/sonification
         *
         * @interface Highcharts.PointInstrumentMappingObject
         */ /**
        * Define the volume of the instrument. This can be a string with a data
        * property name, e.g. `'y'`, in which case this data property is used to define
        * the volume relative to the `y`-values of the other points. A higher `y` value
        * would then result in a higher volume. Alternatively, `'-y'` can be used,
        * which inverts the polarity, so that a higher `y` value results in a lower
        * volume. This option can also be a fixed number or a function. If it is a
        * function, this function is called in regular intervals while the note is
        * playing. It receives three arguments: The point, the dataExtremes, and the
        * current relative time - where 0 is the beginning of the note and 1 is the
        * end. The function should return the volume of the note as a number between
        * 0 and 1.
        * @name Highcharts.PointInstrumentMappingObject#volume
        * @type {string|number|Function}
        */ /**
        * Define the duration of the notes for this instrument. This can be a string
        * with a data property name, e.g. `'y'`, in which case this data property is
        * used to define the duration relative to the `y`-values of the other points. A
        * higher `y` value would then result in a longer duration. Alternatively,
        * `'-y'` can be used, in which case the polarity is inverted, and a higher
        * `y` value would result in a shorter duration. This option can also be a
        * fixed number or a function. If it is a function, this function is called
        * once before the note starts playing, and should return the duration in
        * milliseconds. It receives two arguments: The point, and the dataExtremes.
        * @name Highcharts.PointInstrumentMappingObject#duration
        * @type {string|number|Function}
        */ /**
        * Define the panning of the instrument. This can be a string with a data
        * property name, e.g. `'x'`, in which case this data property is used to define
        * the panning relative to the `x`-values of the other points. A higher `x`
        * value would then result in a higher panning value (panned further to the
        * right). Alternatively, `'-x'` can be used, in which case the polarity is
        * inverted, and a higher `x` value would result in a lower panning value
        * (panned further to the left). This option can also be a fixed number or a
        * function. If it is a function, this function is called in regular intervals
        * while the note is playing. It receives three arguments: The point, the
        * dataExtremes, and the current relative time - where 0 is the beginning of
        * the note and 1 is the end. The function should return the panning of the
        * note as a number between -1 and 1.
        * @name Highcharts.PointInstrumentMappingObject#pan
        * @type {string|number|Function|undefined}
        */ /**
        * Define the frequency of the instrument. This can be a string with a data
        * property name, e.g. `'y'`, in which case this data property is used to define
        * the frequency relative to the `y`-values of the other points. A higher `y`
        * value would then result in a higher frequency. Alternatively, `'-y'` can be
        * used, in which case the polarity is inverted, and a higher `y` value would
        * result in a lower frequency. This option can also be a fixed number or a
        * function. If it is a function, this function is called in regular intervals
        * while the note is playing. It receives three arguments: The point, the
        * dataExtremes, and the current relative time - where 0 is the beginning of
        * the note and 1 is the end. The function should return the frequency of the
        * note as a number (in Hz).
        * @name Highcharts.PointInstrumentMappingObject#frequency
        * @type {string|number|Function}
        */
        /**
         * @requires module:modules/sonification
         *
         * @interface Highcharts.PointInstrumentOptionsObject
         */ /**
        * The minimum duration for a note when using a data property for duration. Can
        * be overridden by using either a fixed number or a function for
        * instrumentMapping.duration. Defaults to 20.
        * @name Highcharts.PointInstrumentOptionsObject#minDuration
        * @type {number|undefined}
        */ /**
        * The maximum duration for a note when using a data property for duration. Can
        * be overridden by using either a fixed number or a function for
        * instrumentMapping.duration. Defaults to 2000.
        * @name Highcharts.PointInstrumentOptionsObject#maxDuration
        * @type {number|undefined}
        */ /**
        * The minimum pan value for a note when using a data property for panning. Can
        * be overridden by using either a fixed number or a function for
        * instrumentMapping.pan. Defaults to -1 (fully left).
        * @name Highcharts.PointInstrumentOptionsObject#minPan
        * @type {number|undefined}
        */ /**
        * The maximum pan value for a note when using a data property for panning. Can
        * be overridden by using either a fixed number or a function for
        * instrumentMapping.pan. Defaults to 1 (fully right).
        * @name Highcharts.PointInstrumentOptionsObject#maxPan
        * @type {number|undefined}
        */ /**
        * The minimum volume for a note when using a data property for volume. Can be
        * overridden by using either a fixed number or a function for
        * instrumentMapping.volume. Defaults to 0.1.
        * @name Highcharts.PointInstrumentOptionsObject#minVolume
        * @type {number|undefined}
        */ /**
        * The maximum volume for a note when using a data property for volume. Can be
        * overridden by using either a fixed number or a function for
        * instrumentMapping.volume. Defaults to 1.
        * @name Highcharts.PointInstrumentOptionsObject#maxVolume
        * @type {number|undefined}
        */ /**
        * The minimum frequency for a note when using a data property for frequency.
        * Can be overridden by using either a fixed number or a function for
        * instrumentMapping.frequency. Defaults to 220.
        * @name Highcharts.PointInstrumentOptionsObject#minFrequency
        * @type {number|undefined}
        */ /**
        * The maximum frequency for a note when using a data property for frequency.
        * Can be overridden by using either a fixed number or a function for
        * instrumentMapping.frequency. Defaults to 2200.
        * @name Highcharts.PointInstrumentOptionsObject#maxFrequency
        * @type {number|undefined}
        */
        /**
         * An instrument definition for a point, specifying the instrument to play and
         * how to play it.
         *
         * @interface Highcharts.PointInstrumentObject
         */ /**
        * An Instrument instance or the name of the instrument in the
        * Highcharts.sonification.instruments map.
        * @name Highcharts.PointInstrumentObject#instrument
        * @type {Highcharts.Instrument|string}
        */ /**
        * Mapping of instrument parameters for this instrument.
        * @name Highcharts.PointInstrumentObject#instrumentMapping
        * @type {Highcharts.PointInstrumentMappingObject}
        */ /**
        * Options for this instrument.
        * @name Highcharts.PointInstrumentObject#instrumentOptions
        * @type {Highcharts.PointInstrumentOptionsObject|undefined}
        */ /**
        * Callback to call when the instrument has stopped playing.
        * @name Highcharts.PointInstrumentObject#onEnd
        * @type {Function|undefined}
        */
        /**
         * Options for sonifying a point.
         * @interface Highcharts.PointSonifyOptionsObject
         */ /**
        * The instrument definitions for this point.
        * @name Highcharts.PointSonifyOptionsObject#instruments
        * @type {Array<Highcharts.PointInstrumentObject>}
        */ /**
        * Optionally provide the minimum/maximum values for the points. If this is not
        * supplied, it is calculated from the points in the chart on demand. This
        * option is supplied in the following format, as a map of point data properties
        * to objects with min/max values:
        *  ```js
        *      dataExtremes: {
        *          y: {
        *              min: 0,
        *              max: 100
        *          },
        *          z: {
        *              min: -10,
        *              max: 10
        *          }
        *          // Properties used and not provided are calculated on demand
        *      }
        *  ```
        * @name Highcharts.PointSonifyOptionsObject#dataExtremes
        * @type {object|undefined}
        */ /**
        * Callback called when the sonification has finished.
        * @name Highcharts.PointSonifyOptionsObject#onEnd
        * @type {Function|undefined}
        */
        (''); // detach doclets above

        return PointSonify;
    });
    _registerModule(_modules, 'masters/modules/sonification.src.js', [_modules['Core/Globals.js'], _modules['Extensions/Sonification/ChartSonify.js'], _modules['Extensions/Sonification/Earcon.js'], _modules['Extensions/Sonification/Instrument.js'], _modules['Extensions/Sonification/PointSonify.js'], _modules['Extensions/Sonification/SeriesSonify.js'], _modules['Extensions/Sonification/Sonification.js'], _modules['Extensions/Sonification/Timeline.js'], _modules['Extensions/Sonification/TimelineEvent.js'], _modules['Extensions/Sonification/TimelinePath.js']], function (Highcharts, ChartSonify, Earcon, Instrument, PointSonify, SeriesSonify, Sonification, Timeline, TimelineEvent, TimelinePath) {

        var __assign = (this && this.__assign) || function () {
                __assign = Object.assign || function(t) {
                    for (var s,
            i = 1,
            n = arguments.length; i < n; i++) {
                        s = arguments[i];
                    for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p))
                        t[p] = s[p];
                }
                return t;
            };
            return __assign.apply(this, arguments);
        };
        var G = Highcharts;
        G.sonification = __assign(__assign({}, Sonification), { instruments: Instrument.definitions, Earcon: Earcon, Instrument: Instrument, Timeline: Timeline, TimelineEvent: TimelineEvent, TimelinePath: TimelinePath });
        G.Earcon = Earcon;
        G.Instrument = Instrument;
        ChartSonify.compose(G.Chart);
        SeriesSonify.compose(G.Series);
        PointSonify.compose(G.Point);

    });
}));