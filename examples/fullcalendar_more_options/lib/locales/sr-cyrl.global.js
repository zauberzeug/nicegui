/*!
FullCalendar Core v6.1.10
Docs & License: https://fullcalendar.io
(c) 2023 Adam Shaw
*/
(function (index_js) {
    'use strict';

    var locale = {
        code: 'sr-cyrl',
        week: {
            dow: 1,
            doy: 7, // The week that contains Jan 1st is the first week of the year.
        },
        buttonText: {
            prev: 'Претходна',
            next: 'следећи',
            today: 'Данас',
            year: 'Година',
            month: 'Месец',
            week: 'Недеља',
            day: 'Дан',
            list: 'Планер',
        },
        weekText: 'Сед',
        allDayText: 'Цео дан',
        moreLinkText(n) {
            return '+ још ' + n;
        },
        noEventsText: 'Нема догађаја за приказ',
    };

    index_js.globalLocales.push(locale);

})(FullCalendar);
