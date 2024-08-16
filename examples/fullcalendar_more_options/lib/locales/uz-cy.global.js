/*!
FullCalendar Core v6.1.10
Docs & License: https://fullcalendar.io
(c) 2023 Adam Shaw
*/
(function (index_js) {
    'use strict';

    var locale = {
        code: 'uz-cy',
        week: {
            dow: 1,
            doy: 4, // The week that contains Jan 4th is the first week of the year.
        },
        buttonText: {
            prev: 'Олин',
            next: 'Кейин',
            today: 'Бугун',
            month: 'Ой',
            week: 'Ҳафта',
            day: 'Кун',
            list: 'Кун тартиби',
        },
        weekText: 'Ҳафта',
        allDayText: 'Кун бўйича',
        moreLinkText(n) {
            return '+ яна ' + n;
        },
        noEventsText: 'Кўрсатиш учун воқеалар йўқ',
    };

    index_js.globalLocales.push(locale);

})(FullCalendar);
