/*!
FullCalendar Core v6.1.10
Docs & License: https://fullcalendar.io
(c) 2023 Adam Shaw
*/
(function (index_js) {
    'use strict';

    var locale = {
        code: 'az',
        week: {
            dow: 1,
            doy: 4, // The week that contains Jan 4th is the first week of the year.
        },
        buttonText: {
            prev: 'Əvvəl',
            next: 'Sonra',
            today: 'Bu Gün',
            year: 'Il',
            month: 'Ay',
            week: 'Həftə',
            day: 'Gün',
            list: 'Gündəm',
        },
        weekText: 'Həftə',
        allDayText: 'Bütün Gün',
        moreLinkText(n) {
            return '+ daha çox ' + n;
        },
        noEventsText: 'Göstərmək üçün hadisə yoxdur',
    };

    index_js.globalLocales.push(locale);

})(FullCalendar);
