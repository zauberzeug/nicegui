/*!
FullCalendar Core v6.1.10
Docs & License: https://fullcalendar.io
(c) 2023 Adam Shaw
*/
(function (index_js) {
    'use strict';

    var locale = {
        code: 'sk',
        week: {
            dow: 1,
            doy: 4, // The week that contains Jan 4th is the first week of the year.
        },
        buttonText: {
            prev: 'Predchádzajúci',
            next: 'Nasledujúci',
            today: 'Dnes',
            year: 'Rok',
            month: 'Mesiac',
            week: 'Týždeň',
            day: 'Deň',
            list: 'Rozvrh',
        },
        weekText: 'Ty',
        allDayText: 'Celý deň',
        moreLinkText(n) {
            return '+ďalšie: ' + n;
        },
        noEventsText: 'Žiadne akcie na zobrazenie',
    };

    index_js.globalLocales.push(locale);

})(FullCalendar);
