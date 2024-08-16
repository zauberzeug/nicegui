/*!
FullCalendar Core v6.1.10
Docs & License: https://fullcalendar.io
(c) 2023 Adam Shaw
*/
(function (index_js) {
    'use strict';

    function affix(buttonText) {
        return (buttonText === 'Tag' || buttonText === 'Monat') ? 'r' :
            buttonText === 'Jahr' ? 's' : '';
    }
    var locale = {
        code: 'de-at',
        week: {
            dow: 1,
            doy: 4, // The week that contains Jan 4th is the first week of the year.
        },
        buttonText: {
            prev: 'Zurück',
            next: 'Vor',
            today: 'Heute',
            year: 'Jahr',
            month: 'Monat',
            week: 'Woche',
            day: 'Tag',
            list: 'Terminübersicht',
        },
        weekText: 'KW',
        weekTextLong: 'Woche',
        allDayText: 'Ganztägig',
        moreLinkText(n) {
            return '+ weitere ' + n;
        },
        noEventsText: 'Keine Ereignisse anzuzeigen',
        buttonHints: {
            prev(buttonText) {
                return `Vorherige${affix(buttonText)} ${buttonText}`;
            },
            next(buttonText) {
                return `Nächste${affix(buttonText)} ${buttonText}`;
            },
            today(buttonText) {
                // → Heute, Diese Woche, Dieser Monat, Dieses Jahr
                if (buttonText === 'Tag') {
                    return 'Heute';
                }
                return `Diese${affix(buttonText)} ${buttonText}`;
            },
        },
        viewHint(buttonText) {
            // → Tagesansicht, Wochenansicht, Monatsansicht, Jahresansicht
            const glue = buttonText === 'Woche' ? 'n' : buttonText === 'Monat' ? 's' : 'es';
            return buttonText + glue + 'ansicht';
        },
        navLinkHint: 'Gehe zu $0',
        moreLinkHint(eventCnt) {
            return 'Zeige ' + (eventCnt === 1 ?
                'ein weiteres Ereignis' :
                eventCnt + ' weitere Ereignisse');
        },
        closeHint: 'Schließen',
        timeHint: 'Uhrzeit',
        eventHint: 'Ereignis',
    };

    index_js.globalLocales.push(locale);

})(FullCalendar);
