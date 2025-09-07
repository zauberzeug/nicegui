#!/usr/bin/env python3
"""Demonstrates embedding anywidget widgets in NiceGUI.

This shows how to embed anywidget widgets in NiceGUI, and how to synchronize
NiceGUI elements with widgets using ``.bind_*`` (widget -> NiceGUI) and ``on_*``
callbacks (NiceGUI -> widget).

The example shows how to embed a counter widget and an altair chart widget
from the getting started examples in anywidget and altair.
"""

import altair
import anywidget
import traitlets

from nicegui import ui


class CounterWidget(anywidget.AnyWidget):
    """Baseline anywidget example"""
    _esm = '''
    function render({ model, el }) {
      let button = document.createElement("button");
      button.innerHTML = `anywidget count is ${model.get("value")}`;
      button.addEventListener("click", () => {
        model.set("value", model.get("value") + 1);
        model.save_changes();
      });
      model.on("change:value", () => {
        button.innerHTML = `anywidget count is ${model.get("value")}`;
      });
      el.classList.add("counter-widget");
      el.appendChild(button);
    }
    export default { render };
    '''
    _css = '''
    .counter-widget button { color: white; font-size: 1.75rem; background-color: #ea580c; padding: 0.5rem 1rem; border: none; border-radius: 0.25rem; }
    .counter-widget button:hover { background-color: #9a3412; }
    '''
    value = traitlets.Int(0).tag(sync=True)


class AltairChart(altair.JupyterChart):
    """
    This is a wrapper around `altair.JupyterChart` that just adds some console
    debugging output, and fixes a minor bug with accessing `.changed` (only
    usable in Jupyter-widget-based environments).
    """
    _esm = '''
import vegaEmbed from "https://esm.sh/vega-embed@v7?deps=vega@6&deps=vega-lite@5.33.0";
import lodashDebounce from "https://esm.sh/lodash-es@4.17.21/debounce";

// Note: For offline support, the import lines above are removed and the remaining script
// is bundled using vl-convert's javascript_bundle function. See the documentation of
// the javascript_bundle function for details on the available imports and their names.
// If an additional import is required in the future, it will need to be added to vl-convert
// in order to preserve offline support.
async function render({ model, el }) {
    let finalize;

    function showError(error){
        el.innerHTML = (
            '<div style="color:red;">'
            + '<p>JavaScript Error: ' + error.message + '</p>'
            + "<p>This usually means there's a typo in your chart specification. "
            + "See the javascript console for the full traceback.</p>"
            + '</div>'
        );
    }

    const reembed = async () => {
        if (finalize != null) {
          finalize();
        }

        model.set("local_tz", Intl.DateTimeFormat().resolvedOptions().timeZone);

        let spec = structuredClone(model.get("spec"));
        if (spec == null) {
            // Remove any existing chart and return
            while (el.firstChild) {
                el.removeChild(el.lastChild);
            }
            model.save_changes();
            return;
        }
        let embedOptions = structuredClone(model.get("embed_options")) ?? undefined;

        let api;
        try {
            api = await vegaEmbed(el, spec, embedOptions);
        } catch (error) {
            showError(error)
            return;
        }

        finalize = api.finalize;

        // Debounce config
        const wait = model.get("debounce_wait") ?? 10;
        const debounceOpts = {leading: false, trailing: true};
        if (model.get("max_wait") ?? true) {
            debounceOpts["maxWait"] = wait;
        }

        const initialSelections = {};
        for (const selectionName of Object.keys(model.get("_vl_selections"))) {
            const storeName = `${selectionName}_store`;
            const selectionHandler = (_, value) => {
                const newSelections = cleanJson(model.get("_vl_selections") ?? {});
                const store = cleanJson(api.view.data(storeName) ?? []);

                newSelections[selectionName] = {value, store};
                model.set("_vl_selections", newSelections);
                model.save_changes();
            };
            api.view.addSignalListener(selectionName, lodashDebounce(selectionHandler, wait, debounceOpts));

            initialSelections[selectionName] = {
                value: cleanJson(api.view.signal(selectionName) ?? {}),
                store: cleanJson(api.view.data(storeName) ?? [])
            }
        }
        model.set("_vl_selections", initialSelections);

        const initialParams = {};
        for (const paramName of Object.keys(model.get("_params"))) {
            const paramHandler = (_, value) => {
                const newParams = JSON.parse(JSON.stringify(model.get("_params"))) || {};
                newParams[paramName] = value;
                model.set("_params", newParams);
                model.save_changes();
            };
            api.view.addSignalListener(paramName, lodashDebounce(paramHandler, wait, debounceOpts));

            initialParams[paramName] = api.view.signal(paramName) ?? null
        }
        model.set("_params", initialParams);
        model.save_changes();

        // Param change callback
        model.on('change:_params', async (new_params) => {
            console.log('change:_params', new_params);
            for (const [param, value] of Object.entries(new_params)) {
                console.log('change:_params', new_params, param, value);
                api.view.signal(param, value);
            }
            await api.view.runAsync();
            console.log('change:_params done');
        });

        // Add signal/data listeners
        for (const watch of model.get("_js_watch_plan") ?? []) {
            if (watch.namespace === "data") {
                const dataHandler = (_, value) => {
                    model.set("_js_to_py_updates", [{
                        namespace: "data",
                        name: watch.name,
                        scope: watch.scope,
                        value: cleanJson(value)
                    }]);
                    model.save_changes();
                };
                addDataListener(api.view, watch.name, watch.scope, lodashDebounce(dataHandler, wait, debounceOpts))

            } else if (watch.namespace === "signal") {
                const signalHandler = (_, value) => {
                    model.set("_js_to_py_updates", [{
                        namespace: "signal",
                        name: watch.name,
                        scope: watch.scope,
                        value: cleanJson(value)
                    }]);
                    model.save_changes();
                };

                addSignalListener(api.view, watch.name, watch.scope, lodashDebounce(signalHandler, wait, debounceOpts))
            }
        }

        // Add signal/data updaters
        model.on('change:_py_to_js_updates', async (updates) => {
            for (const update of updates.changed._py_to_js_updates ?? []) {
                if (update.namespace === "signal") {
                    console.log('change:_py_to_js_updates signal', update.name, update.scope, update.value);
                    setSignalValue(api.view, update.name, update.scope, update.value);
                } else if (update.namespace === "data") {
                    console.log('change:_py_to_js_updates data', update.name, update.scope, update.value);
                    setDataValue(api.view, update.name, update.scope, update.value);
                }
            }
            await api.view.runAsync();
        });
    }

    model.on('change:spec', reembed);
    model.on('change:embed_options', reembed);
    model.on('change:debounce_wait', reembed);
    model.on('change:max_wait', reembed);
    await reembed();
}

function cleanJson(data) {
    return JSON.parse(JSON.stringify(data))
}

function getNestedRuntime(view, scope) {
    var runtime = view._runtime;
    for (const index of scope) {
        runtime = runtime.subcontext[index];
    }
    return runtime
}

function lookupSignalOp(view, name, scope) {
    let parent_runtime = getNestedRuntime(view, scope);
    return parent_runtime.signals[name] ?? null;
}

function dataRef(view, name, scope) {
    let parent_runtime = getNestedRuntime(view, scope);
    return parent_runtime.data[name];
}

export function setSignalValue(view, name, scope, value) {
    let signal_op = lookupSignalOp(view, name, scope);
    view.update(signal_op, value);
}

export function setDataValue(view, name, scope, value) {
    let dataset = dataRef(view, name, scope);
    let changeset = view.changeset().remove(() => true).insert(value)
    dataset.modified = true;
    view.pulse(dataset.input, changeset);
}

export function addSignalListener(view, name, scope, handler) {
    let signal_op = lookupSignalOp(view, name, scope);
    return addOperatorListener(
        view,
        name,
        signal_op,
        handler,
    );
}

export function addDataListener(view, name, scope, handler) {
    let dataset = dataRef(view, name, scope).values;
    return addOperatorListener(
        view,
        name,
        dataset,
        handler,
    );
}

// Private helpers from Vega for dealing with nested signals/data
function findOperatorHandler(op, handler) {
    const h = (op._targets || [])
        .filter(op => op._update && op._update.handler === handler);
    return h.length ? h[0] : null;
}

function addOperatorListener(view, name, op, handler) {
    let h = findOperatorHandler(op, handler);
    if (!h) {
        h = trap(view, () => handler(name, op.value));
        h.handler = handler;
        view.on(op, null, h);
    }
    return view;
}

function trap(view, fn) {
    return !fn ? null : function() {
        try {
            fn.apply(this, arguments);
        } catch (error) {
            view.error(error);
        }
    };
}

export default { render }
'''

