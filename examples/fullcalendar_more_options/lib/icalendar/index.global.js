/*!
FullCalendar iCalendar Plugin v6.1.10
Docs & License: https://fullcalendar.io/docs/icalendar
(c) 2023 Adam Shaw
*/
FullCalendar.ICalendar = (function (exports, core, internal, ICAL) {
    'use strict';

    function _interopNamespace(e) {
        if (e && e.__esModule) return e;
        var n = Object.create(null);
        if (e) {
            Object.keys(e).forEach(function (k) {
                if (k !== 'default') {
                    var d = Object.getOwnPropertyDescriptor(e, k);
                    Object.defineProperty(n, k, d.get ? d : {
                        enumerable: true,
                        get: function () { return e[k]; }
                    });
                }
            });
        }
        n["default"] = e;
        return n;
    }

    var ICAL__namespace = /*#__PURE__*/_interopNamespace(ICAL);

    /* eslint-disable */
    class IcalExpander {
        constructor(opts) {
            this.maxIterations = opts.maxIterations != null ? opts.maxIterations : 1000;
            this.skipInvalidDates = opts.skipInvalidDates != null ? opts.skipInvalidDates : false;
            this.jCalData = ICAL__namespace.parse(opts.ics);
            this.component = new ICAL__namespace.Component(this.jCalData);
            this.events = this.component.getAllSubcomponents('vevent').map(vevent => new ICAL__namespace.Event(vevent));
            if (this.skipInvalidDates) {
                this.events = this.events.filter((evt) => {
                    try {
                        evt.startDate.toJSDate();
                        evt.endDate.toJSDate();
                        return true;
                    }
                    catch (err) {
                        // skipping events with invalid time
                        return false;
                    }
                });
            }
        }
        between(after, before) {
            function isEventWithinRange(startTime, endTime) {
                return (!after || endTime >= after.getTime()) &&
                    (!before || startTime <= before.getTime());
            }
            function getTimes(eventOrOccurrence) {
                const startTime = eventOrOccurrence.startDate.toJSDate().getTime();
                let endTime = eventOrOccurrence.endDate.toJSDate().getTime();
                // If it is an all day event, the end date is set to 00:00 of the next day
                // So we need to make it be 23:59:59 to compare correctly with the given range
                if (eventOrOccurrence.endDate.isDate && (endTime > startTime)) {
                    endTime -= 1;
                }
                return { startTime, endTime };
            }
            const exceptions = [];
            this.events.forEach((event) => {
                if (event.isRecurrenceException())
                    exceptions.push(event);
            });
            const ret = {
                events: [],
                occurrences: [],
            };
            this.events.filter(e => !e.isRecurrenceException()).forEach((event) => {
                const exdates = [];
                event.component.getAllProperties('exdate').forEach((exdateProp) => {
                    const exdate = exdateProp.getFirstValue();
                    exdates.push(exdate.toJSDate().getTime());
                });
                // Recurring event is handled differently
                if (event.isRecurring()) {
                    const iterator = event.iterator();
                    let next;
                    let i = 0;
                    do {
                        i += 1;
                        next = iterator.next();
                        if (next) {
                            const occurrence = event.getOccurrenceDetails(next);
                            const { startTime, endTime } = getTimes(occurrence);
                            const isOccurrenceExcluded = exdates.indexOf(startTime) !== -1;
                            // TODO check that within same day?
                            const exception = exceptions.find(ex => ex.uid === event.uid && ex.recurrenceId.toJSDate().getTime() === occurrence.startDate.toJSDate().getTime());
                            // We have passed the max date, stop
                            if (before && startTime > before.getTime())
                                break;
                            // Check that we are within our range
                            if (isEventWithinRange(startTime, endTime)) {
                                if (exception) {
                                    ret.events.push(exception);
                                }
                                else if (!isOccurrenceExcluded) {
                                    ret.occurrences.push(occurrence);
                                }
                            }
                        }
                    } while (next && (!this.maxIterations || i < this.maxIterations));
                    return;
                }
                // Non-recurring event:
                const { startTime, endTime } = getTimes(event);
                if (isEventWithinRange(startTime, endTime))
                    ret.events.push(event);
            });
            return ret;
        }
        before(before) {
            return this.between(undefined, before);
        }
        after(after) {
            return this.between(after);
        }
        all() {
            return this.between();
        }
    }

    const eventSourceDef = {
        parseMeta(refined) {
            if (refined.url && refined.format === 'ics') {
                return {
                    url: refined.url,
                    format: 'ics',
                };
            }
            return null;
        },
        fetch(arg, successCallback, errorCallback) {
            let meta = arg.eventSource.meta;
            let { internalState } = meta;
            /*
            NOTE: isRefetch is a HACK. we would do the recurring-expanding in a separate plugin hook,
            but we couldn't leverage built-in allDay-guessing, among other things.
            */
            if (!internalState || arg.isRefetch) {
                internalState = meta.internalState = {
                    response: null,
                    iCalExpanderPromise: fetch(meta.url, { method: 'GET' }).then((response) => {
                        return response.text().then((icsText) => {
                            internalState.response = response;
                            return new IcalExpander({
                                ics: icsText,
                                skipInvalidDates: true,
                            });
                        });
                    }),
                };
            }
            internalState.iCalExpanderPromise.then((iCalExpander) => {
                successCallback({
                    rawEvents: expandICalEvents(iCalExpander, arg.range),
                    response: internalState.response,
                });
            }, errorCallback);
        },
    };
    function expandICalEvents(iCalExpander, range) {
        // expand the range. because our `range` is timeZone-agnostic UTC
        // or maybe because ical.js always produces dates in local time? i forget
        let rangeStart = internal.addDays(range.start, -1);
        let rangeEnd = internal.addDays(range.end, 1);
        let iCalRes = iCalExpander.between(rangeStart, rangeEnd); // end inclusive. will give extra results
        let expanded = [];
        // TODO: instead of using startDate/endDate.toString to communicate allDay,
        // we can query startDate/endDate.isDate. More efficient to avoid formatting/reparsing.
        // single events
        for (let iCalEvent of iCalRes.events) {
            expanded.push(Object.assign(Object.assign({}, buildNonDateProps(iCalEvent)), { start: iCalEvent.startDate.toString(), end: (specifiesEnd(iCalEvent) && iCalEvent.endDate)
                    ? iCalEvent.endDate.toString()
                    : null }));
        }
        // recurring event instances
        for (let iCalOccurence of iCalRes.occurrences) {
            let iCalEvent = iCalOccurence.item;
            expanded.push(Object.assign(Object.assign({}, buildNonDateProps(iCalEvent)), { start: iCalOccurence.startDate.toString(), end: (specifiesEnd(iCalEvent) && iCalOccurence.endDate)
                    ? iCalOccurence.endDate.toString()
                    : null }));
        }
        return expanded;
    }
    function buildNonDateProps(iCalEvent) {
        return {
            title: iCalEvent.summary,
            url: extractEventUrl(iCalEvent),
            extendedProps: {
                location: iCalEvent.location,
                organizer: iCalEvent.organizer,
                description: iCalEvent.description,
            },
        };
    }
    function extractEventUrl(iCalEvent) {
        let urlProp = iCalEvent.component.getFirstProperty('url');
        return urlProp ? urlProp.getFirstValue() : '';
    }
    function specifiesEnd(iCalEvent) {
        return Boolean(iCalEvent.component.getFirstProperty('dtend')) ||
            Boolean(iCalEvent.component.getFirstProperty('duration'));
    }

    var plugin = core.createPlugin({
        name: '@fullcalendar/icalendar',
        eventSourceDefs: [eventSourceDef],
    });

    core.globalPlugins.push(plugin);

    exports["default"] = plugin;

    Object.defineProperty(exports, '__esModule', { value: true });

    return exports;

})({}, FullCalendar, FullCalendar.Internal, ICAL);
