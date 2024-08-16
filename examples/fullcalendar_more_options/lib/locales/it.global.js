/*!
FullCalendar Core v6.1.10
Docs & License: https://fullcalendar.io
(c) 2023 Adam Shaw
*/
(function (index_js) {
    'use strict';

    var locale = {
        code: 'it',
        week: {
            dow: 1,
            doy: 4, // The week that contains Jan 4th is the first week of the year.
        },
        buttonText: {
            prev: 'Prec',
            next: 'Succ',
            today: 'Oggi',
            year: 'Anno',
            month: 'Mese',
            week: 'Settimana',
            day: 'Giorno',
            list: 'Agenda',
        },
        weekText: 'Sm',
        allDayText: 'Tutto il giorno',
        moreLinkText(n) {
            return '+altri ' + n;
        },
        noEventsText: 'Non ci sono eventi da visualizzare',
    };

    index_js.globalLocales.push(locale);

})(FullCalendar);
