// wheelzoom.js

/**
 * Wheel zoom plugin for uPlot: https://leeoniya.github.io/uPlot/demos/zoom-wheel.html
 * @param {object} [opts]
 * @returns {object}
 */

export function wheelZoomPlugin(opts = {}) {
    const factor = opts.factor || 0.75;

    // Clamp helper for keeping ranges within bounds
    function clamp(nRange, nMin, nMax, fRange, fMin, fMax) {
        if (nRange > fRange) {
            nMin = fMin;
            nMax = fMax;
        } else if (nMin < fMin) {
            nMin = fMin;
            nMax = fMin + nRange;
        } else if (nMax > fMax) {
            nMax = fMax;
            nMin = fMax - nRange;
        }
        return [nMin, nMax];
    }

    let mousedownHandler = null;
    let wheelHandler = null;

    return {
        hooks: {
            ready: u => {
                const over = u.over;
                const rect = over.getBoundingClientRect();

                // Precompute y-range min/max for fixed axes
                let yRangeMin = +Infinity, yRangeMax = -Infinity;
                let idx = 0;
                for (const i in u.scales) {
                    if (idx === 0) { idx++; continue; }
                    const s = u.scales[i];
                    if (u.series[idx].auto === false && s.min != null && s.max != null) {
                        if (s.min < yRangeMin) yRangeMin = s.min;
                        if (s.max > yRangeMax) yRangeMax = s.max;
                    }
                    idx++;
                }

                // Middle mouse drag pan
                mousedownHandler = function(e) {
                    if (e.button !== 1) return;
                    e.preventDefault();
                    const left0 = e.clientX;
                    const top0 = e.clientY;
                    const xMin0 = u.scales.x.min;
                    const xMax0 = u.scales.x.max;
                    const yMin0 = u.scales.y.min;
                    const yMax0 = u.scales.y.max;
                    const xUnitsPerPx = u.posToVal(1, 'x') - u.posToVal(0, 'x');
                    const yUnitsPerPx = u.posToVal(1, 'y') - u.posToVal(0, 'y');

                    function onmove(ev) {
                        ev.preventDefault();
                        const dx = xUnitsPerPx * (ev.clientX - left0);
                        const dy = yUnitsPerPx * (ev.clientY - top0);
                        u.setScale('x', { min: xMin0 - dx, max: xMax0 - dx });
                        u.setScale('y', { min: yMin0 - dy, max: yMax0 - dy });
                    }
                    function onup() {
                        document.removeEventListener('mousemove', onmove);
                        document.removeEventListener('mouseup', onup);
                    }
                    document.addEventListener('mousemove', onmove);
                    document.addEventListener('mouseup', onup);
                };
                over.addEventListener('mousedown', mousedownHandler);

                // Wheel zoom handler
                wheelHandler = function(e) {
                    e.preventDefault();
                    // X range from data
                    const xData = u.data[0];
                    const xMin = Math.min(...xData);
                    const xMax = Math.max(...xData);

                    // Y range from fixed or data
                    let yMin = yRangeMin, yMax = yRangeMax;
                    if (yMin === +Infinity || yMax === -Infinity) {
                        yMin = +Infinity; yMax = -Infinity;
                        for (let scaleKey in u.scales) {
                            for (let i = 1; i < u.series.length; ++i) {
                                const s = u.series[i];
                                if (s.scale === scaleKey && s.show !== false) {
                                    const arr = u.data[i];
                                    const filtered = arr.filter(v => v != null);
                                    if (!filtered.length) continue;
                                    const sMin = Math.min(...filtered);
                                    const sMax = Math.max(...filtered);
                                    if (sMin < yMin) yMin = sMin;
                                    if (sMax > yMax) yMax = sMax;
                                }
                            }
                        }
                        // Pad y range if needed
                        const pad = 0.1;
                        const delta = yMax - yMin;
                        if (delta === 0) {
                            const padVal = yMin === 0 ? 1 : Math.abs(yMin) * pad;
                            yMin -= padVal;
                            yMax += padVal;
                        } else {
                            yMin -= delta * pad;
                            yMax += delta * pad;
                        }
                    }

                    const xRange = xMax - xMin;
                    const yRange = yMax - yMin;
                    const { left, top } = u.cursor;
                    const leftPct = left / rect.width;
                    const btmPct = 1 - top / rect.height;
                    const xVal = u.posToVal(left, 'x');
                    const yVal = u.posToVal(top, 'y');
                    const oxRange = u.scales.x.max - u.scales.x.min;
                    const oyRange = u.scales.y.max - u.scales.y.min;

                    if (e.shiftKey) {
                        // Only zoom y axis
                        const yCenter = (u.scales.y.min + u.scales.y.max) / 2;
                        const nyRange = e.deltaY < 0 ? oyRange * factor : oyRange / factor;
                        const nyMin = yCenter - nyRange / 2;
                        const nyMax = yCenter + nyRange / 2;
                        u.setScale('y', { min: nyMin, max: nyMax });
                    } else {
                        // Zoom both axes
                        let nxRange = e.deltaY < 0 ? oxRange * factor : oxRange / factor;
                        let nxMin = xVal - leftPct * nxRange;
                        let nxMax = nxMin + nxRange;
                        [nxMin, nxMax] = clamp(nxRange, nxMin, nxMax, xRange, xMin, xMax);

                        let nyRange = e.deltaY < 0 ? oyRange * factor : oyRange / factor;
                        let nyMin = yVal - btmPct * nyRange;
                        let nyMax = nyMin + nyRange;
                        [nyMin, nyMax] = clamp(nyRange, nyMin, nyMax, yRange, yMin, yMax);

                        u.batch(() => {
                            u.setScale('x', { min: nxMin, max: nxMax });
                            u.setScale('y', { min: nyMin, max: nyMax });
                        });
                    }
                };
                over.addEventListener('wheel', wheelHandler);
            },
            destroy: u => {
                const over = u.over;
                if (mousedownHandler) over.removeEventListener('mousedown', mousedownHandler);
                if (wheelHandler) over.removeEventListener('wheel', wheelHandler);
            }
        }
    };
}
