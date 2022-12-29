/**
 * @license Highcharts JS v10.3.2 (2022-11-28)
 *
 * Old IE (v6, v7, v8) module for Highcharts v6+.
 *
 * (c) 2010-2021 Highsoft AS
 * Author: Torstein Honsi
 *
 * License: www.highcharts.com/license
 */
(function (factory) {
    if (typeof module === 'object' && module.exports) {
        factory['default'] = factory;
        module.exports = factory;
    } else if (typeof define === 'function' && define.amd) {
        define('highcharts/modules/oldie', ['highcharts'], function (Highcharts) {
            factory(Highcharts);
            factory.Highcharts = Highcharts;
            return factory;
        });
    } else {
        factory(typeof Highcharts !== 'undefined' ? Highcharts : undefined);
    }
}(function (Highcharts) {
    'use strict';
    var _modules = Highcharts ? Highcharts._modules : {};
    function _registerModule(obj, path, args, fn) {
        if (!obj.hasOwnProperty(path)) {
            obj[path] = fn.apply(null, args);

            if (typeof CustomEvent === 'function') {
                window.dispatchEvent(
                    new CustomEvent(
                        'HighchartsModuleLoaded',
                        { detail: { path: path, module: obj[path] }
                    })
                );
            }
        }
    }
    _registerModule(_modules, 'Extensions/Oldie/VMLAxis3D.js', [_modules['Core/Utilities.js']], function (U) {
        /* *
         *
         *  (c) 2010-2021 Torstein Honsi
         *
         *  Extension to the VML Renderer
         *
         *  License: www.highcharts.com/license
         *
         *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
         *
         * */
        var addEvent = U.addEvent;
        /* *
         *
         *  Class
         *
         * */
        /* eslint-disable valid-jsdoc */
        var VMLAxis3DAdditions = /** @class */ (function () {
                /* *
                 *
                 *  Constructors
                 *
                 * */
                function VMLAxis3DAdditions(axis) {
                    this.axis = axis;
            }
            return VMLAxis3DAdditions;
        }());
        var VMLAxis3D = /** @class */ (function () {
                function VMLAxis3D() {
                }
                /* *
                 *
                 *  Static Properties
                 *
                 * */
                VMLAxis3D.compose = function (AxisClass) {
                    AxisClass.keepProps.push('vml');
                addEvent(AxisClass, 'destroy', VMLAxis3D.onDestroy);
                addEvent(AxisClass, 'init', VMLAxis3D.onInit);
                addEvent(AxisClass, 'render', VMLAxis3D.onRender);
            };
            /**
             * @private
             */
            VMLAxis3D.onDestroy = function () {
                var axis = this,
                    vml = axis.vml;
                if (vml) {
                    var el_1;
                    [
                        'backFrame',
                        'bottomFrame',
                        'sideFrame'
                    ].forEach(function (prop) {
                        el_1 = vml[prop];
                        if (el_1) {
                            vml[prop] = el_1.destroy();
                        }
                    }, this);
                }
            };
            /**
             * @private
             */
            VMLAxis3D.onInit = function () {
                var axis = this;
                if (!axis.vml) {
                    axis.vml = new VMLAxis3DAdditions(axis);
                }
            };
            /**
             * @private
             */
            VMLAxis3D.onRender = function () {
                var axis = this;
                var vml = axis.vml;
                // VML doesn't support a negative z-index
                if (vml.sideFrame) {
                    vml.sideFrame.css({ zIndex: 0 });
                    vml.sideFrame.front.attr({
                        fill: vml.sideFrame.color
                    });
                }
                if (vml.bottomFrame) {
                    vml.bottomFrame.css({ zIndex: 1 });
                    vml.bottomFrame.front.attr({
                        fill: vml.bottomFrame.color
                    });
                }
                if (vml.backFrame) {
                    vml.backFrame.css({ zIndex: 0 });
                    vml.backFrame.front.attr({
                        fill: vml.backFrame.color
                    });
                }
            };
            return VMLAxis3D;
        }());

        return VMLAxis3D;
    });
    _registerModule(_modules, 'Extensions/Oldie/VMLRenderer3D.js', [_modules['Core/Axis/Axis.js'], _modules['Core/Defaults.js'], _modules['Extensions/Oldie/VMLAxis3D.js']], function (Axis, D, VMLAxis3D) {
        /* *
         *
         *  (c) 2010-2021 Torstein Honsi
         *
         *  Extension to the VML Renderer
         *
         *  License: www.highcharts.com/license
         *
         *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
         *
         * */
        var setOptions = D.setOptions;
        var VMLRenderer3D = /** @class */ (function () {
                function VMLRenderer3D() {
                }
                /* *
                 *
                 *  Static Properties
                 *
                 * */
                VMLRenderer3D.compose = function (vmlClass, svgClass) {
                    var svgProto = svgClass.prototype;
                var vmlProto = vmlClass.prototype;
                setOptions({ animate: false });
                vmlProto.face3d = svgProto.face3d;
                vmlProto.polyhedron = svgProto.polyhedron;
                vmlProto.elements3d = svgProto.elements3d;
                vmlProto.element3d = svgProto.element3d;
                vmlProto.cuboid = svgProto.cuboid;
                vmlProto.cuboidPath = svgProto.cuboidPath;
                vmlProto.toLinePath = svgProto.toLinePath;
                vmlProto.toLineSegments = svgProto.toLineSegments;
                vmlProto.arc3d = function (shapeArgs) {
                    var result = svgProto.arc3d.call(this,
                        shapeArgs);
                    result.css({ zIndex: result.zIndex });
                    return result;
                };
                vmlProto.arc3dPath = svgProto.arc3dPath;
                VMLAxis3D.compose(Axis);
            };
            return VMLRenderer3D;
        }());

        return VMLRenderer3D;
    });
    _registerModule(_modules, 'Extensions/Oldie/Oldie.js', [_modules['Core/Chart/Chart.js'], _modules['Core/Color/Color.js'], _modules['Core/Defaults.js'], _modules['Core/Globals.js'], _modules['Core/Pointer.js'], _modules['Core/Renderer/RendererRegistry.js'], _modules['Core/Renderer/SVG/SVGElement.js'], _modules['Core/Renderer/SVG/SVGRenderer.js'], _modules['Core/Utilities.js'], _modules['Extensions/Oldie/VMLRenderer3D.js']], function (Chart, Color, D, H, Pointer, RendererRegistry, SVGElement, SVGRenderer, U, VMLRenderer3D) {
        /* *
         *
         *  (c) 2010-2021 Torstein Honsi
         *
         *  License: www.highcharts.com/license
         *
         *  Support for old IE browsers (6, 7 and 8) in Highcharts v6+.
         *
         *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
         *
         * */
        var color = Color.parse;
        var getOptions = D.getOptions;
        var deg2rad = H.deg2rad,
            doc = H.doc,
            noop = H.noop,
            svg = H.svg,
            win = H.win;
        var addEvent = U.addEvent,
            createElement = U.createElement,
            css = U.css,
            defined = U.defined,
            discardElement = U.discardElement,
            erase = U.erase,
            extend = U.extend,
            extendClass = U.extendClass,
            isArray = U.isArray,
            isNumber = U.isNumber,
            isObject = U.isObject,
            pick = U.pick,
            pInt = U.pInt,
            uniqueKey = U.uniqueKey;
        var VMLRenderer,
            VMLElement;
        /**
         * Path to the pattern image required by VML browsers in order to
         * draw radial gradients.
         *
         * @type      {string}
         * @default   http://code.highcharts.com/{version}/gfx/vml-radial-gradient.png
         * @since     2.3.0
         * @requires  modules/oldie
         * @apioption global.VMLRadialGradientURL
         */
        getOptions().global.VMLRadialGradientURL =
            'http://code.highcharts.com/10.3.2/gfx/vml-radial-gradient.png';
        // Utilites
        if (doc && !doc.defaultView) {
            H.getStyle = U.getStyle = function getStyle(el, prop) {
                var val,
                    alias = {
                        width: 'clientWidth',
                        height: 'clientHeight'
                    }[prop];
                if (el.style[prop]) {
                    return pInt(el.style[prop]);
                }
                if (prop === 'opacity') {
                    prop = 'filter';
                }
                // Getting the rendered width and height
                if (alias) {
                    el.style.zoom = 1;
                    return Math.max(el[alias] - 2 * getStyle(el, 'padding'), 0);
                }
                val = el.currentStyle[prop.replace(/\-(\w)/g, function (a, b) {
                    return b.toUpperCase();
                })];
                if (prop === 'filter') {
                    val = val.replace(/alpha\(opacity=([0-9]+)\)/, function (a, b) {
                        return (b / 100);
                    });
                }
                return val === '' ? 1 : pInt(val);
            };
        }
        /* eslint-disable no-invalid-this, valid-jsdoc */
        if (!svg) {
            // Prevent wrapping from creating false offsetWidths in export in legacy IE.
            // This applies only to charts for export, where IE runs the SVGRenderer
            // instead of the VMLRenderer
            // (#1079, #1063)
            addEvent(SVGElement, 'afterInit', function () {
                if (this.element.nodeName === 'text') {
                    this.css({
                        position: 'absolute'
                    });
                }
            });
            /**
             * Old IE override for pointer normalize, adds chartX and chartY to event
             * arguments.
             *
             * @ignore
             * @function Highcharts.Pointer#normalize
             */
            Pointer.prototype.normalize = function (e, chartPosition) {
                e = e || win.event;
                if (!e.target) {
                    e.target = e.srcElement;
                }
                // Get mouse position
                if (!chartPosition) {
                    this.chartPosition = chartPosition = this.getChartPosition();
                }
                return extend(e, {
                    // #2005, #2129: the second case is for IE10 quirks mode within
                    // framesets
                    chartX: Math.round(Math.max(e.x, e.clientX - chartPosition.left)),
                    chartY: Math.round(e.y)
                });
            };
            /**
             * Further sanitize the mock-SVG that is generated when exporting charts in
             * oldIE.
             *
             * @private
             * @function Highcharts.Chart#ieSanitizeSVG
             */
            Chart.prototype.ieSanitizeSVG = function (svg) {
                svg = svg
                    .replace(/<IMG /g, '<image ')
                    .replace(/<(\/?)TITLE>/g, '<$1title>')
                    .replace(/height=([^" ]+)/g, 'height="$1"')
                    .replace(/width=([^" ]+)/g, 'width="$1"')
                    .replace(/hc-svg-href="([^"]+)">/g, 'xlink:href="$1"/>')
                    .replace(/ id=([^" >]+)/g, ' id="$1"') // #4003
                    .replace(/class=([^" >]+)/g, 'class="$1"')
                    .replace(/ transform /g, ' ')
                    .replace(/:(path|rect)/g, '$1')
                    .replace(/style="([^"]+)"/g, function (s) {
                    return s.toLowerCase();
                });
                return svg;
            };
            /**
             * VML namespaces can't be added until after complete. Listening
             * for Perini's doScroll hack is not enough.
             *
             * @private
             * @function Highcharts.Chart#isReadyToRender
             */
            Chart.prototype.isReadyToRender = function () {
                var chart = this;
                // Note: win == win.top is required
                if (!svg &&
                    (win == win.top && // eslint-disable-line eqeqeq
                        doc.readyState !== 'complete')) {
                    doc.attachEvent('onreadystatechange', function () {
                        doc.detachEvent('onreadystatechange', chart.firstRender);
                        if (doc.readyState === 'complete') {
                            chart.firstRender();
                        }
                    });
                    return false;
                }
                return true;
            };
            // IE compatibility hack for generating SVG content that it doesn't really
            // understand. Used by the exporting module.
            if (!doc.createElementNS) {
                doc.createElementNS = function (ns, tagName) {
                    return doc.createElement(tagName);
                };
            }
            /**
             * Old IE polyfill for addEventListener, called from inside the addEvent
             * function.
             *
             * @private
             * @function Highcharts.addEventListenerPolyfill<T>
             */
            H.addEventListenerPolyfill = function (type, fn) {
                var el = this;
                /**
                 * @private
                 */
                function wrappedFn(e) {
                    e.target = e.srcElement || win; // #2820
                    fn.call(el, e);
                }
                if (el.attachEvent) {
                    if (!el.hcEventsIE) {
                        el.hcEventsIE = {};
                    }
                    // unique function string (#6746)
                    if (!fn.hcKey) {
                        fn.hcKey = uniqueKey();
                    }
                    // Link wrapped fn with original fn, so we can get this in
                    // removeEvent
                    el.hcEventsIE[fn.hcKey] = wrappedFn;
                    el.attachEvent('on' + type, wrappedFn);
                }
            };
            /**
             * @private
             * @function Highcharts.removeEventListenerPolyfill<T>
             */
            H.removeEventListenerPolyfill = function (type, fn) {
                if (this.detachEvent) {
                    fn = this.hcEventsIE[fn.hcKey];
                    this.detachEvent('on' + type, fn);
                }
            };
            /**
             * The VML element wrapper.
             *
             * @private
             * @class
             * @name Highcharts.VMLElement
             *
             * @augments Highcharts.SVGElement
             */
            VMLElement = {
                docMode8: doc && doc.documentMode === 8,
                /**
                 * Initialize a new VML element wrapper. It builds the markup as a
                 * string to minimize DOM traffic.
                 *
                 * @function Highcharts.VMLElement#init
                 */
                init: function (renderer, nodeName) {
                    var wrapper = this, markup = ['<', nodeName, ' filled="f" stroked="f"'], style = ['position: ', 'absolute', ';'], isDiv = nodeName === 'div';
                    // divs and shapes need size
                    if (nodeName === 'shape' || isDiv) {
                        style.push('left:0;top:0;width:1px;height:1px;');
                    }
                    style.push('visibility: ', isDiv ? 'hidden' : 'visible');
                    markup.push(' style="', style.join(''), '"/>');
                    // create element with default attributes and style
                    if (nodeName) {
                        markup = isDiv || nodeName === 'span' || nodeName === 'img' ?
                            markup.join('') :
                            renderer.prepVML(markup);
                        wrapper.element = createElement(markup);
                    }
                    wrapper.renderer = renderer;
                },
                /**
                 * Add the node to the given parent
                 *
                 * @function Highcharts.VMLElement
                 */
                add: function (parent) {
                    var wrapper = this,
                        renderer = wrapper.renderer,
                        element = wrapper.element,
                        box = renderer.box,
                        inverted = parent && parent.inverted, 
                        // get the parent node
                        parentNode = parent ?
                            parent.element || parent :
                            box;
                    if (parent) {
                        this.parentGroup = parent;
                    }
                    // if the parent group is inverted, apply inversion on all children
                    if (inverted) { // only on groups
                        renderer.invertChild(element, parentNode);
                    }
                    // append it
                    parentNode.appendChild(element);
                    // align text after adding to be able to read offset
                    wrapper.added = true;
                    if (wrapper.alignOnAdd && !wrapper.deferUpdateTransform) {
                        wrapper.updateTransform();
                    }
                    // fire an event for internal hooks
                    if (wrapper.onAdd) {
                        wrapper.onAdd();
                    }
                    // IE8 Standards can't set the class name before the element is
                    // appended
                    if (this.className) {
                        this.attr('class', this.className);
                    }
                    return wrapper;
                },
                /**
                 * VML always uses htmlUpdateTransform
                 *
                 * @function Highcharts.VMLElement#updateTransform
                 */
                updateTransform: SVGElement.prototype
                    .htmlUpdateTransform,
                /**
                 * Set the rotation of a span with oldIE's filter
                 *
                 * @function Highcharts.VMLElement#setSpanRotation
                     */
                setSpanRotation: function () {
                    // Adjust for alignment and rotation. Rotation of useHTML content is
                    // not yet implemented but it can probably be implemented for
                    // Firefox 3.5+ on user request. FF3.5+ has support for CSS3
                    // transform. The getBBox method also needs to be updated to
                    // compensate for the rotation, like it currently does for SVG.
                    // Test case: https://jsfiddle.net/highcharts/Ybt44/
                    var rotation = this.rotation,
                        costheta = Math.cos(rotation * deg2rad),
                        sintheta = Math.sin(rotation * deg2rad);
                    css(this.element, {
                        filter: rotation ? [
                            'progid:DXImageTransform.Microsoft.Matrix(M11=', costheta,
                            ', M12=', -sintheta, ', M21=', sintheta, ', M22=', costheta,
                            ', sizingMethod=\'auto expand\')'
                        ].join('') : 'none'
                    });
                },
                /**
                 * Get the positioning correction for the span after rotating.
                 *
                 * @function Highcharts.VMLElement#getSpanCorrection
                 */
                getSpanCorrection: function (width, baseline, alignCorrection, rotation, align) {
                    var costheta = rotation ? Math.cos(rotation * deg2rad) : 1,
                        sintheta = rotation ? Math.sin(rotation * deg2rad) : 0,
                        height = pick(this.elemHeight,
                        this.element.offsetHeight),
                        quad,
                        nonLeft = align && align !== 'left';
                    // correct x and y
                    this.xCorr = (costheta < 0 && -width);
                    this.yCorr = (sintheta < 0 && -height);
                    // correct for baseline and corners spilling out after rotation
                    quad = costheta * sintheta < 0;
                    this.xCorr += (sintheta *
                        baseline *
                        (quad ? 1 - alignCorrection : alignCorrection));
                    this.yCorr -= (costheta *
                        baseline *
                        (rotation ? (quad ? alignCorrection : 1 - alignCorrection) : 1));
                    // correct for the length/height of the text
                    if (nonLeft) {
                        this.xCorr -=
                            width * alignCorrection * (costheta < 0 ? -1 : 1);
                        if (rotation) {
                            this.yCorr -= (height *
                                alignCorrection *
                                (sintheta < 0 ? -1 : 1));
                        }
                        css(this.element, {
                            textAlign: align
                        });
                    }
                },
                /**
                 * Converts a subset of an SVG path definition to its VML counterpart.
                 * Takes an array as the parameter and returns a string.
                 *
                 * @function Highcharts.VMLElement#pathToVML
                 */
                pathToVML: function (value) {
                    // convert paths
                    var i = value.length,
                        path = [];
                    while (i--) {
                        // Multiply by 10 to allow subpixel precision.
                        // Substracting half a pixel seems to make the coordinates
                        // align with SVG, but this hasn't been tested thoroughly
                        if (isNumber(value[i])) {
                            path[i] = Math.round(value[i] * 10) - 5;
                        }
                        else if (value[i] === 'Z') { // close the path
                            path[i] = 'x';
                        }
                        else {
                            path[i] = value[i];
                            // When the start X and end X coordinates of an arc are too
                            // close, they are rounded to the same value above. In this
                            // case, substract or add 1 from the end X and Y positions.
                            // #186, #760, #1371, #1410.
                            if (value.isArc &&
                                (value[i] === 'wa' || value[i] === 'at')) {
                                // Start and end X
                                if (path[i + 5] === path[i + 7]) {
                                    path[i + 7] +=
                                        value[i + 7] > value[i + 5] ? 1 : -1;
                                }
                                // Start and end Y
                                if (path[i + 6] === path[i + 8]) {
                                    path[i + 8] +=
                                        value[i + 8] > value[i + 6] ? 1 : -1;
                                }
                            }
                        }
                    }
                    return path.join(' ') || 'x';
                },
                /**
                 * Set the element's clipping to a predefined rectangle
                 *
                 * @function Highcharts.VMLElement#clip
                 */
                clip: function (clipRect) {
                    var wrapper = this,
                        clipMembers,
                        cssRet;
                    if (clipRect) {
                        clipMembers = clipRect.members;
                        // Ensure unique list of elements (#1258)
                        erase(clipMembers, wrapper);
                        clipMembers.push(wrapper);
                        wrapper.destroyClip = function () {
                            erase(clipMembers, wrapper);
                        };
                        cssRet = clipRect.getCSS(wrapper);
                    }
                    else {
                        if (wrapper.destroyClip) {
                            wrapper.destroyClip();
                        }
                        cssRet = {
                            clip: wrapper.docMode8 ? 'inherit' : 'rect(auto)'
                        }; // #1214
                    }
                    return wrapper.css(cssRet);
                },
                /**
                 * Set styles for the element
                 *
                 * @function Highcharts.VMLElement#css
                 */
                css: SVGElement.prototype.htmlCss,
                /**
                 * Removes a child either by removeChild or move to garbageBin.
                 * Issue 490; in VML removeChild results in Orphaned nodes according to
                 * sIEve, discardElement does not.
                 *
                 * @function Highcharts.VMLElement#safeRemoveChild
                 */
                safeRemoveChild: function (element) {
                    // discardElement will detach the node from its parent before
                    // attaching it to the garbage bin. Therefore it is important that
                    // the node is attached and have parent.
                    if (element.parentNode) {
                        discardElement(element);
                    }
                },
                /**
                 * Extend element.destroy by removing it from the clip members array
                 *
                 * @function Highcharts.VMLElement#destroy
                 */
                destroy: function () {
                    if (this.destroyClip) {
                        this.destroyClip();
                    }
                    return SVGElement.prototype.destroy.apply(this);
                },
                /**
                 * Add an event listener. VML override for normalizing event parameters.
                 *
                 * @function Highcharts.VMLElement#on
                 */
                on: function (eventType, handler) {
                    // simplest possible event model for internal use
                    this.element['on' + eventType] = function () {
                        var e = win.event;
                        e.target = e.srcElement;
                        handler(e);
                    };
                    return this;
                },
                /**
                 * In stacked columns, cut off the shadows so that they don't overlap
                 *
                 * @function Highcharts.VMLElement#cutOffPath
                 */
                cutOffPath: function (path, length) {
                    var len;
                    // The extra comma tricks the trailing comma remover in
                    // "gulp scripts" task
                    path = path.split(/[ ,]/);
                    len = path.length;
                    if (len === 9 || len === 11) {
                        path[len - 4] = path[len - 2] =
                            pInt(path[len - 2]) - 10 * length;
                    }
                    return path.join(' ');
                },
                /**
                 * Apply a drop shadow by copying elements and giving them different
                 * strokes.
                 *
                 * @function Highcharts.VMLElement#shadow
                 */
                shadow: function (shadowOptions, group, cutOff) {
                    var shadows = [],
                        i,
                        element = this.element,
                        renderer = this.renderer,
                        shadow,
                        elemStyle = element.style,
                        markup,
                        path = element.path,
                        strokeWidth,
                        modifiedPath,
                        shadowWidth,
                        shadowElementOpacity;
                    // some times empty paths are not strings
                    if (path && typeof path.value !== 'string') {
                        path = 'x';
                    }
                    modifiedPath = path;
                    if (shadowOptions) {
                        shadowWidth = pick(shadowOptions.width, 3);
                        shadowElementOpacity =
                            (shadowOptions.opacity || 0.15) / shadowWidth;
                        for (i = 1; i <= 3; i++) {
                            strokeWidth = (shadowWidth * 2) + 1 - (2 * i);
                            // Cut off shadows for stacked column items
                            if (cutOff) {
                                modifiedPath = this.cutOffPath(path.value, strokeWidth + 0.5);
                            }
                            markup = [
                                '<shape isShadow="true" strokeweight="', strokeWidth,
                                '" filled="false" path="', modifiedPath,
                                '" coordsize="10 10" style="', element.style.cssText,
                                '" />'
                            ];
                            shadow = createElement(renderer.prepVML(markup), null, {
                                left: (pInt(elemStyle.left) +
                                    pick(shadowOptions.offsetX, 1)) + 'px',
                                top: (pInt(elemStyle.top) +
                                    pick(shadowOptions.offsetY, 1)) + 'px'
                            });
                            if (cutOff) {
                                shadow.cutOff = strokeWidth + 1;
                            }
                            // apply the opacity
                            markup = [
                                '<stroke color="',
                                shadowOptions.color || "#000000" /* Palette.neutralColor100 */,
                                '" opacity="', shadowElementOpacity * i, '"/>'
                            ];
                            createElement(renderer.prepVML(markup), null, null, shadow);
                            // insert it
                            if (group) {
                                group.element.appendChild(shadow);
                            }
                            else {
                                element.parentNode
                                    .insertBefore(shadow, element);
                            }
                            // record it
                            shadows.push(shadow);
                        }
                        this.shadows = shadows;
                    }
                    return this;
                },
                updateShadows: noop,
                setAttr: function (key, value) {
                    if (this.docMode8) { // IE8 setAttribute bug
                        this.element[key] = value;
                    }
                    else {
                        this.element.setAttribute(key, value);
                    }
                },
                getAttr: function (key) {
                    if (this.docMode8) { // IE8 setAttribute bug
                        return this.element[key];
                    }
                    return this.element.getAttribute(key);
                },
                classSetter: function (value) {
                    // IE8 Standards mode has problems retrieving the className unless
                    // set like this. IE8 Standards can't set the class name before the
                    // element is appended.
                    (this.added ? this.element : this).className = value;
                },
                dashstyleSetter: function (value, key, element) {
                    var strokeElem = element.getElementsByTagName('stroke')[0] ||
                            createElement(this.renderer.prepVML(['<stroke/>']),
                        null,
                        null,
                        element);
                    strokeElem[key] = value || 'solid';
                    // Because changing stroke-width will change the dash length and
                    // cause an epileptic effect
                    this[key] = value;
                },
                dSetter: function (value, key, element) {
                    var i,
                        shadows = this.shadows;
                    value = value || [];
                    // Used in getter for animation
                    this.d = value.join && value.join(' ');
                    element.path = value = this.pathToVML(value);
                    // update shadows
                    if (shadows) {
                        i = shadows.length;
                        while (i--) {
                            shadows[i].path = shadows[i].cutOff ?
                                this.cutOffPath(value, shadows[i].cutOff) :
                                value;
                        }
                    }
                    this.setAttr(key, value);
                },
                fillSetter: function (value, key, element) {
                    var nodeName = element.nodeName;
                    if (nodeName === 'SPAN') { // text color
                        element.style.color = value;
                    }
                    else if (nodeName !== 'IMG') { // #1336
                        element.filled = value !== 'none';
                        this.setAttr('fillcolor', this.renderer.color(value, element, key, this));
                    }
                },
                'fill-opacitySetter': function (value, key, element) {
                    createElement(this.renderer.prepVML(['<', key.split('-')[0], ' opacity="', value, '"/>']), null, null, element);
                },
                // Don't bother - animation is too slow and filters introduce artifacts
                opacitySetter: noop,
                rotationSetter: function (value, key, element) {
                    var style = element.style;
                    // style is for #1873:
                    this[key] = style[key] = value;
                    // Correction for the 1x1 size of the shape container. Used in gauge
                    // needles.
                    style.left =
                        -Math.round(Math.sin(value * deg2rad) + 1) + 'px';
                    style.top =
                        Math.round(Math.cos(value * deg2rad)) + 'px';
                },
                strokeSetter: function (value, key, element) {
                    this.setAttr('strokecolor', this.renderer.color(value, element, key, this));
                },
                'stroke-widthSetter': function (value, key, element) {
                    element.stroked = !!value; // VML "stroked" attribute
                    this[key] = value; // used in getter, issue #113
                    if (isNumber(value)) {
                        value += 'px';
                    }
                    this.setAttr('strokeweight', value);
                },
                titleSetter: function (value, key) {
                    this.setAttr(key, value);
                },
                visibilitySetter: function (value, key, element) {
                    // Handle inherited visibility
                    if (value === 'inherit') {
                        value = 'visible';
                    }
                    // Let the shadow follow the main element
                    if (this.shadows) {
                        this.shadows.forEach(function (shadow) {
                            shadow.style[key] = value;
                        });
                    }
                    // Instead of toggling the visibility CSS property, move the div out
                    // of the viewport. This works around #61 and #586
                    if (element.nodeName === 'DIV') {
                        value = value === 'hidden' ? '-999em' : 0;
                        // In order to redraw, IE7 needs the div to be visible when
                        // tucked away outside the viewport. So the visibility is
                        // actually opposite of the expected value. This applies to the
                        // tooltip only.
                        if (!this.docMode8) {
                            element.style[key] = value ? 'visible' : 'hidden';
                        }
                        key = 'top';
                    }
                    element.style[key] = value;
                },
                xSetter: function (value, key, element) {
                    this[key] = value; // used in getter
                    if (key === 'x') {
                        key = 'left';
                    }
                    else if (key === 'y') {
                        key = 'top';
                    }
                    // clipping rectangle special
                    if (this.updateClipping) {
                        // the key is now 'left' or 'top' for 'x' and 'y'
                        this[key] = value;
                        this.updateClipping();
                    }
                    else {
                        // normal
                        element.style[key] = value;
                    }
                },
                zIndexSetter: function (value, key, element) {
                    element.style[key] = value;
                },
                fillGetter: function () {
                    return this.getAttr('fillcolor') || '';
                },
                strokeGetter: function () {
                    return this.getAttr('strokecolor') || '';
                },
                // #7850
                classGetter: function () {
                    return this.getAttr('className') || '';
                }
            };
            VMLElement['stroke-opacitySetter'] =
                VMLElement['fill-opacitySetter'];
            H.VMLElement = VMLElement = extendClass(SVGElement, VMLElement);
            // Some shared setters
            VMLElement.prototype.ySetter =
                VMLElement.prototype.widthSetter =
                    VMLElement.prototype.heightSetter =
                        VMLElement.prototype.xSetter;
            /**
             * The VML renderer
             *
             * @private
             * @class
             * @name Highcharts.VMLRenderer
             *
             * @augments Highcharts.SVGRenderer
             */
            var VMLRendererExtension = {
                    Element: VMLElement,
                    isIE8: win.navigator.userAgent.indexOf('MSIE 8.0') > -1,
                    /**
                     * Initialize the VMLRenderer.
                     *
                     * @function Highcharts.VMLRenderer#init
                     * @param {Highcharts.HTMLDOMElement} container
                     * @param {number} width
                     * @param {number} height
                         */
                    init: function (container,
                width,
                height) {
                        var renderer = this,
                boxWrapper,
                box,
                css;
                    // Extended SVGRenderer member
                    this.crispPolyLine = SVGRenderer.prototype.crispPolyLine;
                    renderer.alignedObjects = [];
                    boxWrapper = renderer.createElement('div')
                        .css({ position: 'relative' });
                    box = boxWrapper.element;
                    container.appendChild(boxWrapper.element);
                    // generate the containing box
                    renderer.isVML = true;
                    renderer.box = box;
                    renderer.boxWrapper = boxWrapper;
                    renderer.gradients = {};
                    renderer.cache = {}; // Cache for numerical bounding boxes
                    renderer.cacheKeys = [];
                    renderer.imgCount = 0;
                    renderer.setSize(width, height, false);
                    // The only way to make IE6 and IE7 print is to use a global
                    // namespace. However, with IE8 the only way to make the dynamic
                    // shapes visible in screen and print mode seems to be to add the
                    // xmlns attribute and the behaviour style inline.
                    if (!doc.namespaces.hcv) {
                        doc.namespaces.add('hcv', 'urn:schemas-microsoft-com:vml');
                        // Setup default CSS (#2153, #2368, #2384)
                        css = 'hcv\\:fill, hcv\\:path, hcv\\:shape, hcv\\:stroke' +
                            '{ behavior:url(#default#VML); display: inline-block; } ';
                        try {
                            doc.createStyleSheet().cssText = css;
                        }
                        catch (e) {
                            doc.styleSheets[0].cssText += css;
                        }
                    }
                },
                /**
                 * Detect whether the renderer is hidden. This happens when one of the
                 * parent elements has display: none
                 *
                 * @function Highcharts.VMLRenderer#isHidden
                 */
                isHidden: function () {
                    return !this.box.offsetWidth;
                },
                /**
                 * Define a clipping rectangle. In VML it is accomplished by storing the
                 * values for setting the CSS style to all associated members.
                 *
                 * @function Highcharts.VMLRenderer#clipRect
                 */
                clipRect: function (x, y, width, height) {
                    // create a dummy element
                    var clipRect = this.createElement(),
                        isObj = isObject(x);
                    // mimic a rectangle with its style object for automatic updating in
                    // attr
                    return extend(clipRect, {
                        members: [],
                        count: 0,
                        left: (isObj ? x.x : x) + 1,
                        top: (isObj ? x.y : y) + 1,
                        width: (isObj ? x.width : width) - 1,
                        height: (isObj ? x.height : height) - 1,
                        getCSS: function (wrapper) {
                            var element = wrapper.element, nodeName = element.nodeName, isShape = nodeName === 'shape', inverted = wrapper.inverted, rect = this, top = rect.top - (isShape ? element.offsetTop : 0), left = rect.left, right = left + rect.width, bottom = top + rect.height, ret = {
                                    clip: 'rect(' +
                                        Math.round(inverted ? left : top) + 'px,' +
                                        Math.round(inverted ? bottom : right) + 'px,' +
                                        Math.round(inverted ? right : bottom) + 'px,' +
                                        Math.round(inverted ? top : left) + 'px)'
                                };
                            // issue 74 workaround
                            if (!inverted && wrapper.docMode8 && nodeName === 'DIV') {
                                extend(ret, {
                                    width: right + 'px',
                                    height: bottom + 'px'
                                });
                            }
                            return ret;
                        },
                        // used in attr and animation to update the clipping of all
                        // members
                        updateClipping: function () {
                            clipRect.members.forEach(function (member) {
                                // Member.element is falsy on deleted series, like in
                                // stock/members/series-remove demo. Should be removed
                                // from members, but this will do.
                                if (member.element) {
                                    member.css(clipRect.getCSS(member));
                                }
                            });
                        }
                    });
                },
                /**
                 * Take a color and return it if it's a string, make it a gradient if
                 * it's a gradient configuration object, and apply opacity.
                 *
                 * @function Highcharts.VMLRenderer#color<T>
                 *
                 * @param {T} color
                 * The color or config object
                 *
                 * @return {T}
                 * Processed color
                 */
                color: function (colorOption, elem, prop, wrapper) {
                    var renderer = this,
                        colorObject,
                        regexRgba = /^rgba/,
                        markup,
                        fillType,
                        ret = 'none';
                    // Check for linear or radial gradient
                    if (colorOption &&
                        colorOption.linearGradient) {
                        fillType = 'gradient';
                    }
                    else if (colorOption &&
                        colorOption.radialGradient) {
                        fillType = 'pattern';
                    }
                    if (fillType) {
                        var stopColor_1, stopOpacity_1, gradient = (colorOption.linearGradient ||
                                colorOption.radialGradient), x1 = void 0, y1 = void 0, x2 = void 0, y2 = void 0, opacity1_1, opacity2_1, color1_1, color2_1, fillAttr_1 = '', stops = colorOption.stops, firstStop = void 0, lastStop = void 0, colors_1 = [], addFillNode_1 = function () {
                                // Add the fill subnode. When colors attribute is used,
                                // the meanings of opacity and o:opacity2 are reversed.
                                markup = ['<fill colors="' + colors_1.join(',') +
                                        '" opacity="', opacity2_1, '" o:opacity2="',
                                    opacity1_1, '" type="', fillType, '" ', fillAttr_1,
                                    'focus="100%" method="any" />'];
                            createElement(renderer.prepVML(markup), null, null, elem);
                        };
                        // Extend from 0 to 1
                        firstStop = stops[0];
                        lastStop = stops[stops.length - 1];
                        if (firstStop[0] > 0) {
                            stops.unshift([
                                0,
                                firstStop[1]
                            ]);
                        }
                        if (lastStop[0] < 1) {
                            stops.push([
                                1,
                                lastStop[1]
                            ]);
                        }
                        // Compute the stops
                        stops.forEach(function (stop, i) {
                            if (regexRgba.test(stop[1])) {
                                colorObject = color(stop[1]);
                                stopColor_1 = colorObject.get('rgb');
                                stopOpacity_1 = colorObject.get('a');
                            }
                            else {
                                stopColor_1 = stop[1];
                                stopOpacity_1 = 1;
                            }
                            // Build the color attribute
                            colors_1.push((stop[0] * 100) + '% ' + stopColor_1);
                            // Only start and end opacities are allowed, so we use the
                            // first and the last
                            if (!i) {
                                opacity1_1 = stopOpacity_1;
                                color2_1 = stopColor_1;
                            }
                            else {
                                opacity2_1 = stopOpacity_1;
                                color1_1 = stopColor_1;
                            }
                        });
                        // Apply the gradient to fills only.
                        if (prop === 'fill') {
                            // Handle linear gradient angle
                            if (fillType === 'gradient') {
                                x1 = gradient.x1 || gradient[0] || 0;
                                y1 = gradient.y1 || gradient[1] || 0;
                                x2 = gradient.x2 || gradient[2] || 0;
                                y2 = gradient.y2 || gradient[3] || 0;
                                fillAttr_1 = 'angle="' + (90 - Math.atan((y2 - y1) / // y vector
                                    (x2 - x1) // x vector
                                ) * 180 / Math.PI) + '"';
                                addFillNode_1();
                                // Radial (circular) gradient
                            }
                            else {
                                var r = gradient.r,
                                    sizex_1 = r * 2,
                                    sizey_1 = r * 2,
                                    cx_1 = gradient.cx,
                                    cy_1 = gradient.cy,
                                    radialReference_1 = elem.radialReference,
                                    bBox_1,
                                    applyRadialGradient = function () {
                                        if (radialReference_1) {
                                            bBox_1 = wrapper.getBBox();
                                        cx_1 += (radialReference_1[0] - bBox_1.x) /
                                            bBox_1.width - 0.5;
                                        cy_1 += (radialReference_1[1] - bBox_1.y) /
                                            bBox_1.height - 0.5;
                                        sizex_1 *= radialReference_1[2] / bBox_1.width;
                                        sizey_1 *= radialReference_1[2] / bBox_1.height;
                                    }
                                    fillAttr_1 =
                                        'src="' + getOptions().global.VMLRadialGradientURL +
                                            '" ' +
                                            'size="' + sizex_1 + ',' + sizey_1 + '" ' +
                                            'origin="0.5,0.5" ' +
                                            'position="' + cx_1 + ',' + cy_1 + '" ' +
                                            'color2="' + color2_1 + '" ';
                                    addFillNode_1();
                                };
                                // Apply radial gradient
                                if (wrapper.added) {
                                    applyRadialGradient();
                                }
                                else {
                                    // We need to know the bounding box to get the size
                                    // and position right
                                    wrapper.onAdd = applyRadialGradient;
                                }
                                // The fill element's color attribute is broken in IE8
                                // standards mode, so we need to set the parent shape's
                                // fillcolor attribute instead.
                                ret = color1_1;
                            }
                            // Gradients are not supported for VML stroke, return the first
                            // color. #722.
                        }
                        else {
                            ret = stopColor_1;
                        }
                        // If the color is an rgba color, split it and add a fill node to
                        // hold the opacity component
                    }
                    else if (regexRgba.test(colorOption) &&
                        elem.tagName !== 'IMG') {
                        colorObject = color(colorOption);
                        wrapper[prop + '-opacitySetter'](colorObject.get('a'), prop, elem);
                        ret = colorObject.get('rgb');
                    }
                    else {
                        // 'stroke' or 'fill' node
                        var propNodes = elem.getElementsByTagName(prop);
                        if (propNodes.length) {
                            propNodes[0].opacity = 1;
                            propNodes[0].type = 'solid';
                        }
                        ret = colorOption;
                    }
                    return ret;
                },
                /**
                 * Take a VML string and prepare it for either IE8 or IE6/IE7.
                 *
                 * @function Highcharts.VMLRenderer#prepVML
                 *
                 * @param {Array<(number|string)>} markup
                 * A string array of the VML markup to prepare
                 */
                prepVML: function (markup) {
                    var vmlStyle = 'display:inline-block;behavior:url(#default#VML);',
                        isIE8 = this.isIE8;
                    markup = markup.join('');
                    if (isIE8) { // add xmlns and style inline
                        markup = markup.replace('/>', ' xmlns="urn:schemas-microsoft-com:vml" />');
                        if (markup.indexOf('style="') === -1) {
                            markup = markup.replace('/>', ' style="' + vmlStyle + '" />');
                        }
                        else {
                            markup = markup.replace('style="', 'style="' + vmlStyle);
                        }
                    }
                    else { // add namespace
                        markup = markup.replace('<', '<hcv:');
                    }
                    return markup;
                },
                /**
                 * Create rotated and aligned text
                 *
                 * @function Highcharts.VMLRenderer#text
                 */
                text: SVGRenderer.prototype.html,
                /**
                 * Create and return a path element
                 *
                 * @function Highcharts.VMLRenderer#path
                 *
                 * @param {Highcharts.VMLAttributes|Highcharts.VMLPathArray} [path]
                 */
                path: function (path) {
                    var attr = {
                            // subpixel precision down to 0.1 (width and height = 1px)
                            coordsize: '10 10'
                        };
                    if (isArray(path)) {
                        attr.d = path;
                    }
                    else if (isObject(path)) { // attributes
                        extend(attr, path);
                    }
                    // create the shape
                    return this.createElement('shape').attr(attr);
                },
                /**
                 * Create and return a circle element. In VML circles are implemented as
                 * shapes, which is faster than v:oval
                 *
                 * @function Highcharts.VMLRenderer#circle
                 */
                circle: function (x, y, r) {
                    var circle = this.symbol('circle');
                    if (isObject(x)) {
                        r = x.r;
                        y = x.y;
                        x = x.x;
                    }
                    circle.isCircle = true; // Causes x and y to mean center (#1682)
                    circle.r = r;
                    return circle.attr({ x: x, y: y });
                },
                /**
                 * Create a group using an outer div and an inner v:group to allow
                 * rotating and flipping. A simple v:group would have problems with
                 * positioning child HTML elements and CSS clip.
                 *
                 * @function Highcharts.VMLRenderer#g
                 *
                 * @param {string} name
                 * The name of the group
                 */
                g: function (name) {
                    var wrapper,
                        attribs;
                    // set the class name
                    if (name) {
                        attribs = {
                            'className': 'highcharts-' + name,
                            'class': 'highcharts-' + name
                        };
                    }
                    // the div to hold HTML and clipping
                    wrapper = this.createElement('div').attr(attribs);
                    return wrapper;
                },
                /**
                 * VML override to create a regular HTML image.
                 *
                 * @function Highcharts.VMLRenderer#image
                 */
                image: function (src, x, y, width, height) {
                    var obj = this.createElement('img').attr({ src: src });
                    if (arguments.length > 1) {
                        obj.attr({
                            x: x,
                            y: y,
                            width: width,
                            height: height
                        });
                    }
                    return obj;
                },
                /**
                 * For rectangles, VML uses a shape for rect to overcome bugs and
                 * rotation problems
                 *
                 * @function Highcharts.VMLRenderer#createElement
                 */
                createElement: function (nodeName) {
                    return nodeName === 'rect' ?
                        this.symbol(nodeName) :
                        SVGRenderer.prototype.createElement.call(this, nodeName);
                },
                /**
                 * In the VML renderer, each child of an inverted div (group) is
                 * inverted
                 *
                 * @function Highcharts.VMLRenderer#invertChild
                 */
                invertChild: function (element, parentNode) {
                    var ren = this,
                        parentStyle = parentNode.style,
                        imgStyle = element.tagName === 'IMG' && element.style; // #1111
                        css(element, {
                            flip: 'x',
                            left: (pInt(parentStyle.width) -
                                (imgStyle ? pInt(imgStyle.top) : 1)) + 'px',
                            top: (pInt(parentStyle.height) -
                                (imgStyle ? pInt(imgStyle.left) : 1)) + 'px',
                            rotation: -90
                        });
                    // Recursively invert child elements, needed for nested composite
                    // shapes like box plots and error bars. #1680, #1806.
                    [].forEach.call(element.childNodes, function (child) {
                        ren.invertChild(child, element);
                    });
                },
                /**
                 * Symbol definitions that override the parent SVG renderer's symbols
                 *
                 * @name Highcharts.VMLRenderer#symbols
                 * @type {Highcharts.Dictionary<Function>}
                 */
                symbols: {
                    // VML specific arc function
                    arc: function (x, y, w, h, options) {
                        var start = options.start,
                            end = options.end,
                            radius = options.r || w || h,
                            innerRadius = options.innerR,
                            cosStart = Math.cos(start),
                            sinStart = Math.sin(start),
                            cosEnd = Math.cos(end),
                            sinEnd = Math.sin(end),
                            ret;
                        if (end - start === 0) { // no angle, don't show it.
                            return ['x'];
                        }
                        ret = [
                            'wa',
                            x - radius,
                            y - radius,
                            x + radius,
                            y + radius,
                            x + radius * cosStart,
                            y + radius * sinStart,
                            x + radius * cosEnd,
                            y + radius * sinEnd // end y
                        ];
                        if (options.open && !innerRadius) {
                            ret.push('e', 'M', x, // - innerRadius,
                            y // - innerRadius
                            );
                        }
                        ret.push('at', // anti clockwise arc to
                        x - innerRadius, // left
                        y - innerRadius, // top
                        x + innerRadius, // right
                        y + innerRadius, // bottom
                        x + innerRadius * cosEnd, // start x
                        y + innerRadius * sinEnd, // start y
                        x + innerRadius * cosStart, // end x
                        y + innerRadius * sinStart, // end y
                        'x', // finish path
                        'e' // close
                        );
                        ret.isArc = true;
                        return ret;
                    },
                    // Add circle symbol path. This performs significantly faster than
                    // v:oval.
                    circle: function (x, y, w, h, wrapper) {
                        if (wrapper && defined(wrapper.r)) {
                            w = h = 2 * wrapper.r;
                        }
                        // Center correction, #1682
                        if (wrapper && wrapper.isCircle) {
                            x -= w / 2;
                            y -= h / 2;
                        }
                        // Return the path
                        return [
                            'wa',
                            x,
                            y,
                            x + w,
                            y + h,
                            x + w,
                            y + h / 2,
                            x + w,
                            y + h / 2,
                            'e' // close
                        ];
                    },
                    /**
                     * Add rectangle symbol path which eases rotation and omits arcsize
                     * problems compared to the built-in VML roundrect shape. When
                     * borders are not rounded, use the simpler square path, else use
                     * the callout path without the arrow.
                     */
                    rect: function (x, y, w, h, options) {
                        return SVGRenderer.prototype.symbols[!defined(options) || !options.r ? 'square' : 'callout'].call(0, x, y, w, h, options);
                    }
                }
            };
            H.VMLRenderer = VMLRenderer = function () {
                this.init.apply(this, arguments);
            };
            extend(VMLRenderer.prototype, SVGRenderer.prototype);
            extend(VMLRenderer.prototype, VMLRendererExtension);
            // general renderer
            RendererRegistry.registerRendererType('VMLRenderer', VMLRenderer, true);
            // 3D additions
            VMLRenderer3D.compose(VMLRenderer, SVGRenderer);
        }
        SVGRenderer.prototype.getSpanWidth = function (wrapper, tspan) {
            var renderer = this,
                bBox = wrapper.getBBox(true),
                actualWidth = bBox.width;
            // Old IE cannot measure the actualWidth for SVG elements (#2314)
            if (!svg && renderer.forExport) {
                actualWidth = renderer.measureSpanWidth(tspan.firstChild.data, wrapper.styles);
            }
            return actualWidth;
        };
        // This method is used with exporting in old IE, when emulating SVG (see #2314)
        SVGRenderer.prototype.measureSpanWidth = function (text, styles) {
            var measuringSpan = doc.createElement('span'),
                offsetWidth,
                textNode = doc.createTextNode(text);
            measuringSpan.appendChild(textNode);
            css(measuringSpan, styles);
            this.box.appendChild(measuringSpan);
            offsetWidth = measuringSpan.offsetWidth;
            discardElement(measuringSpan); // #2463
            return offsetWidth;
        };

    });
    _registerModule(_modules, 'masters/modules/oldie.src.js', [], function () {


    });
}));