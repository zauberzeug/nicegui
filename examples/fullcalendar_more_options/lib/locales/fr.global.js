/*!
FullCalendar Core v6.1.10
Docs & License: https://fullcalendar.io
(c) 2023 Adam Shaw
*/
(function (index_js) {
    'use strict';

    var locale = {
        code: 'fr',
        week: {
            dow: 1,
            doy: 4, // The week that contains Jan 4th is the first week of the year.
        },
        buttonText: {
            prev: 'Précédent',
            next: 'Suivant',
            today: 'Aujourd\'hui',
            year: 'Année',
            month: 'Mois',
            week: 'Semaine',
            day: 'Jour',
            list: 'Planning',
        },
        weekText: 'Sem.',
        weekTextLong: 'Semaine',
        allDayText: 'Toute la journée',
        moreLinkText: 'en plus',
        noEventsText: 'Aucun évènement à afficher',
    };

    index_js.globalLocales.push(locale);

})(FullCalendar);
