/*!
FullCalendar Core v6.1.10
Docs & License: https://fullcalendar.io
(c) 2023 Adam Shaw
*/
(function (index_js) {
    'use strict';

    var locale = {
        code: 'bg',
        week: {
            dow: 1,
            doy: 4, // The week that contains Jan 4th is the first week of the year.
        },
        buttonText: {
            prev: 'назад',
            next: 'напред',
            today: 'днес',
            year: 'година',
            month: 'Месец',
            week: 'Седмица',
            day: 'Ден',
            list: 'График',
        },
        allDayText: 'Цял ден',
        moreLinkText(n) {
            return '+още ' + n;
        },
        noEventsText: 'Няма събития за показване',
    };

    index_js.globalLocales.push(locale);

})(FullCalendar);
