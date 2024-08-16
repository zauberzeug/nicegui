/*!
FullCalendar Core v6.1.10
Docs & License: https://fullcalendar.io
(c) 2023 Adam Shaw
*/
(function (index_js) {
    'use strict';

    var locale = {
        code: 'hr',
        week: {
            dow: 1,
            doy: 7, // The week that contains Jan 1st is the first week of the year.
        },
        buttonText: {
            prev: 'Prijašnji',
            next: 'Sljedeći',
            today: 'Danas',
            year: 'Godina',
            month: 'Mjesec',
            week: 'Tjedan',
            day: 'Dan',
            list: 'Raspored',
        },
        weekText: 'Tje',
        allDayText: 'Cijeli dan',
        moreLinkText(n) {
            return '+ još ' + n;
        },
        noEventsText: 'Nema događaja za prikaz',
    };

    index_js.globalLocales.push(locale);

})(FullCalendar);
