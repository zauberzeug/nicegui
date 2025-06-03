function applyAllPolyfills (){
	applyBrowserPolyfill();
	applyDomUtilPolyfill();
	applyUtilPolyfill();
	applyMouseEventPolyfill();
	applyDomEventPolyfill();
	applyDeprecatedMethodsPolyfill();
	applyFactoryMethodsPolyfill();
	applyMiscPolyfill();
};

function applyMinimumPolyfills() {
	applyMouseEventPolyfill();
	applyFactoryMethodsPolyfill();
};

function applyBrowserPolyfill() {
	/* eslint-disable */
	L.Browser.canvas = (function () {
		return !!document.createElement('canvas').getContext;
	}());

	function userAgentContains(str) {
		return navigator.userAgent.toLowerCase().indexOf(str) >= 0;
	}

	const style = document.documentElement.style;
	L.Browser.ie = 'ActiveXObject' in window;
	L.Browser.ielt9 = L.Browser.ie && !document.addEventListener;
	L.Browser.edge = 'msLaunchUri' in navigator && !('documentMode' in document);
	L.Browser.webkit = userAgentContains('webkit');
	L.Browser.android = userAgentContains('android');
	L.Browser.android23 = userAgentContains('android 2') || userAgentContains('android 3');
	L.Browser.webkitVer = parseInt(/WebKit\/([0-9]+)|$/.exec(navigator.userAgent)[1], 10); // also matches AppleWebKit
	L.Browser.androidStock = L.Browser.android && userAgentContains('Google') && L.Browser.webkitVer < 537 && !('AudioNode' in window);
	L.Browser.opera = !!window.opera;
	L.Browser.chrome = !L.Browser.edge && L.Browser.chrome;
	L.Browser.gecko = userAgentContains('gecko') && !L.Browser.webkit && !L.Browser.opera && !L.Browser.ie;

	L.Browser.phantom = userAgentContains('phantom');
	L.Browser.opera12 = 'OTransition' in style;
	L.Browser.win = navigator.platform.indexOf('Win') === 0;
	L.Browser.ie3d = L.Browser.ie && ('transition' in style);

	L.Browser.webkit3d = ('WebKitCSSMatrix' in window) && ('m11' in new window.WebKitCSSMatrix());
	L.Browser.gecko3d = 'MozPerspective' in style;
	L.Browser.mobileWebkit = L.Browser.mobile && L.Browser.webkit;
	L.Browser.mobileWebkit3d = L.Browser.mobile && L.Browser.webkit3d;

	L.Browser.svg = !!(document.createElementNS && L.SVG.create('svg').createSVGRect);
	L.Browser.inlineSvg = !!L.Browser.svg && (function () {
		const div = document.createElement('div');
		div.innerHTML = '<svg/>';
		return (div.firstChild && div.firstChild.namespaceURI) === 'http://www.w3.org/2000/svg';
	})();

	L.Browser.any3d = !window.L_DISABLE_3D && (L.Browser.webkit3d || L.Browser.gecko3d);
	L.Browser.vml = false;

	L.Browser.msPointer = !window.PointerEvent && window.MSPointerEvent;
	L.Browser.pointer = L.Browser.pointer || L.Browser.msPointer;

	L.Browser.touch = !window.L_NO_TOUCH && L.Browser.touch;

	L.Browser.mobileOpera = L.Browser.mobile && L.Browser.opera;
	L.Browser.mobileGecko = L.Browser.mobile && L.Browser.gecko;

	L.Browser.passiveEvents = (function () {
		var supportsPassiveOption = false;
		try {
			var opts = Object.defineProperty({}, 'passive', {
				get: function () { // eslint-disable-line getter-return
					supportsPassiveOption = true;
				}
			});
			window.addEventListener('testPassiveEventSupport', L.Util.falseFn, opts);
			window.removeEventListener('testPassiveEventSupport', L.Util.falseFn, opts);
		} catch (e) {
			// Errors can safely be ignored since this is only a browser support test.
		}
		return supportsPassiveOption;
	}());
};

