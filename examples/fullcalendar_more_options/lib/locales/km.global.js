/*!
FullCalendar Core v6.1.10
Docs & License: https://fullcalendar.io
(c) 2023 Adam Shaw
*/
(function (index_js) {
    'use strict';

    var locale = {
        code: 'km',
        week: {
            dow: 1,
            doy: 4, // The week that contains Jan 4th is the first week of the year.
        },
        buttonText: {
            prev: 'មុន',
            next: 'បន្ទាប់',
            today: 'ថ្ងៃនេះ',
            year: 'ឆ្នាំ',
            month: 'ខែ',
            week: 'សប្តាហ៍',
            day: 'ថ្ងៃ',
            list: 'បញ្ជី',
        },
        weekText: 'សប្តាហ៍',
        allDayText: 'ពេញមួយថ្ងៃ',
        moreLinkText: 'ច្រើនទៀត',
        noEventsText: 'គ្មានព្រឹត្តិការណ៍ត្រូវបង្ហាញ',
    };

    index_js.globalLocales.push(locale);

})(FullCalendar);
