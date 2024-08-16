/*!
FullCalendar Core v6.1.10
Docs & License: https://fullcalendar.io
(c) 2023 Adam Shaw
*/
!function(e){"use strict";var a={code:"pt-br",buttonText:{prev:"Anterior",next:"Próximo",prevYear:"Ano anterior",nextYear:"Próximo ano",year:"Ano",today:"Hoje",month:"Mês",week:"Semana",day:"Dia",list:"Lista"},buttonHints:{prev:"$0 Anterior",next:"Próximo $0",today:e=>"Dia"===e?"Hoje":("Semana"===e?"Esta":"Este")+" "+e.toLocaleLowerCase()},viewHint:e=>"Visualizar "+("Semana"===e?"a":"o")+" "+e.toLocaleLowerCase(),weekText:"Sm",weekTextLong:"Semana",allDayText:"dia inteiro",moreLinkText:e=>"mais +"+e,moreLinkHint:e=>`Mostrar mais ${e} eventos`,noEventsText:"Não há eventos para mostrar",navLinkHint:"Ir para $0",closeHint:"Fechar",timeHint:"A hora",eventHint:"Evento"};FullCalendar.globalLocales.push(a)}();