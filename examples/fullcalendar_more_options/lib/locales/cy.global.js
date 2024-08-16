/*!
FullCalendar Core v6.1.10
Docs & License: https://fullcalendar.io
(c) 2023 Adam Shaw
*/
(function (index_js) {
    'use strict';

    var locale = {
        code: 'cy',
        week: {
            dow: 1,
            doy: 4, // The week that contains Jan 4th is the first week of the year.
        },
        buttonText: {
            prev: 'Blaenorol',
            next: 'Nesaf',
            today: 'Heddiw',
            year: 'Blwyddyn',
            month: 'Mis',
            week: 'Wythnos',
            day: 'Dydd',
            list: 'Rhestr',
        },
        weekText: 'Wythnos',
        allDayText: 'Trwy\'r dydd',
        moreLinkText: 'Mwy',
        noEventsText: 'Dim digwyddiadau',
    };

    index_js.globalLocales.push(locale);

})(FullCalendar);
