/*!
FullCalendar Core v6.1.10
Docs & License: https://fullcalendar.io
(c) 2023 Adam Shaw
*/
(function (index_js) {
    'use strict';

    var locale = {
        code: 'kk',
        week: {
            dow: 1,
            doy: 7, // The week that contains Jan 1st is the first week of the year.
        },
        buttonText: {
            prev: 'Алдыңғы',
            next: 'Келесі',
            today: 'Бүгін',
            year: 'Жыл',
            month: 'Ай',
            week: 'Апта',
            day: 'Күн',
            list: 'Күн тәртібі',
        },
        weekText: 'Не',
        allDayText: 'Күні бойы',
        moreLinkText(n) {
            return '+ тағы ' + n;
        },
        noEventsText: 'Көрсету үшін оқиғалар жоқ',
    };

    index_js.globalLocales.push(locale);

})(FullCalendar);
