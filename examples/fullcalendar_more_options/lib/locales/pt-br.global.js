/*!
FullCalendar Core v6.1.10
Docs & License: https://fullcalendar.io
(c) 2023 Adam Shaw
*/
(function (index_js) {
    'use strict';

    var locale = {
        code: 'pt-br',
        buttonText: {
            prev: 'Anterior',
            next: 'Próximo',
            prevYear: 'Ano anterior',
            nextYear: 'Próximo ano',
            year: 'Ano',
            today: 'Hoje',
            month: 'Mês',
            week: 'Semana',
            day: 'Dia',
            list: 'Lista',
        },
        buttonHints: {
            prev: '$0 Anterior',
            next: 'Próximo $0',
            today(buttonText) {
                return (buttonText === 'Dia') ? 'Hoje' :
                    ((buttonText === 'Semana') ? 'Esta' : 'Este') + ' ' + buttonText.toLocaleLowerCase();
            },
        },
        viewHint(buttonText) {
            return 'Visualizar ' + (buttonText === 'Semana' ? 'a' : 'o') + ' ' + buttonText.toLocaleLowerCase();
        },
        weekText: 'Sm',
        weekTextLong: 'Semana',
        allDayText: 'dia inteiro',
        moreLinkText(n) {
            return 'mais +' + n;
        },
        moreLinkHint(eventCnt) {
            return `Mostrar mais ${eventCnt} eventos`;
        },
        noEventsText: 'Não há eventos para mostrar',
        navLinkHint: 'Ir para $0',
        closeHint: 'Fechar',
        timeHint: 'A hora',
        eventHint: 'Evento',
    };

    index_js.globalLocales.push(locale);

})(FullCalendar);
