/*!
FullCalendar Core v6.1.10
Docs & License: https://fullcalendar.io
(c) 2023 Adam Shaw
*/
(function (index_js) {
    'use strict';

    var locale = {
        code: 'eu',
        week: {
            dow: 1,
            doy: 7, // The week that contains Jan 1st is the first week of the year.
        },
        buttonText: {
            prev: 'Aur',
            next: 'Hur',
            today: 'Gaur',
            year: 'Urtea',
            month: 'Hilabetea',
            week: 'Astea',
            day: 'Eguna',
            list: 'Agenda',
        },
        weekText: 'As',
        allDayText: 'Egun osoa',
        moreLinkText: 'gehiago',
        noEventsText: 'Ez dago ekitaldirik erakusteko',
    };

    index_js.globalLocales.push(locale);

})(FullCalendar);
