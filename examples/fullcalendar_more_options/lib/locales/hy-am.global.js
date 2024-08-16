/*!
FullCalendar Core v6.1.10
Docs & License: https://fullcalendar.io
(c) 2023 Adam Shaw
*/
(function (index_js) {
    'use strict';

    var locale = {
        code: 'hy-am',
        week: {
            dow: 1,
            doy: 4, // The week that contains Jan 4th is the first week of the year.
        },
        buttonText: {
            prev: 'Նախորդ',
            next: 'Հաջորդ',
            today: 'Այսօր',
            year: 'Տարի',
            month: 'Ամիս',
            week: 'Շաբաթ',
            day: 'Օր',
            list: 'Օրվա ցուցակ',
        },
        weekText: 'Շաբ',
        allDayText: 'Ամբողջ օր',
        moreLinkText(n) {
            return '+ ևս ' + n;
        },
        noEventsText: 'Բացակայում է իրադարձությունը ցուցադրելու',
    };

    index_js.globalLocales.push(locale);

})(FullCalendar);
