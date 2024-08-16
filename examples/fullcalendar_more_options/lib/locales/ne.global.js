/*!
FullCalendar Core v6.1.10
Docs & License: https://fullcalendar.io
(c) 2023 Adam Shaw
*/
(function (index_js) {
    'use strict';

    var locale = {
        code: 'ne',
        week: {
            dow: 7,
            doy: 1, // The week that contains Jan 1st is the first week of the year.
        },
        buttonText: {
            prev: 'अघिल्लो',
            next: 'अर्को',
            today: 'आज',
            year: 'वर्ष',
            month: 'महिना',
            week: 'हप्ता',
            day: 'दिन',
            list: 'सूची',
        },
        weekText: 'हप्ता',
        allDayText: 'दिनभरि',
        moreLinkText: 'थप लिंक',
        noEventsText: 'देखाउनको लागि कुनै घटनाहरू छैनन्',
    };

    index_js.globalLocales.push(locale);

})(FullCalendar);
