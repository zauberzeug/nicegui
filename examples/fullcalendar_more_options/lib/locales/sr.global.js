/*!
FullCalendar Core v6.1.10
Docs & License: https://fullcalendar.io
(c) 2023 Adam Shaw
*/
(function (index_js) {
    'use strict';

    var locale = {
        code: 'sr',
        week: {
            dow: 1,
            doy: 7, // The week that contains Jan 1st is the first week of the year.
        },
        buttonText: {
            prev: 'Prethodna',
            next: 'Sledeći',
            today: 'Danas',
            year: 'Godina',
            month: 'Mеsеc',
            week: 'Nеdеlja',
            day: 'Dan',
            list: 'Planеr',
        },
        weekText: 'Sed',
        allDayText: 'Cеo dan',
        moreLinkText(n) {
            return '+ još ' + n;
        },
        noEventsText: 'Nеma događaja za prikaz',
    };

    index_js.globalLocales.push(locale);

})(FullCalendar);