function applyDomUtilPolyfill() {
	L.noConflict = L.noConflict || function () {
		console.error('noConflict doesn\'t work anymore');
		return this;
	};

	const setPosCore = L.DomUtil.setPosition;
	L.DomUtil.setPosition = function (el, point) {
		el._leaflet_pos = point;
		setPosCore(el, point);
	};

	const getPosCore = L.DomUtil.getPosition;
	L.DomUtil.getPosition = function (el) {
		return el._leaflet_pos || getPosCore(el);
	};

	L.DomUtil.getStyle = function (el, style) {
		let value = el.style[style] || (el.currentStyle && el.currentStyle[style]);

		if ((!value || value === 'auto') && document.defaultView) {
			const css = document.defaultView.getComputedStyle(el, null);
			value = css ? css[style] : null;
		}
		return value === 'auto' ? null : value;
	};

	L.DomUtil.testProp = function (props) {
		const style = document.documentElement.style;

		for (let i = 0; i < props.length; i++) {
			if (props[i] in style) {
				return props[i];
			}
		}
		return false;
	};

	L.DomUtil.empty = function (el) {
		while (el.firstChild) {
			el.removeChild(el.firstChild);
		}

	};

	L.DomUtil.remove = function (el) {
		const parent = el.parentNode;
		if (parent) {
			parent.removeChild(el);
		}
	};

	L.DomUtil.TRANSITION = L.DomUtil.testProp(['webkitTransition', 'transition', 'OTransition', 'MozTransition', 'msTransition']);

	L.DomUtil.TRANSITION_END = L.DomUtil.TRANSITION === 'webkitTransition' || L.DomUtil.TRANSITION === 'OTransition' ? `${L.DomUtil.TRANSITION}End` : 'transitionend';

	L.DomUtil.TRANSFORM = L.DomUtil.testProp(['transform', 'webkitTransform', 'OTransform', 'MozTransform', 'msTransform']);
	L.DomUtil.setTransform = function(el, offset, scale) {
		var pos = offset || new Point(0, 0);

		el.style[L.DomUtil.TRANSFORM] =
			(Browser.ie3d ?
				'translate(' + pos.x + 'px,' + pos.y + 'px)' :
				'translate3d(' + pos.x + 'px,' + pos.y + 'px,0)') +
			(scale ? ' scale(' + scale + ')' : '');
	}

	L.DomUtil.removeClass = (el, name) => el.classList.remove(name);

	// @function setOpacity(el: HTMLElement, opacity: Number)
	// Set the opacity of an element (including old IE support).
	// `opacity` must be a number from `0` to `1`.
	L.DomUtil.setOpacity = function (el, value) {
		if ('opacity' in el.style) {
			el.style.opacity = value;
		} else if ('filter' in el.style) {
			_setOpacityIE(el, value);
		}
	};

	function _setOpacityIE(el, value) {
		let filter = false;
		const filterName = 'DXImageTransform.Microsoft.Alpha';

		// filters collection throws an error if we try to retrieve a filter that doesn't exist
		try {
			filter = el.filters.item(filterName);
		} catch (e) {
			// don't set opacity to 1 if we haven't already set an opacity,
			// it isn't needed and breaks transparent pngs.
			if (value === 1) { return; }
		}

		value = Math.round(value * 100);

		if (filter) {
			filter.Enabled = (value !== 100);
			filter.Opacity = value;
		} else {
			el.style.filter += ` progid:${filterName}(opacity=${value})`;
		}
	}

	L.DomUtil.addClass = function (el, name) {
		const classes = L.Util.splitWords(name);
		el.classList.add(...classes);
	};

	L.DomUtil.setClass = (el, name) => { el.classList.value = name; };
	L.DomUtil.getClass = el => el.classList.value;
	L.DomUtil.hasClass = (el, name) => el.classList.contains(name);

	if (!('onselectstart' in document)) {
		var userSelectProperty = L.DomUtil.testProp(
			['userSelect', 'WebkitUserSelect', 'OUserSelect', 'MozUserSelect', 'msUserSelect']);

		L.DomUtil.disableTextSelection = function () {
			if (userSelectProperty) {
				var style = document.documentElement.style;
				_userSelect = style[userSelectProperty];
				style[userSelectProperty] = 'none';
			}
		};
		L.DomUtil.enableTextSelection = function () {
			if (userSelectProperty) {
				document.documentElement.style[userSelectProperty] = _userSelect;
				_userSelect = undefined;
			}
		};
	}
};

