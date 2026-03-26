// Polyfill for Object.is
if (!Object.is) {
    Object.defineProperty(Object, "is", {
        value: function(x, y) {
            return (x === y && (x !== 0 || 1 / x === 1 / y)) || (x !== x && y !== y);
        },
        configurable: true,
        enumerable: false,
        writable: true
    });
}

// Compares uPlot options for update/create/keep
function optionsUpdateState(_lhs, _rhs) {
    const {width: lhsWidth, height: lhsHeight, ...lhs} = _lhs;
    const {width: rhsWidth, height: rhsHeight, ...rhs} = _rhs;

    let state = 'keep';
    if (lhsHeight !== rhsHeight || lhsWidth !== rhsWidth) {
        state = 'update';
    }
    if (Object.keys(lhs).length !== Object.keys(rhs).length) {
        return 'create';
    }
    for (const k of Object.keys(lhs)) {
        if (!Object.is(lhs[k], rhs[k])) {
            state = 'create';
            break;
        }
    }
    return state;
}

// Compares uPlot data arrays
function dataMatch(lhs, rhs) {
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

// Based on uplot-vue by @skalinichev (https://github.com/skalinichev/uplot-wrappers)
export default {
    template: '<div></div>',
    props: {
        options: { type: Object, required: true },
        data: { type: Array, required: true },
        resetScales: { type: Boolean, required: false, default: true },
        class: { type: String, required: false },
    },
    data() {
        return { _chart: null, _uPlot: null };
    },
    async mounted() {
        const { uPlot } = await import('nicegui-uplot');
        this._uPlot = uPlot;
        this._create();
    },
    unmounted() {
        this._destroy();
    },
    watch: {
        options: {
            handler(options, prevOptions) {
                const optionsState = optionsUpdateState(prevOptions, options);
                if (!this._chart || optionsState === 'create') {
                    this._destroy();
                    this._create();
                } else if (optionsState === 'update') {
                    this._chart.setSize({ width: options.width, height: options.height });
                }
            },
            deep: true
        },
        data: {
            handler(data, prevData) {
                if (!this._chart) {
                    this._create();
                } else if (!dataMatch(prevData, data)) {
                    if (this.$props.resetScales) {
                        this._chart.setData(data);
                    } else {
                        this._chart.setData(data, false);
                        this._chart.redraw();
                    }
                }
            },
            deep: true
        }
    },
    methods: {
        _destroy() {
            if (this._chart) {
                this._chart.destroy();
                this._chart = null;
            }
        },
        _create() {
            if (!this._uPlot) return;
            if (this._chart) {
                this._destroy();
            }
            this._chart = new this._uPlot(this.$props.options, this.$props.data, this.$el);
        },
    },
};
