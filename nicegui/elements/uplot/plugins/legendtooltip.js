// legendtooltip.js
import { uPlot } from "../src/index.mjs";

/**
 * Legend as a tooltip plugin for uPlot: https://leeoniya.github.io/uPlot/demos/candlestick-ohlc.html
 * @param {object}
 * @returns {object}
 */
export function legendAsTooltipPlugin({ className, style = { backgroundColor:"rgba(255, 249, 196, 0.92)", color: "black" } } = {}) {
    let legendEl;

    function init(u, opts) {
        legendEl = u.root.querySelector(".u-legend");

        legendEl.classList.remove("u-inline");
        className && legendEl.classList.add(className);

        uPlot.assign(legendEl.style, {
            textAlign: "left",
            pointerEvents: "none",
            display: "none",
            position: "absolute",
            left: 0,
            top: 0,
            zIndex: 100,
            boxShadow: "2px 2px 10px rgba(0,0,0,0.5)",
            ...style
        });

        // hide series color markers
        const idents = legendEl.querySelectorAll(".u-marker");

        for (let i = 0; i < idents.length; i++)
            idents[i].style.display = "none";

        const overEl = u.over;
        overEl.style.overflow = "visible";

        // move legend into plot bounds
        overEl.appendChild(legendEl);

        // show/hide tooltip on enter/exit
        overEl.addEventListener("mouseenter", () => {legendEl.style.display = null;});
        overEl.addEventListener("mouseleave", () => {legendEl.style.display = "none";});

        // let tooltip exit plot
    //	overEl.style.overflow = "visible";
    }

    function update(u) {
        const { left, top } = u.cursor;
        // Get plot area dimensions
        const plotRect = u.over.getBoundingClientRect();
        const legendRect = legendEl.getBoundingClientRect();
        // Calculate max allowed left/top so tooltip stays inside plot
        let maxLeft = plotRect.width - legendRect.width;
        let maxTop = plotRect.height - legendRect.height;
        let clampedLeft = Math.max(0, Math.min(left, maxLeft));
        let clampedTop = Math.max(0, Math.min(top, maxTop));
        legendEl.style.transform = `translate(${clampedLeft}px, ${clampedTop}px)`;
    }

    return {
        hooks: {
            init: init,
            setCursor: update,
        }
    };
}
