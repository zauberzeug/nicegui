/*!
FullCalendar Core v6.1.10
Docs & License: https://fullcalendar.io
(c) 2023 Adam Shaw
*/
(function (index_js) {
    'use strict';

    var locale = {
        code: 'fi',
        week: {
            dow: 1,
            doy: 4, // The week that contains Jan 4th is the first week of the year.
        },
        buttonText: {
            prev: 'Edellinen',
            next: 'Seuraava',
            today: 'Tänään',
            year: 'Vuosi',
            month: 'Kuukausi',
            week: 'Viikko',
            day: 'Päivä',
            list: 'Tapahtumat',
        },
        weekText: 'Vk',
        allDayText: 'Koko päivä',
        moreLinkText: 'lisää',
        noEventsText: 'Ei näytettäviä tapahtumia',
    };

    index_js.globalLocales.push(locale);

})(FullCalendar);