function applyUtilPolyfill() {
	L.Util.trim = function (str) {
		return str.trim ? str.trim() : str.replace(/^\s+|\s+$/g, '');
	};

	L.Util.create = Object.create || (function () {
		function F() { }
		return function (proto) {
			F.prototype = proto;
			return new F();
		};
	})();

	L.Util.isArray = Array.isArray || function (obj) {
		return (Object.prototype.toString.call(obj) === '[object Array]');
	};

	L.Util.bind = function (fn, obj) {
		const slice = Array.prototype.slice;

		if (fn.bind) {
			return fn.bind.apply(fn, slice.call(arguments, 1));
		}

		const args = slice.call(arguments, 2);

		return function () {
			return fn.apply(obj, args.length ? args.concat(slice.call(arguments)) : arguments);
		};
	};

	L.Util.getParamString = function (obj, existingUrl, uppercase) {
		const params = [];
		for (const i in obj) {
			if (Object.hasOwn(obj, i)) {
				params.push(`${encodeURIComponent(uppercase ? i.toUpperCase() : i)}=${encodeURIComponent(obj[i])}`);
			}
		}
		return ((!existingUrl || !existingUrl.includes('?')) ? '?' : '&') + params.join('&');
	}



	const requestFn = typeof window === 'undefined' ? L.Util.falseFn : window.requestAnimationFrame;
	const cancelFn = typeof window === 'undefined' ? L.Util.falseFn : window.cancelAnimationFrame;
	L.Util.requestAnimFrame = function (fn, context) {
		return requestFn.call(window, fn.bind(context));
	}
	L.Util.cancelAnimFrame = function (id) {
		cancelFn.call(window, id);
	}

	L.Util.extend = function(dest) {
		var i, j, len, src;

		for (j = 1, len = arguments.length; j < len; j++) {
			src = arguments[j];
			for (i in src) {
				dest[i] = src[i];
			}
		}
		return dest;
	};
	
	L.extend = L.Util.extend;
	L.bind = L.Util.bind;
	L.stamp = L.Util.stamp;
	L.setOptions = L.Util.setOptions;
};

function applyMouseEventPolyfill() {
	L.DomEvent.getMousePosition = L.DomEvent.getPointerPosition;

	const _super_findEventTargets = L.Map.prototype._findEventTargets;
	const _super_initEvents = L.Map.prototype._initEvents;
	L.Map.include({
		mouseEventToContainerPoint(e) {
			return this.pointerEventToContainerPoint(e);
		},
		mouseEventToLayerPoint(e) {
			return this.pointerEventToLayerPoint(e);
		},
		mouseEventToLatLng(e) {
			return this.pointerEventToLatLng(e);
		},
	
		// Fallback bubblingMouseEvents
		_findEventTargets(e, type) {
			const targets = _super_findEventTargets.call(this, e, type);
			for (let i = 0; i < targets.length; i++) {
				if (targets[i].options.bubblingMouseEvents !== undefined) {
					targets[i].options.bubblingPointerEvents = targets[i].options.bubblingMouseEvents;
				}
			}
			return targets;
		},
	
		// Add support for mouse events
		_initEvents(remove) {
			_super_initEvents.call(this, remove);
			const onOff = remove ? L.DomEvent.off : L.DomEvent.on;
			onOff(this._container, 'mousedown mouseup mouseover mouseout mousemove', this._handleDOMEvent, this);
		}
	});
	
	const _super_disableClickPropagation = L.DomEvent.disableClickPropagation;
	L.DomEvent.disableClickPropagation = function disableClickPropagation(el) {
		L.DomEvent.on(el, 'mousedown touchstart', L.DomEvent.stopPropagation);
		return _super_disableClickPropagation(el);
	}
};

