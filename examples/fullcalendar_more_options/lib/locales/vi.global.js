/*!
FullCalendar Core v6.1.10
Docs & License: https://fullcalendar.io
(c) 2023 Adam Shaw
*/
(function (index_js) {
    'use strict';

    var locale = {
        code: 'vi',
        week: {
            dow: 1,
            doy: 4, // The week that contains Jan 4th is the first week of the year.
        },
        buttonText: {
            prev: 'Trước',
            next: 'Tiếp',
            today: 'Hôm nay',
            year: 'Năm',
            month: 'Tháng',
            week: 'Tuần',
            day: 'Ngày',
            list: 'Lịch biểu',
        },
        weekText: 'Tu',
        allDayText: 'Cả ngày',
        moreLinkText(n) {
            return '+ thêm ' + n;
        },
        noEventsText: 'Không có sự kiện để hiển thị',
    };

    index_js.globalLocales.push(locale);

})(FullCalendar);