@ui.page('/')
def page():
    ### Example 1: counter widget synchronized with nicegui & anywidget
    # This is the getting started example from the anywidget documentation:
    # https://anywidget.dev/en/getting-started/
    counter = CounterWidget(value=42)
    anywidget_counter = ui.anywidget(counter)

    def increment_counter():
        counter.value += 1
    ui.button(f'NiceGUI count is {counter.value}', on_click=increment_counter).bind_text_from(counter, 'value', backward=lambda c: f'NiceGUI count is {c}')


    ### Example 2: altair chart widget synchronized with nicegui & altair
    # This is the JupyterChart variable params example from the altair documentation:
    # https://altair-viz.github.io/user_guide/interactions/jupyter_chart.html#accessing-variable-params
    import altair as alt
    import numpy as np
    import pandas as pd

    rand = np.random.RandomState(42)

    df = pd.DataFrame({
        'xval': range(100),
        'yval': rand.randn(100).cumsum()
    })

    slider = alt.binding_range(min=0, max=100, step=1)
    cutoff = alt.param(name='cutoff', bind=slider, value=50)
    predicate = alt.datum.xval < 50

    chart = alt.Chart(df).mark_point().encode(
        x='xval',
        y='yval',
        color=alt.when(predicate).then(alt.value('red')).otherwise(alt.value('blue')),
    ).add_params(
        cutoff
    )
    # jchart = alt.JupyterChart(chart)
    jchart = AltairChart(chart)
    ui.anywidget(jchart, throttle=0.2)

    def update_cutoff(change):
        jchart.params.cutoff = change.value
    slider = ui.slider(min=0, max=100, value=cutoff.value, on_change=update_cutoff).bind_value_from(jchart, '_params', backward=lambda p: p['cutoff'])
    ui.label().bind_text_from(slider, 'value', backward=lambda c: f'Cutoff is {c}')



ui.run(show=False)
