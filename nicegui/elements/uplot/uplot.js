

import { convertDynamicProperties } from "../../static/utils/dynamic_properties.js";
import { uPlot, resolvePlugin, optionsUpdateState, dataMatch } from "nicegui-uplot";

// Plugin cache to avoid redundant loading on refresh
const pluginCache = new Map();

// Based on uplot-vue by @skalinichev (https://github.com/skalinichev/uplot-wrappers)
export default {
    template: '<div></div>',
    props: {
        options: { type: Object, required: true },
        data: { type: Array, required: true },
        resetScales: { type: Boolean, required: false, default: true },
    },
    data() {
        return {
            _chart: null,
            _uPlot: null,
            lastPluginNames: [],
        };
    },
    async mounted() {
        this._uPlot = uPlot;
        await this._create();
    },
    unmounted() {
        this._destroy();
    },
    watch: {
        options: {
            handler(options, prevOptions) {
                (async () => {
                    let next = { ...options };
                    let prev = { ...prevOptions };
                    convertDynamicProperties(next, true);
                    convertDynamicProperties(prev, true);
                    prev.plugins = this.lastPluginNames ? this.lastPluginNames : prev.plugins;
                    const optionsState = optionsUpdateState(prev, next);
                    if (!this._chart || optionsState === 'create') {
                        this._destroy();
                        await this._create();
                    } else if (optionsState === 'update') {
                        this._chart.setSize({ width: options.width, height: options.height });
                    }
                })();
            },
            deep: true
        },
        data: {
            handler(data, prevData) {
                (async () => {
                    if (!this._chart) {
                        await this._create();
                    } else if (!dataMatch(prevData, data)) {
                        if (this.$props.resetScales) {
                            this._chart.setData(data);
                            var min = Math.min(...prevData[0]);
                            var max = Math.max(...prevData[0]);
                            if (this._chart.scales.x.max != max || this._chart.scales.x.min != min) {
                                this._restoreZoomState();
                            }
                        } else {
                            this._chart.setData(data, false);
                            this._chart.redraw();
                        }
                    }
                })();
            },
            deep: true
        }
    },
    methods: {
        _restoreZoomState() {
            if (this._chart) {
                const zoom = {};
                for (const [key, scale] of Object.entries(this._chart.scales)) {
                    if (scale && typeof scale.min === 'number' && typeof scale.max === 'number') {
                        zoom[key] = { min: scale.min, max: scale.max };
                    }
                }
                if (zoom) {
                    for (const [key, state] of Object.entries(zoom)) {
                        if (this._chart.scales && this._chart.scales[key] && typeof state.min === 'number' && typeof state.max === 'number') {
                            this._chart.setScale(key, { min: state.min, max: state.max });
                        }
                    }
                }
            }
        },
        _destroy() {
            if (this._chart) {
                this._chart.destroy();
                this._chart = null;
            }
        },
        async _create() {
            if (!this._uPlot) return;
            if (this._chart) {
                this._destroy();
            }
            let options = { ...this.$props.options };
            convertDynamicProperties(options, true);
            if (options.plugins && Array.isArray(options.plugins)) {
                const lastPluginNames = [];
                options.plugins = (await Promise.all(options.plugins.map(async plugin => {
                    let name = null;
                    if (typeof plugin === 'string') name = plugin;
                    if (typeof plugin === 'object' && plugin && plugin.name) name = plugin.name;
                    if (name) lastPluginNames.push(name);
                    if (name && pluginCache.has(name)) {
                        return pluginCache.get(name);
                    }
                    if (typeof plugin === 'string') {
                        const loaded = await resolvePlugin(plugin);
                        if (loaded) {
                            pluginCache.set(plugin, loaded);
                            return loaded;
                        }
                        if (typeof window !== 'undefined' && typeof window[plugin] === 'function') {
                            const winLoaded = window[plugin]();
                            pluginCache.set(plugin, winLoaded);
                            return winLoaded;
                        }
                    }
                    if (typeof plugin === 'object' && plugin.name) {
                        const loaded = await resolvePlugin(plugin.name, plugin.options || {});
                        if (loaded) {
                            pluginCache.set(plugin.name, loaded);
                            return loaded;
                        }
                        if (typeof window !== 'undefined' && typeof window[plugin.name] === 'function') {
                            const winLoaded = window[plugin.name](plugin.options || {});
                            pluginCache.set(plugin.name, winLoaded);
                            return winLoaded;
                        }
                    }
                    return plugin;
                }))).filter(Boolean);
                this.lastPluginNames = lastPluginNames;
            }
            this._chart = new this._uPlot(options, this.$props.data, this.$el);
        },
    },
};
