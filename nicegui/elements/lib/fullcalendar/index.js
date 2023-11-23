import { globalPlugins } from '@fullcalendar/core/index.js';
export * from '@fullcalendar/core/index.js';
import interactionPlugin__default from '@fullcalendar/interaction/index.js';
export * from '@fullcalendar/interaction/index.js';
import dayGridPlugin from '@fullcalendar/daygrid/index.js';
import timeGridPlugin from '@fullcalendar/timegrid/index.js';
import listPlugin from '@fullcalendar/list/index.js';
import multiMonthPlugin from '@fullcalendar/multimonth/index.js';

globalPlugins.push(interactionPlugin__default, dayGridPlugin, timeGridPlugin, listPlugin, multiMonthPlugin);
