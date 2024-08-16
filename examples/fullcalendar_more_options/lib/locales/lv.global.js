/*!
FullCalendar Core v6.1.10
Docs & License: https://fullcalendar.io
(c) 2023 Adam Shaw
*/
(function (index_js) {
    'use strict';

    var locale = {
        code: 'lv',
        week: {
            dow: 1,
            doy: 4, // The week that contains Jan 4th is the first week of the year.
        },
        buttonText: {
            prev: 'Iepr.',
            next: 'Nāk.',
            today: 'Šodien',
            year: 'Gads',
            month: 'Mēnesis',
            week: 'Nedēļa',
            day: 'Diena',
            list: 'Dienas kārtība',
        },
        weekText: 'Ned.',
        allDayText: 'Visu dienu',
        moreLinkText(n) {
            return '+vēl ' + n;
        },
        noEventsText: 'Nav notikumu',
    };

    index_js.globalLocales.push(locale);

})(FullCalendar);
