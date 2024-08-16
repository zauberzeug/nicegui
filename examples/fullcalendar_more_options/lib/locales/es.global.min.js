/*!
FullCalendar Core v6.1.10
Docs & License: https://fullcalendar.io
(c) 2023 Adam Shaw
*/
!function(e){"use strict";var t={code:"es",week:{dow:1,doy:4},buttonText:{prev:"Ant",next:"Sig",today:"Hoy",year:"Año",month:"Mes",week:"Semana",day:"Día",list:"Agenda"},buttonHints:{prev:"$0 antes",next:"$0 siguiente",today:e=>"Día"===e?"Hoy":("Semana"===e?"Esta":"Este")+" "+e.toLocaleLowerCase()},viewHint:e=>"Vista "+("Semana"===e?"de la":"del")+" "+e.toLocaleLowerCase(),weekText:"Sm",weekTextLong:"Semana",allDayText:"Todo el día",moreLinkText:"más",moreLinkHint:e=>`Mostrar ${e} eventos más`,noEventsText:"No hay eventos para mostrar",navLinkHint:"Ir al $0",closeHint:"Cerrar",timeHint:"La hora",eventHint:"Evento"};FullCalendar.globalLocales.push(t)}();