// Core functions from anywidget's Jupyter widget implementation
// In the future, should attempt to vendor this directly.
// https://github.com/manzt/anywidget/blob/main/packages/anywidget/src/widget.js

/** @import { Initialize, Render, AnyModel } from "@anywidget/types" */

/**
 * @template T
 * @typedef {T | PromiseLike<T>} Awaitable
 */

/**
 * @typedef AnyWidget
 * @prop initialize {Initialize}
 * @prop render {Render}
 */

/**
 *  @typedef AnyWidgetModule
 *  @prop render {Render=}
 *  @prop default {AnyWidget | (() => AnyWidget | Promise<AnyWidget>)=}
 */

/**
 * @param {unknown} condition
 * @param {string} message
 * @returns {asserts condition}
 */
function assert(condition, message) {
  if (!condition) throw new Error(message);
}

/**
 * @param {string} str
 * @returns {str is "https://${string}" | "http://${string}"}
 */
function is_href(str) {
  return str.startsWith("http://") || str.startsWith("https://");
}

/**
 * @param {string} href
 * @param {string} anywidget_id
 * @returns {Promise<void>}
 */
async function load_css_href(href, anywidget_id) {
  /** @type {HTMLLinkElement | null} */
  let prev = document.querySelector(`link[id='${anywidget_id}']`);

  // Adapted from https://github.com/vitejs/vite/blob/d59e1acc2efc0307488364e9f2fad528ec57f204/packages/vite/src/client/client.ts#L185-L201
  // Swaps out old styles with new, but avoids flash of unstyled content.
  // No need to await the load since we already have styles applied.
  if (prev) {
    let newLink = /** @type {HTMLLinkElement} */ (prev.cloneNode());
    newLink.href = href;
    newLink.addEventListener("load", () => prev?.remove());
    newLink.addEventListener("error", () => prev?.remove());
    prev.after(newLink);
    return;
  }

  return new Promise((resolve) => {
    let link = Object.assign(document.createElement("link"), {
      rel: "stylesheet",
      href,
      onload: resolve,
    });
    document.head.appendChild(link);
  });
}

/**
 * @param {string} css_text
 * @param {string} anywidget_id
 * @returns {void}
 */
function load_css_text(css_text, anywidget_id) {
  /** @type {HTMLStyleElement | null} */
  let prev = document.querySelector(`style[id='${anywidget_id}']`);
  if (prev) {
    // replace instead of creating a new DOM node
    prev.textContent = css_text;
    return;
  }
  let style = Object.assign(document.createElement("style"), {
    id: anywidget_id,
    type: "text/css",
  });
  style.appendChild(document.createTextNode(css_text));
  document.head.appendChild(style);
}

/**
 * @param {string | undefined} css
 * @param {string} anywidget_id
 * @returns {Promise<void>}
 */
async function load_css(css, anywidget_id) {
  if (!css || !anywidget_id) return;
  if (is_href(css)) return load_css_href(css, anywidget_id);
  return load_css_text(css, anywidget_id);
}

/**
 * @param {string} esm
 * @returns {Promise<AnyWidgetModule>}
 */
async function load_esm(esm) {
  if (is_href(esm)) {
    return await import(/* webpackIgnore: true */ /* @vite-ignore */ esm);
  }
  let url = URL.createObjectURL(new Blob([esm], { type: "text/javascript" }));
  let mod = await import(/* webpackIgnore: true */ /* @vite-ignore */ url);
  URL.revokeObjectURL(url);
  return mod;
}

/** @param {string} anywidget_id */
function warn_render_deprecation(anywidget_id) {
  console.warn(`\
[anywidget] Deprecation Warning for ${anywidget_id}: Direct export of a 'render' will likely be deprecated in the future. To migrate ...

Remove the 'export' keyword from 'render'
-----------------------------------------

export function render({ model, el }) { ... }
^^^^^^

Create a default export that returns an object with 'render'
------------------------------------------------------------

function render({ model, el }) { ... }
         ^^^^^^
export default { render }
                 ^^^^^^

Pin to anywidget>=0.9.0 in your pyproject.toml
----------------------------------------------

dependencies = ["anywidget>=0.9.0"]

To learn more, please see: https://github.com/manzt/anywidget/pull/395.
`);
}

/**
 * @param {string} esm
 * @param {string} anywidget_id
 * @returns {Promise<AnyWidget>}
 */
async function load_widget(esm, anywidget_id) {
  let mod = await load_esm(esm);
  if (mod.render) {
    warn_render_deprecation(anywidget_id);
    return {
      async initialize() { },
      render: mod.render,
    };
  }
  assert(
    mod.default,
    `[anywidget] module must export a default function or object.`,
  );
  let widget =
    typeof mod.default === "function" ? await mod.default() : mod.default;
  return widget;
}

export { load_widget, load_css };
