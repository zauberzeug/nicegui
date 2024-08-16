/*!
FullCalendar Core v6.1.10
Docs & License: https://fullcalendar.io
(c) 2023 Adam Shaw
*/
!function(e){"use strict";var t={code:"sv",week:{dow:1,doy:4},buttonText:{prev:"Förra",next:"Nästa",today:"Idag",year:"År",month:"Månad",week:"Vecka",day:"Dag",list:"Program"},buttonHints:{prev:e=>"Föregående "+e.toLocaleLowerCase(),next:e=>"Nästa "+e.toLocaleLowerCase(),today:e=>("Program"===e?"Detta":"Denna")+" "+e.toLocaleLowerCase()},viewHint:"$0 vy",navLinkHint:"Gå till $0",moreLinkHint:e=>`Visa ytterligare ${e} händelse${1===e?"":"r"}`,weekText:"v.",weekTextLong:"Vecka",allDayText:"Heldag",moreLinkText:"till",noEventsText:"Inga händelser att visa",closeHint:"Stäng",timeHint:"Klockan",eventHint:"Händelse"};FullCalendar.globalLocales.push(t)}();