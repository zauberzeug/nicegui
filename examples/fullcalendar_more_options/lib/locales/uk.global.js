/*!
FullCalendar Core v6.1.10
Docs & License: https://fullcalendar.io
(c) 2023 Adam Shaw
*/
(function (index_js) {
    'use strict';

    var locale = {
        code: 'uk',
        week: {
            dow: 1,
            doy: 7, // The week that contains Jan 1st is the first week of the year.
        },
        buttonText: {
            prev: 'Попередній',
            next: 'далі',
            today: 'Сьогодні',
            year: 'рік',
            month: 'Місяць',
            week: 'Тиждень',
            day: 'День',
            list: 'Порядок денний',
        },
        weekText: 'Тиж',
        allDayText: 'Увесь день',
        moreLinkText(n) {
            return '+ще ' + n + '...';
        },
        noEventsText: 'Немає подій для відображення',
    };

    index_js.globalLocales.push(locale);

})(FullCalendar);
