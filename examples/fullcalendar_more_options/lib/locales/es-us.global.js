/*!
FullCalendar Core v6.1.10
Docs & License: https://fullcalendar.io
(c) 2023 Adam Shaw
*/
(function (index_js) {
    'use strict';

    var locale = {
        code: 'es',
        week: {
            dow: 0,
            doy: 6, // The week that contains Jan 1st is the first week of the year.
        },
        buttonText: {
            prev: 'Ant',
            next: 'Sig',
            today: 'Hoy',
            year: 'Año',
            month: 'Mes',
            week: 'Semana',
            day: 'Día',
            list: 'Agenda',
        },
        weekText: 'Sm',
        allDayText: 'Todo el día',
        moreLinkText: 'más',
        noEventsText: 'No hay eventos para mostrar',
    };

    index_js.globalLocales.push(locale);

})(FullCalendar);
