/*!
FullCalendar Core v6.1.10
Docs & License: https://fullcalendar.io
(c) 2023 Adam Shaw
*/
(function (index_js) {
    'use strict';

    var locale = {
        code: 'ca',
        week: {
            dow: 1,
            doy: 4, // The week that contains Jan 4th is the first week of the year.
        },
        buttonText: {
            prev: 'Anterior',
            next: 'Següent',
            today: 'Avui',
            year: 'Any',
            month: 'Mes',
            week: 'Setmana',
            day: 'Dia',
            list: 'Agenda',
        },
        weekText: 'Set',
        allDayText: 'Tot el dia',
        moreLinkText: 'més',
        noEventsText: 'No hi ha esdeveniments per mostrar',
    };

    index_js.globalLocales.push(locale);

})(FullCalendar);
