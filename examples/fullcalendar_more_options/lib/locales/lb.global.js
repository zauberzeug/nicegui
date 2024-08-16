/*!
FullCalendar Core v6.1.10
Docs & License: https://fullcalendar.io
(c) 2023 Adam Shaw
*/
(function (index_js) {
    'use strict';

    var locale = {
        code: 'lb',
        week: {
            dow: 1,
            doy: 4, // The week that contains Jan 4th is the first week of the year.
        },
        buttonText: {
            prev: 'Zréck',
            next: 'Weider',
            today: 'Haut',
            year: 'Joer',
            month: 'Mount',
            week: 'Woch',
            day: 'Dag',
            list: 'Terminiwwersiicht',
        },
        weekText: 'W',
        allDayText: 'Ganzen Dag',
        moreLinkText: 'méi',
        noEventsText: 'Nee Evenementer ze affichéieren',
    };

    index_js.globalLocales.push(locale);

})(FullCalendar);