function applyDomEventPolyfill() {
	L.DomEvent.getPropagationPath = function(ev) {
		if (ev.composedPath) {
			return ev.composedPath();
		}

		const path = [];
		let el = ev.target;

		while (el) {
			path.push(el);
			el = el.parentNode;
		}
		return path;
	}

	L.DomEvent.getWheelDelta = function(e) {
		return (e.deltaY && e.deltaMode === 0) ? -e.deltaY / getWheelPxFactor() : // Pixels
			(e.deltaY && e.deltaMode === 1) ? -e.deltaY * 20 : // Lines
			(e.deltaY && e.deltaMode === 2) ? -e.deltaY * 60 : // Pages
			(e.deltaX || e.deltaZ) ? 0 :	// Skip horizontal/depth wheel events
			e.wheelDelta ? (e.wheelDeltaY || e.wheelDelta) / 2 : // Legacy IE pixels
			(e.detail && Math.abs(e.detail) < 32765) ? -e.detail * 20 : // Legacy Moz lines
			e.detail ? e.detail / -32765 * 60 : // Legacy Moz pages
			0;
	}
};

function applyDeprecatedMethodsPolyfill() {
	const _super_initLayout = L.Control.Layers.prototype._initLayout;
	L.Control.Layers.include({
		_initLayout() {
			_super_initLayout.call(this);

			this._container.setAttribute('aria-haspopup', true);
		}
	});

	L.Evented.include({
		_propagateEvent(e) {
			for (const p of Object.values(this._eventParents ?? {})) {
				p.fire(e.type, {
					layer: e.target,
					propagatedFrom: e.target,
					...e
				}, true);
			}
		}
	});

	const _super_getIconUrl = L.Icon.Default.prototype._getIconUrl;
	L.Icon.Default.include({
		_getIconUrl: function (name) {
			if (typeof L.Icon.Default.imagePath !== 'string') {	// Deprecated, backwards-compatibility only
				L.Icon.Default.imagePath = this._detectIconPath();
			}
			return _super_getIconUrl.call(this, name);
		},
	})

	const _super_initializeCircle = L.Control.Layers.prototype.initialize;
	L.Circle.include({
		initialize: function (latlng, options, legacyOptions) {
			if (typeof options === 'number') {
				// Backwards compatibility with 0.7.x factory (latlng, radius, options?)
				options ??= {};
				Object.assign(options, legacyOptions, {radius: options});
			}
			_super_initializeCircle.call(this, latlng, options);
		}
	});

	function exportPrototypeMethods(klass) {
		const proto = klass.prototype;
		const methodNames = Object.getOwnPropertyNames(proto)
			.filter(name => name !== 'constructor' && typeof proto[name] === 'function');

		return Object.fromEntries(
			methodNames.map(name => [name, proto[name].bind(proto)])
		);
	};

	L.Mixin = {
		Events: exportPrototypeMethods(L.Evented)
	};

	L.LineUtil._flat = function (latlngs) {
		console.warn('Deprecated use of _flat, please use L.LineUtil.isFlat instead.');
		return L.LineUtil.isFlat(latlngs);
	};

	L.Polyline._flat = L.LineUtil._flat;
};

