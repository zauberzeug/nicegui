/*!
FullCalendar Core v6.1.10
Docs & License: https://fullcalendar.io
(c) 2023 Adam Shaw
*/
(function (index_js) {
    'use strict';

    var locale = {
        code: 'el',
        week: {
            dow: 1,
            doy: 4, // The week that contains Jan 4st is the first week of the year.
        },
        buttonText: {
            prev: 'Προηγούμενος',
            next: 'Επόμενος',
            today: 'Σήμερα',
            year: 'Ετος',
            month: 'Μήνας',
            week: 'Εβδομάδα',
            day: 'Ημέρα',
            list: 'Ατζέντα',
        },
        weekText: 'Εβδ',
        allDayText: 'Ολοήμερο',
        moreLinkText: 'περισσότερα',
        noEventsText: 'Δεν υπάρχουν γεγονότα προς εμφάνιση',
    };

    index_js.globalLocales.push(locale);

})(FullCalendar);
