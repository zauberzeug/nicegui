/*!
FullCalendar Core v6.1.10
Docs & License: https://fullcalendar.io
(c) 2023 Adam Shaw
*/
!function(e){"use strict";function t(e){return"Tag"===e||"Monat"===e?"r":"Jahr"===e?"s":""}var n={code:"de-at",week:{dow:1,doy:4},buttonText:{prev:"Zurück",next:"Vor",today:"Heute",year:"Jahr",month:"Monat",week:"Woche",day:"Tag",list:"Terminübersicht"},weekText:"KW",weekTextLong:"Woche",allDayText:"Ganztägig",moreLinkText:e=>"+ weitere "+e,noEventsText:"Keine Ereignisse anzuzeigen",buttonHints:{prev:e=>`Vorherige${t(e)} ${e}`,next:e=>`Nächste${t(e)} ${e}`,today:e=>"Tag"===e?"Heute":`Diese${t(e)} ${e}`},viewHint:e=>e+("Woche"===e?"n":"Monat"===e?"s":"es")+"ansicht",navLinkHint:"Gehe zu $0",moreLinkHint:e=>"Zeige "+(1===e?"ein weiteres Ereignis":e+" weitere Ereignisse"),closeHint:"Schließen",timeHint:"Uhrzeit",eventHint:"Ereignis"};FullCalendar.globalLocales.push(n)}();