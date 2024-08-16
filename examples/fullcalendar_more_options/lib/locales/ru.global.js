/*!
FullCalendar Core v6.1.10
Docs & License: https://fullcalendar.io
(c) 2023 Adam Shaw
*/
(function (index_js) {
    'use strict';

    var locale = {
        code: 'ru',
        week: {
            dow: 1,
            doy: 4, // The week that contains Jan 4th is the first week of the year.
        },
        buttonText: {
            prev: 'Пред',
            next: 'След',
            today: 'Сегодня',
            year: 'Год',
            month: 'Месяц',
            week: 'Неделя',
            day: 'День',
            list: 'Повестка дня',
        },
        weekText: 'Нед',
        allDayText: 'Весь день',
        moreLinkText(n) {
            return '+ ещё ' + n;
        },
        noEventsText: 'Нет событий для отображения',
    };

    index_js.globalLocales.push(locale);

})(FullCalendar);
