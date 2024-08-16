/*!
FullCalendar Core v6.1.10
Docs & License: https://fullcalendar.io
(c) 2023 Adam Shaw
*/
(function (index_js) {
    'use strict';

    var locale = {
        code: 'ar-ly',
        week: {
            dow: 6,
            doy: 12, // The week that contains Jan 1st is the first week of the year.
        },
        direction: 'rtl',
        buttonText: {
            prev: 'السابق',
            next: 'التالي',
            today: 'اليوم',
            year: 'سنة',
            month: 'شهر',
            week: 'أسبوع',
            day: 'يوم',
            list: 'أجندة',
        },
        weekText: 'أسبوع',
        allDayText: 'اليوم كله',
        moreLinkText: 'أخرى',
        noEventsText: 'أي أحداث لعرض',
    };

    index_js.globalLocales.push(locale);

})(FullCalendar);
