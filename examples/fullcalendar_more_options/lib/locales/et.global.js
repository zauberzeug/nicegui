/*!
FullCalendar Core v6.1.10
Docs & License: https://fullcalendar.io
(c) 2023 Adam Shaw
*/
(function (index_js) {
    'use strict';

    var locale = {
        code: 'et',
        week: {
            dow: 1,
            doy: 4, // The week that contains Jan 4th is the first week of the year.
        },
        buttonText: {
            prev: 'Eelnev',
            next: 'Järgnev',
            today: 'Täna',
            year: 'Aasta',
            month: 'Kuu',
            week: 'Nädal',
            day: 'Päev',
            list: 'Päevakord',
        },
        weekText: 'näd',
        allDayText: 'Kogu päev',
        moreLinkText(n) {
            return '+ veel ' + n;
        },
        noEventsText: 'Kuvamiseks puuduvad sündmused',
    };

    index_js.globalLocales.push(locale);

})(FullCalendar);
