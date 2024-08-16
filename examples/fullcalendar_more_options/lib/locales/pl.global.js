/*!
FullCalendar Core v6.1.10
Docs & License: https://fullcalendar.io
(c) 2023 Adam Shaw
*/
(function (index_js) {
    'use strict';

    var locale = {
        code: 'pl',
        week: {
            dow: 1,
            doy: 4, // The week that contains Jan 4th is the first week of the year.
        },
        buttonText: {
            prev: 'Poprzedni',
            next: 'Następny',
            today: 'Dziś',
            year: 'Rok',
            month: 'Miesiąc',
            week: 'Tydzień',
            day: 'Dzień',
            list: 'Plan dnia',
        },
        weekText: 'Tydz',
        allDayText: 'Cały dzień',
        moreLinkText: 'więcej',
        noEventsText: 'Brak wydarzeń do wyświetlenia',
    };

    index_js.globalLocales.push(locale);

})(FullCalendar);
