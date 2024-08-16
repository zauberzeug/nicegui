/*!
FullCalendar Core v6.1.10
Docs & License: https://fullcalendar.io
(c) 2023 Adam Shaw
*/
(function (index_js) {
    'use strict';

    var locale = {
        code: 'ms',
        week: {
            dow: 1,
            doy: 7, // The week that contains Jan 1st is the first week of the year.
        },
        buttonText: {
            prev: 'Sebelum',
            next: 'Selepas',
            today: 'hari ini',
            year: 'Tahun',
            month: 'Bulan',
            week: 'Minggu',
            day: 'Hari',
            list: 'Agenda',
        },
        weekText: 'Mg',
        allDayText: 'Sepanjang hari',
        moreLinkText(n) {
            return 'masih ada ' + n + ' acara';
        },
        noEventsText: 'Tiada peristiwa untuk dipaparkan',
    };

    index_js.globalLocales.push(locale);

})(FullCalendar);
