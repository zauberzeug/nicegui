/*!
FullCalendar Core v6.1.10
Docs & License: https://fullcalendar.io
(c) 2023 Adam Shaw
*/
(function (index_js) {
    'use strict';

    var locale = {
        code: 'th',
        week: {
            dow: 1,
            doy: 4, // The week that contains Jan 4th is the first week of the year.
        },
        buttonText: {
            prev: 'ก่อนหน้า',
            next: 'ถัดไป',
            prevYear: 'ปีก่อนหน้า',
            nextYear: 'ปีถัดไป',
            year: 'ปี',
            today: 'วันนี้',
            month: 'เดือน',
            week: 'สัปดาห์',
            day: 'วัน',
            list: 'กำหนดการ',
        },
        weekText: 'สัปดาห์',
        allDayText: 'ตลอดวัน',
        moreLinkText: 'เพิ่มเติม',
        noEventsText: 'ไม่มีกิจกรรมที่จะแสดง',
    };

    index_js.globalLocales.push(locale);

})(FullCalendar);
