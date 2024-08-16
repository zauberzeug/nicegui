/*!
FullCalendar Core v6.1.10
Docs & License: https://fullcalendar.io
(c) 2023 Adam Shaw
*/
(function (index_js) {
    'use strict';

    var locale = {
        code: 'uz',
        week: {
            dow: 1,
            doy: 4, // The week that contains Jan 4th is the first week of the year.
        },
        buttonText: {
            prev: 'Oldingi',
            next: 'Keyingi',
            today: 'Bugun',
            year: 'Yil',
            month: 'Oy',
            week: 'Xafta',
            day: 'Kun',
            list: 'Kun tartibi',
        },
        allDayText: 'Kun bo\'yi',
        moreLinkText(n) {
            return '+ yana ' + n;
        },
        noEventsText: 'Ko\'rsatish uchun voqealar yo\'q',
    };

    index_js.globalLocales.push(locale);

})(FullCalendar);
