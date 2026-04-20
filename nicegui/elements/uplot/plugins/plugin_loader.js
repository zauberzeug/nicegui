// plugin_loader.js

/**
 * Registry of plugins
 */
export const pluginLoaders = {
    wheelZoom: async (opts) => {
        const { wheelZoomPlugin } = await import('../plugins/wheelzoom.js');
        return wheelZoomPlugin(opts);
    },
    touchZoom: async () => {
        const { touchZoomPlugin } = await import('../plugins/touchzoom.js');
        return touchZoomPlugin();
    },
    legendAsTooltip: async (opts) => {
        const { legendAsTooltipPlugin } = await import('../plugins/legendtooltip.js');
        return legendAsTooltipPlugin(opts);
    },
};

/**
 * Resolves a plugin by name and options, using the registry or global window
 * @param {string} name
 * @param {object} [opts]
 * @returns {Promise<any|null>}
 */
export async function resolvePlugin(name, opts) {
    if (pluginLoaders[name]) {
        return await pluginLoaders[name](opts);
    }
    if (typeof window !== 'undefined' && typeof window[name] === 'function') {
        return window[name](opts);
    }
    return null;
}
