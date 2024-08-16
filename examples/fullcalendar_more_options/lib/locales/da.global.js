/*!
FullCalendar Core v6.1.10
Docs & License: https://fullcalendar.io
(c) 2023 Adam Shaw
*/
(function (index_js) {
    'use strict';

    var locale = {
        code: 'da',
        week: {
            dow: 1,
            doy: 4, // The week that contains Jan 4th is the first week of the year.
        },
        buttonText: {
            prev: 'Forrige',
            next: 'Næste',
            today: 'I dag',
            year: 'År',
            month: 'Måned',
            week: 'Uge',
            day: 'Dag',
            list: 'Agenda',
        },
        weekText: 'Uge',
        allDayText: 'Hele dagen',
        moreLinkText: 'flere',
        noEventsText: 'Ingen arrangementer at vise',
    };

    index_js.globalLocales.push(locale);

})(FullCalendar);
