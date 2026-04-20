// uplot_helpers.js


/**
 * Equal compare for plain objects/arrays
 * @param {object} a
 * @param {object} b
 * @returns {boolean}
 */
function deepCompare(a, b) {
    if (a === b) return true;
    if (typeof a !== typeof b) return false;
    if (!a || !b || typeof a !== 'object') return false;
    if (Array.isArray(a)) {
        if (!Array.isArray(b) || a.length !== b.length) return false;
        for (let i = 0; i < a.length; i++) {
            if (!deepCompare(a[i], b[i])) return false;
        }
        return true;
    }
    // plain object
    const aKeys = Object.keys(a);
    const bKeys = Object.keys(b);
    if (aKeys.length !== bKeys.length) return false;
    for (let i = 0; i < aKeys.length; i++) {
        const k = aKeys[i];
        if (!b.hasOwnProperty(k) || !deepCompare(a[k], b[k])) return false;
    }
    return true;
}

/**
 * Compares uPlot options for update/create/keep
 * @param {Object} _lhs
 * @param {Object} _rhs
 * @returns {'keep'|'update'|'create'}
 */
export function optionsUpdateState(_lhs, _rhs) {
    const {width: lhsWidth, height: lhsHeight, plugins: lhsPlugins, ...lhs} = _lhs;
    const {width: rhsWidth, height: rhsHeight, plugins: rhsPlugins, ...rhs} = _rhs;
    let state = 'keep';
    if (lhsHeight !== rhsHeight || lhsWidth !== rhsWidth) {
        state = 'update';
    }
    if (Object.keys(lhs).length !== Object.keys(rhs).length) {
        return 'create';
    }
    const lhsKeys = Object.keys(lhs);
    for (let i = 0; i < lhsKeys.length; i++) {
        const k = lhsKeys[i];
        if (!deepCompare(lhs[k], rhs[k])) {
            return 'create';
        }
    }

    function extractPluginNames(plugins) {
        if (!plugins) return [];
        if (Array.isArray(plugins)) {
            return plugins.map(p => {
                if (typeof p === 'string') return p;
                if (typeof p === 'object' && p && p.name && typeof p.name === 'string') return p.name;
                return null; // skip unknown types
            }).filter(Boolean);
        }
        if (typeof plugins === 'string') return [plugins];
        if (typeof plugins === 'object' && plugins && 'name' in plugins && typeof plugins.name === 'string') return [plugins.name];
        return [];
    }
    const lhsNames = extractPluginNames(lhsPlugins);
    const rhsNames = extractPluginNames(rhsPlugins);
    if (lhsNames.length !== rhsNames.length || lhsNames.some(n => !rhsNames.includes(n)) || rhsNames.some(n => !lhsNames.includes(n))) {
        state = 'create';
    }
    return state;
}

/**
 * Compares uPlot data arrays
 * @param {Array} lhs
 * @param {Array} rhs
 * @returns {boolean}
 */
export function dataMatch(lhs, rhs) {
    if (lhs.length !== rhs.length) {
        return false;
    }
    return lhs.every(function(lhsOneSeries, seriesIdx) {
        const rhsOneSeries = rhs[seriesIdx];
        if (lhsOneSeries.length !== rhsOneSeries.length) {
            return false;
        }
        return lhsOneSeries.every(function(value, valueIdx) {
            return value === rhsOneSeries[valueIdx];
        });
    });
}
