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
            dow: 1,
            doy: 4, // The week that contains Jan 4th is the first week of the year.
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
        buttonHints: {
            prev: '$0 antes',
            next: '$0 siguiente',
            today(buttonText) {
                return (buttonText === 'Día') ? 'Hoy' :
                    ((buttonText === 'Semana') ? 'Esta' : 'Este') + ' ' + buttonText.toLocaleLowerCase();
            },
        },
        viewHint(buttonText) {
            return 'Vista ' + (buttonText === 'Semana' ? 'de la' : 'del') + ' ' + buttonText.toLocaleLowerCase();
        },
        weekText: 'Sm',
        weekTextLong: 'Semana',
        allDayText: 'Todo el día',
        moreLinkText: 'más',
        moreLinkHint(eventCnt) {
            return `Mostrar ${eventCnt} eventos más`;
        },
        noEventsText: 'No hay eventos para mostrar',
        navLinkHint: 'Ir al $0',
        closeHint: 'Cerrar',
        timeHint: 'La hora',
        eventHint: 'Evento',
    };

    index_js.globalLocales.push(locale);

})(FullCalendar);
