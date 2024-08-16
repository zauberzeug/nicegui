/*!
FullCalendar Core v6.1.10
Docs & License: https://fullcalendar.io
(c) 2023 Adam Shaw
*/
(function (index_js) {
    'use strict';

    var locale = {
        code: 'sv',
        week: {
            dow: 1,
            doy: 4, // The week that contains Jan 4th is the first week of the year.
        },
        buttonText: {
            prev: 'Förra',
            next: 'Nästa',
            today: 'Idag',
            year: 'År',
            month: 'Månad',
            week: 'Vecka',
            day: 'Dag',
            list: 'Program',
        },
        buttonHints: {
            prev(buttonText) {
                return `Föregående ${buttonText.toLocaleLowerCase()}`;
            },
            next(buttonText) {
                return `Nästa ${buttonText.toLocaleLowerCase()}`;
            },
            today(buttonText) {
                return (buttonText === 'Program' ? 'Detta' : 'Denna') + ' ' + buttonText.toLocaleLowerCase();
            },
        },
        viewHint: '$0 vy',
        navLinkHint: 'Gå till $0',
        moreLinkHint(eventCnt) {
            return `Visa ytterligare ${eventCnt} händelse${eventCnt === 1 ? '' : 'r'}`;
        },
        weekText: 'v.',
        weekTextLong: 'Vecka',
        allDayText: 'Heldag',
        moreLinkText: 'till',
        noEventsText: 'Inga händelser att visa',
        closeHint: 'Stäng',
        timeHint: 'Klockan',
        eventHint: 'Händelse',
    };

    index_js.globalLocales.push(locale);

})(FullCalendar);
