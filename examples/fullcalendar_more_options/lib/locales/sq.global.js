/*!
FullCalendar Core v6.1.10
Docs & License: https://fullcalendar.io
(c) 2023 Adam Shaw
*/
(function (index_js) {
    'use strict';

    var locale = {
        code: 'sq',
        week: {
            dow: 1,
            doy: 4, // The week that contains Jan 4th is the first week of the year.
        },
        buttonText: {
            prev: 'mbrapa',
            next: 'Përpara',
            today: 'Sot',
            year: 'Viti',
            month: 'Muaj',
            week: 'Javë',
            day: 'Ditë',
            list: 'Listë',
        },
        weekText: 'Ja',
        allDayText: 'Gjithë ditën',
        moreLinkText(n) {
            return '+më tepër ' + n;
        },
        noEventsText: 'Nuk ka evente për të shfaqur',
    };

    index_js.globalLocales.push(locale);

})(FullCalendar);
