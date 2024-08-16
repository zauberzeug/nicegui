/*!
FullCalendar Core v6.1.10
Docs & License: https://fullcalendar.io
(c) 2023 Adam Shaw
*/
(function (index_js) {
    'use strict';

    var locale = {
        code: 'id',
        week: {
            dow: 1,
            doy: 7, // The week that contains Jan 1st is the first week of the year.
        },
        buttonText: {
            prev: 'mundur',
            next: 'maju',
            today: 'hari ini',
            year: 'Tahun',
            month: 'Bulan',
            week: 'Minggu',
            day: 'Hari',
            list: 'Agenda',
        },
        weekText: 'Mg',
        allDayText: 'Sehari penuh',
        moreLinkText: 'lebih',
        noEventsText: 'Tidak ada acara untuk ditampilkan',
    };

    index_js.globalLocales.push(locale);

})(FullCalendar);
