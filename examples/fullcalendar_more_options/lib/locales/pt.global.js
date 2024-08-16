/*!
FullCalendar Core v6.1.10
Docs & License: https://fullcalendar.io
(c) 2023 Adam Shaw
*/
(function (index_js) {
    'use strict';

    var locale = {
        code: 'pt',
        week: {
            dow: 1,
            doy: 4, // The week that contains Jan 4th is the first week of the year.
        },
        buttonText: {
            prev: 'Anterior',
            next: 'Seguinte',
            today: 'Hoje',
            year: 'Ano',
            month: 'Mês',
            week: 'Semana',
            day: 'Dia',
            list: 'Agenda',
        },
        weekText: 'Sem',
        allDayText: 'Todo o dia',
        moreLinkText: 'mais',
        noEventsText: 'Não há eventos para mostrar',
    };

    index_js.globalLocales.push(locale);

})(FullCalendar);
