/*!
FullCalendar Core v6.1.10
Docs & License: https://fullcalendar.io
(c) 2023 Adam Shaw
*/
(function (index_js) {
    'use strict';

    var locale = {
        code: 'af',
        week: {
            dow: 1,
            doy: 4, // Die week wat die 4de Januarie bevat is die eerste week van die jaar.
        },
        buttonText: {
            prev: 'Vorige',
            next: 'Volgende',
            today: 'Vandag',
            year: 'Jaar',
            month: 'Maand',
            week: 'Week',
            day: 'Dag',
            list: 'Agenda',
        },
        allDayText: 'Heeldag',
        moreLinkText: 'Addisionele',
        noEventsText: 'Daar is geen gebeurtenisse nie',
    };

    index_js.globalLocales.push(locale);

})(FullCalendar);