function applyFactoryMethodsPolyfill() {
	L.control = function (options) {
		return new L.Control(options);
	};
	L.control.layers = function (baseLayers, overlays, options) {
		return new L.Control.Layers(baseLayers, overlays, options);
	};

	L.control.zoom = function (options) {
		return new L.Control.Zoom(options);
	};
	L.control.scale = function (options) {
		return new L.Control.Scale(options);
	};
	L.control.attribution = function (options) {
		return new L.Control.Attribution(options);
	};

	L.latLng = function (a, b, c) {
		return new L.LatLng(a, b, c);
	};
	L.latLngBounds = function (a, b) {
		return new L.LatLngBounds(a, b);
	};
	L.point = function (x, y, round) {
		return new L.Point(x, y, round);
	};
	L.bounds = function (a, b) {
		return new L.Bounds(a, b);
	};
	L.transformation = function (a, b, c, d) {
		return new L.Transformation(a, b, c, d);
	}

	L.icon = function (options) {
		return new L.Icon(options);
	}
	L.divIcon = function(options) {
		return new L.DivIcon(options);
	}
	L.marker = function (latlng, options) {
		return new L.Marker(latlng, options);
	};
	L.gridLayer = function (options) {
		return new L.GridLayer(options);
	}
	L.tileLayer = function (url, options) {
		return new L.TileLayer(url, options);
	};
	L.tileLayer.wms = function (url, options) {
		return new L.TileLayer.WMS(url, options);
	};
	L.canvas = function (options) {
		return L.Browser.canvas ? new L.Canvas(options) : null;
	};
	L.svg = function (options) {
		return L.Browser.svg ? new L.SVG(options) : null;
	}
	L.circle = function (latlng, options, legacyOptions) {
		return new L.Circle(latlng, options, legacyOptions);
	};
	L.circleMarker = function (latlng, options) {
		return new L.CircleMarker(latlng, options);
	};
	L.polygon = function (latlngs, options) {
		return new L.Polygon(latlngs, options);
	};
	L.polyline = function (latlngs, options) {
		return new L.Polyline(latlngs, options);
	};
	L.rectangle = function (latLngBounds, options) {
		return new L.Rectangle(latLngBounds, options);
	};
	L.geoJSON = L.geoJson = function (geojson, options) {
		return new L.GeoJSON(geojson, options);
	};
	L.layerGroup = function (layers, options) {
		return new L.LayerGroup(layers, options);
	};
	L.featureGroup = function (layers, options) {
		return new L.FeatureGroup(layers, options);
	};
	L.imageOverlay = function (image, bounds, options) {
		return new L.ImageOverlay(image, bounds, options);
	};
	L.videoOverlay = function (video, bounds, options) {
		return new L.VideoOverlay(video, bounds, options);
	};
	L.svgOverlay = function (el, bounds, options) {
		return new L.SVGOverlay(el, bounds, options);
	};
	L.popup = function (options, source) {
		return new L.Popup(options, source);
	};
	L.tooltip = function (options, source) {
		return new L.Tooltip(options, source);
	};
	L.map = function (id, options) {
		return new L.Map(id, options);
	};
};

function applyMiscPolyfill() {
	const ccsStyle = document.createElement('style');
	ccsStyle.textContent = `
	.leaflet-tile {
		filter: inherit;
	}
	`;
	document.head.appendChild(ccsStyle);
}

globalThis.applyAllPolyfills = applyAllPolyfills;
globalThis.applyMinimumPolyfills = applyMinimumPolyfills;
globalThis.applyBrowserPolyfill = applyBrowserPolyfill;
globalThis.applyDomUtilPolyfill = applyDomUtilPolyfill;
globalThis.applyUtilPolyfill = applyUtilPolyfill;
globalThis.applyMouseEventPolyfill = applyMouseEventPolyfill;
globalThis.applyDomEventPolyfill = applyDomEventPolyfill;
globalThis.applyDeprecatedMethodsPolyfill = applyDeprecatedMethodsPolyfill;
globalThis.applyFactoryMethodsPolyfill = applyFactoryMethodsPolyfill;
globalThis.applyMiscPolyfill = applyMiscPolyfill;