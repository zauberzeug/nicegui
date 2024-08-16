/*!
FullCalendar Core v6.1.10
Docs & License: https://fullcalendar.io
(c) 2023 Adam Shaw
*/
(function (index_js) {
    'use strict';

    var locale = {
        code: 'ta-in',
        week: {
            dow: 1,
            doy: 4, // The week that contains Jan 4th is the first week of the year.
        },
        buttonText: {
            prev: 'முந்தைய',
            next: 'அடுத்தது',
            today: 'இன்று',
            year: 'ஆண்டு',
            month: 'மாதம்',
            week: 'வாரம்',
            day: 'நாள்',
            list: 'தினசரி அட்டவணை',
        },
        weekText: 'வாரம்',
        allDayText: 'நாள் முழுவதும்',
        moreLinkText(n) {
            return '+ மேலும் ' + n;
        },
        noEventsText: 'காண்பிக்க நிகழ்வுகள் இல்லை',
    };

    index_js.globalLocales.push(locale);

})(FullCalendar);
