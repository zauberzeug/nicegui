/*!
FullCalendar Core v6.1.10
Docs & License: https://fullcalendar.io
(c) 2023 Adam Shaw
*/
!function(e){"use strict";var a={code:"gl",week:{dow:1,doy:4},buttonText:{prev:"Ant",next:"Seg",today:"Hoxe",year:"Ano",month:"Mes",week:"Semana",day:"Día",list:"Axenda"},buttonHints:{prev:"$0 antes",next:"$0 seguinte",today:e=>"Día"===e?"Hoxe":("Semana"===e?"Esta":"Este")+" "+e.toLocaleLowerCase()},viewHint:e=>"Vista "+("Semana"===e?"da":"do")+" "+e.toLocaleLowerCase(),weekText:"Sm",weekTextLong:"Semana",allDayText:"Todo o día",moreLinkText:"máis",moreLinkHint:e=>`Amosar ${e} eventos máis`,noEventsText:"Non hai eventos para amosar",navLinkHint:"Ir ao $0",closeHint:"Pechar",timeHint:"A hora",eventHint:"Evento"};FullCalendar.globalLocales.push(a)}();