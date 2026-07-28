/*!
* Quasar Framework v2.22.0
* (c) 2015-present Razvan Stoenescu
* Released under the MIT License.
*/
(function(vue) {
	//#region \0rolldown/runtime.js
	var __defProp = Object.defineProperty;
	var __exportAll = (all, no_symbols) => {
		let target = {};
		for (var name in all) __defProp(target, name, {
			get: all[name],
			enumerable: true
		});
		if (!no_symbols) __defProp(target, Symbol.toStringTag, { value: "Module" });
		return target;
	};
	//#endregion
	//#region src/utils/private.inject-obj-prop/inject-obj-prop.js
	function injectProp(target, propName, get, set) {
		Object.defineProperty(target, propName, {
			get,
			set,
			enumerable: true
		});
		return target;
	}
	function injectMultipleProps(target, props) {
		for (const key in props) injectProp(target, key, props[key]);
		return target;
	}
	//#endregion
	//#region src/plugins/platform/Platform.js
	/**
	* __ QUASAR_SSR __            -> runs on SSR on client or server
	* __ QUASAR_SSR_SERVER __     -> runs on SSR on server
	* __ QUASAR_SSR_CLIENT __     -> runs on SSR on client
	* __ QUASAR_SSR_PWA __        -> built with SSR+PWA; may run on SSR on client or on PWA client
	*                              (needs runtime detection)
	*/
	const isRuntimeSsrPreHydration = (0, vue.ref)(false);
	let preHydrationBrowser;
	function getMatch(userAgent, platformMatch) {
		const match = /(edg|edge|edga|edgios)\/([\w.]+)/.exec(userAgent) || /(opr)[\/]([\w.]+)/.exec(userAgent) || /(vivaldi)[\/]([\w.]+)/.exec(userAgent) || /(chrome|crios)[\/]([\w.]+)/.exec(userAgent) || /(version)(applewebkit)[\/]([\w.]+).*(safari)[\/]([\w.]+)/.exec(userAgent) || /(webkit)[\/]([\w.]+).*(version)[\/]([\w.]+).*(safari)[\/]([\w.]+)/.exec(userAgent) || /(firefox|fxios)[\/]([\w.]+)/.exec(userAgent) || /(webkit)[\/]([\w.]+)/.exec(userAgent) || /(opera)(?:.*version|)[\/]([\w.]+)/.exec(userAgent) || [];
		return {
			browser: match[5] || match[3] || match[1] || "",
			version: match[4] || match[2] || "0",
			platform: platformMatch[0] || ""
		};
	}
	function getPlatformMatch(userAgent) {
		return /(ipad)/.exec(userAgent) || /(ipod)/.exec(userAgent) || /(windows phone)/.exec(userAgent) || /(iphone)/.exec(userAgent) || /(kindle)/.exec(userAgent) || /(silk)/.exec(userAgent) || /(android)/.exec(userAgent) || /(win)/.exec(userAgent) || /(mac)/.exec(userAgent) || /(linux)/.exec(userAgent) || /(cros)/.exec(userAgent) || /(playbook)/.exec(userAgent) || /(bb)/.exec(userAgent) || /(blackberry)/.exec(userAgent) || [];
	}
	const hasTouch = "ontouchstart" in window || window.navigator.maxTouchPoints > 0;
	function getPlatform(UA) {
		const userAgent = UA.toLowerCase();
		const matched = getMatch(userAgent, getPlatformMatch(userAgent));
		const browser = {
			mobile: false,
			desktop: false,
			cordova: false,
			capacitor: false,
			nativeMobile: false,
			electron: false,
			bex: false,
			linux: false,
			mac: false,
			win: false,
			cros: false,
			chrome: false,
			firefox: false,
			opera: false,
			safari: false,
			vivaldi: false,
			edge: false,
			edgeChromium: false,
			ie: false,
			webkit: false,
			android: false,
			ios: false,
			ipad: false,
			iphone: false,
			ipod: false,
			kindle: false,
			winphone: false,
			blackberry: false,
			playbook: false,
			silk: false
		};
		if (matched.browser) {
			browser[matched.browser] = true;
			browser.version = matched.version;
			browser.versionNumber = Number.parseInt(matched.version, 10);
		}
		if (matched.platform) browser[matched.platform] = true;
		const knownMobiles = browser.android || browser.ios || browser.bb || browser.blackberry || browser.ipad || browser.iphone || browser.ipod || browser.kindle || browser.playbook || browser.silk || browser["windows phone"];
		if (knownMobiles === true || userAgent.includes("mobile")) browser.mobile = true;
		else browser.desktop = true;
		if (browser["windows phone"]) {
			browser.winphone = true;
			delete browser["windows phone"];
		}
		if (browser.edga || browser.edgios || browser.edg) {
			browser.edge = true;
			matched.browser = "edge";
		} else if (browser.crios) {
			browser.chrome = true;
			matched.browser = "chrome";
		} else if (browser.fxios) {
			browser.firefox = true;
			matched.browser = "firefox";
		}
		if (browser.ipod || browser.ipad || browser.iphone) browser.ios = true;
		if (browser.vivaldi) {
			matched.browser = "vivaldi";
			browser.vivaldi = true;
		}
		if (browser.chrome || browser.opr || browser.safari || browser.vivaldi || browser.mobile && !browser.ios && !knownMobiles) browser.webkit = true;
		if (browser.opr) {
			matched.browser = "opera";
			browser.opera = true;
		}
		if (browser.safari) {
			if (browser.blackberry || browser.bb) {
				matched.browser = "blackberry";
				browser.blackberry = true;
			} else if (browser.playbook) {
				matched.browser = "playbook";
				browser.playbook = true;
			} else if (browser.android) {
				matched.browser = "android";
				browser.android = true;
			} else if (browser.kindle) {
				matched.browser = "kindle";
				browser.kindle = true;
			} else if (browser.silk) {
				matched.browser = "silk";
				browser.silk = true;
			}
		}
		browser.name = matched.browser;
		browser.platform = matched.platform;
		if (userAgent.includes("electron")) browser.electron = true;
		else if (document.location.href.includes("-extension://")) browser.bex = true;
		else {
			if (window.Capacitor !== void 0) {
				browser.capacitor = true;
				browser.nativeMobile = true;
				browser.nativeMobileWrapper = "capacitor";
			} else if (window._cordovaNative !== void 0 || window.cordova !== void 0) {
				browser.cordova = true;
				browser.nativeMobile = true;
				browser.nativeMobileWrapper = "cordova";
			}
			if (isRuntimeSsrPreHydration.value) preHydrationBrowser = { is: { ...browser } };
			if (hasTouch && browser.mac && (browser.desktop && browser.safari || browser.nativeMobile && !browser.android && !browser.ios && !browser.ipad)) {
				delete browser.mac;
				delete browser.desktop;
				const platform = Math.min(window.innerHeight, window.innerWidth) > 414 ? "ipad" : "iphone";
				Object.assign(browser, {
					mobile: true,
					ios: true,
					platform,
					[platform]: true
				});
			}
			if (!browser.mobile && window.navigator.userAgentData && window.navigator.userAgentData.mobile) {
				delete browser.desktop;
				browser.mobile = true;
			}
		}
		return browser;
	}
	const userAgent = navigator.userAgent || navigator.vendor || window.opera;
	const ssrClient = {
		has: {
			touch: false,
			webStorage: false
		},
		within: { iframe: false }
	};
	const client = {
		userAgent,
		is: getPlatform(userAgent),
		has: { touch: hasTouch },
		within: { iframe: window.self !== window.top }
	};
	const Platform = { install(opts) {
		const { $q } = opts;
		if (isRuntimeSsrPreHydration.value) {
			opts.onSSRHydrated.push(() => {
				Object.assign($q.platform, client);
				isRuntimeSsrPreHydration.value = false;
			});
			$q.platform = (0, vue.reactive)(this);
		} else $q.platform = this;
	} };
	{
		let hasWebStorage;
		injectProp(client.has, "webStorage", () => {
			if (hasWebStorage !== void 0) return hasWebStorage;
			try {
				if (window.localStorage) {
					hasWebStorage = true;
					return true;
				}
			} catch {}
			hasWebStorage = false;
			return false;
		});
		Object.assign(Platform, client);
		if (isRuntimeSsrPreHydration.value) {
			Object.assign(Platform, preHydrationBrowser, ssrClient);
			preHydrationBrowser = null;
		}
	}
	//#endregion
	//#region src/utils/private.create/create.js
	function createComponent(raw) {
		return (0, vue.markRaw)((0, vue.defineComponent)(raw));
	}
	function createDirective(raw) {
		return (0, vue.markRaw)(raw);
	}
	const createReactivePlugin = (state, plugin) => {
		const reactiveState = (0, vue.reactive)(state);
		for (const name in state) injectProp(plugin, name, () => reactiveState[name], (val) => {
			reactiveState[name] = val;
		});
		return plugin;
	};
	//#endregion
	//#region src/utils/event/event.js
	const listenOpts = {
		hasPassive: false,
		passiveCapture: true,
		notPassiveCapture: true
	};
	try {
		const opts = Object.defineProperty({}, "passive", { get() {
			Object.assign(listenOpts, {
				hasPassive: true,
				passive: { passive: true },
				notPassive: { passive: false },
				passiveCapture: {
					passive: true,
					capture: true
				},
				notPassiveCapture: {
					passive: false,
					capture: true
				}
			});
		} });
		window.addEventListener("qtest", null, opts);
		window.removeEventListener("qtest", null, opts);
	} catch {}
	function noop() {}
	function leftClick(e) {
		return e.button === 0;
	}
	function middleClick(e) {
		return e.button === 1;
	}
	function rightClick(e) {
		return e.button === 2;
	}
	function position(e) {
		if (e.touches && e.touches[0]) e = e.touches[0];
		else if (e.changedTouches && e.changedTouches[0]) e = e.changedTouches[0];
		else if (e.targetTouches && e.targetTouches[0]) e = e.targetTouches[0];
		return {
			top: e.clientY,
			left: e.clientX
		};
	}
	function getEventPath(e) {
		if (e.path) return e.path;
		if (e.composedPath) return e.composedPath();
		const path = [];
		let el = e.target;
		while (el) {
			path.push(el);
			if (el.tagName === "HTML") {
				path.push(document, window);
				return path;
			}
			el = el.parentElement;
		}
	}
	const LINE_HEIGHT = 40;
	const PAGE_HEIGHT = 800;
	function getMouseWheelDistance(e) {
		let x = e.deltaX, y = e.deltaY;
		if ((x || y) && e.deltaMode) {
			const multiplier = e.deltaMode === 1 ? LINE_HEIGHT : PAGE_HEIGHT;
			x *= multiplier;
			y *= multiplier;
		}
		if (e.shiftKey && !x) [y, x] = [x, y];
		return {
			x,
			y
		};
	}
	function stop(e) {
		e.stopPropagation();
	}
	function prevent(e) {
		if (e.cancelable !== false) e.preventDefault();
	}
	function stopAndPrevent(e) {
		if (e.cancelable !== false) e.preventDefault();
		e.stopPropagation();
	}
	function preventDraggable(el, status) {
		if (el === void 0 || status && el.__dragPrevented) return;
		const fn = status ? (element) => {
			element.__dragPrevented = true;
			element.addEventListener("dragstart", prevent, listenOpts.notPassiveCapture);
		} : (element) => {
			delete element.__dragPrevented;
			element.removeEventListener("dragstart", prevent, listenOpts.notPassiveCapture);
		};
		el.querySelectorAll("a, img").forEach(fn);
	}
	function addEvt(ctx, targetName, events) {
		const name = `__q_${targetName}_evt`;
		ctx[name] = [...ctx[name] ?? [], ...events];
		events.forEach((evt) => {
			evt[0].addEventListener(evt[1], ctx[evt[2]], listenOpts[evt[3]]);
		});
	}
	function cleanEvt(ctx, targetName) {
		const name = `__q_${targetName}_evt`;
		if (ctx[name] !== void 0) {
			ctx[name].forEach((evt) => {
				evt[0].removeEventListener(evt[1], ctx[evt[2]], listenOpts[evt[3]]);
			});
			ctx[name] = void 0;
		}
	}
	var event_default = {
		listenOpts,
		leftClick,
		middleClick,
		rightClick,
		position,
		getEventPath,
		getMouseWheelDistance,
		stop,
		prevent,
		stopAndPrevent,
		preventDraggable
	};
	//#endregion
	//#region src/utils/debounce/debounce.js
	function debounce(fn, wait = 250, immediate) {
		let timer = null;
		function debounced(...args) {
			const later = () => {
				timer = null;
				if (!immediate) fn.apply(this, args);
			};
			if (timer !== null) clearTimeout(timer);
			else if (immediate) fn.apply(this, args);
			timer = setTimeout(later, wait);
		}
		debounced.cancel = () => {
			if (timer !== null) clearTimeout(timer);
		};
		return debounced;
	}
	//#endregion
	//#region src/plugins/screen/Screen.js
	const SIZE_LIST = [
		"sm",
		"md",
		"lg",
		"xl"
	];
	const { passive: passive$4 } = listenOpts;
	var Screen_default = createReactivePlugin({
		width: 0,
		height: 0,
		name: "xs",
		sizes: {
			sm: 600,
			md: 1024,
			lg: 1440,
			xl: 1920
		},
		lt: {
			sm: true,
			md: true,
			lg: true,
			xl: true
		},
		gt: {
			xs: false,
			sm: false,
			md: false,
			lg: false
		},
		xs: true,
		sm: false,
		md: false,
		lg: false,
		xl: false
	}, {
		setSizes: noop,
		setDebounce: noop,
		install({ $q, onSSRHydrated }) {
			$q.screen = this;
			if (this.__installed) {
				if ($q.config.screen !== void 0) if (!$q.config.screen.bodyClasses) document.body.classList.remove(`screen--${this.name}`);
				else this.__update(true);
				return;
			}
			const { visualViewport } = window;
			const target = visualViewport || window;
			const scrollingElement = document.scrollingElement || document.documentElement;
			const getSize = visualViewport === void 0 || client.is.mobile ? () => [Math.max(window.innerWidth, scrollingElement.clientWidth), Math.max(window.innerHeight, scrollingElement.clientHeight)] : () => [visualViewport.width * visualViewport.scale + window.innerWidth - scrollingElement.clientWidth, visualViewport.height * visualViewport.scale + window.innerHeight - scrollingElement.clientHeight];
			const useBodyClasses = $q.config.screen?.bodyClasses === true;
			this.__update = (force) => {
				const [w, h] = getSize();
				if (h !== this.height) this.height = h;
				if (w !== this.width) this.width = w;
				else if (force !== true) return;
				let s = this.sizes;
				this.gt.xs = w >= s.sm;
				this.gt.sm = w >= s.md;
				this.gt.md = w >= s.lg;
				this.gt.lg = w >= s.xl;
				this.lt.sm = w < s.sm;
				this.lt.md = w < s.md;
				this.lt.lg = w < s.lg;
				this.lt.xl = w < s.xl;
				this.xs = this.lt.sm;
				this.sm = this.gt.xs && this.lt.md;
				this.md = this.gt.sm && this.lt.lg;
				this.lg = this.gt.md && this.lt.xl;
				this.xl = this.gt.lg;
				s = this.xs && "xs" || this.sm && "sm" || this.md && "md" || this.lg && "lg" || "xl";
				if (s !== this.name) {
					if (useBodyClasses) {
						document.body.classList.remove(`screen--${this.name}`);
						document.body.classList.add(`screen--${s}`);
					}
					this.name = s;
				}
			};
			let updateEvt, updateSizes = {}, updateDebounce = 16;
			this.setSizes = (sizes) => {
				SIZE_LIST.forEach((name) => {
					if (sizes[name] !== void 0) updateSizes[name] = sizes[name];
				});
			};
			this.setDebounce = (deb) => {
				updateDebounce = deb;
			};
			const start = () => {
				const style = getComputedStyle(document.body);
				if (style.getPropertyValue("--q-size-sm")) SIZE_LIST.forEach((name) => {
					this.sizes[name] = Number.parseInt(style.getPropertyValue(`--q-size-${name}`), 10);
				});
				this.setSizes = (sizes) => {
					SIZE_LIST.forEach((name) => {
						if (sizes[name]) this.sizes[name] = sizes[name];
					});
					this.__update(true);
				};
				this.setDebounce = (delay) => {
					if (updateEvt !== void 0) target.removeEventListener("resize", updateEvt, passive$4);
					updateEvt = delay > 0 ? debounce(this.__update, delay) : this.__update;
					target.addEventListener("resize", updateEvt, passive$4);
				};
				this.setDebounce(updateDebounce);
				if (Object.keys(updateSizes).length !== 0) {
					this.setSizes(updateSizes);
					updateSizes = void 0;
				} else this.__update();
				if (useBodyClasses && this.name === "xs") document.body.classList.add("screen--xs");
			};
			if (isRuntimeSsrPreHydration.value) onSSRHydrated.push(start);
			else start();
		}
	});
	//#endregion
	//#region src/plugins/dark/Dark.js
	const Plugin$9 = createReactivePlugin({
		isActive: false,
		mode: false
	}, {
		__media: void 0,
		set(val) {
			Plugin$9.mode = val;
			if (val === "auto") {
				if (Plugin$9.__media === void 0) {
					Plugin$9.__media = window.matchMedia("(prefers-color-scheme: dark)");
					Plugin$9.__updateMedia = () => {
						Plugin$9.set("auto");
					};
					Plugin$9.__media.addListener(Plugin$9.__updateMedia);
				}
				val = Plugin$9.__media.matches;
			} else if (Plugin$9.__media !== void 0) {
				Plugin$9.__media.removeListener(Plugin$9.__updateMedia);
				Plugin$9.__media = void 0;
			}
			Plugin$9.isActive = val === true;
			document.body.classList.remove(`body--${val === true ? "light" : "dark"}`);
			document.body.classList.add(`body--${val === true ? "dark" : "light"}`);
		},
		toggle() {
			Plugin$9.set(!Plugin$9.isActive);
		},
		install({ $q, ssrContext }) {
			const dark = $q.config.dark;
			$q.dark = this;
			if (!this.__installed) this.set(dark !== void 0 ? dark : false);
		}
	});
	//#endregion
	//#region src/utils/css-var/set-css-var.js
	function setCssVar(propName, value, element = document.body) {
		if (typeof propName !== "string") throw new TypeError("Expected a string as propName");
		if (typeof value !== "string") throw new TypeError("Expected a string as value");
		if (!(element instanceof Element)) throw new TypeError("Expected a DOM element");
		element.style.setProperty(`--q-${propName}`, value);
	}
	//#endregion
	//#region src/utils/private.keyboard/key-composition.js
	let lastKeyCompositionStatus = false;
	function onKeyDownComposition(evt) {
		lastKeyCompositionStatus = evt.isComposing === true;
	}
	function shouldIgnoreKey(evt) {
		return lastKeyCompositionStatus || evt !== Object(evt) || evt.isComposing || evt.qKeyEvent;
	}
	function isKeyCode(evt, keyCodes) {
		return !shouldIgnoreKey(evt) && [keyCodes].flat().includes(evt.keyCode);
	}
	//#endregion
	//#region src/plugins/private.body/Body.js
	function getMobilePlatform(is) {
		if (is.ios) return "ios";
		if (is.android) return "android";
	}
	function getBodyClasses({ is, has, within }, cfg) {
		const cls = [is.desktop ? "desktop" : "mobile", `${has.touch ? "" : "no-"}touch`];
		if (is.mobile) {
			const mobile = getMobilePlatform(is);
			if (mobile !== void 0) cls.push("platform-" + mobile);
		}
		if (is.nativeMobile) {
			const type = is.nativeMobileWrapper;
			cls.push(type, "native-mobile");
			if (is.ios && (cfg[type] === void 0 || cfg[type].iosStatusBarPadding)) cls.push("q-ios-padding");
		} else if (is.electron) cls.push("electron");
		else if (is.bex) cls.push("bex");
		if (within.iframe) cls.push("within-iframe");
		return cls;
	}
	function applyClientSsrCorrections() {
		const { is } = client;
		const classes = document.body.className;
		const classList = new Set(classes.replaceAll(/ {2}/g, " ").split(" "));
		if (!is.nativeMobile && !is.electron && !is.bex) {
			if (is.desktop) {
				classList.delete("mobile");
				classList.delete("platform-ios");
				classList.delete("platform-android");
				classList.add("desktop");
			} else if (is.mobile) {
				classList.delete("desktop");
				classList.add("mobile");
				classList.delete("platform-ios");
				classList.delete("platform-android");
				const mobile = getMobilePlatform(is);
				if (mobile !== void 0) classList.add(`platform-${mobile}`);
			}
		}
		if (client.has.touch) {
			classList.delete("no-touch");
			classList.add("touch");
		}
		if (client.within.iframe) classList.add("within-iframe");
		const newCls = [...classList].join(" ");
		if (classes !== newCls) document.body.className = newCls;
	}
	function setColors(brand) {
		for (const color in brand) setCssVar(color, brand[color]);
	}
	var Body_default = { install(opts) {
		if (this.__installed) return;
		if (isRuntimeSsrPreHydration.value) applyClientSsrCorrections();
		else {
			const { $q } = opts;
			if ($q.config.brand !== void 0) setColors($q.config.brand);
			document.body.classList.add(...getBodyClasses(client, $q.config));
		}
		if (client.is.ios) document.body.addEventListener("touchstart", noop);
		window.addEventListener("keydown", onKeyDownComposition, true);
	} };
	//#endregion
	//#region src/plugins/private.history/History.js
	const getTrue = () => true;
	function filterInvalidPath(path) {
		return typeof path === "string" && path !== "" && path !== "/" && path !== "#/";
	}
	function normalizeExitPath(path) {
		if (path.startsWith("#")) path = path.slice(1);
		if (!path.startsWith("/")) path = "/" + path;
		if (path.endsWith("/")) path = path.slice(0, -1);
		return "#" + path;
	}
	function getShouldExitFn(cfg) {
		if (cfg.backButtonExit === false) return () => false;
		if (cfg.backButtonExit === "*") return getTrue;
		const exitPaths = ["#/"];
		if (Array.isArray(cfg.backButtonExit)) exitPaths.push(...cfg.backButtonExit.filter(filterInvalidPath).map(normalizeExitPath));
		return () => exitPaths.includes(window.location.hash);
	}
	var History_default = {
		__history: [],
		add: noop,
		remove: noop,
		install({ $q }) {
			if (this.__installed) return;
			const { cordova, capacitor } = client.is;
			if (!cordova && !capacitor) return;
			const qConf = $q.config[cordova ? "cordova" : "capacitor"];
			if (qConf?.backButton === false) return;
			if (capacitor && (window.Capacitor === void 0 || window.Capacitor.Plugins.App === void 0)) return;
			this.add = (entry) => {
				if (entry.condition === void 0) entry.condition = getTrue;
				this.__history.push(entry);
			};
			this.remove = (entry) => {
				const index = this.__history.indexOf(entry);
				if (index !== -1) this.__history.splice(index, 1);
			};
			const shouldExit = getShouldExitFn({
				backButtonExit: true,
				...qConf
			});
			const backHandler = () => {
				if (this.__history.length !== 0) {
					const entry = this.__history.at(-1);
					if (entry.condition()) {
						this.__history.pop();
						entry.handler();
					}
				} else if (shouldExit()) navigator.app.exitApp();
				else window.history.back();
			};
			if (cordova) document.addEventListener("deviceready", () => {
				document.addEventListener("backbutton", backHandler, false);
			});
			else window.Capacitor.Plugins.App.addListener("backButton", backHandler);
		}
	};
	//#endregion
	//#region lang/en-US.js
	var en_US_default = {
		isoName: "en-US",
		nativeName: "English (US)",
		label: {
			clear: "Clear",
			ok: "OK",
			cancel: "Cancel",
			close: "Close",
			set: "Set",
			select: "Select",
			reset: "Reset",
			remove: "Remove",
			update: "Update",
			create: "Create",
			search: "Search",
			filter: "Filter",
			refresh: "Refresh",
			expand: (label) => label ? `Expand "${label}"` : "Expand",
			collapse: (label) => label ? `Collapse "${label}"` : "Collapse"
		},
		date: {
			days: "Sunday_Monday_Tuesday_Wednesday_Thursday_Friday_Saturday".split("_"),
			daysShort: "Sun_Mon_Tue_Wed_Thu_Fri_Sat".split("_"),
			months: "January_February_March_April_May_June_July_August_September_October_November_December".split("_"),
			monthsShort: "Jan_Feb_Mar_Apr_May_Jun_Jul_Aug_Sep_Oct_Nov_Dec".split("_"),
			firstDayOfWeek: 0,
			format24h: false,
			pluralDay: "days",
			prevMonth: "Previous month",
			nextMonth: "Next month",
			prevYear: "Previous year",
			nextYear: "Next year",
			today: "Today",
			prevRangeYears: (range) => `Previous ${range} years`,
			nextRangeYears: (range) => `Next ${range} years`
		},
		table: {
			noData: "No data available",
			noResults: "No matching records found",
			loading: "Loading...",
			selectedRecords: (rows) => rows === 1 ? "1 record selected." : (rows === 0 ? "No" : rows) + " records selected.",
			recordsPerPage: "Records per page:",
			allRows: "All",
			pagination: (start, end, total) => start + "–" + end + " of " + total,
			columns: "Columns"
		},
		pagination: {
			first: "First page",
			prev: "Previous page",
			next: "Next page",
			last: "Last page"
		},
		editor: {
			url: "URL",
			bold: "Bold",
			italic: "Italic",
			strikethrough: "Strikethrough",
			underline: "Underline",
			unorderedList: "Unordered List",
			orderedList: "Ordered List",
			subscript: "Subscript",
			superscript: "Superscript",
			hyperlink: "Hyperlink",
			toggleFullscreen: "Toggle Fullscreen",
			quote: "Quote",
			left: "Left align",
			center: "Center align",
			right: "Right align",
			justify: "Justify align",
			print: "Print",
			outdent: "Decrease indentation",
			indent: "Increase indentation",
			removeFormat: "Remove formatting",
			formatting: "Formatting",
			fontSize: "Font Size",
			align: "Align",
			hr: "Insert Horizontal Rule",
			undo: "Undo",
			redo: "Redo",
			heading1: "Heading 1",
			heading2: "Heading 2",
			heading3: "Heading 3",
			heading4: "Heading 4",
			heading5: "Heading 5",
			heading6: "Heading 6",
			paragraph: "Paragraph",
			code: "Code",
			size1: "Very small",
			size2: "A bit small",
			size3: "Normal",
			size4: "Medium-large",
			size5: "Big",
			size6: "Very big",
			size7: "Maximum",
			defaultFont: "Default Font",
			viewSource: "View Source"
		},
		tree: {
			noNodes: "No nodes available",
			noResults: "No matching nodes found"
		}
	};
	//#endregion
	//#region src/plugins/lang/Lang.js
	function getLocale() {
		const val = Array.isArray(navigator.languages) && navigator.languages.length !== 0 ? navigator.languages[0] : navigator.language;
		if (typeof val === "string") return val.split(/[-_]/).map((v, i) => i === 0 ? v.toLowerCase() : i > 1 || v.length < 4 ? v.toUpperCase() : v[0].toUpperCase() + v.slice(1).toLowerCase()).join("-");
	}
	const Plugin$8 = createReactivePlugin({ __qLang: {} }, {
		getLocale,
		set(langObject = en_US_default, ssrContext) {
			const lang = {
				...langObject,
				rtl: langObject.rtl === true,
				getLocale
			};
			lang.set = Plugin$8.set;
			if (Plugin$8.__langConfig === void 0 || !Plugin$8.__langConfig.noHtmlAttrs) {
				const el = document.documentElement;
				el.setAttribute("dir", lang.rtl ? "rtl" : "ltr");
				el.setAttribute("lang", lang.isoName);
			}
			Object.assign(Plugin$8.__qLang, lang);
		},
		install({ $q, lang, ssrContext }) {
			$q.lang = Plugin$8.__qLang;
			Plugin$8.__langConfig = $q.config.lang;
			if (this.__installed) {
				if (lang !== void 0) this.set(lang);
			} else {
				this.props = new Proxy(this.__qLang, {
					get: Reflect.get,
					ownKeys(target) {
						return Reflect.ownKeys(target).filter((key) => key !== "set" && key !== "getLocale");
					}
				});
				this.set(lang || en_US_default);
			}
		}
	});
	//#endregion
	//#region icon-set/material-icons.js
	var material_icons_default = {
		name: "material-icons",
		type: {
			positive: "check_circle",
			negative: "warning",
			info: "info",
			warning: "priority_high"
		},
		arrow: {
			up: "arrow_upward",
			right: "arrow_forward",
			down: "arrow_downward",
			left: "arrow_back",
			dropdown: "arrow_drop_down"
		},
		chevron: {
			left: "chevron_left",
			right: "chevron_right"
		},
		colorPicker: {
			spectrum: "gradient",
			tune: "tune",
			palette: "style"
		},
		pullToRefresh: { icon: "refresh" },
		carousel: {
			left: "chevron_left",
			right: "chevron_right",
			up: "keyboard_arrow_up",
			down: "keyboard_arrow_down",
			navigationIcon: "lens"
		},
		chip: {
			remove: "cancel",
			selected: "check"
		},
		datetime: {
			arrowLeft: "chevron_left",
			arrowRight: "chevron_right",
			now: "access_time",
			today: "today"
		},
		editor: {
			bold: "format_bold",
			italic: "format_italic",
			strikethrough: "strikethrough_s",
			underline: "format_underlined",
			unorderedList: "format_list_bulleted",
			orderedList: "format_list_numbered",
			subscript: "vertical_align_bottom",
			superscript: "vertical_align_top",
			hyperlink: "link",
			toggleFullscreen: "fullscreen",
			quote: "format_quote",
			left: "format_align_left",
			center: "format_align_center",
			right: "format_align_right",
			justify: "format_align_justify",
			print: "print",
			outdent: "format_indent_decrease",
			indent: "format_indent_increase",
			removeFormat: "format_clear",
			formatting: "text_format",
			fontSize: "format_size",
			align: "format_align_left",
			hr: "remove",
			undo: "undo",
			redo: "redo",
			heading: "format_size",
			code: "code",
			size: "format_size",
			font: "font_download",
			viewSource: "code"
		},
		expansionItem: {
			icon: "keyboard_arrow_down",
			denseIcon: "arrow_drop_down"
		},
		fab: {
			icon: "add",
			activeIcon: "close"
		},
		field: {
			clear: "cancel",
			error: "error"
		},
		pagination: {
			first: "first_page",
			prev: "keyboard_arrow_left",
			next: "keyboard_arrow_right",
			last: "last_page"
		},
		rating: { icon: "grade" },
		stepper: {
			done: "check",
			active: "edit",
			error: "warning"
		},
		tabs: {
			left: "chevron_left",
			right: "chevron_right",
			up: "keyboard_arrow_up",
			down: "keyboard_arrow_down"
		},
		table: {
			arrowUp: "arrow_upward",
			warning: "warning",
			firstPage: "first_page",
			prevPage: "chevron_left",
			nextPage: "chevron_right",
			lastPage: "last_page"
		},
		tree: { icon: "play_arrow" },
		uploader: {
			done: "done",
			clear: "clear",
			add: "add_box",
			upload: "cloud_upload",
			removeQueue: "clear_all",
			removeUploaded: "done_all"
		}
	};
	//#endregion
	//#region src/plugins/icon-set/IconSet.js
	const Plugin$7 = createReactivePlugin({
		iconMapFn: null,
		__qIconSet: {}
	}, {
		set(setObject, ssrContext) {
			const def = { ...setObject };
			def.set = Plugin$7.set;
			Object.assign(Plugin$7.__qIconSet, def);
		},
		install({ $q, iconSet, ssrContext }) {
			if ($q.config.iconMapFn !== void 0) this.iconMapFn = $q.config.iconMapFn;
			$q.iconSet = this.__qIconSet;
			injectProp($q, "iconMapFn", () => this.iconMapFn, (val) => {
				this.iconMapFn = val;
			});
			if (this.__installed) {
				if (iconSet !== void 0) this.set(iconSet);
			} else {
				this.props = new Proxy(this.__qIconSet, {
					get: Reflect.get,
					ownKeys(target) {
						return Reflect.ownKeys(target).filter((key) => key !== "set");
					}
				});
				this.set(iconSet || material_icons_default);
			}
		}
	});
	//#endregion
	//#region src/utils/private.symbols/symbols.js
	const timelineKey = "_q_t_";
	const stepperKey = "_q_s_";
	const layoutKey = "_q_l_";
	const pageContainerKey = "_q_pc_";
	const fabKey = "_q_f_";
	const formKey = "_q_fo_";
	const tabsKey = "_q_tabs_";
	const uploaderKey = "_q_u_";
	function emptyRenderFn() {}
	//#endregion
	//#region src/utils/is/is.js
	function isDeepEqual(a, b) {
		if (a === b) return true;
		if (a !== null && b !== null && typeof a === "object" && typeof b === "object") {
			if (a.constructor !== b.constructor) return false;
			let length, i;
			if (a.constructor === Array) {
				length = a.length;
				if (length !== b.length) return false;
				for (i = length; i-- !== 0;) if (!isDeepEqual(a[i], b[i])) return false;
				return true;
			}
			if (a.constructor === Map) {
				if (a.size !== b.size) return false;
				let iter = a.entries();
				i = iter.next();
				while (!i.done) {
					if (!b.has(i.value[0])) return false;
					i = iter.next();
				}
				iter = a.entries();
				i = iter.next();
				while (!i.done) {
					if (!isDeepEqual(i.value[1], b.get(i.value[0]))) return false;
					i = iter.next();
				}
				return true;
			}
			if (a.constructor === Set) {
				if (a.size !== b.size) return false;
				const iter = a.entries();
				i = iter.next();
				while (!i.done) {
					if (!b.has(i.value[0])) return false;
					i = iter.next();
				}
				return true;
			}
			if (a.buffer != null && a.buffer.constructor === ArrayBuffer) {
				length = a.length;
				if (length !== b.length) return false;
				for (i = length; i-- !== 0;) if (a[i] !== b[i]) return false;
				return true;
			}
			if (a.constructor === RegExp) return a.source === b.source && a.flags === b.flags;
			if (a.valueOf !== Object.prototype.valueOf) return a.valueOf() === b.valueOf();
			if (a.toString !== Object.prototype.toString) return a.toString() === b.toString();
			const keys = Object.keys(a).filter((key) => a[key] !== void 0);
			length = keys.length;
			if (length !== Object.keys(b).filter((key) => b[key] !== void 0).length) return false;
			for (i = length; i-- !== 0;) {
				const key = keys[i];
				if (!isDeepEqual(a[key], b[key])) return false;
			}
			return true;
		}
		return a !== a && b !== b;
	}
	function isObject(v) {
		return v !== null && typeof v === "object" && !Array.isArray(v);
	}
	function isDate(v) {
		return Object.prototype.toString.call(v) === "[object Date]";
	}
	function isRegexp(v) {
		return Object.prototype.toString.call(v) === "[object RegExp]";
	}
	function isNumber(v) {
		return typeof v === "number" && Number.isFinite(v);
	}
	var is_default = {
		deepEqual: isDeepEqual,
		object: isObject,
		date: isDate,
		regexp: isRegexp,
		number: isNumber
	};
	//#endregion
	//#region src/utils/private.config/instance-config.js
	const globalConfig = {};
	let globalConfigIsFrozen = false;
	function freezeGlobalConfig() {
		globalConfigIsFrozen = true;
	}
	//#endregion
	//#region src/install-quasar.js
	/**
	* If the list below changes, make sure
	* to also edit /ui/testing/specs/generators/generator.plugin.js
	* on the "autoInstalledPlugins" array
	*/
	const autoInstalledPlugins = [
		Platform,
		Body_default,
		Plugin$9,
		Screen_default,
		History_default,
		Plugin$8,
		Plugin$7
	];
	function createChildApp(appCfg, parentApp) {
		const app = (0, vue.createApp)(appCfg);
		app.config.globalProperties = parentApp.config.globalProperties;
		const { reload, ...appContext } = parentApp._context;
		Object.assign(app._context, appContext);
		return app;
	}
	function installPlugins(pluginOpts, pluginList) {
		pluginList.forEach((Plugin) => {
			Plugin.install(pluginOpts);
			Plugin.__installed = true;
		});
	}
	function prepareApp(app, uiOpts, pluginOpts) {
		app.config.globalProperties.$q = pluginOpts.$q;
		app.provide("_q_", pluginOpts.$q);
		installPlugins(pluginOpts, autoInstalledPlugins);
		if (uiOpts.components !== void 0) Object.values(uiOpts.components).forEach((c) => {
			if (isObject(c) && c.name !== void 0) app.component(c.name, c);
		});
		if (uiOpts.directives !== void 0) Object.values(uiOpts.directives).forEach((d) => {
			if (isObject(d) && d.name !== void 0) app.directive(d.name, d);
		});
		if (uiOpts.plugins !== void 0) installPlugins(pluginOpts, Object.values(uiOpts.plugins).filter((p) => typeof p.install === "function" && !autoInstalledPlugins.includes(p)));
		if (isRuntimeSsrPreHydration.value) pluginOpts.$q.onSSRHydrated = () => {
			pluginOpts.onSSRHydrated.forEach((fn) => {
				fn();
			});
			pluginOpts.$q.onSSRHydrated = () => {};
		};
	}
	var install_quasar_default = function installQuasar(parentApp, opts = {}) {
		const $q = { version: "2.22.0" };
		if (!globalConfigIsFrozen) {
			if (opts.config !== void 0) Object.assign(globalConfig, opts.config);
			$q.config = { ...globalConfig };
			freezeGlobalConfig();
		} else $q.config = opts.config || {};
		prepareApp(parentApp, opts, {
			parentApp,
			$q,
			lang: opts.lang,
			iconSet: opts.iconSet,
			onSSRHydrated: []
		});
	};
	//#endregion
	//#region src/utils/format/format.js
	const units = [
		"B",
		"KB",
		"MB",
		"GB",
		"TB",
		"PB"
	];
	function humanStorageSize(bytes, decimals = 1) {
		let u = 0;
		while (Number.parseInt(bytes, 10) >= 1024 && u < units.length - 1) {
			bytes /= 1024;
			++u;
		}
		return `${bytes.toFixed(decimals)}${units[u]}`;
	}
	function capitalize(str) {
		return str.at(0).toUpperCase() + str.slice(1);
	}
	function between(v, min, max) {
		return max <= min ? min : Math.min(max, Math.max(min, v));
	}
	function normalizeToInterval(v, min, max) {
		if (max <= min) return min;
		const size = max - min + 1;
		let index = min + (v - min) % size;
		if (index < min) index = size + index;
		return index === 0 ? 0 : index;
	}
	function pad(v, length = 2, char = "0") {
		if (v === void 0 || v === null) return v;
		return String(v).padStart(length, char);
	}
	var format_default = {
		humanStorageSize,
		capitalize,
		between,
		normalizeToInterval,
		pad
	};
	//#endregion
	//#region src/components/ajax-bar/QAjaxBar.js
	const xhr = XMLHttpRequest;
	const open = xhr.prototype.open;
	const positionValues = [
		"top",
		"right",
		"bottom",
		"left"
	];
	let stack = [];
	let highjackCount = 0;
	function translate({ p, pos, active, horiz, reverse, dir }) {
		let x = 1, y = 1;
		if (horiz) {
			if (reverse) x = -1;
			if (pos === "bottom") y = -1;
			return { transform: `translate3d(${x * (p - 100)}%,${active ? 0 : y * -200}%,0)` };
		}
		if (reverse) y = -1;
		if (pos === "right") x = -1;
		return { transform: `translate3d(${active ? 0 : dir * x * -200}%,${y * (p - 100)}%,0)` };
	}
	function inc(p, amount) {
		if (typeof amount !== "number") if (p < 25) amount = Math.random() * 3 + 3;
		else if (p < 65) amount = Math.random() * 3;
		else if (p < 85) amount = Math.random() * 2;
		else if (p < 99) amount = .6;
		else amount = 0;
		return between(p + amount, 0, 100);
	}
	function highjackAjax(stackEntry) {
		highjackCount++;
		stack.push(stackEntry);
		if (highjackCount > 1) return;
		xhr.prototype.open = function qOpen(method, url, ...restArgs) {
			const stopStack = [];
			const loadStart = () => {
				stack.forEach((entry) => {
					if (entry.hijackFilter.value === null || entry.hijackFilter.value(url)) {
						entry.start();
						stopStack.push(entry.stop);
					}
				});
			};
			const loadEnd = () => {
				stopStack.forEach((stop) => {
					stop();
				});
			};
			this.addEventListener("loadstart", loadStart, { once: true });
			this.addEventListener("loadend", loadEnd, { once: true });
			open.call(this, method, url, ...restArgs);
		};
	}
	function restoreAjax(start) {
		stack = stack.filter((entry) => entry.start !== start);
		highjackCount = Math.max(0, highjackCount - 1);
		if (highjackCount === 0) xhr.prototype.open = open;
	}
	var QAjaxBar_default = createComponent({
		name: "QAjaxBar",
		props: {
			position: {
				type: String,
				default: "top",
				validator: (val) => positionValues.includes(val)
			},
			size: {
				type: String,
				default: "2px"
			},
			color: String,
			skipHijack: Boolean,
			reverse: Boolean,
			hijackFilter: Function
		},
		emits: ["start", "stop"],
		setup(props, { emit }) {
			const { proxy } = (0, vue.getCurrentInstance)();
			const progress = (0, vue.ref)(0);
			const onScreen = (0, vue.ref)(false);
			const animate = (0, vue.ref)(true);
			let sessions = 0, timer = null, speed;
			const classes = (0, vue.computed)(() => `q-loading-bar q-loading-bar--${props.position}` + (props.color !== void 0 ? ` bg-${props.color}` : "") + (animate.value ? "" : " no-transition"));
			const horizontal = (0, vue.computed)(() => props.position === "top" || props.position === "bottom");
			const sizeProp = (0, vue.computed)(() => horizontal.value ? "height" : "width");
			const style = (0, vue.computed)(() => {
				const active = onScreen.value;
				const obj = translate({
					p: progress.value,
					pos: props.position,
					active,
					horiz: horizontal.value,
					reverse: proxy.$q.lang.rtl && ["top", "bottom"].includes(props.position) ? !props.reverse : props.reverse,
					dir: proxy.$q.lang.rtl ? -1 : 1
				});
				obj[sizeProp.value] = props.size;
				obj.opacity = active ? 1 : 0;
				return obj;
			});
			const attributes = (0, vue.computed)(() => onScreen.value ? {
				role: "progressbar",
				"aria-valuemin": 0,
				"aria-valuemax": 100,
				"aria-valuenow": progress.value
			} : { "aria-hidden": "true" });
			function start(newSpeed = 300) {
				const oldSpeed = speed;
				speed = Math.max(0, newSpeed) || 0;
				sessions++;
				if (sessions > 1) {
					if (oldSpeed === 0 && newSpeed > 0) planNextStep();
					else if (timer !== null && oldSpeed > 0 && newSpeed <= 0) {
						clearTimeout(timer);
						timer = null;
					}
					return sessions;
				}
				if (timer !== null) clearTimeout(timer);
				emit("start");
				progress.value = 0;
				/**
				* We're trying to avoid side effects if start() is called inside a watchEffect()
				* so we're accessing the _value property directly (under the covers implementation detail of ref())
				*
				* Otherwise, any refs() accessed here would be marked as deps for the watchEffect()
				* -- and we are changing them below, which would cause an infinite loop
				*/
				timer = setTimeout(() => {
					timer = null;
					animate.value = true;
					if (newSpeed > 0) planNextStep();
				}, onScreen._value === true ? 500 : 1);
				if (onScreen._value !== true) {
					onScreen.value = true;
					animate.value = false;
				}
				return sessions;
			}
			function increment(amount) {
				if (sessions > 0) progress.value = inc(progress.value, amount);
				return sessions;
			}
			function stop() {
				sessions = Math.max(0, sessions - 1);
				if (sessions > 0) return sessions;
				if (timer !== null) {
					clearTimeout(timer);
					timer = null;
				}
				emit("stop");
				const end = () => {
					animate.value = true;
					progress.value = 100;
					timer = setTimeout(() => {
						timer = null;
						onScreen.value = false;
					}, 1e3);
				};
				if (progress.value === 0) timer = setTimeout(end, 1);
				else end();
				return sessions;
			}
			function planNextStep() {
				if (progress.value < 100) timer = setTimeout(() => {
					timer = null;
					increment();
					planNextStep();
				}, speed);
			}
			let hijacked = false;
			(0, vue.onMounted)(() => {
				if (!props.skipHijack) {
					hijacked = true;
					highjackAjax({
						start,
						stop,
						hijackFilter: (0, vue.computed)(() => props.hijackFilter || null)
					});
				}
			});
			(0, vue.onBeforeUnmount)(() => {
				if (timer !== null) clearTimeout(timer);
				if (hijacked) restoreAjax(start);
			});
			Object.assign(proxy, {
				start,
				stop,
				increment
			});
			return () => (0, vue.h)("div", {
				class: classes.value,
				style: style.value,
				...attributes.value
			});
		}
	});
	//#endregion
	//#region src/composables/private.use-size/use-size.js
	const useSizeDefaults = {
		xs: 18,
		sm: 24,
		md: 32,
		lg: 38,
		xl: 46
	};
	const useSizeProps = { size: String };
	function useSize(props, sizes = useSizeDefaults) {
		return (0, vue.computed)(() => props.size !== void 0 ? { fontSize: props.size in sizes ? `${sizes[props.size]}px` : props.size } : null);
	}
	//#endregion
	//#region src/utils/private.render/render.js
	function hSlot(slot, otherwise) {
		return slot !== void 0 ? slot() || otherwise : otherwise;
	}
	function hUniqueSlot(slot, otherwise) {
		if (slot !== void 0) {
			const vnode = slot();
			if (vnode !== void 0 && vnode !== null) return [...vnode];
		}
		return otherwise;
	}
	/**
	* Source definitely exists,
	* so it's merged with the possible slot
	*/
	function hMergeSlot(slot, source) {
		return slot !== void 0 ? source.concat(slot()) : source;
	}
	/**
	* Merge with possible slot,
	* even if source might not exist
	*/
	function hMergeSlotSafely(slot, source) {
		if (slot === void 0) return source;
		return source !== void 0 ? source.concat(slot()) : slot();
	}
	function hDir(tag, data, children, key, condition, getDirsFn) {
		data.key = key + condition;
		const vnode = (0, vue.h)(tag, data, children);
		return condition ? (0, vue.withDirectives)(vnode, getDirsFn()) : vnode;
	}
	//#endregion
	//#region src/components/icon/QIcon.js
	const defaultViewBox = "0 0 24 24";
	const sameFn = (i) => i;
	const ionFn = (i) => `ionicons ${i}`;
	const libMap = {
		"mdi-": (i) => `mdi ${i}`,
		"icon-": sameFn,
		"bt-": (i) => `bt ${i}`,
		"eva-": (i) => `eva ${i}`,
		"ion-md": ionFn,
		"ion-ios": ionFn,
		"ion-logo": ionFn,
		"iconfont ": sameFn,
		"ti-": (i) => `themify-icon ${i}`,
		"bi-": (i) => `bootstrap-icons ${i}`,
		"i-": sameFn
	};
	const matMap = {
		o_: "-outlined",
		r_: "-round",
		s_: "-sharp"
	};
	const symMap = {
		sym_o_: "-outlined",
		sym_r_: "-rounded",
		sym_s_: "-sharp"
	};
	const libRE = new RegExp("^(" + Object.keys(libMap).join("|") + ")");
	const matRE = new RegExp("^(" + Object.keys(matMap).join("|") + ")");
	const symRE = new RegExp("^(" + Object.keys(symMap).join("|") + ")");
	const mRE = /^[Mm]\s?[-+]?\.?\d/;
	const imgRE = /^img:/;
	const svgUseRE = /^svguse:/;
	const ionRE = /^ion-/;
	const faRE = /^(fa-(classic|sharp|solid|regular|light|brands|duotone|thin)|[lf]a[srlbdk]?) /;
	var QIcon_default = createComponent({
		name: "QIcon",
		props: {
			...useSizeProps,
			tag: {
				type: String,
				default: "i"
			},
			name: String,
			color: String,
			left: Boolean,
			right: Boolean
		},
		setup(props, { slots }) {
			const { proxy: { $q } } = (0, vue.getCurrentInstance)();
			const sizeStyle = useSize(props);
			const classes = (0, vue.computed)(() => "q-icon" + (props.left ? " on-left" : "") + (props.right ? " on-right" : "") + (props.color !== void 0 ? ` text-${props.color}` : ""));
			const type = (0, vue.computed)(() => {
				let cls;
				let icon = props.name;
				if (icon === "none" || !icon) return { none: true };
				if ($q.iconMapFn !== null) {
					const res = $q.iconMapFn(icon);
					if (res !== void 0) if (res.icon !== void 0) {
						icon = res.icon;
						if (icon === "none" || !icon) return { none: true };
					} else return {
						cls: res.cls,
						content: res.content !== void 0 ? res.content : " "
					};
				}
				if (mRE.test(icon)) {
					const [def, viewBox = defaultViewBox] = icon.split("|");
					return {
						svg: true,
						viewBox,
						nodes: def.split("&&").map((path) => {
							const [d, style, transform] = path.split("@@");
							return (0, vue.h)("path", {
								style,
								d,
								transform
							});
						})
					};
				}
				if (imgRE.test(icon)) return {
					img: true,
					src: icon.slice(4)
				};
				if (svgUseRE.test(icon)) {
					const [def, viewBox = defaultViewBox] = icon.split("|");
					return {
						svguse: true,
						src: def.slice(7),
						viewBox
					};
				}
				let content = " ";
				const matches = icon.match(libRE);
				if (matches !== null) cls = libMap[matches[1]](icon);
				else if (faRE.test(icon)) cls = icon;
				else if (ionRE.test(icon)) cls = `ionicons ion-${$q.platform.is.ios ? "ios" : "md"}${icon.slice(3)}`;
				else if (symRE.test(icon)) {
					cls = "notranslate material-symbols";
					const symMatches = icon.match(symRE);
					if (symMatches !== null) {
						icon = icon.slice(6);
						cls += symMap[symMatches[1]];
					}
					content = icon;
				} else {
					cls = "notranslate material-icons";
					const matMatches = icon.match(matRE);
					if (matMatches !== null) {
						icon = icon.slice(2);
						cls += matMap[matMatches[1]];
					}
					content = icon;
				}
				return {
					cls,
					content
				};
			});
			return () => {
				const data = {
					class: classes.value,
					style: sizeStyle.value,
					"aria-hidden": "true"
				};
				if (type.value.none) return (0, vue.h)(props.tag, data, hSlot(slots.default));
				if (type.value.img) return (0, vue.h)(props.tag, data, hMergeSlot(slots.default, [(0, vue.h)("img", { src: type.value.src })]));
				if (type.value.svg) return (0, vue.h)(props.tag, data, hMergeSlot(slots.default, [(0, vue.h)("svg", { viewBox: type.value.viewBox || "0 0 24 24" }, type.value.nodes)]));
				if (type.value.svguse) return (0, vue.h)(props.tag, data, hMergeSlot(slots.default, [(0, vue.h)("svg", { viewBox: type.value.viewBox }, [(0, vue.h)("use", { "xlink:href": type.value.src })])]));
				if (type.value.cls !== void 0) data.class += " " + type.value.cls;
				return (0, vue.h)(props.tag, data, hMergeSlot(slots.default, [type.value.content]));
			};
		}
	});
	//#endregion
	//#region src/components/avatar/QAvatar.js
	var QAvatar_default = createComponent({
		name: "QAvatar",
		props: {
			...useSizeProps,
			fontSize: String,
			color: String,
			textColor: String,
			icon: String,
			square: Boolean,
			rounded: Boolean
		},
		setup(props, { slots }) {
			const sizeStyle = useSize(props);
			const classes = (0, vue.computed)(() => "q-avatar" + (props.color ? ` bg-${props.color}` : "") + (props.textColor ? ` text-${props.textColor} q-chip--colored` : "") + (props.square ? " q-avatar--square" : props.rounded ? " rounded-borders" : ""));
			const contentStyle = (0, vue.computed)(() => props.fontSize ? { fontSize: props.fontSize } : null);
			return () => {
				const icon = props.icon !== void 0 ? [(0, vue.h)(QIcon_default, { name: props.icon })] : void 0;
				return (0, vue.h)("div", {
					class: classes.value,
					style: sizeStyle.value
				}, [(0, vue.h)("div", {
					class: "q-avatar__content row flex-center overflow-hidden",
					style: contentStyle.value
				}, hMergeSlotSafely(slots.default, icon))]);
			};
		}
	});
	//#endregion
	//#region src/components/badge/QBadge.js
	const alignValues$3 = [
		"top",
		"middle",
		"bottom"
	];
	var QBadge_default = createComponent({
		name: "QBadge",
		props: {
			color: String,
			textColor: String,
			floating: Boolean,
			transparent: Boolean,
			multiLine: Boolean,
			outline: Boolean,
			rounded: Boolean,
			label: [Number, String],
			align: {
				type: String,
				validator: (v) => alignValues$3.includes(v)
			}
		},
		setup(props, { slots }) {
			const style = (0, vue.computed)(() => props.align !== void 0 ? { verticalAlign: props.align } : null);
			const classes = (0, vue.computed)(() => {
				const text = props.outline ? props.color || props.textColor : props.textColor;
				return `q-badge flex inline items-center no-wrap q-badge--${props.multiLine ? "multi" : "single"}-line` + (props.outline ? " q-badge--outline" : props.color !== void 0 ? ` bg-${props.color}` : "") + (text !== void 0 ? ` text-${text}` : "") + (props.floating ? " q-badge--floating" : "") + (props.rounded ? " q-badge--rounded" : "") + (props.transparent ? " q-badge--transparent" : "");
			});
			return () => (0, vue.h)("div", {
				class: classes.value,
				style: style.value,
				role: "status",
				"aria-label": props.label
			}, hMergeSlot(slots.default, props.label !== void 0 ? [props.label] : []));
		}
	});
	//#endregion
	//#region src/composables/private.use-dark/use-dark.js
	const useDarkProps = { dark: {
		type: Boolean,
		default: null
	} };
	function useDark(props, $q) {
		return (0, vue.computed)(() => props.dark === null ? $q.dark.isActive : props.dark);
	}
	//#endregion
	//#region src/components/banner/QBanner.js
	var QBanner_default = createComponent({
		name: "QBanner",
		props: {
			...useDarkProps,
			inlineActions: Boolean,
			dense: Boolean,
			rounded: Boolean
		},
		setup(props, { slots }) {
			const { proxy: { $q } } = (0, vue.getCurrentInstance)();
			const isDark = useDark(props, $q);
			const classes = (0, vue.computed)(() => "q-banner row items-center" + (props.dense ? " q-banner--dense" : "") + (isDark.value ? " q-banner--dark q-dark" : "") + (props.rounded ? " rounded-borders" : ""));
			const actionClass = (0, vue.computed)(() => `q-banner__actions row items-center justify-end col-${props.inlineActions ? "auto" : "all"}`);
			return () => {
				const child = [(0, vue.h)("div", { class: "q-banner__avatar col-auto row items-center self-start" }, hSlot(slots.avatar)), (0, vue.h)("div", { class: "q-banner__content col text-body2" }, hSlot(slots.default))];
				const actions = hSlot(slots.action);
				if (actions !== void 0) child.push((0, vue.h)("div", { class: actionClass.value }, actions));
				return (0, vue.h)("div", {
					class: classes.value + (!props.inlineActions && actions !== void 0 ? " q-banner--top-padding" : ""),
					role: "alert"
				}, child);
			};
		}
	});
	//#endregion
	//#region src/components/bar/QBar.js
	var QBar_default = createComponent({
		name: "QBar",
		props: {
			...useDarkProps,
			dense: Boolean
		},
		setup(props, { slots }) {
			const { proxy: { $q } } = (0, vue.getCurrentInstance)();
			const isDark = useDark(props, $q);
			const classes = (0, vue.computed)(() => `q-bar row no-wrap items-center q-bar--${props.dense ? "dense" : "standard"}  q-bar--${isDark.value ? "dark" : "light"}`);
			return () => (0, vue.h)("div", {
				class: classes.value,
				role: "toolbar"
			}, hSlot(slots.default));
		}
	});
	//#endregion
	//#region src/composables/private.use-align/use-align.js
	const alignMap = {
		left: "start",
		center: "center",
		right: "end",
		between: "between",
		around: "around",
		evenly: "evenly",
		stretch: "stretch"
	};
	const alignValues$2 = Object.keys(alignMap);
	const useAlignProps = { align: {
		type: String,
		validator: (v) => alignValues$2.includes(v)
	} };
	function useAlign(props) {
		return (0, vue.computed)(() => {
			const align = props.align === void 0 ? props.vertical ? "stretch" : "left" : props.align;
			return `${props.vertical ? "items" : "justify"}-${alignMap[align]}`;
		});
	}
	//#endregion
	//#region src/utils/private.vm/vm.js
	function getParentProxy(proxy) {
		if (Object(proxy.$parent) === proxy.$parent) return proxy.$parent;
		let { parent } = proxy.$;
		while (Object(parent) === parent) {
			if (Object(parent.proxy) === parent.proxy) return parent.proxy;
			parent = parent.parent;
		}
	}
	function fillNormalizedVNodes(children, vnode) {
		if (typeof vnode.type === "symbol") {
			if (Array.isArray(vnode.children)) vnode.children.forEach((child) => {
				fillNormalizedVNodes(children, child);
			});
		} else children.add(vnode);
	}
	function getNormalizedVNodes(vnodes) {
		const children = /* @__PURE__ */ new Set();
		vnodes.forEach((vnode) => {
			fillNormalizedVNodes(children, vnode);
		});
		return [...children];
	}
	function vmHasRouter(vm) {
		return vm.appContext.config.globalProperties.$router !== void 0;
	}
	function vmIsDestroyed(vm) {
		return vm.isUnmounted === true || vm.isDeactivated === true;
	}
	//#endregion
	//#region src/components/breadcrumbs/QBreadcrumbs.js
	const disabledValues = ["", true];
	var QBreadcrumbs_default = createComponent({
		name: "QBreadcrumbs",
		props: {
			...useAlignProps,
			separator: {
				type: String,
				default: "/"
			},
			separatorColor: String,
			activeColor: {
				type: String,
				default: "primary"
			},
			gutter: {
				type: String,
				validator: (v) => [
					"none",
					"xs",
					"sm",
					"md",
					"lg",
					"xl"
				].includes(v),
				default: "sm"
			}
		},
		setup(props, { slots }) {
			const alignClass = useAlign(props);
			const classes = (0, vue.computed)(() => `flex items-center ${alignClass.value}${props.gutter === "none" ? "" : ` q-gutter-${props.gutter}`}`);
			const sepClass = (0, vue.computed)(() => props.separatorColor ? ` text-${props.separatorColor}` : "");
			const activeClass = (0, vue.computed)(() => ` text-${props.activeColor}`);
			return () => {
				if (slots.default === void 0) return;
				const vnodes = getNormalizedVNodes(hSlot(slots.default));
				if (vnodes.length === 0) return;
				let els = 1;
				const child = [], len = vnodes.filter((c) => c.type?.name === "QBreadcrumbsEl").length, separator = slots.separator !== void 0 ? slots.separator : () => props.separator;
				vnodes.forEach((comp) => {
					if (comp.type?.name === "QBreadcrumbsEl") {
						const middle = els < len;
						const disabled = comp.props !== null && disabledValues.includes(comp.props.disable);
						const cls = (middle ? "" : " q-breadcrumbs--last") + (!disabled && middle ? activeClass.value : "");
						els++;
						child.push((0, vue.h)("div", { class: `flex items-center${cls}` }, [comp]));
						if (middle) child.push((0, vue.h)("div", { class: "q-breadcrumbs__separator" + sepClass.value }, separator()));
					} else child.push(comp);
				});
				return (0, vue.h)("div", { class: "q-breadcrumbs" }, [(0, vue.h)("div", { class: classes.value }, child)]);
			};
		}
	});
	//#endregion
	//#region src/composables/private.use-router-link/use-router-link.js
	function getOriginalPath(record) {
		return record ? record.aliasOf ? record.aliasOf.path : record.path : "";
	}
	function isSameRouteRecord(a, b) {
		return (a.aliasOf || a) === (b.aliasOf || b);
	}
	function includesParams(outer, inner) {
		for (const key in inner) {
			const innerValue = inner[key], outerValue = outer[key];
			if (typeof innerValue === "string") {
				if (innerValue !== outerValue) return false;
			} else if (!Array.isArray(outerValue) || outerValue.length !== innerValue.length || innerValue.some((value, i) => value !== outerValue[i])) return false;
		}
		return true;
	}
	function isEquivalentArray(a, b) {
		return Array.isArray(b) ? a.length === b.length && a.every((value, i) => value === b[i]) : a.length === 1 && a[0] === b;
	}
	function isSameRouteLocationParamsValue(a, b) {
		return Array.isArray(a) ? isEquivalentArray(a, b) : Array.isArray(b) ? isEquivalentArray(b, a) : a === b;
	}
	function isSameRouteLocationParams(a, b) {
		if (Object.keys(a).length !== Object.keys(b).length) return false;
		for (const key in a) if (!isSameRouteLocationParamsValue(a[key], b[key])) return false;
		return true;
	}
	const useRouterLinkNonMatchingProps = {
		to: [String, Object],
		replace: Boolean,
		href: String,
		target: String,
		disable: Boolean
	};
	const useRouterLinkProps = {
		...useRouterLinkNonMatchingProps,
		exact: Boolean,
		activeClass: {
			type: String,
			default: "q-router-link--active"
		},
		exactActiveClass: {
			type: String,
			default: "q-router-link--exact-active"
		}
	};
	function useRouterLink({ fallbackTag, useDisableForRouterLinkProps = true } = {}) {
		const vm = (0, vue.getCurrentInstance)();
		const { props, proxy, emit } = vm;
		const hasRouter = vmHasRouter(vm);
		const hasHrefLink = (0, vue.computed)(() => !props.disable && props.href !== void 0);
		const hasRouterLinkProps = useDisableForRouterLinkProps ? (0, vue.computed)(() => hasRouter && !props.disable && !hasHrefLink.value && props.to !== void 0 && props.to !== null && props.to !== "") : (0, vue.computed)(() => hasRouter && !hasHrefLink.value && props.to !== void 0 && props.to !== null && props.to !== "");
		const resolvedLink = (0, vue.computed)(() => hasRouterLinkProps.value ? getLink(props.to) : null);
		const hasRouterLink = (0, vue.computed)(() => resolvedLink.value !== null);
		const hasLink = (0, vue.computed)(() => hasHrefLink.value || hasRouterLink.value);
		const linkTag = (0, vue.computed)(() => props.type === "a" || hasLink.value ? "a" : props.tag || fallbackTag || "div");
		const linkAttrs = (0, vue.computed)(() => hasHrefLink.value ? {
			href: props.href,
			target: props.target
		} : hasRouterLink.value ? {
			href: resolvedLink.value.href,
			target: props.target
		} : {});
		const linkActiveIndex = (0, vue.computed)(() => {
			if (!hasRouterLink.value) return -1;
			const { matched } = resolvedLink.value, { length } = matched, routeMatched = matched[length - 1];
			if (routeMatched === void 0) return -1;
			const currentMatched = proxy.$route.matched;
			if (currentMatched.length === 0) return -1;
			const index = currentMatched.findIndex(isSameRouteRecord.bind(null, routeMatched));
			if (index !== -1) return index;
			const parentRecordPath = getOriginalPath(matched[length - 2]);
			return length > 1 && getOriginalPath(routeMatched) === parentRecordPath && currentMatched.at(-1).path !== parentRecordPath ? currentMatched.findIndex(isSameRouteRecord.bind(null, matched[length - 2])) : index;
		});
		const linkIsActive = (0, vue.computed)(() => hasRouterLink.value && linkActiveIndex.value !== -1 && includesParams(proxy.$route.params, resolvedLink.value.params));
		const linkIsExactActive = (0, vue.computed)(() => linkIsActive.value && linkActiveIndex.value === proxy.$route.matched.length - 1 && isSameRouteLocationParams(proxy.$route.params, resolvedLink.value.params));
		const linkClass = (0, vue.computed)(() => hasRouterLink.value ? linkIsExactActive.value ? ` ${props.exactActiveClass} ${props.activeClass}` : props.exact ? "" : linkIsActive.value ? ` ${props.activeClass}` : "" : "");
		function getLink(to) {
			try {
				return proxy.$router.resolve(to);
			} catch {}
			return null;
		}
		/**
		* @returns Promise<RouterError | false | undefined>
		*/
		function navigateToRouterLink(e, { returnRouterError, to = props.to, replace = props.replace } = {}) {
			if (props.disable) {
				e.preventDefault();
				return Promise.resolve(false);
			}
			if (e.metaKey || e.altKey || e.ctrlKey || e.shiftKey || e.button !== void 0 && e.button !== 0 || props.target === "_blank") return Promise.resolve(false);
			e.preventDefault();
			const promise = proxy.$router[replace ? "replace" : "push"](to);
			return returnRouterError ? promise : promise.then(() => {}).catch(() => {});
		}
		function navigateOnClick(e) {
			if (hasRouterLink.value) {
				const go = (opts) => navigateToRouterLink(e, opts);
				emit("click", e, go);
				if (!e.defaultPrevented) go();
			} else emit("click", e);
		}
		return {
			hasRouterLink,
			hasHrefLink,
			hasLink,
			linkTag,
			resolvedLink,
			linkIsActive,
			linkIsExactActive,
			linkClass,
			linkAttrs,
			getLink,
			navigateToRouterLink,
			navigateOnClick
		};
	}
	//#endregion
	//#region src/components/breadcrumbs/QBreadcrumbsEl.js
	var QBreadcrumbsEl_default = createComponent({
		name: "QBreadcrumbsEl",
		props: {
			...useRouterLinkProps,
			label: String,
			icon: String,
			tag: {
				type: String,
				default: "span"
			}
		},
		emits: ["click"],
		setup(props, { slots }) {
			const { linkTag, linkAttrs, linkClass, navigateOnClick } = useRouterLink();
			const data = (0, vue.computed)(() => ({
				class: "q-breadcrumbs__el q-link flex inline items-center relative-position " + (props.disable ? "q-breadcrumbs__el--disable" : "q-link--focusable" + linkClass.value),
				...linkAttrs.value,
				onClick: navigateOnClick
			}));
			const iconClass = (0, vue.computed)(() => "q-breadcrumbs__el-icon" + (props.label !== void 0 ? " q-breadcrumbs__el-icon--with-label" : ""));
			return () => {
				const child = [];
				if (props.icon !== void 0) child.push((0, vue.h)(QIcon_default, {
					class: iconClass.value,
					name: props.icon
				}));
				if (props.label !== void 0) child.push(props.label);
				return (0, vue.h)(linkTag.value, { ...data.value }, hMergeSlot(slots.default, child));
			};
		}
	});
	//#endregion
	//#region src/components/spinner/use-spinner.js
	const useSpinnerProps = {
		size: {
			type: [String, Number],
			default: "1em"
		},
		color: String
	};
	function useSpinner(props) {
		return {
			cSize: (0, vue.computed)(() => props.size in useSizeDefaults ? `${useSizeDefaults[props.size]}px` : props.size),
			classes: (0, vue.computed)(() => "q-spinner" + (props.color ? ` text-${props.color}` : ""))
		};
	}
	//#endregion
	//#region src/components/spinner/QSpinner.js
	var QSpinner_default = createComponent({
		name: "QSpinner",
		props: {
			...useSpinnerProps,
			thickness: {
				type: Number,
				default: 5
			}
		},
		setup(props) {
			const { cSize, classes } = useSpinner(props);
			return () => (0, vue.h)("svg", {
				class: classes.value + " q-spinner-mat",
				width: cSize.value,
				height: cSize.value,
				viewBox: "25 25 50 50"
			}, [(0, vue.h)("circle", {
				class: "path",
				cx: "50",
				cy: "50",
				r: "20",
				fill: "none",
				stroke: "currentColor",
				"stroke-width": props.thickness,
				"stroke-miterlimit": "10"
			})]);
		}
	});
	//#endregion
	//#region src/utils/dom/dom.js
	function offset(el) {
		if (el === window) return {
			top: 0,
			left: 0
		};
		const { top, left } = el.getBoundingClientRect();
		return {
			top,
			left
		};
	}
	function style(el, property) {
		return window.getComputedStyle(el).getPropertyValue(property);
	}
	function height(el) {
		return el === window ? window.innerHeight : el.getBoundingClientRect().height;
	}
	function width$1(el) {
		return el === window ? window.innerWidth : el.getBoundingClientRect().width;
	}
	function css(element, cssObject) {
		const elementStyle = element.style;
		for (const prop in cssObject) elementStyle[prop] = cssObject[prop];
	}
	function cssBatch(elements, elementCssObject) {
		elements.forEach((el) => css(el, elementCssObject));
	}
	function ready(fn) {
		if (typeof fn !== "function") return;
		if (document.readyState !== "loading") return fn();
		document.addEventListener("DOMContentLoaded", fn, false);
	}
	function getElement$1(el) {
		if (el === void 0 || el === null) return;
		if (typeof el === "string") try {
			return document.querySelector(el) || void 0;
		} catch {
			return;
		}
		const target = (0, vue.unref)(el);
		if (target) return target.$el || target;
	}
	function childHasFocus(el, focusedEl) {
		if (el === void 0 || el === null || el.contains(focusedEl)) return true;
		for (let next = el.nextElementSibling; next !== null; next = next.nextElementSibling) if (next.contains(focusedEl)) return true;
		return false;
	}
	var dom_default = {
		offset,
		style,
		height,
		width: width$1,
		css,
		cssBatch,
		ready
	};
	//#endregion
	//#region src/utils/throttle/throttle.js
	function throttle(fn, limit = 250) {
		let wait = false, result;
		return function runThrottle(...args) {
			if (!wait) {
				wait = true;
				setTimeout(() => {
					wait = false;
				}, limit);
				result = fn.apply(this, args);
			}
			return result;
		};
	}
	//#endregion
	//#region src/directives/ripple/Ripple.js
	function showRipple(evt, el, ctx, forceCenter) {
		if (ctx.modifiers.stop) stop(evt);
		const color = ctx.modifiers.color, center = ctx.modifiers.center || forceCenter === true, node = document.createElement("span"), innerNode = document.createElement("span"), pos = position(evt), { left, top, width, height } = el.getBoundingClientRect(), diameter = Math.hypot(width, height), radius = diameter / 2, centerX = `${(width - diameter) / 2}px`, x = center ? centerX : `${pos.left - left - radius}px`, centerY = `${(height - diameter) / 2}px`, y = center ? centerY : `${pos.top - top - radius}px`;
		innerNode.className = "q-ripple__inner";
		css(innerNode, {
			height: `${diameter}px`,
			width: `${diameter}px`,
			transform: `translate3d(${x},${y},0) scale3d(.2,.2,1)`,
			opacity: 0
		});
		node.className = `q-ripple${color ? " text-" + color : ""}`;
		node.setAttribute("dir", "ltr");
		node.append(innerNode);
		el.append(node);
		const abort = () => {
			node.remove();
			clearTimeout(timer);
		};
		ctx.abort.push(abort);
		let timer = setTimeout(() => {
			innerNode.classList.add("q-ripple__inner--enter");
			innerNode.style.transform = `translate3d(${centerX},${centerY},0) scale3d(1,1,1)`;
			innerNode.style.opacity = .2;
			timer = setTimeout(() => {
				innerNode.classList.remove("q-ripple__inner--enter");
				innerNode.classList.add("q-ripple__inner--leave");
				innerNode.style.opacity = 0;
				timer = setTimeout(() => {
					node.remove();
					ctx.abort.splice(ctx.abort.indexOf(abort), 1);
				}, 275);
			}, 250);
		}, 50);
	}
	function updateModifiers$1(ctx, { modifiers, value, arg }) {
		const cfg = {
			...ctx.cfg.ripple,
			...modifiers,
			...value
		};
		ctx.modifiers = {
			early: cfg.early === true,
			stop: cfg.stop === true,
			center: cfg.center === true,
			color: cfg.color || arg,
			keyCodes: [cfg.keyCodes || 13].flat()
		};
	}
	var Ripple_default = createDirective({
		name: "ripple",
		beforeMount(el, binding) {
			const cfg = binding.instance.$.appContext.config.globalProperties.$q.config || {};
			if (cfg.ripple === false) return;
			const ctx = {
				cfg,
				enabled: binding.value !== false,
				modifiers: {},
				abort: [],
				start(evt) {
					if (ctx.enabled && !evt.qSkipRipple && evt.type === (ctx.modifiers.early ? "pointerdown" : "click")) showRipple(evt, el, ctx, evt.qKeyEvent === true);
				},
				keystart: throttle((evt) => {
					if (ctx.enabled && !evt.qSkipRipple && isKeyCode(evt, ctx.modifiers.keyCodes) && evt.type === `key${ctx.modifiers.early ? "down" : "up"}`) showRipple(evt, el, ctx, true);
				}, 300)
			};
			updateModifiers$1(ctx, binding);
			el.__qripple = ctx;
			addEvt(ctx, "main", [
				[
					el,
					"pointerdown",
					"start",
					"passive"
				],
				[
					el,
					"click",
					"start",
					"passive"
				],
				[
					el,
					"keydown",
					"keystart",
					"passive"
				],
				[
					el,
					"keyup",
					"keystart",
					"passive"
				]
			]);
		},
		updated(el, binding) {
			if (binding.oldValue !== binding.value) {
				const ctx = el.__qripple;
				if (ctx !== void 0) {
					ctx.enabled = binding.value !== false;
					if (ctx.enabled && Object(binding.value) === binding.value) updateModifiers$1(ctx, binding);
				}
			}
		},
		beforeUnmount(el) {
			const ctx = el.__qripple;
			if (ctx !== void 0) {
				ctx.abort.forEach((fn) => {
					fn();
				});
				cleanEvt(ctx, "main");
				delete el.__qripple;
			}
		}
	});
	//#endregion
	//#region src/components/btn/use-btn.js
	const btnPadding = {
		none: 0,
		xs: 4,
		sm: 8,
		md: 16,
		lg: 24,
		xl: 32
	};
	const defaultSizes$2 = {
		xs: 8,
		sm: 10,
		md: 14,
		lg: 20,
		xl: 24
	};
	const formTypes = [
		"button",
		"submit",
		"reset"
	];
	const mediaTypeRE = /[^\s]\/[^\s]/;
	const btnDesignOptions = [
		"flat",
		"outline",
		"push",
		"unelevated"
	];
	function getBtnDesign(props, defaultValue) {
		if (props.flat) return "flat";
		if (props.outline) return "outline";
		if (props.push) return "push";
		if (props.unelevated) return "unelevated";
		return defaultValue;
	}
	function getBtnDesignAttr(props) {
		const design = getBtnDesign(props);
		return design !== void 0 ? { [design]: true } : {};
	}
	const nonRoundBtnProps = {
		...useSizeProps,
		...useRouterLinkNonMatchingProps,
		type: {
			type: String,
			default: "button"
		},
		label: [Number, String],
		icon: String,
		iconRight: String,
		...btnDesignOptions.reduce((acc, val) => (acc[val] = Boolean) && acc, {}),
		square: Boolean,
		rounded: Boolean,
		glossy: Boolean,
		size: String,
		fab: Boolean,
		fabMini: Boolean,
		padding: String,
		color: String,
		textColor: String,
		noCaps: Boolean,
		noWrap: Boolean,
		dense: Boolean,
		tabindex: [Number, String],
		ripple: {
			type: [Boolean, Object],
			default: true
		},
		align: {
			...useAlignProps.align,
			default: "center"
		},
		stack: Boolean,
		stretch: Boolean,
		loading: {
			type: Boolean,
			default: null
		},
		disable: Boolean
	};
	const useBtnProps = {
		...nonRoundBtnProps,
		round: Boolean
	};
	function useBtn(props) {
		const sizeStyle = useSize(props, defaultSizes$2);
		const alignClass = useAlign(props);
		const { hasRouterLink, hasLink, linkTag, linkAttrs, navigateOnClick } = useRouterLink({ fallbackTag: "button" });
		const style = (0, vue.computed)(() => {
			const obj = props.fab || props.fabMini ? {} : sizeStyle.value;
			return props.padding !== void 0 ? {
				...obj,
				padding: props.padding.split(/\s+/).map((v) => v in btnPadding ? btnPadding[v] + "px" : v).join(" "),
				minWidth: "0",
				minHeight: "0"
			} : obj;
		});
		const isRounded = (0, vue.computed)(() => props.rounded || props.fab || props.fabMini);
		const isActionable = (0, vue.computed)(() => !props.disable && !props.loading);
		const tabIndex = (0, vue.computed)(() => isActionable.value ? props.tabindex || 0 : -1);
		const design = (0, vue.computed)(() => getBtnDesign(props, "standard"));
		const attributes = (0, vue.computed)(() => {
			const acc = { tabindex: tabIndex.value };
			if (hasLink.value) Object.assign(acc, linkAttrs.value);
			else if (formTypes.includes(props.type)) acc.type = props.type;
			if (linkTag.value === "a") {
				if (props.disable) acc["aria-disabled"] = "true";
				else if (acc.href === void 0) acc.role = "button";
				if (!hasRouterLink.value && mediaTypeRE.test(props.type)) acc.type = props.type;
			} else if (props.disable) {
				acc.disabled = "";
				acc["aria-disabled"] = "true";
			}
			if (props.loading && props.percentage !== void 0) Object.assign(acc, {
				role: "progressbar",
				"aria-valuemin": 0,
				"aria-valuemax": 100,
				"aria-valuenow": props.percentage
			});
			return acc;
		});
		return {
			classes: (0, vue.computed)(() => {
				let colors;
				if (props.color !== void 0) colors = props.flat || props.outline ? `text-${props.textColor || props.color}` : `bg-${props.color} text-${props.textColor || "white"}`;
				else if (props.textColor) colors = `text-${props.textColor}`;
				const shape = props.round ? "round" : `rectangle${isRounded.value ? " q-btn--rounded" : props.square ? " q-btn--square" : ""}`;
				return `q-btn--${design.value} q-btn--${shape}` + (colors !== void 0 ? " " + colors : "") + (isActionable.value ? " q-btn--actionable q-focusable q-hoverable" : props.disable ? " disabled" : "") + (props.fab ? " q-btn--fab" : props.fabMini ? " q-btn--fab-mini" : "") + (props.noCaps ? " q-btn--no-uppercase" : "") + (props.dense ? " q-btn--dense" : "") + (props.stretch ? " no-border-radius self-stretch" : "") + (props.glossy ? " glossy" : "") + (props.square ? " q-btn--square" : "");
			}),
			style,
			innerClasses: (0, vue.computed)(() => alignClass.value + (props.stack ? " column" : " row") + (props.noWrap ? " no-wrap text-no-wrap" : "") + (props.loading ? " q-btn__content--hidden" : "")),
			attributes,
			hasLink,
			linkTag,
			navigateOnClick,
			isActionable
		};
	}
	//#endregion
	//#region src/components/btn/QBtn.js
	const { passiveCapture } = listenOpts;
	let touchTarget = null;
	let keyboardTarget = null;
	let mouseTarget = null;
	function onLoadingEvt(evt) {
		stopAndPrevent(evt);
		evt.qSkipRipple = true;
	}
	var QBtn_default = createComponent({
		name: "QBtn",
		props: {
			...useBtnProps,
			percentage: Number,
			darkPercentage: Boolean,
			onTouchstart: [Function, Array]
		},
		emits: [
			"click",
			"keydown",
			"mousedown",
			"keyup"
		],
		setup(props, { slots, emit }) {
			const { proxy } = (0, vue.getCurrentInstance)();
			const { classes, style, innerClasses, attributes, hasLink, linkTag, navigateOnClick, isActionable } = useBtn(props);
			const rootRef = (0, vue.ref)(null);
			const blurTargetRef = (0, vue.ref)(null);
			let localTouchTargetEl = null, avoidMouseRipple, mouseTimer = null;
			const hasLabel = (0, vue.computed)(() => props.label !== void 0 && props.label !== null && props.label !== "");
			const ripple = (0, vue.computed)(() => props.disable || props.ripple === false ? false : {
				keyCodes: hasLink.value ? [13, 32] : [13],
				...props.ripple === true ? {} : props.ripple
			});
			const rippleProps = (0, vue.computed)(() => ({ center: props.round }));
			const percentageStyle = (0, vue.computed)(() => {
				const val = Math.max(0, Math.min(100, props.percentage));
				return val > 0 ? {
					transition: "transform 0.6s",
					transform: `translateX(${val - 100}%)`
				} : {};
			});
			const onEvents = (0, vue.computed)(() => {
				if (props.loading) return {
					onMousedown: onLoadingEvt,
					onTouchstart: onLoadingEvt,
					onClick: onLoadingEvt,
					onKeydown: onLoadingEvt,
					onKeyup: onLoadingEvt
				};
				if (isActionable.value) {
					const acc = {
						onClick,
						onKeydown,
						onMousedown
					};
					if (proxy.$q.platform.has.touch) {
						const suffix = props.onTouchstart !== void 0 ? "" : "Passive";
						acc[`onTouchstart${suffix}`] = onTouchstart;
					}
					return acc;
				}
				return { onClick: stopAndPrevent };
			});
			const nodeProps = (0, vue.computed)(() => ({
				ref: rootRef,
				class: "q-btn q-btn-item non-selectable no-outline " + classes.value,
				style: style.value,
				...attributes.value,
				...onEvents.value
			}));
			function onClick(e) {
				if (rootRef.value === null) return;
				if (e !== void 0) {
					if (e.defaultPrevented) return;
					const el = document.activeElement;
					if (props.type === "submit" && el !== document.body && !rootRef.value.contains(el) && !el.contains(rootRef.value)) {
						if (!e.qAvoidFocus) rootRef.value.focus();
						const onClickCleanup = () => {
							document.removeEventListener("keydown", stopAndPrevent, true);
							document.removeEventListener("keyup", onClickCleanup, passiveCapture);
							rootRef.value?.removeEventListener("blur", onClickCleanup, passiveCapture);
						};
						document.addEventListener("keydown", stopAndPrevent, true);
						document.addEventListener("keyup", onClickCleanup, passiveCapture);
						rootRef.value.addEventListener("blur", onClickCleanup, passiveCapture);
					}
				}
				navigateOnClick(e);
			}
			function onKeydown(e) {
				if (rootRef.value === null) return;
				emit("keydown", e);
				if (isKeyCode(e, [13, 32]) && keyboardTarget !== rootRef.value) {
					if (keyboardTarget !== null) cleanup();
					if (!e.defaultPrevented) {
						if (!e.qAvoidFocus) rootRef.value.focus();
						keyboardTarget = rootRef.value;
						rootRef.value.classList.add("q-btn--active");
						document.addEventListener("keyup", onPressEnd, true);
						rootRef.value.addEventListener("blur", onPressEnd, passiveCapture);
					}
					stopAndPrevent(e);
				}
			}
			function onTouchstart(e) {
				if (rootRef.value === null) return;
				emit("touchstart", e);
				if (e.defaultPrevented) return;
				if (touchTarget !== rootRef.value) {
					if (touchTarget !== null) cleanup();
					touchTarget = rootRef.value;
					localTouchTargetEl = e.target;
					localTouchTargetEl.addEventListener("touchcancel", onPressEnd, passiveCapture);
					localTouchTargetEl.addEventListener("touchend", onPressEnd, passiveCapture);
				}
				avoidMouseRipple = true;
				if (mouseTimer !== null) clearTimeout(mouseTimer);
				mouseTimer = setTimeout(() => {
					mouseTimer = null;
					avoidMouseRipple = false;
				}, 200);
			}
			function onMousedown(e) {
				if (rootRef.value === null) return;
				e.qSkipRipple = avoidMouseRipple === true;
				emit("mousedown", e);
				if (!e.defaultPrevented && mouseTarget !== rootRef.value) {
					if (mouseTarget !== null) cleanup();
					mouseTarget = rootRef.value;
					rootRef.value.classList.add("q-btn--active");
					document.addEventListener("mouseup", onPressEnd, passiveCapture);
				}
			}
			function onPressEnd(e) {
				if (rootRef.value === null) return;
				if (e?.type === "blur" && document.activeElement === rootRef.value) return;
				if (e?.type === "keyup") {
					if (keyboardTarget === rootRef.value && isKeyCode(e, [13, 32])) {
						const evt = new MouseEvent("click", e);
						evt.qKeyEvent = true;
						if (e.defaultPrevented) prevent(evt);
						if (e.cancelBubble) stop(evt);
						rootRef.value.dispatchEvent(evt);
						stopAndPrevent(e);
						e.qKeyEvent = true;
					}
					emit("keyup", e);
				}
				cleanup();
			}
			function cleanup(destroying) {
				const blurTarget = blurTargetRef.value;
				if (!destroying && (touchTarget === rootRef.value || mouseTarget === rootRef.value) && blurTarget !== null && blurTarget !== document.activeElement) {
					blurTarget.setAttribute("tabindex", -1);
					blurTarget.focus();
				}
				if (touchTarget === rootRef.value) {
					if (localTouchTargetEl !== null) {
						localTouchTargetEl.removeEventListener("touchcancel", onPressEnd, passiveCapture);
						localTouchTargetEl.removeEventListener("touchend", onPressEnd, passiveCapture);
					}
					touchTarget = localTouchTargetEl = null;
				}
				if (mouseTarget === rootRef.value) {
					document.removeEventListener("mouseup", onPressEnd, passiveCapture);
					mouseTarget = null;
				}
				if (keyboardTarget === rootRef.value) {
					document.removeEventListener("keyup", onPressEnd, true);
					rootRef.value?.removeEventListener("blur", onPressEnd, passiveCapture);
					keyboardTarget = null;
				}
				rootRef.value?.classList.remove("q-btn--active");
			}
			(0, vue.onBeforeUnmount)(() => {
				cleanup(true);
			});
			Object.assign(proxy, { click: (e) => {
				if (isActionable.value) onClick(e);
			} });
			return () => {
				let inner = [];
				if (props.icon !== void 0) inner.push((0, vue.h)(QIcon_default, {
					name: props.icon,
					left: !props.stack && hasLabel.value,
					role: "img"
				}));
				if (hasLabel.value) inner.push((0, vue.h)("span", { class: "block" }, [props.label]));
				inner = hMergeSlot(slots.default, inner);
				if (props.iconRight !== void 0 && !props.round) inner.push((0, vue.h)(QIcon_default, {
					name: props.iconRight,
					right: !props.stack && hasLabel.value,
					role: "img"
				}));
				const child = [(0, vue.h)("span", {
					class: "q-focus-helper",
					ref: blurTargetRef
				})];
				if (props.loading && props.percentage !== void 0) child.push((0, vue.h)("span", { class: "q-btn__progress absolute-full overflow-hidden" + (props.darkPercentage ? " q-btn__progress--dark" : "") }, [(0, vue.h)("span", {
					class: "q-btn__progress-indicator fit block",
					style: percentageStyle.value
				})]));
				child.push((0, vue.h)("span", { class: "q-btn__content text-center col items-center q-anchor--skip " + innerClasses.value }, inner));
				if (props.loading !== null) child.push((0, vue.h)(vue.Transition, { name: "q-transition--fade" }, () => props.loading ? [(0, vue.h)("span", {
					key: "loading",
					class: "absolute-full flex flex-center"
				}, slots.loading !== void 0 ? slots.loading() : [(0, vue.h)(QSpinner_default)])] : null));
				return (0, vue.withDirectives)((0, vue.h)(linkTag.value, nodeProps.value, child), [[
					Ripple_default,
					ripple.value,
					void 0,
					rippleProps.value
				]]);
			};
		}
	});
	//#endregion
	//#region src/components/btn-group/QBtnGroup.js
	var QBtnGroup_default = createComponent({
		name: "QBtnGroup",
		props: {
			unelevated: Boolean,
			outline: Boolean,
			flat: Boolean,
			rounded: Boolean,
			square: Boolean,
			push: Boolean,
			stretch: Boolean,
			glossy: Boolean,
			spread: Boolean
		},
		setup(props, { slots }) {
			const classes = (0, vue.computed)(() => {
				const cls = [
					"unelevated",
					"outline",
					"flat",
					"rounded",
					"square",
					"push",
					"stretch",
					"glossy"
				].filter((t) => props[t]).map((t) => `q-btn-group--${t}`).join(" ");
				return `q-btn-group row no-wrap${cls.length !== 0 ? " " + cls : ""}` + (props.spread ? " q-btn-group--spread" : " inline");
			});
			return () => (0, vue.h)("div", { class: classes.value }, hSlot(slots.default));
		}
	});
	//#endregion
	//#region src/utils/private.selection/selection.js
	function clearSelection() {
		if (window.getSelection !== void 0) {
			const selection = window.getSelection();
			if (selection.empty !== void 0) selection.empty();
			else if (selection.removeAllRanges !== void 0) {
				selection.removeAllRanges();
				if (!Platform.is.mobile) selection.addRange(document.createRange());
			}
		} else if (document.selection !== void 0) document.selection.empty();
	}
	//#endregion
	//#region src/composables/private.use-anchor/use-anchor.js
	const useAnchorStaticProps = {
		target: {
			type: [
				Boolean,
				String,
				Element
			],
			default: true
		},
		noParentEvent: Boolean
	};
	const useAnchorProps = {
		...useAnchorStaticProps,
		contextMenu: Boolean
	};
	function useAnchor({ showing, avoidEmit, configureAnchorEl }) {
		const { props, proxy, emit } = (0, vue.getCurrentInstance)();
		const anchorEl = (0, vue.ref)(null);
		let touchTimer = null;
		function canShow(evt) {
			return anchorEl.value === null ? false : evt === void 0 || evt.touches === void 0 || evt.touches.length <= 1;
		}
		const anchorEvents = {};
		if (configureAnchorEl === void 0) {
			Object.assign(anchorEvents, {
				hide(evt) {
					proxy.hide(evt);
				},
				toggle(evt) {
					proxy.toggle(evt);
					evt.qAnchorHandled = true;
				},
				toggleKey(evt) {
					if (isKeyCode(evt, 13)) anchorEvents.toggle(evt);
				},
				contextClick(evt) {
					proxy.hide(evt);
					prevent(evt);
					(0, vue.nextTick)(() => {
						proxy.show(evt);
						evt.qAnchorHandled = true;
					});
				},
				prevent,
				mobileTouch(evt) {
					anchorEvents.mobileCleanup(evt);
					if (!canShow(evt)) return;
					proxy.hide(evt);
					anchorEl.value.classList.add("non-selectable");
					const target = evt.target;
					addEvt(anchorEvents, "anchor", [
						[
							target,
							"touchmove",
							"mobileCleanup",
							"passive"
						],
						[
							target,
							"touchend",
							"mobileCleanup",
							"passive"
						],
						[
							target,
							"touchcancel",
							"mobileCleanup",
							"passive"
						],
						[
							anchorEl.value,
							"contextmenu",
							"prevent",
							"notPassive"
						]
					]);
					touchTimer = setTimeout(() => {
						touchTimer = null;
						proxy.show(evt);
						evt.qAnchorHandled = true;
					}, 300);
				},
				mobileCleanup(evt) {
					anchorEl.value.classList.remove("non-selectable");
					if (touchTimer !== null) {
						clearTimeout(touchTimer);
						touchTimer = null;
					}
					if (showing.value && evt !== void 0) clearSelection();
				}
			});
			configureAnchorEl = function configureAnchorElFn(context = props.contextMenu) {
				if (props.noParentEvent || anchorEl.value === null) return;
				const evts = context ? proxy.$q.platform.is.mobile ? [[
					anchorEl.value,
					"touchstart",
					"mobileTouch",
					"passive"
				]] : [[
					anchorEl.value,
					"mousedown",
					"hide",
					"passive"
				], [
					anchorEl.value,
					"contextmenu",
					"contextClick",
					"notPassive"
				]] : [[
					anchorEl.value,
					"click",
					"toggle",
					"passive"
				], [
					anchorEl.value,
					"keyup",
					"toggleKey",
					"passive"
				]];
				addEvt(anchorEvents, "anchor", evts);
			};
		}
		function unconfigureAnchorEl() {
			cleanEvt(anchorEvents, "anchor");
		}
		function setAnchorEl(el) {
			anchorEl.value = el;
			while (anchorEl.value.classList.contains("q-anchor--skip")) anchorEl.value = anchorEl.value.parentNode;
			configureAnchorEl();
		}
		function pickAnchorEl() {
			if (props.target === false || props.target === "" || proxy.$el.parentNode === null) anchorEl.value = null;
			else if (props.target === true) setAnchorEl(proxy.$el.parentNode);
			else {
				let el = props.target;
				if (typeof props.target === "string") try {
					el = document.querySelector(props.target);
				} catch {
					el = void 0;
				}
				if (el !== void 0 && el !== null) {
					anchorEl.value = el.$el || el;
					configureAnchorEl();
				} else {
					anchorEl.value = null;
					console.error(`Anchor: target "${props.target}" not found`);
				}
			}
		}
		(0, vue.watch)(() => props.contextMenu, (val) => {
			if (anchorEl.value !== null) {
				unconfigureAnchorEl();
				configureAnchorEl(val);
			}
		});
		(0, vue.watch)(() => props.target, () => {
			if (anchorEl.value !== null) unconfigureAnchorEl();
			pickAnchorEl();
		});
		(0, vue.watch)(() => props.noParentEvent, (val) => {
			if (anchorEl.value !== null) if (val) unconfigureAnchorEl();
			else configureAnchorEl();
		});
		(0, vue.onMounted)(() => {
			pickAnchorEl();
			if (!avoidEmit && props.modelValue && anchorEl.value === null) emit("update:modelValue", false);
		});
		(0, vue.onBeforeUnmount)(() => {
			if (touchTimer !== null) clearTimeout(touchTimer);
			unconfigureAnchorEl();
		});
		return {
			anchorEl,
			canShow,
			anchorEvents
		};
	}
	//#endregion
	//#region src/composables/private.use-scroll-target/use-scroll-target.js
	function useScrollTarget(props, configureScrollTarget) {
		const localScrollTarget = (0, vue.ref)(null);
		let scrollFn;
		function changeScrollEvent(scrollTarget, fn) {
			const fnProp = `${fn !== void 0 ? "add" : "remove"}EventListener`;
			const fnHandler = fn !== void 0 ? fn : scrollFn;
			if (scrollTarget !== window) scrollTarget[fnProp]("scroll", fnHandler, listenOpts.passive);
			window[fnProp]("scroll", fnHandler, listenOpts.passive);
			scrollFn = fn;
		}
		function unconfigureScrollTarget() {
			if (localScrollTarget.value !== null) {
				changeScrollEvent(localScrollTarget.value);
				localScrollTarget.value = null;
			}
		}
		(0, vue.onBeforeUnmount)((0, vue.watch)(() => props.noParentEvent, () => {
			if (localScrollTarget.value !== null) {
				unconfigureScrollTarget();
				configureScrollTarget();
			}
		}));
		return {
			localScrollTarget,
			unconfigureScrollTarget,
			changeScrollEvent
		};
	}
	//#endregion
	//#region src/composables/private.use-model-toggle/use-model-toggle.js
	const useModelToggleProps = {
		modelValue: {
			type: Boolean,
			default: null
		},
		"onUpdate:modelValue": [Function, Array]
	};
	const useModelToggleEmits = [
		"beforeShow",
		"show",
		"beforeHide",
		"hide"
	];
	function useModelToggle({ showing, canShow, hideOnRouteChange, handleShow, handleHide, handleRouteChange, processOnMount }) {
		const vm = (0, vue.getCurrentInstance)();
		const { props, emit, proxy } = vm;
		let payload;
		function toggle(evt) {
			if (showing.value) hide(evt);
			else show(evt);
		}
		function show(evt) {
			if (props.disable || evt?.qAnchorHandled === true || canShow !== void 0 && !canShow(evt)) return;
			const listener = props["onUpdate:modelValue"] !== void 0;
			if (listener && true) {
				emit("update:modelValue", true);
				payload = evt;
				(0, vue.nextTick)(() => {
					if (payload === evt) payload = void 0;
				});
			}
			if (props.modelValue === null || !listener) processShow(evt);
		}
		function processShow(evt) {
			if (showing.value) return;
			showing.value = true;
			emit("beforeShow", evt);
			if (handleShow !== void 0) handleShow(evt);
			else emit("show", evt);
		}
		function hide(evt) {
			if (props.disable) return;
			const listener = props["onUpdate:modelValue"] !== void 0;
			if (listener && true) {
				emit("update:modelValue", false);
				payload = evt;
				(0, vue.nextTick)(() => {
					if (payload === evt) payload = void 0;
				});
			}
			if (props.modelValue === null || !listener) processHide(evt);
		}
		function processHide(evt) {
			if (!showing.value) return;
			showing.value = false;
			emit("beforeHide", evt);
			if (handleHide !== void 0) handleHide(evt);
			else emit("hide", evt);
		}
		function processModelChange(val) {
			if (props.disable && val) {
				if (props["onUpdate:modelValue"] !== void 0) emit("update:modelValue", false);
			} else if (val === true !== showing.value) (val ? processShow : processHide)(payload);
		}
		(0, vue.watch)(() => props.modelValue, processModelChange);
		if (hideOnRouteChange !== void 0 && vmHasRouter(vm)) (0, vue.watch)(() => proxy.$route.fullPath, () => {
			if (hideOnRouteChange.value && showing.value) {
				handleRouteChange?.();
				hide();
			}
		});
		if (processOnMount) (0, vue.onMounted)(() => {
			processModelChange(props.modelValue);
		});
		const publicMethods = {
			show,
			hide,
			toggle
		};
		Object.assign(proxy, publicMethods);
		return publicMethods;
	}
	//#endregion
	//#region src/utils/private.portal/portal.js
	const portalProxyList = [];
	function getPortalProxy(el) {
		return portalProxyList.find((proxy) => proxy.contentEl !== null && proxy.contentEl.contains(el));
	}
	function closePortalMenus(proxy, evt) {
		do {
			if (proxy.$options.name === "QMenu") {
				proxy.hide(evt);
				if (proxy.$props.separateClosePopup) return getParentProxy(proxy);
			} else if (proxy.__qPortal) {
				const parent = getParentProxy(proxy);
				if (parent?.$options.name === "QPopupProxy") {
					proxy.hide(evt);
					return parent;
				}
				return proxy;
			}
			proxy = getParentProxy(proxy);
		} while (proxy !== void 0 && proxy !== null);
	}
	function closePortals(proxy, evt, depth) {
		while (depth !== 0 && proxy !== void 0 && proxy !== null) {
			if (proxy.__qPortal) {
				depth--;
				if (proxy.$options.name === "QMenu") {
					proxy = closePortalMenus(proxy, evt);
					continue;
				}
				proxy.hide(evt);
			}
			proxy = getParentProxy(proxy);
		}
	}
	//#endregion
	//#region src/utils/private.focus/focus-manager.js
	let queue = [];
	let waitFlags = [];
	function clearFlag(flag) {
		waitFlags = waitFlags.filter((entry) => entry !== flag);
	}
	function addFocusWaitFlag(flag) {
		clearFlag(flag);
		waitFlags.push(flag);
	}
	function removeFocusWaitFlag(flag) {
		clearFlag(flag);
		if (waitFlags.length === 0 && queue.length !== 0) {
			queue.at(-1)();
			queue = [];
		}
	}
	function addFocusFn(fn) {
		if (waitFlags.length === 0) fn();
		else queue.push(fn);
	}
	function removeFocusFn(fn) {
		queue = queue.filter((entry) => entry !== fn);
	}
	//#endregion
	//#region src/utils/private.config/nodes.js
	const nodesList = [];
	const portalTypeList = [];
	let portalIndex = 1;
	let target = document.body;
	function createGlobalNode(id, portalType) {
		const el = document.createElement("div");
		el.id = portalType !== void 0 ? `q-portal--${portalType}--${portalIndex++}` : id;
		if (globalConfig.globalNodes !== void 0) {
			const cls = globalConfig.globalNodes.class;
			if (cls !== void 0) el.className = cls;
		}
		target.append(el);
		nodesList.push(el);
		portalTypeList.push(portalType);
		return el;
	}
	function removeGlobalNode(el) {
		const nodeIndex = nodesList.indexOf(el);
		nodesList.splice(nodeIndex, 1);
		portalTypeList.splice(nodeIndex, 1);
		el.remove();
	}
	function changeGlobalNodesTarget(newTarget) {
		if (newTarget === target) return;
		target = newTarget;
		if (target === document.body || portalTypeList.reduce((acc, type) => type === "dialog" ? acc + 1 : acc, 0) < 2) {
			nodesList.forEach((node) => {
				if (!node.contains(target)) target.append(node);
			});
			return;
		}
		const lastDialogIndex = portalTypeList.lastIndexOf("dialog");
		for (let i = 0; i < nodesList.length; i++) {
			const el = nodesList[i];
			if ((i === lastDialogIndex || portalTypeList[i] !== "dialog") && !el.contains(target)) target.append(el);
		}
	}
	//#endregion
	//#region src/composables/private.use-portal/use-portal.js
	/**
	* Noop internal component to ease testing
	* of the teleported content.
	*
	* const wrapper = mount(QDialog, { ... })
	* const teleportedWrapper = wrapper.findComponent({ name: 'QPortal' })
	*/
	const QPortal = createComponent({
		name: "QPortal",
		setup(_, { slots }) {
			return () => slots.default();
		}
	});
	function isOnGlobalDialog(vm) {
		vm = vm.parent;
		while (vm !== void 0 && vm !== null) {
			if (vm.type.name === "QGlobalDialog") return true;
			if (vm.type.name === "QDialog" || vm.type.name === "QMenu") return false;
			vm = vm.parent;
		}
		return false;
	}
	function usePortal(vm, innerRef, renderPortalContent, type) {
		const portalIsActive = (0, vue.ref)(false);
		const portalIsAccessible = (0, vue.ref)(false);
		let portalEl = null;
		const focusObj = {};
		const onGlobalDialog = type === "dialog" && isOnGlobalDialog(vm);
		function showPortal(isReady) {
			if (isReady) {
				removeFocusWaitFlag(focusObj);
				portalIsAccessible.value = true;
				return;
			}
			portalIsAccessible.value = false;
			if (!portalIsActive.value) {
				if (!onGlobalDialog && portalEl === null) portalEl = createGlobalNode(false, type);
				portalIsActive.value = true;
				portalProxyList.push(vm.proxy);
				addFocusWaitFlag(focusObj);
			}
		}
		function hidePortal(isReady) {
			portalIsAccessible.value = false;
			if (!isReady) return;
			removeFocusWaitFlag(focusObj);
			portalIsActive.value = false;
			const index = portalProxyList.indexOf(vm.proxy);
			if (index !== -1) portalProxyList.splice(index, 1);
			if (portalEl !== null) {
				removeGlobalNode(portalEl);
				portalEl = null;
			}
		}
		(0, vue.onUnmounted)(() => {
			hidePortal(true);
		});
		vm.proxy.__qPortal = true;
		injectProp(vm.proxy, "contentEl", () => innerRef.value);
		return {
			showPortal,
			hidePortal,
			portalIsActive,
			portalIsAccessible,
			renderPortal: () => onGlobalDialog ? renderPortalContent() : portalIsActive.value ? [(0, vue.h)(vue.Teleport, { to: portalEl }, (0, vue.h)(QPortal, renderPortalContent))] : void 0
		};
	}
	//#endregion
	//#region src/composables/private.use-transition/use-transition.js
	const useTransitionProps = {
		transitionShow: {
			type: String,
			default: "fade"
		},
		transitionHide: {
			type: String,
			default: "fade"
		},
		transitionDuration: {
			type: [String, Number],
			default: 300
		}
	};
	function useTransition(props, defaultShowFn = () => {}, defaultHideFn = () => {}) {
		return {
			transitionProps: (0, vue.computed)(() => {
				const show = `q-transition--${props.transitionShow || defaultShowFn()}`;
				const hide = `q-transition--${props.transitionHide || defaultHideFn()}`;
				return {
					appear: true,
					enterFromClass: `${show}-enter-from`,
					enterActiveClass: `${show}-enter-active`,
					enterToClass: `${show}-enter-to`,
					leaveFromClass: `${hide}-leave-from`,
					leaveActiveClass: `${hide}-leave-active`,
					leaveToClass: `${hide}-leave-to`
				};
			}),
			transitionStyle: (0, vue.computed)(() => `--q-transition-duration: ${props.transitionDuration}ms`)
		};
	}
	//#endregion
	//#region src/composables/use-tick/use-tick.js
	function useTick() {
		let tickFn;
		const vm = (0, vue.getCurrentInstance)();
		function removeTick() {
			tickFn = void 0;
		}
		(0, vue.onDeactivated)(removeTick);
		(0, vue.onBeforeUnmount)(removeTick);
		return {
			removeTick,
			registerTick(fn) {
				tickFn = fn;
				(0, vue.nextTick)(() => {
					if (tickFn === fn) {
						if (!vmIsDestroyed(vm)) tickFn();
						tickFn = void 0;
					}
				});
			}
		};
	}
	//#endregion
	//#region src/composables/use-timeout/use-timeout.js
	function useTimeout() {
		let timer = null;
		const vm = (0, vue.getCurrentInstance)();
		function removeTimeout() {
			if (timer !== null) {
				clearTimeout(timer);
				timer = null;
			}
		}
		(0, vue.onDeactivated)(removeTimeout);
		(0, vue.onBeforeUnmount)(removeTimeout);
		return {
			removeTimeout,
			registerTimeout(fn, delay) {
				removeTimeout();
				if (!vmIsDestroyed(vm)) timer = setTimeout(() => {
					timer = null;
					fn();
				}, delay);
			}
		};
	}
	//#endregion
	//#region src/utils/scroll/scroll.js
	const scrollTargetProp = [Element, String];
	const scrollTargets = [
		null,
		document,
		document.body,
		document.scrollingElement,
		document.documentElement
	];
	function getScrollTarget(el, targetEl) {
		let target = getElement$1(targetEl);
		if (target === void 0) {
			if (el === void 0 || el === null) return window;
			target = el.closest(".scroll,.scroll-y,.overflow-auto");
		}
		return scrollTargets.includes(target) ? window : target;
	}
	function getScrollHeight(el) {
		return (el === window ? document.body : el).scrollHeight;
	}
	function getScrollWidth(el) {
		return (el === window ? document.body : el).scrollWidth;
	}
	function getVerticalScrollPosition(scrollTarget) {
		return scrollTarget === window ? window.pageYOffset || window.scrollY || document.body.scrollTop || 0 : scrollTarget.scrollTop;
	}
	function getHorizontalScrollPosition(scrollTarget) {
		return scrollTarget === window ? window.pageXOffset || window.scrollX || document.body.scrollLeft || 0 : scrollTarget.scrollLeft;
	}
	function animVerticalScrollTo(el, to, duration = 0, rawPrevTime) {
		const prevTime = rawPrevTime === void 0 ? performance.now() : rawPrevTime;
		const pos = getVerticalScrollPosition(el);
		if (duration <= 0) {
			if (pos !== to) setScroll$1(el, to);
			return;
		}
		requestAnimationFrame((nowTime) => {
			const frameTime = nowTime - prevTime;
			const newPos = pos + (to - pos) / Math.max(frameTime, duration) * frameTime;
			setScroll$1(el, newPos);
			if (newPos !== to) animVerticalScrollTo(el, to, duration - frameTime, nowTime);
		});
	}
	function animHorizontalScrollTo(el, to, duration = 0, rawPrevTime) {
		const prevTime = rawPrevTime === void 0 ? performance.now() : rawPrevTime;
		const pos = getHorizontalScrollPosition(el);
		if (duration <= 0) {
			if (pos !== to) setHorizontalScroll(el, to);
			return;
		}
		requestAnimationFrame((nowTime) => {
			const frameTime = nowTime - prevTime;
			const newPos = pos + (to - pos) / Math.max(frameTime, duration) * frameTime;
			setHorizontalScroll(el, newPos);
			if (newPos !== to) animHorizontalScrollTo(el, to, duration - frameTime, nowTime);
		});
	}
	function setScroll$1(scrollTarget, offset) {
		if (scrollTarget === window) {
			window.scrollTo(window.pageXOffset || window.scrollX || document.body.scrollLeft || 0, offset);
			return;
		}
		scrollTarget.scrollTop = offset;
	}
	function setHorizontalScroll(scrollTarget, offset) {
		if (scrollTarget === window) {
			window.scrollTo(offset, window.pageYOffset || window.scrollY || document.body.scrollTop || 0);
			return;
		}
		scrollTarget.scrollLeft = offset;
	}
	function setVerticalScrollPosition(scrollTarget, offset, duration) {
		if (duration) {
			animVerticalScrollTo(scrollTarget, offset, duration);
			return;
		}
		setScroll$1(scrollTarget, offset);
	}
	function setHorizontalScrollPosition(scrollTarget, offset, duration) {
		if (duration) {
			animHorizontalScrollTo(scrollTarget, offset, duration);
			return;
		}
		setHorizontalScroll(scrollTarget, offset);
	}
	let size;
	function getScrollbarWidth() {
		if (size !== void 0) return size;
		const inner = document.createElement("p"), outer = document.createElement("div");
		css(inner, {
			width: "100%",
			height: "200px"
		});
		css(outer, {
			position: "absolute",
			top: "0px",
			left: "0px",
			visibility: "hidden",
			width: "200px",
			height: "150px",
			overflow: "hidden"
		});
		outer.append(inner);
		document.body.append(outer);
		const w1 = inner.offsetWidth;
		outer.style.overflow = "scroll";
		let w2 = inner.offsetWidth;
		if (w1 === w2) w2 = outer.clientWidth;
		outer.remove();
		size = w1 - w2;
		return size;
	}
	const autoAndScroll = ["auto", "scroll"];
	function hasScrollbar(el, onY = true) {
		if (!el || el.nodeType !== Node.ELEMENT_NODE) return false;
		return onY ? el.scrollHeight > el.clientHeight && (el.classList.contains("scroll") || el.classList.contains("overflow-auto") || autoAndScroll.includes(window.getComputedStyle(el)["overflow-y"])) : el.scrollWidth > el.clientWidth && (el.classList.contains("scroll") || el.classList.contains("overflow-auto") || autoAndScroll.includes(window.getComputedStyle(el)["overflow-x"]));
	}
	var scroll_default = {
		getScrollTarget,
		getScrollHeight,
		getScrollWidth,
		getVerticalScrollPosition,
		getHorizontalScrollPosition,
		animVerticalScrollTo,
		animHorizontalScrollTo,
		setVerticalScrollPosition,
		setHorizontalScrollPosition,
		getScrollbarWidth,
		hasScrollbar
	};
	//#endregion
	//#region src/utils/private.keyboard/escape-key.js
	const handlers$1 = [];
	let escDown;
	function onKeydown$3(evt) {
		escDown = evt.keyCode === 27;
	}
	function onBlur() {
		if (escDown) escDown = false;
	}
	function onKeyup(evt) {
		if (escDown) {
			escDown = false;
			if (isKeyCode(evt, 27)) handlers$1.at(-1)(evt);
		}
	}
	function update$4(action) {
		window[action]("keydown", onKeydown$3);
		window[action]("blur", onBlur);
		window[action]("keyup", onKeyup);
		escDown = false;
	}
	function addEscapeKey(fn) {
		if (client.is.desktop) {
			handlers$1.push(fn);
			if (handlers$1.length === 1) update$4("addEventListener");
		}
	}
	function removeEscapeKey(fn) {
		const index = handlers$1.indexOf(fn);
		if (index !== -1) {
			handlers$1.splice(index, 1);
			if (handlers$1.length === 0) update$4("removeEventListener");
		}
	}
	//#endregion
	//#region src/utils/private.focus/focusout.js
	const handlers = [];
	function trigger$1(e) {
		handlers.at(-1)(e);
	}
	function addFocusout(fn) {
		if (client.is.desktop) {
			handlers.push(fn);
			if (handlers.length === 1) document.body.addEventListener("focusin", trigger$1);
		}
	}
	function removeFocusout(fn) {
		const index = handlers.indexOf(fn);
		if (index !== -1) {
			handlers.splice(index, 1);
			if (handlers.length === 0) document.body.removeEventListener("focusin", trigger$1);
		}
	}
	//#endregion
	//#region src/utils/private.click-outside/click-outside.js
	let timer = null;
	const { notPassiveCapture } = listenOpts, registeredList = [];
	function globalHandler(evt) {
		if (timer !== null) {
			clearTimeout(timer);
			timer = null;
		}
		const target = evt.target;
		if (target === void 0 || target.nodeType === 8 || target.classList.contains("no-pointer-events")) return;
		let portalIndex = portalProxyList.length - 1;
		while (portalIndex >= 0) {
			const proxy = portalProxyList[portalIndex].$;
			if (proxy.type.name === "QTooltip") {
				portalIndex--;
				continue;
			}
			if (proxy.type.name !== "QDialog") break;
			if (!proxy.props.seamless) return;
			portalIndex--;
		}
		for (let i = registeredList.length - 1; i >= 0; i--) {
			const state = registeredList[i];
			if ((state.anchorEl.value === null || !state.anchorEl.value.contains(target)) && (target === document.body || state.innerRef.value !== null && !state.innerRef.value.contains(target))) {
				evt.qClickOutside = true;
				state.onClickOutside(evt);
			} else return;
		}
	}
	function addClickOutside(clickOutsideProps) {
		registeredList.push(clickOutsideProps);
		if (registeredList.length === 1) {
			document.addEventListener("mousedown", globalHandler, notPassiveCapture);
			document.addEventListener("touchstart", globalHandler, notPassiveCapture);
		}
	}
	function removeClickOutside(clickOutsideProps) {
		const index = registeredList.indexOf(clickOutsideProps);
		if (index !== -1) {
			registeredList.splice(index, 1);
			if (registeredList.length === 0) {
				if (timer !== null) {
					clearTimeout(timer);
					timer = null;
				}
				document.removeEventListener("mousedown", globalHandler, notPassiveCapture);
				document.removeEventListener("touchstart", globalHandler, notPassiveCapture);
			}
		}
	}
	//#endregion
	//#region src/utils/private.position-engine/position-engine.js
	let vpLeft;
	let vpTop;
	const partsFirst = [
		"top",
		"center",
		"bottom"
	];
	const partsSecond = [
		"left",
		"middle",
		"right",
		"start",
		"end"
	];
	function validatePosition(pos) {
		const parts = pos.split(" ");
		if (parts.length !== 2) return false;
		if (!partsFirst.includes(parts[0])) {
			console.error("Anchor/Self position must start with one of top/center/bottom");
			return false;
		}
		if (!partsSecond.includes(parts[1])) {
			console.error("Anchor/Self position must end with one of left/middle/right/start/end");
			return false;
		}
		return true;
	}
	function validateOffset(val) {
		if (!val) return true;
		if (val.length !== 2) return false;
		if (typeof val[0] !== "number" || typeof val[1] !== "number") return false;
		return true;
	}
	const horizontalPos = {
		"start#ltr": "left",
		"start#rtl": "right",
		"end#ltr": "right",
		"end#rtl": "left"
	};
	[
		"left",
		"middle",
		"right"
	].forEach((pos) => {
		horizontalPos[`${pos}#ltr`] = pos;
		horizontalPos[`${pos}#rtl`] = pos;
	});
	function parsePosition(pos, rtl) {
		const parts = pos.split(" ");
		return {
			vertical: parts[0],
			horizontal: horizontalPos[`${parts[1]}#${rtl ? "rtl" : "ltr"}`]
		};
	}
	function getAnchorProps(el, offset) {
		let { top, left, right, bottom, width, height } = el.getBoundingClientRect();
		if (offset !== void 0) {
			top -= offset[1];
			left -= offset[0];
			bottom += offset[1];
			right += offset[0];
			width += offset[0];
			height += offset[1];
		}
		return {
			top,
			bottom,
			height,
			left,
			right,
			width,
			middle: left + (right - left) / 2,
			center: top + (bottom - top) / 2
		};
	}
	function getAbsoluteAnchorProps(el, absoluteOffset, offset) {
		let { top, left } = el.getBoundingClientRect();
		top += absoluteOffset.top;
		left += absoluteOffset.left;
		if (offset !== void 0) {
			top += offset[1];
			left += offset[0];
		}
		return {
			top,
			bottom: top + 1,
			height: 1,
			left,
			right: left + 1,
			width: 1,
			middle: left,
			center: top
		};
	}
	function getTargetProps(width, height) {
		return {
			top: 0,
			center: height / 2,
			bottom: height,
			left: 0,
			middle: width / 2,
			right: width
		};
	}
	function getTopLeftProps(anchorProps, targetProps, anchorOrigin, selfOrigin) {
		return {
			top: anchorProps[anchorOrigin.vertical] - targetProps[selfOrigin.vertical],
			left: anchorProps[anchorOrigin.horizontal] - targetProps[selfOrigin.horizontal]
		};
	}
	function setPosition(cfg, retryNumber = 0) {
		if (cfg.targetEl === null || cfg.anchorEl === null || retryNumber > 5) return;
		if (cfg.targetEl.offsetHeight === 0 || cfg.targetEl.offsetWidth === 0) {
			setTimeout(() => {
				setPosition(cfg, retryNumber + 1);
			}, 10);
			return;
		}
		const { targetEl, offset, anchorEl, anchorOrigin, selfOrigin, absoluteOffset, fit, cover, maxHeight, maxWidth } = cfg;
		if (client.is.ios && window.visualViewport !== void 0) {
			const el = document.body.style;
			const { offsetLeft: left, offsetTop: top } = window.visualViewport;
			if (left !== vpLeft) {
				el.setProperty("--q-pe-left", left + "px");
				vpLeft = left;
			}
			if (top !== vpTop) {
				el.setProperty("--q-pe-top", top + "px");
				vpTop = top;
			}
		}
		const { scrollLeft, scrollTop } = targetEl;
		const anchorProps = absoluteOffset === void 0 ? getAnchorProps(anchorEl, cover ? [0, 0] : offset) : getAbsoluteAnchorProps(anchorEl, absoluteOffset, offset);
		/**
		* We "reset" the critical CSS properties
		* so we can take an accurate measurement.
		*
		* Ensure that targetEl has a max-width & max-height
		* set in CSS and that the value does NOT exceeds 100vw/vh.
		* All users of the position-engine (currently QMenu & QTooltip)
		* have CSS for this.
		*/
		Object.assign(targetEl.style, {
			top: 0,
			left: 0,
			minWidth: null,
			minHeight: null,
			maxWidth,
			maxHeight,
			visibility: "visible"
		});
		const { offsetWidth: origElWidth, offsetHeight: origElHeight } = targetEl;
		const { elWidth, elHeight } = fit || cover ? {
			elWidth: Math.max(anchorProps.width, origElWidth),
			elHeight: cover ? Math.max(anchorProps.height, origElHeight) : origElHeight
		} : {
			elWidth: origElWidth,
			elHeight: origElHeight
		};
		let elStyle = {
			maxWidth,
			maxHeight
		};
		if (fit || cover) {
			elStyle.minWidth = anchorProps.width + "px";
			if (cover) elStyle.minHeight = anchorProps.height + "px";
		}
		Object.assign(targetEl.style, elStyle);
		const targetProps = getTargetProps(elWidth, elHeight);
		let props = getTopLeftProps(anchorProps, targetProps, anchorOrigin, selfOrigin);
		if (absoluteOffset === void 0 || offset === void 0) applyBoundaries(props, anchorProps, targetProps, anchorOrigin, selfOrigin);
		else {
			const { top, left } = props;
			applyBoundaries(props, anchorProps, targetProps, anchorOrigin, selfOrigin);
			let hasChanged = false;
			if (props.top !== top) {
				hasChanged = true;
				const offsetY = 2 * offset[1];
				anchorProps.center = anchorProps.top -= offsetY;
				anchorProps.bottom -= offsetY + 2;
			}
			if (props.left !== left) {
				hasChanged = true;
				const offsetX = 2 * offset[0];
				anchorProps.middle = anchorProps.left -= offsetX;
				anchorProps.right -= offsetX + 2;
			}
			if (hasChanged) {
				props = getTopLeftProps(anchorProps, targetProps, anchorOrigin, selfOrigin);
				applyBoundaries(props, anchorProps, targetProps, anchorOrigin, selfOrigin);
			}
		}
		elStyle = {
			top: props.top + "px",
			left: props.left + "px"
		};
		if (props.maxHeight !== void 0) {
			elStyle.maxHeight = props.maxHeight + "px";
			if (anchorProps.height > props.maxHeight) elStyle.minHeight = elStyle.maxHeight;
		}
		if (props.maxWidth !== void 0) {
			elStyle.maxWidth = props.maxWidth + "px";
			if (anchorProps.width > props.maxWidth) elStyle.minWidth = elStyle.maxWidth;
		}
		Object.assign(targetEl.style, elStyle);
		if (targetEl.scrollTop !== scrollTop) targetEl.scrollTop = scrollTop;
		if (targetEl.scrollLeft !== scrollLeft) targetEl.scrollLeft = scrollLeft;
	}
	function applyBoundaries(props, anchorProps, targetProps, anchorOrigin, selfOrigin) {
		const currentHeight = targetProps.bottom, currentWidth = targetProps.right, margin = getScrollbarWidth(), innerHeight = window.innerHeight - margin, innerWidth = document.body.clientWidth;
		if (props.top < 0 || props.top + currentHeight > innerHeight) if (selfOrigin.vertical === "center") {
			props.top = anchorProps[anchorOrigin.vertical] > innerHeight / 2 ? Math.max(0, innerHeight - currentHeight) : 0;
			props.maxHeight = Math.min(currentHeight, innerHeight);
		} else if (anchorProps[anchorOrigin.vertical] > innerHeight / 2) {
			const anchorY = Math.min(innerHeight, anchorOrigin.vertical === "center" ? anchorProps.center : anchorOrigin.vertical === selfOrigin.vertical ? anchorProps.bottom : anchorProps.top);
			props.maxHeight = Math.min(currentHeight, anchorY);
			props.top = Math.max(0, anchorY - currentHeight);
		} else {
			props.top = Math.max(0, anchorOrigin.vertical === "center" ? anchorProps.center : anchorOrigin.vertical === selfOrigin.vertical ? anchorProps.top : anchorProps.bottom);
			props.maxHeight = Math.min(currentHeight, innerHeight - props.top);
		}
		if (props.left < 0 || props.left + currentWidth > innerWidth) {
			props.maxWidth = Math.min(currentWidth, innerWidth);
			if (selfOrigin.horizontal === "middle") props.left = anchorProps[anchorOrigin.horizontal] > innerWidth / 2 ? Math.max(0, innerWidth - currentWidth) : 0;
			else if (anchorProps[anchorOrigin.horizontal] > innerWidth / 2) {
				const anchorX = Math.min(innerWidth, anchorOrigin.horizontal === "middle" ? anchorProps.middle : anchorOrigin.horizontal === selfOrigin.horizontal ? anchorProps.right : anchorProps.left);
				props.maxWidth = Math.min(currentWidth, anchorX);
				props.left = Math.max(0, anchorX - props.maxWidth);
			} else {
				props.left = Math.max(0, anchorOrigin.horizontal === "middle" ? anchorProps.middle : anchorOrigin.horizontal === selfOrigin.horizontal ? anchorProps.left : anchorProps.right);
				props.maxWidth = Math.min(currentWidth, innerWidth - props.left);
			}
		}
	}
	//#endregion
	//#region src/components/menu/QMenu.js
	var QMenu_default = createComponent({
		name: "QMenu",
		inheritAttrs: false,
		props: {
			...useAnchorProps,
			...useModelToggleProps,
			...useDarkProps,
			...useTransitionProps,
			persistent: Boolean,
			autoClose: Boolean,
			separateClosePopup: Boolean,
			noEscDismiss: Boolean,
			noRouteDismiss: Boolean,
			noRefocus: Boolean,
			noFocus: Boolean,
			fit: Boolean,
			cover: Boolean,
			square: Boolean,
			anchor: {
				type: String,
				validator: validatePosition
			},
			self: {
				type: String,
				validator: validatePosition
			},
			offset: {
				type: Array,
				validator: validateOffset
			},
			scrollTarget: scrollTargetProp,
			touchPosition: Boolean,
			maxHeight: {
				type: String,
				default: null
			},
			maxWidth: {
				type: String,
				default: null
			}
		},
		emits: [
			...useModelToggleEmits,
			"click",
			"escapeKey"
		],
		setup(props, { slots, emit, attrs }) {
			let refocusTarget = null, absoluteOffset, unwatchPosition, avoidAutoClose;
			const vm = (0, vue.getCurrentInstance)();
			const { proxy } = vm;
			const { $q } = proxy;
			const innerRef = (0, vue.ref)(null);
			const showing = (0, vue.ref)(false);
			const hideOnRouteChange = (0, vue.computed)(() => !props.persistent && !props.noRouteDismiss);
			const isDark = useDark(props, $q);
			const { registerTick, removeTick } = useTick();
			const { registerTimeout } = useTimeout();
			const { transitionProps, transitionStyle } = useTransition(props);
			const { localScrollTarget, changeScrollEvent, unconfigureScrollTarget } = useScrollTarget(props, configureScrollTarget);
			const { anchorEl, canShow } = useAnchor({ showing });
			const { hide } = useModelToggle({
				showing,
				canShow,
				handleShow,
				handleHide,
				handleRouteChange,
				hideOnRouteChange,
				processOnMount: true
			});
			const { showPortal, hidePortal, renderPortal } = usePortal(vm, innerRef, renderPortalContent, "menu");
			const clickOutsideProps = {
				anchorEl,
				innerRef,
				onClickOutside(e) {
					if (!props.persistent && showing.value) {
						hide(e);
						if (e.type === "touchstart" || e.target.classList.contains("q-dialog__backdrop")) stopAndPrevent(e);
						return true;
					}
				}
			};
			const anchorOrigin = (0, vue.computed)(() => parsePosition(props.anchor || (props.cover ? "center middle" : "bottom start"), $q.lang.rtl));
			const selfOrigin = (0, vue.computed)(() => props.cover ? anchorOrigin.value : parsePosition(props.self || "top start", $q.lang.rtl));
			const menuClass = (0, vue.computed)(() => (props.square ? " q-menu--square" : "") + (isDark.value ? " q-menu--dark q-dark" : ""));
			const onEvents = (0, vue.computed)(() => props.autoClose ? { onClick: onAutoClose } : {});
			const handlesFocus = (0, vue.computed)(() => showing.value && !props.persistent);
			(0, vue.watch)(handlesFocus, (val) => {
				if (val) {
					addEscapeKey(onEscapeKey);
					addClickOutside(clickOutsideProps);
				} else {
					removeEscapeKey(onEscapeKey);
					removeClickOutside(clickOutsideProps);
				}
			});
			function focus() {
				addFocusFn(() => {
					let node = innerRef.value;
					if (node && !node.contains(document.activeElement)) {
						node = node.querySelector("[autofocus][tabindex], [data-autofocus][tabindex]") || node.querySelector("[autofocus] [tabindex], [data-autofocus] [tabindex]") || node.querySelector("[autofocus], [data-autofocus]") || node;
						node.focus({ preventScroll: true });
					}
				});
			}
			function handleShow(evt) {
				refocusTarget = props.noRefocus ? null : document.activeElement;
				addFocusout(onFocusout);
				showPortal();
				configureScrollTarget();
				absoluteOffset = void 0;
				if (evt !== void 0 && (props.touchPosition || props.contextMenu)) {
					const pos = position(evt);
					if (pos.left !== void 0) {
						const { top, left } = anchorEl.value.getBoundingClientRect();
						absoluteOffset = {
							left: pos.left - left,
							top: pos.top - top
						};
					}
				}
				if (unwatchPosition === void 0) unwatchPosition = (0, vue.watch)(() => $q.screen.width + "|" + $q.screen.height + "|" + props.self + "|" + props.anchor + "|" + $q.lang.rtl, updatePosition);
				if (!props.noFocus) document.activeElement.blur();
				registerTick(() => {
					updatePosition();
					if (!props.noFocus) focus();
				});
				registerTimeout(() => {
					if ($q.platform.is.ios) {
						avoidAutoClose = props.autoClose;
						innerRef.value.click();
					}
					updatePosition();
					showPortal(true);
					emit("show", evt);
				}, props.transitionDuration);
			}
			function handleHide(evt) {
				removeTick();
				hidePortal();
				anchorCleanup(true);
				if (refocusTarget !== null && (evt === void 0 || !evt.qClickOutside)) {
					const target = (evt?.type.indexOf("key") === 0 ? refocusTarget.closest("[tabindex]:not([tabindex^=\"-\"])") : void 0) || refocusTarget;
					refocusTarget = null;
					addFocusFn(() => {
						if (target.isConnected) target.focus();
					});
				}
				registerTimeout(() => {
					hidePortal(true);
					emit("hide", evt);
				}, props.transitionDuration);
			}
			function handleRouteChange() {
				refocusTarget = null;
			}
			function anchorCleanup(hiding) {
				absoluteOffset = void 0;
				if (unwatchPosition !== void 0) {
					unwatchPosition();
					unwatchPosition = void 0;
				}
				if (hiding || showing.value) {
					removeFocusout(onFocusout);
					unconfigureScrollTarget();
					removeClickOutside(clickOutsideProps);
					removeEscapeKey(onEscapeKey);
				}
				if (!hiding) refocusTarget = null;
			}
			function configureScrollTarget() {
				if (anchorEl.value !== null || props.scrollTarget !== void 0) {
					localScrollTarget.value = getScrollTarget(anchorEl.value, props.scrollTarget);
					changeScrollEvent(localScrollTarget.value, updatePosition);
				}
			}
			function onAutoClose(e) {
				if (!avoidAutoClose) {
					closePortalMenus(proxy, e);
					emit("click", e);
				} else avoidAutoClose = false;
			}
			function onFocusout(evt) {
				if (handlesFocus.value && !props.noFocus && !childHasFocus(innerRef.value, evt.target)) focus();
			}
			function onEscapeKey(evt) {
				if (!props.noEscDismiss) {
					emit("escapeKey");
					hide(evt);
				}
			}
			function updatePosition() {
				setPosition({
					targetEl: innerRef.value,
					offset: props.offset,
					anchorEl: anchorEl.value,
					anchorOrigin: anchorOrigin.value,
					selfOrigin: selfOrigin.value,
					absoluteOffset,
					fit: props.fit,
					cover: props.cover,
					maxHeight: props.maxHeight,
					maxWidth: props.maxWidth
				});
			}
			function renderPortalContent() {
				return (0, vue.h)(vue.Transition, transitionProps.value, () => showing.value ? (0, vue.h)("div", {
					role: "menu",
					...attrs,
					ref: innerRef,
					tabindex: -1,
					class: ["q-menu q-position-engine scroll" + menuClass.value, attrs.class],
					style: [attrs.style, transitionStyle.value],
					...onEvents.value
				}, hSlot(slots.default)) : null);
			}
			(0, vue.onBeforeUnmount)(() => {
				anchorCleanup();
			});
			Object.assign(proxy, {
				focus,
				updatePosition
			});
			return renderPortal;
		}
	});
	//#endregion
	//#region src/utils/uid/uid.js
	function createUidFn() {
		if (typeof crypto === "undefined") return () => {
			throw new Error("[Quasar uid()] Secure RNG not available. Cannot generate collision-resistant UUID.");
		};
		if (crypto.randomUUID) return () => crypto.randomUUID();
		const hex = Array.from({ length: 256 }, (_, i) => (i + 256).toString(16).slice(1));
		let buf, bufIdx;
		return () => {
			if (buf === void 0 || bufIdx + 16 > 4096) {
				bufIdx = 0;
				buf = /* @__PURE__ */ new Uint8Array(4096);
				crypto.getRandomValues(buf);
			}
			const i = bufIdx;
			bufIdx += 16;
			buf[i + 6] = buf[i + 6] & 15 | 64;
			buf[i + 8] = buf[i + 8] & 63 | 128;
			return hex[buf[i]] + hex[buf[i + 1]] + hex[buf[i + 2]] + hex[buf[i + 3]] + "-" + hex[buf[i + 4]] + hex[buf[i + 5]] + "-" + hex[buf[i + 6]] + hex[buf[i + 7]] + "-" + hex[buf[i + 8]] + hex[buf[i + 9]] + "-" + hex[buf[i + 10]] + hex[buf[i + 11]] + hex[buf[i + 12]] + hex[buf[i + 13]] + hex[buf[i + 14]] + hex[buf[i + 15]];
		};
	}
	var uid_default = createUidFn();
	//#endregion
	//#region src/composables/use-id/use-id.js
	function parseValue(val) {
		return val === void 0 || val === null ? null : val;
	}
	function getId(val, required) {
		return val === void 0 || val === null ? required ? `f_${uid_default()}` : null : val;
	}
	/**
	* Returns an "id" which is a ref() that can be used as
	* a unique identifier to apply to a DOM node attribute.
	*
	* On SSR, it takes care of generating the id on the client side (only) to
	* avoid hydration errors.
	*/
	function useId({ getValue, required = true } = {}) {
		if (isRuntimeSsrPreHydration.value) {
			const id = getValue !== void 0 ? (0, vue.ref)(parseValue(getValue())) : (0, vue.ref)(null);
			if (required && id.value === null) (0, vue.onMounted)(() => {
				id.value = `f_${uid_default()}`;
			});
			if (getValue !== void 0) (0, vue.watch)(getValue, (newId) => {
				id.value = getId(newId, required);
			});
			return id;
		}
		return getValue !== void 0 ? (0, vue.computed)(() => getId(getValue(), required)) : (0, vue.ref)(`f_${uid_default()}`);
	}
	//#endregion
	//#region src/components/btn-dropdown/QBtnDropdown.js
	const btnPropsList = Object.keys(nonRoundBtnProps);
	function passBtnProps(props) {
		return btnPropsList.reduce((acc, key) => {
			const val = props[key];
			if (val !== void 0) acc[key] = val;
			return acc;
		}, {});
	}
	var QBtnDropdown_default = createComponent({
		name: "QBtnDropdown",
		props: {
			...nonRoundBtnProps,
			...useTransitionProps,
			modelValue: Boolean,
			split: Boolean,
			dropdownIcon: String,
			contentClass: [
				Array,
				String,
				Object
			],
			contentStyle: [
				Array,
				String,
				Object
			],
			cover: Boolean,
			persistent: Boolean,
			noEscDismiss: Boolean,
			noRouteDismiss: Boolean,
			autoClose: Boolean,
			noRefocus: Boolean,
			noFocus: Boolean,
			menuAnchor: {
				type: String,
				default: "bottom end"
			},
			menuSelf: {
				type: String,
				default: "top end"
			},
			menuOffset: Array,
			disableMainBtn: Boolean,
			disableDropdown: Boolean,
			noIconAnimation: Boolean,
			toggleAriaLabel: String
		},
		emits: [
			"update:modelValue",
			"click",
			"beforeShow",
			"show",
			"beforeHide",
			"hide"
		],
		setup(props, { slots, emit }) {
			const { proxy } = (0, vue.getCurrentInstance)();
			const showing = (0, vue.ref)(props.modelValue);
			const menuRef = (0, vue.ref)(null);
			const targetUid = useId();
			const ariaAttrs = (0, vue.computed)(() => {
				const acc = {
					"aria-expanded": showing.value ? "true" : "false",
					"aria-haspopup": "true",
					"aria-controls": targetUid.value,
					"aria-label": props.toggleAriaLabel || proxy.$q.lang.label[showing.value ? "collapse" : "expand"](props.label)
				};
				if (props.disable || !props.split && props.disableMainBtn || props.disableDropdown) acc["aria-disabled"] = "true";
				return acc;
			});
			const iconClass = (0, vue.computed)(() => "q-btn-dropdown__arrow" + (showing.value && !props.noIconAnimation ? " rotate-180" : "") + (props.split ? "" : " q-btn-dropdown__arrow-container"));
			const btnDesignAttr = (0, vue.computed)(() => getBtnDesignAttr(props));
			const btnProps = (0, vue.computed)(() => passBtnProps(props));
			(0, vue.watch)(() => props.modelValue, (val) => {
				menuRef.value?.[val ? "show" : "hide"]();
			});
			(0, vue.watch)(() => props.split, hide);
			function onBeforeShow(e) {
				showing.value = true;
				emit("beforeShow", e);
			}
			function onShow(e) {
				emit("show", e);
				emit("update:modelValue", true);
			}
			function onBeforeHide(e) {
				showing.value = false;
				emit("beforeHide", e);
			}
			function onHide(e) {
				emit("hide", e);
				emit("update:modelValue", false);
			}
			function onClick(e) {
				emit("click", e);
			}
			function onClickHide(e) {
				stop(e);
				hide();
				emit("click", e);
			}
			function toggle(evt) {
				menuRef.value?.toggle(evt);
			}
			function show(evt) {
				menuRef.value?.show(evt);
			}
			function hide(evt) {
				menuRef.value?.hide(evt);
			}
			Object.assign(proxy, {
				show,
				hide,
				toggle
			});
			(0, vue.onMounted)(() => {
				if (props.modelValue) show();
			});
			return () => {
				const Arrow = [(0, vue.h)(QIcon_default, {
					class: iconClass.value,
					name: props.dropdownIcon || proxy.$q.iconSet.arrow.dropdown
				})];
				if (!props.disableDropdown) Arrow.push((0, vue.h)(QMenu_default, {
					ref: menuRef,
					id: targetUid.value,
					class: props.contentClass,
					style: props.contentStyle,
					cover: props.cover,
					fit: true,
					persistent: props.persistent,
					noEscDismiss: props.noEscDismiss,
					noRouteDismiss: props.noRouteDismiss,
					autoClose: props.autoClose,
					noFocus: props.noFocus,
					noRefocus: props.noRefocus,
					anchor: props.menuAnchor,
					self: props.menuSelf,
					offset: props.menuOffset,
					separateClosePopup: true,
					transitionShow: props.transitionShow,
					transitionHide: props.transitionHide,
					transitionDuration: props.transitionDuration,
					onBeforeShow,
					onShow,
					onBeforeHide,
					onHide
				}, slots.default));
				if (!props.split) return (0, vue.h)(QBtn_default, {
					class: "q-btn-dropdown q-btn-dropdown--simple",
					...btnProps.value,
					...ariaAttrs.value,
					disable: props.disable || props.disableMainBtn,
					noWrap: true,
					round: false,
					onClick
				}, {
					default: () => hSlot(slots.label, []).concat(Arrow),
					loading: slots.loading
				});
				return (0, vue.h)(QBtnGroup_default, {
					class: "q-btn-dropdown q-btn-dropdown--split no-wrap q-btn-item",
					rounded: props.rounded,
					square: props.square,
					...btnDesignAttr.value,
					glossy: props.glossy,
					stretch: props.stretch
				}, () => [(0, vue.h)(QBtn_default, {
					class: "q-btn-dropdown--current",
					...btnProps.value,
					disable: props.disable || props.disableMainBtn,
					noWrap: true,
					round: false,
					onClick: onClickHide
				}, {
					default: slots.label,
					loading: slots.loading
				}), (0, vue.h)(QBtn_default, {
					class: "q-btn-dropdown__arrow-container q-anchor--skip",
					...ariaAttrs.value,
					...btnDesignAttr.value,
					disable: props.disable || props.disableDropdown,
					rounded: props.rounded,
					color: props.color,
					textColor: props.textColor,
					dense: props.dense,
					size: props.size,
					padding: props.padding,
					ripple: props.ripple
				}, () => Arrow)]);
			};
		}
	});
	//#endregion
	//#region src/composables/use-form/private.use-form.js
	const useFormProps = { name: String };
	function useFormAttrs(props) {
		return (0, vue.computed)(() => ({
			type: "hidden",
			name: props.name,
			value: props.modelValue
		}));
	}
	function useFormInject(formAttrs = {}) {
		return (child, action, className) => {
			child[action]((0, vue.h)("input", {
				class: "hidden" + (className || ""),
				...formAttrs.value
			}));
		};
	}
	function useFormInputNameAttr(props) {
		return (0, vue.computed)(() => props.name || props.for);
	}
	//#endregion
	//#region src/components/btn-toggle/QBtnToggle.js
	var QBtnToggle_default = createComponent({
		name: "QBtnToggle",
		props: {
			...useFormProps,
			modelValue: { required: true },
			options: {
				type: Array,
				required: true,
				validator: (v) => v.every((opt) => ("label" in opt || "icon" in opt || "slot" in opt) && "value" in opt)
			},
			color: String,
			textColor: String,
			toggleColor: {
				type: String,
				default: "primary"
			},
			toggleTextColor: String,
			outline: Boolean,
			flat: Boolean,
			unelevated: Boolean,
			rounded: Boolean,
			push: Boolean,
			glossy: Boolean,
			size: String,
			padding: String,
			noCaps: Boolean,
			noWrap: Boolean,
			dense: Boolean,
			readonly: Boolean,
			disable: Boolean,
			stack: Boolean,
			stretch: Boolean,
			spread: Boolean,
			clearable: Boolean,
			ripple: {
				type: [Boolean, Object],
				default: true
			}
		},
		emits: [
			"update:modelValue",
			"clear",
			"click"
		],
		setup(props, { slots, emit }) {
			const hasActiveValue = (0, vue.computed)(() => props.options.find((opt) => opt.value === props.modelValue) !== void 0);
			const injectFormInput = useFormInject((0, vue.computed)(() => ({
				type: "hidden",
				name: props.name,
				value: props.modelValue
			})));
			const btnDesignAttr = (0, vue.computed)(() => getBtnDesignAttr(props));
			const btnOptionDesign = (0, vue.computed)(() => ({
				rounded: props.rounded,
				dense: props.dense,
				...btnDesignAttr.value
			}));
			const btnOptions = (0, vue.computed)(() => props.options.map((item, i) => {
				const { attrs, value, slot, ...opt } = item;
				return {
					slot,
					props: {
						key: i,
						"aria-pressed": value === props.modelValue ? "true" : "false",
						...attrs,
						...opt,
						...btnOptionDesign.value,
						disable: props.disable || opt.disable === true,
						color: value === props.modelValue ? mergeOpt(opt, "toggleColor") : mergeOpt(opt, "color"),
						textColor: value === props.modelValue ? mergeOpt(opt, "toggleTextColor") : mergeOpt(opt, "textColor"),
						noCaps: mergeOpt(opt, "noCaps") === true,
						noWrap: mergeOpt(opt, "noWrap") === true,
						size: mergeOpt(opt, "size"),
						padding: mergeOpt(opt, "padding"),
						ripple: mergeOpt(opt, "ripple"),
						stack: mergeOpt(opt, "stack") === true,
						stretch: mergeOpt(opt, "stretch") === true,
						onClick(e) {
							set(value, item, e);
						}
					}
				};
			}));
			function set(value, opt, e) {
				if (!props.readonly) {
					if (props.modelValue === value) {
						if (props.clearable) {
							emit("update:modelValue", null, null);
							emit("clear");
						}
					} else emit("update:modelValue", value, opt);
					emit("click", e);
				}
			}
			function mergeOpt(opt, key) {
				return opt[key] === void 0 ? props[key] : opt[key];
			}
			function getContent() {
				const child = btnOptions.value.map((opt) => (0, vue.h)(QBtn_default, opt.props, opt.slot !== void 0 ? slots[opt.slot] : void 0));
				if (props.name !== void 0 && !props.disable && hasActiveValue.value) injectFormInput(child, "push");
				return hMergeSlot(slots.default, child);
			}
			return () => (0, vue.h)(QBtnGroup_default, {
				class: "q-btn-toggle",
				...btnDesignAttr.value,
				rounded: props.rounded,
				stretch: props.stretch,
				glossy: props.glossy,
				spread: props.spread
			}, getContent);
		}
	});
	//#endregion
	//#region src/components/card/QCard.js
	var QCard_default = createComponent({
		name: "QCard",
		props: {
			...useDarkProps,
			tag: {
				type: String,
				default: "div"
			},
			square: Boolean,
			flat: Boolean,
			bordered: Boolean
		},
		setup(props, { slots }) {
			const { proxy: { $q } } = (0, vue.getCurrentInstance)();
			const isDark = useDark(props, $q);
			const classes = (0, vue.computed)(() => "q-card" + (isDark.value ? " q-card--dark q-dark" : "") + (props.bordered ? " q-card--bordered" : "") + (props.square ? " q-card--square no-border-radius" : "") + (props.flat ? " q-card--flat no-shadow" : ""));
			return () => (0, vue.h)(props.tag, { class: classes.value }, hSlot(slots.default));
		}
	});
	//#endregion
	//#region src/components/card/QCardSection.js
	var QCardSection_default = createComponent({
		name: "QCardSection",
		props: {
			tag: {
				type: String,
				default: "div"
			},
			horizontal: Boolean
		},
		setup(props, { slots }) {
			const classes = (0, vue.computed)(() => `q-card__section q-card__section--${props.horizontal ? "horiz row no-wrap" : "vert"}`);
			return () => (0, vue.h)(props.tag, { class: classes.value }, hSlot(slots.default));
		}
	});
	//#endregion
	//#region src/components/card/QCardActions.js
	var QCardActions_default = createComponent({
		name: "QCardActions",
		props: {
			...useAlignProps,
			vertical: Boolean
		},
		setup(props, { slots }) {
			const alignClass = useAlign(props);
			const classes = (0, vue.computed)(() => `q-card__actions ${alignClass.value} q-card__actions--${props.vertical ? "vert column" : "horiz row"}`);
			return () => (0, vue.h)("div", { class: classes.value }, hSlot(slots.default));
		}
	});
	//#endregion
	//#region src/utils/private.touch/touch.js
	const modifiersAll = {
		left: true,
		right: true,
		up: true,
		down: true,
		horizontal: true,
		vertical: true
	};
	const directionList = Object.keys(modifiersAll);
	modifiersAll.all = true;
	function getModifierDirections(mod) {
		const dir = {};
		for (const direction of directionList) if (mod[direction]) dir[direction] = true;
		if (Object.keys(dir).length === 0) return modifiersAll;
		if (dir.horizontal) dir.left = dir.right = true;
		else if (dir.left && dir.right) dir.horizontal = true;
		if (dir.vertical) dir.up = dir.down = true;
		else if (dir.up && dir.down) dir.vertical = true;
		if (dir.horizontal && dir.vertical) dir.all = true;
		return dir;
	}
	const avoidNodeNamesList = ["INPUT", "TEXTAREA"];
	function shouldStart(evt, ctx) {
		return ctx.event === void 0 && evt.target !== void 0 && !evt.target.draggable && typeof ctx.handler === "function" && !avoidNodeNamesList.includes(evt.target.nodeName.toUpperCase()) && (evt.qClonedBy === void 0 || !evt.qClonedBy.includes(ctx.uid));
	}
	//#endregion
	//#region src/directives/touch-swipe/TouchSwipe.js
	function parseArg(arg) {
		const data = [
			.06,
			6,
			50
		];
		if (typeof arg === "string" && arg.length !== 0) arg.split(":").forEach((val, index) => {
			const v = Number.parseFloat(val);
			if (v) data[index] = v;
		});
		return data;
	}
	function removeBodyChildrenNoPointerEvents() {
		document.body.classList.remove("no-pointer-events--children");
	}
	var TouchSwipe_default = createDirective({
		name: "touch-swipe",
		beforeMount(el, { value, arg, modifiers }) {
			if (!modifiers.mouse && !client.has.touch) return;
			const mouseCapture = modifiers.mouseCapture || modifiers.mousecapture ? "Capture" : "";
			const ctx = {
				handler: value,
				sensitivity: parseArg(arg),
				direction: getModifierDirections(modifiers),
				noop,
				mouseStart(evt) {
					if (shouldStart(evt, ctx) && leftClick(evt)) {
						addEvt(ctx, "temp", [[
							document,
							"mousemove",
							"move",
							`notPassive${mouseCapture}`
						], [
							document,
							"mouseup",
							"end",
							"notPassiveCapture"
						]]);
						ctx.start(evt, true);
					}
				},
				touchStart(evt) {
					if (shouldStart(evt, ctx)) {
						const target = evt.target;
						addEvt(ctx, "temp", [
							[
								target,
								"touchmove",
								"move",
								"notPassiveCapture"
							],
							[
								target,
								"touchcancel",
								"end",
								"notPassiveCapture"
							],
							[
								target,
								"touchend",
								"end",
								"notPassiveCapture"
							]
						]);
						ctx.start(evt);
					}
				},
				start(evt, mouseEvent) {
					if (client.is.firefox) preventDraggable(el, true);
					const pos = position(evt);
					ctx.event = {
						x: pos.left,
						y: pos.top,
						time: Date.now(),
						mouse: mouseEvent === true,
						dir: false
					};
				},
				move(evt) {
					if (ctx.event === void 0) return;
					if (ctx.event.dir !== false) {
						stopAndPrevent(evt);
						return;
					}
					const time = Date.now() - ctx.event.time;
					if (time === 0) return;
					const pos = position(evt), distX = pos.left - ctx.event.x, absX = Math.abs(distX), distY = pos.top - ctx.event.y, absY = Math.abs(distY);
					if (!ctx.event.mouse) {
						if (absX < ctx.sensitivity[1] && absY < ctx.sensitivity[1]) {
							ctx.end(evt);
							return;
						}
					} else if (window.getSelection().toString() !== "") {
						ctx.end(evt);
						return;
					} else if (absX < ctx.sensitivity[2] && absY < ctx.sensitivity[2]) return;
					const velX = absX / time, velY = absY / time;
					if (ctx.direction.vertical && absX < absY && absX < 100 && velY > ctx.sensitivity[0]) ctx.event.dir = distY < 0 ? "up" : "down";
					if (ctx.direction.horizontal && absX > absY && absY < 100 && velX > ctx.sensitivity[0]) ctx.event.dir = distX < 0 ? "left" : "right";
					if (ctx.direction.up && absX < absY && distY < 0 && absX < 100 && velY > ctx.sensitivity[0]) ctx.event.dir = "up";
					if (ctx.direction.down && absX < absY && distY > 0 && absX < 100 && velY > ctx.sensitivity[0]) ctx.event.dir = "down";
					if (ctx.direction.left && absX > absY && distX < 0 && absY < 100 && velX > ctx.sensitivity[0]) ctx.event.dir = "left";
					if (ctx.direction.right && absX > absY && distX > 0 && absY < 100 && velX > ctx.sensitivity[0]) ctx.event.dir = "right";
					if (ctx.event.dir !== false) {
						stopAndPrevent(evt);
						if (ctx.event.mouse) {
							document.body.classList.add("no-pointer-events--children", "non-selectable");
							clearSelection();
							ctx.styleCleanup = (withDelay) => {
								ctx.styleCleanup = void 0;
								document.body.classList.remove("non-selectable");
								if (withDelay === true) setTimeout(removeBodyChildrenNoPointerEvents, 50);
								else removeBodyChildrenNoPointerEvents();
							};
						}
						ctx.handler({
							evt,
							touch: ctx.event.mouse !== true,
							mouse: ctx.event.mouse,
							direction: ctx.event.dir,
							duration: time,
							distance: {
								x: absX,
								y: absY
							}
						});
					} else ctx.end(evt);
				},
				end(evt) {
					if (ctx.event === void 0) return;
					cleanEvt(ctx, "temp");
					if (client.is.firefox) preventDraggable(el, false);
					ctx.styleCleanup?.(true);
					if (evt !== void 0 && ctx.event.dir !== false) stopAndPrevent(evt);
					ctx.event = void 0;
				}
			};
			el.__qtouchswipe = ctx;
			if (modifiers.mouse) addEvt(ctx, "main", [[
				el,
				"mousedown",
				"mouseStart",
				`passive${modifiers.mouseCapture || modifiers.mousecapture ? "Capture" : ""}`
			]]);
			if (client.has.touch) addEvt(ctx, "main", [[
				el,
				"touchstart",
				"touchStart",
				`passive${modifiers.capture ? "Capture" : ""}`
			], [
				el,
				"touchmove",
				"noop",
				"notPassiveCapture"
			]]);
		},
		updated(el, bindings) {
			const ctx = el.__qtouchswipe;
			if (ctx !== void 0) {
				if (bindings.oldValue !== bindings.value) {
					if (typeof bindings.value !== "function") ctx.end();
					ctx.handler = bindings.value;
				}
				ctx.direction = getModifierDirections(bindings.modifiers);
			}
		},
		beforeUnmount(el) {
			const ctx = el.__qtouchswipe;
			if (ctx !== void 0) {
				cleanEvt(ctx, "main");
				cleanEvt(ctx, "temp");
				if (client.is.firefox) preventDraggable(el, false);
				ctx.styleCleanup?.();
				delete el.__qtouchswipe;
			}
		}
	});
	//#endregion
	//#region src/composables/use-render-cache/use-render-cache.js
	function useRenderCache() {
		let cache = Object.create(null);
		return {
			getCache: (key, defaultValue) => Object.hasOwn(cache, key) ? cache[key] : cache[key] = typeof defaultValue === "function" ? defaultValue() : defaultValue,
			setCache(key, obj) {
				cache[key] = obj;
			},
			hasCache(key) {
				return Object.hasOwn(cache, key);
			},
			clearCache(key) {
				if (key !== void 0) delete cache[key];
				else cache = Object.create(null);
			}
		};
	}
	//#endregion
	//#region src/composables/private.use-panel/use-panel.js
	const usePanelChildProps = {
		name: { required: true },
		disable: Boolean
	};
	const PanelWrapper$1 = { setup(_, { slots }) {
		return () => (0, vue.h)("div", {
			class: "q-panel scroll",
			role: "tabpanel"
		}, hSlot(slots.default));
	} };
	const usePanelProps = {
		modelValue: { required: true },
		animated: Boolean,
		infinite: Boolean,
		swipeable: Boolean,
		vertical: Boolean,
		transitionPrev: String,
		transitionNext: String,
		transitionDuration: {
			type: [String, Number],
			default: 300
		},
		keepAlive: Boolean,
		keepAliveInclude: [
			String,
			Array,
			RegExp
		],
		keepAliveExclude: [
			String,
			Array,
			RegExp
		],
		keepAliveMax: Number
	};
	const usePanelEmits = [
		"update:modelValue",
		"beforeTransition",
		"transition"
	];
	function isValidPanelName(name) {
		return name !== void 0 && name !== null && name !== "";
	}
	function usePanel() {
		const { props, emit, proxy } = (0, vue.getCurrentInstance)();
		const { getCache } = useRenderCache();
		const { registerTimeout } = useTimeout();
		let panels, forcedPanelTransition;
		const panelTransition = (0, vue.ref)(null);
		const panelIndex = { value: null };
		function onSwipe(evt) {
			const dir = props.vertical ? "up" : "left";
			goToPanelByOffset((proxy.$q.lang.rtl ? -1 : 1) * (evt.direction === dir ? 1 : -1));
		}
		const panelDirectives = (0, vue.computed)(() => [[
			TouchSwipe_default,
			onSwipe,
			void 0,
			{
				horizontal: !props.vertical,
				vertical: props.vertical,
				mouse: true
			}
		]]);
		const transitionPrev = (0, vue.computed)(() => props.transitionPrev || `slide-${props.vertical ? "down" : proxy.$q.lang.rtl ? "left" : "right"}`);
		const transitionNext = (0, vue.computed)(() => props.transitionNext || `slide-${props.vertical ? "up" : proxy.$q.lang.rtl ? "right" : "left"}`);
		const transitionStyle = (0, vue.computed)(() => `--q-transition-duration: ${props.transitionDuration}ms`);
		const contentKey = (0, vue.computed)(() => typeof props.modelValue === "string" || typeof props.modelValue === "number" ? props.modelValue : String(props.modelValue));
		const keepAliveProps = (0, vue.computed)(() => ({
			include: props.keepAliveInclude,
			exclude: props.keepAliveExclude,
			max: props.keepAliveMax
		}));
		const needsUniqueKeepAliveWrapper = (0, vue.computed)(() => props.keepAliveInclude !== void 0 || props.keepAliveExclude !== void 0);
		(0, vue.watch)(() => props.modelValue, (newVal, oldVal) => {
			const index = isValidPanelName(newVal) ? getPanelIndex(newVal) : -1;
			if (!forcedPanelTransition) updatePanelTransition(index === -1 ? 0 : index < getPanelIndex(oldVal) ? -1 : 1);
			if (panelIndex.value !== index) {
				panelIndex.value = index;
				emit("beforeTransition", newVal, oldVal);
				registerTimeout(() => {
					emit("transition", newVal, oldVal);
				}, props.transitionDuration);
			}
		});
		function nextPanel() {
			goToPanelByOffset(1);
		}
		function previousPanel() {
			goToPanelByOffset(-1);
		}
		function goToPanel(name) {
			emit("update:modelValue", name);
		}
		function getPanelIndex(name) {
			return panels.findIndex((panel) => panel.props.name === name && panel.props.disable !== "" && panel.props.disable !== true);
		}
		function getEnabledPanels() {
			return panels.filter((panel) => panel.props.disable !== "" && panel.props.disable !== true);
		}
		function updatePanelTransition(direction) {
			const val = direction !== 0 && props.animated && panelIndex.value !== -1 ? "q-transition--" + (direction === -1 ? transitionPrev.value : transitionNext.value) : null;
			if (panelTransition.value !== val) panelTransition.value = val;
		}
		function goToPanelByOffset(direction, startIndex = panelIndex.value) {
			let index = startIndex + direction;
			while (index !== -1 && index < panels.length) {
				const opt = panels[index];
				if (opt !== void 0 && opt.props.disable !== "" && opt.props.disable !== true) {
					updatePanelTransition(direction);
					forcedPanelTransition = true;
					emit("update:modelValue", opt.props.name);
					setTimeout(() => {
						forcedPanelTransition = false;
					}, 0);
					return;
				}
				index += direction;
			}
			if (props.infinite && panels.length !== 0 && startIndex !== -1 && startIndex !== panels.length) goToPanelByOffset(direction, direction === -1 ? panels.length : -1);
		}
		function updatePanelIndex() {
			const index = getPanelIndex(props.modelValue);
			if (panelIndex.value !== index) panelIndex.value = index;
			return true;
		}
		function getPanelContentChild() {
			const panel = isValidPanelName(props.modelValue) && updatePanelIndex() && panels[panelIndex.value];
			return props.keepAlive ? [(0, vue.h)(vue.KeepAlive, keepAliveProps.value, [(0, vue.h)(needsUniqueKeepAliveWrapper.value ? getCache(contentKey.value, () => ({
				...PanelWrapper$1,
				name: contentKey.value
			})) : PanelWrapper$1, {
				key: contentKey.value,
				style: transitionStyle.value
			}, () => panel)])] : [(0, vue.h)("div", {
				class: "q-panel scroll",
				style: transitionStyle.value,
				key: contentKey.value,
				role: "tabpanel"
			}, [panel])];
		}
		function getPanelContent() {
			if (panels.length === 0) return;
			return props.animated ? [(0, vue.h)(vue.Transition, { name: panelTransition.value }, getPanelContentChild)] : getPanelContentChild();
		}
		function updatePanelsList(slots) {
			panels = getNormalizedVNodes(hSlot(slots.default, [])).filter((panel) => panel.props !== null && panel.props.slot === void 0 && isValidPanelName(panel.props.name));
			return panels.length;
		}
		function getPanels() {
			return panels;
		}
		Object.assign(proxy, {
			next: nextPanel,
			previous: previousPanel,
			goTo: goToPanel
		});
		return {
			panelIndex,
			panelDirectives,
			updatePanelsList,
			updatePanelIndex,
			getPanelContent,
			getEnabledPanels,
			getPanels,
			isValidPanelName,
			keepAliveProps,
			needsUniqueKeepAliveWrapper,
			goToPanelByOffset,
			goToPanel,
			nextPanel,
			previousPanel
		};
	}
	//#endregion
	//#region src/composables/private.use-fullscreen/use-fullscreen.js
	let counter = 0;
	const useFullscreenProps = {
		fullscreen: Boolean,
		noRouteFullscreenExit: Boolean
	};
	const useFullscreenEmits = ["update:fullscreen", "fullscreen"];
	function useFullscreen() {
		const vm = (0, vue.getCurrentInstance)();
		const { props, emit, proxy } = vm;
		let historyEntry, fullscreenFillerNode, isUnmounting = false;
		const inFullscreen = (0, vue.ref)(false);
		if (vmHasRouter(vm)) (0, vue.watch)(() => proxy.$route.fullPath, () => {
			if (!props.noRouteFullscreenExit) exitFullscreen();
		});
		(0, vue.watch)(() => props.fullscreen, (v) => {
			if (inFullscreen.value !== v) toggleFullscreen();
		});
		(0, vue.watch)(inFullscreen, (v) => {
			emit("update:fullscreen", v);
			emit("fullscreen", v);
		});
		function toggleFullscreen() {
			if (inFullscreen.value) exitFullscreen();
			else setFullscreen();
		}
		function setFullscreen() {
			if (inFullscreen.value) return;
			inFullscreen.value = true;
			proxy.$el.replaceWith(fullscreenFillerNode);
			document.body.append(proxy.$el);
			counter++;
			if (counter === 1) document.body.classList.add("q-body--fullscreen-mixin");
			historyEntry = { handler: exitFullscreen };
			History_default.add(historyEntry);
		}
		function exitFullscreen() {
			if (!inFullscreen.value) return;
			if (historyEntry !== void 0) {
				History_default.remove(historyEntry);
				historyEntry = void 0;
			}
			fullscreenFillerNode.replaceWith(proxy.$el);
			inFullscreen.value = false;
			counter = Math.max(0, counter - 1);
			if (counter === 0) {
				document.body.classList.remove("q-body--fullscreen-mixin");
				if (!isUnmounting && proxy.$el.scrollIntoView !== void 0) setTimeout(() => {
					proxy.$el.scrollIntoView();
				}, 0);
			}
		}
		(0, vue.onBeforeMount)(() => {
			fullscreenFillerNode = document.createElement("span");
		});
		(0, vue.onMounted)(() => {
			if (props.fullscreen) setFullscreen();
		});
		(0, vue.onBeforeUnmount)(() => {
			isUnmounting = true;
			exitFullscreen();
		});
		Object.assign(proxy, {
			toggleFullscreen,
			setFullscreen,
			exitFullscreen
		});
		return {
			inFullscreen,
			toggleFullscreen
		};
	}
	//#endregion
	//#region src/components/carousel/QCarousel.js
	const navigationPositionOptions = [
		"top",
		"right",
		"bottom",
		"left"
	];
	const controlTypeOptions = [
		"regular",
		"flat",
		"outline",
		"push",
		"unelevated"
	];
	var QCarousel_default = createComponent({
		name: "QCarousel",
		props: {
			...useDarkProps,
			...usePanelProps,
			...useFullscreenProps,
			transitionPrev: {
				type: String,
				default: "fade"
			},
			transitionNext: {
				type: String,
				default: "fade"
			},
			height: String,
			padding: Boolean,
			controlColor: String,
			controlTextColor: String,
			controlType: {
				type: String,
				validator: (v) => controlTypeOptions.includes(v),
				default: "flat"
			},
			autoplay: [Number, Boolean],
			arrows: Boolean,
			prevIcon: String,
			nextIcon: String,
			navigation: Boolean,
			navigationPosition: {
				type: String,
				validator: (v) => navigationPositionOptions.includes(v)
			},
			navigationIcon: String,
			navigationActiveIcon: String,
			thumbnails: Boolean
		},
		emits: [...useFullscreenEmits, ...usePanelEmits],
		setup(props, { slots }) {
			const { proxy: { $q } } = (0, vue.getCurrentInstance)();
			const isDark = useDark(props, $q);
			let timer = null, panelsLen;
			const { updatePanelsList, updatePanelIndex, getPanelContent, panelDirectives, goToPanel, previousPanel, nextPanel, getEnabledPanels, panelIndex } = usePanel();
			const { inFullscreen } = useFullscreen();
			const style = (0, vue.computed)(() => !inFullscreen.value && props.height !== void 0 ? { height: props.height } : {});
			const direction = (0, vue.computed)(() => props.vertical ? "vertical" : "horizontal");
			const navigationPosition = (0, vue.computed)(() => props.navigationPosition || (props.vertical ? "right" : "bottom"));
			const classes = (0, vue.computed)(() => `q-carousel q-panel-parent q-carousel--with${props.padding ? "" : "out"}-padding` + (inFullscreen.value ? " fullscreen" : "") + (isDark.value ? " q-carousel--dark q-dark" : "") + (props.arrows ? ` q-carousel--arrows-${direction.value}` : "") + (props.navigation ? ` q-carousel--navigation-${navigationPosition.value}` : ""));
			const arrowIcons = (0, vue.computed)(() => {
				const ico = [props.prevIcon || $q.iconSet.carousel[props.vertical ? "up" : "left"], props.nextIcon || $q.iconSet.carousel[props.vertical ? "down" : "right"]];
				return !props.vertical && $q.lang.rtl ? ico.reverse() : ico;
			});
			const navIcon = (0, vue.computed)(() => props.navigationIcon || $q.iconSet.carousel.navigationIcon);
			const navActiveIcon = (0, vue.computed)(() => props.navigationActiveIcon || navIcon.value);
			const controlProps = (0, vue.computed)(() => ({
				color: props.controlColor,
				textColor: props.controlTextColor,
				round: true,
				[props.controlType]: true,
				dense: true
			}));
			(0, vue.watch)(() => props.modelValue, () => {
				if (props.autoplay) startTimer();
			});
			(0, vue.watch)(() => props.autoplay, (val) => {
				if (val) startTimer();
				else if (timer !== null) {
					clearTimeout(timer);
					timer = null;
				}
			});
			function startTimer() {
				const duration = isNumber(props.autoplay) ? Math.abs(props.autoplay) : 5e3;
				if (timer !== null) clearTimeout(timer);
				timer = setTimeout(() => {
					timer = null;
					if (duration >= 0) nextPanel();
					else previousPanel();
				}, duration);
			}
			(0, vue.onMounted)(() => {
				if (props.autoplay) startTimer();
			});
			(0, vue.onBeforeUnmount)(() => {
				if (timer !== null) clearTimeout(timer);
			});
			function getNavigationContainer(type, mapping) {
				return (0, vue.h)("div", { class: `q-carousel__control q-carousel__navigation no-wrap absolute flex q-carousel__navigation--${type} q-carousel__navigation--${navigationPosition.value}` + (props.controlColor !== void 0 ? ` text-${props.controlColor}` : "") }, [(0, vue.h)("div", { class: "q-carousel__navigation-inner flex flex-center no-wrap" }, getEnabledPanels().map(mapping))]);
			}
			function getContent() {
				const node = [];
				if (props.navigation) {
					const fn = slots["navigation-icon"] !== void 0 ? slots["navigation-icon"] : (opts) => (0, vue.h)(QBtn_default, {
						key: "nav" + opts.name,
						class: `q-carousel__navigation-icon q-carousel__navigation-icon--${opts.active === true ? "" : "in"}active`,
						...opts.btnProps,
						onClick: opts.onClick
					});
					const maxIndex = panelsLen - 1;
					node.push(getNavigationContainer("buttons", (panel, index) => {
						const name = panel.props.name;
						const active = panelIndex.value === index;
						return fn({
							index,
							maxIndex,
							name,
							active,
							btnProps: {
								icon: active ? navActiveIcon.value : navIcon.value,
								size: "sm",
								...controlProps.value
							},
							onClick: () => {
								goToPanel(name);
							}
						});
					}));
				} else if (props.thumbnails) {
					const color = props.controlColor !== void 0 ? ` text-${props.controlColor}` : "";
					node.push(getNavigationContainer("thumbnails", (panel) => {
						const slide = panel.props;
						return (0, vue.h)("img", {
							key: "tmb#" + slide.name,
							class: `q-carousel__thumbnail q-carousel__thumbnail--${slide.name === props.modelValue ? "" : "in"}active` + color,
							src: slide.imgSrc || slide["img-src"],
							onClick: () => {
								goToPanel(slide.name);
							}
						});
					}));
				}
				if (props.arrows && panelIndex.value >= 0) {
					if (props.infinite || panelIndex.value > 0) node.push((0, vue.h)("div", {
						key: "prev",
						class: `q-carousel__control q-carousel__arrow q-carousel__prev-arrow q-carousel__prev-arrow--${direction.value} absolute flex flex-center`
					}, [(0, vue.h)(QBtn_default, {
						icon: arrowIcons.value[0],
						...controlProps.value,
						onClick: previousPanel
					})]));
					if (props.infinite || panelIndex.value < panelsLen - 1) node.push((0, vue.h)("div", {
						key: "next",
						class: `q-carousel__control q-carousel__arrow q-carousel__next-arrow q-carousel__next-arrow--${direction.value} absolute flex flex-center`
					}, [(0, vue.h)(QBtn_default, {
						icon: arrowIcons.value[1],
						...controlProps.value,
						onClick: nextPanel
					})]));
				}
				return hMergeSlot(slots.control, node);
			}
			return () => {
				panelsLen = updatePanelsList(slots);
				updatePanelIndex();
				return (0, vue.h)("div", {
					class: classes.value,
					style: style.value
				}, [hDir("div", { class: "q-carousel__slides-container" }, getPanelContent(), "sl-cont", props.swipeable, () => panelDirectives.value), ...getContent()]);
			};
		}
	});
	//#endregion
	//#region src/components/carousel/QCarouselSlide.js
	var QCarouselSlide_default = createComponent({
		name: "QCarouselSlide",
		props: {
			...usePanelChildProps,
			imgSrc: String
		},
		setup(props, { slots }) {
			const style = (0, vue.computed)(() => props.imgSrc ? { backgroundImage: `url("${props.imgSrc}")` } : {});
			return () => (0, vue.h)("div", {
				class: "q-carousel__slide",
				style: style.value
			}, hSlot(slots.default));
		}
	});
	//#endregion
	//#region src/components/carousel/QCarouselControl.js
	var QCarouselControl_default = createComponent({
		name: "QCarouselControl",
		props: {
			position: {
				type: String,
				default: "bottom-right",
				validator: (v) => [
					"top-right",
					"top-left",
					"bottom-right",
					"bottom-left",
					"top",
					"right",
					"bottom",
					"left"
				].includes(v)
			},
			offset: {
				type: Array,
				default: () => [18, 18],
				validator: (v) => v.length === 2
			}
		},
		setup(props, { slots }) {
			const classes = (0, vue.computed)(() => `q-carousel__control absolute absolute-${props.position}`);
			const style = (0, vue.computed)(() => ({ margin: `${props.offset[1]}px ${props.offset[0]}px` }));
			return () => (0, vue.h)("div", {
				class: classes.value,
				style: style.value
			}, hSlot(slots.default));
		}
	});
	//#endregion
	//#region src/components/chat/QChatMessage.js
	var QChatMessage_default = createComponent({
		name: "QChatMessage",
		props: {
			sent: Boolean,
			label: String,
			bgColor: String,
			textColor: String,
			name: String,
			avatar: String,
			text: Array,
			stamp: String,
			size: String,
			labelHtml: Boolean,
			nameHtml: Boolean,
			textHtml: Boolean,
			stampHtml: Boolean
		},
		setup(props, { slots }) {
			const op = (0, vue.computed)(() => props.sent ? "sent" : "received");
			const textClass = (0, vue.computed)(() => `q-message-text-content q-message-text-content--${op.value}` + (props.textColor !== void 0 ? ` text-${props.textColor}` : ""));
			const messageClass = (0, vue.computed)(() => `q-message-text q-message-text--${op.value}` + (props.bgColor !== void 0 ? ` text-${props.bgColor}` : ""));
			const containerClass = (0, vue.computed)(() => "q-message-container row items-end no-wrap" + (props.sent ? " reverse" : ""));
			const sizeClass = (0, vue.computed)(() => props.size !== void 0 ? `col-${props.size}` : "");
			const domProps = (0, vue.computed)(() => ({
				msg: props.textHtml ? "innerHTML" : "textContent",
				stamp: props.stampHtml ? "innerHTML" : "textContent",
				name: props.nameHtml ? "innerHTML" : "textContent",
				label: props.labelHtml ? "innerHTML" : "textContent"
			}));
			function wrapStamp(node) {
				if (slots.stamp !== void 0) return [node, (0, vue.h)("div", { class: "q-message-stamp" }, slots.stamp())];
				if (props.stamp) return [node, (0, vue.h)("div", {
					class: "q-message-stamp",
					[domProps.value.stamp]: props.stamp
				})];
				return [node];
			}
			function getText(contentList, withSlots) {
				const content = withSlots ? contentList.length > 1 ? (text) => text : (text) => (0, vue.h)("div", [text]) : (text) => (0, vue.h)("div", { [domProps.value.msg]: text });
				return contentList.map((msg, index) => (0, vue.h)("div", {
					key: index,
					class: messageClass.value
				}, [(0, vue.h)("div", { class: textClass.value }, wrapStamp(content(msg)))]));
			}
			return () => {
				const container = [];
				if (slots.avatar !== void 0) container.push(slots.avatar());
				else if (props.avatar !== void 0) container.push((0, vue.h)("img", {
					class: `q-message-avatar q-message-avatar--${op.value}`,
					src: props.avatar,
					"aria-hidden": "true"
				}));
				const msg = [];
				if (slots.name !== void 0) msg.push((0, vue.h)("div", { class: `q-message-name q-message-name--${op.value}` }, slots.name()));
				else if (props.name !== void 0) msg.push((0, vue.h)("div", {
					class: `q-message-name q-message-name--${op.value}`,
					[domProps.value.name]: props.name
				}));
				if (slots.default !== void 0) msg.push(getText(getNormalizedVNodes(slots.default()), true));
				else if (props.text !== void 0) msg.push(getText(props.text, false));
				container.push((0, vue.h)("div", { class: sizeClass.value }, msg));
				const child = [];
				if (slots.label !== void 0) child.push((0, vue.h)("div", { class: "q-message-label" }, slots.label()));
				else if (props.label !== void 0) child.push((0, vue.h)("div", {
					class: "q-message-label",
					[domProps.value.label]: props.label
				}));
				child.push((0, vue.h)("div", { class: containerClass.value }, container));
				return (0, vue.h)("div", { class: `q-message q-message-${op.value}` }, child);
			};
		}
	});
	//#endregion
	//#region src/composables/private.use-refocus-target/use-refocus-target.js
	function useRefocusTarget(props, rootRef) {
		const refocusRef = (0, vue.ref)(null);
		const refocusTargetEl = (0, vue.computed)(() => {
			if (props.disable) return null;
			return (0, vue.h)("span", {
				ref: refocusRef,
				class: "no-outline",
				tabindex: -1
			});
		});
		function refocusTarget(e) {
			const root = rootRef.value;
			if (e?.qAvoidFocus === true) return;
			if (e?.type.indexOf("key") === 0) {
				if (document.activeElement !== root && root?.contains(document.activeElement) === true) root.focus();
			} else if (refocusRef.value !== null && (e === void 0 || root?.contains(e.target) === true)) refocusRef.value.focus();
		}
		return {
			refocusTargetEl,
			refocusTarget
		};
	}
	//#endregion
	//#region src/utils/private.option-sizes/option-sizes.js
	var option_sizes_default = {
		xs: 30,
		sm: 35,
		md: 40,
		lg: 50,
		xl: 60
	};
	//#endregion
	//#region src/components/checkbox/use-checkbox.js
	const useCheckboxProps = {
		...useDarkProps,
		...useSizeProps,
		...useFormProps,
		modelValue: {
			required: true,
			default: null
		},
		val: {},
		trueValue: { default: true },
		falseValue: { default: false },
		indeterminateValue: { default: null },
		checkedIcon: String,
		uncheckedIcon: String,
		indeterminateIcon: String,
		toggleOrder: {
			type: String,
			validator: (v) => v === "tf" || v === "ft"
		},
		toggleIndeterminate: Boolean,
		label: String,
		leftLabel: Boolean,
		color: String,
		keepColor: Boolean,
		dense: Boolean,
		disable: Boolean,
		tabindex: [String, Number]
	};
	const useCheckboxEmits = ["update:modelValue"];
	function onKeydown$2(e) {
		if (e.keyCode === 13 || e.keyCode === 32) stopAndPrevent(e);
	}
	function useCheckbox(type, getInner) {
		const { props, slots, emit, proxy } = (0, vue.getCurrentInstance)();
		const { $q } = proxy;
		const isDark = useDark(props, $q);
		const rootRef = (0, vue.ref)(null);
		const { refocusTargetEl, refocusTarget } = useRefocusTarget(props, rootRef);
		const sizeStyle = useSize(props, option_sizes_default);
		const modelIsArray = (0, vue.computed)(() => props.val !== void 0 && Array.isArray(props.modelValue));
		const index = (0, vue.computed)(() => {
			const val = (0, vue.toRaw)(props.val);
			return modelIsArray.value ? props.modelValue.findIndex((opt) => (0, vue.toRaw)(opt) === val) : -1;
		});
		const isTrue = (0, vue.computed)(() => modelIsArray.value ? index.value !== -1 : (0, vue.toRaw)(props.modelValue) === (0, vue.toRaw)(props.trueValue));
		const isFalse = (0, vue.computed)(() => modelIsArray.value ? index.value === -1 : (0, vue.toRaw)(props.modelValue) === (0, vue.toRaw)(props.falseValue));
		const isIndeterminate = (0, vue.computed)(() => !isTrue.value && !isFalse.value);
		const tabindex = (0, vue.computed)(() => props.disable ? -1 : props.tabindex || 0);
		const classes = (0, vue.computed)(() => `q-${type} cursor-pointer no-outline row inline no-wrap items-center` + (props.disable ? " disabled" : "") + (isDark.value ? ` q-${type}--dark` : "") + (props.dense ? ` q-${type}--dense` : "") + (props.leftLabel ? " reverse" : ""));
		const innerClass = (0, vue.computed)(() => {
			return `q-${type}__inner relative-position non-selectable q-${type}__inner--${isTrue.value ? "truthy" : isFalse.value ? "falsy" : "indet"}${props.color !== void 0 && (props.keepColor || (type === "toggle" ? isTrue.value : !isFalse.value)) ? ` text-${props.color}` : ""}`;
		});
		const injectFormInput = useFormInject((0, vue.computed)(() => {
			const prop = { type: "checkbox" };
			if (props.name !== void 0) Object.assign(prop, {
				".checked": isTrue.value,
				"^checked": isTrue.value ? "checked" : void 0,
				name: props.name,
				value: modelIsArray.value ? props.val : props.trueValue
			});
			return prop;
		}));
		const attributes = (0, vue.computed)(() => {
			const attrs = {
				tabindex: tabindex.value,
				role: type === "toggle" ? "switch" : "checkbox",
				"aria-label": props.label,
				"aria-checked": isIndeterminate.value ? "mixed" : isTrue.value ? "true" : "false"
			};
			if (props.disable) attrs["aria-disabled"] = "true";
			return attrs;
		});
		function onClick(e) {
			if (e !== void 0) {
				stopAndPrevent(e);
				refocusTarget(e);
			}
			if (!props.disable) emit("update:modelValue", getNextValue(), e);
		}
		function getNextValue() {
			if (modelIsArray.value) {
				if (isTrue.value) {
					const val = [...props.modelValue];
					val.splice(index.value, 1);
					return val;
				}
				return [...props.modelValue, props.val];
			}
			if (isTrue.value) {
				if (props.toggleOrder !== "ft" || !props.toggleIndeterminate) return props.falseValue;
			} else if (isFalse.value) {
				if (props.toggleOrder === "ft" || !props.toggleIndeterminate) return props.trueValue;
			} else return props.toggleOrder !== "ft" ? props.trueValue : props.falseValue;
			return props.indeterminateValue;
		}
		function onKeyup(e) {
			if (e.keyCode === 13 || e.keyCode === 32) onClick(e);
		}
		const getInnerContent = getInner(isTrue, isIndeterminate);
		Object.assign(proxy, { toggle: onClick });
		return () => {
			const inner = getInnerContent();
			if (!props.disable) injectFormInput(inner, "unshift", ` q-${type}__native absolute q-ma-none q-pa-none`);
			const child = [(0, vue.h)("div", {
				class: innerClass.value,
				style: sizeStyle.value,
				"aria-hidden": "true"
			}, inner)];
			if (refocusTargetEl.value !== null) child.push(refocusTargetEl.value);
			const label = props.label !== void 0 ? hMergeSlot(slots.default, [props.label]) : hSlot(slots.default);
			if (label !== void 0) child.push((0, vue.h)("div", { class: `q-${type}__label q-anchor--skip` }, label));
			return (0, vue.h)("div", {
				ref: rootRef,
				class: classes.value,
				...attributes.value,
				onClick,
				onKeydown: onKeydown$2,
				onKeyup
			}, child);
		};
	}
	//#endregion
	//#region src/components/checkbox/QCheckbox.js
	const createBgNode = () => (0, vue.h)("div", {
		key: "svg",
		class: "q-checkbox__bg absolute"
	}, [(0, vue.h)("svg", {
		class: "q-checkbox__svg fit absolute-full",
		viewBox: "0 0 24 24"
	}, [(0, vue.h)("path", {
		class: "q-checkbox__truthy",
		fill: "none",
		d: "M1.73,12.91 8.1,19.28 22.79,4.59"
	}), (0, vue.h)("path", {
		class: "q-checkbox__indet",
		d: "M4,14H20V10H4"
	})])]);
	var QCheckbox_default = createComponent({
		name: "QCheckbox",
		props: useCheckboxProps,
		emits: useCheckboxEmits,
		setup(props) {
			const bgNode = createBgNode();
			function getInner(isTrue, isIndeterminate) {
				const icon = (0, vue.computed)(() => (isTrue.value ? props.checkedIcon : isIndeterminate.value ? props.indeterminateIcon : props.uncheckedIcon) || null);
				return () => icon.value !== null ? [(0, vue.h)("div", {
					key: "icon",
					class: "q-checkbox__icon-container absolute-full flex flex-center no-wrap"
				}, [(0, vue.h)(QIcon_default, {
					class: "q-checkbox__icon",
					name: icon.value
				})])] : [bgNode];
			}
			return useCheckbox("checkbox", getInner);
		}
	});
	//#endregion
	//#region src/components/chip/QChip.js
	function preventSpace$3(e) {
		if (e.keyCode === 32) stopAndPrevent(e);
	}
	const defaultSizes$1 = {
		xs: 8,
		sm: 10,
		md: 14,
		lg: 20,
		xl: 24
	};
	var QChip_default = createComponent({
		name: "QChip",
		props: {
			...useDarkProps,
			...useSizeProps,
			dense: Boolean,
			icon: String,
			iconRight: String,
			iconRemove: String,
			iconSelected: String,
			label: [String, Number],
			color: String,
			textColor: String,
			modelValue: {
				type: Boolean,
				default: true
			},
			selected: {
				type: Boolean,
				default: null
			},
			square: Boolean,
			outline: Boolean,
			clickable: Boolean,
			removable: Boolean,
			removeAriaLabel: String,
			tabindex: [String, Number],
			disable: Boolean,
			ripple: {
				type: [Boolean, Object],
				default: true
			}
		},
		emits: [
			"update:modelValue",
			"update:selected",
			"remove",
			"click"
		],
		setup(props, { slots, emit }) {
			const { proxy: { $q } } = (0, vue.getCurrentInstance)();
			const isDark = useDark(props, $q);
			const sizeStyle = useSize(props, defaultSizes$1);
			const hasLeftIcon = (0, vue.computed)(() => props.selected || props.icon !== void 0);
			const leftIcon = (0, vue.computed)(() => props.selected ? props.iconSelected || $q.iconSet.chip.selected : props.icon);
			const removeIcon = (0, vue.computed)(() => props.iconRemove || $q.iconSet.chip.remove);
			const isClickable = (0, vue.computed)(() => !props.disable && (props.clickable || props.selected !== null));
			const classes = (0, vue.computed)(() => {
				const text = props.outline ? props.color || props.textColor : props.textColor;
				return "q-chip row inline no-wrap items-center" + (!props.outline && props.color !== void 0 ? ` bg-${props.color}` : "") + (text ? ` text-${text} q-chip--colored` : "") + (props.disable ? " disabled" : "") + (props.dense ? " q-chip--dense" : "") + (props.outline ? " q-chip--outline" : "") + (props.selected ? " q-chip--selected" : "") + (isClickable.value ? " q-chip--clickable cursor-pointer non-selectable q-hoverable" : "") + (props.square ? " q-chip--square" : "") + (isDark.value ? " q-chip--dark q-dark" : "");
			});
			const attributes = (0, vue.computed)(() => {
				const chip = props.disable ? {
					tabindex: -1,
					"aria-disabled": "true"
				} : {
					tabindex: props.tabindex || 0,
					role: "button",
					"aria-pressed": props.selected ? "true" : "false"
				};
				return {
					chip,
					remove: {
						...chip,
						role: "button",
						"aria-hidden": "false",
						"aria-label": props.removeAriaLabel || $q.lang.label.remove
					}
				};
			});
			function onKeyup(e) {
				if ([13, 32].includes(e.keyCode)) {
					onClick(e);
					stopAndPrevent(e);
				}
			}
			function onClick(e) {
				if (!props.disable) {
					emit("update:selected", !props.selected);
					emit("click", e);
				}
			}
			function onRemove(e) {
				if (e.keyCode === void 0 || [13, 32].includes(e.keyCode)) {
					stopAndPrevent(e);
					if (!props.disable) {
						emit("update:modelValue", false);
						emit("remove");
					}
				}
			}
			function getContent() {
				const child = [];
				if (isClickable.value) child.push((0, vue.h)("div", { class: "q-focus-helper" }));
				if (hasLeftIcon.value) child.push((0, vue.h)(QIcon_default, {
					class: "q-chip__icon q-chip__icon--left",
					name: leftIcon.value
				}));
				const label = props.label !== void 0 ? [(0, vue.h)("div", { class: "ellipsis" }, [props.label])] : void 0;
				child.push((0, vue.h)("div", { class: "q-chip__content col row no-wrap items-center q-anchor--skip" }, hMergeSlotSafely(slots.default, label)));
				if (props.iconRight) child.push((0, vue.h)(QIcon_default, {
					class: "q-chip__icon q-chip__icon--right",
					name: props.iconRight
				}));
				if (props.removable) child.push((0, vue.h)(QIcon_default, {
					class: "q-chip__icon q-chip__icon--remove cursor-pointer",
					name: removeIcon.value,
					...attributes.value.remove,
					onClick: onRemove,
					onKeydown: preventSpace$3,
					onKeyup: onRemove
				}));
				return child;
			}
			return () => {
				if (!props.modelValue) return;
				const data = {
					class: classes.value,
					style: sizeStyle.value
				};
				if (isClickable.value) Object.assign(data, attributes.value.chip, {
					onClick,
					onKeydown: preventSpace$3,
					onKeyup
				});
				return hDir("div", data, getContent(), "ripple", props.ripple !== false && !props.disable, () => [[Ripple_default, props.ripple]]);
			};
		}
	});
	//#endregion
	//#region src/components/circular-progress/circular-progress.js
	const useCircularCommonProps = {
		...useSizeProps,
		min: {
			type: Number,
			default: 0
		},
		max: {
			type: Number,
			default: 100
		},
		color: String,
		centerColor: String,
		trackColor: String,
		fontSize: String,
		rounded: Boolean,
		thickness: {
			type: Number,
			default: .2,
			validator: (v) => v >= 0 && v <= 1
		},
		angle: {
			type: Number,
			default: 0
		},
		showValue: Boolean,
		reverse: Boolean,
		instantFeedback: Boolean
	};
	//#endregion
	//#region src/components/circular-progress/QCircularProgress.js
	const radius = 50;
	const diameter = 2 * radius;
	const circumference = diameter * Math.PI;
	const strokeDashArray = Math.round(circumference * 1e3) / 1e3;
	var QCircularProgress_default = createComponent({
		name: "QCircularProgress",
		props: {
			...useCircularCommonProps,
			value: {
				type: Number,
				default: 0
			},
			animationSpeed: {
				type: [String, Number],
				default: 600
			},
			indeterminate: Boolean
		},
		setup(props, { slots }) {
			const { proxy: { $q } } = (0, vue.getCurrentInstance)();
			const sizeStyle = useSize(props);
			const svgStyle = (0, vue.computed)(() => {
				const angle = ($q.lang.rtl ? -1 : 1) * props.angle;
				return { transform: props.reverse !== ($q.lang.rtl === true) ? `scale3d(-1, 1, 1) rotate3d(0, 0, 1, ${-90 - angle}deg)` : `rotate3d(0, 0, 1, ${angle - 90}deg)` };
			});
			const circleStyle = (0, vue.computed)(() => !props.instantFeedback && !props.indeterminate ? { transition: `stroke-dashoffset ${props.animationSpeed}ms ease 0s, stroke ${props.animationSpeed}ms ease` } : "");
			const viewBox = (0, vue.computed)(() => diameter / (1 - props.thickness / 2));
			const viewBoxAttr = (0, vue.computed)(() => `${viewBox.value / 2} ${viewBox.value / 2} ${viewBox.value} ${viewBox.value}`);
			const normalized = (0, vue.computed)(() => between(props.value, props.min, props.max));
			const range = (0, vue.computed)(() => props.max - props.min);
			const strokeWidth = (0, vue.computed)(() => props.thickness / 2 * viewBox.value);
			const strokeDashOffset = (0, vue.computed)(() => {
				const dashRatio = (props.max - normalized.value) / range.value;
				const dashGap = props.rounded && normalized.value < props.max && dashRatio < .25 ? strokeWidth.value / 2 * (1 - dashRatio / .25) : 0;
				return circumference * dashRatio + dashGap;
			});
			function getCircle({ thickness, offset, color, cls, rounded }) {
				return (0, vue.h)("circle", {
					class: "q-circular-progress__" + cls + (color !== void 0 ? ` text-${color}` : ""),
					style: circleStyle.value,
					fill: "transparent",
					stroke: "currentColor",
					"stroke-width": thickness,
					"stroke-dasharray": strokeDashArray,
					"stroke-dashoffset": offset,
					"stroke-linecap": rounded,
					cx: viewBox.value,
					cy: viewBox.value,
					r: radius
				});
			}
			return () => {
				const svgChild = [];
				if (props.centerColor !== void 0 && props.centerColor !== "transparent") svgChild.push((0, vue.h)("circle", {
					class: `q-circular-progress__center text-${props.centerColor}`,
					fill: "currentColor",
					r: radius - strokeWidth.value / 2,
					cx: viewBox.value,
					cy: viewBox.value
				}));
				if (props.trackColor !== void 0 && props.trackColor !== "transparent") svgChild.push(getCircle({
					cls: "track",
					thickness: strokeWidth.value,
					offset: 0,
					color: props.trackColor
				}));
				svgChild.push(getCircle({
					cls: "circle",
					thickness: strokeWidth.value,
					offset: strokeDashOffset.value,
					color: props.color,
					rounded: props.rounded ? "round" : void 0
				}));
				const child = [(0, vue.h)("svg", {
					class: "q-circular-progress__svg",
					style: svgStyle.value,
					viewBox: viewBoxAttr.value,
					"aria-hidden": "true"
				}, svgChild)];
				if (props.showValue) child.push((0, vue.h)("div", {
					class: "q-circular-progress__text absolute-full row flex-center content-center",
					style: { fontSize: props.fontSize }
				}, slots.default !== void 0 ? slots.default() : [(0, vue.h)("div", normalized.value)]));
				return (0, vue.h)("div", {
					class: `q-circular-progress q-circular-progress--${props.indeterminate ? "in" : ""}determinate`,
					style: sizeStyle.value,
					role: "progressbar",
					"aria-valuemin": props.min,
					"aria-valuemax": props.max,
					"aria-valuenow": props.indeterminate ? void 0 : normalized.value
				}, hMergeSlotSafely(slots.internal, child));
			};
		}
	});
	//#endregion
	//#region src/directives/touch-pan/TouchPan.js
	function getChanges(evt, ctx, isFinal) {
		const pos = position(evt);
		let dir, distX = pos.left - ctx.event.x, distY = pos.top - ctx.event.y, absX = Math.abs(distX), absY = Math.abs(distY);
		const direction = ctx.direction;
		if (direction.horizontal && !direction.vertical) dir = distX < 0 ? "left" : "right";
		else if (!direction.horizontal && direction.vertical) dir = distY < 0 ? "up" : "down";
		else if (direction.up && distY < 0) {
			dir = "up";
			if (absX > absY) {
				if (direction.left && distX < 0) dir = "left";
				else if (direction.right && distX > 0) dir = "right";
			}
		} else if (direction.down && distY > 0) {
			dir = "down";
			if (absX > absY) {
				if (direction.left && distX < 0) dir = "left";
				else if (direction.right && distX > 0) dir = "right";
			}
		} else if (direction.left && distX < 0) {
			dir = "left";
			if (absX < absY) {
				if (direction.up && distY < 0) dir = "up";
				else if (direction.down && distY > 0) dir = "down";
			}
		} else if (direction.right && distX > 0) {
			dir = "right";
			if (absX < absY) {
				if (direction.up && distY < 0) dir = "up";
				else if (direction.down && distY > 0) dir = "down";
			}
		}
		let synthetic = false;
		if (dir === void 0 && isFinal === false) {
			if (ctx.event.isFirst || ctx.event.lastDir === void 0) return {};
			dir = ctx.event.lastDir;
			synthetic = true;
			if (dir === "left" || dir === "right") {
				pos.left -= distX;
				absX = 0;
				distX = 0;
			} else {
				pos.top -= distY;
				absY = 0;
				distY = 0;
			}
		}
		return {
			synthetic,
			payload: {
				evt,
				touch: ctx.event.mouse !== true,
				mouse: ctx.event.mouse === true,
				position: pos,
				direction: dir,
				isFirst: ctx.event.isFirst,
				isFinal: isFinal === true,
				duration: Date.now() - ctx.event.time,
				distance: {
					x: absX,
					y: absY
				},
				offset: {
					x: distX,
					y: distY
				},
				delta: {
					x: pos.left - ctx.event.lastX,
					y: pos.top - ctx.event.lastY
				}
			}
		};
	}
	function removeChildrenNoPointerEvents() {
		document.body.classList.remove("no-pointer-events--children");
	}
	let uid$2 = 0;
	var TouchPan_default = createDirective({
		name: "touch-pan",
		beforeMount(el, { value, modifiers }) {
			if (!modifiers.mouse && !client.has.touch) return;
			function handleEvent(evt, mouseEvent) {
				if (modifiers.mouse && mouseEvent) stopAndPrevent(evt);
				else {
					if (modifiers.stop) stop(evt);
					if (modifiers.prevent) prevent(evt);
				}
			}
			const ctx = {
				uid: "qvtp_" + uid$2++,
				handler: value,
				modifiers,
				direction: getModifierDirections(modifiers),
				noop,
				mouseStart(evt) {
					if (shouldStart(evt, ctx) && leftClick(evt)) {
						addEvt(ctx, "temp", [[
							document,
							"mousemove",
							"move",
							"notPassiveCapture"
						], [
							document,
							"mouseup",
							"end",
							"passiveCapture"
						]]);
						ctx.start(evt, true);
					}
				},
				touchStart(evt) {
					if (shouldStart(evt, ctx)) {
						const target = evt.target;
						addEvt(ctx, "temp", [
							[
								target,
								"touchmove",
								"move",
								"notPassiveCapture"
							],
							[
								target,
								"touchcancel",
								"end",
								"passiveCapture"
							],
							[
								target,
								"touchend",
								"end",
								"passiveCapture"
							]
						]);
						ctx.start(evt);
					}
				},
				start(evt, mouseEvent) {
					if (client.is.firefox) preventDraggable(el, true);
					ctx.lastEvt = evt;
					if (mouseEvent || modifiers.stop) {
						if (!ctx.direction.all && (!mouseEvent || !ctx.modifiers.mouseAllDir && !ctx.modifiers.mousealldir)) {
							const clone = evt.type.includes("mouse") ? new MouseEvent(evt.type, evt) : new TouchEvent(evt.type, evt);
							if (evt.defaultPrevented) prevent(clone);
							if (evt.cancelBubble) stop(clone);
							Object.assign(clone, {
								qKeyEvent: evt.qKeyEvent,
								qClickOutside: evt.qClickOutside,
								qAnchorHandled: evt.qAnchorHandled,
								qClonedBy: evt.qClonedBy === void 0 ? [ctx.uid] : evt.qClonedBy.concat(ctx.uid)
							});
							ctx.initialEvent = {
								target: evt.target,
								event: clone
							};
						}
						stop(evt);
					}
					const { left, top } = position(evt);
					ctx.event = {
						x: left,
						y: top,
						time: Date.now(),
						mouse: mouseEvent === true,
						detected: false,
						isFirst: true,
						isFinal: false,
						lastX: left,
						lastY: top
					};
				},
				move(evt) {
					if (ctx.event === void 0) return;
					const pos = position(evt), distX = pos.left - ctx.event.x, distY = pos.top - ctx.event.y;
					if (distX === 0 && distY === 0) return;
					ctx.lastEvt = evt;
					const isMouseEvt = ctx.event.mouse === true;
					const start = () => {
						handleEvent(evt, isMouseEvt);
						let cursor;
						if (!modifiers.preserveCursor && !modifiers.preservecursor) {
							cursor = document.documentElement.style.cursor || "";
							document.documentElement.style.cursor = "grabbing";
						}
						if (isMouseEvt) document.body.classList.add("no-pointer-events--children");
						document.body.classList.add("non-selectable");
						clearSelection();
						ctx.styleCleanup = (withDelayedFn) => {
							ctx.styleCleanup = void 0;
							if (cursor !== void 0) document.documentElement.style.cursor = cursor;
							document.body.classList.remove("non-selectable");
							if (isMouseEvt) if (withDelayedFn !== void 0) setTimeout(() => {
								removeChildrenNoPointerEvents();
								withDelayedFn();
							}, 50);
							else removeChildrenNoPointerEvents();
							else if (withDelayedFn !== void 0) withDelayedFn();
						};
					};
					if (ctx.event.detected) {
						if (!ctx.event.isFirst) handleEvent(evt, ctx.event.mouse);
						const { payload, synthetic } = getChanges(evt, ctx, false);
						if (payload !== void 0) if (ctx.handler(payload) === false) ctx.end(evt);
						else {
							if (ctx.styleCleanup === void 0 && ctx.event.isFirst) start();
							ctx.event.lastX = payload.position.left;
							ctx.event.lastY = payload.position.top;
							ctx.event.lastDir = synthetic ? void 0 : payload.direction;
							ctx.event.isFirst = false;
						}
						return;
					}
					if (ctx.direction.all || isMouseEvt && (ctx.modifiers.mouseAllDir || ctx.modifiers.mousealldir)) {
						start();
						ctx.event.detected = true;
						ctx.move(evt);
						return;
					}
					const absX = Math.abs(distX), absY = Math.abs(distY);
					if (absX !== absY) if (ctx.direction.horizontal && absX > absY || ctx.direction.vertical && absX < absY || ctx.direction.up && absX < absY && distY < 0 || ctx.direction.down && absX < absY && distY > 0 || ctx.direction.left && absX > absY && distX < 0 || ctx.direction.right && absX > absY && distX > 0) {
						ctx.event.detected = true;
						ctx.move(evt);
					} else ctx.end(evt, true);
				},
				end(evt, abort) {
					if (ctx.event === void 0) return;
					cleanEvt(ctx, "temp");
					if (client.is.firefox) preventDraggable(el, false);
					if (abort) {
						ctx.styleCleanup?.();
						if (!ctx.event.detected && ctx.initialEvent !== void 0) ctx.initialEvent.target.dispatchEvent(ctx.initialEvent.event);
					} else if (ctx.event.detected) {
						if (ctx.event.isFirst) ctx.handler(getChanges(evt === void 0 ? ctx.lastEvt : evt, ctx).payload);
						const { payload } = getChanges(evt === void 0 ? ctx.lastEvt : evt, ctx, true);
						const fn = () => {
							ctx.handler(payload);
						};
						if (ctx.styleCleanup !== void 0) ctx.styleCleanup(fn);
						else fn();
					}
					ctx.event = void 0;
					ctx.initialEvent = void 0;
					ctx.lastEvt = void 0;
				}
			};
			el.__qtouchpan = ctx;
			if (modifiers.mouse) addEvt(ctx, "main", [[
				el,
				"mousedown",
				"mouseStart",
				`passive${modifiers.mouseCapture || modifiers.mousecapture ? "Capture" : ""}`
			]]);
			if (client.has.touch) addEvt(ctx, "main", [[
				el,
				"touchstart",
				"touchStart",
				`passive${modifiers.capture ? "Capture" : ""}`
			], [
				el,
				"touchmove",
				"noop",
				"notPassiveCapture"
			]]);
		},
		updated(el, bindings) {
			const ctx = el.__qtouchpan;
			if (ctx !== void 0) {
				if (bindings.oldValue !== bindings.value) {
					if (typeof value !== "function") ctx.end();
					ctx.handler = bindings.value;
				}
				ctx.direction = getModifierDirections(bindings.modifiers);
			}
		},
		beforeUnmount(el) {
			const ctx = el.__qtouchpan;
			if (ctx !== void 0) {
				if (ctx.event !== void 0) ctx.end();
				cleanEvt(ctx, "main");
				cleanEvt(ctx, "temp");
				if (client.is.firefox) preventDraggable(el, false);
				ctx.styleCleanup?.();
				delete el.__qtouchpan;
			}
		}
	});
	//#endregion
	//#region src/components/slider/use-slider.js
	const markerPrefixClass = "q-slider__marker-labels";
	const defaultMarkerConvertFn = (v) => ({ value: v });
	const defaultMarkerLabelRenderFn = ({ marker }) => (0, vue.h)("div", {
		key: marker.value,
		style: marker.style,
		class: marker.classes
	}, marker.label);
	const keyCodes$2 = [
		34,
		37,
		40,
		33,
		39,
		38
	];
	const useSliderProps = {
		...useDarkProps,
		...useFormProps,
		min: {
			type: Number,
			default: 0
		},
		max: {
			type: Number,
			default: 100
		},
		innerMin: Number,
		innerMax: Number,
		step: {
			type: Number,
			default: 1,
			validator: (v) => v >= 0
		},
		snap: Boolean,
		vertical: Boolean,
		reverse: Boolean,
		color: String,
		markerLabelsClass: String,
		label: Boolean,
		labelColor: String,
		labelTextColor: String,
		labelAlways: Boolean,
		switchLabelSide: Boolean,
		markers: [Boolean, Number],
		markerLabels: [
			Boolean,
			Array,
			Object,
			Function
		],
		switchMarkerLabelsSide: Boolean,
		trackImg: String,
		trackColor: String,
		innerTrackImg: String,
		innerTrackColor: String,
		selectionColor: String,
		selectionImg: String,
		thumbSize: {
			type: String,
			default: "20px"
		},
		trackSize: {
			type: String,
			default: "4px"
		},
		disable: Boolean,
		readonly: Boolean,
		dense: Boolean,
		tabindex: [String, Number],
		thumbColor: String,
		thumbPath: {
			type: String,
			default: "M 4, 10 a 6,6 0 1,0 12,0 a 6,6 0 1,0 -12,0"
		}
	};
	const useSliderEmits = [
		"pan",
		"update:modelValue",
		"change"
	];
	function useSlider({ updateValue, updatePosition, getDragging, formAttrs }) {
		const { props, emit, slots, proxy: { $q } } = (0, vue.getCurrentInstance)();
		const isDark = useDark(props, $q);
		const injectFormInput = useFormInject(formAttrs);
		const active = (0, vue.ref)(false);
		const preventFocus = (0, vue.ref)(false);
		const focus = (0, vue.ref)(false);
		const dragging = (0, vue.ref)(false);
		const axis = (0, vue.computed)(() => props.vertical ? "--v" : "--h");
		const labelSide = (0, vue.computed)(() => "-" + (props.switchLabelSide ? "switched" : "standard"));
		const isReversed = (0, vue.computed)(() => props.vertical ? props.reverse : props.reverse !== ($q.lang.rtl === true));
		const innerMin = (0, vue.computed)(() => !Number.isFinite(props.innerMin) || props.innerMin < props.min ? props.min : props.innerMin);
		const innerMax = (0, vue.computed)(() => !Number.isFinite(props.innerMax) || props.innerMax > props.max ? props.max : props.innerMax);
		const editable = (0, vue.computed)(() => !props.disable && !props.readonly && innerMin.value < innerMax.value);
		const roundValueFn = (0, vue.computed)(() => {
			if (props.step === 0) return (v) => v;
			const decimals = (String(props.step).trim().split(".")[1] || "").length;
			return (v) => Number.parseFloat(v.toFixed(decimals));
		});
		const keyStep = (0, vue.computed)(() => props.step === 0 ? 1 : props.step);
		const tabindex = (0, vue.computed)(() => editable.value ? props.tabindex || 0 : -1);
		const trackLen = (0, vue.computed)(() => props.max - props.min);
		const innerBarLen = (0, vue.computed)(() => innerMax.value - innerMin.value);
		const innerMinRatio = (0, vue.computed)(() => convertModelToRatio(innerMin.value));
		const innerMaxRatio = (0, vue.computed)(() => convertModelToRatio(innerMax.value));
		const positionProp = (0, vue.computed)(() => props.vertical ? isReversed.value ? "bottom" : "top" : isReversed.value ? "right" : "left");
		const sizeProp = (0, vue.computed)(() => props.vertical ? "height" : "width");
		const thicknessProp = (0, vue.computed)(() => props.vertical ? "width" : "height");
		const orientation = (0, vue.computed)(() => props.vertical ? "vertical" : "horizontal");
		const attributes = (0, vue.computed)(() => {
			const acc = {
				role: "slider",
				"aria-valuemin": innerMin.value,
				"aria-valuemax": innerMax.value,
				"aria-orientation": orientation.value,
				"data-step": props.step
			};
			if (props.disable) acc["aria-disabled"] = "true";
			else if (props.readonly) acc["aria-readonly"] = "true";
			return acc;
		});
		const classes = (0, vue.computed)(() => `q-slider q-slider${axis.value} q-slider--${active.value ? "" : "in"}active inline no-wrap ` + (props.vertical ? "row" : "column") + (props.disable ? " disabled" : " q-slider--enabled" + (editable.value ? " q-slider--editable" : "")) + (focus.value === "both" ? " q-slider--focus" : "") + (props.label || props.labelAlways ? " q-slider--label" : "") + (props.labelAlways ? " q-slider--label-always" : "") + (isDark.value ? " q-slider--dark" : "") + (props.dense ? " q-slider--dense q-slider--dense" + axis.value : ""));
		function getPositionClass(name) {
			const cls = "q-slider__" + name;
			return `${cls} ${cls}${axis.value} ${cls}${axis.value}${labelSide.value}`;
		}
		function getAxisClass(name) {
			const cls = "q-slider__" + name;
			return `${cls} ${cls}${axis.value}`;
		}
		const selectionBarClass = (0, vue.computed)(() => {
			const color = props.selectionColor || props.color;
			return "q-slider__selection absolute" + (color !== void 0 ? ` text-${color}` : "");
		});
		const markerClass = (0, vue.computed)(() => getAxisClass("markers") + " absolute overflow-hidden");
		const trackContainerClass = (0, vue.computed)(() => getAxisClass("track-container"));
		const pinClass = (0, vue.computed)(() => getPositionClass("pin"));
		const labelClass = (0, vue.computed)(() => getPositionClass("label"));
		const textContainerClass = (0, vue.computed)(() => getPositionClass("text-container"));
		const markerLabelsContainerClass = (0, vue.computed)(() => getPositionClass("marker-labels-container") + (props.markerLabelsClass !== void 0 ? ` ${props.markerLabelsClass}` : ""));
		const trackClass = (0, vue.computed)(() => "q-slider__track relative-position no-outline" + (props.trackColor !== void 0 ? ` bg-${props.trackColor}` : ""));
		const trackStyle = (0, vue.computed)(() => {
			const acc = { [thicknessProp.value]: props.trackSize };
			if (props.trackImg !== void 0) acc.backgroundImage = `url(${props.trackImg}) !important`;
			return acc;
		});
		const innerBarClass = (0, vue.computed)(() => "q-slider__inner absolute" + (props.innerTrackColor !== void 0 ? ` bg-${props.innerTrackColor}` : ""));
		const innerBarStyle = (0, vue.computed)(() => {
			const innerDiff = innerMaxRatio.value - innerMinRatio.value;
			const acc = {
				[positionProp.value]: `${100 * innerMinRatio.value}%`,
				[sizeProp.value]: innerDiff === 0 ? "2px" : `${100 * innerDiff}%`
			};
			if (props.innerTrackImg !== void 0) acc.backgroundImage = `url(${props.innerTrackImg}) !important`;
			return acc;
		});
		function convertRatioToModel(ratio) {
			const { min, max, step } = props;
			let model = min + ratio * (max - min);
			if (step > 0) {
				const modulo = (model - innerMin.value) % step;
				model += (Math.abs(modulo) >= step / 2 ? (modulo < 0 ? -1 : 1) * step : 0) - modulo;
			}
			model = roundValueFn.value(model);
			return between(model, innerMin.value, innerMax.value);
		}
		function convertModelToRatio(model) {
			return trackLen.value === 0 ? 0 : (model - props.min) / trackLen.value;
		}
		function getDraggingRatio(evt, draggingInfo) {
			const pos = position(evt), val = props.vertical ? between((pos.top - draggingInfo.top) / draggingInfo.height, 0, 1) : between((pos.left - draggingInfo.left) / draggingInfo.width, 0, 1);
			return between(isReversed.value ? 1 - val : val, innerMinRatio.value, innerMaxRatio.value);
		}
		const markerStep = (0, vue.computed)(() => isNumber(props.markers) ? props.markers : keyStep.value);
		const markerTicks = (0, vue.computed)(() => {
			const acc = [];
			const step = markerStep.value;
			const max = props.max;
			let value = props.min;
			do {
				acc.push(value);
				value += step;
			} while (value < max);
			acc.push(max);
			return acc;
		});
		const markerLabelClass = (0, vue.computed)(() => {
			const prefix = ` ${markerPrefixClass}${axis.value}-`;
			return `q-slider__marker-labels${prefix}${props.switchMarkerLabelsSide ? "switched" : "standard"}${prefix}${isReversed.value ? "rtl" : "ltr"}`;
		});
		const markerLabelsList = (0, vue.computed)(() => {
			if (props.markerLabels === false) return null;
			return getMarkerList(props.markerLabels).map((entry, index) => ({
				index,
				value: entry.value,
				label: entry.label || entry.value,
				classes: markerLabelClass.value + (entry.classes !== void 0 ? " " + entry.classes : ""),
				style: {
					...getMarkerLabelStyle(entry.value),
					...entry.style
				}
			}));
		});
		const markerScope = (0, vue.computed)(() => ({
			markerList: markerLabelsList.value,
			markerMap: markerLabelsMap.value,
			classes: markerLabelClass.value,
			getStyle: getMarkerLabelStyle
		}));
		const markerStyle = (0, vue.computed)(() => {
			const size = innerBarLen.value === 0 ? "2px" : 100 * markerStep.value / innerBarLen.value;
			return {
				...innerBarStyle.value,
				backgroundSize: props.vertical ? `2px ${size}%` : `${size}% 2px`
			};
		});
		function getMarkerList(def) {
			if (def === false) return null;
			if (def === true) return markerTicks.value.map(defaultMarkerConvertFn);
			if (typeof def === "function") return markerTicks.value.map((value) => {
				const item = def(value);
				return isObject(item) ? {
					...item,
					value
				} : {
					value,
					label: item
				};
			});
			const filterFn = ({ value }) => value >= props.min && value <= props.max;
			if (Array.isArray(def)) return def.map((item) => isObject(item) ? item : { value: item }).filter(filterFn);
			return Object.keys(def).map((key) => {
				const item = def[key];
				const value = Number(key);
				return isObject(item) ? {
					...item,
					value
				} : {
					value,
					label: item
				};
			}).filter(filterFn);
		}
		function getMarkerLabelStyle(val) {
			return { [positionProp.value]: `${100 * (val - props.min) / trackLen.value}%` };
		}
		const markerLabelsMap = (0, vue.computed)(() => {
			if (props.markerLabels === false) return null;
			const acc = {};
			markerLabelsList.value.forEach((entry) => {
				acc[entry.value] = entry;
			});
			return acc;
		});
		function getMarkerLabelsContent() {
			if (slots["marker-label-group"] !== void 0) return slots["marker-label-group"](markerScope.value);
			const fn = slots["marker-label"] || defaultMarkerLabelRenderFn;
			return markerLabelsList.value.map((marker) => fn({
				marker,
				...markerScope.value
			}));
		}
		const panDirective = (0, vue.computed)(() => [[
			TouchPan_default,
			onPan,
			void 0,
			{
				[orientation.value]: true,
				prevent: true,
				stop: true,
				mouse: true,
				mouseAllDir: true
			}
		]]);
		function onPan(event) {
			if (event.isFinal) {
				if (dragging.value !== void 0) {
					updatePosition(event.evt);
					if (event.touch) updateValue(true);
					dragging.value = void 0;
					emit("pan", "end");
				}
				active.value = false;
				focus.value = false;
			} else if (event.isFirst) {
				dragging.value = getDragging(event.evt);
				updatePosition(event.evt);
				updateValue();
				active.value = true;
				emit("pan", "start");
			} else {
				updatePosition(event.evt);
				updateValue();
			}
		}
		function onBlur() {
			focus.value = false;
		}
		function onActivate(evt) {
			updatePosition(evt, getDragging(evt));
			updateValue();
			preventFocus.value = true;
			active.value = true;
			document.addEventListener("mouseup", onDeactivate, true);
		}
		function onDeactivate() {
			preventFocus.value = false;
			active.value = false;
			updateValue(true);
			onBlur();
			document.removeEventListener("mouseup", onDeactivate, true);
		}
		function onMobileClick(evt) {
			updatePosition(evt, getDragging(evt));
			updateValue(true);
		}
		function onKeyup(evt) {
			if (keyCodes$2.includes(evt.keyCode)) updateValue(true);
		}
		function getTextContainerStyle(ratio) {
			if (props.vertical) return null;
			const p = $q.lang.rtl !== props.reverse ? 1 - ratio : ratio;
			return { transform: `translateX(calc(${2 * p - 1} * ${props.thumbSize} / 2 + ${50 - 100 * p}%))` };
		}
		function getThumbRenderFn(thumb) {
			const focusClass = (0, vue.computed)(() => !preventFocus.value && (focus.value === thumb.focusValue || focus.value === "both") ? " q-slider--focus" : "");
			const thumbClasses = (0, vue.computed)(() => `q-slider__thumb q-slider__thumb${axis.value} q-slider__thumb${axis.value}-${isReversed.value ? "rtl" : "ltr"} absolute non-selectable` + focusClass.value + (thumb.thumbColor.value !== void 0 ? ` text-${thumb.thumbColor.value}` : ""));
			const style = (0, vue.computed)(() => ({
				width: props.thumbSize,
				height: props.thumbSize,
				[positionProp.value]: `${100 * thumb.ratio.value}%`,
				zIndex: focus.value === thumb.focusValue ? 2 : void 0
			}));
			const pinColor = (0, vue.computed)(() => thumb.labelColor.value !== void 0 ? ` text-${thumb.labelColor.value}` : "");
			const textContainerStyle = (0, vue.computed)(() => getTextContainerStyle(thumb.ratio.value));
			const textClass = (0, vue.computed)(() => "q-slider__text" + (thumb.labelTextColor.value !== void 0 ? ` text-${thumb.labelTextColor.value}` : ""));
			return () => {
				const thumbContent = [(0, vue.h)("svg", {
					class: "q-slider__thumb-shape absolute-full",
					viewBox: "0 0 20 20",
					"aria-hidden": "true"
				}, [(0, vue.h)("path", { d: props.thumbPath })]), (0, vue.h)("div", { class: "q-slider__focus-ring fit" })];
				if (props.label || props.labelAlways) thumbContent.push((0, vue.h)("div", { class: pinClass.value + " absolute fit no-pointer-events" + pinColor.value }, [(0, vue.h)("div", {
					class: labelClass.value,
					style: { minWidth: props.thumbSize }
				}, [(0, vue.h)("div", {
					class: textContainerClass.value,
					style: textContainerStyle.value
				}, [(0, vue.h)("span", { class: textClass.value }, thumb.label.value)])])]));
				if (thumb.injectFormInput !== false && props.name !== void 0 && !props.disable) injectFormInput(thumbContent, "push");
				return (0, vue.h)("div", {
					class: thumbClasses.value,
					style: style.value,
					...thumb.getNodeData()
				}, thumbContent);
			};
		}
		function getContent(selectionBarStyle, trackContainerTabindex, trackContainerEvents, injectThumb) {
			const trackContent = [];
			if (props.innerTrackColor !== "transparent") trackContent.push((0, vue.h)("div", {
				key: "inner",
				class: innerBarClass.value,
				style: innerBarStyle.value
			}));
			if (props.selectionColor !== "transparent") trackContent.push((0, vue.h)("div", {
				key: "selection",
				class: selectionBarClass.value,
				style: selectionBarStyle.value
			}));
			if (props.markers !== false) trackContent.push((0, vue.h)("div", {
				key: "marker",
				class: markerClass.value,
				style: markerStyle.value
			}));
			injectThumb(trackContent);
			const content = [hDir("div", {
				key: "trackC",
				class: trackContainerClass.value,
				tabindex: trackContainerTabindex.value,
				...trackContainerEvents.value
			}, [(0, vue.h)("div", {
				class: trackClass.value,
				style: trackStyle.value
			}, trackContent)], "slide", editable.value, () => panDirective.value)];
			if (props.markerLabels !== false) content[props.switchMarkerLabelsSide ? "unshift" : "push"]((0, vue.h)("div", {
				key: "markerL",
				class: markerLabelsContainerClass.value
			}, getMarkerLabelsContent()));
			return content;
		}
		(0, vue.onBeforeUnmount)(() => {
			document.removeEventListener("mouseup", onDeactivate, true);
		});
		return {
			state: {
				active,
				focus,
				preventFocus,
				dragging,
				editable,
				classes,
				tabindex,
				attributes,
				roundValueFn,
				keyStep,
				trackLen,
				innerMin,
				innerMinRatio,
				innerMax,
				innerMaxRatio,
				positionProp,
				sizeProp,
				isReversed
			},
			methods: {
				onActivate,
				onMobileClick,
				onBlur,
				onKeyup,
				getContent,
				getThumbRenderFn,
				convertRatioToModel,
				convertModelToRatio,
				getDraggingRatio
			}
		};
	}
	//#endregion
	//#region src/components/slider/QSlider.js
	const getNodeData = () => ({});
	var QSlider_default = createComponent({
		name: "QSlider",
		props: {
			...useSliderProps,
			modelValue: {
				required: true,
				default: null,
				validator: (v) => typeof v === "number" || v === null
			},
			labelValue: [String, Number]
		},
		emits: useSliderEmits,
		setup(props, { emit }) {
			const { proxy: { $q } } = (0, vue.getCurrentInstance)();
			const { state, methods } = useSlider({
				updateValue,
				updatePosition,
				getDragging,
				formAttrs: useFormAttrs(props)
			});
			const rootRef = (0, vue.ref)(null);
			const curRatio = (0, vue.ref)(0);
			const model = (0, vue.ref)(0);
			function normalizeModel() {
				model.value = props.modelValue === null ? state.innerMin.value : between(props.modelValue, state.innerMin.value, state.innerMax.value);
			}
			(0, vue.watch)(() => `${props.modelValue}|${state.innerMin.value}|${state.innerMax.value}`, normalizeModel, { immediate: true });
			const modelRatio = (0, vue.computed)(() => methods.convertModelToRatio(model.value));
			const ratio = (0, vue.computed)(() => state.active.value ? curRatio.value : modelRatio.value);
			const selectionBarStyle = (0, vue.computed)(() => {
				const acc = {
					[state.positionProp.value]: `${100 * state.innerMinRatio.value}%`,
					[state.sizeProp.value]: `${100 * (ratio.value - state.innerMinRatio.value)}%`
				};
				if (props.selectionImg !== void 0) acc.backgroundImage = `url(${props.selectionImg}) !important`;
				return acc;
			});
			const getThumb = methods.getThumbRenderFn({
				focusValue: true,
				getNodeData,
				ratio,
				label: (0, vue.computed)(() => props.labelValue !== void 0 ? props.labelValue : model.value),
				thumbColor: (0, vue.computed)(() => props.thumbColor || props.color),
				labelColor: (0, vue.computed)(() => props.labelColor),
				labelTextColor: (0, vue.computed)(() => props.labelTextColor)
			});
			const trackContainerEvents = (0, vue.computed)(() => {
				if (!state.editable.value) return {};
				return $q.platform.is.mobile ? { onClick: methods.onMobileClick } : {
					onMousedown: methods.onActivate,
					onFocus,
					onBlur: methods.onBlur,
					onKeydown,
					onKeyup: methods.onKeyup
				};
			});
			function updateValue(change) {
				if (model.value !== props.modelValue) emit("update:modelValue", model.value);
				if (change) emit("change", model.value);
			}
			function getDragging() {
				return rootRef.value.getBoundingClientRect();
			}
			function updatePosition(event, dragging = state.dragging.value) {
				const localRatio = methods.getDraggingRatio(event, dragging);
				model.value = methods.convertRatioToModel(localRatio);
				curRatio.value = !props.snap || props.step === 0 ? localRatio : methods.convertModelToRatio(model.value);
			}
			function onFocus() {
				state.focus.value = true;
			}
			function onKeydown(evt) {
				if (!keyCodes$2.includes(evt.keyCode)) return;
				stopAndPrevent(evt);
				const stepVal = ([34, 33].includes(evt.keyCode) ? 10 : 1) * state.keyStep.value, offset = ([
					34,
					37,
					40
				].includes(evt.keyCode) ? -1 : 1) * (state.isReversed.value ? -1 : 1) * (props.vertical ? -1 : 1) * stepVal;
				model.value = between(state.roundValueFn.value(model.value + offset), state.innerMin.value, state.innerMax.value);
				updateValue();
			}
			return () => {
				const content = methods.getContent(selectionBarStyle, state.tabindex, trackContainerEvents, (node) => {
					node.push(getThumb());
				});
				return (0, vue.h)("div", {
					ref: rootRef,
					class: state.classes.value + (props.modelValue === null ? " q-slider--no-value" : ""),
					...state.attributes.value,
					"aria-valuenow": props.modelValue
				}, content);
			};
		}
	});
	//#endregion
	//#region src/composables/use-hydration/use-hydration.js
	function useHydration() {
		const isHydrated = (0, vue.ref)(!isRuntimeSsrPreHydration.value);
		if (!isHydrated.value) (0, vue.onMounted)(() => {
			isHydrated.value = true;
		});
		return { isHydrated };
	}
	//#endregion
	//#region src/components/resize-observer/QResizeObserver.js
	const hasObserver = typeof ResizeObserver !== "undefined";
	const resizeProps = hasObserver ? {} : {
		style: "display:block;position:absolute;top:0;left:0;right:0;bottom:0;height:100%;width:100%;overflow:hidden;pointer-events:none;z-index:-1;",
		url: "about:blank"
	};
	var QResizeObserver_default = createComponent({
		name: "QResizeObserver",
		props: { debounce: {
			type: [String, Number],
			default: 100
		} },
		emits: ["resize"],
		setup(props, { emit }) {
			let timer = null, targetEl, size = {
				width: -1,
				height: -1
			};
			function trigger(immediately) {
				if (immediately === true || props.debounce === 0 || props.debounce === "0") emitEvent();
				else if (timer === null) timer = setTimeout(emitEvent, props.debounce);
			}
			function emitEvent() {
				if (timer !== null) {
					clearTimeout(timer);
					timer = null;
				}
				if (targetEl) {
					const { offsetWidth: width, offsetHeight: height } = targetEl;
					if (width !== size.width || height !== size.height) {
						size = {
							width,
							height
						};
						emit("resize", size);
					}
				}
			}
			const { proxy } = (0, vue.getCurrentInstance)();
			proxy.trigger = trigger;
			if (hasObserver) {
				let observer, isDestroyed = false;
				const init = (stop) => {
					if (isDestroyed) return;
					targetEl = proxy.$el.parentNode;
					if (targetEl) {
						observer = new ResizeObserver(trigger);
						observer.observe(targetEl);
						emitEvent();
					} else if (!stop) (0, vue.nextTick)(() => {
						init(true);
					});
				};
				(0, vue.onMounted)(() => {
					init();
				});
				(0, vue.onBeforeUnmount)(() => {
					isDestroyed = true;
					if (timer !== null) clearTimeout(timer);
					if (observer !== void 0) {
						if (observer.disconnect !== void 0) observer.disconnect();
						else if (targetEl) observer.unobserve(targetEl);
					}
				});
				return noop;
			}
			const { isHydrated } = useHydration();
			let curDocView, isDestroyed = false;
			const cleanup = () => {
				if (timer !== null) {
					clearTimeout(timer);
					timer = null;
				}
				if (curDocView !== void 0) {
					if (curDocView.removeEventListener !== void 0) curDocView.removeEventListener("resize", trigger, listenOpts.passive);
					curDocView = void 0;
				}
			};
			const onObjLoad = () => {
				cleanup();
				if (targetEl?.contentDocument) {
					curDocView = targetEl.contentDocument.defaultView;
					curDocView.addEventListener("resize", trigger, listenOpts.passive);
					emitEvent();
				}
			};
			(0, vue.onMounted)(() => {
				(0, vue.nextTick)(() => {
					if (isDestroyed) return;
					targetEl = proxy.$el;
					if (targetEl) onObjLoad();
				});
			});
			(0, vue.onBeforeUnmount)(() => {
				isDestroyed = true;
				cleanup();
			});
			return () => {
				if (isHydrated.value) return (0, vue.h)("object", {
					class: "q--avoid-card-border",
					style: resizeProps.style,
					tabindex: -1,
					type: "text/html",
					data: resizeProps.url,
					"aria-hidden": "true",
					onLoad: onObjLoad
				});
			};
		}
	});
	//#endregion
	//#region src/utils/private.rtl/rtl.js
	let rtlHasScrollBug = false;
	{
		const scroller = document.createElement("div");
		scroller.setAttribute("dir", "rtl");
		Object.assign(scroller.style, {
			width: "1px",
			height: "1px",
			overflow: "auto"
		});
		const spacer = document.createElement("div");
		Object.assign(spacer.style, {
			width: "1000px",
			height: "1px"
		});
		document.body.append(scroller);
		scroller.append(spacer);
		scroller.scrollLeft = -1e3;
		rtlHasScrollBug = scroller.scrollLeft >= 0;
		scroller.remove();
	}
	//#endregion
	//#region src/components/tabs/QTabs.js
	function getIndicatorClass(color, top, vertical) {
		const pos = vertical ? ["left", "right"] : ["top", "bottom"];
		return `absolute-${top ? pos[0] : pos[1]}${color ? ` text-${color}` : ""}`;
	}
	function hasQueryIncluded(targetQuery, matchingQuery) {
		for (const key in targetQuery) if (targetQuery[key] !== matchingQuery[key]) return false;
		return true;
	}
	const alignValues$1 = [
		"left",
		"center",
		"right",
		"justify"
	];
	var QTabs_default = createComponent({
		name: "QTabs",
		props: {
			modelValue: [Number, String],
			align: {
				type: String,
				default: "center",
				validator: (v) => alignValues$1.includes(v)
			},
			breakpoint: {
				type: [String, Number],
				default: 600
			},
			vertical: Boolean,
			shrink: Boolean,
			stretch: Boolean,
			activeClass: String,
			activeColor: String,
			activeBgColor: String,
			indicatorColor: String,
			leftIcon: String,
			rightIcon: String,
			outsideArrows: Boolean,
			mobileArrows: Boolean,
			switchIndicator: Boolean,
			narrowIndicator: Boolean,
			inlineLabel: Boolean,
			noCaps: Boolean,
			dense: Boolean,
			contentClass: String,
			"onUpdate:modelValue": [Function, Array]
		},
		setup(props, { slots, emit }) {
			const { proxy } = (0, vue.getCurrentInstance)();
			const { $q } = proxy;
			const { registerTick: registerScrollTick } = useTick();
			const { registerTick: registerUpdateArrowsTick } = useTick();
			const { registerTick: registerAnimateTick } = useTick();
			const { registerTimeout: registerFocusTimeout, removeTimeout: removeFocusTimeout } = useTimeout();
			const { registerTimeout: registerScrollToTabTimeout, removeTimeout: removeScrollToTabTimeout } = useTimeout();
			const rootRef = (0, vue.ref)(null);
			const contentRef = (0, vue.ref)(null);
			const currentModel = (0, vue.ref)(props.modelValue);
			const scrollable = (0, vue.ref)(false);
			const leftArrow = (0, vue.ref)(true);
			const rightArrow = (0, vue.ref)(false);
			const justify = (0, vue.ref)(false);
			const tabDataList = [];
			const tabDataListLen = (0, vue.ref)(0);
			const hasFocus = (0, vue.ref)(false);
			let animateTimer = null, scrollTimer = null, unwatchRoute;
			const tabProps = (0, vue.computed)(() => ({
				activeClass: props.activeClass,
				activeColor: props.activeColor,
				activeBgColor: props.activeBgColor,
				indicatorClass: getIndicatorClass(props.indicatorColor, props.switchIndicator, props.vertical),
				narrowIndicator: props.narrowIndicator,
				inlineLabel: props.inlineLabel,
				noCaps: props.noCaps
			}));
			const hasActiveTab = (0, vue.computed)(() => {
				const len = tabDataListLen.value;
				const val = currentModel.value;
				for (let i = 0; i < len; i++) if (tabDataList[i].name.value === val) return true;
				return false;
			});
			const alignClass = (0, vue.computed)(() => {
				return `q-tabs__content--align-${scrollable.value ? "left" : justify.value ? "justify" : props.align}`;
			});
			const classes = (0, vue.computed)(() => `q-tabs row no-wrap items-center q-tabs--${scrollable.value ? "" : "not-"}scrollable q-tabs--${props.vertical ? "vertical" : "horizontal"} q-tabs__arrows--${props.outsideArrows ? "outside" : "inside"} q-tabs--mobile-with${props.mobileArrows ? "" : "out"}-arrows` + (props.dense ? " q-tabs--dense" : "") + (props.shrink ? " col-shrink" : "") + (props.stretch ? " self-stretch" : ""));
			const innerClass = (0, vue.computed)(() => "q-tabs__content scroll--mobile row no-wrap items-center self-stretch hide-scrollbar relative-position " + alignClass.value + (props.contentClass !== void 0 ? ` ${props.contentClass}` : ""));
			const domProps = (0, vue.computed)(() => props.vertical ? {
				container: "height",
				content: "offsetHeight",
				scroll: "scrollHeight"
			} : {
				container: "width",
				content: "offsetWidth",
				scroll: "scrollWidth"
			});
			const isRTL = (0, vue.computed)(() => !props.vertical && $q.lang.rtl === true);
			const rtlPosCorrection = (0, vue.computed)(() => !rtlHasScrollBug && isRTL.value);
			(0, vue.watch)(isRTL, updateArrows);
			(0, vue.watch)(() => props.modelValue, (name) => {
				updateModel({
					name,
					setCurrent: true,
					skipEmit: true
				});
			});
			(0, vue.watch)(() => props.outsideArrows, recalculateScroll);
			function updateModel({ name, setCurrent, skipEmit }) {
				if (currentModel.value === name) return;
				if (!skipEmit && props["onUpdate:modelValue"] !== void 0) emit("update:modelValue", name);
				if (setCurrent || props["onUpdate:modelValue"] === void 0) {
					animate(currentModel.value, name);
					currentModel.value = name;
				}
			}
			function recalculateScroll() {
				registerScrollTick(() => {
					if (rootRef.value) updateContainer({
						width: rootRef.value.offsetWidth,
						height: rootRef.value.offsetHeight
					});
				});
			}
			function updateContainer(domSize) {
				if (domProps.value === void 0 || contentRef.value === null) return;
				const size = domSize[domProps.value.container], scrollSize = Math.min(contentRef.value[domProps.value.scroll], Array.prototype.reduce.call(contentRef.value.children, (acc, el) => acc + (el[domProps.value.content] || 0), 0)), scroll = size > 0 && scrollSize > size;
				scrollable.value = scroll;
				if (scroll) registerUpdateArrowsTick(updateArrows);
				justify.value = size < Number.parseInt(props.breakpoint, 10);
			}
			function animate(oldName, newName) {
				const oldTab = oldName !== void 0 && oldName !== null && oldName !== "" ? tabDataList.find((tab) => tab.name.value === oldName) : null, newTab = newName !== void 0 && newName !== null && newName !== "" ? tabDataList.find((tab) => tab.name.value === newName) : null;
				if (hadActivated) hadActivated = false;
				else if (oldTab && newTab) {
					const oldEl = oldTab.tabIndicatorRef.value, newEl = newTab.tabIndicatorRef.value;
					if (animateTimer !== null) {
						clearTimeout(animateTimer);
						animateTimer = null;
					}
					oldEl.style.transition = "none";
					oldEl.style.transform = "none";
					newEl.style.transition = "none";
					newEl.style.transform = "none";
					const oldPos = oldEl.getBoundingClientRect(), newPos = newEl.getBoundingClientRect();
					newEl.style.transform = props.vertical ? `translate3d(0,${oldPos.top - newPos.top}px,0) scale3d(1,${newPos.height ? oldPos.height / newPos.height : 1},1)` : `translate3d(${oldPos.left - newPos.left}px,0,0) scale3d(${newPos.width ? oldPos.width / newPos.width : 1},1,1)`;
					registerAnimateTick(() => {
						animateTimer = setTimeout(() => {
							animateTimer = null;
							newEl.style.transition = "transform .25s cubic-bezier(.4, 0, .2, 1)";
							newEl.style.transform = "none";
						}, 70);
					});
				}
				if (newTab && scrollable.value) scrollToTabEl(newTab.rootRef.value);
			}
			function scrollToTabEl(el) {
				const { left, width, top, height } = contentRef.value.getBoundingClientRect(), newPos = el.getBoundingClientRect();
				let offset = props.vertical ? newPos.top - top : newPos.left - left;
				if (offset < 0) {
					contentRef.value[props.vertical ? "scrollTop" : "scrollLeft"] += Math.floor(offset);
					updateArrows();
					return;
				}
				offset += props.vertical ? newPos.height - height : newPos.width - width;
				if (offset > 0) {
					contentRef.value[props.vertical ? "scrollTop" : "scrollLeft"] += Math.ceil(offset);
					updateArrows();
				}
			}
			function updateArrows() {
				const content = contentRef.value;
				if (content === null) return;
				const rect = content.getBoundingClientRect(), pos = props.vertical ? content.scrollTop : Math.abs(content.scrollLeft);
				if (isRTL.value) {
					leftArrow.value = Math.ceil(pos + rect.width) < content.scrollWidth - 1;
					rightArrow.value = pos > 0;
				} else {
					leftArrow.value = pos > 0;
					rightArrow.value = props.vertical ? Math.ceil(pos + rect.height) < content.scrollHeight : Math.ceil(pos + rect.width) < content.scrollWidth;
				}
			}
			function animScrollTo(value) {
				if (scrollTimer !== null) clearInterval(scrollTimer);
				scrollTimer = setInterval(() => {
					if (scrollTowards(value)) stopAnimScroll();
				}, 5);
			}
			function scrollToStart() {
				animScrollTo(rtlPosCorrection.value ? Number.MAX_SAFE_INTEGER : 0);
			}
			function scrollToEnd() {
				animScrollTo(rtlPosCorrection.value ? 0 : Number.MAX_SAFE_INTEGER);
			}
			function stopAnimScroll() {
				if (scrollTimer !== null) {
					clearInterval(scrollTimer);
					scrollTimer = null;
				}
			}
			function onKbdNavigate(keyCode, fromEl) {
				const tabs = Array.prototype.filter.call(contentRef.value.children, (el) => el === fromEl || el.matches?.(".q-tab.q-focusable"));
				const len = tabs.length;
				if (len === 0) return;
				if (keyCode === 36) {
					scrollToTabEl(tabs[0]);
					tabs[0].focus();
					return true;
				}
				if (keyCode === 35) {
					scrollToTabEl(tabs[len - 1]);
					tabs[len - 1].focus();
					return true;
				}
				const dirPrev = keyCode === (props.vertical ? 38 : 37);
				const dirNext = keyCode === (props.vertical ? 40 : 39);
				const dir = dirPrev ? -1 : dirNext ? 1 : void 0;
				if (dir !== void 0) {
					const rtlDir = props.vertical !== true && isRTL.value ? -1 : 1;
					const index = (tabs.indexOf(fromEl) + dir * rtlDir + len) % len;
					scrollToTabEl(tabs[index]);
					tabs[index].focus({ preventScroll: true });
					return true;
				}
			}
			const posFn = (0, vue.computed)(() => rtlPosCorrection.value ? {
				get: (content) => Math.abs(content.scrollLeft),
				set: (content, pos) => {
					content.scrollLeft = -pos;
				}
			} : props.vertical ? {
				get: (content) => content.scrollTop,
				set: (content, pos) => {
					content.scrollTop = pos;
				}
			} : {
				get: (content) => content.scrollLeft,
				set: (content, pos) => {
					content.scrollLeft = pos;
				}
			});
			function scrollTowards(value) {
				const content = contentRef.value, { get, set } = posFn.value;
				let done = false, pos = get(content);
				const direction = value < pos ? -1 : 1;
				pos += direction * 5;
				if (pos < 0) {
					done = true;
					pos = 0;
				} else if (direction === -1 && pos <= value || direction === 1 && pos >= value) {
					done = true;
					pos = value;
				}
				set(content, pos);
				updateArrows();
				return done;
			}
			function updateActiveRoute() {
				let name = null, bestScore = {
					matchedLen: 0,
					queryDiff: 9999,
					hrefLen: 0
				};
				const list = tabDataList.filter((tab) => tab.routeData?.hasRouterLink.value === true);
				const { hash: currentHash, query: currentQuery } = proxy.$route;
				const currentQueryLen = Object.keys(currentQuery).length;
				for (const tab of list) {
					const exact = tab.routeData.exact.value === true;
					if (!tab.routeData[exact ? "linkIsExactActive" : "linkIsActive"].value) continue;
					const { hash, query, matched, href } = tab.routeData.resolvedLink.value;
					const queryLen = Object.keys(query).length;
					if (exact) {
						if (hash !== currentHash) continue;
						if (queryLen !== currentQueryLen || !hasQueryIncluded(currentQuery, query)) continue;
						name = tab.name.value;
						break;
					}
					if (hash !== "" && hash !== currentHash) continue;
					if (queryLen !== 0 && !hasQueryIncluded(query, currentQuery)) continue;
					const newScore = {
						matchedLen: matched.length,
						queryDiff: currentQueryLen - queryLen,
						hrefLen: href.length - hash.length
					};
					if (newScore.matchedLen > bestScore.matchedLen) {
						name = tab.name.value;
						bestScore = newScore;
						continue;
					} else if (newScore.matchedLen !== bestScore.matchedLen) continue;
					if (newScore.queryDiff < bestScore.queryDiff) {
						name = tab.name.value;
						bestScore = newScore;
					} else if (newScore.queryDiff !== bestScore.queryDiff) continue;
					if (newScore.hrefLen > bestScore.hrefLen) {
						name = tab.name.value;
						bestScore = newScore;
					}
				}
				if (name === null && tabDataList.some((tab) => tab.routeData === void 0 && tab.name.value === currentModel.value)) {
					hadActivated = false;
					return;
				}
				updateModel({
					name,
					setCurrent: true
				});
			}
			function onFocusin(e) {
				removeFocusTimeout();
				if (!hasFocus.value && rootRef.value !== null && e.target && typeof e.target.closest === "function") {
					const tab = e.target.closest(".q-tab");
					if (tab && rootRef.value.contains(tab)) {
						hasFocus.value = true;
						if (scrollable.value) scrollToTabEl(tab);
					}
				}
			}
			function onFocusout() {
				registerFocusTimeout(() => {
					hasFocus.value = false;
				}, 30);
			}
			function verifyRouteModel() {
				if ($tabs.avoidRouteWatcher === false) registerScrollToTabTimeout(updateActiveRoute);
				else removeScrollToTabTimeout();
			}
			function watchRoute() {
				if (unwatchRoute === void 0) {
					const unwatch = (0, vue.watch)(() => proxy.$route.fullPath, verifyRouteModel);
					unwatchRoute = () => {
						unwatch();
						unwatchRoute = void 0;
					};
				}
			}
			function registerTab(tabData) {
				tabDataList.push(tabData);
				tabDataListLen.value++;
				recalculateScroll();
				if (tabData.routeData === void 0 || proxy.$route === void 0) registerScrollToTabTimeout(() => {
					if (scrollable.value) {
						const value = currentModel.value;
						const newTab = value !== void 0 && value !== null && value !== "" ? tabDataList.find((tab) => tab.name.value === value) : null;
						if (newTab) scrollToTabEl(newTab.rootRef.value);
					}
				});
				else {
					watchRoute();
					if (tabData.routeData.hasRouterLink.value) verifyRouteModel();
				}
			}
			function unregisterTab(tabData) {
				tabDataList.splice(tabDataList.indexOf(tabData), 1);
				tabDataListLen.value--;
				recalculateScroll();
				if (unwatchRoute !== void 0 && tabData.routeData !== void 0) {
					if (tabDataList.every((tab) => tab.routeData === void 0)) unwatchRoute();
					verifyRouteModel();
				}
			}
			const $tabs = {
				currentModel,
				tabProps,
				hasFocus,
				hasActiveTab,
				registerTab,
				unregisterTab,
				verifyRouteModel,
				updateModel,
				onKbdNavigate,
				avoidRouteWatcher: false
			};
			(0, vue.provide)(tabsKey, $tabs);
			function cleanup() {
				if (animateTimer !== null) clearTimeout(animateTimer);
				stopAnimScroll();
				unwatchRoute?.();
			}
			let hadRouteWatcher = false, hadActivated = false;
			(0, vue.onBeforeUnmount)(cleanup);
			(0, vue.onDeactivated)(() => {
				hadRouteWatcher = unwatchRoute !== void 0;
				cleanup();
			});
			(0, vue.onActivated)(() => {
				if (hadRouteWatcher) {
					watchRoute();
					hadActivated = true;
					verifyRouteModel();
				}
				recalculateScroll();
			});
			return () => (0, vue.h)("div", {
				ref: rootRef,
				class: classes.value,
				role: "tablist",
				"aria-orientation": props.vertical ? "vertical" : "horizontal",
				onFocusin,
				onFocusout
			}, [
				(0, vue.h)(QResizeObserver_default, { onResize: updateContainer }),
				(0, vue.h)("div", {
					ref: contentRef,
					class: innerClass.value,
					onScroll: updateArrows
				}, hSlot(slots.default)),
				(0, vue.h)(QIcon_default, {
					class: "q-tabs__arrow q-tabs__arrow--left absolute q-tab__icon" + (leftArrow.value ? "" : " q-tabs__arrow--faded"),
					name: props.leftIcon || $q.iconSet.tabs[props.vertical ? "up" : "left"],
					onMousedownPassive: scrollToStart,
					onTouchstartPassive: scrollToStart,
					onMouseupPassive: stopAnimScroll,
					onMouseleavePassive: stopAnimScroll,
					onTouchendPassive: stopAnimScroll
				}),
				(0, vue.h)(QIcon_default, {
					class: "q-tabs__arrow q-tabs__arrow--right absolute q-tab__icon" + (rightArrow.value ? "" : " q-tabs__arrow--faded"),
					name: props.rightIcon || $q.iconSet.tabs[props.vertical ? "down" : "right"],
					onMousedownPassive: scrollToEnd,
					onTouchstartPassive: scrollToEnd,
					onMouseupPassive: stopAnimScroll,
					onMouseleavePassive: stopAnimScroll,
					onTouchendPassive: stopAnimScroll
				})
			]);
		}
	});
	//#endregion
	//#region src/components/tabs/use-tab.js
	let id$1 = 0;
	const useTabEmits = ["click", "keydown"];
	const useTabProps = {
		icon: String,
		label: [Number, String],
		alert: [Boolean, String],
		alertIcon: String,
		name: {
			type: [Number, String],
			default: () => `t_${id$1++}`
		},
		noCaps: Boolean,
		tabindex: [String, Number],
		disable: Boolean,
		contentClass: String,
		ripple: {
			type: [Boolean, Object],
			default: true
		}
	};
	function useTab(props, slots, emit, routeData) {
		const $tabs = (0, vue.inject)(tabsKey, emptyRenderFn);
		if ($tabs === emptyRenderFn) {
			console.error("QTab/QRouteTab component needs to be child of QTabs");
			return emptyRenderFn;
		}
		const { proxy } = (0, vue.getCurrentInstance)();
		const blurTargetRef = (0, vue.ref)(null);
		const rootRef = (0, vue.ref)(null);
		const tabIndicatorRef = (0, vue.ref)(null);
		const ripple = (0, vue.computed)(() => props.disable || props.ripple === false ? false : {
			keyCodes: [13, 32],
			early: true,
			...props.ripple === true ? {} : props.ripple
		});
		const isActive = (0, vue.computed)(() => $tabs.currentModel.value === props.name);
		const classes = (0, vue.computed)(() => "q-tab relative-position self-stretch flex flex-center text-center" + (isActive.value ? " q-tab--active" + ($tabs.tabProps.value.activeClass ? " " + $tabs.tabProps.value.activeClass : "") + ($tabs.tabProps.value.activeColor ? ` text-${$tabs.tabProps.value.activeColor}` : "") + ($tabs.tabProps.value.activeBgColor ? ` bg-${$tabs.tabProps.value.activeBgColor}` : "") : " q-tab--inactive") + (props.icon && props.label && !$tabs.tabProps.value.inlineLabel ? " q-tab--full" : "") + (props.noCaps || $tabs.tabProps.value.noCaps ? " q-tab--no-caps" : "") + (props.disable ? " disabled" : " q-focusable q-hoverable cursor-pointer") + (routeData !== void 0 ? routeData.linkClass.value : ""));
		const innerClass = (0, vue.computed)(() => "q-tab__content self-stretch flex-center relative-position q-anchor--skip non-selectable " + ($tabs.tabProps.value.inlineLabel ? "row no-wrap q-tab__content--inline" : "column") + (props.contentClass !== void 0 ? ` ${props.contentClass}` : ""));
		const tabIndex = (0, vue.computed)(() => props.disable || $tabs.hasFocus.value || !isActive.value && $tabs.hasActiveTab.value ? -1 : props.tabindex || 0);
		function onClick(e, keyboard) {
			if (!keyboard && !e?.qAvoidFocus) blurTargetRef.value?.focus();
			if (props.disable) {
				if (routeData?.hasRouterLink.value === true) stopAndPrevent(e);
				return;
			}
			if (routeData === void 0) {
				$tabs.updateModel({ name: props.name });
				emit("click", e);
				return;
			}
			if (routeData.hasRouterLink.value) {
				const go = (opts = {}) => {
					let hardError;
					const reqId = opts.to === void 0 || isDeepEqual(opts.to, props.to) ? $tabs.avoidRouteWatcher = uid_default() : null;
					return routeData.navigateToRouterLink(e, {
						...opts,
						returnRouterError: true
					}).catch((err) => {
						hardError = err;
					}).then((softError) => {
						if (reqId === $tabs.avoidRouteWatcher) {
							$tabs.avoidRouteWatcher = false;
							if (hardError === void 0 && (softError === void 0 || softError.message?.startsWith("Avoided redundant navigation") === true)) $tabs.updateModel({ name: props.name });
						}
						if (opts.returnRouterError) return hardError !== void 0 ? Promise.reject(hardError) : softError;
					});
				};
				emit("click", e, go);
				if (!e.defaultPrevented) go();
				return;
			}
			emit("click", e);
		}
		function onKeydown(e) {
			if (isKeyCode(e, [13, 32])) onClick(e, true);
			else if (!shouldIgnoreKey(e) && e.keyCode >= 35 && e.keyCode <= 40 && !e.altKey && !e.metaKey && $tabs.onKbdNavigate(e.keyCode, proxy.$el)) stopAndPrevent(e);
			emit("keydown", e);
		}
		function getContent() {
			const narrow = $tabs.tabProps.value.narrowIndicator, content = [], indicator = (0, vue.h)("div", {
				ref: tabIndicatorRef,
				class: ["q-tab__indicator", $tabs.tabProps.value.indicatorClass]
			});
			if (props.icon !== void 0) content.push((0, vue.h)(QIcon_default, {
				class: "q-tab__icon",
				name: props.icon
			}));
			if (props.label !== void 0) content.push((0, vue.h)("div", { class: "q-tab__label" }, props.label));
			if (props.alert) content.push(props.alertIcon !== void 0 ? (0, vue.h)(QIcon_default, {
				class: "q-tab__alert-icon",
				color: props.alert !== true ? props.alert : void 0,
				name: props.alertIcon
			}) : (0, vue.h)("div", { class: "q-tab__alert" + (props.alert !== true ? ` text-${props.alert}` : "") }));
			if (narrow) content.push(indicator);
			const node = [(0, vue.h)("div", {
				class: "q-focus-helper",
				tabindex: -1,
				ref: blurTargetRef
			}), (0, vue.h)("div", { class: innerClass.value }, hMergeSlot(slots.default, content))];
			if (!narrow) node.push(indicator);
			return node;
		}
		const tabData = {
			name: (0, vue.computed)(() => props.name),
			rootRef,
			tabIndicatorRef,
			routeData
		};
		(0, vue.onBeforeUnmount)(() => {
			$tabs.unregisterTab(tabData);
		});
		(0, vue.onMounted)(() => {
			$tabs.registerTab(tabData);
		});
		function renderTab(tag, customData) {
			return (0, vue.withDirectives)((0, vue.h)(tag, {
				ref: rootRef,
				class: classes.value,
				tabindex: tabIndex.value,
				role: "tab",
				"aria-selected": isActive.value ? "true" : "false",
				"aria-disabled": props.disable ? "true" : void 0,
				onClick,
				onKeydown,
				...customData
			}, getContent()), [[Ripple_default, ripple.value]]);
		}
		return {
			renderTab,
			$tabs
		};
	}
	//#endregion
	//#region src/components/tabs/QTab.js
	var QTab_default = createComponent({
		name: "QTab",
		props: useTabProps,
		emits: useTabEmits,
		setup(props, { slots, emit }) {
			const { renderTab } = useTab(props, slots, emit);
			return () => renderTab("div");
		}
	});
	//#endregion
	//#region src/components/tab-panels/QTabPanels.js
	var QTabPanels_default = createComponent({
		name: "QTabPanels",
		props: {
			...usePanelProps,
			...useDarkProps
		},
		emits: usePanelEmits,
		setup(props, { slots }) {
			const isDark = useDark(props, (0, vue.getCurrentInstance)().proxy.$q);
			const { updatePanelsList, getPanelContent, panelDirectives } = usePanel();
			const classes = (0, vue.computed)(() => "q-tab-panels q-panel-parent" + (isDark.value ? " q-tab-panels--dark q-dark" : ""));
			return () => {
				updatePanelsList(slots);
				return hDir("div", { class: classes.value }, getPanelContent(), "pan", props.swipeable, () => panelDirectives.value);
			};
		}
	});
	//#endregion
	//#region src/components/tab-panels/QTabPanel.js
	var QTabPanel_default = createComponent({
		name: "QTabPanel",
		props: usePanelChildProps,
		setup(_, { slots }) {
			return () => (0, vue.h)("div", {
				class: "q-tab-panel",
				role: "tabpanel"
			}, hSlot(slots.default));
		}
	});
	//#endregion
	//#region src/utils/patterns/patterns.js
	const hexRE$1 = /^#[0-9a-fA-F]{3}([0-9a-fA-F]{3})?$/;
	const hexaRE = /^#[0-9a-fA-F]{4}([0-9a-fA-F]{4})?$/;
	const hexOrHexaRE = /^#([0-9a-fA-F]{3}|[0-9a-fA-F]{4}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})$/;
	const rgbRE$1 = /^rgb\(((0|[1-9][\d]?|1[\d]{0,2}|2[\d]?|2[0-4][\d]|25[0-5]),){2}(0|[1-9][\d]?|1[\d]{0,2}|2[\d]?|2[0-4][\d]|25[0-5])\)$/;
	const rgbaRE$1 = /^rgba\(((0|[1-9][\d]?|1[\d]{0,2}|2[\d]?|2[0-4][\d]|25[0-5]),){2}(0|[1-9][\d]?|1[\d]{0,2}|2[\d]?|2[0-4][\d]|25[0-5]),(0|0\.[0-9]+[1-9]|0\.[1-9]+|1)\)$/;
	const dateRE = /^-?[\d]+\/[0-1]\d\/[0-3]\d$/;
	const timeRE = /^([0-1]?\d|2[0-3]):[0-5]\d$/;
	const fulltimeRE = /^([0-1]?\d|2[0-3]):[0-5]\d:[0-5]\d$/;
	const timeOrFulltimeRE = /^([0-1]?\d|2[0-3]):[0-5]\d(:[0-5]\d)?$/;
	const emailRE = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
	const testPattern = {
		date: (v) => dateRE.test(v),
		time: (v) => timeRE.test(v),
		fulltime: (v) => fulltimeRE.test(v),
		timeOrFulltime: (v) => timeOrFulltimeRE.test(v),
		email: (v) => emailRE.test(v),
		hexColor: (v) => hexRE$1.test(v),
		hexaColor: (v) => hexaRE.test(v),
		hexOrHexaColor: (v) => hexOrHexaRE.test(v),
		rgbColor: (v) => rgbRE$1.test(v),
		rgbaColor: (v) => rgbaRE$1.test(v),
		rgbOrRgbaColor: (v) => rgbRE$1.test(v) || rgbaRE$1.test(v),
		hexOrRgbColor: (v) => hexRE$1.test(v) || rgbRE$1.test(v),
		hexaOrRgbaColor: (v) => hexaRE.test(v) || rgbaRE$1.test(v),
		anyColor: (v) => hexOrHexaRE.test(v) || rgbRE$1.test(v) || rgbaRE$1.test(v)
	};
	var patterns_default = { testPattern };
	//#endregion
	//#region src/utils/colors/colors.js
	const reRGBA = /^rgb(a)?\((\d{1,3}),(\d{1,3}),(\d{1,3}),?([01]?\.?\d*?)?\)$/;
	function rgbToHex({ r, g, b, a }) {
		const alpha = a !== void 0;
		r = Math.round(r);
		g = Math.round(g);
		b = Math.round(b);
		if (r > 255 || g > 255 || b > 255 || alpha && a > 100) throw new TypeError("Expected 3 numbers below 256 (and optionally one below 100)");
		a = alpha ? (Math.round(255 * a / 100) | 256).toString(16).slice(1) : "";
		return "#" + (b | g << 8 | r << 16 | 1 << 24).toString(16).slice(1) + a;
	}
	function rgbToString({ r, g, b, a }) {
		return `rgb${a !== void 0 ? "a" : ""}(${r},${g},${b}${a !== void 0 ? "," + a / 100 : ""})`;
	}
	function hexToRgb(hex) {
		if (typeof hex !== "string") throw new TypeError("Expected a string");
		hex = hex.replace(/^#/, "");
		if (hex.length === 3) hex = hex[0] + hex[0] + hex[1] + hex[1] + hex[2] + hex[2];
		else if (hex.length === 4) hex = hex[0] + hex[0] + hex[1] + hex[1] + hex[2] + hex[2] + hex[3] + hex[3];
		const num = Number.parseInt(hex, 16);
		return hex.length > 6 ? {
			r: num >> 24 & 255,
			g: num >> 16 & 255,
			b: num >> 8 & 255,
			a: Math.round((num & 255) / 2.55)
		} : {
			r: num >> 16,
			g: num >> 8 & 255,
			b: num & 255
		};
	}
	function hsvToRgb({ h, s, v, a }) {
		let r, g, b;
		s = s / 100;
		v = v / 100;
		h = h / 360;
		const i = Math.floor(h * 6), f = h * 6 - i, p = v * (1 - s), q = v * (1 - f * s), t = v * (1 - (1 - f) * s);
		switch (i % 6) {
			case 0:
				r = v;
				g = t;
				b = p;
				break;
			case 1:
				r = q;
				g = v;
				b = p;
				break;
			case 2:
				r = p;
				g = v;
				b = t;
				break;
			case 3:
				r = p;
				g = q;
				b = v;
				break;
			case 4:
				r = t;
				g = p;
				b = v;
				break;
			case 5:
				r = v;
				g = p;
				b = q;
				break;
		}
		return {
			r: Math.round(r * 255),
			g: Math.round(g * 255),
			b: Math.round(b * 255),
			a
		};
	}
	function rgbToHsv({ r, g, b, a }) {
		const max = Math.max(r, g, b), min = Math.min(r, g, b), d = max - min, s = max === 0 ? 0 : d / max, v = max / 255;
		let h;
		switch (max) {
			case min:
				h = 0;
				break;
			case r:
				h = g - b + d * (g < b ? 6 : 0);
				h /= 6 * d;
				break;
			case g:
				h = b - r + d * 2;
				h /= 6 * d;
				break;
			case b:
				h = r - g + d * 4;
				h /= 6 * d;
				break;
		}
		return {
			h: Math.round(h * 360),
			s: Math.round(s * 100),
			v: Math.round(v * 100),
			a
		};
	}
	function textToRgb(str) {
		if (typeof str !== "string") throw new TypeError("Expected a string");
		const color = str.replaceAll(" ", "");
		const m = reRGBA.exec(color);
		if (m === null) return hexToRgb(color);
		const rgb = {
			r: Math.min(255, Math.max(0, Number.parseInt(m[2], 10))),
			g: Math.min(255, Math.max(0, Number.parseInt(m[3], 10))),
			b: Math.min(255, Math.max(0, Number.parseInt(m[4], 10)))
		};
		if (m[1]) {
			const alpha = Number.parseFloat(m[5]);
			rgb.a = Math.round((Number.isFinite(alpha) ? Math.max(0, Math.min(1, alpha)) : 1) * 100);
		}
		return rgb;
	}
	function lighten(color, percent) {
		if (typeof color !== "string") throw new TypeError("Expected a string as color");
		if (typeof percent !== "number") throw new TypeError("Expected a numeric percent");
		const rgb = textToRgb(color), t = percent < 0 ? 0 : 255, p = Math.abs(percent) / 100, R = rgb.r, G = rgb.g, B = rgb.b;
		return "#" + (16777216 + (Math.round((t - R) * p) + R) * 65536 + (Math.round((t - G) * p) + G) * 256 + (Math.round((t - B) * p) + B)).toString(16).slice(1);
	}
	function luminosity(color) {
		if (typeof color !== "string" && (!color || color.r === void 0)) throw new TypeError("Expected a string or a {r, g, b} object as color");
		const rgb = typeof color === "string" ? textToRgb(color) : color, r = rgb.r / 255, g = rgb.g / 255, b = rgb.b / 255, R = r <= .03928 ? r / 12.92 : ((r + .055) / 1.055) ** 2.4, G = g <= .03928 ? g / 12.92 : ((g + .055) / 1.055) ** 2.4, B = b <= .03928 ? b / 12.92 : ((b + .055) / 1.055) ** 2.4;
		return .2126 * R + .7152 * G + .0722 * B;
	}
	function brightness(color) {
		if (typeof color !== "string" && (!color || color.r === void 0)) throw new TypeError("Expected a string or a {r, g, b} object as color");
		const rgb = typeof color === "string" ? textToRgb(color) : color;
		return (rgb.r * 299 + rgb.g * 587 + rgb.b * 114) / 1e3;
	}
	function blend(fgColor, bgColor) {
		if (typeof fgColor !== "string" && (!fgColor || fgColor.r === void 0)) throw new TypeError("Expected a string or a {r, g, b[, a]} object as fgColor");
		if (typeof bgColor !== "string" && (!bgColor || bgColor.r === void 0)) throw new TypeError("Expected a string or a {r, g, b[, a]} object as bgColor");
		const rgb1 = typeof fgColor === "string" ? textToRgb(fgColor) : fgColor, r1 = rgb1.r / 255, g1 = rgb1.g / 255, b1 = rgb1.b / 255, a1 = rgb1.a !== void 0 ? rgb1.a / 100 : 1, rgb2 = typeof bgColor === "string" ? textToRgb(bgColor) : bgColor, r2 = rgb2.r / 255, g2 = rgb2.g / 255, b2 = rgb2.b / 255, a2 = rgb2.a !== void 0 ? rgb2.a / 100 : 1, a = a1 + a2 * (1 - a1);
		const ret = {
			r: Math.round((r1 * a1 + r2 * a2 * (1 - a1)) / a * 255),
			g: Math.round((g1 * a1 + g2 * a2 * (1 - a1)) / a * 255),
			b: Math.round((b1 * a1 + b2 * a2 * (1 - a1)) / a * 255),
			a: Math.round(a * 100)
		};
		return typeof fgColor === "string" ? rgbToHex(ret) : ret;
	}
	function changeAlpha(color, offset) {
		if (typeof color !== "string") throw new TypeError("Expected a string as color");
		if (offset === void 0 || offset < -1 || offset > 1) throw new TypeError("Expected offset to be between -1 and 1");
		const { r, g, b, a } = textToRgb(color);
		const alpha = a !== void 0 ? a / 100 : 0;
		return rgbToHex({
			r,
			g,
			b,
			a: Math.round(Math.min(1, Math.max(0, alpha + offset)) * 100)
		});
	}
	function getPaletteColor(colorName) {
		if (typeof colorName !== "string") throw new TypeError("Expected a string as color");
		const el = document.createElement("div");
		el.className = `text-${colorName} invisible fixed no-pointer-events`;
		document.body.append(el);
		const result = getComputedStyle(el).getPropertyValue("color");
		el.remove();
		return rgbToHex(textToRgb(result));
	}
	var colors_default = {
		rgbToHex,
		hexToRgb,
		hsvToRgb,
		rgbToHsv,
		textToRgb,
		lighten,
		luminosity,
		brightness,
		blend,
		changeAlpha,
		getPaletteColor
	};
	//#endregion
	//#region src/components/color/QColor.js
	const palette = [
		"rgb(255,204,204)",
		"rgb(255,230,204)",
		"rgb(255,255,204)",
		"rgb(204,255,204)",
		"rgb(204,255,230)",
		"rgb(204,255,255)",
		"rgb(204,230,255)",
		"rgb(204,204,255)",
		"rgb(230,204,255)",
		"rgb(255,204,255)",
		"rgb(255,153,153)",
		"rgb(255,204,153)",
		"rgb(255,255,153)",
		"rgb(153,255,153)",
		"rgb(153,255,204)",
		"rgb(153,255,255)",
		"rgb(153,204,255)",
		"rgb(153,153,255)",
		"rgb(204,153,255)",
		"rgb(255,153,255)",
		"rgb(255,102,102)",
		"rgb(255,179,102)",
		"rgb(255,255,102)",
		"rgb(102,255,102)",
		"rgb(102,255,179)",
		"rgb(102,255,255)",
		"rgb(102,179,255)",
		"rgb(102,102,255)",
		"rgb(179,102,255)",
		"rgb(255,102,255)",
		"rgb(255,51,51)",
		"rgb(255,153,51)",
		"rgb(255,255,51)",
		"rgb(51,255,51)",
		"rgb(51,255,153)",
		"rgb(51,255,255)",
		"rgb(51,153,255)",
		"rgb(51,51,255)",
		"rgb(153,51,255)",
		"rgb(255,51,255)",
		"rgb(255,0,0)",
		"rgb(255,128,0)",
		"rgb(255,255,0)",
		"rgb(0,255,0)",
		"rgb(0,255,128)",
		"rgb(0,255,255)",
		"rgb(0,128,255)",
		"rgb(0,0,255)",
		"rgb(128,0,255)",
		"rgb(255,0,255)",
		"rgb(245,0,0)",
		"rgb(245,123,0)",
		"rgb(245,245,0)",
		"rgb(0,245,0)",
		"rgb(0,245,123)",
		"rgb(0,245,245)",
		"rgb(0,123,245)",
		"rgb(0,0,245)",
		"rgb(123,0,245)",
		"rgb(245,0,245)",
		"rgb(214,0,0)",
		"rgb(214,108,0)",
		"rgb(214,214,0)",
		"rgb(0,214,0)",
		"rgb(0,214,108)",
		"rgb(0,214,214)",
		"rgb(0,108,214)",
		"rgb(0,0,214)",
		"rgb(108,0,214)",
		"rgb(214,0,214)",
		"rgb(163,0,0)",
		"rgb(163,82,0)",
		"rgb(163,163,0)",
		"rgb(0,163,0)",
		"rgb(0,163,82)",
		"rgb(0,163,163)",
		"rgb(0,82,163)",
		"rgb(0,0,163)",
		"rgb(82,0,163)",
		"rgb(163,0,163)",
		"rgb(92,0,0)",
		"rgb(92,46,0)",
		"rgb(92,92,0)",
		"rgb(0,92,0)",
		"rgb(0,92,46)",
		"rgb(0,92,92)",
		"rgb(0,46,92)",
		"rgb(0,0,92)",
		"rgb(46,0,92)",
		"rgb(92,0,92)",
		"rgb(255,255,255)",
		"rgb(205,205,205)",
		"rgb(178,178,178)",
		"rgb(153,153,153)",
		"rgb(127,127,127)",
		"rgb(102,102,102)",
		"rgb(76,76,76)",
		"rgb(51,51,51)",
		"rgb(25,25,25)",
		"rgb(0,0,0)"
	];
	const thumbPath = "M5 5 h10 v10 h-10 v-10 z";
	const alphaTrackImg = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAgAAAAICAYAAADED76LAAAAH0lEQVQoU2NkYGAwZkAFZ5G5jPRRgOYEVDeB3EBjBQBOZwTVugIGyAAAAABJRU5ErkJggg==";
	const numericRE = /^[0-9]+$/;
	const hexRE = /^#[0-9A-Fa-f]+$/;
	const rgbRE = /^rgb\([0-9]{1,3},[0-9]{1,3},[0-9]{1,3}\)$/;
	const rgbaRE = /^rgba\([0-9]{1,3},[0-9]{1,3},[0-9]{1,3},(0|0\.[0-9]+[1-9]|0\.[1-9]+|1)\)$/;
	var QColor_default = createComponent({
		name: "QColor",
		props: {
			...useDarkProps,
			...useFormProps,
			modelValue: String,
			defaultValue: String,
			defaultView: {
				type: String,
				default: "spectrum",
				validator: (v) => [
					"spectrum",
					"tune",
					"palette"
				].includes(v)
			},
			formatModel: {
				type: String,
				default: "auto",
				validator: (v) => [
					"auto",
					"hex",
					"rgb",
					"hexa",
					"rgba"
				].includes(v)
			},
			palette: Array,
			noHeader: Boolean,
			noHeaderTabs: Boolean,
			noFooter: Boolean,
			square: Boolean,
			flat: Boolean,
			bordered: Boolean,
			disable: Boolean,
			readonly: Boolean
		},
		emits: ["update:modelValue", "change"],
		setup(props, { emit }) {
			const { proxy } = (0, vue.getCurrentInstance)();
			const { $q } = proxy;
			const isDark = useDark(props, $q);
			const { getCache } = useRenderCache();
			const spectrumRef = (0, vue.ref)(null);
			const errorIconRef = (0, vue.ref)(null);
			const forceHex = (0, vue.computed)(() => props.formatModel === "auto" ? null : props.formatModel.includes("hex"));
			const forceAlpha = (0, vue.computed)(() => props.formatModel === "auto" ? null : props.formatModel.includes("a"));
			const topView = (0, vue.ref)(props.formatModel === "auto" ? props.modelValue === void 0 || props.modelValue === null || props.modelValue === "" || props.modelValue.startsWith("#") ? "hex" : "rgb" : props.formatModel.startsWith("hex") ? "hex" : "rgb");
			const view = (0, vue.ref)(props.defaultView);
			const model = (0, vue.ref)(parseModel(props.modelValue || props.defaultValue));
			const editable = (0, vue.computed)(() => !props.disable && !props.readonly);
			const isHex = (0, vue.computed)(() => props.modelValue === void 0 || props.modelValue === null || props.modelValue === "" || props.modelValue.startsWith("#"));
			const isOutputHex = (0, vue.computed)(() => forceHex.value !== null ? forceHex.value : isHex.value);
			const injectFormInput = useFormInject((0, vue.computed)(() => ({
				type: "hidden",
				name: props.name,
				value: model.value[isOutputHex.value ? "hex" : "rgb"]
			})));
			const hasAlpha = (0, vue.computed)(() => forceAlpha.value !== null ? forceAlpha.value : model.value.a !== void 0);
			const currentBgColor = (0, vue.computed)(() => ({ backgroundColor: model.value.rgb || "#000" }));
			const headerClass = (0, vue.computed)(() => {
				return `q-color-picker__header-content q-color-picker__header-content--${(model.value.a !== void 0 && model.value.a < 65 ? true : luminosity(model.value) > .4) ? "light" : "dark"}`;
			});
			const spectrumStyle = (0, vue.computed)(() => ({ background: `hsl(${model.value.h},100%,50%)` }));
			const spectrumPointerStyle = (0, vue.computed)(() => ({
				top: `${100 - model.value.v}%`,
				[$q.lang.rtl ? "right" : "left"]: `${model.value.s}%`
			}));
			const computedPalette = (0, vue.computed)(() => props.palette !== void 0 && props.palette.length !== 0 ? props.palette : palette);
			const classes = (0, vue.computed)(() => "q-color-picker" + (props.bordered ? " q-color-picker--bordered" : "") + (props.square ? " q-color-picker--square no-border-radius" : "") + (props.flat ? " q-color-picker--flat no-shadow" : "") + (props.disable ? " disabled" : "") + (isDark.value ? " q-color-picker--dark q-dark" : ""));
			const attributes = (0, vue.computed)(() => props.disable ? { "aria-disabled": "true" } : {});
			const spectrumDirective = (0, vue.computed)(() => [[
				TouchPan_default,
				onSpectrumPan,
				void 0,
				{
					prevent: true,
					stop: true,
					mouse: true
				}
			]]);
			(0, vue.watch)(() => props.modelValue, (v) => {
				const localModel = parseModel(v || props.defaultValue);
				if (localModel.hex !== model.value.hex) model.value = localModel;
			});
			(0, vue.watch)(() => props.defaultValue, (v) => {
				if (!props.modelValue && v) {
					const localModel = parseModel(v);
					if (localModel.hex !== model.value.hex) model.value = localModel;
				}
			});
			function updateModel(rgb, change) {
				model.value.hex = rgbToHex(rgb);
				model.value.rgb = rgbToString(rgb);
				model.value.r = rgb.r;
				model.value.g = rgb.g;
				model.value.b = rgb.b;
				model.value.a = rgb.a;
				const value = model.value[isOutputHex.value ? "hex" : "rgb"];
				emit("update:modelValue", value);
				if (change) emit("change", value);
			}
			function parseModel(v) {
				const alpha = forceAlpha.value !== void 0 ? forceAlpha.value : props.formatModel === "auto" ? null : props.formatModel.includes("a");
				if (typeof v !== "string" || v.length === 0 || !testPattern.anyColor(v.replaceAll(" ", ""))) return {
					h: 0,
					s: 0,
					v: 0,
					r: 0,
					g: 0,
					b: 0,
					a: alpha ? 100 : void 0,
					hex: void 0,
					rgb: void 0
				};
				const localModel = textToRgb(v);
				if (alpha && localModel.a === void 0) localModel.a = 100;
				localModel.hex = rgbToHex(localModel);
				localModel.rgb = rgbToString(localModel);
				return Object.assign(localModel, rgbToHsv(localModel));
			}
			function changeSpectrum(left, top, change) {
				const panel = spectrumRef.value;
				if (panel === null) return;
				const width = panel.clientWidth, height = panel.clientHeight, rect = panel.getBoundingClientRect();
				let x = Math.min(width, Math.max(0, left - rect.left));
				if ($q.lang.rtl) x = width - x;
				const y = Math.min(height, Math.max(0, top - rect.top)), s = Math.round(100 * x / width), v = Math.round(100 * Math.max(0, Math.min(1, -(y / height) + 1))), rgb = hsvToRgb({
					h: model.value.h,
					s,
					v,
					a: hasAlpha.value ? model.value.a : void 0
				});
				model.value.s = s;
				model.value.v = v;
				updateModel(rgb, change);
			}
			function onHue(val, change) {
				const hue = Math.round(val);
				const rgb = hsvToRgb({
					h: hue,
					s: model.value.s,
					v: model.value.v,
					a: hasAlpha.value ? model.value.a : void 0
				});
				model.value.h = hue;
				updateModel(rgb, change);
			}
			function onHueChange(val) {
				onHue(val, true);
			}
			function onNumericChange(value, formatModel, max, evt, change) {
				if (evt !== void 0) stop(evt);
				if (!numericRE.test(value)) {
					if (change) proxy.$forceUpdate();
					return;
				}
				const val = Math.floor(Number(value));
				if (val < 0 || val > max) {
					if (change) proxy.$forceUpdate();
					return;
				}
				const rgb = {
					r: formatModel === "r" ? val : model.value.r,
					g: formatModel === "g" ? val : model.value.g,
					b: formatModel === "b" ? val : model.value.b,
					a: hasAlpha.value ? formatModel === "a" ? val : model.value.a : void 0
				};
				if (formatModel !== "a") {
					const hsv = rgbToHsv(rgb);
					model.value.h = hsv.h;
					model.value.s = hsv.s;
					model.value.v = hsv.v;
				}
				updateModel(rgb, change);
				if (!change && evt?.target.selectionEnd !== void 0) {
					const index = evt.target.selectionEnd;
					(0, vue.nextTick)(() => {
						evt.target.setSelectionRange(index, index);
					});
				}
			}
			function onEditorChange(evt, change) {
				let rgb;
				const inp = evt.target.value;
				stop(evt);
				if (topView.value === "hex") {
					if (inp.length !== (hasAlpha.value ? 9 : 7) || !hexRE.test(inp)) return true;
					rgb = hexToRgb(inp);
				} else {
					let localModel;
					if (!inp.endsWith(")")) return true;
					else if (!hasAlpha.value && inp.startsWith("rgb(")) {
						localModel = inp.slice(4, -1).split(",").map((n) => Number.parseInt(n, 10));
						if (localModel.length !== 3 || !rgbRE.test(inp)) return true;
					} else if (hasAlpha.value && inp.startsWith("rgba(")) {
						localModel = inp.slice(5, -1).split(",");
						if (localModel.length !== 4 || !rgbaRE.test(inp)) return true;
						for (let i = 0; i < 3; i++) {
							const v = Number.parseInt(localModel[i], 10);
							if (v < 0 || v > 255) return true;
							localModel[i] = v;
						}
						const v = Number.parseFloat(localModel[3]);
						if (v < 0 || v > 1) return true;
						localModel[3] = v;
					} else return true;
					if (localModel[0] < 0 || localModel[0] > 255 || localModel[1] < 0 || localModel[1] > 255 || localModel[2] < 0 || localModel[2] > 255 || hasAlpha.value && (localModel[3] < 0 || localModel[3] > 1)) return true;
					rgb = {
						r: localModel[0],
						g: localModel[1],
						b: localModel[2],
						a: hasAlpha.value ? localModel[3] * 100 : void 0
					};
				}
				const hsv = rgbToHsv(rgb);
				model.value.h = hsv.h;
				model.value.s = hsv.s;
				model.value.v = hsv.v;
				updateModel(rgb, change);
				if (!change) {
					const index = evt.target.selectionEnd;
					(0, vue.nextTick)(() => {
						evt.target.setSelectionRange(index, index);
					});
				}
			}
			function onPalettePick(color) {
				const def = parseModel(color);
				const rgb = {
					r: def.r,
					g: def.g,
					b: def.b,
					a: def.a
				};
				if (rgb.a === void 0) rgb.a = model.value.a;
				model.value.h = def.h;
				model.value.s = def.s;
				model.value.v = def.v;
				updateModel(rgb, true);
			}
			function onSpectrumPan(evt) {
				if (evt.isFinal) changeSpectrum(evt.position.left, evt.position.top, true);
				else onSpectrumChange(evt);
			}
			const onSpectrumChange = throttle((evt) => {
				changeSpectrum(evt.position.left, evt.position.top);
			}, 20);
			function onSpectrumClick(evt) {
				changeSpectrum(evt.pageX - window.pageXOffset, evt.pageY - window.pageYOffset, true);
			}
			function onActivate(evt) {
				changeSpectrum(evt.pageX - window.pageXOffset, evt.pageY - window.pageYOffset);
			}
			function updateErrorIcon(val) {
				if (errorIconRef.value !== null) errorIconRef.value.$el.style.opacity = val ? 1 : 0;
			}
			function setTopView(val) {
				topView.value = val;
			}
			function getHeader() {
				const child = [];
				if (!props.noHeaderTabs) child.push((0, vue.h)(QTabs_default, {
					class: "q-color-picker__header-tabs",
					modelValue: topView.value,
					dense: true,
					align: "justify",
					"onUpdate:modelValue": setTopView
				}, () => [(0, vue.h)(QTab_default, {
					label: "HEX" + (hasAlpha.value ? "A" : ""),
					name: "hex",
					ripple: false
				}), (0, vue.h)(QTab_default, {
					label: "RGB" + (hasAlpha.value ? "A" : ""),
					name: "rgb",
					ripple: false
				})]));
				child.push((0, vue.h)("div", { class: "q-color-picker__header-banner row flex-center no-wrap" }, [(0, vue.h)("input", {
					class: "fit",
					value: model.value[topView.value],
					...editable.value ? {} : { readonly: true },
					...getCache("topIn", {
						onInput: (evt) => {
							updateErrorIcon(onEditorChange(evt));
						},
						onChange: stop,
						onBlur: (evt) => {
							if (onEditorChange(evt, true)) proxy.$forceUpdate();
							updateErrorIcon(false);
						}
					})
				}), (0, vue.h)(QIcon_default, {
					ref: errorIconRef,
					class: "q-color-picker__error-icon absolute no-pointer-events",
					name: $q.iconSet.type.negative
				})]));
				return (0, vue.h)("div", { class: "q-color-picker__header relative-position overflow-hidden" }, [(0, vue.h)("div", { class: "q-color-picker__header-bg absolute-full" }), (0, vue.h)("div", {
					class: headerClass.value,
					style: currentBgColor.value
				}, child)]);
			}
			function getContent() {
				return (0, vue.h)(QTabPanels_default, {
					modelValue: view.value,
					animated: true
				}, () => [
					(0, vue.h)(QTabPanel_default, {
						class: "q-color-picker__spectrum-tab overflow-hidden",
						name: "spectrum"
					}, getSpectrumTab),
					(0, vue.h)(QTabPanel_default, {
						class: "q-pa-md q-color-picker__tune-tab",
						name: "tune"
					}, getTuneTab),
					(0, vue.h)(QTabPanel_default, {
						class: "q-color-picker__palette-tab",
						name: "palette"
					}, getPaletteTab)
				]);
			}
			function setView(val) {
				view.value = val;
			}
			function getFooter() {
				return (0, vue.h)("div", { class: "q-color-picker__footer relative-position overflow-hidden" }, [(0, vue.h)(QTabs_default, {
					class: "absolute-full",
					modelValue: view.value,
					dense: true,
					align: "justify",
					"onUpdate:modelValue": setView
				}, () => [
					(0, vue.h)(QTab_default, {
						icon: $q.iconSet.colorPicker.spectrum,
						name: "spectrum",
						ripple: false
					}),
					(0, vue.h)(QTab_default, {
						icon: $q.iconSet.colorPicker.tune,
						name: "tune",
						ripple: false
					}),
					(0, vue.h)(QTab_default, {
						icon: $q.iconSet.colorPicker.palette,
						name: "palette",
						ripple: false
					})
				])]);
			}
			function getSpectrumTab() {
				const data = {
					ref: spectrumRef,
					class: "q-color-picker__spectrum non-selectable relative-position cursor-pointer" + (editable.value ? "" : " readonly"),
					style: spectrumStyle.value,
					...editable.value ? {
						onClick: onSpectrumClick,
						onMousedown: onActivate
					} : {}
				};
				const child = [
					(0, vue.h)("div", { style: { paddingBottom: "100%" } }),
					(0, vue.h)("div", { class: "q-color-picker__spectrum-white absolute-full" }),
					(0, vue.h)("div", { class: "q-color-picker__spectrum-black absolute-full" }),
					(0, vue.h)("div", {
						class: "absolute",
						style: spectrumPointerStyle.value
					}, [model.value.hex !== void 0 ? (0, vue.h)("div", { class: "q-color-picker__spectrum-circle" }) : null])
				];
				const sliders = [(0, vue.h)(QSlider_default, {
					class: "q-color-picker__hue non-selectable",
					modelValue: model.value.h,
					min: 0,
					max: 360,
					trackSize: "8px",
					innerTrackColor: "transparent",
					selectionColor: "transparent",
					readonly: !editable.value,
					thumbPath,
					"onUpdate:modelValue": onHue,
					onChange: onHueChange
				})];
				if (hasAlpha.value) sliders.push((0, vue.h)(QSlider_default, {
					class: "q-color-picker__alpha non-selectable",
					modelValue: model.value.a,
					min: 0,
					max: 100,
					trackSize: "8px",
					trackColor: "white",
					innerTrackColor: "transparent",
					selectionColor: "transparent",
					trackImg: alphaTrackImg,
					readonly: !editable.value,
					hideSelection: true,
					thumbPath,
					...getCache("alphaSlide", {
						"onUpdate:modelValue": (value) => onNumericChange(value, "a", 100),
						onChange: (value) => onNumericChange(value, "a", 100, void 0, true)
					})
				}));
				return [hDir("div", data, child, "spec", editable.value, () => spectrumDirective.value), (0, vue.h)("div", { class: "q-color-picker__sliders" }, sliders)];
			}
			function getTuneTab() {
				return [
					(0, vue.h)("div", { class: "row items-center no-wrap" }, [
						(0, vue.h)("div", "R"),
						(0, vue.h)(QSlider_default, {
							modelValue: model.value.r,
							min: 0,
							max: 255,
							color: "red",
							dark: isDark.value,
							readonly: !editable.value,
							...getCache("rSlide", {
								"onUpdate:modelValue": (value) => onNumericChange(value, "r", 255),
								onChange: (value) => onNumericChange(value, "r", 255, void 0, true)
							})
						}),
						(0, vue.h)("input", {
							value: model.value.r,
							maxlength: 3,
							readonly: !editable.value,
							onChange: stop,
							...getCache("rIn", {
								onInput: (evt) => onNumericChange(evt.target.value, "r", 255, evt),
								onBlur: (evt) => onNumericChange(evt.target.value, "r", 255, evt, true)
							})
						})
					]),
					(0, vue.h)("div", { class: "row items-center no-wrap" }, [
						(0, vue.h)("div", "G"),
						(0, vue.h)(QSlider_default, {
							modelValue: model.value.g,
							min: 0,
							max: 255,
							color: "green",
							dark: isDark.value,
							readonly: !editable.value,
							...getCache("gSlide", {
								"onUpdate:modelValue": (value) => onNumericChange(value, "g", 255),
								onChange: (value) => onNumericChange(value, "g", 255, void 0, true)
							})
						}),
						(0, vue.h)("input", {
							value: model.value.g,
							maxlength: 3,
							readonly: !editable.value,
							onChange: stop,
							...getCache("gIn", {
								onInput: (evt) => onNumericChange(evt.target.value, "g", 255, evt),
								onBlur: (evt) => onNumericChange(evt.target.value, "g", 255, evt, true)
							})
						})
					]),
					(0, vue.h)("div", { class: "row items-center no-wrap" }, [
						(0, vue.h)("div", "B"),
						(0, vue.h)(QSlider_default, {
							modelValue: model.value.b,
							min: 0,
							max: 255,
							color: "blue",
							readonly: !editable.value,
							dark: isDark.value,
							...getCache("bSlide", {
								"onUpdate:modelValue": (value) => onNumericChange(value, "b", 255),
								onChange: (value) => onNumericChange(value, "b", 255, void 0, true)
							})
						}),
						(0, vue.h)("input", {
							value: model.value.b,
							maxlength: 3,
							readonly: !editable.value,
							onChange: stop,
							...getCache("bIn", {
								onInput: (evt) => onNumericChange(evt.target.value, "b", 255, evt),
								onBlur: (evt) => onNumericChange(evt.target.value, "b", 255, evt, true)
							})
						})
					]),
					hasAlpha.value ? (0, vue.h)("div", { class: "row items-center no-wrap" }, [
						(0, vue.h)("div", "A"),
						(0, vue.h)(QSlider_default, {
							modelValue: model.value.a,
							color: "grey",
							readonly: !editable.value,
							dark: isDark.value,
							...getCache("aSlide", {
								"onUpdate:modelValue": (value) => onNumericChange(value, "a", 100),
								onChange: (value) => onNumericChange(value, "a", 100, void 0, true)
							})
						}),
						(0, vue.h)("input", {
							value: model.value.a,
							maxlength: 3,
							readonly: !editable.value,
							onChange: stop,
							...getCache("aIn", {
								onInput: (evt) => onNumericChange(evt.target.value, "a", 100, evt),
								onBlur: (evt) => onNumericChange(evt.target.value, "a", 100, evt, true)
							})
						})
					]) : null
				];
			}
			function getPaletteTab() {
				const fn = (color) => (0, vue.h)("div", {
					class: "q-color-picker__cube col-auto",
					style: { backgroundColor: color },
					...editable.value ? getCache("palette#" + color, { onClick: () => {
						onPalettePick(color);
					} }) : {}
				});
				return [(0, vue.h)("div", { class: "row items-center q-color-picker__palette-rows" + (editable.value ? " q-color-picker__palette-rows--editable" : "") }, computedPalette.value.map(fn))];
			}
			return () => {
				const child = [getContent()];
				if (props.name !== void 0 && !props.disable) injectFormInput(child, "push");
				if (!props.noHeader) child.unshift(getHeader());
				if (!props.noFooter) child.push(getFooter());
				return (0, vue.h)("div", {
					class: classes.value,
					...attributes.value
				}, child);
			};
		}
	});
	//#endregion
	//#region src/utils/date/private.persian.js
	const breaks = [
		-61,
		9,
		38,
		199,
		426,
		686,
		756,
		818,
		1111,
		1181,
		1210,
		1635,
		2060,
		2097,
		2192,
		2262,
		2324,
		2394,
		2456,
		3178
	];
	function toJalaali(gy, gm, gd) {
		if (Object.prototype.toString.call(gy) === "[object Date]") {
			gd = gy.getDate();
			gm = gy.getMonth() + 1;
			gy = gy.getFullYear();
		}
		return d2j(g2d(gy, gm, gd));
	}
	function toGregorian(jy, jm, jd) {
		return d2g(j2d(jy, jm, jd));
	}
	function isLeapJalaaliYear(jy) {
		return jalCalLeap(jy) === 0;
	}
	function jalaaliMonthLength(jy, jm) {
		if (jm <= 6) return 31;
		if (jm <= 11) return 30;
		if (isLeapJalaaliYear(jy)) return 30;
		return 29;
	}
	function jalCalLeap(jy) {
		const bl = breaks.length;
		let jp = breaks[0], jm, jump, leap, n, i;
		if (jy < jp || jy >= breaks[bl - 1]) throw new Error("Invalid Jalaali year " + jy);
		for (i = 1; i < bl; i += 1) {
			jm = breaks[i];
			jump = jm - jp;
			if (jy < jm) break;
			jp = jm;
		}
		n = jy - jp;
		if (jump - n < 6) n = n - jump + div(jump + 4, 33) * 33;
		leap = mod(mod(n + 1, 33) - 1, 4);
		if (leap === -1) leap = 4;
		return leap;
	}
	function jalCal(jy, withoutLeap) {
		const bl = breaks.length, gy = jy + 621;
		let leapJ = -14, jp = breaks[0], jm, jump, leap, n, i;
		if (jy < jp || jy >= breaks[bl - 1]) throw new Error("Invalid Jalaali year " + jy);
		for (i = 1; i < bl; i += 1) {
			jm = breaks[i];
			jump = jm - jp;
			if (jy < jm) break;
			leapJ = leapJ + div(jump, 33) * 8 + div(mod(jump, 33), 4);
			jp = jm;
		}
		n = jy - jp;
		leapJ = leapJ + div(n, 33) * 8 + div(mod(n, 33) + 3, 4);
		if (mod(jump, 33) === 4 && jump - n === 4) leapJ += 1;
		const leapG = div(gy, 4) - div((div(gy, 100) + 1) * 3, 4) - 150;
		const march = 20 + leapJ - leapG;
		if (!withoutLeap) {
			if (jump - n < 6) n = n - jump + div(jump + 4, 33) * 33;
			leap = mod(mod(n + 1, 33) - 1, 4);
			if (leap === -1) leap = 4;
		}
		return {
			leap,
			gy,
			march
		};
	}
	function j2d(jy, jm, jd) {
		const r = jalCal(jy, true);
		return g2d(r.gy, 3, r.march) + (jm - 1) * 31 - div(jm, 7) * (jm - 7) + jd - 1;
	}
	function d2j(jdn) {
		const gy = d2g(jdn).gy;
		let jy = gy - 621, jd, jm, k;
		const r = jalCal(jy, false);
		k = jdn - g2d(gy, 3, r.march);
		if (k >= 0) {
			if (k <= 185) {
				jm = 1 + div(k, 31);
				jd = mod(k, 31) + 1;
				return {
					jy,
					jm,
					jd
				};
			}
			k -= 186;
		} else {
			jy -= 1;
			k += 179;
			if (r.leap === 1) k += 1;
		}
		jm = 7 + div(k, 30);
		jd = mod(k, 30) + 1;
		return {
			jy,
			jm,
			jd
		};
	}
	function g2d(gy, gm, gd) {
		let d = div((gy + div(gm - 8, 6) + 100100) * 1461, 4) + div(153 * mod(gm + 9, 12) + 2, 5) + gd - 34840408;
		d = d - div(div(gy + 100100 + div(gm - 8, 6), 100) * 3, 4) + 752;
		return d;
	}
	function d2g(jdn) {
		let j = 4 * jdn + 139361631;
		j = j + div(div(4 * jdn + 183187720, 146097) * 3, 4) * 4 - 3908;
		const i = div(mod(j, 1461), 4) * 5 + 308, gd = div(mod(i, 153), 5) + 1, gm = mod(div(i, 153), 12) + 1;
		return {
			gy: div(j, 1461) - 100100 + div(8 - gm, 6),
			gm,
			gd
		};
	}
	function div(a, b) {
		return Math.trunc(a / b);
	}
	function mod(a, b) {
		return a - Math.trunc(a / b) * b;
	}
	//#endregion
	//#region src/components/date/use-datetime.js
	const calendars = ["gregorian", "persian"];
	const useDatetimeProps = {
		mask: { type: String },
		locale: Object,
		calendar: {
			type: String,
			validator: (v) => calendars.includes(v),
			default: "gregorian"
		},
		landscape: Boolean,
		color: String,
		textColor: String,
		square: Boolean,
		flat: Boolean,
		bordered: Boolean,
		readonly: Boolean,
		disable: Boolean
	};
	const useDatetimeEmits = ["update:modelValue"];
	function getDayHash(date) {
		return date.year + "/" + pad(date.month) + "/" + pad(date.day);
	}
	function useDatetime(props, $q) {
		const editable = (0, vue.computed)(() => !props.disable && !props.readonly);
		const tabindex = (0, vue.computed)(() => editable.value ? 0 : -1);
		const headerClass = (0, vue.computed)(() => {
			const cls = [];
			if (props.color !== void 0) cls.push(`bg-${props.color}`);
			if (props.textColor !== void 0) cls.push(`text-${props.textColor}`);
			return cls.join(" ");
		});
		function getLocale() {
			return props.locale !== void 0 ? {
				...$q.lang.date,
				...props.locale
			} : $q.lang.date;
		}
		function getCurrentDate(dateOnly) {
			const d = /* @__PURE__ */ new Date();
			const timeFill = dateOnly ? null : 0;
			if (props.calendar === "persian") {
				const jDate = toJalaali(d);
				return {
					year: jDate.jy,
					month: jDate.jm,
					day: jDate.jd
				};
			}
			return {
				year: d.getFullYear(),
				month: d.getMonth() + 1,
				day: d.getDate(),
				hour: timeFill,
				minute: timeFill,
				second: timeFill,
				millisecond: timeFill
			};
		}
		return {
			editable,
			tabindex,
			headerClass,
			getLocale,
			getCurrentDate
		};
	}
	//#endregion
	//#region src/utils/date/date.js
	const MILLISECONDS_IN_DAY = 864e5;
	const MILLISECONDS_IN_HOUR = 36e5;
	const MILLISECONDS_IN_MINUTE = 6e4;
	const defaultMask = "YYYY-MM-DDTHH:mm:ss.SSSZ";
	const token = /\[((?:[^\]\\]|\\]|\\)*)\]|do|d{1,4}|Mo|M{1,4}|m{1,2}|wo|w{1,2}|Qo|Do|DDDo|D{1,4}|YY(?:YY)?|H{1,2}|h{1,2}|s{1,2}|S{1,3}|Z{1,2}|a{1,2}|[AQExX]/g;
	const reverseToken = /(\[[^\]]*\])|do|d{1,4}|Mo|M{1,4}|m{1,2}|wo|w{1,2}|Qo|Do|DDDo|D{1,4}|YY(?:YY)?|H{1,2}|h{1,2}|s{1,2}|S{1,3}|Z{1,2}|a{1,2}|[AQExX]|([.*+:?^,\s${}()|\\]+)/g;
	const regexStore = {};
	function getRegexData(mask, dateLocale) {
		const days = "(" + dateLocale.days.join("|") + ")", key = mask + days;
		if (regexStore[key] !== void 0) return regexStore[key];
		const daysShort = "(" + dateLocale.daysShort.join("|") + ")", months = "(" + dateLocale.months.join("|") + ")", monthsShort = "(" + dateLocale.monthsShort.join("|") + ")";
		const map = {};
		let index = 0;
		const regexText = mask.replace(reverseToken, (match) => {
			index++;
			switch (match) {
				case "YY":
					map.YY = index;
					return String.raw`(-?\d{1,2})`;
				case "YYYY":
					map.YYYY = index;
					return String.raw`(-?\d{1,4})`;
				case "M":
					map.M = index;
					return String.raw`(\d{1,2})`;
				case "Mo":
					map.M = index++;
					return String.raw`(\d{1,2}(st|nd|rd|th))`;
				case "MM":
					map.M = index;
					return String.raw`(\d{2})`;
				case "MMM":
					map.MMM = index;
					return monthsShort;
				case "MMMM":
					map.MMMM = index;
					return months;
				case "D":
					map.D = index;
					return String.raw`(\d{1,2})`;
				case "Do":
					map.D = index++;
					return String.raw`(\d{1,2}(st|nd|rd|th))`;
				case "DD":
					map.D = index;
					return String.raw`(\d{2})`;
				case "H":
					map.H = index;
					return String.raw`(\d{1,2})`;
				case "HH":
					map.H = index;
					return String.raw`(\d{2})`;
				case "h":
					map.h = index;
					return String.raw`(\d{1,2})`;
				case "hh":
					map.h = index;
					return String.raw`(\d{2})`;
				case "m":
					map.m = index;
					return String.raw`(\d{1,2})`;
				case "mm":
					map.m = index;
					return String.raw`(\d{2})`;
				case "s":
					map.s = index;
					return String.raw`(\d{1,2})`;
				case "ss":
					map.s = index;
					return String.raw`(\d{2})`;
				case "S":
					map.S = index;
					return String.raw`(\d{1})`;
				case "SS":
					map.S = index;
					return String.raw`(\d{2})`;
				case "SSS":
					map.S = index;
					return String.raw`(\d{3})`;
				case "A":
					map.A = index;
					return "(AM|PM)";
				case "a":
					map.a = index;
					return "(am|pm)";
				case "aa":
					map.aa = index;
					return String.raw`(a\.m\.|p\.m\.)`;
				case "ddd": return daysShort;
				case "dddd": return days;
				case "Q":
				case "d":
				case "E": return String.raw`(\d{1})`;
				case "do":
					index++;
					return String.raw`(\d{1}(st|nd|rd|th))`;
				case "Qo": return "(1st|2nd|3rd|4th)";
				case "DDD":
				case "DDDD": return String.raw`(\d{1,3})`;
				case "DDDo":
					index++;
					return String.raw`(\d{1,3}(st|nd|rd|th))`;
				case "w": return String.raw`(\d{1,2})`;
				case "wo":
					index++;
					return String.raw`(\d{1,2}(st|nd|rd|th))`;
				case "ww": return String.raw`(\d{2})`;
				case "Z":
					map.Z = index;
					return String.raw`(Z|[+-]\d{2}:\d{2})`;
				case "ZZ":
					map.ZZ = index;
					return String.raw`(Z|[+-]\d{2}\d{2})`;
				case "X":
					map.X = index;
					return String.raw`(-?\d+)`;
				case "x":
					map.x = index;
					return String.raw`(-?\d{4,})`;
				default:
					index--;
					if (match[0] === "[") match = match.slice(1, -1);
					return match.replaceAll(/[.*+?^${}()|[\]\\]/g, String.raw`\$&`);
			}
		});
		const res = {
			map,
			regex: new RegExp("^" + regexText)
		};
		regexStore[key] = res;
		return res;
	}
	function getDateLocale(paramDateLocale, langProps) {
		return paramDateLocale !== void 0 ? paramDateLocale : langProps !== void 0 ? langProps.date : en_US_default.date;
	}
	function formatTimezone(offset, delimeter = "") {
		const sign = offset > 0 ? "-" : "+", absOffset = Math.abs(offset), hours = Math.floor(absOffset / 60), minutes = absOffset % 60;
		return sign + pad(hours) + delimeter + pad(minutes);
	}
	function applyYearMonthDayChange(date, mod, sign) {
		let year = date.getFullYear(), month = date.getMonth();
		const day = date.getDate();
		if (mod.year !== void 0) {
			year += sign * mod.year;
			delete mod.year;
		}
		if (mod.month !== void 0) {
			month += sign * mod.month;
			delete mod.month;
		}
		date.setDate(1);
		date.setMonth(2);
		date.setFullYear(year);
		date.setMonth(month);
		date.setDate(Math.min(day, daysInMonth(date)));
		if (mod.date !== void 0) {
			date.setDate(date.getDate() + sign * mod.date);
			delete mod.date;
		}
		return date;
	}
	function applyYearMonthDay(date, mod, middle) {
		const year = mod.year !== void 0 ? mod.year : date[`get${middle}FullYear`](), month = mod.month !== void 0 ? mod.month - 1 : date[`get${middle}Month`](), maxDay = new Date(year, month + 1, 0).getDate(), day = Math.min(maxDay, mod.date !== void 0 ? mod.date : date[`get${middle}Date`]());
		date[`set${middle}Date`](1);
		date[`set${middle}Month`](2);
		date[`set${middle}FullYear`](year);
		date[`set${middle}Month`](month);
		date[`set${middle}Date`](day);
		delete mod.year;
		delete mod.month;
		delete mod.date;
		return date;
	}
	function getChange(date, rawMod, sign) {
		const mod = normalizeMod(rawMod), d = new Date(date), t = mod.year !== void 0 || mod.month !== void 0 || mod.date !== void 0 ? applyYearMonthDayChange(d, mod, sign) : d;
		for (const key in mod) {
			const op = capitalize(key);
			t[`set${op}`](t[`get${op}`]() + sign * mod[key]);
		}
		return t;
	}
	function normalizeMod(mod) {
		const acc = { ...mod };
		if (mod.years !== void 0) {
			acc.year = mod.years;
			delete acc.years;
		}
		if (mod.months !== void 0) {
			acc.month = mod.months;
			delete acc.months;
		}
		if (mod.days !== void 0) {
			acc.date = mod.days;
			delete acc.days;
		}
		if (mod.day !== void 0) {
			acc.date = mod.day;
			delete acc.day;
		}
		if (mod.hour !== void 0) {
			acc.hours = mod.hour;
			delete acc.hour;
		}
		if (mod.minute !== void 0) {
			acc.minutes = mod.minute;
			delete acc.minute;
		}
		if (mod.second !== void 0) {
			acc.seconds = mod.second;
			delete acc.second;
		}
		if (mod.millisecond !== void 0) {
			acc.milliseconds = mod.millisecond;
			delete acc.millisecond;
		}
		return acc;
	}
	function adjustDate(date, rawMod, utc) {
		const mod = normalizeMod(rawMod), middle = utc ? "UTC" : "", d = new Date(date), t = mod.year !== void 0 || mod.month !== void 0 || mod.date !== void 0 ? applyYearMonthDay(d, mod, middle) : d;
		for (const key in mod) t[`set${middle}${key.at(0).toUpperCase() + key.slice(1)}`](mod[key]);
		return t;
	}
	function extractDate(str, mask, dateLocale) {
		const d = __splitDate(str, mask, dateLocale);
		const date = new Date(d.year, d.month === null ? null : d.month - 1, d.day === null ? 1 : d.day, d.hour, d.minute, d.second, d.millisecond);
		const tzOffset = date.getTimezoneOffset();
		return d.timezoneOffset === null || d.timezoneOffset === tzOffset ? date : getChange(date, { minutes: d.timezoneOffset - tzOffset }, 1);
	}
	function __splitDate(str, mask, dateLocale, calendar, defaultModel) {
		const date = {
			year: null,
			month: null,
			day: null,
			hour: null,
			minute: null,
			second: null,
			millisecond: null,
			timezoneOffset: null,
			dateHash: null,
			timeHash: null
		};
		if (defaultModel !== void 0) Object.assign(date, defaultModel);
		if (str === void 0 || str === null || str === "" || typeof str !== "string") return date;
		if (mask === void 0) mask = defaultMask;
		const langOpts = getDateLocale(dateLocale, Plugin$8.props), months = langOpts.months, monthsShort = langOpts.monthsShort;
		const { regex, map } = getRegexData(mask, langOpts);
		const match = str.match(regex);
		if (match === null) return date;
		let tzString = "";
		if (map.X !== void 0 || map.x !== void 0) {
			const stamp = Number.parseInt(match[map.X ?? map.x], 10);
			if (Number.isNaN(stamp) || stamp < 0) return date;
			const d = /* @__PURE__ */ new Date(stamp * (map.X !== void 0 ? 1e3 : 1));
			date.year = d.getFullYear();
			date.month = d.getMonth() + 1;
			date.day = d.getDate();
			date.hour = d.getHours();
			date.minute = d.getMinutes();
			date.second = d.getSeconds();
			date.millisecond = d.getMilliseconds();
		} else {
			if (map.YYYY !== void 0) date.year = Number.parseInt(match[map.YYYY], 10);
			else if (map.YY !== void 0) {
				const y = Number.parseInt(match[map.YY], 10);
				date.year = y < 0 ? y : 2e3 + y;
			}
			if (map.M !== void 0) {
				date.month = Number.parseInt(match[map.M], 10);
				if (date.month < 1 || date.month > 12) return date;
			} else if (map.MMM !== void 0) date.month = monthsShort.indexOf(match[map.MMM]) + 1;
			else if (map.MMMM !== void 0) date.month = months.indexOf(match[map.MMMM]) + 1;
			if (map.D !== void 0) {
				date.day = Number.parseInt(match[map.D], 10);
				if (date.year === null || date.month === null || date.day < 1) return date;
				const maxDay = calendar !== "persian" ? new Date(date.year, date.month, 0).getDate() : jalaaliMonthLength(date.year, date.month);
				if (date.day > maxDay) return date;
			}
			if (map.H !== void 0) date.hour = Number.parseInt(match[map.H], 10) % 24;
			else if (map.h !== void 0) {
				date.hour = Number.parseInt(match[map.h], 10) % 12;
				if (map.A && match[map.A] === "PM" || map.a && match[map.a] === "pm" || map.aa && match[map.aa] === "p.m.") date.hour += 12;
				date.hour = date.hour % 24;
			}
			if (map.m !== void 0) date.minute = Number.parseInt(match[map.m], 10) % 60;
			if (map.s !== void 0) date.second = Number.parseInt(match[map.s], 10) % 60;
			if (map.S !== void 0) date.millisecond = Number.parseInt(match[map.S], 10) * 10 ** (3 - match[map.S].length);
			if (map.Z !== void 0 || map.ZZ !== void 0) {
				tzString = map.Z !== void 0 ? match[map.Z].replace(":", "") : match[map.ZZ];
				date.timezoneOffset = (tzString[0] === "+" ? -1 : 1) * (60 * tzString.slice(1, 3) + Number(tzString.slice(3, 5)));
			}
		}
		date.dateHash = pad(date.year, 4) + "/" + pad(date.month) + "/" + pad(date.day);
		date.timeHash = pad(date.hour) + ":" + pad(date.minute) + ":" + pad(date.second) + tzString;
		return date;
	}
	function isValid(date) {
		return Number.isFinite(date) || Number.isFinite(Date.parse(date));
	}
	function buildDate(mod, utc) {
		return adjustDate(/* @__PURE__ */ new Date(), mod, utc);
	}
	function getDayOfWeek(date) {
		const dow = new Date(date).getDay();
		return dow === 0 ? 7 : dow;
	}
	function getWeekOfYear(date) {
		const thursday = new Date(date.getFullYear(), date.getMonth(), date.getDate());
		thursday.setDate(thursday.getDate() - (thursday.getDay() + 6) % 7 + 3);
		const firstThursday = new Date(thursday.getFullYear(), 0, 4);
		firstThursday.setDate(firstThursday.getDate() - (firstThursday.getDay() + 6) % 7 + 3);
		const ds = thursday.getTimezoneOffset() - firstThursday.getTimezoneOffset();
		thursday.setHours(thursday.getHours() - ds);
		const weekDiff = (thursday - firstThursday) / (MILLISECONDS_IN_DAY * 7);
		return 1 + Math.floor(weekDiff);
	}
	function getDayIdentifier(date) {
		return date.getFullYear() * 1e4 + date.getMonth() * 100 + date.getDate();
	}
	function getDateIdentifier(date, onlyDate) {
		const d = new Date(date);
		return onlyDate ? getDayIdentifier(d) : d.getTime();
	}
	function isBetweenDates(date, from, to, opts = {}) {
		const d1 = getDateIdentifier(from, opts.onlyDate), d2 = getDateIdentifier(to, opts.onlyDate), cur = getDateIdentifier(date, opts.onlyDate);
		return (cur > d1 || opts.inclusiveFrom && cur === d1) && (cur < d2 || opts.inclusiveTo && cur === d2);
	}
	function addToDate(date, mod) {
		return getChange(date, mod, 1);
	}
	function subtractFromDate(date, mod) {
		return getChange(date, mod, -1);
	}
	function startOfDate(date, unit, utc) {
		const t = new Date(date), prefix = `set${utc ? "UTC" : ""}`;
		switch (unit) {
			case "year":
			case "years": t[`${prefix}Month`](0);
			case "month":
			case "months": t[`${prefix}Date`](1);
			case "day":
			case "days":
			case "date": t[`${prefix}Hours`](0);
			case "hour":
			case "hours": t[`${prefix}Minutes`](0);
			case "minute":
			case "minutes": t[`${prefix}Seconds`](0);
			case "second":
			case "seconds": t[`${prefix}Milliseconds`](0);
		}
		return t;
	}
	function endOfDate(date, unit, utc) {
		const t = new Date(date), prefix = `set${utc ? "UTC" : ""}`;
		switch (unit) {
			case "year":
			case "years": t[`${prefix}Month`](11);
			case "month":
			case "months": t[`${prefix}Date`](daysInMonth(t));
			case "day":
			case "days":
			case "date": t[`${prefix}Hours`](23);
			case "hour":
			case "hours": t[`${prefix}Minutes`](59);
			case "minute":
			case "minutes": t[`${prefix}Seconds`](59);
			case "second":
			case "seconds": t[`${prefix}Milliseconds`](999);
		}
		return t;
	}
	function getMaxDate(date, ...args) {
		const maxTimestamp = Math.max(new Date(date).getTime(), ...args.map((d) => new Date(d).getTime()));
		return new Date(maxTimestamp);
	}
	function getMinDate(date, ...args) {
		const minTimestamp = Math.min(new Date(date).getTime(), ...args.map((d) => new Date(d).getTime()));
		return new Date(minTimestamp);
	}
	function getDiff(t, sub, interval) {
		return (t.getTime() - t.getTimezoneOffset() * MILLISECONDS_IN_MINUTE - (sub.getTime() - sub.getTimezoneOffset() * MILLISECONDS_IN_MINUTE)) / interval;
	}
	function getDateDiff(date, subtract, unit = "days") {
		const t = new Date(date), sub = new Date(subtract);
		switch (unit) {
			case "years":
			case "year": return t.getFullYear() - sub.getFullYear();
			case "months":
			case "month": return (t.getFullYear() - sub.getFullYear()) * 12 + t.getMonth() - sub.getMonth();
			case "days":
			case "day":
			case "date": return getDiff(startOfDate(t, "day"), startOfDate(sub, "day"), MILLISECONDS_IN_DAY);
			case "hours":
			case "hour": return getDiff(startOfDate(t, "hour"), startOfDate(sub, "hour"), MILLISECONDS_IN_HOUR);
			case "minutes":
			case "minute": return getDiff(startOfDate(t, "minute"), startOfDate(sub, "minute"), MILLISECONDS_IN_MINUTE);
			case "seconds":
			case "second": return getDiff(startOfDate(t, "second"), startOfDate(sub, "second"), 1e3);
		}
	}
	function getDayOfYear(date) {
		return getDateDiff(date, startOfDate(date, "year"), "days") + 1;
	}
	function inferDateFormat(date) {
		return isDate(date) ? "date" : typeof date === "number" ? "number" : "string";
	}
	function getDateBetween(date, min, max) {
		const t = new Date(date);
		if (min) {
			const low = new Date(min);
			if (t < low) return low;
		}
		if (max) {
			const high = new Date(max);
			if (t > high) return high;
		}
		return t;
	}
	function isSameDate(date, date2, unit) {
		const t = new Date(date), d = new Date(date2);
		if (unit === void 0) return t.getTime() === d.getTime();
		switch (unit) {
			case "second":
			case "seconds": if (t.getSeconds() !== d.getSeconds()) return false;
			case "minute":
			case "minutes": if (t.getMinutes() !== d.getMinutes()) return false;
			case "hour":
			case "hours": if (t.getHours() !== d.getHours()) return false;
			case "day":
			case "days":
			case "date": if (t.getDate() !== d.getDate()) return false;
			case "month":
			case "months": if (t.getMonth() !== d.getMonth()) return false;
			case "year":
			case "years":
				if (t.getFullYear() !== d.getFullYear()) return false;
				break;
			default: throw new Error(`date isSameDate unknown unit ${unit}`);
		}
		return true;
	}
	function daysInMonth(date) {
		return new Date(date.getFullYear(), date.getMonth() + 1, 0).getDate();
	}
	function getOrdinal(n) {
		if (n >= 11 && n <= 13) return `${n}th`;
		switch (n % 10) {
			case 1: return `${n}st`;
			case 2: return `${n}nd`;
			case 3: return `${n}rd`;
		}
		return `${n}th`;
	}
	const formatter = {
		YY(date, dateLocale, forcedYear) {
			const y = this.YYYY(date, dateLocale, forcedYear) % 100;
			return y >= 0 ? pad(y) : "-" + pad(Math.abs(y));
		},
		YYYY(date, _dateLocale, forcedYear) {
			return forcedYear !== void 0 && forcedYear !== null ? forcedYear : date.getFullYear();
		},
		M(date) {
			return date.getMonth() + 1;
		},
		Mo(date) {
			return getOrdinal(date.getMonth() + 1);
		},
		MM(date) {
			return pad(date.getMonth() + 1);
		},
		MMM(date, dateLocale) {
			return dateLocale.monthsShort[date.getMonth()];
		},
		MMMM(date, dateLocale) {
			return dateLocale.months[date.getMonth()];
		},
		Q(date) {
			return Math.ceil((date.getMonth() + 1) / 3);
		},
		Qo(date) {
			return getOrdinal(this.Q(date));
		},
		D(date) {
			return date.getDate();
		},
		Do(date) {
			return getOrdinal(date.getDate());
		},
		DD(date) {
			return pad(date.getDate());
		},
		DDD(date) {
			return getDayOfYear(date);
		},
		DDDo(date) {
			return getOrdinal(getDayOfYear(date));
		},
		DDDD(date) {
			return pad(getDayOfYear(date), 3);
		},
		d(date) {
			return date.getDay();
		},
		do(date) {
			return getOrdinal(date.getDay());
		},
		dd(date, dateLocale) {
			return dateLocale.days[date.getDay()].slice(0, 2);
		},
		ddd(date, dateLocale) {
			return dateLocale.daysShort[date.getDay()];
		},
		dddd(date, dateLocale) {
			return dateLocale.days[date.getDay()];
		},
		E(date) {
			return date.getDay() || 7;
		},
		w(date) {
			return getWeekOfYear(date);
		},
		wo(date) {
			return getOrdinal(getWeekOfYear(date));
		},
		ww(date) {
			return pad(getWeekOfYear(date));
		},
		H(date) {
			return date.getHours();
		},
		HH(date) {
			return pad(date.getHours());
		},
		h(date) {
			const hours = date.getHours();
			return hours === 0 ? 12 : hours > 12 ? hours % 12 : hours;
		},
		hh(date) {
			return pad(this.h(date));
		},
		m(date) {
			return date.getMinutes();
		},
		mm(date) {
			return pad(date.getMinutes());
		},
		s(date) {
			return date.getSeconds();
		},
		ss(date) {
			return pad(date.getSeconds());
		},
		S(date) {
			return Math.floor(date.getMilliseconds() / 100);
		},
		SS(date) {
			return pad(Math.floor(date.getMilliseconds() / 10));
		},
		SSS(date) {
			return pad(date.getMilliseconds(), 3);
		},
		A(date) {
			return date.getHours() < 12 ? "AM" : "PM";
		},
		a(date) {
			return date.getHours() < 12 ? "am" : "pm";
		},
		aa(date) {
			return date.getHours() < 12 ? "a.m." : "p.m.";
		},
		Z(date, _dateLocale, _forcedYear, forcedTimezoneOffset) {
			return formatTimezone(forcedTimezoneOffset === void 0 || forcedTimezoneOffset === null ? date.getTimezoneOffset() : forcedTimezoneOffset, ":");
		},
		ZZ(date, _dateLocale, _forcedYear, forcedTimezoneOffset) {
			return formatTimezone(forcedTimezoneOffset === void 0 || forcedTimezoneOffset === null ? date.getTimezoneOffset() : forcedTimezoneOffset);
		},
		X(date) {
			return Math.floor(date.getTime() / 1e3);
		},
		x(date) {
			return date.getTime();
		}
	};
	function formatDate(val, mask, dateLocale, __forcedYear, __forcedTimezoneOffset) {
		if (val !== 0 && !val || val === Infinity || val === -Infinity) return;
		const date = new Date(val);
		if (Number.isNaN(date)) return;
		if (mask === void 0) mask = defaultMask;
		const locale = getDateLocale(dateLocale, Plugin$8.props);
		return mask.replace(token, (match, text) => match in formatter ? formatter[match](date, locale, __forcedYear, __forcedTimezoneOffset) : text === void 0 ? match : text.split(String.raw`\]`).join("]"));
	}
	function clone(date) {
		return isDate(date) ? new Date(date) : date;
	}
	var date_default = {
		isValid,
		extractDate,
		buildDate,
		getDayOfWeek,
		getWeekOfYear,
		isBetweenDates,
		addToDate,
		subtractFromDate,
		adjustDate,
		startOfDate,
		endOfDate,
		getMaxDate,
		getMinDate,
		getDateDiff,
		getDayOfYear,
		inferDateFormat,
		getDateBetween,
		isSameDate,
		daysInMonth,
		formatDate,
		clone
	};
	//#endregion
	//#region src/components/date/QDate.js
	const yearsInterval = 20;
	const views = [
		"Calendar",
		"Years",
		"Months"
	];
	const viewIsValid = (v) => views.includes(v);
	const yearMonthRE = /^-?[\d]+\/[0-1]\d$/;
	const yearMonthValidator = (v) => yearMonthRE.test(v);
	const lineStr = " — ";
	function getMonthHash(date) {
		return date.year + "/" + pad(date.month);
	}
	function getShortDate(date) {
		return {
			year: date.year,
			month: date.month,
			day: date.day
		};
	}
	var QDate_default = createComponent({
		name: "QDate",
		props: {
			...useDatetimeProps,
			...useFormProps,
			...useDarkProps,
			modelValue: {
				required: true,
				validator: (val) => typeof val === "string" || Array.isArray(val) || Object(val) === val || val === null
			},
			multiple: Boolean,
			range: Boolean,
			title: String,
			subtitle: String,
			mask: {
				...useDatetimeProps.mask,
				default: "YYYY/MM/DD"
			},
			defaultYearMonth: {
				type: String,
				validator: yearMonthValidator
			},
			yearsInMonthView: Boolean,
			events: [Array, Function],
			eventColor: [String, Function],
			emitImmediately: Boolean,
			options: [Array, Function],
			navigationMinYearMonth: {
				type: String,
				validator: yearMonthValidator
			},
			navigationMaxYearMonth: {
				type: String,
				validator: yearMonthValidator
			},
			noUnset: Boolean,
			firstDayOfWeek: [String, Number],
			todayBtn: Boolean,
			minimal: Boolean,
			defaultView: {
				type: String,
				default: "Calendar",
				validator: viewIsValid
			}
		},
		emits: [
			...useDatetimeEmits,
			"rangeStart",
			"rangeEnd",
			"navigation"
		],
		setup(props, { slots, emit }) {
			const { proxy } = (0, vue.getCurrentInstance)();
			const { $q } = proxy;
			const isDark = useDark(props, $q);
			const { getCache } = useRenderCache();
			const { isHydrated } = useHydration();
			const { tabindex, headerClass, getLocale, getCurrentDate } = useDatetime(props, $q);
			let lastEmitValue;
			const injectFormInput = useFormInject(useFormAttrs(props));
			const blurTargetRef = (0, vue.ref)(null);
			const innerMask = (0, vue.ref)(getMask());
			const innerLocale = (0, vue.ref)(getLocale());
			const mask = (0, vue.computed)(() => getMask());
			const locale = (0, vue.computed)(() => getLocale());
			const today = (0, vue.computed)(() => getCurrentDate());
			const viewModel = (0, vue.ref)(getViewModel(innerMask.value, innerLocale.value));
			const view = (0, vue.ref)(props.defaultView);
			const direction = (0, vue.computed)(() => $q.lang.rtl ? "right" : "left");
			const monthDirection = (0, vue.ref)(direction.value);
			const yearDirection = (0, vue.ref)(direction.value);
			const localYear = viewModel.value.year;
			const startYear = (0, vue.ref)(localYear - localYear % yearsInterval - (localYear < 0 ? yearsInterval : 0));
			const editRange = (0, vue.ref)(null);
			const classes = (0, vue.computed)(() => {
				const type = props.landscape ? "landscape" : "portrait";
				return `q-date q-date--${type} q-date--${type}-${props.minimal ? "minimal" : "standard"}` + (isDark.value ? " q-date--dark q-dark" : "") + (props.bordered ? " q-date--bordered" : "") + (props.square ? " q-date--square no-border-radius" : "") + (props.flat ? " q-date--flat no-shadow" : "") + (props.disable ? " disabled" : props.readonly ? " q-date--readonly" : "");
			});
			const computedColor = (0, vue.computed)(() => props.color || "primary");
			const computedTextColor = (0, vue.computed)(() => props.textColor || "white");
			const isImmediate = (0, vue.computed)(() => props.emitImmediately && !props.multiple && !props.range);
			const normalizedModel = (0, vue.computed)(() => Array.isArray(props.modelValue) ? props.modelValue : props.modelValue !== null && props.modelValue !== void 0 ? [props.modelValue] : []);
			const daysModel = (0, vue.computed)(() => normalizedModel.value.filter((date) => typeof date === "string").map((date) => decodeString(date, innerMask.value, innerLocale.value)).filter((date) => date.dateHash !== null && date.day !== null && date.month !== null && date.year !== null));
			const rangeModel = (0, vue.computed)(() => {
				const fn = (date) => decodeString(date, innerMask.value, innerLocale.value);
				return normalizedModel.value.filter((date) => isObject(date) && date.from !== void 0 && date.to !== void 0).map((range) => ({
					from: fn(range.from),
					to: fn(range.to)
				})).filter((range) => range.from.dateHash !== null && range.to.dateHash !== null && range.from.dateHash < range.to.dateHash);
			});
			const getNativeDateFn = (0, vue.computed)(() => props.calendar !== "persian" ? (model) => new Date(model.year, model.month - 1, model.day) : (model) => {
				const gDate = toGregorian(model.year, model.month, model.day);
				return new Date(gDate.gy, gDate.gm - 1, gDate.gd);
			});
			const encodeObjectFn = (0, vue.computed)(() => props.calendar === "persian" ? getDayHash : (date, dateMask, dateLocale) => formatDate(new Date(date.year, date.month - 1, date.day, date.hour, date.minute, date.second, date.millisecond), dateMask === void 0 ? innerMask.value : dateMask, dateLocale === void 0 ? innerLocale.value : dateLocale, date.year, date.timezoneOffset));
			const daysInModel = (0, vue.computed)(() => daysModel.value.length + rangeModel.value.reduce((acc, range) => acc + 1 + getDateDiff(getNativeDateFn.value(range.to), getNativeDateFn.value(range.from)), 0));
			const headerTitle = (0, vue.computed)(() => {
				if (props.title !== void 0 && props.title !== null && props.title.length !== 0) return props.title;
				if (editRange.value !== null) {
					const model = editRange.value.init;
					const date = getNativeDateFn.value(model);
					return innerLocale.value.daysShort[date.getDay()] + ", " + innerLocale.value.monthsShort[model.month - 1] + " " + model.day + " — ?";
				}
				if (daysInModel.value === 0) return lineStr;
				if (daysInModel.value > 1) return `${daysInModel.value} ${innerLocale.value.pluralDay}`;
				const model = daysModel.value[0];
				const date = getNativeDateFn.value(model);
				if (Number.isNaN(date.valueOf())) return lineStr;
				if (innerLocale.value.headerTitle !== void 0) return innerLocale.value.headerTitle(date, model);
				return innerLocale.value.daysShort[date.getDay()] + ", " + innerLocale.value.monthsShort[model.month - 1] + " " + model.day;
			});
			const minSelectedModel = (0, vue.computed)(() => {
				return [...daysModel.value, ...rangeModel.value.map((range) => range.from)].sort((a, b) => a.year - b.year || a.month - b.month)[0];
			});
			const maxSelectedModel = (0, vue.computed)(() => {
				return [...daysModel.value, ...rangeModel.value.map((range) => range.to)].sort((a, b) => b.year - a.year || b.month - a.month)[0];
			});
			const headerSubtitle = (0, vue.computed)(() => {
				if (props.subtitle !== void 0 && props.subtitle !== null && props.subtitle.length !== 0) return props.subtitle;
				if (daysInModel.value === 0) return lineStr;
				if (daysInModel.value > 1) {
					const from = minSelectedModel.value;
					const to = maxSelectedModel.value;
					const month = innerLocale.value.monthsShort;
					return month[from.month - 1] + (from.year !== to.year ? " " + from.year + lineStr + month[to.month - 1] + " " : from.month !== to.month ? lineStr + month[to.month - 1] : "") + " " + to.year;
				}
				return daysModel.value[0].year;
			});
			const dateArrow = (0, vue.computed)(() => {
				const val = [$q.iconSet.datetime.arrowLeft, $q.iconSet.datetime.arrowRight];
				return $q.lang.rtl ? val.reverse() : val;
			});
			const computedFirstDayOfWeek = (0, vue.computed)(() => props.firstDayOfWeek !== void 0 ? Number(props.firstDayOfWeek) : innerLocale.value.firstDayOfWeek);
			const daysOfWeek = (0, vue.computed)(() => {
				const days = innerLocale.value.daysShort, first = computedFirstDayOfWeek.value;
				return first > 0 ? [...days.slice(first, 7), ...days.slice(0, first)] : days;
			});
			const daysInMonth = (0, vue.computed)(() => {
				const date = viewModel.value;
				return props.calendar !== "persian" ? new Date(date.year, date.month, 0).getDate() : jalaaliMonthLength(date.year, date.month);
			});
			const evtColor = (0, vue.computed)(() => typeof props.eventColor === "function" ? props.eventColor : () => props.eventColor);
			const minNav = (0, vue.computed)(() => {
				if (props.navigationMinYearMonth === void 0) return null;
				const data = props.navigationMinYearMonth.split("/");
				return {
					year: Number.parseInt(data[0], 10),
					month: Number.parseInt(data[1], 10)
				};
			});
			const maxNav = (0, vue.computed)(() => {
				if (props.navigationMaxYearMonth === void 0) return null;
				const data = props.navigationMaxYearMonth.split("/");
				return {
					year: Number.parseInt(data[0], 10),
					month: Number.parseInt(data[1], 10)
				};
			});
			const navBoundaries = (0, vue.computed)(() => {
				const data = {
					month: {
						prev: true,
						next: true
					},
					year: {
						prev: true,
						next: true
					}
				};
				if (minNav.value !== null && minNav.value.year >= viewModel.value.year) {
					data.year.prev = false;
					if (minNav.value.year === viewModel.value.year && minNav.value.month >= viewModel.value.month) data.month.prev = false;
				}
				if (maxNav.value !== null && maxNav.value.year <= viewModel.value.year) {
					data.year.next = false;
					if (maxNav.value.year === viewModel.value.year && maxNav.value.month <= viewModel.value.month) data.month.next = false;
				}
				return data;
			});
			const daysMap = (0, vue.computed)(() => {
				const map = {};
				daysModel.value.forEach((entry) => {
					const hash = getMonthHash(entry);
					if (map[hash] === void 0) map[hash] = [];
					map[hash].push(entry.day);
				});
				return map;
			});
			const rangeMap = (0, vue.computed)(() => {
				const map = {};
				rangeModel.value.forEach((entry) => {
					const hashFrom = getMonthHash(entry.from);
					const hashTo = getMonthHash(entry.to);
					if (map[hashFrom] === void 0) map[hashFrom] = [];
					map[hashFrom].push({
						from: entry.from.day,
						to: hashFrom === hashTo ? entry.to.day : void 0,
						range: entry
					});
					if (hashFrom < hashTo) {
						let hash;
						const { year, month } = entry.from;
						const cur = month < 12 ? {
							year,
							month: month + 1
						} : {
							year: year + 1,
							month: 1
						};
						while ((hash = getMonthHash(cur)) <= hashTo) {
							if (map[hash] === void 0) map[hash] = [];
							map[hash].push({
								from: void 0,
								to: hash === hashTo ? entry.to.day : void 0,
								range: entry
							});
							cur.month++;
							if (cur.month > 12) {
								cur.year++;
								cur.month = 1;
							}
						}
					}
				});
				return map;
			});
			const rangeView = (0, vue.computed)(() => {
				if (editRange.value === null) return;
				const { init, initHash, final, finalHash } = editRange.value;
				const [from, to] = initHash <= finalHash ? [init, final] : [final, init];
				const fromHash = getMonthHash(from);
				const toHash = getMonthHash(to);
				if (fromHash !== viewMonthHash.value && toHash !== viewMonthHash.value) return;
				const localView = {};
				if (fromHash === viewMonthHash.value) {
					localView.from = from.day;
					localView.includeFrom = true;
				} else localView.from = 1;
				if (toHash === viewMonthHash.value) {
					localView.to = to.day;
					localView.includeTo = true;
				} else localView.to = daysInMonth.value;
				return localView;
			});
			const viewMonthHash = (0, vue.computed)(() => getMonthHash(viewModel.value));
			const selectionDaysMap = (0, vue.computed)(() => {
				const map = {};
				if (props.options === void 0) {
					for (let i = 1; i <= daysInMonth.value; i++) map[i] = true;
					return map;
				}
				const fn = typeof props.options === "function" ? props.options : (date) => props.options.includes(date);
				for (let i = 1; i <= daysInMonth.value; i++) map[i] = fn(viewMonthHash.value + "/" + pad(i));
				return map;
			});
			const eventDaysMap = (0, vue.computed)(() => {
				const map = {};
				if (props.events === void 0) for (let i = 1; i <= daysInMonth.value; i++) map[i] = false;
				else {
					const fn = typeof props.events === "function" ? props.events : (date) => props.events.includes(date);
					for (let i = 1; i <= daysInMonth.value; i++) {
						const dayHash = viewMonthHash.value + "/" + pad(i);
						map[i] = fn(dayHash) && evtColor.value(dayHash);
					}
				}
				return map;
			});
			const viewDays = (0, vue.computed)(() => {
				let date, endDay;
				const { year, month } = viewModel.value;
				if (props.calendar !== "persian") {
					date = new Date(year, month - 1, 1);
					endDay = new Date(year, month - 1, 0).getDate();
				} else {
					const gDate = toGregorian(year, month, 1);
					date = new Date(gDate.gy, gDate.gm - 1, gDate.gd);
					let prevJM = month - 1;
					let prevJY = year;
					if (prevJM === 0) {
						prevJM = 12;
						prevJY--;
					}
					endDay = jalaaliMonthLength(prevJY, prevJM);
				}
				return {
					days: date.getDay() - computedFirstDayOfWeek.value - 1,
					endDay
				};
			});
			const days = (0, vue.computed)(() => {
				const res = [];
				const { days: localDays, endDay } = viewDays.value;
				const len = localDays < 0 ? localDays + 7 : localDays;
				if (len < 6) for (let i = endDay - len; i <= endDay; i++) res.push({
					i,
					fill: true
				});
				const index = res.length;
				for (let i = 1; i <= daysInMonth.value; i++) {
					const day = {
						i,
						event: eventDaysMap.value[i],
						classes: []
					};
					if (selectionDaysMap.value[i]) {
						day.in = true;
						day.flat = true;
					}
					res.push(day);
				}
				if (daysMap.value[viewMonthHash.value] !== void 0) daysMap.value[viewMonthHash.value].forEach((day) => {
					const i = index + day - 1;
					Object.assign(res[i], {
						selected: true,
						unelevated: true,
						flat: false,
						color: computedColor.value,
						textColor: computedTextColor.value
					});
				});
				if (rangeMap.value[viewMonthHash.value] !== void 0) rangeMap.value[viewMonthHash.value].forEach((entry) => {
					if (entry.from !== void 0) {
						const from = index + entry.from - 1;
						const to = index + (entry.to || daysInMonth.value) - 1;
						for (let day = from; day <= to; day++) Object.assign(res[day], {
							range: entry.range,
							unelevated: true,
							color: computedColor.value,
							textColor: computedTextColor.value
						});
						Object.assign(res[from], {
							rangeFrom: true,
							flat: false
						});
						if (entry.to !== void 0) Object.assign(res[to], {
							rangeTo: true,
							flat: false
						});
					} else if (entry.to !== void 0) {
						const to = index + entry.to - 1;
						for (let day = index; day <= to; day++) Object.assign(res[day], {
							range: entry.range,
							unelevated: true,
							color: computedColor.value,
							textColor: computedTextColor.value
						});
						Object.assign(res[to], {
							flat: false,
							rangeTo: true
						});
					} else {
						const to = index + daysInMonth.value - 1;
						for (let day = index; day <= to; day++) Object.assign(res[day], {
							range: entry.range,
							unelevated: true,
							color: computedColor.value,
							textColor: computedTextColor.value
						});
					}
				});
				if (rangeView.value !== void 0) {
					const from = index + rangeView.value.from - 1;
					const to = index + rangeView.value.to - 1;
					for (let day = from; day <= to; day++) {
						res[day].color = computedColor.value;
						res[day].editRange = true;
					}
					if (rangeView.value.includeFrom) res[from].editRangeFrom = true;
					if (rangeView.value.includeTo) res[to].editRangeTo = true;
				}
				if (isHydrated.value && viewModel.value.year === today.value.year && viewModel.value.month === today.value.month) res[index + today.value.day - 1].today = true;
				const left = res.length % 7;
				if (left > 0) {
					const afterDays = 7 - left;
					for (let i = 1; i <= afterDays; i++) res.push({
						i,
						fill: true
					});
				}
				res.forEach((day) => {
					let cls = "q-date__calendar-item ";
					if (day.fill) cls += "q-date__calendar-item--fill";
					else {
						cls += `q-date__calendar-item--${day.in ? "in" : "out"}`;
						if (day.range !== void 0) cls += ` q-date__range${day.rangeTo ? "-to" : day.rangeFrom ? "-from" : ""}`;
						if (day.editRange) cls += ` q-date__edit-range${day.editRangeFrom ? "-from" : ""}${day.editRangeTo ? "-to" : ""}`;
						if (day.range !== void 0 || day.editRange) cls += ` text-${day.color}`;
					}
					day.classes = cls;
				});
				return res;
			});
			const attributes = (0, vue.computed)(() => props.disable ? { "aria-disabled": "true" } : {});
			(0, vue.watch)(() => props.modelValue, (v) => {
				if (lastEmitValue === JSON.stringify(v)) lastEmitValue = 0;
				else {
					const model = getViewModel(innerMask.value, innerLocale.value);
					updateViewModel(model.year, model.month, model);
				}
			});
			(0, vue.watch)(view, () => {
				if (blurTargetRef.value !== null && proxy.$el.contains(document.activeElement)) blurTargetRef.value.focus();
			});
			(0, vue.watch)(() => viewModel.value.year + "|" + viewModel.value.month, () => {
				emit("navigation", {
					year: viewModel.value.year,
					month: viewModel.value.month
				});
			});
			(0, vue.watch)(mask, (val) => {
				updateValue(val, innerLocale.value, "mask");
				innerMask.value = val;
			});
			(0, vue.watch)(locale, (val) => {
				updateValue(innerMask.value, val, "locale");
				innerLocale.value = val;
			});
			function setLastValue(v) {
				lastEmitValue = JSON.stringify(v);
			}
			function setToday() {
				const { year, month, day } = today.value;
				const date = {
					...viewModel.value,
					year,
					month,
					day
				};
				const monthMap = daysMap.value[getMonthHash(date)];
				if (monthMap === void 0 || !monthMap.includes(date.day)) addToModel(date);
				setCalendarTo(date.year, date.month);
			}
			function setView(viewMode) {
				if (viewIsValid(viewMode)) view.value = viewMode;
			}
			function offsetCalendar(type, descending) {
				if (["month", "year"].includes(type)) (type === "month" ? goToMonth : goToYear)(descending ? -1 : 1);
			}
			function setCalendarTo(year, month) {
				view.value = "Calendar";
				updateViewModel(year, month);
			}
			function setEditingRange(from, to) {
				if (!props.range || !from) {
					editRange.value = null;
					return;
				}
				const init = {
					...viewModel.value,
					...from
				};
				const final = to !== void 0 ? {
					...viewModel.value,
					...to
				} : init;
				editRange.value = {
					init,
					initHash: getDayHash(init),
					final,
					finalHash: getDayHash(final)
				};
				setCalendarTo(init.year, init.month);
			}
			function getMask() {
				return props.calendar === "persian" ? "YYYY/MM/DD" : props.mask;
			}
			function decodeString(date, dateMask, dateLocale) {
				return __splitDate(date, dateMask, dateLocale, props.calendar, {
					hour: 0,
					minute: 0,
					second: 0,
					millisecond: 0
				});
			}
			function getViewModel(dateMask, dateLocale) {
				const model = Array.isArray(props.modelValue) ? props.modelValue : props.modelValue ? [props.modelValue] : [];
				if (model.length === 0) return getDefaultViewModel();
				const target = model.at(-1);
				const decoded = decodeString(target.from !== void 0 ? target.from : target, dateMask, dateLocale);
				return decoded.dateHash === null ? getDefaultViewModel() : decoded;
			}
			function getDefaultViewModel() {
				let year, month;
				if (props.defaultYearMonth !== void 0) {
					const d = props.defaultYearMonth.split("/");
					year = Number.parseInt(d[0], 10);
					month = Number.parseInt(d[1], 10);
				} else {
					const d = today.value !== void 0 ? today.value : getCurrentDate();
					year = d.year;
					month = d.month;
				}
				return {
					year,
					month,
					day: 1,
					hour: 0,
					minute: 0,
					second: 0,
					millisecond: 0,
					dateHash: year + "/" + pad(month) + "/01"
				};
			}
			function goToMonth(offset) {
				let year = viewModel.value.year;
				let month = Number(viewModel.value.month) + offset;
				if (month === 13) {
					month = 1;
					year++;
				} else if (month === 0) {
					month = 12;
					year--;
				}
				updateViewModel(year, month);
				if (isImmediate.value) emitImmediately("month");
			}
			function goToYear(offset) {
				updateViewModel(Number(viewModel.value.year) + offset, viewModel.value.month);
				if (isImmediate.value) emitImmediately("year");
			}
			function setYear(year) {
				updateViewModel(year, viewModel.value.month);
				view.value = props.defaultView === "Years" ? "Months" : "Calendar";
				if (isImmediate.value) emitImmediately("year");
			}
			function setMonth(month) {
				updateViewModel(viewModel.value.year, month);
				view.value = "Calendar";
				if (isImmediate.value) emitImmediately("month");
			}
			function toggleDate(date, monthHash) {
				(daysMap.value[monthHash]?.includes(date.day) === true ? removeFromModel : addToModel)(date);
			}
			function updateViewModel(year, month, time) {
				if (minNav.value !== null && year <= minNav.value.year) {
					if (month < minNav.value.month || year < minNav.value.year) month = minNav.value.month;
					year = minNav.value.year;
				}
				if (maxNav.value !== null && year >= maxNav.value.year) {
					if (month > maxNav.value.month || year > maxNav.value.year) month = maxNav.value.month;
					year = maxNav.value.year;
				}
				if (time !== void 0) {
					const { hour, minute, second, millisecond, timezoneOffset, timeHash } = time;
					Object.assign(viewModel.value, {
						hour,
						minute,
						second,
						millisecond,
						timezoneOffset,
						timeHash
					});
				}
				const newHash = year + "/" + pad(month) + "/01";
				if (newHash !== viewModel.value.dateHash) {
					monthDirection.value = viewModel.value.dateHash < newHash === ($q.lang.rtl !== true) ? "left" : "right";
					if (year !== viewModel.value.year) yearDirection.value = monthDirection.value;
					(0, vue.nextTick)(() => {
						startYear.value = year - year % yearsInterval - (year < 0 ? yearsInterval : 0);
						Object.assign(viewModel.value, {
							year,
							month,
							day: 1,
							dateHash: newHash
						});
					});
				}
			}
			function emitValue(val, action, date) {
				const value = val !== null && val.length === 1 && !props.multiple ? val[0] : val;
				const { reason, details } = getEmitParams(action, date);
				setLastValue(value);
				emit("update:modelValue", value, reason, details);
			}
			function emitImmediately(reason) {
				const date = daysModel.value[0] !== void 0 && daysModel.value[0].dateHash !== null ? { ...daysModel.value[0] } : { ...viewModel.value };
				(0, vue.nextTick)(() => {
					date.year = viewModel.value.year;
					date.month = viewModel.value.month;
					const maxDay = props.calendar !== "persian" ? new Date(date.year, date.month, 0).getDate() : jalaaliMonthLength(date.year, date.month);
					date.day = Math.min(Math.max(1, date.day), maxDay);
					const value = encodeEntry(date);
					const { details } = getEmitParams("", date);
					setLastValue(value);
					emit("update:modelValue", value, reason, details);
				});
			}
			function getEmitParams(action, date) {
				return date.from !== void 0 ? {
					reason: `${action}-range`,
					details: {
						...getShortDate(date.target),
						from: getShortDate(date.from),
						to: getShortDate(date.to)
					}
				} : {
					reason: `${action}-day`,
					details: getShortDate(date)
				};
			}
			function encodeEntry(date, dateMask, dateLocale) {
				return date.from !== void 0 ? {
					from: encodeObjectFn.value(date.from, dateMask, dateLocale),
					to: encodeObjectFn.value(date.to, dateMask, dateLocale)
				} : encodeObjectFn.value(date, dateMask, dateLocale);
			}
			function addToModel(date) {
				let value;
				if (props.multiple) if (date.from !== void 0) {
					const fromHash = getDayHash(date.from);
					const toHash = getDayHash(date.to);
					const localDays = daysModel.value.filter((day) => day.dateHash < fromHash || day.dateHash > toHash);
					const ranges = rangeModel.value.filter(({ from, to }) => to.dateHash < fromHash || from.dateHash > toHash);
					value = [
						...localDays,
						...ranges,
						date
					].map((entry) => encodeEntry(entry));
				} else value = [...normalizedModel.value, encodeEntry(date)];
				else value = encodeEntry(date);
				emitValue(value, "add", date);
			}
			function removeFromModel(date) {
				if (props.noUnset) return;
				let model = null;
				if (props.multiple && Array.isArray(props.modelValue)) {
					const val = encodeEntry(date);
					model = date.from !== void 0 ? props.modelValue.filter((item) => item.from !== void 0 ? item.from !== val.from && item.to !== val.to : true) : props.modelValue.filter((item) => item !== val);
					if (model.length === 0) model = null;
				}
				emitValue(model, "remove", date);
			}
			function updateValue(dateMask, dateLocale, reason) {
				const model = [...daysModel.value, ...rangeModel.value].map((entry) => encodeEntry(entry, dateMask, dateLocale)).filter((entry) => entry.from !== void 0 ? entry.from.dateHash !== null && entry.to.dateHash !== null : entry.dateHash !== null);
				const value = (props.multiple ? model : model[0]) || null;
				setLastValue(value);
				emit("update:modelValue", value, reason);
			}
			function getHeader() {
				if (props.minimal) return;
				return (0, vue.h)("div", { class: "q-date__header " + headerClass.value }, [(0, vue.h)("div", { class: "relative-position" }, [(0, vue.h)(vue.Transition, { name: "q-transition--fade" }, () => (0, vue.h)("div", {
					key: "h-yr-" + headerSubtitle.value,
					class: "q-date__header-subtitle q-date__header-link " + (view.value === "Years" ? "q-date__header-link--active" : "cursor-pointer"),
					tabindex: tabindex.value,
					...getCache("vY", {
						onClick() {
							view.value = "Years";
						},
						onKeyup(e) {
							if (e.keyCode === 13) view.value = "Years";
						}
					})
				}, [headerSubtitle.value]))]), (0, vue.h)("div", { class: "q-date__header-title relative-position flex no-wrap" }, [(0, vue.h)("div", { class: "relative-position col" }, [(0, vue.h)(vue.Transition, { name: "q-transition--fade" }, () => (0, vue.h)("div", {
					key: "h-sub" + headerTitle.value,
					class: "q-date__header-title-label q-date__header-link " + (view.value === "Calendar" ? "q-date__header-link--active" : "cursor-pointer"),
					tabindex: tabindex.value,
					...getCache("vC", {
						onClick() {
							view.value = "Calendar";
						},
						onKeyup(e) {
							if (e.keyCode === 13) view.value = "Calendar";
						}
					})
				}, [headerTitle.value]))]), props.todayBtn ? (0, vue.h)(QBtn_default, {
					class: "q-date__header-today self-start",
					icon: $q.iconSet.datetime.today,
					"aria-label": $q.lang.date.today,
					flat: true,
					size: "sm",
					round: true,
					tabindex: tabindex.value,
					onClick: setToday
				}) : null])]);
			}
			function getNavigation({ label, type, key, dir, goTo, boundaries, cls }) {
				return [
					(0, vue.h)("div", { class: "row items-center q-date__arrow" }, [(0, vue.h)(QBtn_default, {
						round: true,
						dense: true,
						size: "sm",
						flat: true,
						icon: dateArrow.value[0],
						"aria-label": type === "Years" ? $q.lang.date.prevYear : $q.lang.date.prevMonth,
						tabindex: tabindex.value,
						disable: !boundaries.prev,
						...getCache("go-#" + type, { onClick() {
							goTo(-1);
						} })
					})]),
					(0, vue.h)("div", { class: "relative-position overflow-hidden flex flex-center" + cls }, [(0, vue.h)(vue.Transition, { name: "q-transition--jump-" + dir }, () => (0, vue.h)("div", { key }, [(0, vue.h)(QBtn_default, {
						flat: true,
						dense: true,
						noCaps: true,
						label,
						tabindex: tabindex.value,
						...getCache("view#" + type, { onClick: () => {
							view.value = type;
						} })
					})]))]),
					(0, vue.h)("div", { class: "row items-center q-date__arrow" }, [(0, vue.h)(QBtn_default, {
						round: true,
						dense: true,
						size: "sm",
						flat: true,
						icon: dateArrow.value[1],
						"aria-label": type === "Years" ? $q.lang.date.nextYear : $q.lang.date.nextMonth,
						tabindex: tabindex.value,
						disable: !boundaries.next,
						...getCache("go+#" + type, { onClick() {
							goTo(1);
						} })
					})])
				];
			}
			const renderViews = {
				Calendar: () => [(0, vue.h)("div", {
					key: "calendar-view",
					class: "q-date__view q-date__calendar"
				}, [
					(0, vue.h)("div", { class: "q-date__navigation row items-center no-wrap" }, [...getNavigation({
						label: innerLocale.value.months[viewModel.value.month - 1],
						type: "Months",
						key: viewModel.value.month,
						dir: monthDirection.value,
						goTo: goToMonth,
						boundaries: navBoundaries.value.month,
						cls: " col"
					}), ...getNavigation({
						label: viewModel.value.year,
						type: "Years",
						key: viewModel.value.year,
						dir: yearDirection.value,
						goTo: goToYear,
						boundaries: navBoundaries.value.year,
						cls: ""
					})]),
					(0, vue.h)("div", { class: "q-date__calendar-weekdays row items-center no-wrap" }, daysOfWeek.value.map((day) => (0, vue.h)("div", { class: "q-date__calendar-item" }, [(0, vue.h)("div", day)]))),
					(0, vue.h)("div", { class: "q-date__calendar-days-container relative-position overflow-hidden" }, [(0, vue.h)(vue.Transition, { name: "q-transition--slide-" + monthDirection.value }, () => (0, vue.h)("div", {
						key: viewMonthHash.value,
						class: "q-date__calendar-days fit"
					}, days.value.map((day) => (0, vue.h)("div", { class: day.classes }, [day.in ? (0, vue.h)(QBtn_default, {
						class: day.today ? "q-date__today" : "",
						dense: true,
						flat: day.flat,
						unelevated: day.unelevated,
						color: day.color,
						textColor: day.textColor,
						label: day.i,
						tabindex: tabindex.value,
						...getCache("day#" + day.i, {
							onClick: () => {
								onDayClick(day.i);
							},
							onMouseover: () => {
								onDayMouseover(day.i);
							}
						})
					}, day.event ? () => (0, vue.h)("div", { class: "q-date__event bg-" + day.event }) : null) : (0, vue.h)("div", String(day.i))]))))])
				])],
				Months() {
					const currentYear = isHydrated.value && viewModel.value.year === today.value.year;
					const isDisabled = (month) => minNav.value !== null && viewModel.value.year === minNav.value.year && minNav.value.month > month || maxNav.value !== null && viewModel.value.year === maxNav.value.year && maxNav.value.month < month;
					const content = innerLocale.value.monthsShort.map((month, i) => {
						const active = viewModel.value.month === i + 1;
						return (0, vue.h)("div", { class: "q-date__months-item flex flex-center" }, [(0, vue.h)(QBtn_default, {
							class: currentYear && today.value.month === i + 1 ? "q-date__today" : null,
							flat: !active,
							label: month,
							unelevated: active,
							color: active ? computedColor.value : null,
							textColor: active ? computedTextColor.value : null,
							tabindex: tabindex.value,
							disable: isDisabled(i + 1),
							...getCache("month#" + i, { onClick: () => {
								setMonth(i + 1);
							} })
						})]);
					});
					if (props.yearsInMonthView) content.unshift((0, vue.h)("div", { class: "row no-wrap full-width" }, [getNavigation({
						label: viewModel.value.year,
						type: "Years",
						key: viewModel.value.year,
						dir: yearDirection.value,
						goTo: goToYear,
						boundaries: navBoundaries.value.year,
						cls: " col"
					})]));
					return (0, vue.h)("div", {
						key: "months-view",
						class: "q-date__view q-date__months flex flex-center"
					}, content);
				},
				Years() {
					const start = startYear.value, stop = start + yearsInterval, years = [];
					const isDisabled = (year) => minNav.value !== null && minNav.value.year > year || maxNav.value !== null && maxNav.value.year < year;
					for (let i = start; i <= stop; i++) {
						const active = viewModel.value.year === i;
						years.push((0, vue.h)("div", { class: "q-date__years-item flex flex-center" }, [(0, vue.h)(QBtn_default, {
							key: "yr" + i,
							class: isHydrated.value && today.value.year === i ? "q-date__today" : null,
							flat: !active,
							label: i,
							dense: true,
							unelevated: active,
							color: active ? computedColor.value : null,
							textColor: active ? computedTextColor.value : null,
							tabindex: tabindex.value,
							disable: isDisabled(i),
							...getCache("yr#" + i, { onClick: () => {
								setYear(i);
							} })
						})]));
					}
					return (0, vue.h)("div", { class: "q-date__view q-date__years flex flex-center" }, [
						(0, vue.h)("div", { class: "col-auto" }, [(0, vue.h)(QBtn_default, {
							round: true,
							dense: true,
							flat: true,
							icon: dateArrow.value[0],
							"aria-label": $q.lang.date.prevRangeYears(yearsInterval),
							tabindex: tabindex.value,
							disable: isDisabled(start),
							...getCache("y-", { onClick: () => {
								startYear.value -= yearsInterval;
							} })
						})]),
						(0, vue.h)("div", { class: "q-date__years-content col self-stretch row items-center" }, years),
						(0, vue.h)("div", { class: "col-auto" }, [(0, vue.h)(QBtn_default, {
							round: true,
							dense: true,
							flat: true,
							icon: dateArrow.value[1],
							"aria-label": $q.lang.date.nextRangeYears(yearsInterval),
							tabindex: tabindex.value,
							disable: isDisabled(stop),
							...getCache("y+", { onClick: () => {
								startYear.value += yearsInterval;
							} })
						})])
					]);
				}
			};
			function onDayClick(dayIndex) {
				const day = {
					...viewModel.value,
					day: dayIndex
				};
				if (!props.range) {
					toggleDate(day, viewMonthHash.value);
					return;
				}
				if (editRange.value === null) {
					const dayProps = days.value.find((item) => !item.fill && item.i === dayIndex);
					if (!props.noUnset && dayProps.range !== void 0) {
						removeFromModel({
							target: day,
							from: dayProps.range.from,
							to: dayProps.range.to
						});
						return;
					}
					if (dayProps.selected) {
						removeFromModel(day);
						return;
					}
					const initHash = getDayHash(day);
					editRange.value = {
						init: day,
						initHash,
						final: day,
						finalHash: initHash
					};
					emit("rangeStart", getShortDate(day));
				} else {
					const initHash = editRange.value.initHash, finalHash = getDayHash(day), payload = initHash <= finalHash ? {
						from: editRange.value.init,
						to: day
					} : {
						from: day,
						to: editRange.value.init
					};
					editRange.value = null;
					addToModel(initHash === finalHash ? day : {
						target: day,
						...payload
					});
					emit("rangeEnd", {
						from: getShortDate(payload.from),
						to: getShortDate(payload.to)
					});
				}
			}
			function onDayMouseover(dayIndex) {
				if (editRange.value !== null) {
					const final = {
						...viewModel.value,
						day: dayIndex
					};
					Object.assign(editRange.value, {
						final,
						finalHash: getDayHash(final)
					});
				}
			}
			Object.assign(proxy, {
				setToday,
				setView,
				offsetCalendar,
				setCalendarTo,
				setEditingRange
			});
			return () => {
				const content = [(0, vue.h)("div", { class: "q-date__content col relative-position" }, [(0, vue.h)(vue.Transition, { name: "q-transition--fade" }, renderViews[view.value])])];
				const def = hSlot(slots.default);
				if (def !== void 0) content.push((0, vue.h)("div", { class: "q-date__actions" }, def));
				if (props.name !== void 0 && !props.disable) injectFormInput(content, "push");
				return (0, vue.h)("div", {
					class: classes.value,
					...attributes.value
				}, [getHeader(), (0, vue.h)("div", {
					ref: blurTargetRef,
					class: "q-date__main col column",
					tabindex: -1
				}, content)]);
			};
		}
	});
	//#endregion
	//#region src/composables/private.use-history/use-history.js
	function useHistory(showing, hide, hideOnRouteChange) {
		let historyEntry;
		function removeFromHistory() {
			if (historyEntry !== void 0) {
				History_default.remove(historyEntry);
				historyEntry = void 0;
			}
		}
		(0, vue.onBeforeUnmount)(() => {
			if (showing.value) removeFromHistory();
		});
		return {
			removeFromHistory,
			addToHistory() {
				historyEntry = {
					condition: () => hideOnRouteChange.value,
					handler: hide
				};
				History_default.add(historyEntry);
			}
		};
	}
	//#endregion
	//#region src/utils/scroll/prevent-scroll.js
	let registered = 0;
	let scrollPositionX;
	let scrollPositionY;
	let maxScrollTop;
	let vpPendingUpdate = false;
	let bodyLeft;
	let bodyTop;
	let routePath;
	let closeTimer = null;
	function onAppleScroll(e) {
		if (e.target === document) document.scrollingElement.scrollTop = document.scrollingElement.scrollTop;
	}
	function onAppleResize(evt) {
		if (vpPendingUpdate) return;
		vpPendingUpdate = true;
		requestAnimationFrame(() => {
			vpPendingUpdate = false;
			const { height } = evt.target, { clientHeight, scrollTop } = document.scrollingElement;
			if (maxScrollTop === void 0 || height !== window.innerHeight) {
				maxScrollTop = clientHeight - height;
				document.scrollingElement.scrollTop = scrollTop;
			}
			if (scrollTop > maxScrollTop) document.scrollingElement.scrollTop -= Math.ceil((scrollTop - maxScrollTop) / 8);
		});
	}
	function apply$1(action) {
		const body = document.body, hasViewport = window.visualViewport !== void 0;
		if (action === "add") {
			const { overflowY, overflowX } = window.getComputedStyle(body);
			scrollPositionX = getHorizontalScrollPosition(window);
			scrollPositionY = getVerticalScrollPosition(window);
			bodyLeft = body.style.left;
			bodyTop = body.style.top;
			routePath = window.location.pathname;
			body.style.left = `-${scrollPositionX}px`;
			body.style.top = `-${scrollPositionY}px`;
			if (overflowX !== "hidden" && (overflowX === "scroll" || body.scrollWidth > window.innerWidth)) body.classList.add("q-body--force-scrollbar-x");
			if (overflowY !== "hidden" && (overflowY === "scroll" || body.scrollHeight > window.innerHeight)) body.classList.add("q-body--force-scrollbar-y");
			document.documentElement.classList.add("q-document--prevent-scroll");
			document.qScrollPrevented = true;
			if (client.is.ios) if (hasViewport) {
				window.scrollTo(0, 0);
				window.visualViewport.addEventListener("resize", onAppleResize, listenOpts.passiveCapture);
				window.visualViewport.addEventListener("scroll", onAppleResize, listenOpts.passiveCapture);
				window.scrollTo(0, 0);
			} else window.addEventListener("scroll", onAppleScroll, listenOpts.passiveCapture);
		} else {
			if (client.is.ios) if (hasViewport) {
				window.visualViewport.removeEventListener("resize", onAppleResize, listenOpts.passiveCapture);
				window.visualViewport.removeEventListener("scroll", onAppleResize, listenOpts.passiveCapture);
			} else window.removeEventListener("scroll", onAppleScroll, listenOpts.passiveCapture);
			document.documentElement.classList.remove("q-document--prevent-scroll");
			body.classList.remove("q-body--force-scrollbar-x", "q-body--force-scrollbar-y");
			document.qScrollPrevented = false;
			body.style.left = bodyLeft;
			body.style.top = bodyTop;
			if (window.location.pathname === routePath) window.scrollTo(scrollPositionX, scrollPositionY);
			maxScrollTop = void 0;
		}
	}
	function preventScroll(state) {
		let action = "add";
		if (state === true) {
			registered++;
			if (closeTimer !== null) {
				clearTimeout(closeTimer);
				closeTimer = null;
				return;
			}
			if (registered > 1) return;
		} else {
			if (registered === 0) return;
			registered--;
			if (registered > 0) return;
			action = "remove";
			if (client.is.ios && client.is.nativeMobile) {
				if (closeTimer !== null) clearTimeout(closeTimer);
				closeTimer = setTimeout(() => {
					apply$1(action);
					closeTimer = null;
				}, 100);
				return;
			}
		}
		apply$1(action);
	}
	//#endregion
	//#region src/composables/private.use-prevent-scroll/use-prevent-scroll.js
	function usePreventScroll() {
		let currentState;
		return { preventBodyScroll(state) {
			if (state !== currentState && (currentState !== void 0 || state)) {
				currentState = state;
				preventScroll(state);
			}
		} };
	}
	//#endregion
	//#region src/components/dialog/QDialog.js
	let maximizedModals = 0;
	const positionClass$1 = {
		standard: "fixed-full flex-center",
		top: "fixed-top justify-center",
		bottom: "fixed-bottom justify-center",
		right: "fixed-right items-center",
		left: "fixed-left items-center"
	};
	const defaultTransitions = {
		standard: ["scale", "scale"],
		top: ["slide-down", "slide-up"],
		bottom: ["slide-up", "slide-down"],
		right: ["slide-left", "slide-right"],
		left: ["slide-right", "slide-left"]
	};
	var QDialog_default = createComponent({
		name: "QDialog",
		inheritAttrs: false,
		props: {
			...useModelToggleProps,
			...useTransitionProps,
			transitionShow: String,
			transitionHide: String,
			persistent: Boolean,
			autoClose: Boolean,
			allowFocusOutside: Boolean,
			noEscDismiss: Boolean,
			noBackdropDismiss: Boolean,
			noRouteDismiss: Boolean,
			noRefocus: Boolean,
			noFocus: Boolean,
			noShake: Boolean,
			seamless: Boolean,
			maximized: Boolean,
			fullWidth: Boolean,
			fullHeight: Boolean,
			square: Boolean,
			backdropFilter: String,
			position: {
				type: String,
				default: "standard",
				validator: (val) => [
					"standard",
					"top",
					"bottom",
					"left",
					"right"
				].includes(val)
			}
		},
		emits: [
			...useModelToggleEmits,
			"shake",
			"click",
			"escapeKey"
		],
		setup(props, { slots, emit, attrs }) {
			const vm = (0, vue.getCurrentInstance)();
			const innerRef = (0, vue.ref)(null);
			const showing = (0, vue.ref)(false);
			const animating = (0, vue.ref)(false);
			let shakeTimeout = null, refocusTarget = null, isMaximized = false, avoidAutoClose = false;
			const hideOnRouteChange = (0, vue.computed)(() => !props.persistent && !props.noRouteDismiss && !props.seamless);
			const { preventBodyScroll } = usePreventScroll();
			const { registerTimeout } = useTimeout();
			const { registerTick, removeTick } = useTick();
			const { transitionProps, transitionStyle } = useTransition(props, () => defaultTransitions[props.position][0], () => defaultTransitions[props.position][1]);
			const backdropStyle = (0, vue.computed)(() => transitionStyle.value + (props.backdropFilter !== void 0 ? `;backdrop-filter:${props.backdropFilter};-webkit-backdrop-filter:${props.backdropFilter}` : ""));
			const { showPortal, hidePortal, portalIsAccessible, renderPortal } = usePortal(vm, innerRef, renderPortalContent, "dialog");
			const { hide } = useModelToggle({
				showing,
				hideOnRouteChange,
				handleShow,
				handleHide,
				handleRouteChange,
				processOnMount: true
			});
			const { addToHistory, removeFromHistory } = useHistory(showing, hide, hideOnRouteChange);
			const classes = (0, vue.computed)(() => `q-dialog__inner flex no-pointer-events q-dialog__inner--${props.maximized ? "maximized" : "minimized"} q-dialog__inner--${props.position} ${positionClass$1[props.position]}` + (animating.value ? " q-dialog__inner--animating" : "") + (props.fullWidth ? " q-dialog__inner--fullwidth" : "") + (props.fullHeight ? " q-dialog__inner--fullheight" : "") + (props.square ? " q-dialog__inner--square" : ""));
			const useBackdrop = (0, vue.computed)(() => showing.value && !props.seamless);
			const onEvents = (0, vue.computed)(() => props.autoClose ? { onClick: onAutoClose } : {});
			const rootClasses = (0, vue.computed)(() => [`q-dialog fullscreen no-pointer-events q-dialog--${useBackdrop.value ? "modal" : "seamless"}`, attrs.class]);
			(0, vue.watch)(() => props.maximized, (state) => {
				if (showing.value) updateMaximized(state);
			});
			(0, vue.watch)(useBackdrop, (val) => {
				preventBodyScroll(val);
				if (val) {
					addFocusout(onFocusChange);
					addEscapeKey(onEscapeKey);
				} else {
					removeFocusout(onFocusChange);
					removeEscapeKey(onEscapeKey);
				}
			});
			function handleShow(evt) {
				addToHistory();
				refocusTarget = !props.noRefocus && document.activeElement !== null ? document.activeElement : null;
				updateMaximized(props.maximized);
				showPortal();
				animating.value = true;
				if (props.noFocus) removeTick();
				else {
					document.activeElement?.blur();
					registerTick(focus);
				}
				registerTimeout(() => {
					if (vm.proxy.$q.platform.is.ios) {
						if (!props.seamless && document.activeElement) {
							const { top, bottom } = document.activeElement.getBoundingClientRect(), { innerHeight } = window, height = window.visualViewport !== void 0 ? window.visualViewport.height : innerHeight;
							if (top > 0 && bottom > height / 2) document.scrollingElement.scrollTop = Math.min(document.scrollingElement.scrollHeight - height, bottom >= innerHeight ? Infinity : Math.ceil(document.scrollingElement.scrollTop + bottom - height / 2));
							document.activeElement.scrollIntoView();
						}
						avoidAutoClose = true;
						innerRef.value.click();
						avoidAutoClose = false;
					}
					showPortal(true);
					animating.value = false;
					emit("show", evt);
				}, props.transitionDuration);
			}
			function handleHide(evt) {
				removeTick();
				removeFromHistory();
				cleanup(true);
				animating.value = true;
				hidePortal();
				if (refocusTarget !== null) {
					const target = (evt?.type.indexOf("key") === 0 ? refocusTarget.closest("[tabindex]:not([tabindex^=\"-\"])") : void 0) || refocusTarget;
					refocusTarget = null;
					addFocusFn(() => {
						if (target.isConnected) target.focus();
					});
				}
				registerTimeout(() => {
					hidePortal(true);
					animating.value = false;
					emit("hide", evt);
				}, props.transitionDuration);
			}
			function handleRouteChange() {
				refocusTarget = null;
			}
			function focus(selector) {
				addFocusFn(() => {
					let node = innerRef.value;
					if (node === null) return;
					if (selector !== void 0) {
						const target = node.querySelector(selector);
						if (target !== null) {
							target.focus({ preventScroll: true });
							return;
						}
					}
					if (!node.contains(document.activeElement)) {
						node = node.querySelector("[autofocus][tabindex], [data-autofocus][tabindex]") || node.querySelector("[autofocus] [tabindex], [data-autofocus] [tabindex]") || node.querySelector("[autofocus], [data-autofocus]") || node;
						node.focus({ preventScroll: true });
					}
				});
			}
			function shake(focusTarget) {
				if (focusTarget && typeof focusTarget.focus === "function") focusTarget.focus({ preventScroll: true });
				else focus();
				emit("shake");
				const node = innerRef.value;
				if (node !== null) {
					node.classList.remove("q-animate--scale");
					node.classList.add("q-animate--scale");
					if (shakeTimeout !== null) clearTimeout(shakeTimeout);
					shakeTimeout = setTimeout(() => {
						shakeTimeout = null;
						if (innerRef.value !== null) {
							node.classList.remove("q-animate--scale");
							focus();
						}
					}, 170);
				}
			}
			function onEscapeKey() {
				if (!props.seamless) if (props.persistent || props.noEscDismiss) {
					if (!props.maximized && !props.noShake) shake();
				} else {
					emit("escapeKey");
					hide();
				}
			}
			function cleanup(hiding) {
				if (shakeTimeout !== null) {
					clearTimeout(shakeTimeout);
					shakeTimeout = null;
				}
				if (hiding || showing.value) {
					updateMaximized(false);
					if (!props.seamless) {
						preventBodyScroll(false);
						removeFocusout(onFocusChange);
						removeEscapeKey(onEscapeKey);
					}
				}
				if (!hiding) refocusTarget = null;
			}
			function updateMaximized(active) {
				if (active) {
					if (!isMaximized) {
						if (maximizedModals < 1) document.body.classList.add("q-body--dialog");
						maximizedModals++;
						isMaximized = true;
					}
				} else if (isMaximized) {
					if (maximizedModals < 2) document.body.classList.remove("q-body--dialog");
					maximizedModals--;
					isMaximized = false;
				}
			}
			function onAutoClose(e) {
				if (!avoidAutoClose) {
					hide(e);
					emit("click", e);
				}
			}
			function onBackdropClick(e) {
				if (!props.persistent && !props.noBackdropDismiss) hide(e);
				else if (!props.noShake) shake();
			}
			function onFocusChange(evt) {
				if (!props.allowFocusOutside && portalIsAccessible.value && !childHasFocus(innerRef.value, evt.target)) focus("[tabindex]:not([tabindex=\"-1\"])");
			}
			Object.assign(vm.proxy, {
				focus,
				shake,
				__updateRefocusTarget(target) {
					refocusTarget = target || null;
				}
			});
			(0, vue.onBeforeUnmount)(cleanup);
			function renderPortalContent() {
				return (0, vue.h)("div", {
					role: "dialog",
					"aria-modal": useBackdrop.value ? "true" : "false",
					...attrs,
					class: rootClasses.value
				}, [(0, vue.h)(vue.Transition, {
					name: "q-transition--fade",
					appear: true
				}, () => useBackdrop.value ? (0, vue.h)("div", {
					class: "q-dialog__backdrop fixed-full",
					style: backdropStyle.value,
					"aria-hidden": "true",
					onClick: onBackdropClick
				}) : null), (0, vue.h)(vue.Transition, transitionProps.value, () => showing.value ? (0, vue.h)("div", {
					ref: innerRef,
					class: classes.value,
					style: transitionStyle.value,
					tabindex: -1,
					...onEvents.value
				}, hSlot(slots.default)) : null)]);
			}
			return renderPortal;
		}
	});
	//#endregion
	//#region src/components/drawer/QDrawer.js
	const duration = 150;
	function updateLocal$2(prop, val) {
		if (prop.value !== val) prop.value = val;
	}
	var QDrawer_default = createComponent({
		name: "QDrawer",
		inheritAttrs: false,
		props: {
			...useModelToggleProps,
			...useDarkProps,
			side: {
				type: String,
				default: "left",
				validator: (v) => ["left", "right"].includes(v)
			},
			width: {
				type: Number,
				default: 300
			},
			mini: Boolean,
			miniToOverlay: Boolean,
			miniWidth: {
				type: Number,
				default: 57
			},
			noMiniAnimation: Boolean,
			breakpoint: {
				type: Number,
				default: 1023
			},
			showIfAbove: Boolean,
			behavior: {
				type: String,
				validator: (v) => [
					"default",
					"desktop",
					"mobile"
				].includes(v),
				default: "default"
			},
			bordered: Boolean,
			elevated: Boolean,
			overlay: Boolean,
			persistent: Boolean,
			noSwipeOpen: Boolean,
			noSwipeClose: Boolean,
			noSwipeBackdrop: Boolean
		},
		emits: [
			...useModelToggleEmits,
			"onLayout",
			"miniState"
		],
		setup(props, { slots, emit, attrs }) {
			const vm = (0, vue.getCurrentInstance)();
			const { proxy: { $q } } = vm;
			const isDark = useDark(props, $q);
			const { preventBodyScroll } = usePreventScroll();
			const { registerTimeout, removeTimeout } = useTimeout();
			const $layout = (0, vue.inject)(layoutKey, emptyRenderFn);
			if ($layout === emptyRenderFn) {
				console.error("QDrawer needs to be child of QLayout");
				return emptyRenderFn;
			}
			let lastDesktopState, timerMini = null, layoutTotalWidthWatcher;
			const belowBreakpoint = (0, vue.ref)(props.behavior === "mobile" || props.behavior !== "desktop" && $layout.totalWidth.value <= props.breakpoint);
			const isMini = (0, vue.computed)(() => props.mini && !belowBreakpoint.value);
			const size = (0, vue.computed)(() => isMini.value ? props.miniWidth : props.width);
			const fixed = (0, vue.computed)(() => props.overlay || props.miniToOverlay || $layout.view.value.includes(rightSide.value ? "R" : "L") || $q.platform.is.ios && $layout.isContainer.value);
			const showing = (0, vue.ref)(props.showIfAbove && !belowBreakpoint.value || props.modelValue === true);
			const onLayout = (0, vue.computed)(() => !props.overlay && showing.value && !belowBreakpoint.value);
			const onScreenOverlay = (0, vue.computed)(() => props.overlay && showing.value && !belowBreakpoint.value);
			const hideOnRouteChange = (0, vue.computed)(() => !props.persistent && (belowBreakpoint.value || onScreenOverlay.value));
			function handleShow(evt, noEvent) {
				addToHistory();
				if (evt !== false) $layout.animate();
				applyPosition(0);
				if (belowBreakpoint.value) {
					const otherInstance = $layout.instances[otherSide.value];
					if (otherInstance?.belowBreakpoint === true) otherInstance.hide(false);
					applyBackdrop(1);
					if (!$layout.isContainer.value) preventBodyScroll(true);
				} else {
					applyBackdrop(0);
					if (evt !== false) setScrollable(false);
				}
				registerTimeout(() => {
					if (evt !== false) setScrollable(true);
					if (!noEvent) emit("show", evt);
				}, duration);
			}
			function handleHide(evt, noEvent) {
				removeFromHistory();
				if (evt !== false) $layout.animate();
				applyBackdrop(0);
				applyPosition(stateDirection.value * size.value);
				cleanup();
				if (!noEvent) registerTimeout(() => {
					emit("hide", evt);
				}, duration);
				else removeTimeout();
			}
			const { show, hide } = useModelToggle({
				showing,
				hideOnRouteChange,
				handleShow,
				handleHide
			});
			const { addToHistory, removeFromHistory } = useHistory(showing, hide, hideOnRouteChange);
			const instance = {
				belowBreakpoint,
				hide
			};
			const rightSide = (0, vue.computed)(() => props.side === "right");
			const stateDirection = (0, vue.computed)(() => ($q.lang.rtl ? -1 : 1) * (rightSide.value ? 1 : -1));
			const flagBackdropBg = (0, vue.ref)(0);
			const flagPanning = (0, vue.ref)(false);
			const flagMiniAnimate = (0, vue.ref)(false);
			const flagContentPosition = (0, vue.ref)(size.value * stateDirection.value);
			const otherSide = (0, vue.computed)(() => rightSide.value ? "left" : "right");
			const offset = (0, vue.computed)(() => showing.value && !belowBreakpoint.value && !props.overlay ? props.miniToOverlay ? props.miniWidth : size.value : 0);
			const backdropClass = (0, vue.computed)(() => "fullscreen q-drawer__backdrop" + (!showing.value && !flagPanning.value ? " hidden" : ""));
			const backdropStyle = (0, vue.computed)(() => ({ backgroundColor: `rgba(0,0,0,${flagBackdropBg.value * .4})` }));
			const headerSlot = (0, vue.computed)(() => rightSide.value ? $layout.rows.value.top[2] === "r" : $layout.rows.value.top[0] === "l");
			const footerSlot = (0, vue.computed)(() => rightSide.value ? $layout.rows.value.bottom[2] === "r" : $layout.rows.value.bottom[0] === "l");
			const aboveStyle = (0, vue.computed)(() => {
				const css = {};
				if ($layout.header.space && !headerSlot.value) {
					if (fixed.value) css.top = `${$layout.header.offset}px`;
					else if ($layout.header.space) css.top = `${$layout.header.size}px`;
				}
				if ($layout.footer.space && !footerSlot.value) {
					if (fixed.value) css.bottom = `${$layout.footer.offset}px`;
					else if ($layout.footer.space) css.bottom = `${$layout.footer.size}px`;
				}
				return css;
			});
			const style = (0, vue.computed)(() => {
				const acc = {
					width: `${size.value}px`,
					transform: `translateX(${flagContentPosition.value}px)`
				};
				return belowBreakpoint.value ? acc : Object.assign(acc, aboveStyle.value);
			});
			const contentClass = (0, vue.computed)(() => "q-drawer__content fit " + ($layout.isContainer.value ? "overflow-auto" : "scroll"));
			const classes = (0, vue.computed)(() => `q-drawer q-drawer--${props.side}` + (flagMiniAnimate.value ? " q-drawer--mini-animate" : "") + (props.bordered ? " q-drawer--bordered" : "") + (isDark.value ? " q-drawer--dark q-dark" : "") + (flagPanning.value ? " no-transition" : showing.value ? "" : " q-layout--prevent-focus") + (belowBreakpoint.value ? " fixed q-drawer--on-top q-drawer--mobile q-drawer--top-padding" : ` q-drawer--${isMini.value ? "mini" : "standard"}` + (fixed.value || !onLayout.value ? " fixed" : "") + (props.overlay || props.miniToOverlay ? " q-drawer--on-top" : "") + (headerSlot.value ? " q-drawer--top-padding" : "")));
			const openDirective = (0, vue.computed)(() => {
				return [[
					TouchPan_default,
					onOpenPan,
					void 0,
					{
						[$q.lang.rtl ? props.side : otherSide.value]: true,
						mouse: true
					}
				]];
			});
			const contentCloseDirective = (0, vue.computed)(() => {
				return [[
					TouchPan_default,
					onClosePan,
					void 0,
					{
						[$q.lang.rtl ? otherSide.value : props.side]: true,
						mouse: true
					}
				]];
			});
			const backdropCloseDirective = (0, vue.computed)(() => {
				return [[
					TouchPan_default,
					onClosePan,
					void 0,
					{
						[$q.lang.rtl ? otherSide.value : props.side]: true,
						mouse: true,
						mouseAllDir: true
					}
				]];
			});
			function updateBelowBreakpoint() {
				updateLocal$2(belowBreakpoint, props.behavior === "mobile" || props.behavior !== "desktop" && $layout.totalWidth.value <= props.breakpoint);
			}
			(0, vue.watch)(belowBreakpoint, (val) => {
				if (val) {
					lastDesktopState = showing.value;
					if (showing.value) hide(false);
				} else if (!props.overlay && props.behavior !== "mobile" && lastDesktopState !== false) if (showing.value) {
					applyPosition(0);
					applyBackdrop(0);
					cleanup();
				} else show(false);
			});
			(0, vue.watch)(() => props.side, (newSide, oldSide) => {
				if ($layout.instances[oldSide] === instance) {
					$layout.instances[oldSide] = void 0;
					$layout[oldSide].space = false;
					$layout[oldSide].offset = 0;
				}
				$layout.instances[newSide] = instance;
				$layout[newSide].size = size.value;
				$layout[newSide].space = onLayout.value;
				$layout[newSide].offset = offset.value;
			});
			(0, vue.watch)($layout.totalWidth, () => {
				if ($layout.isContainer.value || !document.qScrollPrevented) updateBelowBreakpoint();
			});
			(0, vue.watch)(() => props.behavior + props.breakpoint, updateBelowBreakpoint);
			(0, vue.watch)($layout.isContainer, (val) => {
				if (showing.value) preventBodyScroll(!val);
				if (val) updateBelowBreakpoint();
			});
			(0, vue.watch)($layout.scrollbarWidth, () => {
				applyPosition(showing.value ? 0 : void 0);
			});
			(0, vue.watch)(offset, (val) => {
				updateLayout("offset", val);
			});
			(0, vue.watch)(onLayout, (val) => {
				emit("onLayout", val);
				updateLayout("space", val);
			});
			(0, vue.watch)(rightSide, () => {
				applyPosition();
			});
			(0, vue.watch)(size, (val) => {
				applyPosition();
				updateSizeOnLayout(props.miniToOverlay, val);
			});
			(0, vue.watch)(() => props.miniToOverlay, (val) => {
				updateSizeOnLayout(val, size.value);
			});
			(0, vue.watch)(() => $q.lang.rtl, () => {
				applyPosition();
			});
			(0, vue.watch)(() => props.mini, () => {
				if (props.noMiniAnimation) return;
				if (props.modelValue) {
					animateMini();
					$layout.animate();
				}
			});
			(0, vue.watch)(isMini, (val) => {
				emit("miniState", val);
			});
			function applyPosition(position) {
				if (position === void 0) (0, vue.nextTick)(() => {
					position = showing.value ? 0 : size.value;
					applyPosition(stateDirection.value * position);
				});
				else {
					if ($layout.isContainer.value && rightSide.value && (belowBreakpoint.value || Math.abs(position) === size.value)) position += stateDirection.value * $layout.scrollbarWidth.value;
					flagContentPosition.value = position;
				}
			}
			function applyBackdrop(x) {
				flagBackdropBg.value = x;
			}
			function setScrollable(v) {
				const action = v ? "remove" : $layout.isContainer.value ? "" : "add";
				if (action !== "") document.body.classList[action]("q-body--drawer-toggle");
			}
			function animateMini() {
				if (timerMini !== null) clearTimeout(timerMini);
				if (vm.proxy && vm.proxy.$el) vm.proxy.$el.classList.add("q-drawer--mini-animate");
				flagMiniAnimate.value = true;
				timerMini = setTimeout(() => {
					timerMini = null;
					flagMiniAnimate.value = false;
					vm?.proxy?.$el?.classList.remove("q-drawer--mini-animate");
				}, 150);
			}
			function onOpenPan(evt) {
				if (showing.value) return;
				const width = size.value, position = between(evt.distance.x, 0, width);
				if (evt.isFinal) {
					if (position >= Math.min(75, width)) show();
					else {
						$layout.animate();
						applyBackdrop(0);
						applyPosition(stateDirection.value * width);
					}
					flagPanning.value = false;
					return;
				}
				applyPosition(($q.lang.rtl ? !rightSide.value : rightSide.value) ? Math.max(width - position, 0) : Math.min(0, position - width));
				applyBackdrop(between(position / width, 0, 1));
				if (evt.isFirst) flagPanning.value = true;
			}
			function onClosePan(evt) {
				if (!showing.value) return;
				const width = size.value, dir = evt.direction === props.side, position = ($q.lang.rtl ? !dir : dir) ? between(evt.distance.x, 0, width) : 0;
				if (evt.isFinal) {
					if (Math.abs(position) < Math.min(75, width)) {
						$layout.animate();
						applyBackdrop(1);
						applyPosition(0);
					} else hide();
					flagPanning.value = false;
					return;
				}
				applyPosition(stateDirection.value * position);
				applyBackdrop(between(1 - position / width, 0, 1));
				if (evt.isFirst) flagPanning.value = true;
			}
			function cleanup() {
				preventBodyScroll(false);
				setScrollable(true);
			}
			function updateLayout(prop, val) {
				$layout.update(props.side, prop, val);
			}
			function updateSizeOnLayout(miniToOverlay, newSize) {
				updateLayout("size", miniToOverlay ? props.miniWidth : newSize);
			}
			$layout.instances[props.side] = instance;
			updateSizeOnLayout(props.miniToOverlay, size.value);
			updateLayout("space", onLayout.value);
			updateLayout("offset", offset.value);
			if (props.showIfAbove && !props.modelValue && showing.value && props["onUpdate:modelValue"] !== void 0) emit("update:modelValue", true);
			(0, vue.onMounted)(() => {
				emit("onLayout", onLayout.value);
				emit("miniState", isMini.value);
				lastDesktopState = props.showIfAbove;
				const fn = () => {
					(showing.value ? handleShow : handleHide)(false, true);
				};
				if ($layout.totalWidth.value !== 0) {
					(0, vue.nextTick)(fn);
					return;
				}
				layoutTotalWidthWatcher = (0, vue.watch)($layout.totalWidth, () => {
					layoutTotalWidthWatcher();
					layoutTotalWidthWatcher = void 0;
					if (!showing.value && props.showIfAbove && !belowBreakpoint.value) show(false);
					else fn();
				});
			});
			(0, vue.onBeforeUnmount)(() => {
				layoutTotalWidthWatcher?.();
				if (timerMini !== null) {
					clearTimeout(timerMini);
					timerMini = null;
				}
				if (showing.value) cleanup();
				if ($layout.instances[props.side] === instance) {
					$layout.instances[props.side] = void 0;
					updateLayout("size", 0);
					updateLayout("offset", 0);
					updateLayout("space", false);
				}
			});
			return () => {
				const child = [];
				if (belowBreakpoint.value) {
					if (!props.noSwipeOpen) child.push((0, vue.withDirectives)((0, vue.h)("div", {
						key: "open",
						class: `q-drawer__opener fixed-${props.side}`,
						"aria-hidden": "true"
					}), openDirective.value));
					child.push(hDir("div", {
						ref: "backdrop",
						class: backdropClass.value,
						style: backdropStyle.value,
						"aria-hidden": "true",
						onClick: hide
					}, void 0, "backdrop", !props.noSwipeBackdrop && showing.value, () => backdropCloseDirective.value));
				}
				const mini = isMini.value && slots.mini !== void 0;
				const content = [(0, vue.h)("div", {
					...attrs,
					key: String(mini),
					class: [contentClass.value, attrs.class]
				}, mini ? slots.mini() : hSlot(slots.default))];
				if (props.elevated && showing.value) content.push((0, vue.h)("div", { class: "q-layout__shadow absolute-full overflow-hidden no-pointer-events" }));
				child.push(hDir("aside", {
					ref: "content",
					class: classes.value,
					style: style.value
				}, content, "contentclose", !props.noSwipeClose && belowBreakpoint.value, () => contentCloseDirective.value));
				return (0, vue.h)("div", { class: "q-drawer-container" }, child);
			};
		}
	});
	//#endregion
	//#region src/components/editor/editor-caret.js
	const tagList = [
		"div",
		"li",
		"ul",
		"ol",
		"blockquote"
	];
	function getBlockElement(el, parent) {
		if (parent && el === parent) return null;
		const nodeName = el.nodeName.toLowerCase();
		if (tagList.includes(nodeName)) return el;
		const display = (window.getComputedStyle ? window.getComputedStyle(el) : el.currentStyle).display;
		if (display === "block" || display === "table") return el;
		return getBlockElement(el.parentNode);
	}
	function isChildOf(el, parent, orSame) {
		return !el || el === document.body ? false : orSame && el === parent || (parent === document ? document.body : parent).contains(el.parentNode);
	}
	function createRange(node, chars, range) {
		if (!range) {
			range = document.createRange();
			range.selectNode(node);
			range.setStart(node, 0);
		}
		if (chars.count === 0) range.setEnd(node, chars.count);
		else if (chars.count > 0) if (node.nodeType === Node.TEXT_NODE) if (node.textContent.length < chars.count) chars.count -= node.textContent.length;
		else {
			range.setEnd(node, chars.count);
			chars.count = 0;
		}
		else for (let lp = 0; chars.count !== 0 && lp < node.childNodes.length; lp++) range = createRange(node.childNodes[lp], chars, range);
		return range;
	}
	const urlRegex = /^https?:\/\//;
	var Caret = class {
		constructor(el, eVm) {
			this.el = el;
			this.eVm = eVm;
			this._range = null;
		}
		get selection() {
			if (this.el) {
				const sel = document.getSelection();
				if (isChildOf(sel.anchorNode, this.el, true) && isChildOf(sel.focusNode, this.el, true)) return sel;
			}
			return null;
		}
		get hasSelection() {
			return this.selection !== null ? this.selection.toString().length !== 0 : false;
		}
		get range() {
			const sel = this.selection;
			if (sel?.rangeCount) return sel.getRangeAt(0);
			return this._range;
		}
		get parent() {
			const range = this.range;
			if (range !== null) {
				const node = range.startContainer;
				return node.nodeType === document.ELEMENT_NODE ? node : node.parentNode;
			}
			return null;
		}
		get blockParent() {
			const parent = this.parent;
			if (parent !== null) return getBlockElement(parent, this.el);
			return null;
		}
		save(range = this.range) {
			if (range !== null) this._range = range;
		}
		restore(range = this._range) {
			const r = document.createRange(), sel = document.getSelection();
			if (range !== null) {
				r.setStart(range.startContainer, range.startOffset);
				r.setEnd(range.endContainer, range.endOffset);
				sel.removeAllRanges();
				sel.addRange(r);
			} else {
				sel.selectAllChildren(this.el);
				sel.collapseToEnd();
			}
		}
		savePosition() {
			let charCount = -1, node;
			const selection = document.getSelection(), parentEl = this.el.parentNode;
			if (selection.focusNode && isChildOf(selection.focusNode, parentEl)) {
				node = selection.focusNode;
				charCount = selection.focusOffset;
				while (node && node !== parentEl) if (node !== this.el && node.previousSibling) {
					node = node.previousSibling;
					charCount += node.textContent.length;
				} else node = node.parentNode;
			}
			this.savedPos = charCount;
		}
		restorePosition(length = 0) {
			if (this.savedPos > 0 && this.savedPos < length) {
				const selection = window.getSelection(), range = createRange(this.el, { count: this.savedPos });
				if (range) {
					range.collapse(false);
					selection.removeAllRanges();
					selection.addRange(range);
				}
			}
		}
		hasParent(name, spanLevel) {
			const el = spanLevel ? this.parent : this.blockParent;
			return el !== null ? el.nodeName.toLowerCase() === name.toLowerCase() : false;
		}
		hasParents(list, recursive, el = this.parent) {
			if (el === null) return false;
			if (list.includes(el.nodeName.toLowerCase())) return true;
			return recursive ? this.hasParents(list, recursive, el.parentNode) : false;
		}
		is(cmd, param) {
			if (this.selection === null) return false;
			switch (cmd) {
				case "formatBlock": return param === "DIV" && this.parent === this.el || this.hasParent(param, param === "PRE");
				case "link": return this.hasParent("A", true);
				case "fontSize": return document.queryCommandValue(cmd) === param;
				case "fontName": {
					const res = document.queryCommandValue(cmd);
					return res === `"${param}"` || res === param;
				}
				case "fullscreen": return this.eVm.inFullscreen.value;
				case "viewsource": return this.eVm.isViewingSource.value;
				case void 0: return false;
				default: {
					const state = document.queryCommandState(cmd);
					return param !== void 0 ? state === param : state;
				}
			}
		}
		getParentAttribute(attrib) {
			if (this.parent !== null) return this.parent.getAttribute(attrib);
			return null;
		}
		can(name) {
			if (name === "outdent") return this.hasParents(["blockquote", "li"], true);
			if (name === "indent") return this.hasParents(["li"], true);
			if (name === "link") return this.selection !== null || this.is("link");
		}
		apply(cmd, param, done = noop) {
			if (cmd === "formatBlock") {
				if ([
					"BLOCKQUOTE",
					"H1",
					"H2",
					"H3",
					"H4",
					"H5",
					"H6"
				].includes(param) && this.is(cmd, param)) {
					cmd = "outdent";
					param = null;
				}
				if (param === "PRE" && this.is(cmd, "PRE")) param = "P";
			} else if (cmd === "print") {
				done();
				const win = window.open();
				win.document.write(`
        <!doctype html>
        <html>
          <head>
            <title>Print - ${document.title}</title>
          </head>
          <body>
            <div>${this.el.innerHTML}</div>
          </body>
        </html>
      `);
				win.print();
				win.close();
				return;
			} else if (cmd === "link") {
				const link = this.getParentAttribute("href");
				if (link === null) {
					const selection = this.selectWord(this.selection);
					const url = selection ? selection.toString() : "";
					if (url.length === 0 && (!this.range || !this.range.cloneContents().querySelector("img"))) return;
					this.eVm.editLinkUrl.value = urlRegex.test(url) ? url : "https://";
					this.save(selection.getRangeAt(0));
					document.execCommand("createLink", false, this.eVm.editLinkUrl.value);
				} else {
					this.eVm.editLinkUrl.value = link;
					this.range.selectNodeContents(this.parent);
					this.save();
				}
				return;
			} else if (cmd === "fullscreen") {
				this.eVm.toggleFullscreen();
				done();
				return;
			} else if (cmd === "viewsource") {
				this.eVm.isViewingSource.value = !this.eVm.isViewingSource.value;
				this.eVm.setContent(this.eVm.props.modelValue);
				done();
				return;
			}
			document.execCommand(cmd, false, param);
			done();
		}
		selectWord(sel) {
			if (sel === null || !sel.isCollapsed) return sel;
			const range = document.createRange();
			range.setStart(sel.anchorNode, sel.anchorOffset);
			range.setEnd(sel.focusNode, sel.focusOffset);
			const direction = range.collapsed ? ["backward", "forward"] : ["forward", "backward"];
			range.detach();
			const endNode = sel.focusNode, endOffset = sel.focusOffset;
			sel.collapse(sel.anchorNode, sel.anchorOffset);
			sel.modify("move", direction[0], "character");
			sel.modify("move", direction[1], "word");
			sel.extend(endNode, endOffset);
			sel.modify("extend", direction[1], "character");
			sel.modify("extend", direction[0], "word");
			return sel;
		}
	};
	//#endregion
	//#region src/components/tooltip/QTooltip.js
	let nonSelectableCount = 0;
	var QTooltip_default = createComponent({
		name: "QTooltip",
		inheritAttrs: false,
		props: {
			...useAnchorStaticProps,
			...useModelToggleProps,
			...useTransitionProps,
			maxHeight: {
				type: String,
				default: null
			},
			maxWidth: {
				type: String,
				default: null
			},
			transitionShow: {
				...useTransitionProps.transitionShow,
				default: "jump-down"
			},
			transitionHide: {
				...useTransitionProps.transitionHide,
				default: "jump-up"
			},
			anchor: {
				type: String,
				default: "bottom middle",
				validator: validatePosition
			},
			self: {
				type: String,
				default: "top middle",
				validator: validatePosition
			},
			offset: {
				type: Array,
				default: () => [14, 14],
				validator: validateOffset
			},
			scrollTarget: scrollTargetProp,
			delay: {
				type: Number,
				default: 0
			},
			hideDelay: {
				type: Number,
				default: 0
			},
			persistent: Boolean
		},
		emits: [...useModelToggleEmits],
		setup(props, { slots, emit, attrs }) {
			let unwatchPosition, observer, removeNonSelectableTimer, hasNonSelectable = false, describedBy;
			const vm = (0, vue.getCurrentInstance)();
			const { proxy: { $q } } = vm;
			const innerRef = (0, vue.ref)(null);
			const showing = (0, vue.ref)(false);
			const targetUid = useId();
			const tooltipId = (0, vue.computed)(() => attrs.id || targetUid.value);
			const anchorOrigin = (0, vue.computed)(() => parsePosition(props.anchor, $q.lang.rtl));
			const selfOrigin = (0, vue.computed)(() => parsePosition(props.self, $q.lang.rtl));
			const hideOnRouteChange = (0, vue.computed)(() => !props.persistent);
			const { registerTick, removeTick } = useTick();
			const { registerTimeout } = useTimeout();
			const { transitionProps, transitionStyle } = useTransition(props);
			const { localScrollTarget, changeScrollEvent, unconfigureScrollTarget } = useScrollTarget(props, configureScrollTarget);
			const { anchorEl, canShow, anchorEvents } = useAnchor({
				showing,
				configureAnchorEl
			});
			const { show, hide } = useModelToggle({
				showing,
				canShow,
				handleShow,
				handleHide,
				hideOnRouteChange,
				processOnMount: true
			});
			Object.assign(anchorEvents, {
				delayShow,
				delayHide,
				onFocusin
			});
			const { showPortal, hidePortal, renderPortal } = usePortal(vm, innerRef, renderPortalContent, "tooltip");
			if ($q.platform.is.mobile) {
				const clickOutsideProps = {
					anchorEl,
					innerRef,
					onClickOutside(e) {
						hide(e);
						if (e.target.classList.contains("q-dialog__backdrop")) stopAndPrevent(e);
						return true;
					}
				};
				(0, vue.watch)((0, vue.computed)(() => props.modelValue === null && !props.persistent && showing.value), (val) => {
					(val ? addClickOutside : removeClickOutside)(clickOutsideProps);
				});
				(0, vue.onBeforeUnmount)(() => {
					removeClickOutside(clickOutsideProps);
				});
			} else (0, vue.watch)(() => (props.modelValue === null || props["onUpdate:modelValue"]) && showing.value === true && props.persistent !== true, (val) => {
				(val === true ? addEscapeKey : removeEscapeKey)(onEscapeKey);
			});
			function handleShow(evt) {
				showPortal();
				addAriaDescription();
				registerTick(() => {
					observer?.disconnect();
					if (innerRef.value === null) {
						observer = void 0;
						return;
					}
					observer = new MutationObserver(() => updatePosition());
					observer.observe(innerRef.value, {
						attributes: false,
						childList: true,
						characterData: true,
						subtree: true
					});
					updatePosition();
					configureScrollTarget();
				});
				if (unwatchPosition === void 0) unwatchPosition = (0, vue.watch)(() => $q.screen.width + "|" + $q.screen.height + "|" + props.self + "|" + props.anchor + "|" + $q.lang.rtl, updatePosition);
				registerTimeout(() => {
					showPortal(true);
					emit("show", evt);
				}, props.transitionDuration);
			}
			function handleHide(evt) {
				removeTick();
				hidePortal();
				anchorCleanup();
				registerTimeout(() => {
					hidePortal(true);
					emit("hide", evt);
				}, props.transitionDuration);
			}
			function anchorCleanup() {
				if (observer !== void 0) {
					observer.disconnect();
					observer = void 0;
				}
				if (unwatchPosition !== void 0) {
					unwatchPosition();
					unwatchPosition = void 0;
				}
				unconfigureScrollTarget();
				removeEscapeKey(onEscapeKey);
				cleanEvt(anchorEvents, "tooltipTemp");
				removeAriaDescription();
				setNonSelectable(false);
			}
			function updatePosition() {
				setPosition({
					targetEl: innerRef.value,
					offset: props.offset,
					anchorEl: anchorEl.value,
					anchorOrigin: anchorOrigin.value,
					selfOrigin: selfOrigin.value,
					maxHeight: props.maxHeight,
					maxWidth: props.maxWidth
				});
			}
			function delayShow(evt) {
				if ($q.platform.is.mobile) {
					if (removeNonSelectableTimer !== void 0) {
						clearTimeout(removeNonSelectableTimer);
						removeNonSelectableTimer = void 0;
					}
					clearSelection();
					setNonSelectable(true);
					const target = anchorEl.value;
					const evts = [
						"touchmove",
						"touchcancel",
						"touchend",
						"click"
					].map((e) => [
						target,
						e,
						"delayHide",
						"passiveCapture"
					]);
					addEvt(anchorEvents, "tooltipTemp", evts);
				}
				registerTimeout(() => {
					show(evt);
				}, props.delay);
			}
			function delayHide(evt) {
				if ($q.platform.is.mobile) {
					cleanEvt(anchorEvents, "tooltipTemp");
					clearSelection();
					removeNonSelectableTimer = setTimeout(() => {
						removeNonSelectableTimer = void 0;
						setNonSelectable(false);
					}, 10);
				}
				registerTimeout(() => {
					hide(evt);
				}, props.hideDelay);
			}
			function onFocusin(evt) {
				const el = evt.target;
				if (!el) return;
				try {
					if (el.matches(":focus-visible") === false) return;
				} catch {}
				delayShow(evt);
			}
			function onEscapeKey(evt) {
				hide(evt);
			}
			function configureAnchorEl() {
				if (props.noParentEvent || anchorEl.value === null) return;
				const evts = $q.platform.is.mobile ? [[
					anchorEl.value,
					"touchstart",
					"delayShow",
					"passive"
				]] : [
					[
						anchorEl.value,
						"mouseenter",
						"delayShow",
						"passive"
					],
					[
						anchorEl.value,
						"mouseleave",
						"delayHide",
						"passive"
					],
					[
						anchorEl.value,
						"focusin",
						"onFocusin",
						"passive"
					],
					[
						anchorEl.value,
						"focusout",
						"delayHide",
						"passive"
					]
				];
				addEvt(anchorEvents, "anchor", evts);
			}
			function setNonSelectable(state) {
				if (hasNonSelectable === state) return;
				hasNonSelectable = state;
				nonSelectableCount += state ? 1 : -1;
				document.body.classList.toggle("non-selectable", nonSelectableCount > 0);
				if (!state && removeNonSelectableTimer !== void 0) {
					clearTimeout(removeNonSelectableTimer);
					removeNonSelectableTimer = void 0;
				}
			}
			function addAriaDescription() {
				const el = anchorEl.value, id = tooltipId.value;
				if (el === null || id === void 0) return;
				const ids = (el.getAttribute("aria-describedby") || "").split(/\s+/).filter(Boolean);
				describedBy = {
					el,
					id,
					added: !ids.includes(id)
				};
				if (describedBy.added) {
					ids.push(id);
					el.setAttribute("aria-describedby", ids.join(" "));
				}
			}
			function removeAriaDescription() {
				if (describedBy?.added === true) {
					const { el, id } = describedBy, value = (el.getAttribute("aria-describedby") || "").split(/\s+/).filter((entry) => entry !== "" && entry !== id);
					if (value.length === 0) el.removeAttribute("aria-describedby");
					else el.setAttribute("aria-describedby", value.join(" "));
				}
				describedBy = void 0;
			}
			function configureScrollTarget() {
				if (anchorEl.value !== null || props.scrollTarget !== void 0) {
					localScrollTarget.value = getScrollTarget(anchorEl.value, props.scrollTarget);
					const fn = props.noParentEvent ? updatePosition : hide;
					changeScrollEvent(localScrollTarget.value, fn);
				}
			}
			function getTooltipContent() {
				return showing.value ? (0, vue.h)("div", {
					...attrs,
					id: tooltipId.value,
					ref: innerRef,
					class: ["q-tooltip q-tooltip--style q-position-engine no-pointer-events", attrs.class],
					style: [attrs.style, transitionStyle.value],
					role: "tooltip"
				}, hSlot(slots.default)) : null;
			}
			function renderPortalContent() {
				return (0, vue.h)(vue.Transition, transitionProps.value, getTooltipContent);
			}
			(0, vue.onBeforeUnmount)(anchorCleanup);
			Object.assign(vm.proxy, { updatePosition });
			return renderPortal;
		}
	});
	//#endregion
	//#region src/components/item/QItem.js
	var QItem_default = createComponent({
		name: "QItem",
		props: {
			...useDarkProps,
			...useRouterLinkProps,
			tag: {
				type: String,
				default: "div"
			},
			active: {
				type: Boolean,
				default: null
			},
			clickable: Boolean,
			dense: Boolean,
			insetLevel: Number,
			tabindex: [String, Number],
			focused: Boolean,
			manualFocus: Boolean
		},
		emits: ["click", "keyup"],
		setup(props, { slots, emit }) {
			const { proxy: { $q } } = (0, vue.getCurrentInstance)();
			const isDark = useDark(props, $q);
			const { hasLink, linkAttrs, linkClass, linkTag, navigateOnClick } = useRouterLink();
			const rootRef = (0, vue.ref)(null);
			const blurTargetRef = (0, vue.ref)(null);
			const isActionable = (0, vue.computed)(() => props.clickable || hasLink.value || props.tag === "label");
			const isClickable = (0, vue.computed)(() => !props.disable && isActionable.value);
			const classes = (0, vue.computed)(() => "q-item q-item-type row no-wrap" + (props.dense ? " q-item--dense" : "") + (isDark.value ? " q-item--dark" : "") + (hasLink.value && props.active === null ? linkClass.value : props.active ? ` q-item--active${props.activeClass !== void 0 ? ` ${props.activeClass}` : ""}` : "") + (props.disable ? " disabled" : "") + (isClickable.value ? " q-item--clickable q-link cursor-pointer " + (props.manualFocus ? "q-manual-focusable" : "q-focusable q-hoverable") + (props.focused ? " q-manual-focusable--focused" : "") : ""));
			const style = (0, vue.computed)(() => {
				if (props.insetLevel === void 0) return null;
				return { ["padding" + ($q.lang.rtl ? "Right" : "Left")]: 16 + props.insetLevel * 56 + "px" };
			});
			function onClick(e) {
				if (isClickable.value) {
					if (blurTargetRef.value !== null && !e.qAvoidFocus) {
						if (!e.qKeyEvent && document.activeElement === rootRef.value) blurTargetRef.value.focus();
						else if (document.activeElement === blurTargetRef.value) rootRef.value.focus();
					}
					navigateOnClick(e);
				}
			}
			function onKeyup(e) {
				if (isClickable.value && isKeyCode(e, [13, 32])) {
					stopAndPrevent(e);
					e.qKeyEvent = true;
					const evt = new MouseEvent("click", e);
					evt.qKeyEvent = true;
					rootRef.value.dispatchEvent(evt);
				}
				emit("keyup", e);
			}
			function onKeydown(e) {
				if (isClickable.value && e.keyCode === 32) stopAndPrevent(e);
			}
			function getContent() {
				const child = hUniqueSlot(slots.default, []);
				if (isClickable.value) child.unshift((0, vue.h)("div", {
					class: "q-focus-helper",
					tabindex: -1,
					ref: blurTargetRef
				}));
				return child;
			}
			return () => {
				const data = {
					ref: rootRef,
					class: classes.value,
					style: style.value,
					role: hasLink.value ? void 0 : isClickable.value ? "button" : "listitem",
					onClick,
					onKeydown,
					onKeyup
				};
				if (isClickable.value) {
					data.tabindex = props.tabindex || "0";
					Object.assign(data, linkAttrs.value);
				} else if (isActionable.value) data["aria-disabled"] = "true";
				return (0, vue.h)(linkTag.value, data, getContent());
			};
		}
	});
	//#endregion
	//#region src/components/item/QItemSection.js
	var QItemSection_default = createComponent({
		name: "QItemSection",
		props: {
			avatar: Boolean,
			thumbnail: Boolean,
			side: Boolean,
			top: Boolean,
			noWrap: Boolean
		},
		setup(props, { slots }) {
			const classes = (0, vue.computed)(() => `q-item__section column q-item__section--${props.avatar || props.side || props.thumbnail ? "side" : "main"}` + (props.top ? " q-item__section--top justify-start" : " justify-center") + (props.avatar ? " q-item__section--avatar" : "") + (props.thumbnail ? " q-item__section--thumbnail" : "") + (props.noWrap ? " q-item__section--nowrap" : ""));
			return () => (0, vue.h)("div", { class: classes.value }, hSlot(slots.default));
		}
	});
	//#endregion
	//#region src/components/editor/editor-utils.js
	function run(e, btn, eVm) {
		if (btn.handler) btn.handler(e, eVm, eVm.caret);
		else eVm.runCmd(btn.cmd, btn.param);
	}
	function getGroup(children) {
		return (0, vue.h)("div", { class: "q-editor__toolbar-group" }, children);
	}
	function getBtn(eVm, btn, clickHandler, active = false) {
		const toggled = active || (btn.type === "toggle" ? btn.toggled ? btn.toggled(eVm) : btn.cmd && eVm.caret.is(btn.cmd, btn.param) : false), child = [];
		if (eVm.$q.platform.is.desktop && (btn.tip || btn.htmlTip)) {
			const Key = btn.key ? (0, vue.h)("div", [(0, vue.h)("small", `(CTRL + ${String.fromCodePoint(btn.key)})`)]) : null;
			child.push((0, vue.h)(QTooltip_default, { delay: 1e3 }, () => [(0, vue.h)("div", btn.htmlTip ? { innerHTML: btn.htmlTip } : btn.tip), Key]));
		}
		return (0, vue.h)(QBtn_default, {
			...eVm.buttonProps.value,
			icon: btn.icon !== null ? btn.icon : void 0,
			color: toggled ? btn.toggleColor || eVm.props.toolbarToggleColor : btn.color || eVm.props.toolbarColor,
			textColor: toggled && !eVm.props.toolbarPush ? null : btn.textColor || eVm.props.toolbarTextColor,
			label: btn.label,
			"aria-label": btn.label === null ? btn.tip : void 0,
			disable: btn.disable ? typeof btn.disable === "function" ? btn.disable(eVm) : true : false,
			size: "sm",
			onClick(e) {
				clickHandler?.();
				run(e, btn, eVm);
			}
		}, () => child);
	}
	function getDropdown(eVm, btn) {
		const onlyIcons = btn.list === "only-icons";
		let label = btn.label, icon = btn.icon !== null ? btn.icon : void 0, contentClass, Items;
		function closeDropdown() {
			Dropdown.component.proxy.hide();
		}
		if (onlyIcons) {
			Items = btn.options.map((localBtn) => {
				const active = localBtn.type === void 0 ? eVm.caret.is(localBtn.cmd, localBtn.param) : false;
				if (active) {
					label = localBtn.tip;
					icon = localBtn.icon !== null ? localBtn.icon : void 0;
				}
				return getBtn(eVm, localBtn, closeDropdown, active);
			});
			contentClass = eVm.toolbarBackgroundClass.value;
			Items = [getGroup(Items)];
		} else {
			const activeClass = eVm.props.toolbarToggleColor !== void 0 ? `text-${eVm.props.toolbarToggleColor}` : null;
			const inactiveClass = eVm.props.toolbarTextColor !== void 0 ? `text-${eVm.props.toolbarTextColor}` : null;
			const noIcons = btn.list === "no-icons";
			Items = btn.options.map((localBtn) => {
				const disable = localBtn.disable ? localBtn.disable(eVm) : false;
				const active = localBtn.type === void 0 ? eVm.caret.is(localBtn.cmd, localBtn.param) : false;
				if (active) {
					label = localBtn.tip;
					icon = localBtn.icon !== null ? localBtn.icon : void 0;
				}
				const htmlTip = localBtn.htmlTip;
				return (0, vue.h)(QItem_default, {
					active,
					activeClass,
					clickable: true,
					disable,
					dense: true,
					onClick(e) {
						closeDropdown();
						if (e?.qAvoidFocus !== true) eVm.contentRef.value?.focus();
						eVm.caret.restore();
						run(e, localBtn, eVm);
					}
				}, () => [noIcons ? null : (0, vue.h)(QItemSection_default, {
					class: active ? activeClass : inactiveClass,
					side: true
				}, () => (0, vue.h)(QIcon_default, { name: localBtn.icon !== null ? localBtn.icon : void 0 })), (0, vue.h)(QItemSection_default, htmlTip ? () => (0, vue.h)("div", {
					class: "text-no-wrap",
					innerHTML: localBtn.htmlTip
				}) : localBtn.tip ? () => (0, vue.h)("div", { class: "text-no-wrap" }, localBtn.tip) : void 0)]);
			});
			contentClass = [eVm.toolbarBackgroundClass.value, inactiveClass];
		}
		const highlight = btn.highlight && label !== btn.label;
		const Dropdown = (0, vue.h)(QBtnDropdown_default, {
			...eVm.buttonProps.value,
			noCaps: true,
			noWrap: true,
			color: highlight ? eVm.props.toolbarToggleColor : eVm.props.toolbarColor,
			textColor: highlight && !eVm.props.toolbarPush ? null : eVm.props.toolbarTextColor,
			label: btn.fixedLabel ? btn.label : label,
			icon: btn.fixedIcon ? btn.icon !== null ? btn.icon : void 0 : icon,
			contentClass,
			onShow: (evt) => eVm.emit("dropdownShow", evt),
			onHide: (evt) => eVm.emit("dropdownHide", evt),
			onBeforeShow: (evt) => eVm.emit("dropdownBeforeShow", evt),
			onBeforeHide: (evt) => eVm.emit("dropdownBeforeHide", evt)
		}, () => Items);
		return Dropdown;
	}
	function getToolbar(eVm) {
		if (eVm.caret) return eVm.buttons.value.filter((f) => !eVm.isViewingSource.value || f.find((fb) => fb.cmd === "viewsource")).map((group) => getGroup(group.map((btn) => {
			if (eVm.isViewingSource.value && btn.cmd !== "viewsource") return false;
			if (btn.type === "slot") return hSlot(eVm.slots[btn.slot]);
			if (btn.type === "dropdown") return getDropdown(eVm, btn);
			return getBtn(eVm, btn);
		})));
	}
	function getFonts(defaultFont, defaultFontLabel, defaultFontIcon, fonts = {}) {
		const aliases = Object.keys(fonts);
		if (aliases.length === 0) return {};
		const def = { default_font: {
			cmd: "fontName",
			param: defaultFont,
			icon: defaultFontIcon,
			tip: defaultFontLabel
		} };
		aliases.forEach((alias) => {
			const name = fonts[alias];
			def[alias] = {
				cmd: "fontName",
				param: name,
				icon: defaultFontIcon,
				tip: name,
				htmlTip: `<font face="${name}">${name}</font>`
			};
		});
		return def;
	}
	function getLinkEditor(eVm) {
		if (eVm.caret) {
			const color = eVm.props.toolbarColor || eVm.props.toolbarTextColor;
			let link = eVm.editLinkUrl.value;
			const updateLink = () => {
				eVm.caret.restore();
				if (link !== eVm.editLinkUrl.value) document.execCommand("createLink", false, link === "" ? " " : link);
				eVm.editLinkUrl.value = null;
			};
			return [
				(0, vue.h)("div", { class: `q-mx-xs text-${color}` }, `${eVm.$q.lang.editor.url}: `),
				(0, vue.h)("input", {
					key: "qedt_btm_input",
					class: "col q-editor__link-input",
					value: link,
					onInput: (evt) => {
						stop(evt);
						link = evt.target.value;
					},
					onKeydown: (evt) => {
						if (shouldIgnoreKey(evt)) return;
						switch (evt.keyCode) {
							case 13:
								prevent(evt);
								return updateLink();
							case 27:
								prevent(evt);
								eVm.caret.restore();
								if (!eVm.editLinkUrl.value || eVm.editLinkUrl.value === "https://") document.execCommand("unlink");
								eVm.editLinkUrl.value = null;
								break;
						}
					}
				}),
				getGroup([(0, vue.h)(QBtn_default, {
					key: "qedt_btm_rem",
					...eVm.buttonProps.value,
					label: eVm.$q.lang.label.remove,
					noCaps: true,
					onClick: () => {
						eVm.caret.restore();
						document.execCommand("unlink");
						eVm.editLinkUrl.value = null;
					}
				}), (0, vue.h)(QBtn_default, {
					key: "qedt_btm_upd",
					...eVm.buttonProps.value,
					label: eVm.$q.lang.label.update,
					noCaps: true,
					onClick: updateLink
				})])
			];
		}
	}
	//#endregion
	//#region src/composables/use-split-attrs/use-split-attrs.js
	const listenerRE = /^on[A-Z]/;
	function useSplitAttrs() {
		const { attrs, vnode } = (0, vue.getCurrentInstance)();
		const acc = {
			listeners: (0, vue.ref)({}),
			attributes: (0, vue.ref)({})
		};
		function update() {
			const attributes = {};
			const listeners = {};
			for (const key in attrs) if (key !== "class" && key !== "style" && !listenerRE.test(key)) attributes[key] = attrs[key];
			for (const key in vnode.props) if (listenerRE.test(key)) listeners[key] = vnode.props[key];
			acc.attributes.value = attributes;
			acc.listeners.value = listeners;
		}
		(0, vue.onBeforeUpdate)(update);
		update();
		return acc;
	}
	//#endregion
	//#region src/utils/extend/extend.js
	const toString = Object.prototype.toString;
	const hasOwn = Object.prototype.hasOwnProperty;
	const notPlainObject = new Set([
		"Boolean",
		"Number",
		"String",
		"Function",
		"Array",
		"Date",
		"RegExp"
	].map((name) => "[object " + name + "]"));
	function isPlainObject(obj) {
		if (obj !== Object(obj) || notPlainObject.has(toString.call(obj))) return false;
		if (obj.constructor && !hasOwn.call(obj, "constructor") && !hasOwn.call(obj.constructor.prototype, "isPrototypeOf")) return false;
		let key;
		for (key in obj);
		return key === void 0 || hasOwn.call(obj, key);
	}
	function extend(...args) {
		let options, name, src, copy, copyIsArray, clone, target = args[0] || {}, i = 1, deep = false;
		const length = args.length;
		if (typeof target === "boolean") {
			deep = target;
			target = args[1] || {};
			i = 2;
		}
		if (Object(target) !== target && typeof target !== "function") target = {};
		if (length === i) {
			target = this;
			i--;
		}
		for (; i < length; i++) if ((options = args[i]) !== null) for (name in options) {
			if (name === "__proto__") continue;
			src = target[name];
			copy = options[name];
			if (target === copy) continue;
			if (deep && copy && ((copyIsArray = Array.isArray(copy)) || isPlainObject(copy))) {
				if (copyIsArray) clone = Array.isArray(src) ? src : [];
				else clone = isPlainObject(src) ? src : {};
				target[name] = extend(deep, clone, copy);
			} else if (copy !== void 0) target[name] = copy;
		}
		return target;
	}
	//#endregion
	//#region src/components/editor/QEditor.js
	var QEditor_default = createComponent({
		name: "QEditor",
		props: {
			...useDarkProps,
			...useFullscreenProps,
			modelValue: {
				type: String,
				required: true
			},
			readonly: Boolean,
			disable: Boolean,
			minHeight: {
				type: String,
				default: "10rem"
			},
			maxHeight: String,
			height: String,
			definitions: Object,
			fonts: Object,
			placeholder: String,
			toolbar: {
				type: Array,
				validator: (v) => v.every((group) => group.length),
				default: () => [
					[
						"left",
						"center",
						"right",
						"justify"
					],
					[
						"bold",
						"italic",
						"underline",
						"strike"
					],
					["undo", "redo"]
				]
			},
			toolbarColor: String,
			toolbarBg: String,
			toolbarTextColor: String,
			toolbarToggleColor: {
				type: String,
				default: "primary"
			},
			toolbarOutline: Boolean,
			toolbarPush: Boolean,
			toolbarRounded: Boolean,
			paragraphTag: {
				type: String,
				validator: (v) => ["div", "p"].includes(v),
				default: "div"
			},
			contentStyle: Object,
			contentClass: [
				Object,
				Array,
				String
			],
			square: Boolean,
			flat: Boolean,
			dense: Boolean
		},
		emits: [
			...useFullscreenEmits,
			"update:modelValue",
			"keydown",
			"click",
			"focus",
			"blur",
			"dropdownShow",
			"dropdownHide",
			"dropdownBeforeShow",
			"dropdownBeforeHide",
			"linkShow",
			"linkHide"
		],
		setup(props, { slots, emit }) {
			const { proxy } = (0, vue.getCurrentInstance)();
			const { $q } = proxy;
			const isDark = useDark(props, $q);
			const { inFullscreen, toggleFullscreen } = useFullscreen();
			const splitAttrs = useSplitAttrs();
			const rootRef = (0, vue.ref)(null);
			const contentRef = (0, vue.ref)(null);
			const editLinkUrl = (0, vue.ref)(null);
			const isViewingSource = (0, vue.ref)(false);
			const editable = (0, vue.computed)(() => !props.readonly && !props.disable);
			let defaultFont, offsetBottom, refreshToolbarTimer = null;
			let lastEmit = props.modelValue;
			const renderInitialContent = isRuntimeSsrPreHydration.value;
			document.execCommand("defaultParagraphSeparator", false, props.paragraphTag);
			defaultFont = window.getComputedStyle(document.body).fontFamily;
			const toolbarBackgroundClass = (0, vue.computed)(() => props.toolbarBg ? ` bg-${props.toolbarBg}` : "");
			const buttonProps = (0, vue.computed)(() => {
				return {
					type: "a",
					flat: !props.toolbarOutline && !props.toolbarPush,
					noWrap: true,
					outline: props.toolbarOutline,
					push: props.toolbarPush,
					rounded: props.toolbarRounded,
					dense: true,
					color: props.toolbarColor,
					disable: !editable.value,
					size: "sm"
				};
			});
			const buttonDef = (0, vue.computed)(() => {
				const e = $q.lang.editor, i = $q.iconSet.editor;
				return {
					bold: {
						cmd: "bold",
						icon: i.bold,
						tip: e.bold,
						key: 66
					},
					italic: {
						cmd: "italic",
						icon: i.italic,
						tip: e.italic,
						key: 73
					},
					strike: {
						cmd: "strikeThrough",
						icon: i.strikethrough,
						tip: e.strikethrough,
						key: 83
					},
					underline: {
						cmd: "underline",
						icon: i.underline,
						tip: e.underline,
						key: 85
					},
					unordered: {
						cmd: "insertUnorderedList",
						icon: i.unorderedList,
						tip: e.unorderedList
					},
					ordered: {
						cmd: "insertOrderedList",
						icon: i.orderedList,
						tip: e.orderedList
					},
					subscript: {
						cmd: "subscript",
						icon: i.subscript,
						tip: e.subscript,
						htmlTip: "x<subscript>2</subscript>"
					},
					superscript: {
						cmd: "superscript",
						icon: i.superscript,
						tip: e.superscript,
						htmlTip: "x<superscript>2</superscript>"
					},
					link: {
						cmd: "link",
						disable: (eVm) => eVm.caret && !eVm.caret.can("link"),
						icon: i.hyperlink,
						tip: e.hyperlink,
						key: 76
					},
					fullscreen: {
						cmd: "fullscreen",
						icon: i.toggleFullscreen,
						tip: e.toggleFullscreen,
						key: 70
					},
					viewsource: {
						cmd: "viewsource",
						icon: i.viewSource,
						tip: e.viewSource
					},
					quote: {
						cmd: "formatBlock",
						param: "BLOCKQUOTE",
						icon: i.quote,
						tip: e.quote,
						key: 81
					},
					left: {
						cmd: "justifyLeft",
						icon: i.left,
						tip: e.left
					},
					center: {
						cmd: "justifyCenter",
						icon: i.center,
						tip: e.center
					},
					right: {
						cmd: "justifyRight",
						icon: i.right,
						tip: e.right
					},
					justify: {
						cmd: "justifyFull",
						icon: i.justify,
						tip: e.justify
					},
					print: {
						type: "no-state",
						cmd: "print",
						icon: i.print,
						tip: e.print,
						key: 80
					},
					outdent: {
						type: "no-state",
						disable: (eVm) => eVm.caret && !eVm.caret.can("outdent"),
						cmd: "outdent",
						icon: i.outdent,
						tip: e.outdent
					},
					indent: {
						type: "no-state",
						disable: (eVm) => eVm.caret && !eVm.caret.can("indent"),
						cmd: "indent",
						icon: i.indent,
						tip: e.indent
					},
					removeFormat: {
						type: "no-state",
						cmd: "removeFormat",
						icon: i.removeFormat,
						tip: e.removeFormat
					},
					hr: {
						type: "no-state",
						cmd: "insertHorizontalRule",
						icon: i.hr,
						tip: e.hr
					},
					undo: {
						type: "no-state",
						cmd: "undo",
						icon: i.undo,
						tip: e.undo,
						key: 90
					},
					redo: {
						type: "no-state",
						cmd: "redo",
						icon: i.redo,
						tip: e.redo,
						key: 89
					},
					h1: {
						cmd: "formatBlock",
						param: "H1",
						icon: i.heading1 || i.heading,
						tip: e.heading1,
						htmlTip: `<h1 class="q-ma-none">${e.heading1}</h1>`
					},
					h2: {
						cmd: "formatBlock",
						param: "H2",
						icon: i.heading2 || i.heading,
						tip: e.heading2,
						htmlTip: `<h2 class="q-ma-none">${e.heading2}</h2>`
					},
					h3: {
						cmd: "formatBlock",
						param: "H3",
						icon: i.heading3 || i.heading,
						tip: e.heading3,
						htmlTip: `<h3 class="q-ma-none">${e.heading3}</h3>`
					},
					h4: {
						cmd: "formatBlock",
						param: "H4",
						icon: i.heading4 || i.heading,
						tip: e.heading4,
						htmlTip: `<h4 class="q-ma-none">${e.heading4}</h4>`
					},
					h5: {
						cmd: "formatBlock",
						param: "H5",
						icon: i.heading5 || i.heading,
						tip: e.heading5,
						htmlTip: `<h5 class="q-ma-none">${e.heading5}</h5>`
					},
					h6: {
						cmd: "formatBlock",
						param: "H6",
						icon: i.heading6 || i.heading,
						tip: e.heading6,
						htmlTip: `<h6 class="q-ma-none">${e.heading6}</h6>`
					},
					p: {
						cmd: "formatBlock",
						param: props.paragraphTag,
						icon: i.heading,
						tip: e.paragraph
					},
					code: {
						cmd: "formatBlock",
						param: "PRE",
						icon: i.code,
						htmlTip: `<code>${e.code}</code>`
					},
					"size-1": {
						cmd: "fontSize",
						param: "1",
						icon: i.size1 || i.size,
						tip: e.size1,
						htmlTip: `<font size="1">${e.size1}</font>`
					},
					"size-2": {
						cmd: "fontSize",
						param: "2",
						icon: i.size2 || i.size,
						tip: e.size2,
						htmlTip: `<font size="2">${e.size2}</font>`
					},
					"size-3": {
						cmd: "fontSize",
						param: "3",
						icon: i.size3 || i.size,
						tip: e.size3,
						htmlTip: `<font size="3">${e.size3}</font>`
					},
					"size-4": {
						cmd: "fontSize",
						param: "4",
						icon: i.size4 || i.size,
						tip: e.size4,
						htmlTip: `<font size="4">${e.size4}</font>`
					},
					"size-5": {
						cmd: "fontSize",
						param: "5",
						icon: i.size5 || i.size,
						tip: e.size5,
						htmlTip: `<font size="5">${e.size5}</font>`
					},
					"size-6": {
						cmd: "fontSize",
						param: "6",
						icon: i.size6 || i.size,
						tip: e.size6,
						htmlTip: `<font size="6">${e.size6}</font>`
					},
					"size-7": {
						cmd: "fontSize",
						param: "7",
						icon: i.size7 || i.size,
						tip: e.size7,
						htmlTip: `<font size="7">${e.size7}</font>`
					}
				};
			});
			const buttons = (0, vue.computed)(() => {
				const userDef = props.definitions || {};
				const def = props.definitions || props.fonts ? extend(true, {}, buttonDef.value, userDef, getFonts(defaultFont, $q.lang.editor.defaultFont, $q.iconSet.editor.font, props.fonts)) : buttonDef.value;
				return props.toolbar.map((group) => group.map((token) => {
					if (token.options) return {
						type: "dropdown",
						icon: token.icon,
						label: token.label,
						size: "sm",
						dense: true,
						fixedLabel: token.fixedLabel,
						fixedIcon: token.fixedIcon,
						highlight: token.highlight,
						list: token.list,
						options: token.options.map((item) => def[item])
					};
					const obj = def[token];
					if (obj) return obj.type === "no-state" || userDef[token] && (obj.cmd === void 0 || buttonDef.value[obj.cmd] && buttonDef.value[obj.cmd].type === "no-state") ? obj : {
						type: "toggle",
						...obj
					};
					return {
						type: "slot",
						slot: token
					};
				}));
			});
			const eVm = {
				$q,
				props,
				slots,
				emit,
				inFullscreen,
				toggleFullscreen,
				runCmd,
				isViewingSource,
				editLinkUrl,
				toolbarBackgroundClass,
				buttonProps,
				contentRef,
				buttons,
				setContent
			};
			(0, vue.watch)(() => props.modelValue, (v) => {
				if (lastEmit !== v) {
					lastEmit = v;
					setContent(v, true);
				}
			});
			(0, vue.watch)(editLinkUrl, (v) => {
				emit(`link${v ? "Show" : "Hide"}`);
			});
			const hasToolbar = (0, vue.computed)(() => props.toolbar && props.toolbar.length !== 0);
			const keys = (0, vue.computed)(() => {
				const k = {}, add = (btn) => {
					if (btn.key) k[btn.key] = {
						cmd: btn.cmd,
						param: btn.param
					};
				};
				buttons.value.forEach((group) => {
					group.forEach((token) => {
						if (token.options) token.options.forEach(add);
						else add(token);
					});
				});
				return k;
			});
			const innerStyle = (0, vue.computed)(() => inFullscreen.value ? props.contentStyle : [{
				minHeight: props.minHeight,
				height: props.height,
				maxHeight: props.maxHeight
			}, props.contentStyle]);
			const classes = (0, vue.computed)(() => `q-editor q-editor--${isViewingSource.value ? "source" : "default"}` + (props.disable ? " disabled" : "") + (inFullscreen.value ? " fullscreen column" : "") + (props.square ? " q-editor--square no-border-radius" : "") + (props.flat ? " q-editor--flat" : "") + (props.dense ? " q-editor--dense" : "") + (isDark.value ? " q-editor--dark q-dark" : ""));
			const innerClass = (0, vue.computed)(() => [
				props.contentClass,
				"q-editor__content",
				{
					col: inFullscreen.value,
					"overflow-auto": inFullscreen.value || props.maxHeight
				}
			]);
			const attributes = (0, vue.computed)(() => props.disable ? { "aria-disabled": "true" } : {});
			function onInput() {
				if (contentRef.value !== null) {
					const prop = `inner${isViewingSource.value ? "Text" : "HTML"}`;
					const val = contentRef.value[prop];
					if (val !== props.modelValue) {
						lastEmit = val;
						emit("update:modelValue", val);
					}
				}
			}
			function onKeydown(e) {
				emit("keydown", e);
				if (!e.ctrlKey || shouldIgnoreKey(e)) {
					refreshToolbar();
					return;
				}
				const key = e.keyCode;
				const target = keys.value[key];
				if (target !== void 0) {
					const { cmd, param } = target;
					stopAndPrevent(e);
					runCmd(cmd, param, false);
				}
			}
			function onClick(e) {
				refreshToolbar();
				emit("click", e);
			}
			function onBlur(e) {
				if (contentRef.value !== null) {
					const { scrollTop, scrollHeight } = contentRef.value;
					offsetBottom = scrollHeight - scrollTop;
				}
				eVm.caret.save();
				emit("blur", e);
			}
			function onFocus(e) {
				(0, vue.nextTick)(() => {
					if (contentRef.value !== null && offsetBottom !== void 0) contentRef.value.scrollTop = contentRef.value.scrollHeight - offsetBottom;
				});
				emit("focus", e);
			}
			function onFocusin(e) {
				const root = rootRef.value;
				if (root !== null && root.contains(e.target) && (e.relatedTarget === null || !root.contains(e.relatedTarget))) {
					const prop = `inner${isViewingSource.value ? "Text" : "HTML"}`;
					eVm.caret.restorePosition(contentRef.value[prop].length);
					refreshToolbar();
				}
			}
			function onFocusout(e) {
				const root = rootRef.value;
				if (root !== null && root.contains(e.target) && (e.relatedTarget === null || !root.contains(e.relatedTarget))) {
					eVm.caret.savePosition();
					refreshToolbar();
				}
			}
			function onPointerStart() {
				offsetBottom = void 0;
			}
			function onSelectionchange() {
				eVm.caret.save();
			}
			function setContent(v, restorePosition) {
				if (contentRef.value !== null) {
					if (restorePosition) eVm.caret.savePosition();
					const prop = `inner${isViewingSource.value ? "Text" : "HTML"}`;
					contentRef.value[prop] = v;
					if (restorePosition) {
						eVm.caret.restorePosition(contentRef.value[prop].length);
						refreshToolbar();
					}
				}
			}
			function runCmd(cmd, param, update = true) {
				focus();
				eVm.caret.restore();
				eVm.caret.apply(cmd, param, () => {
					focus();
					eVm.caret.save();
					if (update) refreshToolbar();
				});
			}
			function refreshToolbar() {
				if (refreshToolbarTimer !== null) clearTimeout(refreshToolbarTimer);
				refreshToolbarTimer = setTimeout(() => {
					refreshToolbarTimer = null;
					editLinkUrl.value = null;
					proxy.$forceUpdate();
				}, 1);
			}
			function focus() {
				addFocusFn(() => {
					contentRef.value?.focus({ preventScroll: true });
				});
			}
			function getContentEl() {
				return contentRef.value;
			}
			(0, vue.onMounted)(() => {
				eVm.caret = proxy.caret = new Caret(contentRef.value, eVm);
				setContent(props.modelValue);
				refreshToolbar();
				document.addEventListener("selectionchange", onSelectionchange);
			});
			(0, vue.onBeforeUnmount)(() => {
				if (refreshToolbarTimer !== null) clearTimeout(refreshToolbarTimer);
				document.removeEventListener("selectionchange", onSelectionchange);
			});
			Object.assign(proxy, {
				runCmd,
				refreshToolbar,
				focus,
				getContentEl
			});
			return () => {
				let toolbars;
				if (hasToolbar.value) {
					const bars = [(0, vue.h)("div", {
						key: "qedt_top",
						class: "q-editor__toolbar row no-wrap scroll-x" + toolbarBackgroundClass.value
					}, getToolbar(eVm))];
					if (editLinkUrl.value !== null) bars.push((0, vue.h)("div", {
						key: "qedt_btm",
						class: "q-editor__toolbar row no-wrap items-center scroll-x" + toolbarBackgroundClass.value
					}, getLinkEditor(eVm)));
					toolbars = (0, vue.h)("div", {
						key: "toolbar_ctainer",
						class: "q-editor__toolbars-container"
					}, bars);
				}
				return (0, vue.h)("div", {
					ref: rootRef,
					class: classes.value,
					style: { height: inFullscreen.value ? "100%" : null },
					...attributes.value,
					onFocusin,
					onFocusout
				}, [toolbars, (0, vue.h)("div", {
					ref: contentRef,
					style: innerStyle.value,
					class: innerClass.value,
					contenteditable: editable.value,
					placeholder: props.placeholder,
					...renderInitialContent ? { innerHTML: props.modelValue } : {},
					...splitAttrs.listeners.value,
					onInput,
					onKeydown,
					onClick,
					onBlur,
					onFocus,
					onMousedown: onPointerStart,
					onTouchstartPassive: onPointerStart
				})]);
			};
		}
	});
	//#endregion
	//#region src/components/item/QItemLabel.js
	var QItemLabel_default = createComponent({
		name: "QItemLabel",
		props: {
			overline: Boolean,
			caption: Boolean,
			header: Boolean,
			lines: [Number, String]
		},
		setup(props, { slots }) {
			const parsedLines = (0, vue.computed)(() => Number.parseInt(props.lines, 10));
			const classes = (0, vue.computed)(() => "q-item__label" + (props.overline ? " q-item__label--overline text-overline" : "") + (props.caption ? " q-item__label--caption text-caption" : "") + (props.header ? " q-item__label--header" : "") + (parsedLines.value === 1 ? " ellipsis" : ""));
			const style = (0, vue.computed)(() => props.lines !== void 0 && parsedLines.value > 1 ? {
				overflow: "hidden",
				display: "-webkit-box",
				"-webkit-box-orient": "vertical",
				"-webkit-line-clamp": parsedLines.value
			} : null);
			return () => (0, vue.h)("div", {
				style: style.value,
				class: classes.value
			}, hSlot(slots.default));
		}
	});
	//#endregion
	//#region src/components/slide-transition/QSlideTransition.js
	var QSlideTransition_default = createComponent({
		name: "QSlideTransition",
		props: {
			appear: Boolean,
			duration: {
				type: Number,
				default: 300
			}
		},
		emits: ["show", "hide"],
		setup(props, { slots, emit }) {
			let animating = false, doneFn, element;
			let timer = null, timerFallback = null, animListener, lastEvent;
			function cleanup() {
				doneFn?.();
				doneFn = null;
				animating = false;
				if (timer !== null) {
					clearTimeout(timer);
					timer = null;
				}
				if (timerFallback !== null) {
					clearTimeout(timerFallback);
					timerFallback = null;
				}
				element?.removeEventListener("transitionend", animListener);
				animListener = null;
			}
			function begin(el, height, done) {
				if (height !== void 0) el.style.height = `${height}px`;
				el.style.transition = `height ${props.duration}ms cubic-bezier(.25, .8, .50, 1)`;
				animating = true;
				doneFn = done;
			}
			function end(el, event) {
				el.style.overflowY = null;
				el.style.height = null;
				el.style.transition = null;
				cleanup();
				if (event !== lastEvent) emit(event);
			}
			function onEnter(el, done) {
				let pos = 0;
				element = el;
				if (animating) {
					cleanup();
					pos = el.offsetHeight === el.scrollHeight ? 0 : void 0;
				} else {
					lastEvent = "hide";
					el.style.overflowY = "hidden";
				}
				begin(el, pos, done);
				timer = setTimeout(() => {
					timer = null;
					el.style.height = `${el.scrollHeight}px`;
					animListener = (evt) => {
						timerFallback = null;
						if (Object(evt) !== evt || evt.target === el) end(el, "show");
					};
					el.addEventListener("transitionend", animListener);
					timerFallback = setTimeout(animListener, props.duration * 1.1);
				}, 100);
			}
			function onLeave(el, done) {
				let pos;
				element = el;
				if (animating) cleanup();
				else {
					lastEvent = "show";
					el.style.overflowY = "hidden";
					pos = el.scrollHeight;
				}
				begin(el, pos, done);
				timer = setTimeout(() => {
					timer = null;
					el.style.height = 0;
					animListener = (evt) => {
						timerFallback = null;
						if (Object(evt) !== evt || evt.target === el) end(el, "hide");
					};
					el.addEventListener("transitionend", animListener);
					timerFallback = setTimeout(animListener, props.duration * 1.1);
				}, 100);
			}
			(0, vue.onBeforeUnmount)(() => {
				if (animating) cleanup();
			});
			return () => (0, vue.h)(vue.Transition, {
				css: false,
				appear: props.appear,
				onEnter,
				onLeave
			}, slots.default);
		}
	});
	//#endregion
	//#region src/components/separator/QSeparator.js
	const insetMap = {
		true: "inset",
		item: "item-inset",
		"item-thumbnail": "item-thumbnail-inset"
	};
	const margins = {
		xs: 2,
		sm: 4,
		md: 8,
		lg: 16,
		xl: 24
	};
	var QSeparator_default = createComponent({
		name: "QSeparator",
		props: {
			...useDarkProps,
			spaced: [Boolean, String],
			inset: [Boolean, String],
			vertical: Boolean,
			color: String,
			size: String
		},
		setup(props) {
			const isDark = useDark(props, (0, vue.getCurrentInstance)().proxy.$q);
			const orientation = (0, vue.computed)(() => props.vertical ? "vertical" : "horizontal");
			const orientClass = (0, vue.computed)(() => ` q-separator--${orientation.value}`);
			const insetClass = (0, vue.computed)(() => props.inset ? `${orientClass.value}-${insetMap[props.inset]}` : "");
			const classes = (0, vue.computed)(() => `q-separator${orientClass.value}${insetClass.value}` + (props.color !== void 0 ? ` bg-${props.color}` : "") + (isDark.value ? " q-separator--dark" : ""));
			const style = (0, vue.computed)(() => {
				const acc = {};
				if (props.size !== void 0) acc[props.vertical ? "width" : "height"] = props.size;
				if (props.spaced) {
					const size = props.spaced === true ? `${margins.md}px` : props.spaced in margins ? `${margins[props.spaced]}px` : props.spaced;
					const dir = props.vertical ? ["Left", "Right"] : ["Top", "Bottom"];
					acc[`margin${dir[0]}`] = acc[`margin${dir[1]}`] = size;
				}
				return acc;
			});
			return () => (0, vue.h)("hr", {
				class: classes.value,
				style: style.value,
				"aria-orientation": orientation.value
			});
		}
	});
	//#endregion
	//#region src/components/expansion-item/QExpansionItem.js
	const itemGroups = (0, vue.shallowReactive)({});
	function preventSpace$2(e) {
		if (e.keyCode === 32) stopAndPrevent(e);
	}
	const LINK_PROPS = Object.keys(useRouterLinkProps);
	var QExpansionItem_default = createComponent({
		name: "QExpansionItem",
		props: {
			...useRouterLinkProps,
			...useModelToggleProps,
			...useDarkProps,
			icon: String,
			label: String,
			labelLines: [Number, String],
			caption: String,
			captionLines: [Number, String],
			dense: Boolean,
			toggleAriaLabel: String,
			expandIcon: String,
			expandedIcon: String,
			expandIconClass: [
				Array,
				String,
				Object
			],
			duration: {},
			headerInsetLevel: Number,
			contentInsetLevel: Number,
			expandSeparator: Boolean,
			defaultOpened: Boolean,
			hideExpandIcon: Boolean,
			expandIconToggle: Boolean,
			switchToggleSide: Boolean,
			denseToggle: Boolean,
			group: String,
			popup: Boolean,
			headerStyle: [
				Array,
				String,
				Object
			],
			headerClass: [
				Array,
				String,
				Object
			]
		},
		emits: [
			...useModelToggleEmits,
			"click",
			"afterShow",
			"afterHide"
		],
		setup(props, { slots, emit }) {
			const { proxy: { $q } } = (0, vue.getCurrentInstance)();
			const isDark = useDark(props, $q);
			const showing = (0, vue.ref)(props.modelValue !== null ? props.modelValue : props.defaultOpened);
			const blurTargetRef = (0, vue.ref)(null);
			const targetUid = useId();
			const { show, hide, toggle } = useModelToggle({ showing });
			let uniqueId, exitGroup;
			const classes = (0, vue.computed)(() => `q-expansion-item q-item-type q-expansion-item--${showing.value ? "expanded" : "collapsed"} q-expansion-item--${props.popup ? "popup" : "standard"}`);
			const contentStyle = (0, vue.computed)(() => {
				if (props.contentInsetLevel === void 0) return null;
				return { ["padding" + ($q.lang.rtl ? "Right" : "Left")]: props.contentInsetLevel * 56 + "px" };
			});
			const hasLink = (0, vue.computed)(() => !props.disable && (props.href !== void 0 || props.to !== void 0 && props.to !== null && props.to !== ""));
			const linkProps = (0, vue.computed)(() => {
				const acc = {};
				LINK_PROPS.forEach((key) => {
					acc[key] = props[key];
				});
				return acc;
			});
			const isClickable = (0, vue.computed)(() => hasLink.value || !props.expandIconToggle);
			const expansionIcon = (0, vue.computed)(() => props.expandedIcon !== void 0 && showing.value ? props.expandedIcon : props.expandIcon || $q.iconSet.expansionItem[props.denseToggle ? "denseIcon" : "icon"]);
			const activeToggleIcon = (0, vue.computed)(() => !props.disable && (hasLink.value || props.expandIconToggle));
			const headerSlotScope = (0, vue.computed)(() => ({
				expanded: showing.value,
				detailsId: targetUid.value,
				toggle,
				show,
				hide
			}));
			const toggleAriaAttrs = (0, vue.computed)(() => {
				const toggleAriaLabel = props.toggleAriaLabel !== void 0 ? props.toggleAriaLabel : $q.lang.label[showing.value ? "collapse" : "expand"](props.label);
				return {
					role: "button",
					"aria-expanded": showing.value ? "true" : "false",
					"aria-controls": targetUid.value,
					"aria-label": toggleAriaLabel
				};
			});
			(0, vue.watch)(() => props.group, (name) => {
				exitGroup?.();
				if (name !== void 0) enterGroup();
			});
			function onHeaderClick(e) {
				if (!hasLink.value) toggle(e);
				emit("click", e);
			}
			function toggleIconKeyboard(e) {
				if ([13, 32].includes(e.keyCode)) toggleIcon(e, true);
			}
			function toggleIcon(e, keyboard) {
				if (!keyboard && !e.qAvoidFocus) blurTargetRef.value?.focus();
				toggle(e);
				stopAndPrevent(e);
			}
			function onShow() {
				emit("afterShow");
			}
			function onHide() {
				emit("afterHide");
			}
			function enterGroup() {
				if (uniqueId === void 0) uniqueId = uid_default();
				if (showing.value) itemGroups[props.group] = uniqueId;
				const stopShowWatcher = (0, vue.watch)(showing, (val) => {
					if (val) itemGroups[props.group] = uniqueId;
					else if (itemGroups[props.group] === uniqueId) delete itemGroups[props.group];
				});
				const stopGroupWatcher = (0, vue.watch)(() => itemGroups[props.group], (val, oldVal) => {
					if (oldVal === uniqueId && val !== void 0 && val !== uniqueId) hide();
				});
				exitGroup = () => {
					stopShowWatcher();
					stopGroupWatcher();
					if (itemGroups[props.group] === uniqueId) delete itemGroups[props.group];
					exitGroup = void 0;
				};
			}
			function getToggleIcon() {
				const data = {
					class: [`q-focusable relative-position cursor-pointer${props.denseToggle && props.switchToggleSide ? " items-end" : ""}`, props.expandIconClass],
					side: !props.switchToggleSide,
					avatar: props.switchToggleSide
				};
				const child = [(0, vue.h)(QIcon_default, {
					class: "q-expansion-item__toggle-icon" + (props.expandedIcon === void 0 && showing.value ? " q-expansion-item__toggle-icon--rotated" : ""),
					name: expansionIcon.value
				})];
				if (activeToggleIcon.value) {
					Object.assign(data, {
						tabindex: 0,
						...toggleAriaAttrs.value,
						onClick: toggleIcon,
						onKeydown: preventSpace$2,
						onKeyup: toggleIconKeyboard
					});
					child.unshift((0, vue.h)("div", {
						ref: blurTargetRef,
						class: "q-expansion-item__toggle-focus q-icon q-focus-helper q-focus-helper--rounded",
						tabindex: -1
					}));
				}
				return (0, vue.h)(QItemSection_default, data, () => child);
			}
			function getHeaderChild() {
				let child;
				if (slots.header !== void 0) child = [slots.header(headerSlotScope.value)].flat();
				else {
					child = [(0, vue.h)(QItemSection_default, () => [(0, vue.h)(QItemLabel_default, { lines: props.labelLines }, () => props.label || ""), props.caption ? (0, vue.h)(QItemLabel_default, {
						lines: props.captionLines,
						caption: true
					}, () => props.caption) : null])];
					if (props.icon) child[props.switchToggleSide ? "push" : "unshift"]((0, vue.h)(QItemSection_default, {
						side: props.switchToggleSide,
						avatar: !props.switchToggleSide
					}, () => (0, vue.h)(QIcon_default, { name: props.icon })));
				}
				if (!props.disable && !props.hideExpandIcon) child[props.switchToggleSide ? "unshift" : "push"](getToggleIcon());
				return child;
			}
			function getHeader() {
				const data = {
					ref: "item",
					style: props.headerStyle,
					class: props.headerClass,
					dark: isDark.value,
					disable: props.disable,
					dense: props.dense,
					insetLevel: props.headerInsetLevel
				};
				if (isClickable.value) {
					data.clickable = true;
					data.onClick = onHeaderClick;
					Object.assign(data, hasLink.value ? linkProps.value : toggleAriaAttrs.value);
				}
				return (0, vue.h)(QItem_default, data, getHeaderChild);
			}
			function getTransitionChild() {
				return (0, vue.withDirectives)((0, vue.h)("div", {
					key: "e-content",
					class: "q-expansion-item__content relative-position",
					style: contentStyle.value,
					id: targetUid.value
				}, hSlot(slots.default)), [[vue.vShow, showing.value]]);
			}
			function getContent() {
				const node = [getHeader(), (0, vue.h)(QSlideTransition_default, {
					duration: props.duration,
					onShow,
					onHide
				}, getTransitionChild)];
				if (props.expandSeparator) node.push((0, vue.h)(QSeparator_default, {
					class: "q-expansion-item__border q-expansion-item__border--top absolute-top",
					dark: isDark.value
				}), (0, vue.h)(QSeparator_default, {
					class: "q-expansion-item__border q-expansion-item__border--bottom absolute-bottom",
					dark: isDark.value
				}));
				return node;
			}
			if (props.group !== void 0) enterGroup();
			(0, vue.onBeforeUnmount)(() => {
				exitGroup?.();
			});
			return () => (0, vue.h)("div", { class: classes.value }, [(0, vue.h)("div", { class: "q-expansion-item__container relative-position" }, getContent())]);
		}
	});
	//#endregion
	//#region src/components/fab/use-fab.js
	const labelPositions = [
		"top",
		"right",
		"bottom",
		"left"
	];
	const useFabProps = {
		type: {
			type: String,
			default: "a"
		},
		outline: Boolean,
		push: Boolean,
		flat: Boolean,
		unelevated: Boolean,
		color: String,
		textColor: String,
		glossy: Boolean,
		square: Boolean,
		padding: String,
		label: {
			type: [String, Number],
			default: ""
		},
		labelPosition: {
			type: String,
			default: "right",
			validator: (v) => labelPositions.includes(v)
		},
		externalLabel: Boolean,
		hideLabel: { type: Boolean },
		labelClass: [
			Array,
			String,
			Object
		],
		labelStyle: [
			Array,
			String,
			Object
		],
		disable: Boolean,
		tabindex: [Number, String]
	};
	function useFab(props, showing) {
		return {
			formClass: (0, vue.computed)(() => `q-fab--form-${props.square ? "square" : "rounded"}`),
			stacked: (0, vue.computed)(() => !props.externalLabel && ["top", "bottom"].includes(props.labelPosition)),
			labelProps: (0, vue.computed)(() => {
				if (props.externalLabel) {
					const hideLabel = props.hideLabel === null ? !showing.value : props.hideLabel;
					return {
						action: "push",
						data: {
							class: [props.labelClass, `q-fab__label q-tooltip--style q-fab__label--external q-fab__label--external-${props.labelPosition}` + (hideLabel ? " q-fab__label--external-hidden" : "")],
							style: props.labelStyle
						}
					};
				}
				return {
					action: ["left", "top"].includes(props.labelPosition) ? "unshift" : "push",
					data: {
						class: [props.labelClass, `q-fab__label q-fab__label--internal q-fab__label--internal-${props.labelPosition}` + (props.hideLabel ? " q-fab__label--internal-hidden" : "")],
						style: props.labelStyle
					}
				};
			})
		};
	}
	//#endregion
	//#region src/components/fab/QFab.js
	const directions = [
		"up",
		"right",
		"down",
		"left"
	];
	const alignValues = [
		"left",
		"center",
		"right"
	];
	var QFab_default = createComponent({
		name: "QFab",
		props: {
			...useFabProps,
			...useModelToggleProps,
			icon: String,
			activeIcon: String,
			hideIcon: Boolean,
			hideLabel: {
				...useFabProps.hideLabel,
				default: null
			},
			direction: {
				type: String,
				default: "right",
				validator: (v) => directions.includes(v)
			},
			persistent: Boolean,
			verticalActionsAlign: {
				type: String,
				default: "center",
				validator: (v) => alignValues.includes(v)
			}
		},
		emits: useModelToggleEmits,
		setup(props, { slots }) {
			const triggerRef = (0, vue.ref)(null);
			const showing = (0, vue.ref)(props.modelValue === true);
			const targetUid = useId();
			const { proxy: { $q } } = (0, vue.getCurrentInstance)();
			const { formClass, labelProps } = useFab(props, showing);
			const { hide, toggle } = useModelToggle({
				showing,
				hideOnRouteChange: (0, vue.computed)(() => !props.persistent)
			});
			const slotScope = (0, vue.computed)(() => ({ opened: showing.value }));
			const classes = (0, vue.computed)(() => `q-fab z-fab row inline justify-center q-fab--align-${props.verticalActionsAlign} ${formClass.value}` + (showing.value ? " q-fab--opened" : " q-fab--closed"));
			const actionClass = (0, vue.computed)(() => `q-fab__actions flex no-wrap inline q-fab__actions--${props.direction} q-fab__actions--${showing.value ? "opened" : "closed"}`);
			const actionAttrs = (0, vue.computed)(() => {
				const attrs = {
					id: targetUid.value,
					role: "menu"
				};
				if (!showing.value) attrs["aria-hidden"] = "true";
				return attrs;
			});
			const iconHolderClass = (0, vue.computed)(() => `q-fab__icon-holder  q-fab__icon-holder--${showing.value ? "opened" : "closed"}`);
			function getIcon(kebab, camel) {
				const slotFn = slots[kebab];
				const localClass = `q-fab__${kebab} absolute-full`;
				return slotFn === void 0 ? (0, vue.h)(QIcon_default, {
					class: localClass,
					name: props[camel] || $q.iconSet.fab[camel]
				}) : (0, vue.h)("div", { class: localClass }, slotFn(slotScope.value));
			}
			function getTriggerContent() {
				const child = [];
				if (!props.hideIcon) child.push((0, vue.h)("div", { class: iconHolderClass.value }, [getIcon("icon", "icon"), getIcon("active-icon", "activeIcon")]));
				if (props.label !== "" || slots.label !== void 0) child[labelProps.value.action]((0, vue.h)("div", labelProps.value.data, slots.label !== void 0 ? slots.label(slotScope.value) : [props.label]));
				return hMergeSlot(slots.tooltip, child);
			}
			(0, vue.provide)(fabKey, {
				showing,
				onChildClick(evt) {
					hide(evt);
					if (evt?.qAvoidFocus !== true) triggerRef.value?.$el.focus();
				}
			});
			return () => (0, vue.h)("div", { class: classes.value }, [(0, vue.h)(QBtn_default, {
				ref: triggerRef,
				class: formClass.value,
				...props,
				noWrap: true,
				stack: props.stacked,
				align: void 0,
				icon: void 0,
				label: void 0,
				noCaps: true,
				fab: true,
				"aria-expanded": showing.value ? "true" : "false",
				"aria-haspopup": "true",
				"aria-controls": targetUid.value,
				onClick: toggle
			}, getTriggerContent), (0, vue.h)("div", {
				class: actionClass.value,
				...actionAttrs.value
			}, hSlot(slots.default))]);
		}
	});
	//#endregion
	//#region src/components/fab/QFabAction.js
	const anchorMap = {
		start: "self-end",
		center: "self-center",
		end: "self-start"
	};
	const anchorValues = Object.keys(anchorMap);
	var QFabAction_default = createComponent({
		name: "QFabAction",
		props: {
			...useFabProps,
			icon: {
				type: String,
				default: ""
			},
			anchor: {
				type: String,
				validator: (v) => anchorValues.includes(v)
			},
			to: [String, Object],
			replace: Boolean
		},
		emits: ["click"],
		setup(props, { slots, emit }) {
			const $fab = (0, vue.inject)(fabKey, () => ({
				showing: { value: true },
				onChildClick: noop
			}));
			const { formClass, labelProps } = useFab(props, $fab.showing);
			const classes = (0, vue.computed)(() => {
				const align = anchorMap[props.anchor];
				return formClass.value + (align !== void 0 ? ` ${align}` : "");
			});
			const isDisabled = (0, vue.computed)(() => props.disable || !$fab.showing.value);
			function click(e) {
				$fab.onChildClick(e);
				emit("click", e);
			}
			function getContent() {
				const child = [];
				if (slots.icon !== void 0) child.push(slots.icon());
				else if (props.icon !== "") child.push((0, vue.h)(QIcon_default, { name: props.icon }));
				if (props.label !== "" || slots.label !== void 0) child[labelProps.value.action]((0, vue.h)("div", labelProps.value.data, slots.label !== void 0 ? slots.label() : [props.label]));
				return hMergeSlot(slots.default, child);
			}
			const vm = (0, vue.getCurrentInstance)();
			Object.assign(vm.proxy, { click });
			return () => (0, vue.h)(QBtn_default, {
				class: classes.value,
				...props,
				noWrap: true,
				stack: props.stacked,
				icon: void 0,
				label: void 0,
				noCaps: true,
				fabMini: true,
				disable: isDisabled.value,
				onClick: click
			}, getContent);
		}
	});
	//#endregion
	//#region src/composables/use-form/use-form-child.js
	function useFormChild({ validate, resetValidation, requiresQForm }) {
		const $form = (0, vue.inject)(formKey, false);
		if ($form !== false) {
			const { props, proxy } = (0, vue.getCurrentInstance)();
			Object.assign(proxy, {
				validate,
				resetValidation
			});
			(0, vue.watch)(() => props.disable, (val) => {
				if (val) {
					if (typeof resetValidation === "function") resetValidation();
					$form.unbindComponent(proxy);
				} else $form.bindComponent(proxy);
			});
			(0, vue.onMounted)(() => {
				if (!props.disable) $form.bindComponent(proxy);
			});
			(0, vue.onBeforeUnmount)(() => {
				if (!props.disable) $form.unbindComponent(proxy);
			});
		} else if (requiresQForm) console.error("Parent QForm not found on useFormChild()!");
	}
	//#endregion
	//#region src/composables/private.use-validate/use-validate.js
	const lazyRulesValues = [
		true,
		false,
		"ondemand"
	];
	const useValidateProps = {
		modelValue: {},
		error: {
			type: Boolean,
			default: null
		},
		errorMessage: String,
		noErrorIcon: Boolean,
		rules: Array,
		reactiveRules: Boolean,
		lazyRules: {
			type: [Boolean, String],
			default: false,
			validator: (v) => lazyRulesValues.includes(v)
		}
	};
	function useValidate(focused, innerLoading) {
		const { props, proxy } = (0, vue.getCurrentInstance)();
		const innerError = (0, vue.ref)(false);
		const innerErrorMessage = (0, vue.ref)(null);
		const isDirtyModel = (0, vue.ref)(false);
		useFormChild({
			validate,
			resetValidation
		});
		let validateIndex = 0, unwatchRules;
		const hasRules = (0, vue.computed)(() => props.rules !== void 0 && props.rules !== null && props.rules.length !== 0);
		const canDebounceValidate = (0, vue.computed)(() => !props.disable && hasRules.value && !innerLoading.value);
		const hasError = (0, vue.computed)(() => props.error === true || innerError.value);
		const errorMessage = (0, vue.computed)(() => typeof props.errorMessage === "string" && props.errorMessage.length !== 0 ? props.errorMessage : innerErrorMessage.value);
		(0, vue.watch)(() => props.modelValue, () => {
			isDirtyModel.value = true;
			if (canDebounceValidate.value && props.lazyRules === false) debouncedValidate();
		});
		function onRulesChange() {
			if (props.lazyRules !== "ondemand" && canDebounceValidate.value && isDirtyModel.value) debouncedValidate();
		}
		(0, vue.watch)(() => props.reactiveRules, (val) => {
			if (val) {
				if (unwatchRules === void 0) unwatchRules = (0, vue.watch)(() => props.rules, onRulesChange, {
					immediate: true,
					deep: true
				});
			} else if (unwatchRules !== void 0) {
				unwatchRules();
				unwatchRules = void 0;
			}
		}, { immediate: true });
		(0, vue.watch)(() => props.lazyRules, onRulesChange);
		(0, vue.watch)(focused, (val) => {
			if (val) isDirtyModel.value = true;
			else if (canDebounceValidate.value && props.lazyRules !== "ondemand") debouncedValidate();
		});
		function resetValidation() {
			validateIndex++;
			innerLoading.value = false;
			isDirtyModel.value = false;
			innerError.value = false;
			innerErrorMessage.value = null;
			debouncedValidate.cancel();
		}
		function validate(val = props.modelValue) {
			if (props.disable || !hasRules.value) return true;
			const index = ++validateIndex;
			const setDirty = innerLoading.value ? () => {} : () => {
				isDirtyModel.value = true;
			};
			const update = (hasErr, msg) => {
				if (hasErr) setDirty();
				innerError.value = hasErr;
				innerErrorMessage.value = msg || null;
				innerLoading.value = false;
			};
			const promises = [];
			for (let i = 0; i < props.rules.length; i++) {
				const rule = props.rules[i];
				let res;
				if (typeof rule === "function") res = rule(val, testPattern);
				else if (typeof rule === "string" && testPattern[rule] !== void 0) res = testPattern[rule](val);
				if (res === false || typeof res === "string") {
					update(true, res);
					return false;
				} else if (res !== true && res !== void 0) promises.push(res);
			}
			if (promises.length === 0) {
				update(false);
				return true;
			}
			innerLoading.value = true;
			return Promise.all(promises).then((res) => {
				if (res === void 0 || !Array.isArray(res) || res.length === 0) {
					if (index === validateIndex) update(false);
					return true;
				}
				const msg = res.find((r) => r === false || typeof r === "string");
				if (index === validateIndex) update(msg !== void 0, msg);
				return msg === void 0;
			}, (err) => {
				if (index === validateIndex) {
					console.error(err);
					update(true);
				}
				return false;
			});
		}
		const debouncedValidate = debounce(validate, 0);
		(0, vue.onBeforeUnmount)(() => {
			unwatchRules?.();
			debouncedValidate.cancel();
		});
		Object.assign(proxy, {
			resetValidation,
			validate
		});
		injectProp(proxy, "hasError", () => hasError.value);
		return {
			isDirtyModel,
			hasRules,
			hasError,
			errorMessage,
			validate,
			resetValidation
		};
	}
	//#endregion
	//#region src/composables/private.use-field/use-field.js
	function fieldValueIsFilled(val) {
		return val !== void 0 && val !== null && String(val).length !== 0;
	}
	const useNonInputFieldProps = {
		...useDarkProps,
		...useValidateProps,
		label: String,
		stackLabel: Boolean,
		hint: String,
		hideHint: Boolean,
		prefix: String,
		suffix: String,
		labelColor: String,
		color: String,
		bgColor: String,
		filled: Boolean,
		outlined: Boolean,
		borderless: Boolean,
		standout: [Boolean, String],
		square: Boolean,
		loading: Boolean,
		labelSlot: Boolean,
		bottomSlots: Boolean,
		hideBottomSpace: Boolean,
		rounded: Boolean,
		dense: Boolean,
		itemAligned: Boolean,
		counter: Boolean,
		clearable: Boolean,
		clearIcon: String,
		disable: Boolean,
		readonly: Boolean,
		autofocus: Boolean,
		for: String
	};
	const useFieldProps = {
		...useNonInputFieldProps,
		maxlength: [Number, String]
	};
	const useFieldEmits = [
		"update:modelValue",
		"clear",
		"focus",
		"blur"
	];
	function useFieldState({ requiredForAttr = true, tagProp, changeEvent = false } = {}) {
		const { props, proxy } = (0, vue.getCurrentInstance)();
		const isDark = useDark(props, proxy.$q);
		const targetUid = useId({
			required: requiredForAttr,
			getValue: () => props.for
		});
		return {
			requiredForAttr,
			changeEvent,
			tag: tagProp ? (0, vue.computed)(() => props.tag) : { value: "label" },
			isDark,
			editable: (0, vue.computed)(() => !props.disable && !props.readonly),
			innerLoading: (0, vue.ref)(false),
			focused: (0, vue.ref)(false),
			hasPopupOpen: false,
			splitAttrs: useSplitAttrs(),
			targetUid,
			rootRef: (0, vue.ref)(null),
			targetRef: (0, vue.ref)(null),
			controlRef: (0, vue.ref)(null)
		};
	}
	function getInnerAppendNode(key, content) {
		return content === null ? null : (0, vue.h)("div", {
			key,
			class: "q-field__append q-field__marginal row no-wrap items-center q-anchor--skip"
		}, content);
	}
	function useField(state) {
		const { props, emit, slots, attrs, proxy } = (0, vue.getCurrentInstance)();
		const { $q } = proxy;
		let focusoutTimer = null;
		if (state.hasValue === void 0) state.hasValue = (0, vue.computed)(() => fieldValueIsFilled(props.modelValue));
		if (state.emitValue === void 0) state.emitValue = (value) => {
			emit("update:modelValue", value);
		};
		if (state.controlEvents === void 0) state.controlEvents = {
			onFocusin: onControlFocusin,
			onFocusout: onControlFocusout
		};
		Object.assign(state, {
			clearValue,
			onControlFocusin,
			onControlFocusout,
			focus
		});
		if (state.computedCounter === void 0) state.computedCounter = (0, vue.computed)(() => {
			if (props.counter) {
				const len = typeof props.modelValue === "string" || typeof props.modelValue === "number" ? String(props.modelValue).length : Array.isArray(props.modelValue) ? props.modelValue.length : 0;
				const max = props.maxlength !== void 0 ? props.maxlength : props.maxValues;
				return len + (max !== void 0 ? " / " + max : "");
			}
		});
		const { isDirtyModel, hasRules, hasError, errorMessage, resetValidation } = useValidate(state.focused, state.innerLoading);
		const floatingLabel = state.floatingLabel !== void 0 ? (0, vue.computed)(() => props.stackLabel || state.focused.value || state.floatingLabel.value) : (0, vue.computed)(() => props.stackLabel || state.focused.value || state.hasValue.value);
		const shouldRenderBottom = (0, vue.computed)(() => props.bottomSlots || props.hint !== void 0 || hasRules.value || props.counter || props.error !== null);
		const styleType = (0, vue.computed)(() => {
			if (props.filled) return "filled";
			if (props.outlined) return "outlined";
			if (props.borderless) return "borderless";
			if (props.standout) return "standout";
			return "standard";
		});
		const classes = (0, vue.computed)(() => `q-field row no-wrap items-start q-field--${styleType.value}` + (state.fieldClass !== void 0 ? ` ${state.fieldClass.value}` : "") + (props.rounded ? " q-field--rounded" : "") + (props.square ? " q-field--square" : "") + (floatingLabel.value ? " q-field--float" : "") + (hasLabel.value ? " q-field--labeled" : "") + (props.dense ? " q-field--dense" : "") + (props.itemAligned ? " q-field--item-aligned q-item-type" : "") + (state.isDark.value ? " q-field--dark" : "") + (state.getControl === void 0 ? " q-field--auto-height" : "") + (state.focused.value ? " q-field--focused" : "") + (hasError.value ? " q-field--error" : "") + (hasError.value || state.focused.value ? " q-field--highlighted" : "") + (!props.hideBottomSpace && shouldRenderBottom.value ? " q-field--with-bottom" : "") + (props.disable ? " q-field--disabled" : props.readonly ? " q-field--readonly" : ""));
		const contentClass = (0, vue.computed)(() => "q-field__control relative-position row no-wrap" + (props.bgColor !== void 0 ? ` bg-${props.bgColor}` : "") + (hasError.value ? " text-negative" : typeof props.standout === "string" && props.standout.length !== 0 && state.focused.value ? ` ${props.standout}` : props.color !== void 0 ? ` text-${props.color}` : ""));
		const hasLabel = (0, vue.computed)(() => props.labelSlot || props.label !== void 0);
		const labelClass = (0, vue.computed)(() => "q-field__label no-pointer-events absolute ellipsis" + (props.labelColor !== void 0 && !hasError.value ? ` text-${props.labelColor}` : ""));
		const controlSlotScope = (0, vue.computed)(() => ({
			id: state.targetUid.value,
			editable: state.editable.value,
			focused: state.focused.value,
			floatingLabel: floatingLabel.value,
			modelValue: props.modelValue,
			emitValue: state.emitValue
		}));
		const attributes = (0, vue.computed)(() => {
			const acc = {};
			if (state.targetUid.value) acc.for = state.targetUid.value;
			if (props.disable) acc["aria-disabled"] = "true";
			return acc;
		});
		function focusHandler() {
			const el = document.activeElement;
			let target = state.targetRef?.value;
			if (target && (el === null || el.id !== state.targetUid.value)) {
				if (!target.hasAttribute("tabindex")) target = target.querySelector("[tabindex]");
				if (target !== el) target?.focus({ preventScroll: true });
			}
		}
		function focus() {
			addFocusFn(focusHandler);
		}
		function blur() {
			removeFocusFn(focusHandler);
			const el = document.activeElement;
			if (el !== null && state.rootRef.value.contains(el)) el.blur();
		}
		function onControlFocusin(e) {
			if (focusoutTimer !== null) {
				clearTimeout(focusoutTimer);
				focusoutTimer = null;
			}
			if (state.editable.value && !state.focused.value) {
				state.focused.value = true;
				emit("focus", e);
			}
		}
		function onControlFocusout(e, then) {
			if (focusoutTimer !== null) clearTimeout(focusoutTimer);
			focusoutTimer = setTimeout(() => {
				focusoutTimer = null;
				if (document.hasFocus() && (state.hasPopupOpen || state.controlRef === void 0 || state.controlRef.value === null || state.controlRef.value.contains(document.activeElement))) return;
				if (state.focused.value) {
					state.focused.value = false;
					emit("blur", e);
				}
				then?.();
			}, 0);
		}
		function clearValue(e) {
			stopAndPrevent(e);
			if (!$q.platform.is.mobile) (state.targetRef?.value || state.rootRef.value).focus();
			else if (state.rootRef.value.contains(document.activeElement)) document.activeElement.blur();
			if (props.type === "file") state.inputRef.value.value = null;
			state.onClear?.();
			emit("update:modelValue", null);
			if (state.changeEvent) emit("change", null);
			emit("clear", props.modelValue);
			(0, vue.nextTick)(() => {
				const isDirty = isDirtyModel.value;
				resetValidation();
				isDirtyModel.value = isDirty;
			});
		}
		function onClearableKeyup(evt) {
			if ([13, 32].includes(evt.keyCode)) clearValue(evt);
		}
		function getContent() {
			const node = [];
			if (slots.prepend !== void 0) node.push((0, vue.h)("div", {
				class: "q-field__prepend q-field__marginal row no-wrap items-center",
				key: "prepend",
				onClick: prevent
			}, slots.prepend()));
			node.push((0, vue.h)("div", { class: "q-field__control-container col relative-position row no-wrap q-anchor--skip" }, getControlContainer()));
			if (hasError.value && !props.noErrorIcon) node.push(getInnerAppendNode("error", [(0, vue.h)(QIcon_default, {
				name: $q.iconSet.field.error,
				color: "negative"
			})]));
			if (props.loading || state.innerLoading.value) node.push(getInnerAppendNode("inner-loading-append", slots.loading !== void 0 ? slots.loading() : [(0, vue.h)(QSpinner_default, { color: props.color })]));
			else if (props.clearable && state.hasValue.value && state.editable.value) node.push(getInnerAppendNode("inner-clearable-append", [(0, vue.h)(QIcon_default, {
				class: "q-field__focusable-action",
				name: props.clearIcon || $q.iconSet.field.clear,
				tabindex: 0,
				role: "button",
				"aria-hidden": "false",
				"aria-label": $q.lang.label.clear,
				onKeyup: onClearableKeyup,
				onClick: clearValue
			})]));
			if (slots.append !== void 0) node.push((0, vue.h)("div", {
				class: "q-field__append q-field__marginal row no-wrap items-center",
				key: "append",
				onClick: prevent
			}, slots.append()));
			if (state.getInnerAppend !== void 0) node.push(getInnerAppendNode("inner-append", state.getInnerAppend()));
			if (state.getControlChild !== void 0) node.push(state.getControlChild());
			return node;
		}
		function getControlContainer() {
			const node = [];
			if (props.prefix !== void 0 && props.prefix !== null) node.push((0, vue.h)("div", { class: "q-field__prefix no-pointer-events row items-center" }, props.prefix));
			if (state.getShadowControl !== void 0 && state.hasShadow.value) node.push(state.getShadowControl());
			if (hasLabel.value) node.push((0, vue.h)("div", { class: labelClass.value }, hSlot(slots.label, props.label)));
			if (state.getControl !== void 0) node.push(state.getControl());
			else if (slots.rawControl !== void 0) node.push(slots.rawControl());
			else if (slots.control !== void 0) node.push((0, vue.h)("div", {
				ref: state.targetRef,
				class: "q-field__native row",
				tabindex: -1,
				...state.splitAttrs.attributes.value,
				"data-autofocus": props.autofocus || void 0
			}, slots.control(controlSlotScope.value)));
			if (props.suffix !== void 0 && props.suffix !== null) node.push((0, vue.h)("div", { class: "q-field__suffix no-pointer-events row items-center" }, props.suffix));
			return node.concat(hSlot(slots.default));
		}
		function getBottom() {
			let msg, key;
			if (hasError.value) if (errorMessage.value !== null) {
				msg = [(0, vue.h)("div", { role: "alert" }, errorMessage.value)];
				key = `q--slot-error-${errorMessage.value}`;
			} else {
				msg = hSlot(slots.error);
				key = "q--slot-error";
			}
			else if (!props.hideHint || state.focused.value) if (props.hint !== void 0) {
				msg = [(0, vue.h)("div", props.hint)];
				key = `q--slot-hint-${props.hint}`;
			} else {
				msg = hSlot(slots.hint);
				key = "q--slot-hint";
			}
			const hasCounter = props.counter || slots.counter !== void 0;
			if (props.hideBottomSpace && !hasCounter && msg === void 0) return;
			const main = (0, vue.h)("div", {
				key,
				class: "q-field__messages col"
			}, msg);
			return (0, vue.h)("div", {
				class: "q-field__bottom row items-start q-field__bottom--" + (props.hideBottomSpace ? "stale" : "animated"),
				onClick: prevent
			}, [props.hideBottomSpace ? main : (0, vue.h)(vue.Transition, { name: "q-transition--field-message" }, () => main), hasCounter ? (0, vue.h)("div", { class: "q-field__counter" }, slots.counter !== void 0 ? slots.counter() : state.computedCounter.value) : null]);
		}
		let shouldActivate = false;
		(0, vue.onDeactivated)(() => {
			shouldActivate = true;
		});
		(0, vue.onActivated)(() => {
			if (shouldActivate && props.autofocus) proxy.focus();
		});
		if (props.autofocus) (0, vue.onMounted)(() => {
			proxy.focus();
		});
		(0, vue.onBeforeUnmount)(() => {
			if (focusoutTimer !== null) clearTimeout(focusoutTimer);
		});
		Object.assign(proxy, {
			focus,
			blur
		});
		return function renderField() {
			const labelAttrs = state.getControl === void 0 && slots.control === void 0 ? {
				...state.splitAttrs.attributes.value,
				"data-autofocus": props.autofocus || void 0,
				...attributes.value
			} : attributes.value;
			return (0, vue.h)(state.tag.value, {
				ref: state.rootRef,
				class: [classes.value, attrs.class],
				style: attrs.style,
				...labelAttrs
			}, [
				slots.before !== void 0 ? (0, vue.h)("div", {
					class: "q-field__before q-field__marginal row no-wrap items-center",
					onClick: prevent
				}, slots.before()) : null,
				(0, vue.h)("div", { class: "q-field__inner relative-position col self-stretch" }, [(0, vue.h)("div", {
					ref: state.controlRef,
					class: contentClass.value,
					tabindex: -1,
					...state.controlEvents
				}, getContent()), shouldRenderBottom.value ? getBottom() : null]),
				slots.after !== void 0 ? (0, vue.h)("div", {
					class: "q-field__after q-field__marginal row no-wrap items-center",
					onClick: prevent
				}, slots.after()) : null
			]);
		};
	}
	//#endregion
	//#region src/components/field/QField.js
	var QField_default = createComponent({
		name: "QField",
		inheritAttrs: false,
		props: {
			...useFieldProps,
			tag: {
				type: String,
				default: "label"
			}
		},
		emits: useFieldEmits,
		setup() {
			return useField(useFieldState({ tagProp: true }));
		}
	});
	//#endregion
	//#region src/composables/private.use-file/use-file.js
	function filterFiles(files, rejectedFiles, failedPropValidation, filterFn) {
		const acceptedFiles = [];
		files.forEach((file) => {
			if (filterFn(file)) acceptedFiles.push(file);
			else rejectedFiles.push({
				failedPropValidation,
				file
			});
		});
		return acceptedFiles;
	}
	function stopAndPreventDrag(e) {
		if (e?.dataTransfer) e.dataTransfer.dropEffect = "copy";
		stopAndPrevent(e);
	}
	const useFileProps = {
		multiple: Boolean,
		accept: String,
		capture: String,
		maxFileSize: [Number, String],
		maxTotalSize: [Number, String],
		maxFiles: [Number, String],
		filter: Function
	};
	const useFileEmits = ["rejected"];
	function useFile({ editable, dnd, getFileInput, addFilesToQueue }) {
		const { props, emit, proxy } = (0, vue.getCurrentInstance)();
		const dndRef = (0, vue.ref)(null);
		const extensions = (0, vue.computed)(() => props.accept !== void 0 ? props.accept.split(",").map((ext) => {
			ext = ext.trim();
			if (ext === "*") return "*/";
			else if (ext.endsWith("/*")) ext = ext.slice(0, -1);
			return ext.toUpperCase();
		}) : null);
		const maxFilesNumber = (0, vue.computed)(() => Number.parseInt(props.maxFiles, 10));
		const maxTotalSizeNumber = (0, vue.computed)(() => Number.parseInt(props.maxTotalSize, 10));
		function pickFiles(e) {
			if (editable.value) {
				if (e !== Object(e)) e = { target: null };
				if (e.target?.matches("input[type=\"file\"]") === true) {
					if (e.clientX === 0 && e.clientY === 0) stop(e);
				} else {
					const input = getFileInput();
					if (input !== e.target) input?.click(e);
				}
			}
		}
		function addFiles(files) {
			if (editable.value && files) addFilesToQueue(null, files);
		}
		function processFiles(e, filesToProcess, currentFileList, append) {
			let files = [...filesToProcess || e.target.files];
			const rejectedFiles = [];
			const done = () => {
				if (rejectedFiles.length !== 0) emit("rejected", rejectedFiles);
			};
			if (props.accept !== void 0 && !extensions.value.includes("*/")) {
				files = filterFiles(files, rejectedFiles, "accept", (file) => extensions.value.some((ext) => (ext.endsWith("/") ? file.type.toUpperCase().startsWith(ext) : file.type.toUpperCase() === ext) || file.name.toUpperCase().endsWith(ext)));
				if (files.length === 0) return done();
			}
			if (props.maxFileSize !== void 0) {
				const maxFileSize = Number.parseInt(props.maxFileSize, 10);
				files = filterFiles(files, rejectedFiles, "max-file-size", (file) => file.size <= maxFileSize);
				if (files.length === 0) return done();
			}
			if (!props.multiple && files.length !== 0) files = [files[0]];
			files.forEach((file) => {
				file.__key = JSON.stringify([
					file.webkitRelativePath,
					file.lastModified,
					file.name,
					file.size
				]);
			});
			if (append) {
				const filenameSet = new Set(currentFileList.map((entry) => entry.__key));
				files = filterFiles(files, rejectedFiles, "duplicate", (file) => {
					if (filenameSet.has(file.__key)) return false;
					filenameSet.add(file.__key);
					return true;
				});
			}
			if (files.length === 0) return done();
			if (props.maxTotalSize !== void 0) {
				let size = append ? currentFileList.reduce((total, file) => total + file.size, 0) : 0;
				files = filterFiles(files, rejectedFiles, "max-total-size", (file) => {
					const newSize = size + file.size;
					if (newSize > maxTotalSizeNumber.value) return false;
					size = newSize;
					return true;
				});
				if (files.length === 0) return done();
			}
			if (typeof props.filter === "function") {
				const filteredFiles = props.filter(files);
				files = filterFiles(files, rejectedFiles, "filter", (file) => filteredFiles.includes(file));
			}
			if (props.maxFiles !== void 0) {
				let filesNumber = append ? currentFileList.length : 0;
				files = filterFiles(files, rejectedFiles, "max-files", () => {
					filesNumber++;
					return filesNumber <= maxFilesNumber.value;
				});
				if (files.length === 0) return done();
			}
			done();
			if (files.length !== 0) return files;
		}
		function onDragover(e) {
			stopAndPreventDrag(e);
			if (!dnd.value) dnd.value = true;
		}
		function onDragleave(e) {
			stopAndPrevent(e);
			if (e.relatedTarget !== null || !client.is.safari ? e.relatedTarget !== dndRef.value : !document.elementsFromPoint(e.clientX, e.clientY).includes(dndRef.value)) dnd.value = false;
		}
		function onDrop(e) {
			stopAndPreventDrag(e);
			const files = e.dataTransfer.files;
			if (files.length !== 0) addFilesToQueue(null, files);
			dnd.value = false;
		}
		function getDndNode(type) {
			if (dnd.value) return (0, vue.h)("div", {
				ref: dndRef,
				class: `q-${type}__dnd absolute-full`,
				onDragenter: stopAndPreventDrag,
				onDragover: stopAndPreventDrag,
				onDragleave,
				onDrop
			});
		}
		Object.assign(proxy, {
			pickFiles,
			addFiles
		});
		return {
			pickFiles,
			addFiles,
			onDragover,
			onDragleave,
			processFiles,
			getDndNode,
			maxFilesNumber,
			maxTotalSizeNumber
		};
	}
	//#endregion
	//#region src/composables/private.use-file/use-file-dom-props.js
	function useFileDomProps(props, typeGuard) {
		function getFormDomProps() {
			const model = props.modelValue;
			try {
				const dt = "DataTransfer" in window ? new DataTransfer() : "ClipboardEvent" in window ? new ClipboardEvent("").clipboardData : void 0;
				if (Object(model) === model) ("length" in model ? [...model] : [model]).forEach((file) => {
					dt.items.add(file);
				});
				return { files: dt.files };
			} catch {
				return { files: void 0 };
			}
		}
		return typeGuard ? (0, vue.computed)(() => {
			if (props.type !== "file") return;
			return getFormDomProps();
		}) : (0, vue.computed)(getFormDomProps);
	}
	//#endregion
	//#region src/components/file/QFile.js
	function onKeydown$1(e) {
		if (e.keyCode === 13) prevent(e);
	}
	var QFile_default = createComponent({
		name: "QFile",
		inheritAttrs: false,
		props: {
			...useNonInputFieldProps,
			...useFormProps,
			...useFileProps,
			modelValue: [
				File,
				FileList,
				Array
			],
			append: Boolean,
			useChips: Boolean,
			displayValue: [String, Number],
			tabindex: {
				type: [String, Number],
				default: 0
			},
			counterLabel: Function,
			inputClass: [
				Array,
				String,
				Object
			],
			inputStyle: [
				Array,
				String,
				Object
			]
		},
		emits: [...useFieldEmits, ...useFileEmits],
		setup(props, { slots, emit, attrs }) {
			const { proxy } = (0, vue.getCurrentInstance)();
			const state = useFieldState();
			const inputRef = (0, vue.ref)(null);
			const dnd = (0, vue.ref)(false);
			const nameProp = useFormInputNameAttr(props);
			const { pickFiles, onDragover, onDragleave, processFiles, getDndNode } = useFile({
				editable: state.editable,
				dnd,
				getFileInput,
				addFilesToQueue
			});
			const formDomProps = useFileDomProps(props);
			const innerValue = (0, vue.computed)(() => Object(props.modelValue) === props.modelValue ? "length" in props.modelValue ? [...props.modelValue] : [props.modelValue] : []);
			const hasValue = (0, vue.computed)(() => fieldValueIsFilled(innerValue.value));
			const selectedString = (0, vue.computed)(() => innerValue.value.map((file) => file.name).join(", "));
			const totalSize = (0, vue.computed)(() => humanStorageSize(innerValue.value.reduce((acc, file) => acc + file.size, 0)));
			const counterProps = (0, vue.computed)(() => ({
				totalSize: totalSize.value,
				filesNumber: innerValue.value.length,
				maxFiles: props.maxFiles
			}));
			const inputAttrs = (0, vue.computed)(() => ({
				tabindex: -1,
				type: "file",
				title: "",
				accept: props.accept,
				capture: props.capture,
				name: nameProp.value,
				...attrs,
				id: state.targetUid.value,
				disabled: !state.editable.value
			}));
			const fieldClass = (0, vue.computed)(() => "q-file q-field--auto-height" + (dnd.value ? " q-file--dnd" : ""));
			const isAppending = (0, vue.computed)(() => props.multiple && props.append);
			function removeAtIndex(index) {
				const files = [...innerValue.value];
				files.splice(index, 1);
				emitValue(files);
			}
			function removeFile(file) {
				const index = innerValue.value.indexOf(file);
				if (index !== -1) removeAtIndex(index);
			}
			function emitValue(files) {
				emit("update:modelValue", props.multiple ? files : files[0]);
			}
			function onKeyup(e) {
				if (e.keyCode === 13 || e.keyCode === 32) pickFiles(e);
			}
			function getFileInput() {
				return inputRef.value;
			}
			function addFilesToQueue(e, fileList) {
				const files = processFiles(e, fileList, innerValue.value, isAppending.value);
				const fileInput = getFileInput();
				if (fileInput !== void 0 && fileInput !== null) fileInput.value = "";
				if (files === void 0) return;
				if (props.multiple ? props.modelValue && files.every((f) => innerValue.value.includes(f)) : props.modelValue === files[0]) return;
				emitValue(isAppending.value ? [...innerValue.value, ...files] : files);
			}
			function getFiller() {
				return [(0, vue.h)("input", {
					class: [props.inputClass, "q-file__filler"],
					style: props.inputStyle
				})];
			}
			function getSelection() {
				if (slots.file !== void 0) return innerValue.value.length === 0 ? getFiller() : innerValue.value.map((file, index) => slots.file({
					index,
					file,
					ref: this
				}));
				if (slots.selected !== void 0) return innerValue.value.length === 0 ? getFiller() : slots.selected({
					files: innerValue.value,
					ref: this
				});
				if (props.useChips) return innerValue.value.length === 0 ? getFiller() : innerValue.value.map((file, i) => (0, vue.h)(QChip_default, {
					key: "file-" + i,
					removable: state.editable.value,
					dense: true,
					textColor: props.color,
					tabindex: props.tabindex,
					onRemove: () => {
						removeAtIndex(i);
					}
				}, () => (0, vue.h)("span", {
					class: "ellipsis",
					textContent: file.name
				})));
				const textContent = props.displayValue !== void 0 ? props.displayValue : selectedString.value;
				return textContent.length !== 0 ? [(0, vue.h)("div", {
					class: props.inputClass,
					style: props.inputStyle,
					textContent
				})] : getFiller();
			}
			function getInput() {
				const data = {
					ref: inputRef,
					...inputAttrs.value,
					...formDomProps.value,
					class: "q-field__input fit absolute-full cursor-pointer",
					onChange: addFilesToQueue
				};
				if (props.multiple) data.multiple = true;
				return (0, vue.h)("input", data);
			}
			Object.assign(state, {
				fieldClass,
				emitValue,
				hasValue,
				inputRef,
				innerValue,
				floatingLabel: (0, vue.computed)(() => hasValue.value || fieldValueIsFilled(props.displayValue)),
				computedCounter: (0, vue.computed)(() => {
					if (props.counterLabel !== void 0) return props.counterLabel(counterProps.value);
					const max = props.maxFiles;
					return `${innerValue.value.length}${max !== void 0 ? " / " + max : ""} (${totalSize.value})`;
				}),
				getControlChild: () => getDndNode("file"),
				getControl: () => {
					const data = {
						ref: state.targetRef,
						class: "q-field__native row items-center cursor-pointer",
						tabindex: props.tabindex
					};
					if (state.editable.value) Object.assign(data, {
						onDragover,
						onDragleave,
						onKeydown: onKeydown$1,
						onKeyup
					});
					return (0, vue.h)("div", data, [getInput()].concat(getSelection()));
				}
			});
			Object.assign(proxy, {
				removeAtIndex,
				removeFile,
				getNativeElement: () => inputRef.value
			});
			injectProp(proxy, "nativeEl", () => inputRef.value);
			return useField(state);
		}
	});
	//#endregion
	//#region src/components/footer/QFooter.js
	function updateLocal$1(prop, val) {
		if (prop.value !== val) prop.value = val;
	}
	var QFooter_default = createComponent({
		name: "QFooter",
		props: {
			modelValue: {
				type: Boolean,
				default: true
			},
			reveal: Boolean,
			bordered: Boolean,
			elevated: Boolean,
			heightHint: {
				type: [String, Number],
				default: 50
			}
		},
		emits: ["reveal", "focusin"],
		setup(props, { slots, emit }) {
			const { proxy: { $q } } = (0, vue.getCurrentInstance)();
			const $layout = (0, vue.inject)(layoutKey, emptyRenderFn);
			if ($layout === emptyRenderFn) {
				console.error("QFooter needs to be child of QLayout");
				return emptyRenderFn;
			}
			const size = (0, vue.ref)(Number.parseInt(props.heightHint, 10));
			const revealed = (0, vue.ref)(true);
			const windowHeight = (0, vue.ref)(isRuntimeSsrPreHydration.value || $layout.isContainer.value ? 0 : window.innerHeight);
			const fixed = (0, vue.computed)(() => props.reveal || $layout.view.value.includes("F") || $q.platform.is.ios && $layout.isContainer.value);
			const containerHeight = (0, vue.computed)(() => $layout.isContainer.value ? $layout.containerHeight.value : windowHeight.value);
			const offset = (0, vue.computed)(() => {
				if (!props.modelValue) return 0;
				if (fixed.value) return revealed.value ? size.value : 0;
				const localOffset = $layout.scroll.value.position + containerHeight.value + size.value - $layout.height.value;
				return Math.max(localOffset, 0);
			});
			const hidden = (0, vue.computed)(() => !props.modelValue || fixed.value && !revealed.value);
			const revealOnFocus = (0, vue.computed)(() => props.modelValue && hidden.value && props.reveal);
			const classes = (0, vue.computed)(() => "q-footer q-layout__section--marginal " + (fixed.value ? "fixed" : "absolute") + "-bottom" + (props.bordered ? " q-footer--bordered" : "") + (hidden.value ? " q-footer--hidden" : "") + (props.modelValue ? "" : " q-layout--prevent-focus" + (fixed.value ? "" : " hidden")));
			const style = (0, vue.computed)(() => {
				const view = $layout.rows.value.bottom, css = {};
				if (view[0] === "l" && $layout.left.space) css[$q.lang.rtl ? "right" : "left"] = `${$layout.left.size}px`;
				if (view[2] === "r" && $layout.right.space) css[$q.lang.rtl ? "left" : "right"] = `${$layout.right.size}px`;
				return css;
			});
			function updateLayout(prop, val) {
				$layout.update("footer", prop, val);
			}
			function onResize({ height }) {
				updateLocal$1(size, height);
				updateLayout("size", height);
			}
			function updateRevealed() {
				if (!props.reveal) return;
				const { direction, position, inflectionPoint } = $layout.scroll.value;
				updateLocal$1(revealed, direction === "up" || position - inflectionPoint < 100 || $layout.height.value - containerHeight.value - position - size.value < 300);
			}
			function onFocusin(evt) {
				if (revealOnFocus.value) updateLocal$1(revealed, true);
				emit("focusin", evt);
			}
			(0, vue.watch)(() => props.modelValue, (val) => {
				updateLayout("space", val);
				updateLocal$1(revealed, true);
				$layout.animate();
			});
			(0, vue.watch)(offset, (val) => {
				updateLayout("offset", val);
			});
			(0, vue.watch)(() => props.reveal, (val) => {
				if (!val) updateLocal$1(revealed, props.modelValue);
			});
			(0, vue.watch)(revealed, (val) => {
				$layout.animate();
				emit("reveal", val);
			});
			(0, vue.watch)([
				size,
				$layout.scroll,
				$layout.height
			], updateRevealed);
			(0, vue.watch)(() => $q.screen.height, (val) => {
				if (!$layout.isContainer.value) updateLocal$1(windowHeight, val);
			});
			const instance = {};
			$layout.instances.footer = instance;
			if (props.modelValue) updateLayout("size", size.value);
			updateLayout("space", props.modelValue);
			updateLayout("offset", offset.value);
			(0, vue.onBeforeUnmount)(() => {
				if ($layout.instances.footer === instance) {
					$layout.instances.footer = void 0;
					updateLayout("size", 0);
					updateLayout("offset", 0);
					updateLayout("space", false);
				}
			});
			return () => {
				const child = hMergeSlot(slots.default, [(0, vue.h)(QResizeObserver_default, {
					debounce: 0,
					onResize
				})]);
				if (props.elevated) child.push((0, vue.h)("div", { class: "q-layout__shadow absolute-full overflow-hidden no-pointer-events" }));
				return (0, vue.h)("footer", {
					class: classes.value,
					style: style.value,
					onFocusin
				}, child);
			};
		}
	});
	//#endregion
	//#region src/components/form/QForm.js
	function validateComponent(comp) {
		const valid = comp.validate();
		return typeof valid.then === "function" ? valid.then((isValid) => ({
			valid: isValid,
			comp
		}), (err) => ({
			valid: false,
			comp,
			err
		})) : Promise.resolve({
			valid,
			comp
		});
	}
	var QForm_default = createComponent({
		name: "QForm",
		props: {
			autofocus: Boolean,
			noErrorFocus: Boolean,
			noResetFocus: Boolean,
			greedy: Boolean,
			onSubmit: Function
		},
		emits: [
			"reset",
			"validationSuccess",
			"validationError"
		],
		setup(props, { slots, emit }) {
			const vm = (0, vue.getCurrentInstance)();
			const rootRef = (0, vue.ref)(null);
			let validateIndex = 0;
			const registeredComponents = [];
			function validate(shouldFocus) {
				const localFocus = typeof shouldFocus === "boolean" ? shouldFocus : !props.noErrorFocus;
				const index = ++validateIndex;
				const emitEvent = (res, compRef) => {
					emit(`validation${res ? "Success" : "Error"}`, compRef);
				};
				return (props.greedy ? Promise.all(registeredComponents.map(validateComponent)).then((res) => res.filter((r) => !r.valid)) : registeredComponents.reduce((acc, comp) => acc.then(() => validateComponent(comp)).then((r) => {
					if (!r.valid) throw r;
				}), Promise.resolve()).catch((err) => [err])).then((errors) => {
					if (errors === void 0 || errors.length === 0) {
						if (index === validateIndex) emitEvent(true);
						return true;
					}
					if (index === validateIndex) {
						const { comp, err } = errors[0];
						if (err !== void 0) console.error(err);
						emitEvent(false, comp);
						if (localFocus) {
							const activeError = errors.find(({ comp: compRef }) => typeof compRef.focus === "function" && !vmIsDestroyed(compRef.$));
							if (activeError !== void 0) activeError.comp.focus();
						}
					}
					return false;
				});
			}
			function resetValidation() {
				validateIndex++;
				registeredComponents.forEach((comp) => {
					if (typeof comp.resetValidation === "function") comp.resetValidation();
				});
			}
			function submit(evt) {
				if (evt !== void 0) stopAndPrevent(evt);
				const index = validateIndex + 1;
				validate().then((val) => {
					if (index === validateIndex && val) {
						if (props.onSubmit !== void 0) emit("submit", evt);
						else if (evt?.target !== void 0 && typeof evt.target.submit === "function") evt.target.submit();
					}
				});
			}
			function reset(evt) {
				if (evt !== void 0) stopAndPrevent(evt);
				emit("reset");
				(0, vue.nextTick)(() => {
					resetValidation();
					if (props.autofocus && !props.noResetFocus) focus();
				});
			}
			function focus() {
				addFocusFn(() => {
					if (rootRef.value === null) return;
					(rootRef.value.querySelector("[autofocus][tabindex], [data-autofocus][tabindex]") || rootRef.value.querySelector("[autofocus] [tabindex], [data-autofocus] [tabindex]") || rootRef.value.querySelector("[autofocus], [data-autofocus]") || Array.prototype.find.call(rootRef.value.querySelectorAll("[tabindex]"), (el) => el.tabIndex !== -1))?.focus({ preventScroll: true });
				});
			}
			(0, vue.provide)(formKey, {
				bindComponent(vmProxy) {
					registeredComponents.push(vmProxy);
				},
				unbindComponent(vmProxy) {
					const index = registeredComponents.indexOf(vmProxy);
					if (index !== -1) registeredComponents.splice(index, 1);
				}
			});
			let shouldActivate = false;
			(0, vue.onDeactivated)(() => {
				shouldActivate = true;
			});
			(0, vue.onActivated)(() => {
				if (shouldActivate && props.autofocus) focus();
			});
			(0, vue.onMounted)(() => {
				if (props.autofocus) focus();
			});
			Object.assign(vm.proxy, {
				validate,
				resetValidation,
				submit,
				reset,
				focus,
				getValidationComponents: () => registeredComponents
			});
			return () => (0, vue.h)("form", {
				class: "q-form",
				ref: rootRef,
				onSubmit: submit,
				onReset: reset
			}, hSlot(slots.default));
		}
	});
	//#endregion
	//#region src/components/form/QFormChildMixin.js
	var QFormChildMixin_default = {
		inject: { [formKey]: { default: noop } },
		watch: { disable(val) {
			const $form = this.$.provides[formKey];
			if ($form !== void 0) if (val) {
				this.resetValidation();
				$form.unbindComponent(this);
			} else $form.bindComponent(this);
		} },
		methods: {
			validate() {},
			resetValidation() {}
		},
		mounted() {
			if (!this.disable) this.$.provides[formKey]?.bindComponent(this);
		},
		beforeUnmount() {
			if (!this.disable) this.$.provides[formKey]?.unbindComponent(this);
		}
	};
	//#endregion
	//#region src/components/header/QHeader.js
	function updateLocal(prop, val) {
		if (prop.value !== val) prop.value = val;
	}
	var QHeader_default = createComponent({
		name: "QHeader",
		props: {
			modelValue: {
				type: Boolean,
				default: true
			},
			reveal: Boolean,
			revealOffset: {
				type: Number,
				default: 250
			},
			bordered: Boolean,
			elevated: Boolean,
			heightHint: {
				type: [String, Number],
				default: 50
			}
		},
		emits: ["reveal", "focusin"],
		setup(props, { slots, emit }) {
			const { proxy: { $q } } = (0, vue.getCurrentInstance)();
			const $layout = (0, vue.inject)(layoutKey, emptyRenderFn);
			if ($layout === emptyRenderFn) {
				console.error("QHeader needs to be child of QLayout");
				return emptyRenderFn;
			}
			const size = (0, vue.ref)(Number.parseInt(props.heightHint, 10));
			const revealed = (0, vue.ref)(true);
			const fixed = (0, vue.computed)(() => props.reveal || $layout.view.value.includes("H") || $q.platform.is.ios && $layout.isContainer.value);
			const offset = (0, vue.computed)(() => {
				if (!props.modelValue) return 0;
				if (fixed.value) return revealed.value ? size.value : 0;
				const localOffset = size.value - $layout.scroll.value.position;
				return Math.max(localOffset, 0);
			});
			const hidden = (0, vue.computed)(() => !props.modelValue || fixed.value && !revealed.value);
			const revealOnFocus = (0, vue.computed)(() => props.modelValue && hidden.value && props.reveal);
			const classes = (0, vue.computed)(() => "q-header q-layout__section--marginal " + (fixed.value ? "fixed" : "absolute") + "-top" + (props.bordered ? " q-header--bordered" : "") + (hidden.value ? " q-header--hidden" : "") + (props.modelValue ? "" : " q-layout--prevent-focus"));
			const style = (0, vue.computed)(() => {
				const view = $layout.rows.value.top, css = {};
				if (view[0] === "l" && $layout.left.space) css[$q.lang.rtl ? "right" : "left"] = `${$layout.left.size}px`;
				if (view[2] === "r" && $layout.right.space) css[$q.lang.rtl ? "left" : "right"] = `${$layout.right.size}px`;
				return css;
			});
			function updateLayout(prop, val) {
				$layout.update("header", prop, val);
			}
			function onResize({ height }) {
				updateLocal(size, height);
				updateLayout("size", height);
			}
			function onFocusin(evt) {
				if (revealOnFocus.value) updateLocal(revealed, true);
				emit("focusin", evt);
			}
			(0, vue.watch)(() => props.modelValue, (val) => {
				updateLayout("space", val);
				updateLocal(revealed, true);
				$layout.animate();
			});
			(0, vue.watch)(offset, (val) => {
				updateLayout("offset", val);
			});
			(0, vue.watch)(() => props.reveal, (val) => {
				if (!val) updateLocal(revealed, props.modelValue);
			});
			(0, vue.watch)(revealed, (val) => {
				$layout.animate();
				emit("reveal", val);
			});
			(0, vue.watch)($layout.scroll, (scroll) => {
				if (props.reveal) updateLocal(revealed, scroll.direction === "up" || scroll.position <= props.revealOffset || scroll.position - scroll.inflectionPoint < 100);
			});
			const instance = {};
			$layout.instances.header = instance;
			if (props.modelValue) updateLayout("size", size.value);
			updateLayout("space", props.modelValue);
			updateLayout("offset", offset.value);
			(0, vue.onBeforeUnmount)(() => {
				if ($layout.instances.header === instance) {
					$layout.instances.header = void 0;
					updateLayout("size", 0);
					updateLayout("offset", 0);
					updateLayout("space", false);
				}
			});
			return () => {
				const child = hUniqueSlot(slots.default, []);
				if (props.elevated) child.push((0, vue.h)("div", { class: "q-layout__shadow absolute-full overflow-hidden no-pointer-events" }));
				child.push((0, vue.h)(QResizeObserver_default, {
					debounce: 0,
					onResize
				}));
				return (0, vue.h)("header", {
					class: classes.value,
					style: style.value,
					onFocusin
				}, child);
			};
		}
	});
	//#endregion
	//#region src/composables/private.use-ratio/use-ratio.js
	const useRatioProps = { ratio: [String, Number] };
	function useRatio(props, naturalRatio) {
		return (0, vue.computed)(() => {
			const rawValue = props.ratio || naturalRatio?.value;
			if (typeof rawValue === "string" && rawValue.trim() === "") return null;
			const ratio = Number(rawValue);
			return Number.isFinite(ratio) && ratio > 0 ? { paddingBottom: `${100 / ratio}%` } : null;
		});
	}
	//#endregion
	//#region src/components/img/QImg.js
	const defaultRatio = 1.7778;
	var QImg_default = createComponent({
		name: "QImg",
		props: {
			...useRatioProps,
			src: String,
			srcset: String,
			sizes: String,
			alt: String,
			crossorigin: String,
			decoding: String,
			referrerpolicy: String,
			draggable: Boolean,
			loading: {
				type: String,
				default: "lazy"
			},
			loadingShowDelay: {
				type: [Number, String],
				default: 0
			},
			fetchpriority: {
				type: String,
				default: "auto"
			},
			width: String,
			height: String,
			initialRatio: {
				type: [Number, String],
				default: defaultRatio
			},
			placeholderSrc: String,
			errorSrc: String,
			fit: {
				type: String,
				default: "cover"
			},
			position: {
				type: String,
				default: "50% 50%"
			},
			imgClass: String,
			imgStyle: Object,
			noSpinner: Boolean,
			noNativeMenu: Boolean,
			noTransition: Boolean,
			spinnerColor: String,
			spinnerSize: String
		},
		emits: ["load", "error"],
		setup(props, { slots, emit }) {
			const naturalRatio = (0, vue.ref)(props.initialRatio);
			const ratioStyle = useRatio(props, naturalRatio);
			const vm = (0, vue.getCurrentInstance)();
			const { registerTimeout: registerLoadTimeout, removeTimeout: removeLoadTimeout } = useTimeout();
			const { registerTimeout: registerLoadShowTimeout, removeTimeout: removeLoadShowTimeout } = useTimeout();
			const placeholderImg = (0, vue.computed)(() => props.placeholderSrc !== void 0 ? { src: props.placeholderSrc } : null);
			const errorImg = (0, vue.computed)(() => props.errorSrc !== void 0 ? {
				src: props.errorSrc,
				__qerror: true
			} : null);
			const images = [(0, vue.ref)(null), (0, vue.ref)(placeholderImg.value)];
			const position = (0, vue.ref)(0);
			const isLoading = (0, vue.ref)(false);
			const hasError = (0, vue.ref)(false);
			const classes = (0, vue.computed)(() => `q-img q-img--${props.noNativeMenu ? "no-" : ""}menu`);
			const style = (0, vue.computed)(() => ({
				width: props.width,
				height: props.height
			}));
			const imgClass = (0, vue.computed)(() => `q-img__image ${props.imgClass !== void 0 ? props.imgClass + " " : ""}q-img__image--with${props.noTransition ? "out" : ""}-transition q-img__image--`);
			const imgStyle = (0, vue.computed)(() => ({
				...props.imgStyle,
				objectFit: props.fit,
				objectPosition: props.position
			}));
			function setLoading() {
				removeLoadShowTimeout();
				if (props.loadingShowDelay === 0) {
					isLoading.value = true;
					return;
				}
				registerLoadShowTimeout(() => {
					isLoading.value = true;
				}, props.loadingShowDelay);
			}
			function clearLoading() {
				removeLoadShowTimeout();
				isLoading.value = false;
			}
			function onLoad({ target }) {
				if (vmIsDestroyed(vm)) return;
				removeLoadTimeout();
				naturalRatio.value = target.naturalHeight === 0 ? .5 : target.naturalWidth / target.naturalHeight;
				waitForCompleteness(target, 1);
			}
			function waitForCompleteness(target, count) {
				if (count === 1e3 || vmIsDestroyed(vm)) return;
				if (target.complete) onReady(target);
				else registerLoadTimeout(() => {
					waitForCompleteness(target, count + 1);
				}, 50);
			}
			function onReady(target) {
				if (vmIsDestroyed(vm)) return;
				position.value = position.value ^ 1;
				images[position.value].value = null;
				clearLoading();
				if (target.getAttribute("__qerror") !== "true") hasError.value = false;
				emit("load", target.currentSrc || target.src);
			}
			function onError(err) {
				removeLoadTimeout();
				clearLoading();
				hasError.value = true;
				images[position.value].value = errorImg.value;
				images[position.value ^ 1].value = placeholderImg.value;
				emit("error", err);
			}
			function getImage(index) {
				const img = images[index].value;
				const data = {
					key: "img_" + index,
					class: imgClass.value,
					style: imgStyle.value,
					alt: props.alt,
					crossorigin: props.crossorigin,
					decoding: props.decoding,
					referrerpolicy: props.referrerpolicy,
					height: props.height,
					width: props.width,
					loading: props.loading,
					fetchpriority: props.fetchpriority,
					"aria-hidden": "true",
					draggable: props.draggable,
					...img
				};
				if (position.value === index) Object.assign(data, {
					class: data.class + "current",
					onLoad,
					onError
				});
				else data.class += "loaded";
				return (0, vue.h)("div", {
					class: "q-img__container absolute-full",
					key: "img" + index
				}, (0, vue.h)("img", data));
			}
			function getContent() {
				if (!isLoading.value) return (0, vue.h)("div", {
					key: "content",
					class: "q-img__content absolute-full q-anchor--skip"
				}, hSlot(slots[hasError.value ? "error" : "default"]));
				return (0, vue.h)("div", {
					key: "loading",
					class: "q-img__loading absolute-full flex flex-center"
				}, slots.loading !== void 0 ? slots.loading() : props.noSpinner ? void 0 : [(0, vue.h)(QSpinner_default, {
					color: props.spinnerColor,
					size: props.spinnerSize
				})]);
			}
			{
				const watchSrc = () => {
					(0, vue.watch)(() => props.src || props.srcset || props.sizes ? {
						src: props.src,
						srcset: props.srcset,
						sizes: props.sizes
					} : null, (imgProps) => {
						removeLoadTimeout();
						hasError.value = false;
						if (imgProps === null) {
							clearLoading();
							images[position.value ^ 1].value = placeholderImg.value;
						} else setLoading();
						images[position.value].value = imgProps;
					}, { immediate: true });
				};
				if (isRuntimeSsrPreHydration.value) (0, vue.onMounted)(watchSrc);
				else watchSrc();
			}
			return () => {
				const content = [];
				if (ratioStyle.value !== null) content.push((0, vue.h)("div", {
					key: "filler",
					style: ratioStyle.value
				}));
				if (images[0].value !== null) content.push(getImage(0));
				if (images[1].value !== null) content.push(getImage(1));
				content.push((0, vue.h)(vue.Transition, { name: "q-transition--fade" }, getContent));
				return (0, vue.h)("div", {
					key: "main",
					class: classes.value,
					style: style.value,
					role: "img",
					"aria-label": props.alt
				}, content);
			};
		}
	});
	//#endregion
	//#region src/components/infinite-scroll/QInfiniteScroll.js
	const { passive: passive$3 } = listenOpts;
	var QInfiniteScroll_default = createComponent({
		name: "QInfiniteScroll",
		props: {
			offset: {
				type: Number,
				default: 500
			},
			debounce: {
				type: [String, Number],
				default: 100
			},
			scrollTarget: scrollTargetProp,
			initialIndex: {
				type: Number,
				default: 0
			},
			disable: Boolean,
			reverse: Boolean
		},
		emits: ["load"],
		setup(props, { slots, emit }) {
			const isFetching = (0, vue.ref)(false);
			const isWorking = (0, vue.ref)(true);
			const rootRef = (0, vue.ref)(null);
			const loadingRef = (0, vue.ref)(null);
			let index = props.initialIndex;
			let localScrollTarget, poll;
			const classes = (0, vue.computed)(() => "q-infinite-scroll__loading" + (isFetching.value ? "" : " invisible"));
			function immediatePoll() {
				if (props.disable || isFetching.value || !isWorking.value) return;
				const scrollHeight = getScrollHeight(localScrollTarget), scrollPosition = getVerticalScrollPosition(localScrollTarget), containerHeight = height(localScrollTarget);
				if (!props.reverse) {
					if (Math.round(scrollPosition + containerHeight + props.offset) >= Math.round(scrollHeight)) trigger();
				} else if (Math.round(scrollPosition) <= props.offset) trigger();
			}
			function trigger() {
				if (props.disable || isFetching.value || !isWorking.value) return;
				index++;
				isFetching.value = true;
				const heightBefore = getScrollHeight(localScrollTarget);
				emit("load", index, (isDone) => {
					if (isWorking.value) {
						isFetching.value = false;
						(0, vue.nextTick)(() => {
							if (props.reverse) {
								const heightAfter = getScrollHeight(localScrollTarget), scrollPosition = getVerticalScrollPosition(localScrollTarget), heightDifference = heightAfter - heightBefore;
								setVerticalScrollPosition(localScrollTarget, scrollPosition + heightDifference);
							}
							if (isDone === true) stop();
							else if (rootRef.value?.closest("body")) poll();
						});
					}
				});
			}
			function reset() {
				index = 0;
			}
			function resume() {
				if (!isWorking.value) {
					isWorking.value = true;
					localScrollTarget.addEventListener("scroll", poll, passive$3);
				}
				immediatePoll();
			}
			function stop() {
				if (isWorking.value) {
					isWorking.value = false;
					isFetching.value = false;
					localScrollTarget.removeEventListener("scroll", poll, passive$3);
					poll?.cancel?.();
				}
			}
			function updateScrollTarget() {
				if (localScrollTarget && isWorking.value) localScrollTarget.removeEventListener("scroll", poll, passive$3);
				localScrollTarget = getScrollTarget(rootRef.value, props.scrollTarget);
				if (isWorking.value) {
					localScrollTarget.addEventListener("scroll", poll, passive$3);
					if (props.reverse) {
						const scrollHeight = getScrollHeight(localScrollTarget), containerHeight = height(localScrollTarget);
						setVerticalScrollPosition(localScrollTarget, scrollHeight - containerHeight);
					}
					immediatePoll();
				}
			}
			function setIndex(newIndex) {
				index = newIndex;
			}
			function setDebounce(val) {
				val = Number.parseInt(val, 10);
				const oldPoll = poll;
				poll = val <= 0 ? immediatePoll : debounce(immediatePoll, Number.isNaN(val) ? 100 : val);
				if (localScrollTarget && isWorking.value) {
					if (oldPoll !== void 0) localScrollTarget.removeEventListener("scroll", oldPoll, passive$3);
					localScrollTarget.addEventListener("scroll", poll, passive$3);
				}
			}
			function updateSvgAnimations(isRetry) {
				if (renderLoadingSlot.value) {
					if (loadingRef.value === null) {
						if (!isRetry) (0, vue.nextTick)(() => {
							updateSvgAnimations(true);
						});
						return;
					}
					const action = `${isFetching.value ? "un" : ""}pauseAnimations`;
					[...loadingRef.value.getElementsByTagName("svg")].forEach((el) => {
						el[action]();
					});
				}
			}
			const renderLoadingSlot = (0, vue.computed)(() => !props.disable && isWorking.value);
			(0, vue.watch)([isFetching, renderLoadingSlot], () => {
				updateSvgAnimations();
			});
			(0, vue.watch)(() => props.disable, (val) => {
				if (val) stop();
				else resume();
			});
			(0, vue.watch)(() => props.reverse, () => {
				if (!isFetching.value && isWorking.value) immediatePoll();
			});
			(0, vue.watch)(() => props.scrollTarget, updateScrollTarget);
			(0, vue.watch)(() => props.debounce, setDebounce);
			let scrollPos = false;
			(0, vue.onActivated)(() => {
				if (scrollPos !== false && localScrollTarget) setVerticalScrollPosition(localScrollTarget, scrollPos);
			});
			(0, vue.onDeactivated)(() => {
				scrollPos = localScrollTarget ? getVerticalScrollPosition(localScrollTarget) : false;
			});
			(0, vue.onBeforeUnmount)(() => {
				if (isWorking.value) localScrollTarget.removeEventListener("scroll", poll, passive$3);
			});
			(0, vue.onMounted)(() => {
				setDebounce(props.debounce);
				updateScrollTarget();
				if (!isFetching.value) updateSvgAnimations();
			});
			const vm = (0, vue.getCurrentInstance)();
			Object.assign(vm.proxy, {
				poll: () => {
					poll?.();
				},
				trigger,
				stop,
				reset,
				resume,
				setIndex,
				updateScrollTarget
			});
			return () => {
				const child = hUniqueSlot(slots.default, []);
				if (renderLoadingSlot.value) child[props.reverse ? "unshift" : "push"]((0, vue.h)("div", {
					ref: loadingRef,
					class: classes.value
				}, hSlot(slots.loading)));
				return (0, vue.h)("div", {
					class: "q-infinite-scroll",
					ref: rootRef
				}, child);
			};
		}
	});
	//#endregion
	//#region src/components/inner-loading/QInnerLoading.js
	var QInnerLoading_default = createComponent({
		name: "QInnerLoading",
		props: {
			...useDarkProps,
			...useTransitionProps,
			showing: Boolean,
			color: String,
			size: {
				type: [String, Number],
				default: "42px"
			},
			label: String,
			labelClass: String,
			labelStyle: [
				String,
				Array,
				Object
			]
		},
		setup(props, { slots }) {
			const isDark = useDark(props, (0, vue.getCurrentInstance)().proxy.$q);
			const { transitionProps, transitionStyle } = useTransition(props);
			const classes = (0, vue.computed)(() => "q-inner-loading q--avoid-card-border absolute-full column flex-center" + (isDark.value ? " q-inner-loading--dark" : ""));
			const labelClass = (0, vue.computed)(() => "q-inner-loading__label" + (props.labelClass !== void 0 ? ` ${props.labelClass}` : ""));
			function getInner() {
				const child = [(0, vue.h)(QSpinner_default, {
					size: props.size,
					color: props.color
				})];
				if (props.label !== void 0) child.push((0, vue.h)("div", {
					class: labelClass.value,
					style: props.labelStyle
				}, [props.label]));
				return child;
			}
			function getContent() {
				return props.showing ? (0, vue.h)("div", {
					class: classes.value,
					style: transitionStyle.value
				}, slots.default !== void 0 ? slots.default() : getInner()) : null;
			}
			return () => (0, vue.h)(vue.Transition, transitionProps.value, getContent);
		}
	});
	//#endregion
	//#region src/components/input/use-mask.js
	const NAMED_MASKS = {
		date: "####/##/##",
		datetime: "####/##/## ##:##",
		time: "##:##",
		fulltime: "##:##:##",
		phone: "(###) ### - ####",
		card: "#### #### #### ####"
	};
	const { tokenMap: DEFAULT_TOKEN_MAP, tokenKeys: DEFAULT_TOKEN_MAP_KEYS } = getTokenMap({
		"#": {
			pattern: "[\\d]",
			negate: "[^\\d]"
		},
		S: {
			pattern: "[a-zA-Z]",
			negate: "[^a-zA-Z]"
		},
		N: {
			pattern: "[0-9a-zA-Z]",
			negate: "[^0-9a-zA-Z]"
		},
		A: {
			pattern: "[a-zA-Z]",
			negate: "[^a-zA-Z]",
			transform: (v) => v.toLocaleUpperCase()
		},
		a: {
			pattern: "[a-zA-Z]",
			negate: "[^a-zA-Z]",
			transform: (v) => v.toLocaleLowerCase()
		},
		X: {
			pattern: "[0-9a-zA-Z]",
			negate: "[^0-9a-zA-Z]",
			transform: (v) => v.toLocaleUpperCase()
		},
		x: {
			pattern: "[0-9a-zA-Z]",
			negate: "[^0-9a-zA-Z]",
			transform: (v) => v.toLocaleLowerCase()
		}
	});
	function getTokenMap(tokens) {
		const tokenKeys = Object.keys(tokens);
		const tokenMap = {};
		tokenKeys.forEach((key) => {
			const entry = tokens[key];
			tokenMap[key] = {
				...entry,
				regex: new RegExp(entry.pattern)
			};
		});
		return {
			tokenMap,
			tokenKeys
		};
	}
	function getTokenRegexMask(keys) {
		return new RegExp("\\\\([^.*+?^${}()|([\\]])|([.*+?^${}()|[\\]])|([" + keys.join("") + "])|(.)", "g");
	}
	const escRegex = /[.*+?^${}()|[\]\\]/g;
	const DEFAULT_TOKEN_REGEX_MASK = getTokenRegexMask(DEFAULT_TOKEN_MAP_KEYS);
	const MARKER = String.fromCodePoint(1);
	const useMaskProps = {
		mask: String,
		reverseFillMask: Boolean,
		fillMask: [Boolean, String],
		unmaskedValue: Boolean,
		maskTokens: Object
	};
	function useMask(props, emit, emitValue, inputRef) {
		let maskMarked, maskReplaced, computedMask, computedUnmask, pastedTextStart, selectionAnchor;
		const tokens = (0, vue.computed)(() => {
			if (props.maskTokens === void 0 || props.maskTokens === null) return {
				tokenMap: DEFAULT_TOKEN_MAP,
				tokenRegexMask: DEFAULT_TOKEN_REGEX_MASK
			};
			const { tokenMap: customTokens } = getTokenMap(props.maskTokens);
			const tokenMap = {
				...DEFAULT_TOKEN_MAP,
				...customTokens
			};
			return {
				tokenMap,
				tokenRegexMask: getTokenRegexMask(Object.keys(tokenMap))
			};
		});
		const hasMask = (0, vue.ref)(null);
		const innerValue = (0, vue.ref)(getInitialMaskedValue());
		function getIsTypeText() {
			return props.autogrow || [
				"textarea",
				"text",
				"search",
				"url",
				"tel",
				"password"
			].includes(props.type);
		}
		(0, vue.watch)(() => props.type + props.autogrow, updateMaskInternals);
		(0, vue.watch)(() => props.mask, (v) => {
			if (v !== void 0) updateMaskValue(innerValue.value, true);
			else {
				const val = unmaskValue(innerValue.value);
				updateMaskInternals();
				if (props.modelValue !== val) emit("update:modelValue", val);
			}
		});
		(0, vue.watch)(() => props.fillMask + props.reverseFillMask, () => {
			if (hasMask.value) updateMaskValue(innerValue.value, true);
		});
		(0, vue.watch)(() => props.unmaskedValue, () => {
			if (hasMask.value) updateMaskValue(innerValue.value);
		});
		(0, vue.watch)(() => props.maskTokens, () => {
			if (hasMask.value) updateMaskValue(innerValue.value, true);
		}, { deep: true });
		function getInitialMaskedValue() {
			updateMaskInternals();
			if (hasMask.value) {
				const masked = maskValue(unmaskValue(props.modelValue));
				return props.fillMask !== false ? fillWithMask(masked) : masked;
			}
			return props.modelValue;
		}
		function getPaddedMaskMarked(size) {
			if (size < maskMarked.length) return maskMarked.slice(-size);
			let pad = "", localMaskMarked = maskMarked;
			const padPos = localMaskMarked.indexOf(MARKER);
			if (padPos !== -1) {
				for (let i = size - localMaskMarked.length; i > 0; i--) pad += MARKER;
				localMaskMarked = localMaskMarked.slice(0, padPos) + pad + localMaskMarked.slice(padPos);
			}
			return localMaskMarked;
		}
		function updateMaskInternals() {
			hasMask.value = props.mask !== void 0 && props.mask.length !== 0 && getIsTypeText();
			if (!hasMask.value) {
				computedUnmask = void 0;
				maskMarked = "";
				maskReplaced = "";
				return;
			}
			const localComputedMask = NAMED_MASKS[props.mask] === void 0 ? props.mask : NAMED_MASKS[props.mask], fillChar = typeof props.fillMask === "string" && props.fillMask.length !== 0 ? props.fillMask.slice(0, 1) : "_", fillCharEscaped = fillChar.replace(escRegex, String.raw`\$&`), unmask = [], extract = [], mask = [];
			let firstMatch = props.reverseFillMask, unmaskChar = "", negateChar = "";
			localComputedMask.replace(tokens.value.tokenRegexMask, (_, char1, esc, token, char2) => {
				if (token !== void 0) {
					const c = tokens.value.tokenMap[token];
					mask.push(c);
					negateChar = c.negate;
					if (firstMatch) {
						extract.push("(?:" + negateChar + "+)?(" + c.pattern + "+)?(?:" + negateChar + "+)?(" + c.pattern + "+)?");
						firstMatch = false;
					}
					extract.push("(?:" + negateChar + "+)?(" + c.pattern + ")?");
					return;
				}
				if (esc !== void 0) {
					unmaskChar = "\\" + (esc === "\\" ? "" : esc);
					mask.push(esc);
				} else {
					const c = char1 !== void 0 ? char1 : char2;
					unmaskChar = c === "\\" ? String.raw`\\\\` : c.replace(escRegex, String.raw`\\$&`);
					mask.push(c);
				}
				unmask.push("([^" + unmaskChar + "]+)?" + unmaskChar + "?");
			});
			const unmaskMatcher = new RegExp("^" + unmask.join("") + "(" + (unmaskChar === "" ? "." : "[^" + unmaskChar + "]") + "+)?" + (unmaskChar === "" ? "" : "[" + unmaskChar + "]*") + "$"), extractLast = extract.length - 1, extractMatcher = extract.map((re, index) => {
				if (index === 0 && props.reverseFillMask) return new RegExp("^" + fillCharEscaped + "*" + re);
				else if (index === extractLast) return new RegExp("^" + re + "(" + (negateChar === "" ? "." : negateChar) + "+)?" + (props.reverseFillMask ? "$" : fillCharEscaped + "*"));
				return new RegExp("^" + re);
			});
			computedMask = mask;
			computedUnmask = (val) => {
				const unmaskMatch = unmaskMatcher.exec(props.reverseFillMask ? val : val.slice(0, mask.length + 1));
				if (unmaskMatch !== null) val = unmaskMatch.slice(1).join("");
				const extractMatch = [], extractMatcherLength = extractMatcher.length;
				for (let i = 0, str = val; i < extractMatcherLength; i++) {
					const m = extractMatcher[i].exec(str);
					if (m === null) break;
					str = str.slice(m.shift().length);
					extractMatch.push(...m);
				}
				if (extractMatch.length !== 0) return extractMatch.join("");
				return val;
			};
			maskMarked = mask.map((v) => typeof v === "string" ? v : MARKER).join("");
			maskReplaced = maskMarked.split(MARKER).join(fillChar);
		}
		function updateMaskValue(rawVal, updateMaskInternalsFlag, inputType) {
			const inp = inputRef.value, end = inp?.selectionEnd ?? 0, endReverse = inp === null ? 0 : inp.value.length - end, unmasked = unmaskValue(rawVal);
			if (updateMaskInternalsFlag === true) updateMaskInternals();
			const preMasked = maskValue(unmasked, updateMaskInternalsFlag), masked = props.fillMask !== false ? fillWithMask(preMasked) : preMasked, changed = innerValue.value !== masked;
			if (inp !== null && inp.value !== masked) inp.value = masked;
			if (changed) innerValue.value = masked;
			if (inp !== null && document.activeElement === inp) (0, vue.nextTick)(() => {
				if (masked === maskReplaced) {
					const cursor = props.reverseFillMask ? maskReplaced.length : 0;
					inp.setSelectionRange(cursor, cursor, "forward");
					return;
				}
				if (inputType === "insertFromPaste" && !props.reverseFillMask) {
					const maxEnd = inp.selectionEnd;
					let cursor = end - 1;
					for (let i = pastedTextStart; i <= cursor && i < maxEnd; i++) if (maskMarked[i] !== MARKER) cursor++;
					moveCursor.right(inp, cursor);
					return;
				}
				if (["deleteContentBackward", "deleteContentForward"].includes(inputType)) {
					const cursor = props.reverseFillMask ? end === 0 ? masked.length > preMasked.length ? 1 : 0 : Math.max(0, masked.length - (masked === maskReplaced ? 0 : Math.min(preMasked.length, endReverse) + 1)) + 1 : end;
					inp.setSelectionRange(cursor, cursor, "forward");
					return;
				}
				if (props.reverseFillMask) if (changed) {
					const cursor = Math.max(0, masked.length - (masked === maskReplaced ? 0 : Math.min(preMasked.length, endReverse + 1)));
					if (cursor === 1 && end === 1) inp.setSelectionRange(cursor, cursor, "forward");
					else moveCursor.rightReverse(inp, cursor);
				} else {
					const cursor = masked.length - endReverse;
					inp.setSelectionRange(cursor, cursor, "backward");
				}
				else if (changed) {
					const cursor = Math.max(0, maskMarked.indexOf(MARKER), Math.min(preMasked.length, end) - 1);
					moveCursor.right(inp, cursor);
				} else {
					const cursor = end - 1;
					moveCursor.right(inp, cursor);
				}
			});
			const val = props.unmaskedValue ? unmaskValue(masked) : masked;
			if (String(props.modelValue) !== val && (props.modelValue !== null || val !== "")) emitValue(val, true);
		}
		function moveCursorForPaste(inp, start, end) {
			const preMasked = maskValue(unmaskValue(inp.value));
			start = Math.max(0, maskMarked.indexOf(MARKER), Math.min(preMasked.length, start));
			pastedTextStart = start;
			inp.setSelectionRange(start, end, "forward");
		}
		const moveCursor = {
			left(inp, cursor) {
				const noMarkBefore = !maskMarked.slice(cursor - 1).includes(MARKER);
				let i = Math.max(0, cursor - 1);
				for (; i >= 0; i--) if (maskMarked[i] === MARKER) {
					cursor = i;
					if (noMarkBefore) cursor++;
					break;
				}
				if (i < 0 && maskMarked[cursor] !== void 0 && maskMarked[cursor] !== MARKER) return moveCursor.right(inp, 0);
				if (cursor >= 0) inp.setSelectionRange(cursor, cursor, "backward");
			},
			right(inp, cursor) {
				const limit = inp.value.length;
				let i = Math.min(limit, cursor + 1);
				for (; i <= limit; i++) if (maskMarked[i] === MARKER) {
					cursor = i;
					break;
				} else if (maskMarked[i - 1] === MARKER) cursor = i;
				if (i > limit && maskMarked[cursor - 1] !== void 0 && maskMarked[cursor - 1] !== MARKER) return moveCursor.left(inp, limit);
				inp.setSelectionRange(cursor, cursor, "forward");
			},
			leftReverse(inp, cursor) {
				const localMaskMarked = getPaddedMaskMarked(inp.value.length);
				let i = Math.max(0, cursor - 1);
				for (; i >= 0; i--) if (localMaskMarked[i - 1] === MARKER) {
					cursor = i;
					break;
				} else if (localMaskMarked[i] === MARKER) {
					cursor = i;
					if (i === 0) break;
				}
				if (i < 0 && localMaskMarked[cursor] !== void 0 && localMaskMarked[cursor] !== MARKER) return moveCursor.rightReverse(inp, 0);
				if (cursor >= 0) inp.setSelectionRange(cursor, cursor, "backward");
			},
			rightReverse(inp, cursor) {
				const limit = inp.value.length, localMaskMarked = getPaddedMaskMarked(limit), noMarkBefore = !localMaskMarked.slice(0, cursor + 1).includes(MARKER);
				let i = Math.min(limit, cursor + 1);
				for (; i <= limit; i++) if (localMaskMarked[i - 1] === MARKER) {
					cursor = i;
					if (cursor > 0 && noMarkBefore) cursor--;
					break;
				}
				if (i > limit && localMaskMarked[cursor - 1] !== void 0 && localMaskMarked[cursor - 1] !== MARKER) return moveCursor.leftReverse(inp, limit);
				inp.setSelectionRange(cursor, cursor, "forward");
			}
		};
		function onMaskedClick(e) {
			emit("click", e);
			selectionAnchor = void 0;
		}
		function onMaskedKeydown(e) {
			emit("keydown", e);
			if (shouldIgnoreKey(e) || e.altKey) return;
			const inp = inputRef.value, start = inp.selectionStart, end = inp.selectionEnd;
			if (!e.shiftKey) selectionAnchor = void 0;
			if (e.keyCode === 37 || e.keyCode === 39) {
				if (e.shiftKey && selectionAnchor === void 0) selectionAnchor = inp.selectionDirection === "forward" ? start : end;
				const fn = moveCursor[(e.keyCode === 39 ? "right" : "left") + (props.reverseFillMask ? "Reverse" : "")];
				e.preventDefault();
				fn(inp, selectionAnchor === start ? end : start);
				if (e.shiftKey) {
					const cursor = inp.selectionStart;
					inp.setSelectionRange(Math.min(selectionAnchor, cursor), Math.max(selectionAnchor, cursor), "forward");
				}
			} else if (e.keyCode === 8 && !props.reverseFillMask && start === end) {
				moveCursor.left(inp, start);
				inp.setSelectionRange(inp.selectionStart, end, "backward");
			} else if (e.keyCode === 46 && props.reverseFillMask && start === end) {
				moveCursor.rightReverse(inp, end);
				inp.setSelectionRange(start, inp.selectionEnd, "forward");
			}
		}
		function maskValue(val, updateMaskInternalsFlag) {
			if (val === void 0 || val === null || val === "") return "";
			if (props.reverseFillMask) return maskValueReverse(val, updateMaskInternalsFlag);
			const mask = computedMask;
			let valIndex = 0, output = "";
			for (let maskIndex = 0; maskIndex < mask.length; maskIndex++) {
				const valChar = val[valIndex], maskDef = mask[maskIndex];
				if (typeof maskDef === "string") {
					output += maskDef;
					if (updateMaskInternalsFlag === true && valChar === maskDef) valIndex++;
				} else if (valChar !== void 0 && maskDef.regex.test(valChar)) {
					output += maskDef.transform !== void 0 ? maskDef.transform(valChar) : valChar;
					valIndex++;
				} else return output;
			}
			return output;
		}
		function maskValueReverse(val, updateMaskInternalsFlag) {
			const mask = computedMask, firstTokenIndex = maskMarked.indexOf(MARKER);
			let valIndex = val.length - 1, output = "";
			for (let maskIndex = mask.length - 1; maskIndex >= 0 && valIndex !== -1; maskIndex--) {
				const maskDef = mask[maskIndex];
				let valChar = val[valIndex];
				if (typeof maskDef === "string") {
					output = maskDef + output;
					if (updateMaskInternalsFlag === true && valChar === maskDef) valIndex--;
				} else if (valChar !== void 0 && maskDef.regex.test(valChar)) do {
					output = (maskDef.transform !== void 0 ? maskDef.transform(valChar) : valChar) + output;
					valIndex--;
					valChar = val[valIndex];
				} while (firstTokenIndex === maskIndex && valChar !== void 0 && maskDef.regex.test(valChar));
				else return output;
			}
			return output;
		}
		function unmaskValue(val) {
			return typeof val !== "string" || computedUnmask === void 0 ? typeof val === "number" ? computedUnmask(String(val)) : val : computedUnmask(val);
		}
		function fillWithMask(val) {
			if (maskReplaced.length - val.length <= 0) return val;
			return props.reverseFillMask && val.length !== 0 ? maskReplaced.slice(0, -val.length) + val : val + maskReplaced.slice(val.length);
		}
		return {
			innerValue,
			hasMask,
			moveCursorForPaste,
			updateMaskValue,
			onMaskedKeydown,
			onMaskedClick
		};
	}
	//#endregion
	//#region src/composables/private.use-key-composition/use-key-composition.js
	const isJapanese = /[\u3000-\u303F\u3040-\u309F\u30A0-\u30FF\uFF00-\uFF9F\u4E00-\u9FAF\u3400-\u4DBF]/;
	const isChinese = /[\u4E00-\u9FFF\u3400-\u4DBF\u{20000}-\u{2A6DF}\u{2A700}-\u{2B73F}\u{2B740}-\u{2B81F}\u{2B820}-\u{2CEAF}\uF900-\uFAFF\u3300-\u33FF\uFE30-\uFE4F\uF900-\uFAFF\u{2F800}-\u{2FA1F}]/u;
	const isKorean = /[\u3131-\u314E\u314F-\u3163\uAC00-\uD7A3]/;
	const isPlainText = /[a-z0-9_ -]$/i;
	function useKeyComposition(onInput) {
		return function onComposition(e) {
			if (e.type === "compositionend" || e.type === "change") {
				if (!e.target.qComposing) return;
				e.target.qComposing = false;
				onInput(e);
			} else if (e.type === "compositionupdate" && !e.target.qComposing && typeof e.data === "string") {
				if (client.is.firefox ? !isPlainText.test(e.data) : isJapanese.test(e.data) || isChinese.test(e.data) || isKorean.test(e.data)) e.target.qComposing = true;
			}
		};
	}
	//#endregion
	//#region src/components/input/QInput.js
	var QInput_default = createComponent({
		name: "QInput",
		inheritAttrs: false,
		props: {
			...useFieldProps,
			...useMaskProps,
			...useFormProps,
			modelValue: [
				String,
				Number,
				FileList
			],
			modelModifiers: Object,
			shadowText: String,
			type: {
				type: String,
				default: "text"
			},
			debounce: [String, Number],
			autogrow: Boolean,
			inputClass: [
				Array,
				String,
				Object
			],
			inputStyle: [
				Array,
				String,
				Object
			]
		},
		emits: [
			...useFieldEmits,
			"paste",
			"change",
			"keydown",
			"click",
			"animationend"
		],
		setup(props, { emit, attrs }) {
			const { proxy } = (0, vue.getCurrentInstance)();
			const { $q } = proxy;
			const temp = {};
			let emitCachedValue = NaN, typedNumber = false, stopValueWatcher = false, emitTimer = null, emitValueFn;
			const inputRef = (0, vue.ref)(null);
			const nameProp = useFormInputNameAttr(props);
			const { innerValue, hasMask, moveCursorForPaste, updateMaskValue, onMaskedKeydown, onMaskedClick } = useMask(props, emit, emitValue, inputRef);
			const formDomProps = useFileDomProps(props, true);
			const hasValue = (0, vue.computed)(() => fieldValueIsFilled(innerValue.value));
			const onComposition = useKeyComposition(onInput);
			const state = useFieldState({ changeEvent: true });
			const isTextarea = (0, vue.computed)(() => props.type === "textarea" || props.autogrow);
			const isTypeText = (0, vue.computed)(() => isTextarea.value || [
				"text",
				"search",
				"url",
				"tel",
				"password"
			].includes(props.type));
			const onEvents = (0, vue.computed)(() => {
				const evt = {
					...state.splitAttrs.listeners.value,
					onInput,
					onPaste,
					onChange,
					onBlur: onFinishEditing,
					onFocus: stop
				};
				evt.onCompositionstart = evt.onCompositionupdate = evt.onCompositionend = onComposition;
				if (hasMask.value) {
					evt.onKeydown = onMaskedKeydown;
					evt.onClick = onMaskedClick;
				}
				if (props.autogrow) evt.onAnimationend = onAnimationend;
				return evt;
			});
			const inputAttrs = (0, vue.computed)(() => {
				const acc = {
					tabindex: 0,
					"data-autofocus": props.autofocus || void 0,
					rows: props.type === "textarea" ? 6 : void 0,
					"aria-label": props.label,
					name: nameProp.value,
					...state.splitAttrs.attributes.value,
					id: state.targetUid.value,
					maxlength: props.maxlength,
					disabled: props.disable,
					readonly: props.readonly
				};
				if (!isTextarea.value) acc.type = props.type;
				if (props.autogrow) acc.rows = 1;
				return acc;
			});
			(0, vue.watch)(() => props.type, () => {
				if (inputRef.value) inputRef.value.value = props.modelValue;
			});
			(0, vue.watch)(() => props.modelValue, (v) => {
				if (emitTimer !== null) {
					cancelPendingValueEmission();
					typedNumber = false;
					stopValueWatcher = false;
					delete temp.value;
				}
				if (hasMask.value) {
					if (stopValueWatcher) {
						stopValueWatcher = false;
						if (String(v) === emitCachedValue) return;
					}
					updateMaskValue(v);
				} else if (innerValue.value !== v) {
					innerValue.value = v;
					if (props.type === "number" && Object.hasOwn(temp, "value")) if (typedNumber) typedNumber = false;
					else delete temp.value;
					if (props.modelModifiers?.trim === true && Object.hasOwn(temp, "value") && (typeof temp.value !== "string" || temp.value.trim() !== v)) delete temp.value;
				}
				if (props.autogrow) (0, vue.nextTick)(adjustHeight);
			});
			(0, vue.watch)(() => props.autogrow, (val) => {
				if (val) (0, vue.nextTick)(adjustHeight);
				else if (inputRef.value !== null && attrs.rows > 0) inputRef.value.style.height = "auto";
			});
			(0, vue.watch)(() => props.dense, () => {
				if (props.autogrow) (0, vue.nextTick)(adjustHeight);
			});
			function focus() {
				addFocusFn(() => {
					const el = document.activeElement;
					if (inputRef.value !== null && inputRef.value !== el && (el === null || el.id !== state.targetUid.value)) inputRef.value.focus({ preventScroll: true });
				});
			}
			function select() {
				inputRef.value?.select();
			}
			function onPaste(e) {
				if (hasMask.value && props.reverseFillMask !== true) {
					const inp = e.target;
					moveCursorForPaste(inp, inp.selectionStart, inp.selectionEnd);
				}
				emit("paste", e);
			}
			function onInput(e) {
				if (!e || !e.target) return;
				if (props.type === "file") {
					emit("update:modelValue", e.target.files);
					return;
				}
				const val = e.target.value;
				if (e.target.qComposing) {
					temp.value = val;
					return;
				}
				if (hasMask.value) updateMaskValue(val, false, e.inputType);
				else {
					if (props.modelModifiers?.trim === true) temp.value = val;
					emitValue(val);
					if (isTypeText.value && e.target === document.activeElement) {
						const { selectionStart, selectionEnd } = e.target;
						if (selectionStart !== void 0 && selectionEnd !== void 0) (0, vue.nextTick)(() => {
							if (e.target === document.activeElement && val.indexOf(e.target.value) === 0) e.target.setSelectionRange(selectionStart, selectionEnd);
						});
					}
				}
				if (props.autogrow) adjustHeight();
			}
			function onAnimationend(e) {
				emit("animationend", e);
				adjustHeight();
			}
			function emitValue(val, stopWatcher) {
				emitValueFn = () => {
					emitTimer = null;
					if (props.type !== "number" && (props.modelModifiers?.trim !== true || hasMask.value) && Object.hasOwn(temp, "value")) delete temp.value;
					if (props.modelValue !== val && emitCachedValue !== val) {
						emitCachedValue = val;
						if (stopWatcher === true) stopValueWatcher = true;
						emit("update:modelValue", val);
						(0, vue.nextTick)(() => {
							if (emitCachedValue === val) emitCachedValue = NaN;
						});
					}
					emitValueFn = void 0;
				};
				if (props.type === "number") {
					typedNumber = true;
					temp.value = val;
				}
				if (props.debounce !== void 0) {
					if (emitTimer !== null) clearTimeout(emitTimer);
					temp.value = val;
					emitTimer = setTimeout(emitValueFn, props.debounce);
				} else emitValueFn();
			}
			function cancelPendingValueEmission() {
				if (emitTimer !== null) {
					clearTimeout(emitTimer);
					emitTimer = null;
				}
				emitValueFn = void 0;
			}
			function onClear() {
				cancelPendingValueEmission();
				typedNumber = false;
				stopValueWatcher = false;
				delete temp.value;
			}
			function adjustHeight() {
				requestAnimationFrame(() => {
					const inp = inputRef.value;
					if (inp !== null) {
						const parentStyle = inp.parentNode.style;
						const { scrollTop } = inp;
						const { overflowY, maxHeight } = $q.platform.is.firefox ? {} : window.getComputedStyle(inp);
						const changeOverflow = overflowY !== void 0 && overflowY !== "scroll";
						if (changeOverflow) inp.style.overflowY = "hidden";
						parentStyle.marginBottom = inp.scrollHeight - 1 + "px";
						inp.style.height = "1px";
						inp.style.height = inp.scrollHeight + "px";
						if (changeOverflow) inp.style.overflowY = Number.parseInt(maxHeight, 10) < inp.scrollHeight ? "auto" : "hidden";
						parentStyle.marginBottom = "";
						inp.scrollTop = scrollTop;
					}
				});
			}
			function onChange(e) {
				onComposition(e);
				if (emitTimer !== null) {
					clearTimeout(emitTimer);
					emitTimer = null;
				}
				emitValueFn?.();
				emit("change", e.target.value);
			}
			function onFinishEditing(e) {
				if (e !== void 0) stop(e);
				if (emitTimer !== null) {
					clearTimeout(emitTimer);
					emitTimer = null;
				}
				emitValueFn?.();
				typedNumber = false;
				stopValueWatcher = false;
				delete temp.value;
				if (props.type !== "file") setTimeout(() => {
					if (inputRef.value !== null) inputRef.value.value = innerValue.value !== void 0 ? innerValue.value : "";
				}, 0);
			}
			function getCurValue() {
				return Object.hasOwn(temp, "value") ? temp.value : innerValue.value !== void 0 ? innerValue.value : "";
			}
			(0, vue.onBeforeUnmount)(() => {
				onFinishEditing();
			});
			(0, vue.onMounted)(() => {
				if (props.autogrow) adjustHeight();
			});
			Object.assign(state, {
				innerValue,
				fieldClass: (0, vue.computed)(() => `q-${isTextarea.value ? "textarea" : "input"}` + (props.autogrow ? " q-textarea--autogrow" : "")),
				hasShadow: (0, vue.computed)(() => props.type !== "file" && typeof props.shadowText === "string" && props.shadowText.length !== 0),
				inputRef,
				emitValue,
				onClear,
				hasValue,
				floatingLabel: (0, vue.computed)(() => hasValue.value && (props.type !== "number" || Number.isFinite(Number(innerValue.value))) || fieldValueIsFilled(props.displayValue)),
				getControl: () => (0, vue.h)(isTextarea.value ? "textarea" : "input", {
					ref: inputRef,
					class: ["q-field__native q-placeholder", props.inputClass],
					style: props.inputStyle,
					...inputAttrs.value,
					...onEvents.value,
					...props.type !== "file" ? { value: getCurValue() } : formDomProps.value
				}),
				getShadowControl: () => (0, vue.h)("div", { class: "q-field__native q-field__shadow absolute-bottom no-pointer-events" + (isTextarea.value ? "" : " text-no-wrap") }, [(0, vue.h)("span", { class: "invisible" }, getCurValue()), (0, vue.h)("span", props.shadowText)])
			});
			const renderFn = useField(state);
			Object.assign(proxy, {
				focus,
				select,
				getNativeElement: () => inputRef.value
			});
			injectProp(proxy, "nativeEl", () => inputRef.value);
			return renderFn;
		}
	});
	//#endregion
	//#region src/directives/intersection/Intersection.js
	const defaultCfg$1 = {
		threshold: 0,
		root: null,
		rootMargin: "0px"
	};
	function update$3(el, ctx, value) {
		let handler, cfg, changed;
		if (typeof value === "function") {
			handler = value;
			cfg = defaultCfg$1;
			changed = ctx.cfg === void 0;
		} else {
			handler = value.handler;
			cfg = {
				...defaultCfg$1,
				...value.cfg
			};
			changed = ctx.cfg === void 0 || !isDeepEqual(ctx.cfg, cfg);
		}
		if (ctx.handler !== handler) ctx.handler = handler;
		if (changed) {
			ctx.cfg = cfg;
			ctx.observer?.disconnect();
			ctx.observer = new IntersectionObserver(([entry]) => {
				if (typeof ctx.handler === "function") {
					if (entry.rootBounds === null && document.body.contains(el)) {
						ctx.observer.unobserve(el);
						ctx.observer.observe(el);
						return;
					}
					if (ctx.handler(entry, ctx.observer) === false || ctx.once && entry.isIntersecting) destroy$1(el);
				}
			}, cfg);
			ctx.observer.observe(el);
		}
	}
	function destroy$1(el) {
		const ctx = el.__qvisible;
		if (ctx !== void 0) {
			ctx.observer?.disconnect();
			delete el.__qvisible;
		}
	}
	var Intersection_default = createDirective({
		name: "intersection",
		mounted(el, { modifiers, value }) {
			const ctx = { once: modifiers.once === true };
			update$3(el, ctx, value);
			el.__qvisible = ctx;
		},
		updated(el, binding) {
			const ctx = el.__qvisible;
			if (ctx !== void 0) update$3(el, ctx, binding.value);
		},
		beforeUnmount: destroy$1
	});
	//#endregion
	//#region src/components/intersection/QIntersection.js
	var QIntersection_default = createComponent({
		name: "QIntersection",
		props: {
			tag: {
				type: String,
				default: "div"
			},
			once: Boolean,
			transition: String,
			transitionDuration: {
				type: [String, Number],
				default: 300
			},
			ssrPrerender: Boolean,
			margin: String,
			threshold: [Number, Array],
			root: { default: null },
			disable: Boolean,
			onVisibility: Function
		},
		setup(props, { slots, emit }) {
			const showing = (0, vue.ref)(isRuntimeSsrPreHydration.value ? props.ssrPrerender : false);
			const intersectionProps = (0, vue.computed)(() => props.root !== void 0 || props.margin !== void 0 || props.threshold !== void 0 ? {
				handler: trigger,
				cfg: {
					root: props.root,
					rootMargin: props.margin,
					threshold: props.threshold
				}
			} : trigger);
			const hasDirective = (0, vue.computed)(() => !props.disable && (!isRuntimeSsrPreHydration.value || !props.once || !props.ssrPrerender));
			const directives = (0, vue.computed)(() => [[
				Intersection_default,
				intersectionProps.value,
				void 0,
				{ once: props.once }
			]]);
			const transitionStyle = (0, vue.computed)(() => `--q-transition-duration: ${props.transitionDuration}ms`);
			function trigger(entry) {
				if (showing.value !== entry.isIntersecting) {
					showing.value = entry.isIntersecting;
					if (props.onVisibility !== void 0) emit("visibility", showing.value);
				}
			}
			function getContent() {
				if (showing.value) return [(0, vue.h)("div", {
					key: "content",
					style: transitionStyle.value
				}, hSlot(slots.default))];
				if (slots.hidden !== void 0) return [(0, vue.h)("div", {
					key: "hidden",
					style: transitionStyle.value
				}, slots.hidden())];
			}
			return () => {
				const child = props.transition ? [(0, vue.h)(vue.Transition, { name: "q-transition--" + props.transition }, getContent)] : getContent();
				return hDir(props.tag, { class: "q-intersection" }, child, "main", hasDirective.value, () => directives.value);
			};
		}
	});
	//#endregion
	//#region src/components/item/QList.js
	const roleAttrExceptions = ["ul", "ol"];
	var QList_default = createComponent({
		name: "QList",
		props: {
			...useDarkProps,
			bordered: Boolean,
			dense: Boolean,
			separator: Boolean,
			padding: Boolean,
			tag: {
				type: String,
				default: "div"
			}
		},
		setup(props, { slots }) {
			const isDark = useDark(props, (0, vue.getCurrentInstance)().proxy.$q);
			const role = (0, vue.computed)(() => roleAttrExceptions.includes(props.tag) ? null : "list");
			const classes = (0, vue.computed)(() => "q-list" + (props.bordered ? " q-list--bordered" : "") + (props.dense ? " q-list--dense" : "") + (props.separator ? " q-list--separator" : "") + (isDark.value ? " q-list--dark" : "") + (props.padding ? " q-list--padding" : ""));
			return () => (0, vue.h)(props.tag, {
				class: classes.value,
				role: role.value
			}, hSlot(slots.default));
		}
	});
	//#endregion
	//#region src/components/knob/QKnob.js
	const keyCodes$1 = [
		34,
		37,
		40,
		33,
		39,
		38
	];
	const commonPropsName = Object.keys(useCircularCommonProps);
	var QKnob_default = createComponent({
		name: "QKnob",
		props: {
			...useFormProps,
			...useCircularCommonProps,
			modelValue: {
				type: Number,
				required: true
			},
			innerMin: Number,
			innerMax: Number,
			step: {
				type: Number,
				default: 1,
				validator: (v) => v >= 0
			},
			tabindex: {
				type: [Number, String],
				default: 0
			},
			disable: Boolean,
			readonly: Boolean
		},
		emits: [
			"update:modelValue",
			"change",
			"dragValue"
		],
		setup(props, { slots, emit }) {
			const { proxy } = (0, vue.getCurrentInstance)();
			const { $q } = proxy;
			const model = (0, vue.ref)(props.modelValue);
			const dragging = (0, vue.ref)(false);
			const innerMin = (0, vue.computed)(() => !Number.isFinite(props.innerMin) || props.innerMin < props.min ? props.min : props.innerMin);
			const innerMax = (0, vue.computed)(() => !Number.isFinite(props.innerMax) || props.innerMax > props.max ? props.max : props.innerMax);
			let centerPosition;
			function normalizeModel() {
				model.value = props.modelValue === null ? innerMin.value : between(props.modelValue, innerMin.value, innerMax.value);
				updateValue(true);
			}
			(0, vue.watch)(() => `${props.modelValue}|${innerMin.value}|${innerMax.value}`, normalizeModel);
			normalizeModel();
			const editable = (0, vue.computed)(() => !props.disable && !props.readonly);
			const classes = (0, vue.computed)(() => "q-knob non-selectable" + (editable.value ? " q-knob--editable" : props.disable ? " disabled" : ""));
			const decimals = (0, vue.computed)(() => (String(props.step).trim().split(".")[1] || "").length);
			const step = (0, vue.computed)(() => props.step === 0 ? 1 : props.step);
			const instantFeedback = (0, vue.computed)(() => props.instantFeedback || dragging.value);
			const onEvents = $q.platform.is.mobile ? (0, vue.computed)(() => editable.value ? { onClick } : {}) : (0, vue.computed)(() => editable.value ? {
				onMousedown,
				onClick,
				onKeydown,
				onKeyup
			} : {});
			const attrs = (0, vue.computed)(() => editable.value ? { tabindex: props.tabindex } : { [`aria-${props.disable ? "disabled" : "readonly"}`]: "true" });
			const circularProps = (0, vue.computed)(() => {
				const agg = {};
				commonPropsName.forEach((name) => {
					agg[name] = props[name];
				});
				return agg;
			});
			function pan(event) {
				if (event.isFinal) {
					updatePosition(event.evt, true);
					dragging.value = false;
					return;
				}
				if (event.isFirst) {
					updateCenterPosition();
					dragging.value = true;
				}
				updatePosition(event.evt, false);
			}
			const directives = (0, vue.computed)(() => [[
				TouchPan_default,
				pan,
				void 0,
				{
					prevent: true,
					stop: true,
					mouse: true
				}
			]]);
			function updateCenterPosition() {
				const { top, left, width, height } = proxy.$el.getBoundingClientRect();
				centerPosition = {
					top: top + height / 2,
					left: left + width / 2
				};
			}
			function onMousedown(evt) {
				updateCenterPosition();
				updatePosition(evt, false);
			}
			function onClick(evt) {
				updateCenterPosition();
				updatePosition(evt, true);
			}
			function onKeydown(evt) {
				if (!keyCodes$1.includes(evt.keyCode)) return;
				stopAndPrevent(evt);
				const stepVal = ([34, 33].includes(evt.keyCode) ? 10 : 1) * step.value, offset = [
					34,
					37,
					40
				].includes(evt.keyCode) ? -stepVal : stepVal;
				model.value = between(Number.parseFloat((model.value + offset).toFixed(decimals.value)), innerMin.value, innerMax.value);
				updateValue(false);
			}
			function updatePosition(evt, change) {
				const pos = position(evt), height = Math.abs(pos.top - centerPosition.top), distance = Math.hypot(height, pos.left - centerPosition.left);
				let angle = Math.asin(height / distance) * (180 / Math.PI);
				if (pos.top < centerPosition.top) angle = centerPosition.left < pos.left ? 90 - angle : 270 + angle;
				else angle = centerPosition.left < pos.left ? angle + 90 : 270 - angle;
				if ($q.lang.rtl) angle = normalizeToInterval(-angle - props.angle, 0, 360);
				else if (props.angle) angle = normalizeToInterval(angle - props.angle, 0, 360);
				if (props.reverse) angle = 360 - angle;
				let newModel = props.min + angle / 360 * (props.max - props.min);
				if (step.value !== 0) {
					const modulo = newModel % step.value;
					newModel = newModel - modulo + (Math.abs(modulo) >= step.value / 2 ? (modulo < 0 ? -1 : 1) * step.value : 0);
					newModel = Number.parseFloat(newModel.toFixed(decimals.value));
				}
				newModel = between(newModel, innerMin.value, innerMax.value);
				emit("dragValue", newModel);
				if (model.value !== newModel) model.value = newModel;
				updateValue(change);
			}
			function onKeyup(evt) {
				if (keyCodes$1.includes(evt.keyCode)) updateValue(true);
			}
			function updateValue(change) {
				if (props.modelValue !== model.value) emit("update:modelValue", model.value);
				if (change) emit("change", model.value);
			}
			const formAttrs = useFormAttrs(props);
			function getNameInput() {
				return (0, vue.h)("input", formAttrs.value);
			}
			return () => {
				const data = {
					class: classes.value,
					role: "slider",
					"aria-valuemin": innerMin.value,
					"aria-valuemax": innerMax.value,
					"aria-valuenow": props.modelValue,
					...attrs.value,
					...circularProps.value,
					value: model.value,
					instantFeedback: instantFeedback.value,
					...onEvents.value
				};
				const child = { default: slots.default };
				if (editable.value && props.name !== void 0) child.internal = getNameInput;
				return hDir(QCircularProgress_default, data, child, "knob", editable.value, () => directives.value);
			};
		}
	});
	//#endregion
	//#region src/components/scroll-observer/QScrollObserver.js
	const { passive: passive$2 } = listenOpts;
	const axisValues = [
		"both",
		"horizontal",
		"vertical"
	];
	var QScrollObserver_default = createComponent({
		name: "QScrollObserver",
		props: {
			axis: {
				type: String,
				validator: (v) => axisValues.includes(v),
				default: "vertical"
			},
			debounce: [String, Number],
			scrollTarget: scrollTargetProp
		},
		emits: ["scroll"],
		setup(props, { emit }) {
			const scroll = {
				position: {
					top: 0,
					left: 0
				},
				direction: "down",
				directionChanged: false,
				delta: {
					top: 0,
					left: 0
				},
				inflectionPoint: {
					top: 0,
					left: 0
				}
			};
			let clearTimer = null, localScrollTarget, parentEl;
			(0, vue.watch)(() => props.scrollTarget, () => {
				unconfigureScrollTarget();
				configureScrollTarget();
			});
			function emitEvent() {
				clearTimer?.();
				const top = Math.max(0, getVerticalScrollPosition(localScrollTarget));
				const left = getHorizontalScrollPosition(localScrollTarget);
				const delta = {
					top: top - scroll.position.top,
					left: left - scroll.position.left
				};
				if (props.axis === "vertical" && delta.top === 0 || props.axis === "horizontal" && delta.left === 0) return;
				const curDir = Math.abs(delta.top) >= Math.abs(delta.left) ? delta.top < 0 ? "up" : "down" : delta.left < 0 ? "left" : "right";
				scroll.position = {
					top,
					left
				};
				scroll.directionChanged = scroll.direction !== curDir;
				scroll.delta = delta;
				if (scroll.directionChanged) {
					scroll.direction = curDir;
					scroll.inflectionPoint = scroll.position;
				}
				emit("scroll", { ...scroll });
			}
			function configureScrollTarget() {
				localScrollTarget = getScrollTarget(parentEl, props.scrollTarget);
				localScrollTarget.addEventListener("scroll", trigger, passive$2);
				trigger(true);
			}
			function unconfigureScrollTarget() {
				if (localScrollTarget !== void 0) {
					localScrollTarget.removeEventListener("scroll", trigger, passive$2);
					localScrollTarget = void 0;
				}
			}
			function trigger(immediately) {
				if (immediately === true || props.debounce === 0 || props.debounce === "0") emitEvent();
				else if (clearTimer === null) {
					const [timer, fn] = props.debounce ? [setTimeout(emitEvent, props.debounce), clearTimeout] : [requestAnimationFrame(emitEvent), cancelAnimationFrame];
					clearTimer = () => {
						fn(timer);
						clearTimer = null;
					};
				}
			}
			const { proxy } = (0, vue.getCurrentInstance)();
			(0, vue.watch)(() => proxy.$q.lang.rtl, emitEvent);
			(0, vue.onMounted)(() => {
				parentEl = proxy.$el.parentNode;
				configureScrollTarget();
			});
			(0, vue.onBeforeUnmount)(() => {
				clearTimer?.();
				unconfigureScrollTarget();
			});
			Object.assign(proxy, {
				trigger,
				getPosition: () => scroll
			});
			return noop;
		}
	});
	//#endregion
	//#region src/components/layout/QLayout.js
	const viewRE = /^(h|l)h(h|r) lpr (f|l)f(f|r)$/;
	var QLayout_default = createComponent({
		name: "QLayout",
		props: {
			container: Boolean,
			view: {
				type: String,
				default: "hhh lpr fff",
				validator: (v) => viewRE.test(v.toLowerCase())
			},
			onScroll: Function,
			onScrollHeight: Function,
			onResize: Function
		},
		setup(props, { slots, emit }) {
			const { proxy: { $q } } = (0, vue.getCurrentInstance)();
			const rootRef = (0, vue.ref)(null);
			const height = (0, vue.ref)($q.screen.height);
			const width = (0, vue.ref)(props.container ? 0 : $q.screen.width);
			const scroll = (0, vue.ref)({
				position: 0,
				direction: "down",
				inflectionPoint: 0
			});
			const containerHeight = (0, vue.ref)(0);
			const scrollbarWidth = (0, vue.ref)(isRuntimeSsrPreHydration.value ? 0 : getScrollbarWidth());
			const classes = (0, vue.computed)(() => "q-layout q-layout--" + (props.container ? "containerized" : "standard"));
			const style = (0, vue.computed)(() => props.container ? null : { minHeight: $q.screen.height + "px" });
			const targetStyle = (0, vue.computed)(() => scrollbarWidth.value !== 0 ? { [$q.lang.rtl ? "left" : "right"]: `${scrollbarWidth.value}px` } : null);
			const targetChildStyle = (0, vue.computed)(() => scrollbarWidth.value !== 0 ? {
				[$q.lang.rtl ? "right" : "left"]: 0,
				[$q.lang.rtl ? "left" : "right"]: `-${scrollbarWidth.value}px`,
				width: `calc(100% + ${scrollbarWidth.value}px)`
			} : null);
			function onPageScroll(data) {
				if (props.container || !document.qScrollPrevented) {
					const info = {
						position: data.position.top,
						direction: data.direction,
						directionChanged: data.directionChanged,
						inflectionPoint: data.inflectionPoint.top,
						delta: data.delta.top
					};
					scroll.value = info;
					if (props.onScroll !== void 0) emit("scroll", info);
				}
			}
			function onPageResize(data) {
				const { height: newHeight, width: newWidth } = data;
				let resized = false;
				if (height.value !== newHeight) {
					resized = true;
					height.value = newHeight;
					if (props.onScrollHeight !== void 0) emit("scrollHeight", newHeight);
					updateScrollbarWidth();
				}
				if (width.value !== newWidth) {
					resized = true;
					width.value = newWidth;
				}
				if (resized && props.onResize !== void 0) emit("resize", data);
			}
			function onContainerResize({ height: newHeight }) {
				if (containerHeight.value !== newHeight) {
					containerHeight.value = newHeight;
					updateScrollbarWidth();
				}
			}
			function updateScrollbarWidth() {
				if (props.container) {
					const newWidth = height.value > containerHeight.value ? getScrollbarWidth() : 0;
					if (scrollbarWidth.value !== newWidth) scrollbarWidth.value = newWidth;
				}
			}
			let animateTimer = null;
			const $layout = {
				instances: {},
				view: (0, vue.computed)(() => props.view),
				isContainer: (0, vue.computed)(() => props.container),
				rootRef,
				height,
				containerHeight,
				scrollbarWidth,
				totalWidth: (0, vue.computed)(() => width.value + scrollbarWidth.value),
				rows: (0, vue.computed)(() => {
					const rows = props.view.toLowerCase().split(" ");
					return {
						top: [...rows[0]],
						middle: [...rows[1]],
						bottom: [...rows[2]]
					};
				}),
				header: (0, vue.reactive)({
					size: 0,
					offset: 0,
					space: false
				}),
				right: (0, vue.reactive)({
					size: 300,
					offset: 0,
					space: false
				}),
				footer: (0, vue.reactive)({
					size: 0,
					offset: 0,
					space: false
				}),
				left: (0, vue.reactive)({
					size: 300,
					offset: 0,
					space: false
				}),
				scroll,
				animate() {
					if (animateTimer !== null) clearTimeout(animateTimer);
					else document.body.classList.add("q-body--layout-animate");
					animateTimer = setTimeout(() => {
						animateTimer = null;
						document.body.classList.remove("q-body--layout-animate");
					}, 155);
				},
				update(part, prop, val) {
					$layout[part][prop] = val;
				}
			};
			(0, vue.provide)(layoutKey, $layout);
			if (getScrollbarWidth() > 0) {
				let timer = null;
				const el = document.body;
				const restoreScrollbar = () => {
					timer = null;
					el.classList.remove("hide-scrollbar");
				};
				const hideScrollbar = () => {
					if (timer === null) {
						if (el.scrollHeight > $q.screen.height) return;
						el.classList.add("hide-scrollbar");
					} else clearTimeout(timer);
					timer = setTimeout(restoreScrollbar, 300);
				};
				const updateScrollEvent = (action) => {
					if (timer !== null && action === "remove") {
						clearTimeout(timer);
						restoreScrollbar();
					}
					window[`${action}EventListener`]("resize", hideScrollbar);
				};
				(0, vue.watch)(() => props.container ? "remove" : "add", updateScrollEvent);
				if (!props.container) updateScrollEvent("add");
				(0, vue.onUnmounted)(() => {
					updateScrollEvent("remove");
				});
			}
			return () => {
				const content = hMergeSlot(slots.default, [(0, vue.h)(QScrollObserver_default, { onScroll: onPageScroll }), (0, vue.h)(QResizeObserver_default, { onResize: onPageResize })]);
				const layout = (0, vue.h)("div", {
					class: classes.value,
					style: style.value,
					ref: props.container ? void 0 : rootRef,
					tabindex: -1
				}, content);
				if (props.container) return (0, vue.h)("div", {
					class: "q-layout-container overflow-hidden",
					ref: rootRef
				}, [(0, vue.h)(QResizeObserver_default, { onResize: onContainerResize }), (0, vue.h)("div", {
					class: "absolute-full",
					style: targetStyle.value
				}, [(0, vue.h)("div", {
					class: "scroll",
					style: targetChildStyle.value
				}, [layout])])]);
				return layout;
			};
		}
	});
	//#endregion
	//#region src/components/linear-progress/QLinearProgress.js
	const defaultSizes = {
		xs: 2,
		sm: 4,
		md: 6,
		lg: 10,
		xl: 14
	};
	function width(val, reverse, $q) {
		return { transform: reverse ? `translateX(${$q.lang.rtl ? "-" : ""}100%) scale3d(${-val},1,1)` : `scale3d(${val},1,1)` };
	}
	var QLinearProgress_default = createComponent({
		name: "QLinearProgress",
		props: {
			...useDarkProps,
			...useSizeProps,
			value: {
				type: Number,
				default: 0
			},
			buffer: Number,
			color: String,
			trackColor: String,
			reverse: Boolean,
			stripe: Boolean,
			indeterminate: Boolean,
			query: Boolean,
			rounded: Boolean,
			animationSpeed: {
				type: [String, Number],
				default: 2100
			},
			instantFeedback: Boolean
		},
		setup(props, { slots }) {
			const { proxy } = (0, vue.getCurrentInstance)();
			const isDark = useDark(props, proxy.$q);
			const sizeStyle = useSize(props, defaultSizes);
			const motion = (0, vue.computed)(() => props.indeterminate || props.query);
			const widthReverse = (0, vue.computed)(() => props.reverse !== props.query);
			const style = (0, vue.computed)(() => ({
				...sizeStyle.value !== null ? sizeStyle.value : {},
				"--q-linear-progress-speed": `${props.animationSpeed}ms`
			}));
			const classes = (0, vue.computed)(() => "q-linear-progress" + (props.color !== void 0 ? ` text-${props.color}` : "") + (props.reverse || props.query ? " q-linear-progress--reverse" : "") + (props.rounded ? " rounded-borders" : ""));
			const trackStyle = (0, vue.computed)(() => width(props.buffer !== void 0 ? props.buffer : 1, widthReverse.value, proxy.$q));
			const transitionSuffix = (0, vue.computed)(() => `with${props.instantFeedback ? "out" : ""}-transition`);
			const trackClass = (0, vue.computed)(() => `q-linear-progress__track absolute-full q-linear-progress__track--${transitionSuffix.value} q-linear-progress__track--${isDark.value ? "dark" : "light"}` + (props.trackColor !== void 0 ? ` bg-${props.trackColor}` : ""));
			const modelStyle = (0, vue.computed)(() => width(motion.value ? 1 : props.value, widthReverse.value, proxy.$q));
			const modelClass = (0, vue.computed)(() => `q-linear-progress__model absolute-full q-linear-progress__model--${transitionSuffix.value} q-linear-progress__model--${motion.value ? "in" : ""}determinate`);
			const stripeStyle = (0, vue.computed)(() => ({ width: `${props.value * 100}%` }));
			const stripeClass = (0, vue.computed)(() => `q-linear-progress__stripe absolute-${props.reverse ? "right" : "left"} q-linear-progress__stripe--${transitionSuffix.value}`);
			return () => {
				const child = [(0, vue.h)("div", {
					class: trackClass.value,
					style: trackStyle.value
				}), (0, vue.h)("div", {
					class: modelClass.value,
					style: modelStyle.value
				})];
				if (props.stripe && !motion.value) child.push((0, vue.h)("div", {
					class: stripeClass.value,
					style: stripeStyle.value
				}));
				return (0, vue.h)("div", {
					class: classes.value,
					style: style.value,
					role: "progressbar",
					"aria-valuemin": 0,
					"aria-valuemax": 1,
					"aria-valuenow": props.indeterminate ? void 0 : props.value
				}, hMergeSlot(slots.default, child));
			};
		}
	});
	//#endregion
	//#region src/components/markup-table/QMarkupTable.js
	const separatorValues = [
		"horizontal",
		"vertical",
		"cell",
		"none"
	];
	var QMarkupTable_default = createComponent({
		name: "QMarkupTable",
		props: {
			...useDarkProps,
			dense: Boolean,
			flat: Boolean,
			bordered: Boolean,
			square: Boolean,
			wrapCells: Boolean,
			separator: {
				type: String,
				default: "horizontal",
				validator: (v) => separatorValues.includes(v)
			}
		},
		setup(props, { slots }) {
			const isDark = useDark(props, (0, vue.getCurrentInstance)().proxy.$q);
			const classes = (0, vue.computed)(() => `q-markup-table q-table__container q-table__card q-table--${props.separator}-separator` + (isDark.value ? " q-table--dark q-table__card--dark q-dark" : "") + (props.dense ? " q-table--dense" : "") + (props.flat ? " q-table--flat" : "") + (props.bordered ? " q-table--bordered" : "") + (props.square ? " q-table--square" : "") + (props.wrapCells ? "" : " q-table--no-wrap"));
			return () => (0, vue.h)("div", { class: classes.value }, [(0, vue.h)("table", { class: "q-table" }, hSlot(slots.default))]);
		}
	});
	//#endregion
	//#region src/components/no-ssr/QNoSsr.js
	var QNoSsr_default = createComponent({
		name: "QNoSsr",
		props: {
			tag: {
				type: String,
				default: "div"
			},
			placeholder: String
		},
		setup(props, { slots }) {
			const { isHydrated } = useHydration();
			return () => {
				if (isHydrated.value) {
					const node = hSlot(slots.default);
					return node === void 0 ? node : node.length > 1 ? (0, vue.h)(props.tag, {}, node) : node[0];
				}
				const data = { class: "q-no-ssr-placeholder" };
				const node = hSlot(slots.placeholder);
				if (node !== void 0) return node.length > 1 ? (0, vue.h)(props.tag, data, node) : node[0];
				if (props.placeholder !== void 0) return (0, vue.h)(props.tag, data, props.placeholder);
			};
		}
	});
	//#endregion
	//#region src/components/radio/QRadio.js
	const createSvg = () => (0, vue.h)("svg", {
		key: "svg",
		class: "q-radio__bg absolute non-selectable",
		viewBox: "0 0 24 24"
	}, [(0, vue.h)("path", { d: "M12,22a10,10 0 0 1 -10,-10a10,10 0 0 1 10,-10a10,10 0 0 1 10,10a10,10 0 0 1 -10,10m0,-22a12,12 0 0 0 -12,12a12,12 0 0 0 12,12a12,12 0 0 0 12,-12a12,12 0 0 0 -12,-12" }), (0, vue.h)("path", {
		class: "q-radio__check",
		d: "M12,6a6,6 0 0 0 -6,6a6,6 0 0 0 6,6a6,6 0 0 0 6,-6a6,6 0 0 0 -6,-6"
	})]);
	function onKeydown(e) {
		if (e.keyCode === 13 || e.keyCode === 32) stopAndPrevent(e);
	}
	var QRadio_default = createComponent({
		name: "QRadio",
		props: {
			...useDarkProps,
			...useSizeProps,
			...useFormProps,
			modelValue: { required: true },
			val: { required: true },
			label: String,
			leftLabel: Boolean,
			checkedIcon: String,
			uncheckedIcon: String,
			color: String,
			keepColor: Boolean,
			dense: Boolean,
			disable: Boolean,
			tabindex: [String, Number]
		},
		emits: ["update:modelValue"],
		setup(props, { slots, emit }) {
			const { proxy } = (0, vue.getCurrentInstance)();
			const isDark = useDark(props, proxy.$q);
			const sizeStyle = useSize(props, option_sizes_default);
			const rootRef = (0, vue.ref)(null);
			const { refocusTargetEl, refocusTarget } = useRefocusTarget(props, rootRef);
			const isTrue = (0, vue.computed)(() => (0, vue.toRaw)(props.modelValue) === (0, vue.toRaw)(props.val));
			const classes = (0, vue.computed)(() => "q-radio cursor-pointer no-outline row inline no-wrap items-center" + (props.disable ? " disabled" : "") + (isDark.value ? " q-radio--dark" : "") + (props.dense ? " q-radio--dense" : "") + (props.leftLabel ? " reverse" : ""));
			const innerClass = (0, vue.computed)(() => {
				const color = props.color !== void 0 && (props.keepColor || isTrue.value) ? ` text-${props.color}` : "";
				return `q-radio__inner relative-position q-radio__inner--${isTrue.value ? "truthy" : "falsy"}${color}`;
			});
			const icon = (0, vue.computed)(() => (isTrue.value ? props.checkedIcon : props.uncheckedIcon) || null);
			const tabindex = (0, vue.computed)(() => props.disable ? -1 : props.tabindex || 0);
			const injectFormInput = useFormInject((0, vue.computed)(() => {
				const prop = { type: "radio" };
				if (props.name !== void 0) Object.assign(prop, {
					".checked": isTrue.value,
					"^checked": isTrue.value ? "checked" : void 0,
					name: props.name,
					value: props.val
				});
				return prop;
			}));
			function onClick(e) {
				if (e !== void 0) {
					stopAndPrevent(e);
					refocusTarget(e);
				}
				if (!props.disable && !isTrue.value) emit("update:modelValue", props.val, e);
			}
			function onKeyup(e) {
				if (e.keyCode === 13 || e.keyCode === 32) onClick(e);
			}
			Object.assign(proxy, { set: onClick });
			const svg = createSvg();
			return () => {
				const content = icon.value !== null ? [(0, vue.h)("div", {
					key: "icon",
					class: "q-radio__icon-container absolute-full flex flex-center no-wrap"
				}, [(0, vue.h)(QIcon_default, {
					class: "q-radio__icon",
					name: icon.value
				})])] : [svg];
				if (!props.disable) injectFormInput(content, "unshift", " q-radio__native q-ma-none q-pa-none");
				const child = [(0, vue.h)("div", {
					class: innerClass.value,
					style: sizeStyle.value,
					"aria-hidden": "true"
				}, content)];
				if (refocusTargetEl.value !== null) child.push(refocusTargetEl.value);
				const label = props.label !== void 0 ? hMergeSlot(slots.default, [props.label]) : hSlot(slots.default);
				if (label !== void 0) child.push((0, vue.h)("div", { class: "q-radio__label q-anchor--skip" }, label));
				return (0, vue.h)("div", {
					ref: rootRef,
					class: classes.value,
					tabindex: tabindex.value,
					role: "radio",
					"aria-label": props.label,
					"aria-checked": isTrue.value ? "true" : "false",
					"aria-disabled": props.disable ? "true" : void 0,
					onClick,
					onKeydown,
					onKeyup
				}, child);
			};
		}
	});
	//#endregion
	//#region src/components/toggle/QToggle.js
	var QToggle_default = createComponent({
		name: "QToggle",
		props: {
			...useCheckboxProps,
			icon: String,
			iconColor: String
		},
		emits: useCheckboxEmits,
		setup(props) {
			function getInner(isTrue, isIndeterminate) {
				const icon = (0, vue.computed)(() => (isTrue.value ? props.checkedIcon : isIndeterminate.value ? props.indeterminateIcon : props.uncheckedIcon) || props.icon);
				const color = (0, vue.computed)(() => isTrue.value ? props.iconColor : null);
				return () => [(0, vue.h)("div", { class: "q-toggle__track" }), (0, vue.h)("div", { class: "q-toggle__thumb absolute flex flex-center no-wrap" }, icon.value !== void 0 ? [(0, vue.h)(QIcon_default, {
					name: icon.value,
					color: color.value
				})] : void 0)];
			}
			return useCheckbox("toggle", getInner);
		}
	});
	//#endregion
	//#region src/components/option-group/QOptionGroup.js
	const components = {
		radio: QRadio_default,
		checkbox: QCheckbox_default,
		toggle: QToggle_default
	};
	const typeValues = Object.keys(components);
	function getPropValueFn$1(userPropName, defaultPropName) {
		if (typeof userPropName === "function") return userPropName;
		const propName = userPropName !== void 0 ? userPropName : defaultPropName;
		return (opt) => opt[propName];
	}
	var QOptionGroup_default = createComponent({
		name: "QOptionGroup",
		props: {
			...useDarkProps,
			modelValue: { required: true },
			options: {
				type: Array,
				validator: (opts) => opts.every(isObject),
				default: () => []
			},
			optionValue: [Function, String],
			optionLabel: [Function, String],
			optionDisable: [Function, String],
			name: String,
			type: {
				type: String,
				default: "radio",
				validator: (v) => typeValues.includes(v)
			},
			color: String,
			keepColor: Boolean,
			dense: Boolean,
			size: String,
			leftLabel: Boolean,
			inline: Boolean,
			disable: Boolean
		},
		emits: ["update:modelValue"],
		setup(props, { emit, slots }) {
			const { proxy: { $q } } = (0, vue.getCurrentInstance)();
			const arrayModel = Array.isArray(props.modelValue);
			if (props.type === "radio") {
				if (arrayModel) console.error("q-option-group: model should not be array");
			} else if (!arrayModel) console.error("q-option-group: model should be array in your case");
			const isDark = useDark(props, $q);
			const component = (0, vue.computed)(() => components[props.type]);
			const getOptionValue = (0, vue.computed)(() => getPropValueFn$1(props.optionValue, "value"));
			const getOptionLabel = (0, vue.computed)(() => getPropValueFn$1(props.optionLabel, "label"));
			const getOptionDisable = (0, vue.computed)(() => getPropValueFn$1(props.optionDisable, "disable"));
			const innerOptions = (0, vue.computed)(() => props.options.map((opt) => ({
				val: getOptionValue.value(opt),
				name: opt.name === void 0 ? props.name : opt.name,
				disable: props.disable || getOptionDisable.value(opt),
				leftLabel: opt.leftLabel === void 0 ? props.leftLabel : opt.leftLabel,
				color: opt.color === void 0 ? props.color : opt.color,
				checkedIcon: opt.checkedIcon,
				uncheckedIcon: opt.uncheckedIcon,
				dark: opt.dark === void 0 ? isDark.value : opt.dark,
				size: opt.size === void 0 ? props.size : opt.size,
				dense: props.dense,
				keepColor: opt.keepColor === void 0 ? props.keepColor : opt.keepColor
			})));
			const classes = (0, vue.computed)(() => "q-option-group q-gutter-x-sm" + (props.inline ? " q-option-group--inline" : ""));
			const attrs = (0, vue.computed)(() => {
				const acc = { role: "group" };
				if (props.type === "radio") {
					acc.role = "radiogroup";
					if (props.disable) acc["aria-disabled"] = "true";
				}
				return acc;
			});
			function onUpdateModelValue(value) {
				emit("update:modelValue", value);
			}
			return () => (0, vue.h)("div", {
				class: classes.value,
				...attrs.value
			}, props.options.map((opt, i) => {
				const child = slots["label-" + i] !== void 0 ? () => slots["label-" + i](opt) : slots.label !== void 0 ? () => slots.label(opt) : void 0;
				return (0, vue.h)("div", [(0, vue.h)(component.value, {
					label: child === void 0 ? getOptionLabel.value(opt) : null,
					modelValue: props.modelValue,
					"onUpdate:modelValue": onUpdateModelValue,
					...innerOptions.value[i]
				}, child)]);
			}));
		}
	});
	//#endregion
	//#region src/components/page/QPage.js
	var QPage_default = createComponent({
		name: "QPage",
		props: {
			padding: Boolean,
			styleFn: Function
		},
		setup(props, { slots }) {
			const { proxy: { $q } } = (0, vue.getCurrentInstance)();
			const $layout = (0, vue.inject)(layoutKey, emptyRenderFn);
			if ($layout === emptyRenderFn) {
				console.error("QPage needs to be a deep child of QLayout");
				return emptyRenderFn;
			}
			if ((0, vue.inject)("_q_pc_", emptyRenderFn) === emptyRenderFn) {
				console.error("QPage needs to be child of QPageContainer");
				return emptyRenderFn;
			}
			const style = (0, vue.computed)(() => {
				const offset = ($layout.header.space ? $layout.header.size : 0) + ($layout.footer.space ? $layout.footer.size : 0);
				if (typeof props.styleFn === "function") {
					const height = $layout.isContainer.value ? $layout.containerHeight.value : $q.screen.height;
					return props.styleFn(offset, height);
				}
				return { minHeight: $layout.isContainer.value ? $layout.containerHeight.value - offset + "px" : $q.screen.height === 0 ? offset !== 0 ? `calc(100vh - ${offset}px)` : "100vh" : $q.screen.height - offset + "px" };
			});
			const classes = (0, vue.computed)(() => `q-page${props.padding ? " q-layout-padding" : ""}`);
			return () => (0, vue.h)("main", {
				class: classes.value,
				style: style.value
			}, hSlot(slots.default));
		}
	});
	//#endregion
	//#region src/components/page/QPageContainer.js
	var QPageContainer_default = createComponent({
		name: "QPageContainer",
		setup(_, { slots }) {
			const { proxy: { $q } } = (0, vue.getCurrentInstance)();
			const $layout = (0, vue.inject)(layoutKey, emptyRenderFn);
			if ($layout === emptyRenderFn) {
				console.error("QPageContainer needs to be child of QLayout");
				return emptyRenderFn;
			}
			(0, vue.provide)(pageContainerKey, true);
			const style = (0, vue.computed)(() => {
				const css = {};
				if ($layout.header.space) css.paddingTop = `${$layout.header.size}px`;
				if ($layout.right.space) css[`padding${$q.lang.rtl ? "Left" : "Right"}`] = `${$layout.right.size}px`;
				if ($layout.footer.space) css.paddingBottom = `${$layout.footer.size}px`;
				if ($layout.left.space) css[`padding${$q.lang.rtl ? "Right" : "Left"}`] = `${$layout.left.size}px`;
				return css;
			});
			return () => (0, vue.h)("div", {
				class: "q-page-container",
				style: style.value
			}, hSlot(slots.default));
		}
	});
	//#endregion
	//#region src/components/page-sticky/use-page-sticky.js
	const usePageStickyProps = {
		position: {
			type: String,
			default: "bottom-right",
			validator: (v) => [
				"top-right",
				"top-left",
				"bottom-right",
				"bottom-left",
				"top",
				"right",
				"bottom",
				"left"
			].includes(v)
		},
		offset: {
			type: Array,
			validator: (v) => v.length === 2
		},
		expand: Boolean
	};
	function usePageSticky() {
		const { props, proxy: { $q } } = (0, vue.getCurrentInstance)();
		const $layout = (0, vue.inject)(layoutKey, emptyRenderFn);
		if ($layout === emptyRenderFn) {
			console.error("QPageSticky needs to be child of QLayout");
			return emptyRenderFn;
		}
		const attach = (0, vue.computed)(() => {
			const pos = props.position;
			return {
				top: pos.includes("top"),
				right: pos.includes("right"),
				bottom: pos.includes("bottom"),
				left: pos.includes("left"),
				vertical: pos === "top" || pos === "bottom",
				horizontal: pos === "left" || pos === "right"
			};
		});
		const top = (0, vue.computed)(() => $layout.header.offset);
		const right = (0, vue.computed)(() => $layout.right.offset);
		const bottom = (0, vue.computed)(() => $layout.footer.offset);
		const left = (0, vue.computed)(() => $layout.left.offset);
		const style = (0, vue.computed)(() => {
			let posX = 0, posY = 0;
			const side = attach.value;
			const dir = $q.lang.rtl ? -1 : 1;
			if (side.top && top.value !== 0) posY = `${top.value}px`;
			else if (side.bottom && bottom.value !== 0) posY = `${-bottom.value}px`;
			if (side.left && left.value !== 0) posX = `${dir * left.value}px`;
			else if (side.right && right.value !== 0) posX = `${-dir * right.value}px`;
			const css = { transform: `translate(${posX}, ${posY})` };
			if (props.offset) css.margin = `${props.offset[1]}px ${props.offset[0]}px`;
			if (side.vertical) {
				if (left.value !== 0) css[$q.lang.rtl ? "right" : "left"] = `${left.value}px`;
				if (right.value !== 0) css[$q.lang.rtl ? "left" : "right"] = `${right.value}px`;
			} else if (side.horizontal) {
				if (top.value !== 0) css.top = `${top.value}px`;
				if (bottom.value !== 0) css.bottom = `${bottom.value}px`;
			}
			return css;
		});
		const classes = (0, vue.computed)(() => `q-page-sticky row flex-center fixed-${props.position} q-page-sticky--${props.expand ? "expand" : "shrink"}`);
		function getStickyContent(slots) {
			const content = hSlot(slots.default);
			return (0, vue.h)("div", {
				class: classes.value,
				style: style.value
			}, props.expand ? content : [(0, vue.h)("div", content)]);
		}
		return {
			$layout,
			getStickyContent
		};
	}
	//#endregion
	//#region src/components/page-scroller/QPageScroller.js
	var QPageScroller_default = createComponent({
		name: "QPageScroller",
		props: {
			...usePageStickyProps,
			scrollOffset: {
				type: Number,
				default: 1e3
			},
			reverse: Boolean,
			duration: {
				type: Number,
				default: 300
			},
			offset: {
				...usePageStickyProps.offset,
				default: () => [18, 18]
			}
		},
		emits: ["click"],
		setup(props, { slots, emit }) {
			const { proxy: { $q } } = (0, vue.getCurrentInstance)();
			const { $layout, getStickyContent } = usePageSticky();
			const rootRef = (0, vue.ref)(null);
			let heightWatcher;
			const scrollHeight = (0, vue.computed)(() => $layout.height.value - ($layout.isContainer.value ? $layout.containerHeight.value : $q.screen.height));
			function isVisible() {
				return props.reverse ? scrollHeight.value - $layout.scroll.value.position > props.scrollOffset : $layout.scroll.value.position > props.scrollOffset;
			}
			const showing = (0, vue.ref)(isVisible());
			function updateVisibility() {
				const newVal = isVisible();
				if (showing.value !== newVal) showing.value = newVal;
			}
			function updateReverse() {
				if (props.reverse) {
					if (heightWatcher === void 0) heightWatcher = (0, vue.watch)(scrollHeight, updateVisibility);
				} else cleanup();
			}
			(0, vue.watch)($layout.scroll, updateVisibility);
			(0, vue.watch)(() => props.reverse, updateReverse);
			function cleanup() {
				if (heightWatcher !== void 0) {
					heightWatcher();
					heightWatcher = void 0;
				}
			}
			function onClick(e) {
				setVerticalScrollPosition(getScrollTarget($layout.isContainer.value ? rootRef.value : $layout.rootRef.value), props.reverse ? $layout.height.value : 0, props.duration);
				emit("click", e);
			}
			function getContent() {
				return showing.value ? (0, vue.h)("div", {
					ref: rootRef,
					class: "q-page-scroller",
					onClick
				}, getStickyContent(slots)) : null;
			}
			updateReverse();
			(0, vue.onBeforeUnmount)(cleanup);
			return () => (0, vue.h)(vue.Transition, { name: "q-transition--fade" }, getContent);
		}
	});
	//#endregion
	//#region src/components/page-sticky/QPageSticky.js
	var QPageSticky_default = createComponent({
		name: "QPageSticky",
		props: usePageStickyProps,
		setup(_, { slots }) {
			const { getStickyContent } = usePageSticky();
			return () => getStickyContent(slots);
		}
	});
	//#endregion
	//#region src/components/pagination/QPagination.js
	function getBool(val, otherwise) {
		return val === true || val === false ? val : otherwise;
	}
	var QPagination_default = createComponent({
		name: "QPagination",
		props: {
			...useDarkProps,
			modelValue: {
				type: Number,
				required: true
			},
			min: {
				type: [Number, String],
				default: 1
			},
			max: {
				type: [Number, String],
				required: true
			},
			maxPages: {
				type: [Number, String],
				default: 0,
				validator: (v) => (typeof v === "string" ? Number.parseInt(v, 10) : v) >= 0
			},
			inputStyle: [
				Array,
				String,
				Object
			],
			inputClass: [
				Array,
				String,
				Object
			],
			size: String,
			disable: Boolean,
			input: Boolean,
			iconPrev: String,
			iconNext: String,
			iconFirst: String,
			iconLast: String,
			toFn: Function,
			boundaryLinks: {
				type: Boolean,
				default: null
			},
			boundaryNumbers: {
				type: Boolean,
				default: null
			},
			directionLinks: {
				type: Boolean,
				default: null
			},
			ellipses: {
				type: Boolean,
				default: null
			},
			ripple: {
				type: [Boolean, Object],
				default: null
			},
			round: Boolean,
			rounded: Boolean,
			flat: Boolean,
			outline: Boolean,
			unelevated: Boolean,
			push: Boolean,
			glossy: Boolean,
			color: {
				type: String,
				default: "primary"
			},
			textColor: String,
			activeDesign: {
				type: String,
				default: "",
				values: (v) => v === "" || btnDesignOptions.includes(v)
			},
			activeColor: String,
			activeTextColor: String,
			gutter: String,
			padding: {
				type: String,
				default: "3px 2px"
			}
		},
		emits: ["update:modelValue"],
		setup(props, { emit }) {
			const { proxy } = (0, vue.getCurrentInstance)();
			const { $q } = proxy;
			const isDark = useDark(props, $q);
			const minProp = (0, vue.computed)(() => Number.parseInt(props.min, 10));
			const maxProp = (0, vue.computed)(() => Number.parseInt(props.max, 10));
			const maxPagesProp = (0, vue.computed)(() => Number.parseInt(props.maxPages, 10));
			const inputPlaceholder = (0, vue.computed)(() => model.value + " / " + maxProp.value);
			const boundaryLinksProp = (0, vue.computed)(() => getBool(props.boundaryLinks, props.input));
			const boundaryNumbersProp = (0, vue.computed)(() => getBool(props.boundaryNumbers, !props.input));
			const directionLinksProp = (0, vue.computed)(() => getBool(props.directionLinks, props.input));
			const ellipsesProp = (0, vue.computed)(() => getBool(props.ellipses, !props.input));
			const newPage = (0, vue.ref)(null);
			const model = (0, vue.computed)({
				get: () => props.modelValue,
				set: (val) => {
					val = Number.parseInt(val, 10);
					if (props.disable || !Number.isFinite(val)) return;
					const value = between(val, minProp.value, maxProp.value);
					if (props.modelValue !== value) emit("update:modelValue", value);
				}
			});
			(0, vue.watch)(() => `${minProp.value}|${maxProp.value}`, () => {
				model.value = props.modelValue;
			});
			const classes = (0, vue.computed)(() => "q-pagination row no-wrap items-center" + (props.disable ? " disabled" : ""));
			const gutterProp = (0, vue.computed)(() => props.gutter in btnPadding ? `${btnPadding[props.gutter]}px` : props.gutter || null);
			const gutterStyle = (0, vue.computed)(() => gutterProp.value !== null ? `--q-pagination-gutter-parent:-${gutterProp.value};--q-pagination-gutter-child:${gutterProp.value}` : null);
			const icons = (0, vue.computed)(() => {
				const ico = [
					props.iconFirst || $q.iconSet.pagination.first,
					props.iconPrev || $q.iconSet.pagination.prev,
					props.iconNext || $q.iconSet.pagination.next,
					props.iconLast || $q.iconSet.pagination.last
				];
				return $q.lang.rtl ? ico.reverse() : ico;
			});
			const attrs = (0, vue.computed)(() => ({
				"aria-disabled": props.disable ? "true" : "false",
				role: "navigation"
			}));
			const btnDesignProp = (0, vue.computed)(() => getBtnDesign(props, "flat"));
			const btnProps = (0, vue.computed)(() => ({
				[btnDesignProp.value]: true,
				round: props.round,
				rounded: props.rounded,
				padding: props.padding,
				color: props.color,
				textColor: props.textColor,
				size: props.size,
				ripple: props.ripple !== null ? props.ripple : true
			}));
			const btnActiveDesignProp = (0, vue.computed)(() => {
				const acc = { [btnDesignProp.value]: false };
				if (props.activeDesign !== "") acc[props.activeDesign] = true;
				return acc;
			});
			const activeBtnProps = (0, vue.computed)(() => ({
				...btnActiveDesignProp.value,
				color: props.activeColor || props.color,
				textColor: props.activeTextColor || props.textColor
			}));
			const btnConfig = (0, vue.computed)(() => {
				let maxPages = Math.max(maxPagesProp.value, 1 + (ellipsesProp.value ? 2 : 0) + (boundaryNumbersProp.value ? 2 : 0));
				const acc = {
					pgFrom: minProp.value,
					pgTo: maxProp.value,
					ellipsesStart: false,
					ellipsesEnd: false,
					boundaryStart: false,
					boundaryEnd: false,
					marginalStyle: { minWidth: `${Math.max(2, String(maxProp.value).length)}em` }
				};
				if (maxPagesProp.value && maxPages < maxProp.value - minProp.value + 1) {
					maxPages = 1 + Math.floor(maxPages / 2) * 2;
					acc.pgFrom = Math.max(minProp.value, Math.min(maxProp.value - maxPages + 1, props.modelValue - Math.floor(maxPages / 2)));
					acc.pgTo = Math.min(maxProp.value, acc.pgFrom + maxPages - 1);
					if (boundaryNumbersProp.value) {
						acc.boundaryStart = true;
						acc.pgFrom++;
					}
					if (ellipsesProp.value && acc.pgFrom > minProp.value + (boundaryNumbersProp.value ? 1 : 0)) {
						acc.ellipsesStart = true;
						acc.pgFrom++;
					}
					if (boundaryNumbersProp.value) {
						acc.boundaryEnd = true;
						acc.pgTo--;
					}
					if (ellipsesProp.value && acc.pgTo < maxProp.value - (boundaryNumbersProp.value ? 1 : 0)) {
						acc.ellipsesEnd = true;
						acc.pgTo--;
					}
				}
				return acc;
			});
			function set(value) {
				model.value = value;
			}
			function setByOffset(offset) {
				model.value = model.value + offset;
			}
			function updateModel() {
				model.value = newPage.value;
				newPage.value = null;
				if ($q.platform.is.mobile) document.activeElement.blur();
			}
			function onInputValue(val) {
				newPage.value = val;
			}
			function onKeyup(e) {
				if (isKeyCode(e, 13)) updateModel();
			}
			function getBtn(cfg, page, active) {
				const data = {
					"aria-label": page,
					"aria-current": "false",
					...btnProps.value,
					...cfg
				};
				if (active) Object.assign(data, {
					"aria-current": "true",
					...activeBtnProps.value
				});
				if (page !== void 0) if (props.toFn !== void 0) data.to = props.toFn(page);
				else data.onClick = () => {
					set(page);
				};
				return (0, vue.h)(QBtn_default, data);
			}
			Object.assign(proxy, {
				set,
				setByOffset
			});
			return () => {
				const contentStart = [];
				const contentEnd = [];
				let contentMiddle;
				if (boundaryLinksProp.value) {
					contentStart.push(getBtn({
						key: "bls",
						disable: props.disable || props.modelValue <= minProp.value,
						icon: icons.value[0],
						"aria-label": $q.lang.pagination.first
					}, minProp.value));
					contentEnd.unshift(getBtn({
						key: "ble",
						disable: props.disable || props.modelValue >= maxProp.value,
						icon: icons.value[3],
						"aria-label": $q.lang.pagination.last
					}, maxProp.value));
				}
				if (directionLinksProp.value) {
					contentStart.push(getBtn({
						key: "bdp",
						disable: props.disable || props.modelValue <= minProp.value,
						icon: icons.value[1],
						"aria-label": $q.lang.pagination.prev
					}, props.modelValue - 1));
					contentEnd.unshift(getBtn({
						key: "bdn",
						disable: props.disable || props.modelValue >= maxProp.value,
						icon: icons.value[2],
						"aria-label": $q.lang.pagination.next
					}, props.modelValue + 1));
				}
				if (!props.input) {
					contentMiddle = [];
					const { pgFrom, pgTo, marginalStyle: style } = btnConfig.value;
					if (btnConfig.value.boundaryStart) contentStart.push(getBtn({
						key: "bns",
						style,
						disable: props.disable,
						label: minProp.value
					}, minProp.value, minProp.value === props.modelValue));
					if (btnConfig.value.boundaryEnd) contentEnd.unshift(getBtn({
						key: "bne",
						style,
						disable: props.disable,
						label: maxProp.value
					}, maxProp.value, maxProp.value === props.modelValue));
					if (btnConfig.value.ellipsesStart) contentStart.push(getBtn({
						key: "bes",
						style,
						disable: props.disable,
						label: "…",
						ripple: false
					}, pgFrom - 1));
					if (btnConfig.value.ellipsesEnd) contentEnd.unshift(getBtn({
						key: "bee",
						style,
						disable: props.disable,
						label: "…",
						ripple: false
					}, pgTo + 1));
					for (let i = pgFrom; i <= pgTo; i++) contentMiddle.push(getBtn({
						key: `bpg${i}`,
						style,
						disable: props.disable,
						label: i
					}, i, i === props.modelValue));
				}
				return (0, vue.h)("div", {
					class: classes.value,
					...attrs.value
				}, [(0, vue.h)("div", {
					class: "q-pagination__content row no-wrap items-center",
					style: gutterStyle.value
				}, [
					...contentStart,
					props.input ? (0, vue.h)(QInput_default, {
						class: "inline",
						style: { width: `${inputPlaceholder.value.length / 1.5}em` },
						type: "number",
						dense: true,
						value: newPage.value,
						disable: props.disable,
						dark: isDark.value,
						borderless: true,
						inputClass: props.inputClass,
						inputStyle: props.inputStyle,
						placeholder: inputPlaceholder.value,
						min: minProp.value,
						max: maxProp.value,
						"onUpdate:modelValue": onInputValue,
						onKeyup,
						onBlur: updateModel
					}) : (0, vue.h)("div", { class: "q-pagination__middle row justify-center" }, contentMiddle),
					...contentEnd
				])]);
			};
		}
	});
	//#endregion
	//#region src/utils/frame-debounce/frame-debounce.js
	function frameDebounce(fn) {
		let frame = null;
		let callArgs = null;
		let context = null;
		function debounced(...args) {
			callArgs = args;
			context = this;
			if (frame !== null) return;
			frame = window.requestAnimationFrame(() => {
				fn.apply(context, callArgs);
				frame = null;
				callArgs = null;
				context = null;
			});
		}
		debounced.cancel = () => {
			if (frame !== null) {
				window.cancelAnimationFrame(frame);
				frame = null;
			}
			callArgs = null;
			context = null;
		};
		return debounced;
	}
	//#endregion
	//#region src/components/parallax/QParallax.js
	const { passive: passive$1 } = listenOpts;
	const mediaEvents = [
		"load",
		"loadstart",
		"loadedmetadata"
	];
	var QParallax_default = createComponent({
		name: "QParallax",
		props: {
			src: String,
			height: {
				type: Number,
				default: 500
			},
			speed: {
				type: Number,
				default: 1,
				validator: (v) => v >= 0 && v <= 1
			},
			scrollTarget: scrollTargetProp,
			onScroll: Function
		},
		setup(props, { slots, emit }) {
			const percentScrolled = (0, vue.ref)(0);
			const rootRef = (0, vue.ref)(null);
			const mediaParentRef = (0, vue.ref)(null);
			const mediaRef = (0, vue.ref)(null);
			let isWorking = false, mediaEl, mediaHeight, resizeHandler, observer, localScrollTarget;
			(0, vue.watch)(() => props.height, () => {
				if (isWorking) updatePos();
			});
			(0, vue.watch)(() => props.scrollTarget, () => {
				if (isWorking) {
					stop();
					start();
				}
			});
			let update = (percentage) => {
				percentScrolled.value = percentage;
				if (props.onScroll !== void 0) emit("scroll", percentage);
			};
			function updatePos() {
				let containerTop, containerHeight, containerBottom;
				if (localScrollTarget === window) {
					containerTop = 0;
					containerBottom = containerHeight = window.innerHeight;
				} else {
					containerTop = offset(localScrollTarget).top;
					containerHeight = height(localScrollTarget);
					containerBottom = containerTop + containerHeight;
				}
				const top = offset(rootRef.value).top;
				const bottom = top + props.height;
				if (observer !== void 0 || bottom > containerTop && top < containerBottom) {
					const percent = (containerBottom - top) / (props.height + containerHeight);
					setPos((mediaHeight - props.height) * percent * props.speed);
					update(percent);
				}
			}
			let setPos = (newOffset) => {
				mediaEl.style.transform = `translate3d(-50%,${Math.round(newOffset)}px,0)`;
			};
			function onResize() {
				mediaHeight = mediaEl.naturalHeight || mediaEl.videoHeight || height(mediaEl);
				if (isWorking) updatePos();
			}
			function start() {
				isWorking = true;
				localScrollTarget = getScrollTarget(rootRef.value, props.scrollTarget);
				localScrollTarget.addEventListener("scroll", updatePos, passive$1);
				window.addEventListener("resize", resizeHandler, passive$1);
				updatePos();
			}
			function stop() {
				if (isWorking) {
					isWorking = false;
					localScrollTarget.removeEventListener("scroll", updatePos, passive$1);
					window.removeEventListener("resize", resizeHandler, passive$1);
					localScrollTarget = void 0;
					setPos.cancel();
					update.cancel();
					resizeHandler.cancel();
				}
			}
			(0, vue.onMounted)(() => {
				setPos = frameDebounce(setPos);
				update = frameDebounce(update);
				resizeHandler = frameDebounce(onResize);
				mediaEl = slots.media !== void 0 ? mediaParentRef.value.children[0] : mediaRef.value;
				mediaEvents.forEach((evtName) => {
					mediaEl.addEventListener(evtName, onResize);
				});
				onResize();
				mediaEl.style.display = "initial";
				if (window.IntersectionObserver !== void 0) {
					observer = new IntersectionObserver((entries) => {
						(entries[0].isIntersecting ? start : stop)();
					});
					observer.observe(rootRef.value);
				} else start();
			});
			(0, vue.onBeforeUnmount)(() => {
				stop();
				observer?.disconnect();
				mediaEvents.forEach((evtName) => {
					mediaEl.removeEventListener(evtName, onResize);
				});
			});
			return () => (0, vue.h)("div", {
				ref: rootRef,
				class: "q-parallax",
				style: { height: `${props.height}px` }
			}, [(0, vue.h)("div", {
				ref: mediaParentRef,
				class: "q-parallax__media absolute-full"
			}, slots.media !== void 0 ? slots.media() : [(0, vue.h)("img", {
				ref: mediaRef,
				src: props.src
			})]), (0, vue.h)("div", { class: "q-parallax__content absolute-full column flex-center" }, slots.content !== void 0 ? slots.content({ percentScrolled: percentScrolled.value }) : hSlot(slots.default))]);
		}
	});
	//#endregion
	//#region src/utils/clone/clone.js
	function cloneDeep(data, hash = /* @__PURE__ */ new WeakMap()) {
		if (Object(data) !== data) return data;
		if (hash.has(data)) return hash.get(data);
		const result = data instanceof Date ? new Date(data) : data instanceof RegExp ? new RegExp(data.source, data.flags) : data instanceof Set ? /* @__PURE__ */ new Set() : data instanceof Map ? /* @__PURE__ */ new Map() : typeof data.constructor !== "function" ? Object.create(null) : data.prototype !== void 0 && typeof data.prototype.constructor === "function" ? data : new data.constructor();
		if (typeof data.constructor === "function" && typeof data.valueOf === "function") {
			const val = data.valueOf();
			if (Object(val) !== val) {
				const localResult = new data.constructor(val);
				hash.set(data, localResult);
				return localResult;
			}
		}
		hash.set(data, result);
		if (data instanceof Set) data.forEach((val) => {
			result.add(cloneDeep(val, hash));
		});
		else if (data instanceof Map) data.forEach((val, key) => {
			result.set(key, cloneDeep(val, hash));
		});
		return Object.assign(result, ...Object.keys(data).map((key) => ({ [key]: cloneDeep(data[key], hash) })));
	}
	//#endregion
	//#region src/components/popup-edit/QPopupEdit.js
	var QPopupEdit_default = createComponent({
		name: "QPopupEdit",
		props: {
			modelValue: { required: true },
			title: String,
			buttons: Boolean,
			labelSet: String,
			labelCancel: String,
			color: {
				type: String,
				default: "primary"
			},
			validate: {
				type: Function,
				default: () => true
			},
			autoSave: Boolean,
			cover: {
				type: Boolean,
				default: true
			},
			disable: Boolean
		},
		emits: [
			"update:modelValue",
			"save",
			"cancel",
			"beforeShow",
			"show",
			"beforeHide",
			"hide"
		],
		setup(props, { slots, emit }) {
			const { proxy } = (0, vue.getCurrentInstance)();
			const { $q } = proxy;
			const menuRef = (0, vue.ref)(null);
			const initialValue = (0, vue.ref)("");
			const currentModel = (0, vue.ref)("");
			let validated = false;
			const scope = (0, vue.computed)(() => injectProp({
				initialValue: initialValue.value,
				validate: props.validate,
				set,
				cancel,
				updatePosition
			}, "value", () => currentModel.value, (val) => {
				currentModel.value = val;
			}));
			function set() {
				if (!props.validate(currentModel.value)) return;
				if (hasModelChanged()) {
					emit("save", currentModel.value, initialValue.value);
					emit("update:modelValue", currentModel.value);
				}
				closeMenu();
			}
			function cancel() {
				if (hasModelChanged()) emit("cancel", currentModel.value, initialValue.value);
				closeMenu();
			}
			function updatePosition() {
				(0, vue.nextTick)(() => {
					menuRef.value.updatePosition();
				});
			}
			function hasModelChanged() {
				return !isDeepEqual(currentModel.value, initialValue.value);
			}
			function closeMenu() {
				validated = true;
				menuRef.value.hide();
			}
			function onBeforeShow() {
				validated = false;
				initialValue.value = cloneDeep(props.modelValue);
				currentModel.value = cloneDeep(props.modelValue);
				emit("beforeShow");
			}
			function onShow() {
				emit("show");
			}
			function onBeforeHide() {
				if (!validated && hasModelChanged()) if (props.autoSave && props.validate(currentModel.value)) {
					emit("save", currentModel.value, initialValue.value);
					emit("update:modelValue", currentModel.value);
				} else emit("cancel", currentModel.value, initialValue.value);
				emit("beforeHide");
			}
			function onHide() {
				emit("hide");
			}
			function getContent() {
				const child = slots.default !== void 0 ? [slots.default(scope.value)].flat() : [];
				if (props.title) child.unshift((0, vue.h)("div", { class: "q-dialog__title q-mt-sm q-mb-sm" }, props.title));
				if (props.buttons) child.push((0, vue.h)("div", { class: "q-popup-edit__buttons row justify-center no-wrap" }, [(0, vue.h)(QBtn_default, {
					flat: true,
					color: props.color,
					label: props.labelCancel || $q.lang.label.cancel,
					onClick: cancel
				}), (0, vue.h)(QBtn_default, {
					flat: true,
					color: props.color,
					label: props.labelSet || $q.lang.label.set,
					onClick: set
				})]));
				return child;
			}
			Object.assign(proxy, {
				set,
				cancel,
				show(e) {
					menuRef.value?.show(e);
				},
				hide(e) {
					menuRef.value?.hide(e);
				},
				updatePosition
			});
			return () => {
				if (props.disable) return;
				return (0, vue.h)(QMenu_default, {
					ref: menuRef,
					class: "q-popup-edit",
					cover: props.cover,
					onBeforeShow,
					onShow,
					onBeforeHide,
					onHide,
					onEscapeKey: cancel
				}, getContent);
			};
		}
	});
	//#endregion
	//#region src/components/popup-proxy/QPopupProxy.js
	var QPopupProxy_default = createComponent({
		name: "QPopupProxy",
		props: {
			...useAnchorProps,
			breakpoint: {
				type: [String, Number],
				default: 450
			}
		},
		emits: ["show", "hide"],
		setup(props, { slots, emit, attrs }) {
			const { proxy } = (0, vue.getCurrentInstance)();
			const { $q } = proxy;
			const showing = (0, vue.ref)(false);
			const popupRef = (0, vue.ref)(null);
			const breakpoint = (0, vue.computed)(() => Number.parseInt(props.breakpoint, 10));
			const { canShow } = useAnchor({
				showing,
				avoidEmit: true
			});
			function getType() {
				return $q.screen.width < breakpoint.value || $q.screen.height < breakpoint.value ? "dialog" : "menu";
			}
			const type = (0, vue.ref)(getType());
			const popupProps = (0, vue.computed)(() => type.value === "menu" ? { maxHeight: "99vh" } : {});
			(0, vue.watch)(() => getType(), (val) => {
				if (!showing.value) type.value = val;
			});
			function onShow(evt) {
				showing.value = true;
				emit("show", evt);
			}
			function onHide(evt) {
				showing.value = false;
				type.value = getType();
				emit("hide", evt);
			}
			Object.assign(proxy, {
				show(evt) {
					if (canShow(evt)) popupRef.value.show(evt);
				},
				hide(evt) {
					popupRef.value.hide(evt);
				},
				toggle(evt) {
					popupRef.value.toggle(evt);
				}
			});
			injectProp(proxy, "currentComponent", () => ({
				type: type.value,
				ref: popupRef.value
			}));
			return () => {
				const data = {
					ref: popupRef,
					...popupProps.value,
					...attrs,
					onShow,
					onHide
				};
				let component;
				if (type.value === "dialog") component = QDialog_default;
				else {
					component = QMenu_default;
					Object.assign(data, {
						target: props.target,
						contextMenu: props.contextMenu,
						noParentEvent: true,
						separateClosePopup: true
					});
				}
				return (0, vue.h)(component, data, slots.default);
			};
		}
	});
	//#endregion
	//#region src/components/pull-to-refresh/QPullToRefresh.js
	const PULLER_HEIGHT = 40;
	const OFFSET_TOP = 20;
	var QPullToRefresh_default = createComponent({
		name: "QPullToRefresh",
		props: {
			color: String,
			bgColor: String,
			icon: String,
			noMouse: Boolean,
			disable: Boolean,
			scrollTarget: scrollTargetProp
		},
		emits: ["refresh"],
		setup(props, { slots, emit }) {
			const { proxy } = (0, vue.getCurrentInstance)();
			const { $q } = proxy;
			const state = (0, vue.ref)("pull");
			const pullRatio = (0, vue.ref)(0);
			const pulling = (0, vue.ref)(false);
			const pullPosition = (0, vue.ref)(-40);
			const animating = (0, vue.ref)(false);
			const positionCSS = (0, vue.ref)({});
			const style = (0, vue.computed)(() => ({
				opacity: pullRatio.value,
				transform: `translateY(${pullPosition.value}px) rotate(${pullRatio.value * 360}deg)`
			}));
			const classes = (0, vue.computed)(() => "q-pull-to-refresh__puller row flex-center" + (animating.value ? " q-pull-to-refresh__puller--animating" : "") + (props.bgColor !== void 0 ? ` bg-${props.bgColor}` : ""));
			function pull(event) {
				if (event.isFinal) {
					if (pulling.value) {
						pulling.value = false;
						if (state.value === "pulled") {
							state.value = "refreshing";
							animateTo({ pos: OFFSET_TOP });
							trigger();
						} else if (state.value === "pull") animateTo({
							pos: -40,
							ratio: 0
						});
					}
					return;
				}
				if (animating.value || state.value === "refreshing") return false;
				if (event.isFirst) {
					if (getVerticalScrollPosition(localScrollTarget) !== 0 || event.direction !== "down") {
						if (pulling.value) {
							pulling.value = false;
							state.value = "pull";
							animateTo({
								pos: -40,
								ratio: 0
							});
						}
						return false;
					}
					pulling.value = true;
					const { top, left } = proxy.$el.getBoundingClientRect();
					positionCSS.value = {
						top: top + "px",
						left: left + "px",
						width: window.getComputedStyle(proxy.$el).getPropertyValue("width")
					};
				}
				prevent(event.evt);
				const distance = Math.min(140, Math.max(0, event.distance.y));
				pullPosition.value = distance - PULLER_HEIGHT;
				pullRatio.value = between(distance / 60, 0, 1);
				const newState = pullPosition.value > OFFSET_TOP ? "pulled" : "pull";
				if (state.value !== newState) state.value = newState;
			}
			const directives = (0, vue.computed)(() => {
				const modifiers = { down: true };
				if (!props.noMouse) modifiers.mouse = true;
				return [[
					TouchPan_default,
					pull,
					void 0,
					modifiers
				]];
			});
			const contentClass = (0, vue.computed)(() => `q-pull-to-refresh__content${pulling.value ? " no-pointer-events" : ""}`);
			function trigger() {
				emit("refresh", () => {
					animateTo({
						pos: -40,
						ratio: 0
					}, () => {
						state.value = "pull";
					});
				});
			}
			let localScrollTarget, timer = null;
			function animateTo({ pos, ratio }, done) {
				animating.value = true;
				pullPosition.value = pos;
				if (ratio !== void 0) pullRatio.value = ratio;
				if (timer !== null) clearTimeout(timer);
				timer = setTimeout(() => {
					timer = null;
					animating.value = false;
					done?.();
				}, 300);
			}
			function updateScrollTarget() {
				localScrollTarget = getScrollTarget(proxy.$el, props.scrollTarget);
			}
			(0, vue.watch)(() => props.scrollTarget, updateScrollTarget);
			(0, vue.onMounted)(updateScrollTarget);
			(0, vue.onBeforeUnmount)(() => {
				if (timer !== null) clearTimeout(timer);
			});
			Object.assign(proxy, {
				trigger,
				updateScrollTarget
			});
			return () => {
				return hDir("div", { class: "q-pull-to-refresh" }, [(0, vue.h)("div", { class: contentClass.value }, hSlot(slots.default)), (0, vue.h)("div", {
					class: "q-pull-to-refresh__puller-container fixed row flex-center no-pointer-events z-top",
					style: positionCSS.value
				}, [(0, vue.h)("div", {
					class: classes.value,
					style: style.value
				}, [state.value !== "refreshing" ? (0, vue.h)(QIcon_default, {
					name: props.icon || $q.iconSet.pullToRefresh.icon,
					color: props.color,
					size: "32px"
				}) : (0, vue.h)(QSpinner_default, {
					size: "24px",
					color: props.color
				})])])], "main", !props.disable, () => directives.value);
			};
		}
	});
	//#endregion
	//#region src/components/range/QRange.js
	const dragType = {
		MIN: 0,
		RANGE: 1,
		MAX: 2
	};
	var QRange_default = createComponent({
		name: "QRange",
		props: {
			...useSliderProps,
			modelValue: {
				type: Object,
				default: () => ({
					min: null,
					max: null
				}),
				validator: (v) => "min" in v && "max" in v
			},
			dragRange: Boolean,
			dragOnlyRange: Boolean,
			leftLabelColor: String,
			leftLabelTextColor: String,
			rightLabelColor: String,
			rightLabelTextColor: String,
			leftLabelValue: [String, Number],
			rightLabelValue: [String, Number],
			leftThumbColor: String,
			rightThumbColor: String
		},
		emits: useSliderEmits,
		setup(props, { emit }) {
			const { proxy: { $q } } = (0, vue.getCurrentInstance)();
			const { state, methods } = useSlider({
				updateValue,
				updatePosition,
				getDragging,
				formAttrs: (0, vue.computed)(() => ({
					type: "hidden",
					name: props.name,
					value: `${props.modelValue.min}|${props.modelValue.max}`
				}))
			});
			const rootRef = (0, vue.ref)(null);
			const curMinRatio = (0, vue.ref)(0);
			const curMaxRatio = (0, vue.ref)(0);
			const model = (0, vue.ref)({
				min: 0,
				max: 0
			});
			function normalizeModel() {
				model.value.min = props.modelValue.min === null ? state.innerMin.value : between(props.modelValue.min, state.innerMin.value, state.innerMax.value);
				model.value.max = props.modelValue.max === null ? state.innerMax.value : between(props.modelValue.max, state.innerMin.value, state.innerMax.value);
			}
			(0, vue.watch)(() => `${props.modelValue.min}|${props.modelValue.max}|${state.innerMin.value}|${state.innerMax.value}`, normalizeModel);
			normalizeModel();
			const modelMinRatio = (0, vue.computed)(() => methods.convertModelToRatio(model.value.min));
			const modelMaxRatio = (0, vue.computed)(() => methods.convertModelToRatio(model.value.max));
			const ratioMin = (0, vue.computed)(() => state.active.value ? curMinRatio.value : modelMinRatio.value);
			const ratioMax = (0, vue.computed)(() => state.active.value ? curMaxRatio.value : modelMaxRatio.value);
			const selectionBarStyle = (0, vue.computed)(() => {
				const acc = {
					[state.positionProp.value]: `${100 * ratioMin.value}%`,
					[state.sizeProp.value]: `${100 * (ratioMax.value - ratioMin.value)}%`
				};
				if (props.selectionImg !== void 0) acc.backgroundImage = `url(${props.selectionImg}) !important`;
				return acc;
			});
			const trackContainerEvents = (0, vue.computed)(() => {
				if (!state.editable.value) return {};
				if ($q.platform.is.mobile) return { onClick: methods.onMobileClick };
				const evt = { onMousedown: methods.onActivate };
				if (props.dragRange || props.dragOnlyRange) Object.assign(evt, {
					onFocus: () => {
						state.focus.value = "both";
					},
					onBlur: methods.onBlur,
					onKeydown,
					onKeyup: methods.onKeyup
				});
				return evt;
			});
			function getEvents(side) {
				return !$q.platform.is.mobile && state.editable.value && !props.dragOnlyRange ? {
					onFocus: () => {
						state.focus.value = side;
					},
					onBlur: methods.onBlur,
					onKeydown,
					onKeyup: methods.onKeyup
				} : {};
			}
			const thumbTabindex = (0, vue.computed)(() => props.dragOnlyRange ? null : state.tabindex.value);
			const trackContainerTabindex = (0, vue.computed)(() => !$q.platform.is.mobile && (props.dragRange || props.dragOnlyRange) ? state.tabindex.value : null);
			const minThumbRef = (0, vue.ref)(null);
			const minEvents = (0, vue.computed)(() => getEvents("min"));
			const getMinThumb = methods.getThumbRenderFn({
				focusValue: "min",
				getNodeData: () => ({
					ref: minThumbRef,
					key: "tmin",
					...minEvents.value,
					tabindex: thumbTabindex.value
				}),
				ratio: ratioMin,
				label: (0, vue.computed)(() => props.leftLabelValue !== void 0 ? props.leftLabelValue : model.value.min),
				thumbColor: (0, vue.computed)(() => props.leftThumbColor || props.thumbColor || props.color),
				labelColor: (0, vue.computed)(() => props.leftLabelColor || props.labelColor),
				labelTextColor: (0, vue.computed)(() => props.leftLabelTextColor || props.labelTextColor)
			});
			const maxEvents = (0, vue.computed)(() => getEvents("max"));
			const getMaxThumb = methods.getThumbRenderFn({
				injectFormInput: false,
				focusValue: "max",
				getNodeData: () => ({
					...maxEvents.value,
					key: "tmax",
					tabindex: thumbTabindex.value
				}),
				ratio: ratioMax,
				label: (0, vue.computed)(() => props.rightLabelValue !== void 0 ? props.rightLabelValue : model.value.max),
				thumbColor: (0, vue.computed)(() => props.rightThumbColor || props.thumbColor || props.color),
				labelColor: (0, vue.computed)(() => props.rightLabelColor || props.labelColor),
				labelTextColor: (0, vue.computed)(() => props.rightLabelTextColor || props.labelTextColor)
			});
			function updateValue(change) {
				if (model.value.min !== props.modelValue.min || model.value.max !== props.modelValue.max) emit("update:modelValue", { ...model.value });
				if (change) emit("change", { ...model.value });
			}
			function getDragging(event) {
				const { left, top, width, height } = rootRef.value.getBoundingClientRect(), sensitivity = props.dragOnlyRange ? 0 : props.vertical ? minThumbRef.value.offsetHeight / (2 * height) : minThumbRef.value.offsetWidth / (2 * width);
				const dragging = {
					left,
					top,
					width,
					height,
					valueMin: model.value.min,
					valueMax: model.value.max,
					ratioMin: modelMinRatio.value,
					ratioMax: modelMaxRatio.value
				};
				const ratio = methods.getDraggingRatio(event, dragging);
				if (!props.dragOnlyRange && ratio < dragging.ratioMin + sensitivity) dragging.type = dragType.MIN;
				else if (props.dragOnlyRange || ratio < dragging.ratioMax - sensitivity) if (props.dragRange || props.dragOnlyRange) {
					dragging.type = dragType.RANGE;
					Object.assign(dragging, {
						offsetRatio: ratio,
						offsetModel: methods.convertRatioToModel(ratio),
						rangeValue: dragging.valueMax - dragging.valueMin,
						rangeRatio: dragging.ratioMax - dragging.ratioMin
					});
				} else dragging.type = dragging.ratioMax - ratio < ratio - dragging.ratioMin ? dragType.MAX : dragType.MIN;
				else dragging.type = dragType.MAX;
				return dragging;
			}
			function updatePosition(event, dragging = state.dragging.value) {
				let pos;
				const ratio = methods.getDraggingRatio(event, dragging);
				const localModel = methods.convertRatioToModel(ratio);
				switch (dragging.type) {
					case dragType.MIN:
						if (ratio <= dragging.ratioMax) {
							pos = {
								minR: ratio,
								maxR: dragging.ratioMax,
								min: localModel,
								max: dragging.valueMax
							};
							state.focus.value = "min";
						} else {
							pos = {
								minR: dragging.ratioMax,
								maxR: ratio,
								min: dragging.valueMax,
								max: localModel
							};
							state.focus.value = "max";
						}
						break;
					case dragType.MAX:
						if (ratio >= dragging.ratioMin) {
							pos = {
								minR: dragging.ratioMin,
								maxR: ratio,
								min: dragging.valueMin,
								max: localModel
							};
							state.focus.value = "max";
						} else {
							pos = {
								minR: ratio,
								maxR: dragging.ratioMin,
								min: localModel,
								max: dragging.valueMin
							};
							state.focus.value = "min";
						}
						break;
					case dragType.RANGE: {
						const ratioDelta = ratio - dragging.offsetRatio, minR = between(dragging.ratioMin + ratioDelta, state.innerMinRatio.value, state.innerMaxRatio.value - dragging.rangeRatio), modelDelta = localModel - dragging.offsetModel, min = between(dragging.valueMin + modelDelta, state.innerMin.value, state.innerMax.value - dragging.rangeValue);
						pos = {
							minR,
							maxR: minR + dragging.rangeRatio,
							min: state.roundValueFn.value(min),
							max: state.roundValueFn.value(min + dragging.rangeValue)
						};
						state.focus.value = "both";
						break;
					}
				}
				model.value = model.value.min === null || model.value.max === null ? {
					min: pos.min ?? props.min,
					max: pos.max ?? props.max
				} : {
					min: pos.min,
					max: pos.max
				};
				if (!props.snap || props.step === 0) {
					curMinRatio.value = pos.minR;
					curMaxRatio.value = pos.maxR;
				} else {
					curMinRatio.value = methods.convertModelToRatio(model.value.min);
					curMaxRatio.value = methods.convertModelToRatio(model.value.max);
				}
			}
			function onKeydown(evt) {
				if (!keyCodes$2.includes(evt.keyCode)) return;
				stopAndPrevent(evt);
				const stepVal = ([34, 33].includes(evt.keyCode) ? 10 : 1) * state.keyStep.value, offset = ([
					34,
					37,
					40
				].includes(evt.keyCode) ? -1 : 1) * (state.isReversed.value ? -1 : 1) * (props.vertical ? -1 : 1) * stepVal;
				if (state.focus.value === "both") {
					const interval = model.value.max - model.value.min;
					const min = between(state.roundValueFn.value(model.value.min + offset), state.innerMin.value, state.innerMax.value - interval);
					model.value = {
						min,
						max: state.roundValueFn.value(min + interval)
					};
				} else if (!state.focus.value) return;
				else {
					const which = state.focus.value;
					model.value = {
						...model.value,
						[which]: between(state.roundValueFn.value(model.value[which] + offset), which === "min" ? state.innerMin.value : model.value.min, which === "max" ? state.innerMax.value : model.value.max)
					};
				}
				updateValue();
			}
			return () => {
				const content = methods.getContent(selectionBarStyle, trackContainerTabindex, trackContainerEvents, (node) => {
					node.push(getMinThumb(), getMaxThumb());
				});
				return (0, vue.h)("div", {
					ref: rootRef,
					class: "q-range " + state.classes.value + (props.modelValue.min === null || props.modelValue.max === null ? " q-slider--no-value" : ""),
					...state.attributes.value,
					"aria-valuenow": props.modelValue.min + "|" + props.modelValue.max
				}, content);
			};
		}
	});
	//#endregion
	//#region src/components/rating/QRating.js
	var QRating_default = createComponent({
		name: "QRating",
		props: {
			...useSizeProps,
			...useFormProps,
			modelValue: {
				type: Number,
				required: true
			},
			max: {
				type: [String, Number],
				default: 5
			},
			icon: [String, Array],
			iconHalf: [String, Array],
			iconSelected: [String, Array],
			iconAriaLabel: [String, Array],
			color: [String, Array],
			colorHalf: [String, Array],
			colorSelected: [String, Array],
			noReset: Boolean,
			noDimming: Boolean,
			readonly: Boolean,
			disable: Boolean
		},
		emits: ["update:modelValue"],
		setup(props, { slots, emit }) {
			const { proxy: { $q } } = (0, vue.getCurrentInstance)();
			const sizeStyle = useSize(props);
			const injectFormInput = useFormInject(useFormAttrs(props));
			const mouseModel = (0, vue.ref)(0);
			let iconRefs = {};
			const editable = (0, vue.computed)(() => !props.readonly && !props.disable);
			const classes = (0, vue.computed)(() => `q-rating row inline items-center q-rating--${editable.value ? "" : "non-"}editable` + (props.noDimming ? " q-rating--no-dimming" : "") + (props.disable ? " disabled" : "") + (props.color !== void 0 && !Array.isArray(props.color) ? ` text-${props.color}` : ""));
			const iconData = (0, vue.computed)(() => {
				const iconLen = Array.isArray(props.icon) ? props.icon.length : 0, selIconLen = Array.isArray(props.iconSelected) ? props.iconSelected.length : 0, halfIconLen = Array.isArray(props.iconHalf) ? props.iconHalf.length : 0, colorLen = Array.isArray(props.color) ? props.color.length : 0, selColorLen = Array.isArray(props.colorSelected) ? props.colorSelected.length : 0, halfColorLen = Array.isArray(props.colorHalf) ? props.colorHalf.length : 0;
				return {
					iconLen,
					icon: iconLen > 0 ? props.icon[iconLen - 1] : props.icon,
					selIconLen,
					selIcon: selIconLen > 0 ? props.iconSelected[selIconLen - 1] : props.iconSelected,
					halfIconLen,
					halfIcon: halfIconLen > 0 ? props.iconHalf[halfIconLen - 1] : props.iconHalf,
					colorLen,
					color: colorLen > 0 ? props.color[colorLen - 1] : props.color,
					selColorLen,
					selColor: selColorLen > 0 ? props.colorSelected[selColorLen - 1] : props.colorSelected,
					halfColorLen,
					halfColor: halfColorLen > 0 ? props.colorHalf[halfColorLen - 1] : props.colorHalf
				};
			});
			const iconLabel = (0, vue.computed)(() => {
				if (typeof props.iconAriaLabel === "string") {
					const label = props.iconAriaLabel.length !== 0 ? `${props.iconAriaLabel} ` : "";
					return (i) => `${label}${i}`;
				}
				if (Array.isArray(props.iconAriaLabel)) {
					const iMax = props.iconAriaLabel.length;
					if (iMax > 0) return (i) => props.iconAriaLabel[Math.min(i, iMax) - 1];
				}
				return (i, label) => `${label} ${i}`;
			});
			const stars = (0, vue.computed)(() => {
				const acc = [], icons = iconData.value, ceil = Math.ceil(props.modelValue), tabIndex = Number.isInteger(props.modelValue) && props.modelValue >= 1 && props.modelValue <= props.max ? props.modelValue : 1;
				const halfIndex = props.iconHalf === void 0 || ceil === props.modelValue ? -1 : ceil;
				for (let i = 1; i <= props.max; i++) {
					const active = mouseModel.value === 0 && props.modelValue >= i || mouseModel.value > 0 && mouseModel.value >= i, half = halfIndex === i && mouseModel.value < i, exSelected = mouseModel.value > 0 && (half ? ceil : props.modelValue) >= i && mouseModel.value < i, color = half ? i <= icons.halfColorLen ? props.colorHalf[i - 1] : icons.halfColor : icons.selColor !== void 0 && active ? i <= icons.selColorLen ? props.colorSelected[i - 1] : icons.selColor : i <= icons.colorLen ? props.color[i - 1] : icons.color, name = (half ? i <= icons.halfIconLen ? props.iconHalf[i - 1] : icons.halfIcon : icons.selIcon !== void 0 && (active || exSelected) ? i <= icons.selIconLen ? props.iconSelected[i - 1] : icons.selIcon : i <= icons.iconLen ? props.icon[i - 1] : icons.icon) || $q.iconSet.rating.icon;
					acc.push({
						name: (half ? i <= icons.halfIconLen ? props.iconHalf[i - 1] : icons.halfIcon : icons.selIcon !== void 0 && (active || exSelected) ? i <= icons.selIconLen ? props.iconSelected[i - 1] : icons.selIcon : i <= icons.iconLen ? props.icon[i - 1] : icons.icon) || $q.iconSet.rating.icon,
						attrs: {
							tabindex: editable.value ? i === tabIndex ? 0 : -1 : null,
							role: "radio",
							"aria-checked": props.modelValue === i ? "true" : "false",
							"aria-label": iconLabel.value(i, name)
						},
						iconClass: "q-rating__icon" + (active || half ? " q-rating__icon--active" : "") + (exSelected ? " q-rating__icon--exselected" : "") + (mouseModel.value === i ? " q-rating__icon--hovered" : "") + (color !== void 0 ? ` text-${color}` : "")
					});
				}
				return acc;
			});
			const attributes = (0, vue.computed)(() => {
				const attrs = { role: "radiogroup" };
				if (props.disable) attrs["aria-disabled"] = "true";
				if (props.readonly) attrs["aria-readonly"] = "true";
				return attrs;
			});
			function set(value) {
				if (editable.value) {
					const model = between(Number.parseInt(value, 10), 1, Number.parseInt(props.max, 10)), newVal = !props.noReset && props.modelValue === model ? 0 : model;
					if (newVal !== props.modelValue) emit("update:modelValue", newVal);
					mouseModel.value = 0;
				}
			}
			function setHoverValue(value) {
				if (editable.value) mouseModel.value = value;
			}
			function onKeydown(e, i) {
				switch (e.keyCode) {
					case 13:
					case 32:
						set(i);
						return stopAndPrevent(e);
					case 37: {
						const index = i + ($q.lang.rtl ? 1 : -1);
						if (iconRefs[`rt${index}`]) iconRefs[`rt${index}`].focus();
						return stopAndPrevent(e);
					}
					case 39: {
						const index = i + ($q.lang.rtl ? -1 : 1);
						if (iconRefs[`rt${index}`]) iconRefs[`rt${index}`].focus();
						return stopAndPrevent(e);
					}
					case 40:
						if (iconRefs[`rt${i - 1}`]) iconRefs[`rt${i - 1}`].focus();
						return stopAndPrevent(e);
					case 38:
						if (iconRefs[`rt${i + 1}`]) iconRefs[`rt${i + 1}`].focus();
						return stopAndPrevent(e);
				}
			}
			function resetMouseModel() {
				mouseModel.value = 0;
			}
			(0, vue.onBeforeUpdate)(() => {
				iconRefs = {};
			});
			return () => {
				const child = [];
				stars.value.forEach(({ iconClass, name, attrs }, index) => {
					const i = index + 1;
					child.push((0, vue.h)("div", {
						key: i,
						ref: (el) => {
							iconRefs[`rt${i}`] = el;
						},
						class: "q-rating__icon-container flex flex-center",
						...attrs,
						onClick() {
							set(i);
						},
						onMouseover() {
							setHoverValue(i);
						},
						onMouseout: resetMouseModel,
						onFocus() {
							setHoverValue(i);
						},
						onBlur: resetMouseModel,
						onKeydown(e) {
							onKeydown(e, i);
						}
					}, hMergeSlot(slots[`tip-${i}`], [(0, vue.h)(QIcon_default, {
						class: iconClass,
						name
					})])));
				});
				if (props.name !== void 0 && !props.disable) injectFormInput(child, "push");
				return (0, vue.h)("div", {
					class: classes.value,
					style: sizeStyle.value,
					...attributes.value
				}, child);
			};
		}
	});
	//#endregion
	//#region src/components/responsive/QResponsive.js
	var QResponsive_default = createComponent({
		name: "QResponsive",
		props: useRatioProps,
		setup(props, { slots }) {
			const ratioStyle = useRatio(props);
			return () => (0, vue.h)("div", { class: "q-responsive" }, [(0, vue.h)("div", { class: "q-responsive__filler overflow-hidden" }, [(0, vue.h)("div", { style: ratioStyle.value })]), (0, vue.h)("div", { class: "q-responsive__content absolute-full fit" }, hSlot(slots.default))]);
		}
	});
	//#endregion
	//#region src/components/scroll-area/ScrollAreaControls.js
	/**
	* We are using a sub-component to avoid unnecessary re-renders
	* of the QScrollArea content when the scrollbars are interacted with.
	*/
	var ScrollAreaControls_default = createComponent({
		props: [
			"store",
			"barStyle",
			"verticalBarStyle",
			"horizontalBarStyle"
		],
		setup(props) {
			return () => [
				(0, vue.h)("div", {
					class: props.store.scroll.vertical.barClass.value,
					style: [props.barStyle, props.verticalBarStyle],
					"aria-hidden": "true",
					onMousedown: props.store.onVerticalMousedown
				}),
				(0, vue.h)("div", {
					class: props.store.scroll.horizontal.barClass.value,
					style: [props.barStyle, props.horizontalBarStyle],
					"aria-hidden": "true",
					onMousedown: props.store.onHorizontalMousedown
				}),
				(0, vue.withDirectives)((0, vue.h)("div", {
					ref: props.store.scroll.vertical.ref,
					class: props.store.scroll.vertical.thumbClass.value,
					style: props.store.scroll.vertical.style.value,
					"aria-hidden": "true"
				}), props.store.thumbVertDir),
				(0, vue.withDirectives)((0, vue.h)("div", {
					ref: props.store.scroll.horizontal.ref,
					class: props.store.scroll.horizontal.thumbClass.value,
					style: props.store.scroll.horizontal.style.value,
					"aria-hidden": "true"
				}), props.store.thumbHorizDir)
			];
		}
	});
	//#endregion
	//#region src/components/scroll-area/QScrollArea.js
	const axisList = ["vertical", "horizontal"];
	const dirProps = {
		vertical: {
			offset: "offsetY",
			scroll: "scrollTop",
			dir: "down",
			dist: "y"
		},
		horizontal: {
			offset: "offsetX",
			scroll: "scrollLeft",
			dir: "right",
			dist: "x"
		}
	};
	const panOpts = {
		prevent: true,
		mouse: true,
		mouseAllDir: true
	};
	const getMinThumbSize = (size) => size >= 250 ? 50 : Math.ceil(size / 5);
	var QScrollArea_default = createComponent({
		name: "QScrollArea",
		props: {
			...useDarkProps,
			thumbStyle: Object,
			verticalThumbStyle: Object,
			horizontalThumbStyle: Object,
			barStyle: [
				Array,
				String,
				Object
			],
			verticalBarStyle: [
				Array,
				String,
				Object
			],
			horizontalBarStyle: [
				Array,
				String,
				Object
			],
			verticalOffset: {
				type: Array,
				default: () => [0, 0]
			},
			horizontalOffset: {
				type: Array,
				default: () => [0, 0]
			},
			contentStyle: [
				Array,
				String,
				Object
			],
			contentActiveStyle: [
				Array,
				String,
				Object
			],
			delay: {
				type: [String, Number],
				default: 1e3
			},
			visible: {
				type: Boolean,
				default: null
			},
			tabindex: [String, Number],
			onScroll: Function
		},
		setup(props, { slots, emit }) {
			const tempShowing = (0, vue.ref)(false);
			const panning = (0, vue.ref)(false);
			const hover = (0, vue.ref)(false);
			const container = {
				vertical: (0, vue.ref)(0),
				horizontal: (0, vue.ref)(0)
			};
			const scroll = {
				vertical: {
					ref: (0, vue.ref)(null),
					position: (0, vue.ref)(0),
					size: (0, vue.ref)(0)
				},
				horizontal: {
					ref: (0, vue.ref)(null),
					position: (0, vue.ref)(0),
					size: (0, vue.ref)(0)
				}
			};
			const { proxy } = (0, vue.getCurrentInstance)();
			const isDark = useDark(props, proxy.$q);
			let timer = null, panRefPos;
			const targetRef = (0, vue.ref)(null);
			const classes = (0, vue.computed)(() => "q-scrollarea" + (isDark.value ? " q-scrollarea--dark" : ""));
			Object.assign(container, {
				verticalInner: (0, vue.computed)(() => container.vertical.value - props.verticalOffset[0] - props.verticalOffset[1]),
				horizontalInner: (0, vue.computed)(() => container.horizontal.value - props.horizontalOffset[0] - props.horizontalOffset[1])
			});
			scroll.vertical.percentage = (0, vue.computed)(() => {
				const diff = scroll.vertical.size.value - container.vertical.value;
				if (diff <= 0) return 0;
				const p = between(scroll.vertical.position.value / diff, 0, 1);
				return Math.round(p * 1e4) / 1e4;
			});
			scroll.vertical.thumbHidden = (0, vue.computed)(() => !(props.visible === null ? hover.value : props.visible) && !tempShowing.value && !panning.value || scroll.vertical.size.value <= container.vertical.value + 1);
			scroll.vertical.thumbStart = (0, vue.computed)(() => props.verticalOffset[0] + scroll.vertical.percentage.value * (container.verticalInner.value - scroll.vertical.thumbSize.value));
			scroll.vertical.thumbSize = (0, vue.computed)(() => Math.round(between(container.verticalInner.value * container.verticalInner.value / scroll.vertical.size.value, getMinThumbSize(container.verticalInner.value), container.verticalInner.value)));
			scroll.vertical.style = (0, vue.computed)(() => ({
				...props.thumbStyle,
				...props.verticalThumbStyle,
				top: `${scroll.vertical.thumbStart.value}px`,
				height: `${scroll.vertical.thumbSize.value}px`,
				right: `${props.horizontalOffset[1]}px`
			}));
			scroll.vertical.thumbClass = (0, vue.computed)(() => "q-scrollarea__thumb q-scrollarea__thumb--v absolute-right" + (scroll.vertical.thumbHidden.value ? " q-scrollarea__thumb--invisible" : ""));
			scroll.vertical.barClass = (0, vue.computed)(() => "q-scrollarea__bar q-scrollarea__bar--v absolute-right" + (scroll.vertical.thumbHidden.value ? " q-scrollarea__bar--invisible" : ""));
			scroll.horizontal.percentage = (0, vue.computed)(() => {
				const diff = scroll.horizontal.size.value - container.horizontal.value;
				if (diff <= 0) return 0;
				const p = between(getHorizontalLogicalPosition(scroll.horizontal.position.value) / diff, 0, 1);
				return Math.round(p * 1e4) / 1e4;
			});
			scroll.horizontal.thumbHidden = (0, vue.computed)(() => !(props.visible === null ? hover.value : props.visible) && !tempShowing.value && !panning.value || scroll.horizontal.size.value <= container.horizontal.value + 1);
			scroll.horizontal.thumbStart = (0, vue.computed)(() => props.horizontalOffset[proxy.$q.lang.rtl ? 1 : 0] + scroll.horizontal.percentage.value * (container.horizontalInner.value - scroll.horizontal.thumbSize.value));
			scroll.horizontal.thumbSize = (0, vue.computed)(() => Math.round(between(container.horizontalInner.value * container.horizontalInner.value / scroll.horizontal.size.value, getMinThumbSize(container.horizontalInner.value), container.horizontalInner.value)));
			scroll.horizontal.style = (0, vue.computed)(() => ({
				...props.thumbStyle,
				...props.horizontalThumbStyle,
				[proxy.$q.lang.rtl ? "right" : "left"]: `${scroll.horizontal.thumbStart.value}px`,
				width: `${scroll.horizontal.thumbSize.value}px`,
				bottom: `${props.verticalOffset[1]}px`
			}));
			scroll.horizontal.thumbClass = (0, vue.computed)(() => "q-scrollarea__thumb q-scrollarea__thumb--h absolute-bottom" + (scroll.horizontal.thumbHidden.value ? " q-scrollarea__thumb--invisible" : ""));
			scroll.horizontal.barClass = (0, vue.computed)(() => "q-scrollarea__bar q-scrollarea__bar--h absolute-bottom" + (scroll.horizontal.thumbHidden.value ? " q-scrollarea__bar--invisible" : ""));
			const mainStyle = (0, vue.computed)(() => scroll.vertical.thumbHidden.value && scroll.horizontal.thumbHidden.value ? props.contentStyle : props.contentActiveStyle);
			function getScroll() {
				const info = {};
				axisList.forEach((axis) => {
					const data = scroll[axis];
					Object.assign(info, {
						[axis + "Position"]: data.position.value,
						[axis + "Percentage"]: data.percentage.value,
						[axis + "Size"]: data.size.value,
						[axis + "ContainerSize"]: container[axis].value,
						[axis + "ContainerInnerSize"]: container[axis + "Inner"].value
					});
				});
				return info;
			}
			const emitScroll = debounce(() => {
				const info = getScroll();
				info.ref = proxy;
				emit("scroll", info);
			}, 0);
			function localSetScrollPosition(axis, offset, duration) {
				if (!axisList.includes(axis)) {
					console.error("[QScrollArea]: wrong first param of setScrollPosition (vertical/horizontal)");
					return;
				}
				(axis === "vertical" ? setVerticalScrollPosition : setHorizontalScrollPosition)(targetRef.value, offset, duration);
			}
			function updateContainer({ height, width }) {
				let change = false;
				if (container.vertical.value !== height) {
					container.vertical.value = height;
					change = true;
				}
				if (container.horizontal.value !== width) {
					container.horizontal.value = width;
					change = true;
				}
				if (change) startTimer();
			}
			function updateScroll({ position }) {
				let change = false;
				if (scroll.vertical.position.value !== position.top) {
					scroll.vertical.position.value = position.top;
					change = true;
				}
				if (scroll.horizontal.position.value !== position.left) {
					scroll.horizontal.position.value = position.left;
					change = true;
				}
				if (change) startTimer();
			}
			function updateScrollSize({ height, width }) {
				if (scroll.horizontal.size.value !== width) {
					scroll.horizontal.size.value = width;
					startTimer();
				}
				if (scroll.vertical.size.value !== height) {
					scroll.vertical.size.value = height;
					startTimer();
				}
			}
			function onPanThumb(e, axis) {
				const data = scroll[axis];
				if (e.isFirst) {
					if (data.thumbHidden.value) return;
					panRefPos = axis === "horizontal" ? getHorizontalLogicalPosition(data.position.value) : data.position.value;
					panning.value = true;
				} else if (!panning.value) return;
				if (e.isFinal) panning.value = false;
				const dProp = dirProps[axis];
				const multiplier = (data.size.value - container[axis].value) / (container[axis + "Inner"].value - data.thumbSize.value);
				const distance = e.distance[dProp.dist];
				const direction = (e.direction === dProp.dir ? 1 : -1) * (axis === "horizontal" && proxy.$q.lang.rtl ? -1 : 1);
				const pos = panRefPos + direction * distance * multiplier;
				setScroll(axis === "horizontal" ? getHorizontalNativePosition(pos) : pos, axis);
			}
			function onMousedown(evt, axis) {
				const data = scroll[axis];
				if (!data.thumbHidden.value) {
					const isHorizontalRtl = axis === "horizontal" && proxy.$q.lang.rtl;
					const startOffset = axis === "vertical" ? props.verticalOffset[0] : props.horizontalOffset[isHorizontalRtl ? 1 : 0];
					const offset = (isHorizontalRtl ? container.horizontal.value - evt.offsetX : evt[dirProps[axis].offset]) - startOffset;
					const thumbStart = data.thumbStart.value - startOffset;
					if (offset < thumbStart || offset > thumbStart + data.thumbSize.value) {
						const percentage = between((offset - data.thumbSize.value / 2) / (container[axis + "Inner"].value - data.thumbSize.value), 0, 1);
						setScroll(isHorizontalRtl ? getHorizontalNativePosition(percentage * Math.max(0, data.size.value - container[axis].value)) : percentage * Math.max(0, data.size.value - container[axis].value), axis);
					}
					if (data.ref.value !== null) data.ref.value.dispatchEvent(new MouseEvent(evt.type, evt));
				}
			}
			function startTimer() {
				tempShowing.value = true;
				if (timer !== null) clearTimeout(timer);
				timer = setTimeout(() => {
					timer = null;
					tempShowing.value = false;
				}, props.delay);
				if (props.onScroll !== void 0) emitScroll();
			}
			function setScroll(offset, axis) {
				targetRef.value[dirProps[axis].scroll] = offset;
			}
			function getHorizontalLogicalPosition(position, rtl = proxy.$q.lang.rtl) {
				if (!rtl) return position;
				return rtlHasScrollBug ? Math.max(0, scroll.horizontal.size.value - container.horizontal.value) - position : -position;
			}
			function getHorizontalNativePosition(position, rtl = proxy.$q.lang.rtl) {
				if (!rtl) return position;
				return rtlHasScrollBug ? Math.max(0, scroll.horizontal.size.value - container.horizontal.value) - position : -position;
			}
			let mouseEventTimer = null;
			function onMouseenter() {
				if (mouseEventTimer !== null) clearTimeout(mouseEventTimer);
				mouseEventTimer = setTimeout(() => {
					mouseEventTimer = null;
					hover.value = true;
				}, proxy.$q.platform.is.ios ? 50 : 0);
			}
			function onMouseleave() {
				if (mouseEventTimer !== null) {
					clearTimeout(mouseEventTimer);
					mouseEventTimer = null;
				}
				hover.value = false;
			}
			let scrollPosition = null;
			(0, vue.watch)(() => proxy.$q.lang.rtl, (rtl, oldRtl) => {
				if (targetRef.value !== null) setHorizontalScrollPosition(targetRef.value, getHorizontalNativePosition(getHorizontalLogicalPosition(scroll.horizontal.position.value, oldRtl), rtl));
			});
			(0, vue.onDeactivated)(() => {
				scrollPosition = {
					top: scroll.vertical.position.value,
					left: scroll.horizontal.position.value
				};
			});
			(0, vue.onActivated)(() => {
				if (scrollPosition === null) return;
				const scrollTarget = targetRef.value;
				if (scrollTarget !== null) {
					setHorizontalScrollPosition(scrollTarget, scrollPosition.left);
					setVerticalScrollPosition(scrollTarget, scrollPosition.top);
				}
			});
			(0, vue.onBeforeUnmount)(emitScroll.cancel);
			Object.assign(proxy, {
				getScrollTarget: () => targetRef.value,
				getScroll,
				getScrollPosition: () => ({
					top: scroll.vertical.position.value,
					left: scroll.horizontal.position.value
				}),
				getScrollPercentage: () => ({
					top: scroll.vertical.percentage.value,
					left: scroll.horizontal.percentage.value
				}),
				setScrollPosition: localSetScrollPosition,
				setScrollPercentage(axis, percentage, duration) {
					const offset = percentage * (scroll[axis].size.value - container[axis].value);
					localSetScrollPosition(axis, axis === "horizontal" ? getHorizontalNativePosition(offset) : offset, duration);
				}
			});
			const store = {
				scroll,
				thumbVertDir: [[
					TouchPan_default,
					(e) => {
						onPanThumb(e, "vertical");
					},
					void 0,
					{
						vertical: true,
						...panOpts
					}
				]],
				thumbHorizDir: [[
					TouchPan_default,
					(e) => {
						onPanThumb(e, "horizontal");
					},
					void 0,
					{
						horizontal: true,
						...panOpts
					}
				]],
				onVerticalMousedown(evt) {
					onMousedown(evt, "vertical");
				},
				onHorizontalMousedown(evt) {
					onMousedown(evt, "horizontal");
				}
			};
			return () => (0, vue.h)("div", {
				class: classes.value,
				onMouseenter,
				onMouseleave
			}, [
				(0, vue.h)("div", {
					ref: targetRef,
					class: "q-scrollarea__container scroll relative-position fit hide-scrollbar",
					tabindex: props.tabindex !== void 0 ? props.tabindex : void 0
				}, [(0, vue.h)("div", {
					class: "q-scrollarea__content absolute",
					style: mainStyle.value
				}, hMergeSlot(slots.default, [(0, vue.h)(QResizeObserver_default, {
					debounce: 0,
					onResize: updateScrollSize
				})])), (0, vue.h)(QScrollObserver_default, {
					axis: "both",
					onScroll: updateScroll
				})]),
				(0, vue.h)(QResizeObserver_default, {
					debounce: 0,
					onResize: updateContainer
				}),
				(0, vue.h)(ScrollAreaControls_default, {
					store,
					barStyle: props.barStyle,
					verticalBarStyle: props.verticalBarStyle,
					horizontalBarStyle: props.horizontalBarStyle
				})
			]);
		}
	});
	//#endregion
	//#region src/components/virtual-scroll/use-virtual-scroll.js
	const aggBucketSize = 1e3;
	const scrollToEdges = [
		"start",
		"center",
		"end",
		"start-force",
		"center-force",
		"end-force"
	];
	const filterProto = Array.prototype.filter;
	const setOverflowAnchor = window.getComputedStyle(document.body).overflowAnchor === void 0 ? noop : function setOverflowAnchor(contentEl, index) {
		if (contentEl === null) return;
		if (contentEl._qOverflowAnimationFrame !== void 0) cancelAnimationFrame(contentEl._qOverflowAnimationFrame);
		contentEl._qOverflowAnimationFrame = requestAnimationFrame(() => {
			if (contentEl === null) return;
			contentEl._qOverflowAnimationFrame = void 0;
			const children = contentEl.children || [];
			filterProto.call(children, (el) => el.dataset && el.dataset.qVsAnchor !== void 0).forEach((el) => {
				delete el.dataset.qVsAnchor;
			});
			const el = children[index];
			if (el?.dataset) el.dataset.qVsAnchor = "";
		});
	};
	function sumFn(acc, item) {
		return acc + item;
	}
	function getScrollDetails(parent, child, beforeRef, afterRef, horizontal, rtl, stickyStart, stickyEnd) {
		const parentCalc = parent === window ? document.scrollingElement || document.documentElement : parent, propElSize = horizontal ? "offsetWidth" : "offsetHeight", details = {
			scrollStart: 0,
			scrollViewSize: -stickyStart - stickyEnd,
			scrollMaxSize: 0,
			offsetStart: -stickyStart,
			offsetEnd: -stickyEnd
		};
		if (horizontal) {
			if (parent === window) {
				details.scrollStart = window.pageXOffset || window.scrollX || document.body.scrollLeft || 0;
				details.scrollViewSize += document.documentElement.clientWidth;
			} else {
				details.scrollStart = parentCalc.scrollLeft;
				details.scrollViewSize += parentCalc.clientWidth;
			}
			details.scrollMaxSize = parentCalc.scrollWidth;
			if (rtl) details.scrollStart = (rtlHasScrollBug ? details.scrollMaxSize - details.scrollViewSize : 0) - details.scrollStart;
		} else {
			if (parent === window) {
				details.scrollStart = window.pageYOffset || window.scrollY || document.body.scrollTop || 0;
				details.scrollViewSize += document.documentElement.clientHeight;
			} else {
				details.scrollStart = parentCalc.scrollTop;
				details.scrollViewSize += parentCalc.clientHeight;
			}
			details.scrollMaxSize = parentCalc.scrollHeight;
		}
		if (beforeRef !== null) {
			for (let el = beforeRef.previousElementSibling; el !== null; el = el.previousElementSibling) if (!el.classList.contains("q-virtual-scroll--skip")) details.offsetStart += el[propElSize];
		}
		if (afterRef !== null) {
			for (let el = afterRef.nextElementSibling; el !== null; el = el.nextElementSibling) if (!el.classList.contains("q-virtual-scroll--skip")) details.offsetEnd += el[propElSize];
		}
		if (child !== parent) {
			const parentRect = parentCalc.getBoundingClientRect(), childRect = child.getBoundingClientRect();
			if (horizontal) {
				details.offsetStart += childRect.left - parentRect.left;
				details.offsetEnd -= childRect.width;
			} else {
				details.offsetStart += childRect.top - parentRect.top;
				details.offsetEnd -= childRect.height;
			}
			if (parent !== window) details.offsetStart += details.scrollStart;
			details.offsetEnd += details.scrollMaxSize - details.offsetStart;
		}
		return details;
	}
	function setScroll(parent, scroll, horizontal, rtl) {
		if (scroll === "end") scroll = (parent === window ? document.body : parent)[horizontal ? "scrollWidth" : "scrollHeight"];
		if (parent === window) if (horizontal) {
			if (rtl) scroll = (rtlHasScrollBug ? document.body.scrollWidth - document.documentElement.clientWidth : 0) - scroll;
			window.scrollTo(scroll, window.pageYOffset || window.scrollY || document.body.scrollTop || 0);
		} else window.scrollTo(window.pageXOffset || window.scrollX || document.body.scrollLeft || 0, scroll);
		else if (horizontal) {
			if (rtl) scroll = (rtlHasScrollBug ? parent.scrollWidth - parent.offsetWidth : 0) - scroll;
			parent.scrollLeft = scroll;
		} else parent.scrollTop = scroll;
	}
	function sumSize(sizeAgg, size, from, to) {
		if (from >= to) return 0;
		const lastTo = size.length, fromAgg = Math.floor(from / aggBucketSize), toAgg = Math.floor((to - 1) / aggBucketSize) + 1;
		let total = sizeAgg.slice(fromAgg, toAgg).reduce(sumFn, 0);
		if (from % aggBucketSize !== 0) total -= size.slice(fromAgg * aggBucketSize, from).reduce(sumFn, 0);
		if (to % aggBucketSize !== 0 && to !== lastTo) total -= size.slice(to, toAgg * aggBucketSize).reduce(sumFn, 0);
		return total;
	}
	const commonVirtScrollProps = {
		virtualScrollSliceSize: {
			type: [Number, String],
			default: 10
		},
		virtualScrollSliceRatioBefore: {
			type: [Number, String],
			default: 1
		},
		virtualScrollSliceRatioAfter: {
			type: [Number, String],
			default: 1
		},
		virtualScrollItemSize: {
			type: [Number, String],
			default: 24
		},
		virtualScrollStickySizeStart: {
			type: [Number, String],
			default: 0
		},
		virtualScrollStickySizeEnd: {
			type: [Number, String],
			default: 0
		},
		tableColspan: [Number, String]
	};
	const commonVirtScrollPropsList = Object.keys(commonVirtScrollProps);
	const useVirtualScrollProps = {
		virtualScrollHorizontal: Boolean,
		onVirtualScroll: Function,
		...commonVirtScrollProps
	};
	function useVirtualScroll({ virtualScrollLength, getVirtualScrollTarget, getVirtualScrollEl, virtualScrollItemSizeComputed }) {
		const { props, emit, proxy } = (0, vue.getCurrentInstance)();
		const { $q } = proxy;
		let prevScrollStart, prevToIndex, localScrollViewSize, virtualScrollSizesAgg = [], virtualScrollSizes;
		const virtualScrollPaddingBefore = (0, vue.ref)(0);
		const virtualScrollPaddingAfter = (0, vue.ref)(0);
		const virtualScrollSliceSizeComputed = (0, vue.ref)({});
		const beforeRef = (0, vue.ref)(null);
		const afterRef = (0, vue.ref)(null);
		const contentRef = (0, vue.ref)(null);
		const virtualScrollSliceRange = (0, vue.ref)({
			from: 0,
			to: 0
		});
		const colspanAttr = (0, vue.computed)(() => props.tableColspan !== void 0 ? props.tableColspan : 100);
		if (virtualScrollItemSizeComputed === void 0) virtualScrollItemSizeComputed = (0, vue.computed)(() => props.virtualScrollItemSize);
		const needsReset = (0, vue.computed)(() => virtualScrollItemSizeComputed.value + ";" + props.virtualScrollHorizontal);
		(0, vue.watch)((0, vue.computed)(() => needsReset.value + ";" + props.virtualScrollSliceRatioBefore + ";" + props.virtualScrollSliceRatioAfter), () => {
			setVirtualScrollSize();
		});
		(0, vue.watch)(needsReset, reset);
		function reset() {
			localResetVirtualScroll(prevToIndex, true);
		}
		function refresh(toIndex) {
			localResetVirtualScroll(toIndex === void 0 ? prevToIndex : toIndex);
		}
		function scrollTo(toIndex, edge) {
			const scrollEl = getVirtualScrollTarget();
			if (scrollEl === void 0 || scrollEl === null || scrollEl.nodeType === 8) return;
			const scrollDetails = getScrollDetails(scrollEl, getVirtualScrollEl(), beforeRef.value, afterRef.value, props.virtualScrollHorizontal, $q.lang.rtl, props.virtualScrollStickySizeStart, props.virtualScrollStickySizeEnd);
			if (localScrollViewSize !== scrollDetails.scrollViewSize) setVirtualScrollSize(scrollDetails.scrollViewSize);
			setVirtualScrollSliceRange(scrollEl, scrollDetails, Math.min(virtualScrollLength.value - 1, Math.max(0, Number.parseInt(toIndex, 10) || 0)), 0, scrollToEdges.includes(edge) ? edge : prevToIndex !== -1 && toIndex > prevToIndex ? "end" : "start");
		}
		function localOnVirtualScrollEvt() {
			const scrollEl = getVirtualScrollTarget();
			if (scrollEl === void 0 || scrollEl === null || scrollEl.nodeType === 8) return;
			const scrollDetails = getScrollDetails(scrollEl, getVirtualScrollEl(), beforeRef.value, afterRef.value, props.virtualScrollHorizontal, $q.lang.rtl, props.virtualScrollStickySizeStart, props.virtualScrollStickySizeEnd), listLastIndex = virtualScrollLength.value - 1, listEndOffset = scrollDetails.scrollMaxSize - scrollDetails.offsetStart - scrollDetails.offsetEnd - virtualScrollPaddingAfter.value;
			if (prevScrollStart === scrollDetails.scrollStart) return;
			if (scrollDetails.scrollMaxSize <= 0) {
				setVirtualScrollSliceRange(scrollEl, scrollDetails, 0, 0);
				return;
			}
			if (localScrollViewSize !== scrollDetails.scrollViewSize) setVirtualScrollSize(scrollDetails.scrollViewSize);
			updateVirtualScrollSizes(virtualScrollSliceRange.value.from);
			const scrollMaxStart = Math.floor(scrollDetails.scrollMaxSize - Math.max(scrollDetails.scrollViewSize, scrollDetails.offsetEnd) - Math.min(virtualScrollSizes[listLastIndex], scrollDetails.scrollViewSize / 2));
			if (scrollMaxStart > 0 && Math.ceil(scrollDetails.scrollStart) >= scrollMaxStart) {
				setVirtualScrollSliceRange(scrollEl, scrollDetails, listLastIndex, scrollDetails.scrollMaxSize - scrollDetails.offsetEnd - virtualScrollSizesAgg.reduce(sumFn, 0));
				return;
			}
			let toIndex = 0, listOffset = scrollDetails.scrollStart - scrollDetails.offsetStart, offset = listOffset;
			if (listOffset <= listEndOffset && listOffset + scrollDetails.scrollViewSize >= virtualScrollPaddingBefore.value) {
				listOffset -= virtualScrollPaddingBefore.value;
				toIndex = virtualScrollSliceRange.value.from;
				offset = listOffset;
			} else for (let j = 0; listOffset >= virtualScrollSizesAgg[j] && toIndex < listLastIndex; j++) {
				listOffset -= virtualScrollSizesAgg[j];
				toIndex += aggBucketSize;
			}
			while (listOffset > 0 && toIndex < listLastIndex) {
				listOffset -= virtualScrollSizes[toIndex];
				if (listOffset > -scrollDetails.scrollViewSize) {
					toIndex++;
					offset = listOffset;
				} else offset = virtualScrollSizes[toIndex] + listOffset;
			}
			setVirtualScrollSliceRange(scrollEl, scrollDetails, toIndex, offset);
		}
		function setVirtualScrollSliceRange(scrollEl, scrollDetails, toIndex, offset, align) {
			const alignForce = typeof align === "string" && align.includes("-force");
			const alignEnd = alignForce ? align.replace("-force", "") : align;
			const alignRange = alignEnd !== void 0 ? alignEnd : "start";
			let from = Math.max(0, toIndex - virtualScrollSliceSizeComputed.value[alignRange]), to = from + virtualScrollSliceSizeComputed.value.total;
			if (to > virtualScrollLength.value) {
				to = virtualScrollLength.value;
				from = Math.max(0, to - virtualScrollSliceSizeComputed.value.total);
			}
			prevScrollStart = scrollDetails.scrollStart;
			const rangeChanged = from !== virtualScrollSliceRange.value.from || to !== virtualScrollSliceRange.value.to;
			if (!rangeChanged && alignEnd === void 0) {
				emitScroll(toIndex);
				return;
			}
			const { activeElement } = document;
			const contentEl = contentRef.value;
			if (rangeChanged && contentEl !== null && contentEl !== activeElement && contentEl.contains(activeElement)) {
				contentEl.addEventListener("focusout", onBlurRefocusFn);
				setTimeout(() => {
					contentEl?.removeEventListener("focusout", onBlurRefocusFn);
				}, 0);
			}
			setOverflowAnchor(contentEl, toIndex - from);
			const sizeBefore = alignEnd !== void 0 ? virtualScrollSizes.slice(from, toIndex).reduce(sumFn, 0) : 0;
			if (rangeChanged) {
				const tempTo = to >= virtualScrollSliceRange.value.from && from <= virtualScrollSliceRange.value.to ? virtualScrollSliceRange.value.to : to;
				virtualScrollSliceRange.value = {
					from,
					to: tempTo
				};
				virtualScrollPaddingBefore.value = sumSize(virtualScrollSizesAgg, virtualScrollSizes, 0, from);
				virtualScrollPaddingAfter.value = sumSize(virtualScrollSizesAgg, virtualScrollSizes, to, virtualScrollLength.value);
				requestAnimationFrame(() => {
					if (virtualScrollSliceRange.value.to !== to && prevScrollStart === scrollDetails.scrollStart) {
						virtualScrollSliceRange.value = {
							from: virtualScrollSliceRange.value.from,
							to
						};
						virtualScrollPaddingAfter.value = sumSize(virtualScrollSizesAgg, virtualScrollSizes, to, virtualScrollLength.value);
					}
				});
			}
			requestAnimationFrame(() => {
				if (prevScrollStart !== scrollDetails.scrollStart) return;
				if (rangeChanged) updateVirtualScrollSizes(from);
				const sizeAfter = virtualScrollSizes.slice(from, toIndex).reduce(sumFn, 0), posStart = sizeAfter + scrollDetails.offsetStart + virtualScrollPaddingBefore.value, posEnd = posStart + virtualScrollSizes[toIndex];
				let scrollPosition = posStart + offset;
				if (alignEnd !== void 0) {
					const sizeDiff = sizeAfter - sizeBefore;
					const scrollStart = scrollDetails.scrollStart + sizeDiff;
					scrollPosition = !alignForce && scrollStart < posStart && posEnd < scrollStart + scrollDetails.scrollViewSize ? scrollStart : alignEnd === "end" ? posEnd - scrollDetails.scrollViewSize : posStart - (alignEnd === "start" ? 0 : Math.round((scrollDetails.scrollViewSize - virtualScrollSizes[toIndex]) / 2));
				}
				prevScrollStart = scrollPosition;
				setScroll(scrollEl, scrollPosition, props.virtualScrollHorizontal, $q.lang.rtl);
				emitScroll(toIndex);
			});
		}
		function updateVirtualScrollSizes(from) {
			const contentEl = contentRef.value;
			if (contentEl) {
				const children = filterProto.call(contentEl.children, (el) => el.classList && !el.classList.contains("q-virtual-scroll--skip")), childrenLength = children.length, sizeFn = props.virtualScrollHorizontal ? (el) => el.getBoundingClientRect().width : (el) => el.offsetHeight;
				let index = from, size, diff;
				for (let i = 0; i < childrenLength;) {
					size = sizeFn(children[i]);
					i++;
					while (i < childrenLength && children[i].classList.contains("q-virtual-scroll--with-prev")) {
						size += sizeFn(children[i]);
						i++;
					}
					diff = size - virtualScrollSizes[index];
					if (diff !== 0) {
						virtualScrollSizes[index] += diff;
						virtualScrollSizesAgg[Math.floor(index / aggBucketSize)] += diff;
					}
					index++;
				}
			}
		}
		function onBlurRefocusFn() {
			contentRef.value?.focus();
		}
		function localResetVirtualScroll(toIndex, fullReset) {
			const defaultSize = Number(virtualScrollItemSizeComputed.value);
			if (fullReset || !Array.isArray(virtualScrollSizes)) virtualScrollSizes = [];
			const oldVirtualScrollSizesLength = virtualScrollSizes.length;
			virtualScrollSizes.length = virtualScrollLength.value;
			for (let i = virtualScrollLength.value - 1; i >= oldVirtualScrollSizesLength; i--) virtualScrollSizes[i] = defaultSize;
			const jMax = Math.floor((virtualScrollLength.value - 1) / aggBucketSize);
			virtualScrollSizesAgg = [];
			for (let j = 0; j <= jMax; j++) {
				let size = 0;
				const iMax = Math.min((j + 1) * aggBucketSize, virtualScrollLength.value);
				for (let i = j * aggBucketSize; i < iMax; i++) size += virtualScrollSizes[i];
				virtualScrollSizesAgg.push(size);
			}
			prevToIndex = -1;
			prevScrollStart = void 0;
			virtualScrollPaddingBefore.value = sumSize(virtualScrollSizesAgg, virtualScrollSizes, 0, virtualScrollSliceRange.value.from);
			virtualScrollPaddingAfter.value = sumSize(virtualScrollSizesAgg, virtualScrollSizes, virtualScrollSliceRange.value.to, virtualScrollLength.value);
			if (toIndex >= 0) {
				updateVirtualScrollSizes(virtualScrollSliceRange.value.from);
				(0, vue.nextTick)(() => {
					scrollTo(toIndex);
				});
			} else onVirtualScrollEvt();
		}
		function setVirtualScrollSize(scrollViewSize) {
			if (scrollViewSize === void 0 && typeof window !== "undefined") {
				const scrollEl = getVirtualScrollTarget();
				if (scrollEl !== void 0 && scrollEl !== null && scrollEl.nodeType !== 8) scrollViewSize = getScrollDetails(scrollEl, getVirtualScrollEl(), beforeRef.value, afterRef.value, props.virtualScrollHorizontal, $q.lang.rtl, props.virtualScrollStickySizeStart, props.virtualScrollStickySizeEnd).scrollViewSize;
			}
			localScrollViewSize = scrollViewSize;
			const virtualScrollSliceRatioBefore = Number.parseFloat(props.virtualScrollSliceRatioBefore) || 0;
			const virtualScrollSliceRatioAfter = Number.parseFloat(props.virtualScrollSliceRatioAfter) || 0;
			const multiplier = 1 + virtualScrollSliceRatioBefore + virtualScrollSliceRatioAfter;
			const view = scrollViewSize === void 0 || scrollViewSize <= 0 ? 1 : Math.ceil(scrollViewSize / virtualScrollItemSizeComputed.value);
			const baseSize = Math.max(1, view, Math.ceil((props.virtualScrollSliceSize > 0 ? props.virtualScrollSliceSize : 10) / multiplier));
			virtualScrollSliceSizeComputed.value = {
				total: Math.ceil(baseSize * multiplier),
				start: Math.ceil(baseSize * virtualScrollSliceRatioBefore),
				center: Math.ceil(baseSize * (.5 + virtualScrollSliceRatioBefore)),
				end: Math.ceil(baseSize * (1 + virtualScrollSliceRatioBefore)),
				view
			};
		}
		function padVirtualScroll(tag, content) {
			const paddingSize = props.virtualScrollHorizontal ? "width" : "height";
			const style = { ["--q-virtual-scroll-item-" + paddingSize]: virtualScrollItemSizeComputed.value + "px" };
			return [
				tag === "tbody" ? (0, vue.h)(tag, {
					class: "q-virtual-scroll__padding",
					key: "before",
					ref: beforeRef
				}, [(0, vue.h)("tr", [(0, vue.h)("td", {
					style: {
						[paddingSize]: `${virtualScrollPaddingBefore.value}px`,
						...style
					},
					colspan: colspanAttr.value
				})])]) : (0, vue.h)(tag, {
					class: "q-virtual-scroll__padding",
					key: "before",
					ref: beforeRef,
					style: {
						[paddingSize]: `${virtualScrollPaddingBefore.value}px`,
						...style
					}
				}),
				(0, vue.h)(tag, {
					class: "q-virtual-scroll__content",
					key: "content",
					ref: contentRef,
					tabindex: -1
				}, content.flat()),
				tag === "tbody" ? (0, vue.h)(tag, {
					class: "q-virtual-scroll__padding",
					key: "after",
					ref: afterRef
				}, [(0, vue.h)("tr", [(0, vue.h)("td", {
					style: {
						[paddingSize]: `${virtualScrollPaddingAfter.value}px`,
						...style
					},
					colspan: colspanAttr.value
				})])]) : (0, vue.h)(tag, {
					class: "q-virtual-scroll__padding",
					key: "after",
					ref: afterRef,
					style: {
						[paddingSize]: `${virtualScrollPaddingAfter.value}px`,
						...style
					}
				})
			];
		}
		function emitScroll(index) {
			if (prevToIndex !== index) {
				if (props.onVirtualScroll !== void 0) emit("virtualScroll", {
					index,
					from: virtualScrollSliceRange.value.from,
					to: virtualScrollSliceRange.value.to - 1,
					direction: index < prevToIndex ? "decrease" : "increase",
					ref: proxy
				});
				prevToIndex = index;
			}
		}
		setVirtualScrollSize();
		const onVirtualScrollEvt = debounce(localOnVirtualScrollEvt, $q.platform.is.ios ? 120 : 35);
		(0, vue.onBeforeMount)(() => {
			setVirtualScrollSize();
		});
		let shouldActivate = false;
		(0, vue.onDeactivated)(() => {
			shouldActivate = true;
		});
		(0, vue.onActivated)(() => {
			if (!shouldActivate) return;
			const scrollEl = getVirtualScrollTarget();
			if (prevScrollStart !== void 0 && scrollEl !== void 0 && scrollEl !== null && scrollEl.nodeType !== 8) setScroll(scrollEl, prevScrollStart, props.virtualScrollHorizontal, $q.lang.rtl);
			else scrollTo(prevToIndex);
		});
		(0, vue.onBeforeUnmount)(() => {
			onVirtualScrollEvt.cancel();
		});
		Object.assign(proxy, {
			scrollTo,
			reset,
			refresh
		});
		return {
			virtualScrollSliceRange,
			virtualScrollSliceSizeComputed,
			setVirtualScrollSize,
			onVirtualScrollEvt,
			localResetVirtualScroll,
			padVirtualScroll,
			scrollTo,
			reset,
			refresh
		};
	}
	//#endregion
	//#region src/components/select/QSelect.js
	const validateNewValueMode = (v) => [
		"add",
		"add-unique",
		"toggle"
	].includes(v);
	const reEscapeList = ".*+?^${}()|[]\\";
	const fieldPropsList = Object.keys(useFieldProps);
	function getPropValueFn(userPropName, defaultPropName) {
		if (typeof userPropName === "function") return userPropName;
		const propName = userPropName !== void 0 ? userPropName : defaultPropName;
		return (opt) => opt !== null && typeof opt === "object" && propName in opt ? opt[propName] : opt;
	}
	var QSelect_default = createComponent({
		name: "QSelect",
		inheritAttrs: false,
		props: {
			...useVirtualScrollProps,
			...useFormProps,
			...useFieldProps,
			modelValue: { required: true },
			multiple: Boolean,
			displayValue: [String, Number],
			displayValueHtml: Boolean,
			dropdownIcon: String,
			options: {
				type: Array,
				default: () => []
			},
			optionValue: [Function, String],
			optionLabel: [Function, String],
			optionDisable: [Function, String],
			hideSelected: Boolean,
			hideDropdownIcon: Boolean,
			fillInput: Boolean,
			maxValues: [Number, String],
			optionsDense: Boolean,
			optionsDark: {
				type: Boolean,
				default: null
			},
			optionsSelectedClass: String,
			optionsHtml: Boolean,
			optionsCover: Boolean,
			menuShrink: Boolean,
			menuAnchor: String,
			menuSelf: String,
			menuOffset: Array,
			popupContentClass: String,
			popupContentStyle: [
				String,
				Array,
				Object
			],
			popupNoRouteDismiss: Boolean,
			useInput: Boolean,
			useChips: Boolean,
			newValueMode: {
				type: String,
				validator: validateNewValueMode
			},
			mapOptions: Boolean,
			emitValue: Boolean,
			disableTabSelection: Boolean,
			inputDebounce: {
				type: [Number, String],
				default: 500
			},
			inputClass: [
				Array,
				String,
				Object
			],
			inputStyle: [
				Array,
				String,
				Object
			],
			tabindex: {
				type: [String, Number],
				default: 0
			},
			autocomplete: String,
			transitionShow: {},
			transitionHide: {},
			transitionDuration: {},
			behavior: {
				type: String,
				validator: (v) => [
					"default",
					"menu",
					"dialog"
				].includes(v),
				default: "default"
			},
			virtualScrollItemSize: useVirtualScrollProps.virtualScrollItemSize.type,
			onNewValue: Function,
			onFilter: Function
		},
		emits: [
			...useFieldEmits,
			"add",
			"remove",
			"inputValue",
			"keyup",
			"keypress",
			"keydown",
			"popupShow",
			"popupHide",
			"filterAbort"
		],
		setup(props, { slots, emit }) {
			const { proxy } = (0, vue.getCurrentInstance)();
			const { $q } = proxy;
			const menu = (0, vue.ref)(false);
			const dialog = (0, vue.ref)(false);
			const optionIndex = (0, vue.ref)(-1);
			const inputValue = (0, vue.ref)("");
			const dialogFieldFocused = (0, vue.ref)(false);
			const innerLoadingIndicator = (0, vue.ref)(false);
			let filterTimer = null, inputValueTimer = null, innerValueCache, hasDialog, userInputValue, filterId = null, defaultInputValue, transitionShowComputed, searchBuffer, searchBufferExp;
			const inputRef = (0, vue.ref)(null);
			const targetRef = (0, vue.ref)(null);
			const menuRef = (0, vue.ref)(null);
			const dialogRef = (0, vue.ref)(null);
			const menuContentRef = (0, vue.ref)(null);
			const nameProp = useFormInputNameAttr(props);
			const onComposition = useKeyComposition(onInput);
			const virtualScrollLength = (0, vue.computed)(() => Array.isArray(props.options) ? props.options.length : 0);
			const { virtualScrollSliceRange, virtualScrollSliceSizeComputed, localResetVirtualScroll, padVirtualScroll, onVirtualScrollEvt, scrollTo, setVirtualScrollSize } = useVirtualScroll({
				virtualScrollLength,
				getVirtualScrollTarget,
				getVirtualScrollEl,
				virtualScrollItemSizeComputed: (0, vue.computed)(() => props.virtualScrollItemSize === void 0 ? props.optionsDense ? 24 : 48 : props.virtualScrollItemSize)
			});
			const state = useFieldState();
			const innerValue = (0, vue.computed)(() => {
				const mapNull = props.mapOptions && !props.multiple, val = props.modelValue !== void 0 && (props.modelValue !== null || mapNull) ? props.multiple && Array.isArray(props.modelValue) ? props.modelValue : [props.modelValue] : [];
				if (props.mapOptions && Array.isArray(props.options)) {
					const cache = props.mapOptions && innerValueCache !== void 0 ? innerValueCache : [];
					const values = val.map((v) => getOption(v, cache));
					return props.modelValue === null && mapNull ? values.filter((v) => v !== null) : values;
				}
				return val;
			});
			const innerFieldProps = (0, vue.computed)(() => {
				const acc = {};
				fieldPropsList.forEach((key) => {
					const val = props[key];
					if (val !== void 0) acc[key] = val;
				});
				return acc;
			});
			const isOptionsDark = (0, vue.computed)(() => props.optionsDark === null ? state.isDark.value : props.optionsDark);
			const hasValue = (0, vue.computed)(() => fieldValueIsFilled(innerValue.value));
			const computedInputClass = (0, vue.computed)(() => {
				let cls = "q-field__input q-placeholder col";
				if (props.hideSelected || innerValue.value.length === 0) return [cls, props.inputClass];
				cls += " q-field__input--padding";
				return props.inputClass === void 0 ? cls : [cls, props.inputClass];
			});
			const menuContentClass = (0, vue.computed)(() => (props.virtualScrollHorizontal ? "q-virtual-scroll--horizontal" : "") + (props.popupContentClass ? " " + props.popupContentClass : ""));
			const noOptions = (0, vue.computed)(() => virtualScrollLength.value === 0);
			const selectedString = (0, vue.computed)(() => innerValue.value.map((opt) => getOptionLabel.value(opt)).join(", "));
			const ariaCurrentValue = (0, vue.computed)(() => props.displayValue !== void 0 ? props.displayValue : selectedString.value);
			const needsHtmlFn = (0, vue.computed)(() => props.optionsHtml ? () => true : (opt) => opt?.html === true);
			const valueAsHtml = (0, vue.computed)(() => props.displayValueHtml || props.displayValue === void 0 && (props.optionsHtml || innerValue.value.some(needsHtmlFn.value)));
			const tabindex = (0, vue.computed)(() => state.focused.value ? props.tabindex : -1);
			const comboboxAttrs = (0, vue.computed)(() => {
				const attrs = {
					tabindex: props.tabindex,
					role: "combobox",
					"aria-label": props.label,
					"aria-readonly": props.readonly ? "true" : "false",
					"aria-autocomplete": props.useInput ? "list" : "none",
					"aria-expanded": menu.value ? "true" : "false",
					"aria-controls": `${state.targetUid.value}_lb`
				};
				if (optionIndex.value >= 0) attrs["aria-activedescendant"] = `${state.targetUid.value}_${optionIndex.value}`;
				return attrs;
			});
			const listboxAttrs = (0, vue.computed)(() => ({
				id: `${state.targetUid.value}_lb`,
				role: "listbox",
				"aria-multiselectable": props.multiple ? "true" : "false"
			}));
			const selectedScope = (0, vue.computed)(() => innerValue.value.map((opt, i) => ({
				index: i,
				opt,
				html: needsHtmlFn.value(opt),
				selected: true,
				removeAtIndex: removeAtIndexAndFocus,
				toggleOption,
				tabindex: tabindex.value
			})));
			const optionScope = (0, vue.computed)(() => {
				if (virtualScrollLength.value === 0) return [];
				const { from, to } = virtualScrollSliceRange.value;
				return props.options.slice(from, to).map((opt, i) => {
					const disable = isOptionDisabled.value(opt) === true;
					const active = isOptionSelected(opt);
					const index = from + i;
					const itemProps = {
						clickable: true,
						active,
						activeClass: computedOptionsSelectedClass.value,
						manualFocus: true,
						focused: false,
						disable,
						tabindex: -1,
						dense: props.optionsDense,
						dark: isOptionsDark.value,
						role: "option",
						"aria-selected": active ? "true" : "false",
						id: `${state.targetUid.value}_${index}`,
						onClick: () => {
							toggleOption(opt);
						}
					};
					if (!disable) {
						if (optionIndex.value === index) itemProps.focused = true;
						if ($q.platform.is.desktop) itemProps.onMousemove = () => {
							if (menu.value) setOptionIndex(index);
						};
					}
					return {
						index,
						opt,
						html: needsHtmlFn.value(opt),
						label: getOptionLabel.value(opt),
						selected: itemProps.active,
						focused: itemProps.focused,
						toggleOption,
						setOptionIndex,
						itemProps
					};
				});
			});
			const dropdownArrowIcon = (0, vue.computed)(() => props.dropdownIcon !== void 0 ? props.dropdownIcon : $q.iconSet.arrow.dropdown);
			const squaredMenu = (0, vue.computed)(() => !props.optionsCover && !props.outlined && !props.standout && !props.borderless && !props.rounded);
			const computedOptionsSelectedClass = (0, vue.computed)(() => props.optionsSelectedClass !== void 0 ? props.optionsSelectedClass : props.color !== void 0 ? `text-${props.color}` : "");
			const getOptionValue = (0, vue.computed)(() => getPropValueFn(props.optionValue, "value"));
			const getOptionLabel = (0, vue.computed)(() => getPropValueFn(props.optionLabel, "label"));
			const isOptionDisabled = (0, vue.computed)(() => getPropValueFn(props.optionDisable, "disable"));
			const innerOptionsValue = (0, vue.computed)(() => innerValue.value.map(getOptionValue.value));
			const inputControlEvents = (0, vue.computed)(() => {
				const evt = {
					onInput,
					onChange: onComposition,
					onKeydown: onTargetKeydown,
					onKeyup: onTargetAutocomplete,
					onKeypress: onTargetKeypress,
					onFocus: selectInputText,
					onClick(e) {
						if (hasDialog) stop(e);
					}
				};
				evt.onCompositionstart = evt.onCompositionupdate = evt.onCompositionend = onComposition;
				return evt;
			});
			(0, vue.watch)(innerValue, (val) => {
				innerValueCache = val;
				if (props.useInput && props.fillInput && !props.multiple && !state.innerLoading.value && (!dialog.value && !menu.value || !hasValue.value)) {
					if (!userInputValue) resetInputValue();
					if (dialog.value || menu.value) filter("");
				}
			}, { immediate: true });
			(0, vue.watch)(() => props.fillInput, resetInputValue);
			(0, vue.watch)(menu, updateMenu);
			(0, vue.watch)(virtualScrollLength, rerenderMenu);
			function getEmittingOptionValue(opt) {
				return props.emitValue ? getOptionValue.value(opt) : opt;
			}
			function removeAtIndex(index) {
				if (index !== -1 && index < innerValue.value.length) if (props.multiple) {
					const model = [...props.modelValue];
					emit("remove", {
						index,
						value: model.splice(index, 1)[0]
					});
					emit("update:modelValue", model);
				} else emit("update:modelValue", null);
			}
			function removeAtIndexAndFocus(index) {
				removeAtIndex(index);
				state.focus();
			}
			function add(opt, unique) {
				const val = getEmittingOptionValue(opt);
				if (!props.multiple) {
					if (props.fillInput) updateInputValue(getOptionLabel.value(opt), true, true);
					emit("update:modelValue", val);
					return;
				}
				if (innerValue.value.length === 0) {
					emit("add", {
						index: 0,
						value: val
					});
					emit("update:modelValue", props.multiple ? [val] : val);
					return;
				}
				if (unique && isOptionSelected(opt)) return;
				if (props.maxValues !== void 0 && props.modelValue.length >= props.maxValues) return;
				const model = [...props.modelValue];
				emit("add", {
					index: model.length,
					value: val
				});
				model.push(val);
				emit("update:modelValue", model);
			}
			function toggleOption(opt, keepOpen) {
				if (!state.editable.value || opt === void 0 || isOptionDisabled.value(opt) === true) return;
				const optValue = getOptionValue.value(opt);
				if (!props.multiple) {
					if (!keepOpen) {
						updateInputValue(props.fillInput ? getOptionLabel.value(opt) : "", true, true);
						hidePopup();
					}
					targetRef.value?.focus();
					if (innerValue.value.length === 0 || !isDeepEqual(getOptionValue.value(innerValue.value[0]), optValue)) emit("update:modelValue", props.emitValue ? optValue : opt);
					return;
				}
				if (!hasDialog || dialogFieldFocused.value) state.focus();
				selectInputText();
				if (innerValue.value.length === 0) {
					const val = props.emitValue ? optValue : opt;
					emit("add", {
						index: 0,
						value: val
					});
					emit("update:modelValue", props.multiple ? [val] : val);
					return;
				}
				const model = [...props.modelValue], index = innerOptionsValue.value.findIndex((v) => isDeepEqual(v, optValue));
				if (index !== -1) emit("remove", {
					index,
					value: model.splice(index, 1)[0]
				});
				else {
					if (props.maxValues !== void 0 && model.length >= props.maxValues) return;
					const val = props.emitValue ? optValue : opt;
					emit("add", {
						index: model.length,
						value: val
					});
					model.push(val);
				}
				emit("update:modelValue", model);
			}
			function setOptionIndex(index) {
				if (!$q.platform.is.desktop) return;
				const val = index !== -1 && index < virtualScrollLength.value ? index : -1;
				if (optionIndex.value !== val) optionIndex.value = val;
			}
			function moveOptionSelection(localOffset = 1, skipInputValue) {
				if (menu.value) {
					let index = optionIndex.value;
					do
						index = normalizeToInterval(index + localOffset, -1, virtualScrollLength.value - 1);
					while (index !== -1 && index !== optionIndex.value && isOptionDisabled.value(props.options[index]) === true);
					if (optionIndex.value !== index) {
						setOptionIndex(index);
						scrollTo(index);
						if (!skipInputValue && props.useInput && props.fillInput) setInputValue(index >= 0 ? getOptionLabel.value(props.options[index]) : defaultInputValue, true);
					}
				}
			}
			function getOption(value, valueCache) {
				const fn = (opt) => isDeepEqual(getOptionValue.value(opt), value);
				return props.options.find(fn) || valueCache.find(fn) || value;
			}
			function isOptionSelected(opt) {
				const val = getOptionValue.value(opt);
				return innerOptionsValue.value.find((v) => isDeepEqual(v, val)) !== void 0;
			}
			function selectInputText(e) {
				if (props.useInput && targetRef.value !== null && (e === void 0 || targetRef.value === e.target && e.target.value === selectedString.value)) targetRef.value.select();
			}
			function onTargetKeyup(e) {
				if (isKeyCode(e, 27) && menu.value) {
					stop(e);
					hidePopup();
					resetInputValue();
				}
				emit("keyup", e);
			}
			function onTargetAutocomplete(e) {
				const { value } = e.target;
				if (e.keyCode !== void 0) {
					onTargetKeyup(e);
					return;
				}
				e.target.value = "";
				if (filterTimer !== null) {
					clearTimeout(filterTimer);
					filterTimer = null;
				}
				if (inputValueTimer !== null) {
					clearTimeout(inputValueTimer);
					inputValueTimer = null;
				}
				resetInputValue();
				if (typeof value === "string" && value.length !== 0) {
					const needle = value.toLocaleLowerCase();
					const findFn = (extractFn) => {
						const option = props.options.find((opt) => String(extractFn.value(opt)).toLocaleLowerCase() === needle);
						if (option === void 0) return false;
						if (innerValue.value.includes(option)) hidePopup();
						else toggleOption(option);
						return true;
					};
					const fillFn = (afterFilter) => {
						if (!findFn(getOptionValue) && !afterFilter && !findFn(getOptionLabel)) filter(value, true, () => fillFn(true));
					};
					fillFn();
				} else state.clearValue(e);
			}
			function onTargetKeypress(e) {
				emit("keypress", e);
			}
			function onTargetKeydown(e) {
				emit("keydown", e);
				if (shouldIgnoreKey(e)) return;
				const newValueModeValid = inputValue.value.length !== 0 && (props.newValueMode !== void 0 || props.onNewValue !== void 0);
				const tabShouldSelect = !e.shiftKey && !props.disableTabSelection && !props.multiple && (optionIndex.value !== -1 || newValueModeValid);
				if (e.keyCode === 27) {
					prevent(e);
					return;
				}
				if (e.keyCode === 9 && !tabShouldSelect) {
					closeMenu();
					return;
				}
				if (e.target === void 0 || e.target.id !== state.targetUid.value || !state.editable.value) return;
				if (e.keyCode === 40 && !state.innerLoading.value && !menu.value) {
					stopAndPrevent(e);
					showPopup();
					return;
				}
				if (e.keyCode === 8 && (props.useChips || props.clearable) && !props.hideSelected && inputValue.value.length === 0) {
					if (props.multiple && Array.isArray(props.modelValue)) removeAtIndex(props.modelValue.length - 1);
					else if (!props.multiple && props.modelValue !== null) emit("update:modelValue", null);
					return;
				}
				if ((e.keyCode === 35 || e.keyCode === 36) && (typeof inputValue.value !== "string" || inputValue.value.length === 0)) {
					stopAndPrevent(e);
					optionIndex.value = -1;
					moveOptionSelection(e.keyCode === 36 ? 1 : -1, props.multiple);
				}
				if ((e.keyCode === 33 || e.keyCode === 34) && virtualScrollSliceSizeComputed.value !== void 0) {
					stopAndPrevent(e);
					optionIndex.value = Math.max(-1, Math.min(virtualScrollLength.value, optionIndex.value + (e.keyCode === 33 ? -1 : 1) * virtualScrollSliceSizeComputed.value.view));
					moveOptionSelection(e.keyCode === 33 ? 1 : -1, props.multiple);
				}
				if (e.keyCode === 38 || e.keyCode === 40) {
					stopAndPrevent(e);
					moveOptionSelection(e.keyCode === 38 ? -1 : 1, props.multiple);
				}
				const optionsLength = virtualScrollLength.value;
				if (searchBuffer === void 0 || searchBufferExp < Date.now()) searchBuffer = "";
				if (optionsLength > 0 && !props.useInput && e.key !== void 0 && e.key.length === 1 && !e.altKey && !e.ctrlKey && !e.metaKey && (e.keyCode !== 32 || searchBuffer.length !== 0)) {
					if (!menu.value) showPopup(e);
					const char = e.key.toLocaleLowerCase(), keyRepeat = searchBuffer.length === 1 && searchBuffer[0] === char;
					searchBufferExp = Date.now() + 1500;
					if (!keyRepeat) {
						stopAndPrevent(e);
						searchBuffer += char;
					}
					const searchRe = new RegExp("^" + [...searchBuffer].map((l) => reEscapeList.includes(l) ? "\\" + l : l).join(".*"), "i");
					let index = optionIndex.value;
					if (keyRepeat || index < 0 || !searchRe.test(getOptionLabel.value(props.options[index]))) do
						index = normalizeToInterval(index + 1, -1, optionsLength - 1);
					while (index !== optionIndex.value && (isOptionDisabled.value(props.options[index]) === true || !searchRe.test(getOptionLabel.value(props.options[index]))));
					if (optionIndex.value !== index) (0, vue.nextTick)(() => {
						setOptionIndex(index);
						scrollTo(index);
						if (index >= 0 && props.useInput && props.fillInput) setInputValue(getOptionLabel.value(props.options[index]), true);
					});
					return;
				}
				if (e.keyCode !== 13 && (e.keyCode !== 32 || props.useInput || searchBuffer !== "") && (e.keyCode !== 9 || !tabShouldSelect)) return;
				if (e.keyCode !== 9) stopAndPrevent(e);
				if (optionIndex.value !== -1 && optionIndex.value < optionsLength) {
					toggleOption(props.options[optionIndex.value]);
					return;
				}
				if (newValueModeValid) {
					const done = (val, mode) => {
						if (mode) {
							if (!validateNewValueMode(mode)) return;
						} else mode = props.newValueMode;
						updateInputValue("", !props.multiple, true);
						if (val === void 0 || val === null) return;
						(mode === "toggle" ? toggleOption : add)(val, mode === "add-unique");
						if (!props.multiple) {
							targetRef.value?.focus();
							hidePopup();
						}
					};
					if (props.onNewValue !== void 0) emit("newValue", inputValue.value, done);
					else done(inputValue.value);
					if (!props.multiple) return;
				}
				if (menu.value) closeMenu();
				else if (!state.innerLoading.value) showPopup();
			}
			function getVirtualScrollEl() {
				return hasDialog ? menuContentRef.value : menuRef.value !== null && menuRef.value.contentEl !== null ? menuRef.value.contentEl : void 0;
			}
			function getVirtualScrollTarget() {
				return getVirtualScrollEl();
			}
			function getSelection() {
				if (props.hideSelected) return [];
				if (slots["selected-item"] !== void 0) return selectedScope.value.map((scope) => slots["selected-item"](scope));
				if (slots.selected !== void 0) return [slots.selected()].flat();
				if (props.useChips) return selectedScope.value.map((scope, i) => (0, vue.h)(QChip_default, {
					key: "option-" + i,
					removable: state.editable.value && isOptionDisabled.value(scope.opt) !== true,
					dense: true,
					textColor: props.color,
					tabindex: tabindex.value,
					onRemove() {
						scope.removeAtIndex(i);
					}
				}, () => (0, vue.h)("span", {
					class: "ellipsis",
					[scope.html ? "innerHTML" : "textContent"]: getOptionLabel.value(scope.opt)
				})));
				return [(0, vue.h)("span", {
					class: "ellipsis",
					[valueAsHtml.value ? "innerHTML" : "textContent"]: ariaCurrentValue.value
				})];
			}
			function getAllOptions() {
				if (noOptions.value) return slots["no-option"] !== void 0 ? slots["no-option"]({ inputValue: inputValue.value }) : void 0;
				const fn = slots.option !== void 0 ? slots.option : (scope) => (0, vue.h)(QItem_default, {
					key: scope.index,
					...scope.itemProps
				}, () => (0, vue.h)(QItemSection_default, () => (0, vue.h)(QItemLabel_default, () => (0, vue.h)("span", { [scope.html ? "innerHTML" : "textContent"]: scope.label }))));
				let options = padVirtualScroll("div", optionScope.value.map(fn));
				if (slots["before-options"] !== void 0) options = [slots["before-options"](), ...options].flat();
				return hMergeSlot(slots["after-options"], options);
			}
			function getInput(fromDialog, isTarget) {
				const attrs = isTarget ? {
					...comboboxAttrs.value,
					...state.splitAttrs.attributes.value
				} : void 0;
				const data = {
					ref: isTarget ? targetRef : void 0,
					key: "i_t",
					class: computedInputClass.value,
					style: props.inputStyle,
					value: inputValue.value !== void 0 ? inputValue.value : "",
					type: "search",
					...attrs,
					id: isTarget ? state.targetUid.value : void 0,
					maxlength: props.maxlength,
					autocomplete: props.autocomplete,
					"data-autofocus": fromDialog === true || props.autofocus || void 0,
					disabled: props.disable,
					readonly: props.readonly,
					...inputControlEvents.value
				};
				if (!fromDialog && hasDialog) if (Array.isArray(data.class)) data.class = [...data.class, "no-pointer-events"];
				else data.class += " no-pointer-events";
				return (0, vue.h)("input", data);
			}
			function onInput(e) {
				if (filterTimer !== null) {
					clearTimeout(filterTimer);
					filterTimer = null;
				}
				if (inputValueTimer !== null) {
					clearTimeout(inputValueTimer);
					inputValueTimer = null;
				}
				if (e?.target?.qComposing) return;
				setInputValue(e.target.value || "");
				userInputValue = true;
				defaultInputValue = inputValue.value;
				if (!state.focused.value && (!hasDialog || dialogFieldFocused.value)) state.focus();
				if (props.onFilter !== void 0) filterTimer = setTimeout(() => {
					filterTimer = null;
					filter(inputValue.value);
				}, props.inputDebounce);
			}
			function setInputValue(val, emitImmediately) {
				if (inputValue.value !== val) {
					inputValue.value = val;
					if (emitImmediately || props.inputDebounce === 0 || props.inputDebounce === "0") emit("inputValue", val);
					else inputValueTimer = setTimeout(() => {
						inputValueTimer = null;
						emit("inputValue", val);
					}, props.inputDebounce);
				}
			}
			function updateInputValue(val, noFiltering, internal) {
				userInputValue = internal !== true;
				if (props.useInput) {
					setInputValue(val, true);
					if (noFiltering || userInputValue) defaultInputValue = val;
					if (!noFiltering) filter(val);
				}
			}
			function filter(val, keepClosed, afterUpdateFn) {
				if (props.onFilter === void 0 || !keepClosed && !state.focused.value) return;
				if (state.innerLoading.value) emit("filterAbort");
				else {
					state.innerLoading.value = true;
					innerLoadingIndicator.value = true;
				}
				if (val !== "" && !props.multiple && innerValue.value.length !== 0 && !userInputValue && val === getOptionLabel.value(innerValue.value[0])) val = "";
				const localFilterId = setTimeout(() => {
					if (menu.value) menu.value = false;
				}, 10);
				if (filterId !== null) clearTimeout(filterId);
				filterId = localFilterId;
				emit("filter", val, (fn, afterFn) => {
					if ((keepClosed || state.focused.value) && filterId === localFilterId) {
						clearTimeout(filterId);
						if (typeof fn === "function") fn();
						innerLoadingIndicator.value = false;
						(0, vue.nextTick)(() => {
							state.innerLoading.value = false;
							if (state.editable.value) if (keepClosed) {
								if (menu.value) hidePopup();
							} else if (menu.value) updateMenu(true);
							else menu.value = true;
							if (typeof afterFn === "function") (0, vue.nextTick)(() => {
								afterFn(proxy);
							});
							if (typeof afterUpdateFn === "function") (0, vue.nextTick)(() => {
								afterUpdateFn(proxy);
							});
						});
					}
				}, () => {
					if (state.focused.value && filterId === localFilterId) {
						clearTimeout(filterId);
						state.innerLoading.value = false;
						innerLoadingIndicator.value = false;
					}
					if (menu.value) menu.value = false;
				});
			}
			function getMenu() {
				return (0, vue.h)(QMenu_default, {
					ref: menuRef,
					class: menuContentClass.value,
					style: props.popupContentStyle,
					modelValue: menu.value,
					fit: !props.menuShrink,
					cover: props.optionsCover && !noOptions.value && !props.useInput,
					anchor: props.menuAnchor,
					self: props.menuSelf,
					offset: props.menuOffset,
					dark: isOptionsDark.value,
					noParentEvent: true,
					noRefocus: true,
					noFocus: true,
					noRouteDismiss: props.popupNoRouteDismiss,
					square: squaredMenu.value,
					transitionShow: props.transitionShow,
					transitionHide: props.transitionHide,
					transitionDuration: props.transitionDuration,
					separateClosePopup: true,
					...listboxAttrs.value,
					onScrollPassive: onVirtualScrollEvt,
					onBeforeShow: onControlPopupShow,
					onBeforeHide: onMenuBeforeHide,
					onShow: onMenuShow
				}, getAllOptions);
			}
			function onMenuBeforeHide(e) {
				onControlPopupHide(e);
				closeMenu();
			}
			function onMenuShow() {
				setVirtualScrollSize();
			}
			function onDialogFieldFocus(e) {
				stop(e);
				targetRef.value?.focus();
				dialogFieldFocused.value = true;
				window.scrollTo(window.pageXOffset || window.scrollX || document.body.scrollLeft || 0, 0);
			}
			function onDialogFieldBlur(e) {
				stop(e);
				(0, vue.nextTick)(() => {
					dialogFieldFocused.value = false;
				});
			}
			function getDialog() {
				const content = [(0, vue.h)(QField_default, {
					class: `col-auto ${state.fieldClass.value}`,
					...innerFieldProps.value,
					for: state.targetUid.value,
					dark: isOptionsDark.value,
					square: true,
					loading: innerLoadingIndicator.value,
					itemAligned: false,
					filled: true,
					stackLabel: inputValue.value.length !== 0,
					...state.splitAttrs.listeners.value,
					onFocus: onDialogFieldFocus,
					onBlur: onDialogFieldBlur
				}, {
					...slots,
					rawControl: () => state.getControl(true),
					before: void 0,
					after: void 0
				})];
				if (menu.value) content.push((0, vue.h)("div", {
					ref: menuContentRef,
					class: menuContentClass.value + " scroll",
					style: props.popupContentStyle,
					...listboxAttrs.value,
					onClick: prevent,
					onScrollPassive: onVirtualScrollEvt
				}, getAllOptions()));
				return (0, vue.h)(QDialog_default, {
					ref: dialogRef,
					modelValue: dialog.value,
					position: props.useInput ? "top" : void 0,
					transitionShow: transitionShowComputed,
					transitionHide: props.transitionHide,
					transitionDuration: props.transitionDuration,
					noRouteDismiss: props.popupNoRouteDismiss,
					onBeforeShow: onControlPopupShow,
					onBeforeHide: onDialogBeforeHide,
					onHide: onDialogHide,
					onShow: onDialogShow
				}, () => (0, vue.h)("div", { class: "q-select__dialog" + (isOptionsDark.value ? " q-select__dialog--dark q-dark" : "") + (dialogFieldFocused.value ? " q-select__dialog--focused" : "") }, content));
			}
			function onDialogBeforeHide(e) {
				onControlPopupHide(e);
				if (dialogRef.value !== null) dialogRef.value.__updateRefocusTarget(state.rootRef.value.querySelector(".q-field__native > [tabindex]:last-child"));
				state.focused.value = false;
			}
			function onDialogHide(e) {
				hidePopup();
				if (!state.focused.value) emit("blur", e);
				resetInputValue();
			}
			function onDialogShow() {
				const el = document.activeElement;
				if ((el === null || el.id !== state.targetUid.value) && targetRef.value !== null && targetRef.value !== el) targetRef.value.focus();
				setVirtualScrollSize();
			}
			function closeMenu() {
				if (dialog.value) return;
				optionIndex.value = -1;
				if (menu.value) menu.value = false;
				if (!state.focused.value) {
					if (filterId !== null) {
						clearTimeout(filterId);
						filterId = null;
					}
					if (state.innerLoading.value) {
						emit("filterAbort");
						state.innerLoading.value = false;
						innerLoadingIndicator.value = false;
					}
				}
			}
			function showPopup(e) {
				if (!state.editable.value) return;
				if (hasDialog) {
					state.onControlFocusin(e);
					dialog.value = true;
					(0, vue.nextTick)(() => {
						state.focus();
					});
				} else state.focus();
				if (props.onFilter !== void 0) filter(inputValue.value);
				else if (!noOptions.value || slots["no-option"] !== void 0) menu.value = true;
			}
			function hidePopup() {
				dialog.value = false;
				closeMenu();
			}
			function resetInputValue() {
				if (props.useInput) updateInputValue(!props.multiple && props.fillInput && innerValue.value.length !== 0 ? getOptionLabel.value(innerValue.value[0]) || "" : "", true, true);
			}
			function updateMenu(show) {
				let localOptionIndex = -1;
				if (show) {
					if (innerValue.value.length !== 0) {
						const val = getOptionValue.value(innerValue.value[0]);
						localOptionIndex = props.options.findIndex((v) => isDeepEqual(getOptionValue.value(v), val));
					}
					localResetVirtualScroll(localOptionIndex);
				}
				setOptionIndex(localOptionIndex);
			}
			function rerenderMenu(newLength, oldLength) {
				if (menu.value && !state.innerLoading.value) {
					localResetVirtualScroll(-1, true);
					(0, vue.nextTick)(() => {
						if (menu.value && !state.innerLoading.value) if (newLength > oldLength) localResetVirtualScroll();
						else updateMenu(true);
					});
				}
			}
			function updateMenuPosition() {
				if (!dialog.value) menuRef.value?.updatePosition();
			}
			function onControlPopupShow(e) {
				if (e !== void 0) stop(e);
				emit("popupShow", e);
				state.hasPopupOpen = true;
				state.onControlFocusin(e);
			}
			function onControlPopupHide(e) {
				if (e !== void 0) stop(e);
				emit("popupHide", e);
				state.hasPopupOpen = false;
				state.onControlFocusout(e);
			}
			function updatePreState() {
				hasDialog = !$q.platform.is.mobile && props.behavior !== "dialog" ? false : props.behavior !== "menu" && (props.useInput ? slots["no-option"] !== void 0 || props.onFilter !== void 0 || !noOptions.value : true);
				transitionShowComputed = $q.platform.is.ios && hasDialog && props.useInput ? "fade" : props.transitionShow;
			}
			(0, vue.onBeforeUpdate)(updatePreState);
			(0, vue.onUpdated)(updateMenuPosition);
			updatePreState();
			(0, vue.onBeforeUnmount)(() => {
				if (filterTimer !== null) clearTimeout(filterTimer);
				if (inputValueTimer !== null) clearTimeout(inputValueTimer);
			});
			Object.assign(proxy, {
				showPopup,
				hidePopup,
				removeAtIndex,
				add,
				toggleOption,
				getOptionIndex: () => optionIndex.value,
				setOptionIndex,
				moveOptionSelection,
				filter,
				updateMenuPosition,
				updateInputValue,
				isOptionSelected,
				getEmittingOptionValue,
				isOptionDisabled: (...args) => isOptionDisabled.value(...args) === true,
				getOptionValue: (...args) => getOptionValue.value(...args),
				getOptionLabel: (...args) => getOptionLabel.value(...args)
			});
			Object.assign(state, {
				innerValue,
				fieldClass: (0, vue.computed)(() => `q-select q-field--auto-height q-select--with${props.useInput ? "" : "out"}-input q-select--with${props.useChips ? "" : "out"}-chips q-select--${props.multiple ? "multiple" : "single"}`),
				inputRef,
				targetRef,
				hasValue,
				showPopup,
				floatingLabel: (0, vue.computed)(() => !props.hideSelected && hasValue.value || typeof inputValue.value === "number" || inputValue.value.length !== 0 || fieldValueIsFilled(props.displayValue)),
				getControlChild: () => {
					if (state.editable.value && (dialog.value || !noOptions.value || slots["no-option"] !== void 0)) return hasDialog ? getDialog() : getMenu();
					else if (state.hasPopupOpen) state.hasPopupOpen = false;
				},
				controlEvents: {
					onFocusin(e) {
						state.onControlFocusin(e);
					},
					onFocusout(e) {
						state.onControlFocusout(e, () => {
							resetInputValue();
							closeMenu();
						});
					},
					onClick(e) {
						prevent(e);
						if (!hasDialog && menu.value) {
							closeMenu();
							targetRef.value?.focus();
							return;
						}
						showPopup(e);
					}
				},
				getControl: (fromDialog) => {
					const child = getSelection();
					const isTarget = fromDialog === true || !dialog.value || !hasDialog;
					if (props.useInput) child.push(getInput(fromDialog, isTarget));
					else if (state.editable.value) {
						const attrs = isTarget ? comboboxAttrs.value : void 0;
						child.push((0, vue.h)("input", {
							ref: isTarget ? targetRef : void 0,
							key: "d_t",
							class: "q-select__focus-target",
							id: isTarget ? state.targetUid.value : void 0,
							value: ariaCurrentValue.value,
							readonly: true,
							"data-autofocus": fromDialog === true || props.autofocus || void 0,
							...attrs,
							onKeydown: onTargetKeydown,
							onKeyup: onTargetKeyup,
							onKeypress: onTargetKeypress
						}));
						if (isTarget && typeof props.autocomplete === "string" && props.autocomplete.length !== 0) child.push((0, vue.h)("input", {
							class: "q-select__autocomplete-input",
							autocomplete: props.autocomplete,
							tabindex: -1,
							onKeyup: onTargetAutocomplete
						}));
					}
					if (nameProp.value !== void 0 && !props.disable && innerOptionsValue.value.length !== 0) {
						const opts = innerOptionsValue.value.map((value) => (0, vue.h)("option", {
							value,
							selected: true
						}));
						child.push((0, vue.h)("select", {
							class: "hidden",
							name: nameProp.value,
							multiple: props.multiple
						}, opts));
					}
					return (0, vue.h)("div", {
						class: "q-field__native row items-center",
						...props.useInput || !isTarget ? void 0 : state.splitAttrs.attributes.value,
						...state.splitAttrs.listeners.value
					}, child);
				},
				getInnerAppend: () => !props.loading && !innerLoadingIndicator.value && !props.hideDropdownIcon ? [(0, vue.h)(QIcon_default, {
					class: "q-select__dropdown-icon" + (menu.value ? " rotate-180" : ""),
					name: dropdownArrowIcon.value
				})] : null
			});
			return useField(state);
		}
	});
	//#endregion
	//#region src/components/skeleton/QSkeleton.js
	const skeletonTypes = [
		"text",
		"rect",
		"circle",
		"QBtn",
		"QBadge",
		"QChip",
		"QToolbar",
		"QCheckbox",
		"QRadio",
		"QToggle",
		"QSlider",
		"QRange",
		"QInput",
		"QAvatar"
	];
	const skeletonAnimations = [
		"wave",
		"pulse",
		"pulse-x",
		"pulse-y",
		"fade",
		"blink",
		"none"
	];
	var QSkeleton_default = createComponent({
		name: "QSkeleton",
		props: {
			...useDarkProps,
			tag: {
				type: String,
				default: "div"
			},
			type: {
				type: String,
				validator: (v) => skeletonTypes.includes(v),
				default: "rect"
			},
			animation: {
				type: String,
				validator: (v) => skeletonAnimations.includes(v),
				default: "wave"
			},
			animationSpeed: {
				type: [String, Number],
				default: 1500
			},
			square: Boolean,
			bordered: Boolean,
			size: String,
			width: String,
			height: String
		},
		setup(props, { slots }) {
			const isDark = useDark(props, (0, vue.getCurrentInstance)().proxy.$q);
			const style = (0, vue.computed)(() => {
				const size = props.size !== void 0 ? [props.size, props.size] : [props.width, props.height];
				return {
					"--q-skeleton-speed": `${props.animationSpeed}ms`,
					width: size[0],
					height: size[1]
				};
			});
			const classes = (0, vue.computed)(() => `q-skeleton q-skeleton--${isDark.value ? "dark" : "light"} q-skeleton--type-${props.type}` + (props.animation !== "none" ? ` q-skeleton--anim q-skeleton--anim-${props.animation}` : "") + (props.square ? " q-skeleton--square" : "") + (props.bordered ? " q-skeleton--bordered" : ""));
			return () => (0, vue.h)(props.tag, {
				class: classes.value,
				style: style.value
			}, hSlot(slots.default));
		}
	});
	//#endregion
	//#region src/components/slide-item/QSlideItem.js
	const slotsDef = [
		[
			"left",
			"center",
			"start",
			"width"
		],
		[
			"right",
			"center",
			"end",
			"width"
		],
		[
			"top",
			"start",
			"center",
			"height"
		],
		[
			"bottom",
			"end",
			"center",
			"height"
		]
	];
	var QSlideItem_default = createComponent({
		name: "QSlideItem",
		props: {
			...useDarkProps,
			leftColor: String,
			rightColor: String,
			topColor: String,
			bottomColor: String,
			onSlide: Function
		},
		emits: [
			"action",
			"top",
			"right",
			"bottom",
			"left"
		],
		setup(props, { slots, emit }) {
			const { proxy } = (0, vue.getCurrentInstance)();
			const { $q } = proxy;
			const isDark = useDark(props, $q);
			const { getCache } = useRenderCache();
			const contentRef = (0, vue.ref)(null);
			let timer = null, pan = {}, dirRefs = {}, dirContentRefs = {};
			const langDir = (0, vue.computed)(() => $q.lang.rtl ? {
				left: "right",
				right: "left"
			} : {
				left: "left",
				right: "right"
			});
			const classes = (0, vue.computed)(() => "q-slide-item q-item-type overflow-hidden" + (isDark.value ? " q-slide-item--dark q-dark" : ""));
			function reset() {
				contentRef.value.style.transform = "translate(0,0)";
			}
			function emitSlide(side, ratio, isReset) {
				if (props.onSlide !== void 0) emit("slide", {
					side,
					ratio,
					isReset
				});
			}
			function onPan(evt) {
				const node = contentRef.value;
				if (evt.isFirst) {
					pan = {
						dir: null,
						size: {
							left: 0,
							right: 0,
							top: 0,
							bottom: 0
						},
						scale: 0
					};
					node.classList.add("no-transition");
					slotsDef.forEach((slotName) => {
						if (slots[slotName[0]] !== void 0) {
							const localNode = dirContentRefs[slotName[0]];
							localNode.style.transform = "scale(1)";
							pan.size[slotName[0]] = localNode.getBoundingClientRect()[slotName[3]];
						}
					});
					pan.axis = evt.direction === "up" || evt.direction === "down" ? "Y" : "X";
				} else if (evt.isFinal) {
					node.classList.remove("no-transition");
					if (pan.scale === 1) {
						node.style.transform = `translate${pan.axis}(${pan.dir * 100}%)`;
						if (timer !== null) clearTimeout(timer);
						const showing = pan.showing;
						timer = setTimeout(() => {
							timer = null;
							emit(showing, { reset });
							emit("action", {
								side: showing,
								reset
							});
						}, 230);
					} else {
						node.style.transform = "translate(0,0)";
						emitSlide(pan.showing, 0, true);
					}
					return;
				} else evt.direction = pan.axis === "X" ? evt.offset.x < 0 ? "left" : "right" : evt.offset.y < 0 ? "up" : "down";
				if (slots.left === void 0 && evt.direction === langDir.value.right || slots.right === void 0 && evt.direction === langDir.value.left || slots.top === void 0 && evt.direction === "down" || slots.bottom === void 0 && evt.direction === "up") {
					node.style.transform = "translate(0,0)";
					return;
				}
				let showing, dir, dist;
				if (pan.axis === "X") {
					dir = evt.direction === "left" ? -1 : 1;
					showing = dir === 1 ? langDir.value.left : langDir.value.right;
					dist = evt.distance.x;
				} else {
					dir = evt.direction === "up" ? -2 : 2;
					showing = dir === 2 ? "top" : "bottom";
					dist = evt.distance.y;
				}
				if (pan.dir !== null && Math.abs(dir) !== Math.abs(pan.dir)) return;
				if (pan.dir !== dir) {
					[
						"left",
						"right",
						"top",
						"bottom"
					].forEach((d) => {
						if (dirRefs[d]) dirRefs[d].style.visibility = showing === d ? "visible" : "hidden";
					});
					pan.showing = showing;
					pan.dir = dir;
				}
				pan.scale = Math.max(0, Math.min(1, (dist - 40) / pan.size[showing]));
				node.style.transform = `translate${pan.axis}(${dist * dir / Math.abs(dir)}px)`;
				dirContentRefs[showing].style.transform = `scale(${pan.scale})`;
				emitSlide(showing, pan.scale, false);
			}
			(0, vue.onBeforeUpdate)(() => {
				dirRefs = {};
				dirContentRefs = {};
			});
			(0, vue.onBeforeUnmount)(() => {
				if (timer !== null) clearTimeout(timer);
			});
			Object.assign(proxy, { reset });
			return () => {
				const content = [], slotsList = {
					left: slots[langDir.value.right] !== void 0,
					right: slots[langDir.value.left] !== void 0,
					up: slots.bottom !== void 0,
					down: slots.top !== void 0
				}, dirs = Object.keys(slotsList).filter((key) => slotsList[key]);
				slotsDef.forEach((slotName) => {
					const dir = slotName[0];
					if (slots[dir] !== void 0) content.push((0, vue.h)("div", {
						key: dir,
						ref: (el) => {
							dirRefs[dir] = el;
						},
						class: `q-slide-item__${dir} absolute-full row no-wrap items-${slotName[1]} justify-${slotName[2]}` + (props[dir + "Color"] !== void 0 ? ` bg-${props[dir + "Color"]}` : "")
					}, [(0, vue.h)("div", { ref: (el) => {
						dirContentRefs[dir] = el;
					} }, slots[dir]())]));
				});
				const node = (0, vue.h)("div", {
					key: `${dirs.length === 0 ? "only-" : ""} content`,
					ref: contentRef,
					class: "q-slide-item__content"
				}, hSlot(slots.default));
				if (dirs.length === 0) content.push(node);
				else content.push((0, vue.withDirectives)(node, getCache("dir#" + dirs.join(""), () => {
					const modifiers = {
						prevent: true,
						stop: true,
						mouse: true
					};
					dirs.forEach((dir) => {
						modifiers[dir] = true;
					});
					return [[
						TouchPan_default,
						onPan,
						void 0,
						modifiers
					]];
				})));
				return (0, vue.h)("div", { class: classes.value }, content);
			};
		}
	});
	//#endregion
	//#region src/components/space/QSpace.js
	var QSpace_default = createComponent({
		name: "QSpace",
		setup() {
			const space = (0, vue.h)("div", { class: "q-space" });
			return () => space;
		}
	});
	//#endregion
	//#region src/components/spinner/QSpinnerAudio.js
	const innerHTML$21 = "<g transform=\"matrix(1 0 0 -1 0 80)\"><rect width=\"10\" height=\"20\" rx=\"3\"><animate attributeName=\"height\" begin=\"0s\" dur=\"4.3s\" values=\"20;45;57;80;64;32;66;45;64;23;66;13;64;56;34;34;2;23;76;79;20\" calcMode=\"linear\" repeatCount=\"indefinite\"></animate></rect><rect x=\"15\" width=\"10\" height=\"80\" rx=\"3\"><animate attributeName=\"height\" begin=\"0s\" dur=\"2s\" values=\"80;55;33;5;75;23;73;33;12;14;60;80\" calcMode=\"linear\" repeatCount=\"indefinite\"></animate></rect><rect x=\"30\" width=\"10\" height=\"50\" rx=\"3\"><animate attributeName=\"height\" begin=\"0s\" dur=\"1.4s\" values=\"50;34;78;23;56;23;34;76;80;54;21;50\" calcMode=\"linear\" repeatCount=\"indefinite\"></animate></rect><rect x=\"45\" width=\"10\" height=\"30\" rx=\"3\"><animate attributeName=\"height\" begin=\"0s\" dur=\"2s\" values=\"30;45;13;80;56;72;45;76;34;23;67;30\" calcMode=\"linear\" repeatCount=\"indefinite\"></animate></rect></g>";
	var QSpinnerAudio_default = createComponent({
		name: "QSpinnerAudio",
		props: useSpinnerProps,
		setup(props) {
			const { cSize, classes } = useSpinner(props);
			return () => (0, vue.h)("svg", {
				class: classes.value,
				fill: "currentColor",
				width: cSize.value,
				height: cSize.value,
				viewBox: "0 0 55 80",
				xmlns: "http://www.w3.org/2000/svg",
				innerHTML: innerHTML$21
			});
		}
	});
	//#endregion
	//#region src/components/spinner/QSpinnerBall.js
	const innerHTML$20 = "<g transform=\"translate(1 1)\" stroke-width=\"2\" fill=\"none\" fill-rule=\"evenodd\"><circle cx=\"5\" cy=\"50\" r=\"5\"><animate attributeName=\"cy\" begin=\"0s\" dur=\"2.2s\" values=\"50;5;50;50\" calcMode=\"linear\" repeatCount=\"indefinite\"></animate><animate attributeName=\"cx\" begin=\"0s\" dur=\"2.2s\" values=\"5;27;49;5\" calcMode=\"linear\" repeatCount=\"indefinite\"></animate></circle><circle cx=\"27\" cy=\"5\" r=\"5\"><animate attributeName=\"cy\" begin=\"0s\" dur=\"2.2s\" from=\"5\" to=\"5\" values=\"5;50;50;5\" calcMode=\"linear\" repeatCount=\"indefinite\"></animate><animate attributeName=\"cx\" begin=\"0s\" dur=\"2.2s\" from=\"27\" to=\"27\" values=\"27;49;5;27\" calcMode=\"linear\" repeatCount=\"indefinite\"></animate></circle><circle cx=\"49\" cy=\"50\" r=\"5\"><animate attributeName=\"cy\" begin=\"0s\" dur=\"2.2s\" values=\"50;50;5;50\" calcMode=\"linear\" repeatCount=\"indefinite\"></animate><animate attributeName=\"cx\" from=\"49\" to=\"49\" begin=\"0s\" dur=\"2.2s\" values=\"49;5;27;49\" calcMode=\"linear\" repeatCount=\"indefinite\"></animate></circle></g>";
	var QSpinnerBall_default = createComponent({
		name: "QSpinnerBall",
		props: useSpinnerProps,
		setup(props) {
			const { cSize, classes } = useSpinner(props);
			return () => (0, vue.h)("svg", {
				class: classes.value,
				stroke: "currentColor",
				width: cSize.value,
				height: cSize.value,
				viewBox: "0 0 57 57",
				xmlns: "http://www.w3.org/2000/svg",
				innerHTML: innerHTML$20
			});
		}
	});
	//#endregion
	//#region src/components/spinner/QSpinnerBars.js
	const innerHTML$19 = "<rect y=\"10\" width=\"15\" height=\"120\" rx=\"6\"><animate attributeName=\"height\" begin=\"0.5s\" dur=\"1s\" values=\"120;110;100;90;80;70;60;50;40;140;120\" calcMode=\"linear\" repeatCount=\"indefinite\"></animate><animate attributeName=\"y\" begin=\"0.5s\" dur=\"1s\" values=\"10;15;20;25;30;35;40;45;50;0;10\" calcMode=\"linear\" repeatCount=\"indefinite\"></animate></rect><rect x=\"30\" y=\"10\" width=\"15\" height=\"120\" rx=\"6\"><animate attributeName=\"height\" begin=\"0.25s\" dur=\"1s\" values=\"120;110;100;90;80;70;60;50;40;140;120\" calcMode=\"linear\" repeatCount=\"indefinite\"></animate><animate attributeName=\"y\" begin=\"0.25s\" dur=\"1s\" values=\"10;15;20;25;30;35;40;45;50;0;10\" calcMode=\"linear\" repeatCount=\"indefinite\"></animate></rect><rect x=\"60\" width=\"15\" height=\"140\" rx=\"6\"><animate attributeName=\"height\" begin=\"0s\" dur=\"1s\" values=\"120;110;100;90;80;70;60;50;40;140;120\" calcMode=\"linear\" repeatCount=\"indefinite\"></animate><animate attributeName=\"y\" begin=\"0s\" dur=\"1s\" values=\"10;15;20;25;30;35;40;45;50;0;10\" calcMode=\"linear\" repeatCount=\"indefinite\"></animate></rect><rect x=\"90\" y=\"10\" width=\"15\" height=\"120\" rx=\"6\"><animate attributeName=\"height\" begin=\"0.25s\" dur=\"1s\" values=\"120;110;100;90;80;70;60;50;40;140;120\" calcMode=\"linear\" repeatCount=\"indefinite\"></animate><animate attributeName=\"y\" begin=\"0.25s\" dur=\"1s\" values=\"10;15;20;25;30;35;40;45;50;0;10\" calcMode=\"linear\" repeatCount=\"indefinite\"></animate></rect><rect x=\"120\" y=\"10\" width=\"15\" height=\"120\" rx=\"6\"><animate attributeName=\"height\" begin=\"0.5s\" dur=\"1s\" values=\"120;110;100;90;80;70;60;50;40;140;120\" calcMode=\"linear\" repeatCount=\"indefinite\"></animate><animate attributeName=\"y\" begin=\"0.5s\" dur=\"1s\" values=\"10;15;20;25;30;35;40;45;50;0;10\" calcMode=\"linear\" repeatCount=\"indefinite\"></animate></rect>";
	var QSpinnerBars_default = createComponent({
		name: "QSpinnerBars",
		props: useSpinnerProps,
		setup(props) {
			const { cSize, classes } = useSpinner(props);
			return () => (0, vue.h)("svg", {
				class: classes.value,
				fill: "currentColor",
				width: cSize.value,
				height: cSize.value,
				viewBox: "0 0 135 140",
				xmlns: "http://www.w3.org/2000/svg",
				innerHTML: innerHTML$19
			});
		}
	});
	//#endregion
	//#region src/components/spinner/QSpinnerBox.js
	const innerHTML$18 = "<rect x=\"25\" y=\"25\" width=\"50\" height=\"50\" fill=\"none\" stroke-width=\"4\" stroke=\"currentColor\"><animateTransform id=\"spinnerBox\" attributeName=\"transform\" type=\"rotate\" from=\"0 50 50\" to=\"180 50 50\" dur=\"0.5s\" begin=\"rectBox.end\"></animateTransform></rect><rect x=\"27\" y=\"27\" width=\"46\" height=\"50\" fill=\"currentColor\"><animate id=\"rectBox\" attributeName=\"height\" begin=\"0s;spinnerBox.end\" dur=\"1.3s\" from=\"50\" to=\"0\" fill=\"freeze\"></animate></rect>";
	var QSpinnerBox_default = createComponent({
		name: "QSpinnerBox",
		props: useSpinnerProps,
		setup(props) {
			const { cSize, classes } = useSpinner(props);
			return () => (0, vue.h)("svg", {
				class: classes.value,
				width: cSize.value,
				height: cSize.value,
				viewBox: "0 0 100 100",
				preserveAspectRatio: "xMidYMid",
				xmlns: "http://www.w3.org/2000/svg",
				innerHTML: innerHTML$18
			});
		}
	});
	//#endregion
	//#region src/components/spinner/QSpinnerClock.js
	const innerHTML$17 = "<circle cx=\"50\" cy=\"50\" r=\"48\" fill=\"none\" stroke-width=\"4\" stroke-miterlimit=\"10\" stroke=\"currentColor\"></circle><line stroke-linecap=\"round\" stroke-width=\"4\" stroke-miterlimit=\"10\" stroke=\"currentColor\" x1=\"50\" y1=\"50\" x2=\"85\" y2=\"50.5\"><animateTransform attributeName=\"transform\" type=\"rotate\" from=\"0 50 50\" to=\"360 50 50\" dur=\"2s\" repeatCount=\"indefinite\"></animateTransform></line><line stroke-linecap=\"round\" stroke-width=\"4\" stroke-miterlimit=\"10\" stroke=\"currentColor\" x1=\"50\" y1=\"50\" x2=\"49.5\" y2=\"74\"><animateTransform attributeName=\"transform\" type=\"rotate\" from=\"0 50 50\" to=\"360 50 50\" dur=\"15s\" repeatCount=\"indefinite\"></animateTransform></line>";
	var QSpinnerClock_default = createComponent({
		name: "QSpinnerClock",
		props: useSpinnerProps,
		setup(props) {
			const { cSize, classes } = useSpinner(props);
			return () => (0, vue.h)("svg", {
				class: classes.value,
				width: cSize.value,
				height: cSize.value,
				viewBox: "0 0 100 100",
				preserveAspectRatio: "xMidYMid",
				xmlns: "http://www.w3.org/2000/svg",
				innerHTML: innerHTML$17
			});
		}
	});
	//#endregion
	//#region src/components/spinner/QSpinnerComment.js
	const innerHTML$16 = "<rect x=\"0\" y=\"0\" width=\"100\" height=\"100\" fill=\"none\"></rect><path d=\"M78,19H22c-6.6,0-12,5.4-12,12v31c0,6.6,5.4,12,12,12h37.2c0.4,3,1.8,5.6,3.7,7.6c2.4,2.5,5.1,4.1,9.1,4 c-1.4-2.1-2-7.2-2-10.3c0-0.4,0-0.8,0-1.3h8c6.6,0,12-5.4,12-12V31C90,24.4,84.6,19,78,19z\" fill=\"currentColor\"></path><circle cx=\"30\" cy=\"47\" r=\"5\" fill=\"#fff\"><animate attributeName=\"opacity\" from=\"0\" to=\"1\" values=\"0;1;1\" keyTimes=\"0;0.2;1\" dur=\"1s\" repeatCount=\"indefinite\"></animate></circle><circle cx=\"50\" cy=\"47\" r=\"5\" fill=\"#fff\"><animate attributeName=\"opacity\" from=\"0\" to=\"1\" values=\"0;0;1;1\" keyTimes=\"0;0.2;0.4;1\" dur=\"1s\" repeatCount=\"indefinite\"></animate></circle><circle cx=\"70\" cy=\"47\" r=\"5\" fill=\"#fff\"><animate attributeName=\"opacity\" from=\"0\" to=\"1\" values=\"0;0;1;1\" keyTimes=\"0;0.4;0.6;1\" dur=\"1s\" repeatCount=\"indefinite\"></animate></circle>";
	var QSpinnerComment_default = createComponent({
		name: "QSpinnerComment",
		props: useSpinnerProps,
		setup(props) {
			const { cSize, classes } = useSpinner(props);
			return () => (0, vue.h)("svg", {
				class: classes.value,
				width: cSize.value,
				height: cSize.value,
				xmlns: "http://www.w3.org/2000/svg",
				viewBox: "0 0 100 100",
				preserveAspectRatio: "xMidYMid",
				innerHTML: innerHTML$16
			});
		}
	});
	//#endregion
	//#region src/components/spinner/QSpinnerCube.js
	const innerHTML$15 = "<rect x=\"0\" y=\"0\" width=\"100\" height=\"100\" fill=\"none\"></rect><g transform=\"translate(25 25)\"><rect x=\"-20\" y=\"-20\" width=\"40\" height=\"40\" fill=\"currentColor\" opacity=\"0.9\"><animateTransform attributeName=\"transform\" type=\"scale\" from=\"1.5\" to=\"1\" repeatCount=\"indefinite\" begin=\"0s\" dur=\"1s\" calcMode=\"spline\" keySplines=\"0.2 0.8 0.2 0.8\" keyTimes=\"0;1\"></animateTransform></rect></g><g transform=\"translate(75 25)\"><rect x=\"-20\" y=\"-20\" width=\"40\" height=\"40\" fill=\"currentColor\" opacity=\"0.8\"><animateTransform attributeName=\"transform\" type=\"scale\" from=\"1.5\" to=\"1\" repeatCount=\"indefinite\" begin=\"0.1s\" dur=\"1s\" calcMode=\"spline\" keySplines=\"0.2 0.8 0.2 0.8\" keyTimes=\"0;1\"></animateTransform></rect></g><g transform=\"translate(25 75)\"><rect x=\"-20\" y=\"-20\" width=\"40\" height=\"40\" fill=\"currentColor\" opacity=\"0.7\"><animateTransform attributeName=\"transform\" type=\"scale\" from=\"1.5\" to=\"1\" repeatCount=\"indefinite\" begin=\"0.3s\" dur=\"1s\" calcMode=\"spline\" keySplines=\"0.2 0.8 0.2 0.8\" keyTimes=\"0;1\"></animateTransform></rect></g><g transform=\"translate(75 75)\"><rect x=\"-20\" y=\"-20\" width=\"40\" height=\"40\" fill=\"currentColor\" opacity=\"0.6\"><animateTransform attributeName=\"transform\" type=\"scale\" from=\"1.5\" to=\"1\" repeatCount=\"indefinite\" begin=\"0.2s\" dur=\"1s\" calcMode=\"spline\" keySplines=\"0.2 0.8 0.2 0.8\" keyTimes=\"0;1\"></animateTransform></rect></g>";
	var QSpinnerCube_default = createComponent({
		name: "QSpinnerCube",
		props: useSpinnerProps,
		setup(props) {
			const { cSize, classes } = useSpinner(props);
			return () => (0, vue.h)("svg", {
				class: classes.value,
				width: cSize.value,
				height: cSize.value,
				xmlns: "http://www.w3.org/2000/svg",
				viewBox: "0 0 100 100",
				preserveAspectRatio: "xMidYMid",
				innerHTML: innerHTML$15
			});
		}
	});
	//#endregion
	//#region src/components/spinner/QSpinnerDots.js
	const innerHTML$14 = "<circle cx=\"15\" cy=\"15\" r=\"15\"><animate attributeName=\"r\" from=\"15\" to=\"15\" begin=\"0s\" dur=\"0.8s\" values=\"15;9;15\" calcMode=\"linear\" repeatCount=\"indefinite\"></animate><animate attributeName=\"fill-opacity\" from=\"1\" to=\"1\" begin=\"0s\" dur=\"0.8s\" values=\"1;.5;1\" calcMode=\"linear\" repeatCount=\"indefinite\"></animate></circle><circle cx=\"60\" cy=\"15\" r=\"9\" fill-opacity=\".3\"><animate attributeName=\"r\" from=\"9\" to=\"9\" begin=\"0s\" dur=\"0.8s\" values=\"9;15;9\" calcMode=\"linear\" repeatCount=\"indefinite\"></animate><animate attributeName=\"fill-opacity\" from=\".5\" to=\".5\" begin=\"0s\" dur=\"0.8s\" values=\".5;1;.5\" calcMode=\"linear\" repeatCount=\"indefinite\"></animate></circle><circle cx=\"105\" cy=\"15\" r=\"15\"><animate attributeName=\"r\" from=\"15\" to=\"15\" begin=\"0s\" dur=\"0.8s\" values=\"15;9;15\" calcMode=\"linear\" repeatCount=\"indefinite\"></animate><animate attributeName=\"fill-opacity\" from=\"1\" to=\"1\" begin=\"0s\" dur=\"0.8s\" values=\"1;.5;1\" calcMode=\"linear\" repeatCount=\"indefinite\"></animate></circle>";
	var QSpinnerDots_default = createComponent({
		name: "QSpinnerDots",
		props: useSpinnerProps,
		setup(props) {
			const { cSize, classes } = useSpinner(props);
			return () => (0, vue.h)("svg", {
				class: classes.value,
				fill: "currentColor",
				width: cSize.value,
				height: cSize.value,
				viewBox: "0 0 120 30",
				xmlns: "http://www.w3.org/2000/svg",
				innerHTML: innerHTML$14
			});
		}
	});
	//#endregion
	//#region src/components/spinner/QSpinnerFacebook.js
	const innerHTML$13 = "<g transform=\"translate(20 50)\"><rect x=\"-10\" y=\"-30\" width=\"20\" height=\"60\" fill=\"currentColor\" opacity=\"0.6\"><animateTransform attributeName=\"transform\" type=\"scale\" from=\"2\" to=\"1\" begin=\"0s\" repeatCount=\"indefinite\" dur=\"1s\" calcMode=\"spline\" keySplines=\"0.1 0.9 0.4 1\" keyTimes=\"0;1\" values=\"2;1\"></animateTransform></rect></g><g transform=\"translate(50 50)\"><rect x=\"-10\" y=\"-30\" width=\"20\" height=\"60\" fill=\"currentColor\" opacity=\"0.8\"><animateTransform attributeName=\"transform\" type=\"scale\" from=\"2\" to=\"1\" begin=\"0.1s\" repeatCount=\"indefinite\" dur=\"1s\" calcMode=\"spline\" keySplines=\"0.1 0.9 0.4 1\" keyTimes=\"0;1\" values=\"2;1\"></animateTransform></rect></g><g transform=\"translate(80 50)\"><rect x=\"-10\" y=\"-30\" width=\"20\" height=\"60\" fill=\"currentColor\" opacity=\"0.9\"><animateTransform attributeName=\"transform\" type=\"scale\" from=\"2\" to=\"1\" begin=\"0.2s\" repeatCount=\"indefinite\" dur=\"1s\" calcMode=\"spline\" keySplines=\"0.1 0.9 0.4 1\" keyTimes=\"0;1\" values=\"2;1\"></animateTransform></rect></g>";
	var QSpinnerFacebook_default = createComponent({
		name: "QSpinnerFacebook",
		props: useSpinnerProps,
		setup(props) {
			const { cSize, classes } = useSpinner(props);
			return () => (0, vue.h)("svg", {
				class: classes.value,
				width: cSize.value,
				height: cSize.value,
				viewBox: "0 0 100 100",
				xmlns: "http://www.w3.org/2000/svg",
				preserveAspectRatio: "xMidYMid",
				innerHTML: innerHTML$13
			});
		}
	});
	//#endregion
	//#region src/components/spinner/QSpinnerGears.js
	const innerHTML$12 = "<g transform=\"translate(-20,-20)\"><path d=\"M79.9,52.6C80,51.8,80,50.9,80,50s0-1.8-0.1-2.6l-5.1-0.4c-0.3-2.4-0.9-4.6-1.8-6.7l4.2-2.9c-0.7-1.6-1.6-3.1-2.6-4.5 L70,35c-1.4-1.9-3.1-3.5-4.9-4.9l2.2-4.6c-1.4-1-2.9-1.9-4.5-2.6L59.8,27c-2.1-0.9-4.4-1.5-6.7-1.8l-0.4-5.1C51.8,20,50.9,20,50,20 s-1.8,0-2.6,0.1l-0.4,5.1c-2.4,0.3-4.6,0.9-6.7,1.8l-2.9-4.1c-1.6,0.7-3.1,1.6-4.5,2.6l2.1,4.6c-1.9,1.4-3.5,3.1-5,4.9l-4.5-2.1 c-1,1.4-1.9,2.9-2.6,4.5l4.1,2.9c-0.9,2.1-1.5,4.4-1.8,6.8l-5,0.4C20,48.2,20,49.1,20,50s0,1.8,0.1,2.6l5,0.4 c0.3,2.4,0.9,4.7,1.8,6.8l-4.1,2.9c0.7,1.6,1.6,3.1,2.6,4.5l4.5-2.1c1.4,1.9,3.1,3.5,5,4.9l-2.1,4.6c1.4,1,2.9,1.9,4.5,2.6l2.9-4.1 c2.1,0.9,4.4,1.5,6.7,1.8l0.4,5.1C48.2,80,49.1,80,50,80s1.8,0,2.6-0.1l0.4-5.1c2.3-0.3,4.6-0.9,6.7-1.8l2.9,4.2 c1.6-0.7,3.1-1.6,4.5-2.6L65,69.9c1.9-1.4,3.5-3,4.9-4.9l4.6,2.2c1-1.4,1.9-2.9,2.6-4.5L73,59.8c0.9-2.1,1.5-4.4,1.8-6.7L79.9,52.6 z M50,65c-8.3,0-15-6.7-15-15c0-8.3,6.7-15,15-15s15,6.7,15,15C65,58.3,58.3,65,50,65z\" fill=\"currentColor\"><animateTransform attributeName=\"transform\" type=\"rotate\" from=\"90 50 50\" to=\"0 50 50\" dur=\"1s\" repeatCount=\"indefinite\"></animateTransform></path></g><g transform=\"translate(20,20) rotate(15 50 50)\"><path d=\"M79.9,52.6C80,51.8,80,50.9,80,50s0-1.8-0.1-2.6l-5.1-0.4c-0.3-2.4-0.9-4.6-1.8-6.7l4.2-2.9c-0.7-1.6-1.6-3.1-2.6-4.5 L70,35c-1.4-1.9-3.1-3.5-4.9-4.9l2.2-4.6c-1.4-1-2.9-1.9-4.5-2.6L59.8,27c-2.1-0.9-4.4-1.5-6.7-1.8l-0.4-5.1C51.8,20,50.9,20,50,20 s-1.8,0-2.6,0.1l-0.4,5.1c-2.4,0.3-4.6,0.9-6.7,1.8l-2.9-4.1c-1.6,0.7-3.1,1.6-4.5,2.6l2.1,4.6c-1.9,1.4-3.5,3.1-5,4.9l-4.5-2.1 c-1,1.4-1.9,2.9-2.6,4.5l4.1,2.9c-0.9,2.1-1.5,4.4-1.8,6.8l-5,0.4C20,48.2,20,49.1,20,50s0,1.8,0.1,2.6l5,0.4 c0.3,2.4,0.9,4.7,1.8,6.8l-4.1,2.9c0.7,1.6,1.6,3.1,2.6,4.5l4.5-2.1c1.4,1.9,3.1,3.5,5,4.9l-2.1,4.6c1.4,1,2.9,1.9,4.5,2.6l2.9-4.1 c2.1,0.9,4.4,1.5,6.7,1.8l0.4,5.1C48.2,80,49.1,80,50,80s1.8,0,2.6-0.1l0.4-5.1c2.3-0.3,4.6-0.9,6.7-1.8l2.9,4.2 c1.6-0.7,3.1-1.6,4.5-2.6L65,69.9c1.9-1.4,3.5-3,4.9-4.9l4.6,2.2c1-1.4,1.9-2.9,2.6-4.5L73,59.8c0.9-2.1,1.5-4.4,1.8-6.7L79.9,52.6 z M50,65c-8.3,0-15-6.7-15-15c0-8.3,6.7-15,15-15s15,6.7,15,15C65,58.3,58.3,65,50,65z\" fill=\"currentColor\"><animateTransform attributeName=\"transform\" type=\"rotate\" from=\"0 50 50\" to=\"90 50 50\" dur=\"1s\" repeatCount=\"indefinite\"></animateTransform></path></g>";
	var QSpinnerGears_default = createComponent({
		name: "QSpinnerGears",
		props: useSpinnerProps,
		setup(props) {
			const { cSize, classes } = useSpinner(props);
			return () => (0, vue.h)("svg", {
				class: classes.value,
				width: cSize.value,
				height: cSize.value,
				viewBox: "0 0 100 100",
				preserveAspectRatio: "xMidYMid",
				xmlns: "http://www.w3.org/2000/svg",
				innerHTML: innerHTML$12
			});
		}
	});
	//#endregion
	//#region src/components/spinner/QSpinnerGrid.js
	const innerHTML$11 = "<circle cx=\"12.5\" cy=\"12.5\" r=\"12.5\"><animate attributeName=\"fill-opacity\" begin=\"0s\" dur=\"1s\" values=\"1;.2;1\" calcMode=\"linear\" repeatCount=\"indefinite\"></animate></circle><circle cx=\"12.5\" cy=\"52.5\" r=\"12.5\" fill-opacity=\".5\"><animate attributeName=\"fill-opacity\" begin=\"100ms\" dur=\"1s\" values=\"1;.2;1\" calcMode=\"linear\" repeatCount=\"indefinite\"></animate></circle><circle cx=\"52.5\" cy=\"12.5\" r=\"12.5\"><animate attributeName=\"fill-opacity\" begin=\"300ms\" dur=\"1s\" values=\"1;.2;1\" calcMode=\"linear\" repeatCount=\"indefinite\"></animate></circle><circle cx=\"52.5\" cy=\"52.5\" r=\"12.5\"><animate attributeName=\"fill-opacity\" begin=\"600ms\" dur=\"1s\" values=\"1;.2;1\" calcMode=\"linear\" repeatCount=\"indefinite\"></animate></circle><circle cx=\"92.5\" cy=\"12.5\" r=\"12.5\"><animate attributeName=\"fill-opacity\" begin=\"800ms\" dur=\"1s\" values=\"1;.2;1\" calcMode=\"linear\" repeatCount=\"indefinite\"></animate></circle><circle cx=\"92.5\" cy=\"52.5\" r=\"12.5\"><animate attributeName=\"fill-opacity\" begin=\"400ms\" dur=\"1s\" values=\"1;.2;1\" calcMode=\"linear\" repeatCount=\"indefinite\"></animate></circle><circle cx=\"12.5\" cy=\"92.5\" r=\"12.5\"><animate attributeName=\"fill-opacity\" begin=\"700ms\" dur=\"1s\" values=\"1;.2;1\" calcMode=\"linear\" repeatCount=\"indefinite\"></animate></circle><circle cx=\"52.5\" cy=\"92.5\" r=\"12.5\"><animate attributeName=\"fill-opacity\" begin=\"500ms\" dur=\"1s\" values=\"1;.2;1\" calcMode=\"linear\" repeatCount=\"indefinite\"></animate></circle><circle cx=\"92.5\" cy=\"92.5\" r=\"12.5\"><animate attributeName=\"fill-opacity\" begin=\"200ms\" dur=\"1s\" values=\"1;.2;1\" calcMode=\"linear\" repeatCount=\"indefinite\"></animate></circle>";
	var QSpinnerGrid_default = createComponent({
		name: "QSpinnerGrid",
		props: useSpinnerProps,
		setup(props) {
			const { cSize, classes } = useSpinner(props);
			return () => (0, vue.h)("svg", {
				class: classes.value,
				fill: "currentColor",
				width: cSize.value,
				height: cSize.value,
				viewBox: "0 0 105 105",
				xmlns: "http://www.w3.org/2000/svg",
				innerHTML: innerHTML$11
			});
		}
	});
	//#endregion
	//#region src/components/spinner/QSpinnerHearts.js
	const innerHTML$10 = "<path d=\"M30.262 57.02L7.195 40.723c-5.84-3.976-7.56-12.06-3.842-18.063 3.715-6 11.467-7.65 17.306-3.68l4.52 3.76 2.6-5.274c3.716-6.002 11.47-7.65 17.304-3.68 5.84 3.97 7.56 12.054 3.842 18.062L34.49 56.118c-.897 1.512-2.793 1.915-4.228.9z\" fill-opacity=\".5\"><animate attributeName=\"fill-opacity\" begin=\"0s\" dur=\"1.4s\" values=\"0.5;1;0.5\" calcMode=\"linear\" repeatCount=\"indefinite\"></animate></path><path d=\"M105.512 56.12l-14.44-24.272c-3.716-6.008-1.996-14.093 3.843-18.062 5.835-3.97 13.588-2.322 17.306 3.68l2.6 5.274 4.52-3.76c5.84-3.97 13.593-2.32 17.308 3.68 3.718 6.003 1.998 14.088-3.842 18.064L109.74 57.02c-1.434 1.014-3.33.61-4.228-.9z\" fill-opacity=\".5\"><animate attributeName=\"fill-opacity\" begin=\"0.7s\" dur=\"1.4s\" values=\"0.5;1;0.5\" calcMode=\"linear\" repeatCount=\"indefinite\"></animate></path><path d=\"M67.408 57.834l-23.01-24.98c-5.864-6.15-5.864-16.108 0-22.248 5.86-6.14 15.37-6.14 21.234 0L70 16.168l4.368-5.562c5.863-6.14 15.375-6.14 21.235 0 5.863 6.14 5.863 16.098 0 22.247l-23.007 24.98c-1.43 1.556-3.757 1.556-5.188 0z\"></path>";
	var QSpinnerHearts_default = createComponent({
		name: "QSpinnerHearts",
		props: useSpinnerProps,
		setup(props) {
			const { cSize, classes } = useSpinner(props);
			return () => (0, vue.h)("svg", {
				class: classes.value,
				fill: "currentColor",
				width: cSize.value,
				height: cSize.value,
				viewBox: "0 0 140 64",
				xmlns: "http://www.w3.org/2000/svg",
				innerHTML: innerHTML$10
			});
		}
	});
	//#endregion
	//#region src/components/spinner/QSpinnerHourglass.js
	const innerHTML$9 = "<g><path fill=\"none\" stroke=\"currentColor\" stroke-width=\"5\" stroke-miterlimit=\"10\" d=\"M58.4,51.7c-0.9-0.9-1.4-2-1.4-2.3s0.5-0.4,1.4-1.4 C70.8,43.8,79.8,30.5,80,15.5H70H30H20c0.2,15,9.2,28.1,21.6,32.3c0.9,0.9,1.4,1.2,1.4,1.5s-0.5,1.6-1.4,2.5 C29.2,56.1,20.2,69.5,20,85.5h10h40h10C79.8,69.5,70.8,55.9,58.4,51.7z\"></path><clipPath id=\"uil-hourglass-clip1\"><rect x=\"15\" y=\"20\" width=\"70\" height=\"25\"><animate attributeName=\"height\" from=\"25\" to=\"0\" dur=\"1s\" repeatCount=\"indefinite\" values=\"25;0;0\" keyTimes=\"0;0.5;1\"></animate><animate attributeName=\"y\" from=\"20\" to=\"45\" dur=\"1s\" repeatCount=\"indefinite\" values=\"20;45;45\" keyTimes=\"0;0.5;1\"></animate></rect></clipPath><clipPath id=\"uil-hourglass-clip2\"><rect x=\"15\" y=\"55\" width=\"70\" height=\"25\"><animate attributeName=\"height\" from=\"0\" to=\"25\" dur=\"1s\" repeatCount=\"indefinite\" values=\"0;25;25\" keyTimes=\"0;0.5;1\"></animate><animate attributeName=\"y\" from=\"80\" to=\"55\" dur=\"1s\" repeatCount=\"indefinite\" values=\"80;55;55\" keyTimes=\"0;0.5;1\"></animate></rect></clipPath><path d=\"M29,23c3.1,11.4,11.3,19.5,21,19.5S67.9,34.4,71,23H29z\" clip-path=\"url(#uil-hourglass-clip1)\" fill=\"currentColor\"></path><path d=\"M71.6,78c-3-11.6-11.5-20-21.5-20s-18.5,8.4-21.5,20H71.6z\" clip-path=\"url(#uil-hourglass-clip2)\" fill=\"currentColor\"></path><animateTransform attributeName=\"transform\" type=\"rotate\" from=\"0 50 50\" to=\"180 50 50\" repeatCount=\"indefinite\" dur=\"1s\" values=\"0 50 50;0 50 50;180 50 50\" keyTimes=\"0;0.7;1\"></animateTransform></g>";
	var QSpinnerHourglass_default = createComponent({
		name: "QSpinnerHourglass",
		props: useSpinnerProps,
		setup(props) {
			const { cSize, classes } = useSpinner(props);
			return () => (0, vue.h)("svg", {
				class: classes.value,
				width: cSize.value,
				height: cSize.value,
				viewBox: "0 0 100 100",
				preserveAspectRatio: "xMidYMid",
				xmlns: "http://www.w3.org/2000/svg",
				innerHTML: innerHTML$9
			});
		}
	});
	//#endregion
	//#region src/components/spinner/QSpinnerInfinity.js
	const innerHTML$8 = "<path d=\"M24.3,30C11.4,30,5,43.3,5,50s6.4,20,19.3,20c19.3,0,32.1-40,51.4-40C88.6,30,95,43.3,95,50s-6.4,20-19.3,20C56.4,70,43.6,30,24.3,30z\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"8\" stroke-dasharray=\"10.691205342610678 10.691205342610678\" stroke-dashoffset=\"0\"><animate attributeName=\"stroke-dashoffset\" from=\"0\" to=\"21.382410685221355\" begin=\"0\" dur=\"2s\" repeatCount=\"indefinite\" fill=\"freeze\"></animate></path>";
	var QSpinnerInfinity_default = createComponent({
		name: "QSpinnerInfinity",
		props: useSpinnerProps,
		setup(props) {
			const { cSize, classes } = useSpinner(props);
			return () => (0, vue.h)("svg", {
				class: classes.value,
				width: cSize.value,
				height: cSize.value,
				viewBox: "0 0 100 100",
				preserveAspectRatio: "xMidYMid",
				innerHTML: innerHTML$8
			});
		}
	});
	//#endregion
	//#region src/components/spinner/QSpinnerIos.js
	const innerHTML$7 = "<g stroke-width=\"4\" stroke-linecap=\"round\"><line y1=\"17\" y2=\"29\" transform=\"translate(32,32) rotate(180)\"><animate attributeName=\"stroke-opacity\" dur=\"750ms\" values=\"1;.85;.7;.65;.55;.45;.35;.25;.15;.1;0;1\" repeatCount=\"indefinite\"></animate></line><line y1=\"17\" y2=\"29\" transform=\"translate(32,32) rotate(210)\"><animate attributeName=\"stroke-opacity\" dur=\"750ms\" values=\"0;1;.85;.7;.65;.55;.45;.35;.25;.15;.1;0\" repeatCount=\"indefinite\"></animate></line><line y1=\"17\" y2=\"29\" transform=\"translate(32,32) rotate(240)\"><animate attributeName=\"stroke-opacity\" dur=\"750ms\" values=\".1;0;1;.85;.7;.65;.55;.45;.35;.25;.15;.1\" repeatCount=\"indefinite\"></animate></line><line y1=\"17\" y2=\"29\" transform=\"translate(32,32) rotate(270)\"><animate attributeName=\"stroke-opacity\" dur=\"750ms\" values=\".15;.1;0;1;.85;.7;.65;.55;.45;.35;.25;.15\" repeatCount=\"indefinite\"></animate></line><line y1=\"17\" y2=\"29\" transform=\"translate(32,32) rotate(300)\"><animate attributeName=\"stroke-opacity\" dur=\"750ms\" values=\".25;.15;.1;0;1;.85;.7;.65;.55;.45;.35;.25\" repeatCount=\"indefinite\"></animate></line><line y1=\"17\" y2=\"29\" transform=\"translate(32,32) rotate(330)\"><animate attributeName=\"stroke-opacity\" dur=\"750ms\" values=\".35;.25;.15;.1;0;1;.85;.7;.65;.55;.45;.35\" repeatCount=\"indefinite\"></animate></line><line y1=\"17\" y2=\"29\" transform=\"translate(32,32) rotate(0)\"><animate attributeName=\"stroke-opacity\" dur=\"750ms\" values=\".45;.35;.25;.15;.1;0;1;.85;.7;.65;.55;.45\" repeatCount=\"indefinite\"></animate></line><line y1=\"17\" y2=\"29\" transform=\"translate(32,32) rotate(30)\"><animate attributeName=\"stroke-opacity\" dur=\"750ms\" values=\".55;.45;.35;.25;.15;.1;0;1;.85;.7;.65;.55\" repeatCount=\"indefinite\"></animate></line><line y1=\"17\" y2=\"29\" transform=\"translate(32,32) rotate(60)\"><animate attributeName=\"stroke-opacity\" dur=\"750ms\" values=\".65;.55;.45;.35;.25;.15;.1;0;1;.85;.7;.65\" repeatCount=\"indefinite\"></animate></line><line y1=\"17\" y2=\"29\" transform=\"translate(32,32) rotate(90)\"><animate attributeName=\"stroke-opacity\" dur=\"750ms\" values=\".7;.65;.55;.45;.35;.25;.15;.1;0;1;.85;.7\" repeatCount=\"indefinite\"></animate></line><line y1=\"17\" y2=\"29\" transform=\"translate(32,32) rotate(120)\"><animate attributeName=\"stroke-opacity\" dur=\"750ms\" values=\".85;.7;.65;.55;.45;.35;.25;.15;.1;0;1;.85\" repeatCount=\"indefinite\"></animate></line><line y1=\"17\" y2=\"29\" transform=\"translate(32,32) rotate(150)\"><animate attributeName=\"stroke-opacity\" dur=\"750ms\" values=\"1;.85;.7;.65;.55;.45;.35;.25;.15;.1;0;1\" repeatCount=\"indefinite\"></animate></line></g>";
	var QSpinnerIos_default = createComponent({
		name: "QSpinnerIos",
		props: useSpinnerProps,
		setup(props) {
			const { cSize, classes } = useSpinner(props);
			return () => (0, vue.h)("svg", {
				class: classes.value,
				width: cSize.value,
				height: cSize.value,
				stroke: "currentColor",
				fill: "currentColor",
				viewBox: "0 0 64 64",
				innerHTML: innerHTML$7
			});
		}
	});
	//#endregion
	//#region src/components/spinner/QSpinnerOrbit.js
	const innerHTML$6 = "<circle cx=\"50\" cy=\"50\" r=\"44\" fill=\"none\" stroke-width=\"4\" stroke-opacity=\".5\" stroke=\"currentColor\"></circle><circle cx=\"8\" cy=\"54\" r=\"6\" fill=\"currentColor\" stroke-width=\"3\" stroke=\"currentColor\"><animateTransform attributeName=\"transform\" type=\"rotate\" from=\"0 50 48\" to=\"360 50 52\" dur=\"2s\" repeatCount=\"indefinite\"></animateTransform></circle>";
	var QSpinnerOrbit_default = createComponent({
		name: "QSpinnerOrbit",
		props: useSpinnerProps,
		setup(props) {
			const { cSize, classes } = useSpinner(props);
			return () => (0, vue.h)("svg", {
				class: classes.value,
				width: cSize.value,
				height: cSize.value,
				viewBox: "0 0 100 100",
				preserveAspectRatio: "xMidYMid",
				xmlns: "http://www.w3.org/2000/svg",
				innerHTML: innerHTML$6
			});
		}
	});
	//#endregion
	//#region src/components/spinner/QSpinnerOval.js
	const innerHTML$5 = "<g transform=\"translate(1 1)\" stroke-width=\"2\" fill=\"none\" fill-rule=\"evenodd\"><circle stroke-opacity=\".5\" cx=\"18\" cy=\"18\" r=\"18\"></circle><path d=\"M36 18c0-9.94-8.06-18-18-18\"><animateTransform attributeName=\"transform\" type=\"rotate\" from=\"0 18 18\" to=\"360 18 18\" dur=\"1s\" repeatCount=\"indefinite\"></animateTransform></path></g>";
	var QSpinnerOval_default = createComponent({
		name: "QSpinnerOval",
		props: useSpinnerProps,
		setup(props) {
			const { cSize, classes } = useSpinner(props);
			return () => (0, vue.h)("svg", {
				class: classes.value,
				stroke: "currentColor",
				width: cSize.value,
				height: cSize.value,
				viewBox: "0 0 38 38",
				xmlns: "http://www.w3.org/2000/svg",
				innerHTML: innerHTML$5
			});
		}
	});
	//#endregion
	//#region src/components/spinner/QSpinnerPie.js
	const innerHTML$4 = "<path d=\"M0 50A50 50 0 0 1 50 0L50 50L0 50\" fill=\"currentColor\" opacity=\"0.5\"><animateTransform attributeName=\"transform\" type=\"rotate\" from=\"0 50 50\" to=\"360 50 50\" dur=\"0.8s\" repeatCount=\"indefinite\"></animateTransform></path><path d=\"M50 0A50 50 0 0 1 100 50L50 50L50 0\" fill=\"currentColor\" opacity=\"0.5\"><animateTransform attributeName=\"transform\" type=\"rotate\" from=\"0 50 50\" to=\"360 50 50\" dur=\"1.6s\" repeatCount=\"indefinite\"></animateTransform></path><path d=\"M100 50A50 50 0 0 1 50 100L50 50L100 50\" fill=\"currentColor\" opacity=\"0.5\"><animateTransform attributeName=\"transform\" type=\"rotate\" from=\"0 50 50\" to=\"360 50 50\" dur=\"2.4s\" repeatCount=\"indefinite\"></animateTransform></path><path d=\"M50 100A50 50 0 0 1 0 50L50 50L50 100\" fill=\"currentColor\" opacity=\"0.5\"><animateTransform attributeName=\"transform\" type=\"rotate\" from=\"0 50 50\" to=\"360 50 50\" dur=\"3.2s\" repeatCount=\"indefinite\"></animateTransform></path>";
	var QSpinnerPie_default = createComponent({
		name: "QSpinnerPie",
		props: useSpinnerProps,
		setup(props) {
			const { cSize, classes } = useSpinner(props);
			return () => (0, vue.h)("svg", {
				class: classes.value,
				width: cSize.value,
				height: cSize.value,
				viewBox: "0 0 100 100",
				preserveAspectRatio: "xMidYMid",
				xmlns: "http://www.w3.org/2000/svg",
				innerHTML: innerHTML$4
			});
		}
	});
	//#endregion
	//#region src/components/spinner/QSpinnerPuff.js
	const innerHTML$3 = "<g fill=\"none\" fill-rule=\"evenodd\" stroke-width=\"2\"><circle cx=\"22\" cy=\"22\" r=\"1\"><animate attributeName=\"r\" begin=\"0s\" dur=\"1.8s\" values=\"1; 20\" calcMode=\"spline\" keyTimes=\"0; 1\" keySplines=\"0.165, 0.84, 0.44, 1\" repeatCount=\"indefinite\"></animate><animate attributeName=\"stroke-opacity\" begin=\"0s\" dur=\"1.8s\" values=\"1; 0\" calcMode=\"spline\" keyTimes=\"0; 1\" keySplines=\"0.3, 0.61, 0.355, 1\" repeatCount=\"indefinite\"></animate></circle><circle cx=\"22\" cy=\"22\" r=\"1\"><animate attributeName=\"r\" begin=\"-0.9s\" dur=\"1.8s\" values=\"1; 20\" calcMode=\"spline\" keyTimes=\"0; 1\" keySplines=\"0.165, 0.84, 0.44, 1\" repeatCount=\"indefinite\"></animate><animate attributeName=\"stroke-opacity\" begin=\"-0.9s\" dur=\"1.8s\" values=\"1; 0\" calcMode=\"spline\" keyTimes=\"0; 1\" keySplines=\"0.3, 0.61, 0.355, 1\" repeatCount=\"indefinite\"></animate></circle></g>";
	var QSpinnerPuff_default = createComponent({
		name: "QSpinnerPuff",
		props: useSpinnerProps,
		setup(props) {
			const { cSize, classes } = useSpinner(props);
			return () => (0, vue.h)("svg", {
				class: classes.value,
				stroke: "currentColor",
				width: cSize.value,
				height: cSize.value,
				viewBox: "0 0 44 44",
				xmlns: "http://www.w3.org/2000/svg",
				innerHTML: innerHTML$3
			});
		}
	});
	//#endregion
	//#region src/components/spinner/QSpinnerRadio.js
	const innerHTML$2 = "<g transform=\"scale(0.55)\"><circle cx=\"30\" cy=\"150\" r=\"30\" fill=\"currentColor\"><animate attributeName=\"opacity\" from=\"0\" to=\"1\" dur=\"1s\" begin=\"0\" repeatCount=\"indefinite\" keyTimes=\"0;0.5;1\" values=\"0;1;1\"></animate></circle><path d=\"M90,150h30c0-49.7-40.3-90-90-90v30C63.1,90,90,116.9,90,150z\" fill=\"currentColor\"><animate attributeName=\"opacity\" from=\"0\" to=\"1\" dur=\"1s\" begin=\"0.1\" repeatCount=\"indefinite\" keyTimes=\"0;0.5;1\" values=\"0;1;1\"></animate></path><path d=\"M150,150h30C180,67.2,112.8,0,30,0v30C96.3,30,150,83.7,150,150z\" fill=\"currentColor\"><animate attributeName=\"opacity\" from=\"0\" to=\"1\" dur=\"1s\" begin=\"0.2\" repeatCount=\"indefinite\" keyTimes=\"0;0.5;1\" values=\"0;1;1\"></animate></path></g>";
	var QSpinnerRadio_default = createComponent({
		name: "QSpinnerRadio",
		props: useSpinnerProps,
		setup(props) {
			const { cSize, classes } = useSpinner(props);
			return () => (0, vue.h)("svg", {
				class: classes.value,
				width: cSize.value,
				height: cSize.value,
				viewBox: "0 0 100 100",
				preserveAspectRatio: "xMidYMid",
				xmlns: "http://www.w3.org/2000/svg",
				innerHTML: innerHTML$2
			});
		}
	});
	//#endregion
	//#region src/components/spinner/QSpinnerRings.js
	const innerHTML$1 = "<g fill=\"none\" fill-rule=\"evenodd\" transform=\"translate(1 1)\" stroke-width=\"2\"><circle cx=\"22\" cy=\"22\" r=\"6\"><animate attributeName=\"r\" begin=\"1.5s\" dur=\"3s\" values=\"6;22\" calcMode=\"linear\" repeatCount=\"indefinite\"></animate><animate attributeName=\"stroke-opacity\" begin=\"1.5s\" dur=\"3s\" values=\"1;0\" calcMode=\"linear\" repeatCount=\"indefinite\"></animate><animate attributeName=\"stroke-width\" begin=\"1.5s\" dur=\"3s\" values=\"2;0\" calcMode=\"linear\" repeatCount=\"indefinite\"></animate></circle><circle cx=\"22\" cy=\"22\" r=\"6\"><animate attributeName=\"r\" begin=\"3s\" dur=\"3s\" values=\"6;22\" calcMode=\"linear\" repeatCount=\"indefinite\"></animate><animate attributeName=\"stroke-opacity\" begin=\"3s\" dur=\"3s\" values=\"1;0\" calcMode=\"linear\" repeatCount=\"indefinite\"></animate><animate attributeName=\"stroke-width\" begin=\"3s\" dur=\"3s\" values=\"2;0\" calcMode=\"linear\" repeatCount=\"indefinite\"></animate></circle><circle cx=\"22\" cy=\"22\" r=\"8\"><animate attributeName=\"r\" begin=\"0s\" dur=\"1.5s\" values=\"6;1;2;3;4;5;6\" calcMode=\"linear\" repeatCount=\"indefinite\"></animate></circle></g>";
	var QSpinnerRings_default = createComponent({
		name: "QSpinnerRings",
		props: useSpinnerProps,
		setup(props) {
			const { cSize, classes } = useSpinner(props);
			return () => (0, vue.h)("svg", {
				class: classes.value,
				stroke: "currentColor",
				width: cSize.value,
				height: cSize.value,
				viewBox: "0 0 45 45",
				xmlns: "http://www.w3.org/2000/svg",
				innerHTML: innerHTML$1
			});
		}
	});
	//#endregion
	//#region src/components/spinner/QSpinnerTail.js
	const innerHTML = "<defs><linearGradient x1=\"8.042%\" y1=\"0%\" x2=\"65.682%\" y2=\"23.865%\" id=\"a\"><stop stop-color=\"currentColor\" stop-opacity=\"0\" offset=\"0%\"></stop><stop stop-color=\"currentColor\" stop-opacity=\".631\" offset=\"63.146%\"></stop><stop stop-color=\"currentColor\" offset=\"100%\"></stop></linearGradient></defs><g transform=\"translate(1 1)\" fill=\"none\" fill-rule=\"evenodd\"><path d=\"M36 18c0-9.94-8.06-18-18-18\" stroke=\"url(#a)\" stroke-width=\"2\"><animateTransform attributeName=\"transform\" type=\"rotate\" from=\"0 18 18\" to=\"360 18 18\" dur=\"0.9s\" repeatCount=\"indefinite\"></animateTransform></path><circle fill=\"currentColor\" cx=\"36\" cy=\"18\" r=\"1\"><animateTransform attributeName=\"transform\" type=\"rotate\" from=\"0 18 18\" to=\"360 18 18\" dur=\"0.9s\" repeatCount=\"indefinite\"></animateTransform></circle></g>";
	var QSpinnerTail_default = createComponent({
		name: "QSpinnerTail",
		props: useSpinnerProps,
		setup(props) {
			const { cSize, classes } = useSpinner(props);
			return () => (0, vue.h)("svg", {
				class: classes.value,
				width: cSize.value,
				height: cSize.value,
				viewBox: "0 0 38 38",
				xmlns: "http://www.w3.org/2000/svg",
				innerHTML
			});
		}
	});
	//#endregion
	//#region src/components/splitter/QSplitter.js
	var QSplitter_default = createComponent({
		name: "QSplitter",
		props: {
			...useDarkProps,
			modelValue: {
				type: Number,
				required: true
			},
			reverse: Boolean,
			unit: {
				type: String,
				default: "%",
				validator: (v) => ["%", "px"].includes(v)
			},
			limits: {
				type: Array,
				validator: (v) => {
					if (v.length !== 2) return false;
					if (typeof v[0] !== "number" || typeof v[1] !== "number") return false;
					return v[0] >= 0 && v[0] <= v[1];
				}
			},
			emitImmediately: Boolean,
			horizontal: Boolean,
			disable: Boolean,
			beforeClass: [
				Array,
				String,
				Object
			],
			afterClass: [
				Array,
				String,
				Object
			],
			separatorClass: [
				Array,
				String,
				Object
			],
			separatorStyle: [
				Array,
				String,
				Object
			]
		},
		emits: ["update:modelValue"],
		setup(props, { slots, emit }) {
			const { proxy: { $q } } = (0, vue.getCurrentInstance)();
			const isDark = useDark(props, $q);
			const rootRef = (0, vue.ref)(null);
			const sideRefs = {
				before: (0, vue.ref)(null),
				after: (0, vue.ref)(null)
			};
			const classes = (0, vue.computed)(() => `q-splitter no-wrap ${props.horizontal ? "q-splitter--horizontal column" : "q-splitter--vertical row"} q-splitter--${props.disable ? "disabled" : "workable"}` + (isDark.value ? " q-splitter--dark" : ""));
			const propName = (0, vue.computed)(() => props.horizontal ? "height" : "width");
			const side = (0, vue.computed)(() => props.reverse ? "after" : "before");
			const computedLimits = (0, vue.computed)(() => props.limits !== void 0 ? props.limits : props.unit === "%" ? [10, 90] : [50, Infinity]);
			function getCSSValue(value) {
				return (props.unit === "%" ? value : Math.round(value)) + props.unit;
			}
			const styles = (0, vue.computed)(() => ({ [side.value]: { [propName.value]: getCSSValue(props.modelValue) } }));
			let __dir, __maxValue, __value, __multiplier, __normalized;
			function pan(evt) {
				if (evt.isFirst) {
					const size = rootRef.value.getBoundingClientRect()[propName.value];
					__dir = props.horizontal ? "up" : "left";
					__maxValue = props.unit === "%" ? 100 : size;
					__value = Math.min(__maxValue, computedLimits.value[1], Math.max(computedLimits.value[0], props.modelValue));
					__multiplier = (props.reverse ? -1 : 1) * (props.horizontal ? 1 : $q.lang.rtl ? -1 : 1) * (props.unit === "%" ? size === 0 ? 0 : 100 / size : 1);
					rootRef.value.classList.add("q-splitter--active");
					return;
				}
				if (evt.isFinal) {
					if (__normalized !== props.modelValue) emit("update:modelValue", __normalized);
					rootRef.value.classList.remove("q-splitter--active");
					return;
				}
				const val = __value + __multiplier * (evt.direction === __dir ? -1 : 1) * evt.distance[props.horizontal ? "y" : "x"];
				__normalized = Math.min(__maxValue, computedLimits.value[1], Math.max(computedLimits.value[0], val));
				sideRefs[side.value].value.style[propName.value] = getCSSValue(__normalized);
				if (props.emitImmediately && props.modelValue !== __normalized) emit("update:modelValue", __normalized);
			}
			const sepDirective = (0, vue.computed)(() => [[
				TouchPan_default,
				pan,
				void 0,
				{
					[props.horizontal ? "vertical" : "horizontal"]: true,
					prevent: true,
					stop: true,
					mouse: true,
					mouseAllDir: true
				}
			]]);
			function normalize(val, limits) {
				if (val < limits[0]) emit("update:modelValue", limits[0]);
				else if (val > limits[1]) emit("update:modelValue", limits[1]);
			}
			(0, vue.watch)(() => props.modelValue, (v) => {
				normalize(v, computedLimits.value);
			});
			(0, vue.watch)(() => props.limits, () => {
				(0, vue.nextTick)(() => {
					normalize(props.modelValue, computedLimits.value);
				});
			});
			return () => {
				const child = [
					(0, vue.h)("div", {
						ref: sideRefs.before,
						class: ["q-splitter__panel q-splitter__before" + (props.reverse ? " col" : ""), props.beforeClass],
						style: styles.value.before
					}, hSlot(slots.before)),
					(0, vue.h)("div", {
						class: ["q-splitter__separator", props.separatorClass],
						style: props.separatorStyle,
						"aria-disabled": props.disable ? "true" : void 0
					}, [hDir("div", { class: "q-splitter__separator-area absolute-full" }, hSlot(slots.separator), "sep", !props.disable, () => sepDirective.value)]),
					(0, vue.h)("div", {
						ref: sideRefs.after,
						class: ["q-splitter__panel q-splitter__after" + (props.reverse ? "" : " col"), props.afterClass],
						style: styles.value.after
					}, hSlot(slots.after))
				];
				return (0, vue.h)("div", {
					class: classes.value,
					ref: rootRef
				}, hMergeSlot(slots.default, child));
			};
		}
	});
	//#endregion
	//#region src/components/stepper/StepHeader.js
	function preventSpace$1(e) {
		if (e.keyCode === 32) stopAndPrevent(e);
	}
	var StepHeader_default = createComponent({
		name: "StepHeader",
		props: {
			stepper: {},
			step: {},
			goToPanel: Function
		},
		setup(props, { attrs }) {
			const { proxy: { $q } } = (0, vue.getCurrentInstance)();
			const blurRef = (0, vue.ref)(null);
			const isActive = (0, vue.computed)(() => props.stepper.modelValue === props.step.name);
			const isDisable = (0, vue.computed)(() => {
				const opt = props.step.disable;
				return opt === true || opt === "";
			});
			const isError = (0, vue.computed)(() => {
				const opt = props.step.error;
				return opt === true || opt === "";
			});
			const isDone = (0, vue.computed)(() => {
				const opt = props.step.done;
				return !isDisable.value && (opt === true || opt === "");
			});
			const headerNav = (0, vue.computed)(() => {
				const opt = props.step.headerNav;
				return !isDisable.value && props.stepper.headerNav && (opt === true || opt === "" || opt === void 0);
			});
			const hasPrefix = (0, vue.computed)(() => props.step.prefix && (!isActive.value || props.stepper.activeIcon === "none") && (!isError.value || props.stepper.errorIcon === "none") && (!isDone.value || props.stepper.doneIcon === "none"));
			const icon = (0, vue.computed)(() => {
				const defaultIcon = props.step.icon || props.stepper.inactiveIcon;
				if (isActive.value) {
					const localIcon = props.step.activeIcon || props.stepper.activeIcon;
					return localIcon === "none" ? defaultIcon : localIcon || $q.iconSet.stepper.active;
				}
				if (isError.value) {
					const localIcon = props.step.errorIcon || props.stepper.errorIcon;
					return localIcon === "none" ? defaultIcon : localIcon || $q.iconSet.stepper.error;
				}
				if (!isDisable.value && isDone.value) {
					const localIcon = props.step.doneIcon || props.stepper.doneIcon;
					return localIcon === "none" ? defaultIcon : localIcon || $q.iconSet.stepper.done;
				}
				return defaultIcon;
			});
			const color = (0, vue.computed)(() => {
				const errorColor = isError.value ? props.step.errorColor || props.stepper.errorColor : void 0;
				if (isActive.value) {
					const localColor = props.step.activeColor || props.stepper.activeColor || props.step.color;
					return localColor !== void 0 ? localColor : errorColor;
				}
				if (errorColor !== void 0) return errorColor;
				if (!isDisable.value && isDone.value) return props.step.doneColor || props.stepper.doneColor || props.step.color || props.stepper.inactiveColor;
				return props.step.color || props.stepper.inactiveColor;
			});
			const classes = (0, vue.computed)(() => "q-stepper__tab col-grow flex items-center no-wrap relative-position" + (color.value !== void 0 ? ` text-${color.value}` : "") + (isError.value ? " q-stepper__tab--error q-stepper__tab--error-with-" + (hasPrefix.value ? "prefix" : "icon") : "") + (isActive.value ? " q-stepper__tab--active" : "") + (isDone.value ? " q-stepper__tab--done" : "") + (headerNav.value ? " q-stepper__tab--navigation q-focusable q-hoverable" : "") + (isDisable.value ? " q-stepper__tab--disabled" : ""));
			const ripple = (0, vue.computed)(() => props.stepper.headerNav && headerNav.value);
			function onActivate() {
				blurRef.value?.focus();
				if (!isActive.value) props.goToPanel(props.step.name);
			}
			function onKeyup(e) {
				if ([13, 32].includes(e.keyCode)) {
					if (!isActive.value) props.goToPanel(props.step.name);
					stopAndPrevent(e);
				}
			}
			return () => {
				const data = { class: classes.value };
				if (headerNav.value) {
					data.onClick = onActivate;
					data.onKeydown = preventSpace$1;
					data.onKeyup = onKeyup;
					data.role = "button";
					data["aria-current"] = isActive.value ? "step" : void 0;
					Object.assign(data, isDisable.value ? {
						tabindex: -1,
						"aria-disabled": "true"
					} : { tabindex: attrs.tabindex || 0 });
				}
				const child = [(0, vue.h)("div", {
					class: "q-focus-helper",
					tabindex: -1,
					ref: blurRef
				}), (0, vue.h)("div", { class: "q-stepper__dot row flex-center q-stepper__line relative-position" }, [(0, vue.h)("span", { class: "row flex-center" }, [hasPrefix.value ? props.step.prefix : (0, vue.h)(QIcon_default, { name: icon.value })])])];
				if (props.step.title !== void 0 && props.step.title !== null) {
					const content = [(0, vue.h)("div", { class: "q-stepper__title" }, props.step.title)];
					if (props.step.caption !== void 0 && props.step.caption !== null) content.push((0, vue.h)("div", { class: "q-stepper__caption" }, props.step.caption));
					child.push((0, vue.h)("div", { class: "q-stepper__label q-stepper__line relative-position" }, content));
				}
				return (0, vue.withDirectives)((0, vue.h)("div", data, child), [[Ripple_default, ripple.value]]);
			};
		}
	});
	//#endregion
	//#region src/components/stepper/QStep.js
	function getStepWrapper(slots) {
		return (0, vue.h)("div", { class: "q-stepper__step-content" }, [(0, vue.h)("div", { class: "q-stepper__step-inner" }, hSlot(slots.default))]);
	}
	const PanelWrapper = { setup(_, { slots }) {
		return () => getStepWrapper(slots);
	} };
	var QStep_default = createComponent({
		name: "QStep",
		props: {
			...usePanelChildProps,
			icon: String,
			color: String,
			title: {
				type: String,
				required: true
			},
			caption: String,
			prefix: [String, Number],
			doneIcon: String,
			doneColor: String,
			activeIcon: String,
			activeColor: String,
			errorIcon: String,
			errorColor: String,
			headerNav: {
				type: Boolean,
				default: true
			},
			done: Boolean,
			error: Boolean,
			onScroll: [Function, Array]
		},
		setup(props, { slots, emit }) {
			const { proxy: { $q } } = (0, vue.getCurrentInstance)();
			const $stepper = (0, vue.inject)(stepperKey, emptyRenderFn);
			if ($stepper === emptyRenderFn) {
				console.error("QStep needs to be a child of QStepper");
				return emptyRenderFn;
			}
			const { getCache } = useRenderCache();
			const rootRef = (0, vue.ref)(null);
			const isActive = (0, vue.computed)(() => $stepper.value.modelValue === props.name);
			const scrollEvent = (0, vue.computed)(() => !$q.platform.is.ios && $q.platform.is.chrome || !isActive.value || !$stepper.value.vertical ? {} : { onScroll(e) {
				const { target } = e;
				if (target.scrollTop > 0) target.scrollTop = 0;
				if (props.onScroll !== void 0) emit("scroll", e);
			} });
			const contentKey = (0, vue.computed)(() => typeof props.name === "string" || typeof props.name === "number" ? props.name : String(props.name));
			function getStepContent() {
				const vertical = $stepper.value.vertical;
				if (vertical && $stepper.value.keepAlive) return (0, vue.h)(vue.KeepAlive, $stepper.value.keepAliveProps.value, isActive.value ? [(0, vue.h)($stepper.value.needsUniqueKeepAliveWrapper.value ? getCache(contentKey.value, () => ({
					...PanelWrapper,
					name: contentKey.value
				})) : PanelWrapper, { key: contentKey.value }, slots.default)] : void 0);
				return !vertical || isActive.value ? getStepWrapper(slots) : void 0;
			}
			return () => (0, vue.h)("div", {
				ref: rootRef,
				class: "q-stepper__step",
				role: "tabpanel",
				...scrollEvent.value
			}, $stepper.value.vertical ? [(0, vue.h)(StepHeader_default, {
				stepper: $stepper.value,
				step: props,
				goToPanel: $stepper.value.goToPanel
			}), $stepper.value.animated ? (0, vue.h)(QSlideTransition_default, getStepContent) : getStepContent()] : [getStepContent()]);
		}
	});
	//#endregion
	//#region src/components/stepper/QStepper.js
	const camelRE = /(-\w)/g;
	function camelizeProps(props) {
		const acc = {};
		for (const key in props) {
			const newKey = key.replace(camelRE, (m) => m[1].toUpperCase());
			acc[newKey] = props[key];
		}
		return acc;
	}
	var QStepper_default = createComponent({
		name: "QStepper",
		props: {
			...useDarkProps,
			...usePanelProps,
			flat: Boolean,
			bordered: Boolean,
			alternativeLabels: Boolean,
			headerNav: Boolean,
			contracted: Boolean,
			headerClass: String,
			inactiveColor: String,
			inactiveIcon: String,
			doneIcon: String,
			doneColor: String,
			activeIcon: String,
			activeColor: String,
			errorIcon: String,
			errorColor: String
		},
		emits: usePanelEmits,
		setup(props, { slots }) {
			const isDark = useDark(props, (0, vue.getCurrentInstance)().proxy.$q);
			const { updatePanelsList, isValidPanelName, updatePanelIndex, getPanelContent, getPanels, panelDirectives, goToPanel, keepAliveProps, needsUniqueKeepAliveWrapper } = usePanel();
			(0, vue.provide)(stepperKey, (0, vue.computed)(() => ({
				goToPanel,
				keepAliveProps,
				needsUniqueKeepAliveWrapper,
				...props
			})));
			const classes = (0, vue.computed)(() => `q-stepper q-stepper--${props.vertical ? "vertical" : "horizontal"}` + (props.flat ? " q-stepper--flat" : "") + (props.bordered ? " q-stepper--bordered" : "") + (isDark.value ? " q-stepper--dark q-dark" : ""));
			const headerClasses = (0, vue.computed)(() => `q-stepper__header row items-stretch justify-between q-stepper__header--${props.alternativeLabels ? "alternative" : "standard"}-labels` + (props.bordered || !props.flat ? " q-stepper__header--border" : "") + (props.contracted ? " q-stepper__header--contracted" : "") + (props.headerClass !== void 0 ? ` ${props.headerClass}` : ""));
			function getContent() {
				const top = hSlot(slots.message, []);
				if (props.vertical) {
					if (isValidPanelName(props.modelValue)) updatePanelIndex();
					const content = (0, vue.h)("div", { class: "q-stepper__content" }, hSlot(slots.default));
					return top === void 0 ? [content] : top.concat(content);
				}
				return [
					(0, vue.h)("div", { class: headerClasses.value }, getPanels().map((panel) => {
						const step = camelizeProps(panel.props);
						return (0, vue.h)(StepHeader_default, {
							key: step.name,
							stepper: props,
							step,
							goToPanel
						});
					})),
					top,
					hDir("div", { class: "q-stepper__content q-panel-parent" }, getPanelContent(), "cont", props.swipeable, () => panelDirectives.value)
				];
			}
			return () => {
				updatePanelsList(slots);
				return (0, vue.h)("div", { class: classes.value }, hMergeSlot(slots.navigation, getContent()));
			};
		}
	});
	//#endregion
	//#region src/components/stepper/QStepperNavigation.js
	var QStepperNavigation_default = createComponent({
		name: "QStepperNavigation",
		setup(_, { slots }) {
			return () => (0, vue.h)("div", { class: "q-stepper__nav" }, hSlot(slots.default));
		}
	});
	//#endregion
	//#region src/components/table/QTh.js
	var QTh_default = createComponent({
		name: "QTh",
		props: {
			props: Object,
			autoWidth: Boolean
		},
		emits: ["click"],
		setup(props, { slots, emit }) {
			const vm = (0, vue.getCurrentInstance)();
			const { proxy: { $q } } = vm;
			const onClick = (evt) => {
				emit("click", evt);
			};
			const onKeyup = (evt, col) => {
				if (evt.key === "Enter" || evt.key === " ") {
					props.props.sort(col);
					onClick(evt);
					evt.preventDefault();
				}
			};
			return () => {
				if (props.props === void 0) return (0, vue.h)("th", {
					class: props.autoWidth ? "q-table--col-auto-width" : "",
					onClick
				}, hSlot(slots.default));
				let col, child;
				const name = vm.vnode.key;
				if (name !== null) {
					col = props.props.colsMap[name];
					if (col === void 0) return;
				} else col = props.props.col;
				if (col.sortable) {
					const action = col.align === "right" ? "unshift" : "push";
					child = hUniqueSlot(slots.default, []);
					child[action]((0, vue.h)(QIcon_default, {
						class: col.__iconClass,
						name: $q.iconSet.table.arrowUp
					}));
				} else child = hSlot(slots.default);
				const data = {
					class: col.__thClass + (props.autoWidth ? " q-table--col-auto-width" : ""),
					style: col.headerStyle,
					onClick: (evt) => {
						if (col.sortable) props.props.sort(col);
						onClick(evt);
					}
				};
				if (col.sortable) {
					data.tabindex = 0;
					data["aria-sort"] = col.__ariaSort;
					data.onKeydown = (evt) => {
						if (evt.key === " ") evt.preventDefault();
					};
					data.onKeyup = (evt) => {
						onKeyup(evt, col);
					};
				}
				return (0, vue.h)("th", data, child);
			};
		}
	});
	//#endregion
	//#region src/components/table/get-table-middle.js
	function getTableMiddle(props, content) {
		return (0, vue.h)("div", props, [(0, vue.h)("table", { class: "q-table" }, content)]);
	}
	//#endregion
	//#region src/components/virtual-scroll/QVirtualScroll.js
	const comps = {
		list: QList_default,
		table: QMarkupTable_default
	};
	const typeOptions = [
		"list",
		"table",
		"__qtable"
	];
	var QVirtualScroll_default = createComponent({
		name: "QVirtualScroll",
		props: {
			...useVirtualScrollProps,
			type: {
				type: String,
				default: "list",
				validator: (v) => typeOptions.includes(v)
			},
			items: {
				type: Array,
				default: () => []
			},
			itemsFn: Function,
			itemsSize: Number,
			scrollTarget: scrollTargetProp
		},
		setup(props, { slots, attrs }) {
			let localScrollTarget;
			const rootRef = (0, vue.ref)(null);
			const virtualScrollLength = (0, vue.computed)(() => props.itemsSize >= 0 && props.itemsFn !== void 0 ? Number.parseInt(props.itemsSize, 10) : Array.isArray(props.items) ? props.items.length : 0);
			const { virtualScrollSliceRange, localResetVirtualScroll, padVirtualScroll, onVirtualScrollEvt } = useVirtualScroll({
				virtualScrollLength,
				getVirtualScrollTarget,
				getVirtualScrollEl
			});
			const virtualScrollScope = (0, vue.computed)(() => {
				if (virtualScrollLength.value === 0) return [];
				const mapFn = (item, i) => ({
					index: virtualScrollSliceRange.value.from + i,
					item
				});
				return props.itemsFn === void 0 ? props.items.slice(virtualScrollSliceRange.value.from, virtualScrollSliceRange.value.to).map(mapFn) : props.itemsFn(virtualScrollSliceRange.value.from, virtualScrollSliceRange.value.to - virtualScrollSliceRange.value.from).map(mapFn);
			});
			const classes = (0, vue.computed)(() => "q-virtual-scroll q-virtual-scroll" + (props.virtualScrollHorizontal ? "--horizontal" : "--vertical") + (props.scrollTarget !== void 0 ? "" : " scroll"));
			const attributes = (0, vue.computed)(() => props.scrollTarget !== void 0 ? {} : { tabindex: 0 });
			(0, vue.watch)(virtualScrollLength, () => {
				localResetVirtualScroll();
			});
			(0, vue.watch)(() => props.scrollTarget, () => {
				unconfigureScrollTarget();
				configureScrollTarget();
			});
			function getVirtualScrollEl() {
				return rootRef.value.$el || rootRef.value;
			}
			function getVirtualScrollTarget() {
				return localScrollTarget;
			}
			function configureScrollTarget() {
				localScrollTarget = getScrollTarget(getVirtualScrollEl(), props.scrollTarget);
				localScrollTarget.addEventListener("scroll", onVirtualScrollEvt, listenOpts.passive);
			}
			function unconfigureScrollTarget() {
				if (localScrollTarget !== void 0) {
					localScrollTarget.removeEventListener("scroll", onVirtualScrollEvt, listenOpts.passive);
					localScrollTarget = void 0;
				}
			}
			function __getVirtualChildren() {
				let child = padVirtualScroll(props.type === "list" ? "div" : "tbody", virtualScrollScope.value.map(slots.default));
				if (slots.before !== void 0) child = slots.before().concat(child);
				return hMergeSlot(slots.after, child);
			}
			(0, vue.onBeforeMount)(() => {
				localResetVirtualScroll();
			});
			(0, vue.onMounted)(() => {
				configureScrollTarget();
			});
			(0, vue.onActivated)(() => {
				configureScrollTarget();
			});
			(0, vue.onDeactivated)(() => {
				unconfigureScrollTarget();
			});
			(0, vue.onBeforeUnmount)(() => {
				unconfigureScrollTarget();
			});
			return () => {
				if (slots.default === void 0) {
					console.error("QVirtualScroll: default scoped slot is required for rendering");
					return;
				}
				return props.type === "__qtable" ? getTableMiddle({
					ref: rootRef,
					class: "q-table__middle " + classes.value
				}, __getVirtualChildren()) : (0, vue.h)(comps[props.type], {
					...attrs,
					ref: rootRef,
					class: [attrs.class, classes.value],
					...attributes.value
				}, __getVirtualChildren);
			};
		}
	});
	//#endregion
	//#region src/utils/private.sort/sort.js
	function sortDate(a, b) {
		return new Date(a) - new Date(b);
	}
	//#endregion
	//#region src/components/table/table-sort.js
	const useTableSortProps = {
		sortMethod: Function,
		binaryStateSort: Boolean,
		columnSortOrder: {
			type: String,
			validator: (v) => v === "ad" || v === "da",
			default: "ad"
		}
	};
	function useTableSort(props, computedPagination, colList, setPagination) {
		const columnToSort = (0, vue.computed)(() => {
			const { sortBy } = computedPagination.value;
			return sortBy ? colList.value.find((def) => def.name === sortBy) || null : null;
		});
		const computedSortMethod = (0, vue.computed)(() => props.sortMethod !== void 0 ? props.sortMethod : (data, sortBy, descending) => {
			const col = colList.value.find((def) => def.name === sortBy);
			if (col === void 0 || col.field === void 0) return data;
			const dir = descending ? -1 : 1, val = typeof col.field === "function" ? (v) => col.field(v) : (v) => v[col.field];
			return data.sort((a, b) => {
				let A = val(a), B = val(b);
				if (col.rawSort !== void 0) return col.rawSort(A, B, a, b) * dir;
				if (A === null || A === void 0) return -1 * dir;
				if (B === null || B === void 0) return Number(dir);
				if (col.sort !== void 0) return col.sort(A, B, a, b) * dir;
				if (isNumber(A) && isNumber(B)) return (A - B) * dir;
				if (isDate(A) && isDate(B)) return sortDate(A, B) * dir;
				if (typeof A === "boolean" && typeof B === "boolean") return (A - B) * dir;
				[A, B] = [A, B].map((s) => String(s).toLocaleString().toLowerCase());
				return A < B ? -1 * dir : A === B ? 0 : dir;
			});
		});
		function sort(col) {
			let sortOrder = props.columnSortOrder;
			if (isObject(col)) {
				if (col.sortOrder) sortOrder = col.sortOrder;
				col = col.name;
			} else {
				const def = colList.value.find((item) => item.name === col);
				if (def?.sortOrder) sortOrder = def.sortOrder;
			}
			let { sortBy, descending } = computedPagination.value;
			if (sortBy !== col) {
				sortBy = col;
				descending = sortOrder === "da";
			} else if (props.binaryStateSort) descending = !descending;
			else if (descending) if (sortOrder === "ad") sortBy = null;
			else descending = false;
			else if (sortOrder === "ad") descending = true;
			else sortBy = null;
			setPagination({
				sortBy,
				descending,
				page: 1
			});
		}
		return {
			columnToSort,
			computedSortMethod,
			sort
		};
	}
	//#endregion
	//#region src/components/table/table-filter.js
	const useTableFilterProps = {
		filter: [String, Object],
		filterMethod: Function
	};
	function useTableFilter(props, setPagination) {
		const computedFilterMethod = (0, vue.computed)(() => props.filterMethod !== void 0 ? props.filterMethod : (rows, terms, cols, cellValue) => {
			const lowerTerms = terms ? terms.toLowerCase() : "";
			return rows.filter((row) => cols.some((col) => {
				const val = String(cellValue(col, row));
				return (val === "undefined" || val === "null" ? "" : val.toLowerCase()).includes(lowerTerms);
			}));
		});
		(0, vue.watch)(() => props.filter, () => {
			(0, vue.nextTick)(() => {
				setPagination({ page: 1 }, true);
			});
		}, { deep: true });
		return { computedFilterMethod };
	}
	//#endregion
	//#region src/components/table/table-pagination.js
	function samePagination(oldPag, newPag) {
		for (const prop in newPag) if (newPag[prop] !== oldPag[prop]) return false;
		return true;
	}
	function fixPagination(p) {
		if (p.page < 1) p.page = 1;
		if (p.rowsPerPage !== void 0 && p.rowsPerPage < 1) p.rowsPerPage = 0;
		return p;
	}
	const useTablePaginationProps = {
		pagination: Object,
		rowsPerPageOptions: {
			type: Array,
			default: () => [
				5,
				7,
				10,
				15,
				20,
				25,
				50,
				0
			]
		},
		"onUpdate:pagination": [Function, Array]
	};
	function useTablePaginationState(vm, getCellValue) {
		const { props, emit } = vm;
		const innerPagination = (0, vue.ref)({
			sortBy: null,
			descending: false,
			page: 1,
			rowsPerPage: props.rowsPerPageOptions.length !== 0 ? props.rowsPerPageOptions[0] : 5,
			...props.pagination
		});
		const computedPagination = (0, vue.computed)(() => {
			return fixPagination(props["onUpdate:pagination"] !== void 0 ? {
				...innerPagination.value,
				...props.pagination
			} : innerPagination.value);
		});
		const isServerSide = (0, vue.computed)(() => computedPagination.value.rowsNumber !== void 0);
		function sendServerRequest(pagination) {
			requestServerInteraction({
				pagination,
				filter: props.filter
			});
		}
		function requestServerInteraction(prop = {}) {
			(0, vue.nextTick)(() => {
				emit("request", {
					pagination: prop.pagination === void 0 ? computedPagination.value : prop.pagination,
					filter: prop.filter === void 0 ? props.filter : prop.filter,
					getCellValue
				});
			});
		}
		function setPagination(val, forceServerRequest) {
			const newPagination = fixPagination({
				...computedPagination.value,
				...val
			});
			if (samePagination(computedPagination.value, newPagination)) {
				if (isServerSide.value && forceServerRequest) sendServerRequest(newPagination);
				return;
			}
			if (isServerSide.value) {
				sendServerRequest(newPagination);
				return;
			}
			if (props.pagination !== void 0 && props["onUpdate:pagination"] !== void 0) emit("update:pagination", newPagination);
			else innerPagination.value = newPagination;
		}
		return {
			innerPagination,
			computedPagination,
			isServerSide,
			requestServerInteraction,
			setPagination
		};
	}
	function useTablePagination(vm, innerPagination, computedPagination, isServerSide, setPagination, filteredSortedRowsNumber) {
		const { props, emit, proxy: { $q } } = vm;
		const computedRowsNumber = (0, vue.computed)(() => isServerSide.value ? computedPagination.value.rowsNumber || 0 : filteredSortedRowsNumber.value);
		const firstRowIndex = (0, vue.computed)(() => {
			const { page, rowsPerPage } = computedPagination.value;
			return (page - 1) * rowsPerPage;
		});
		const lastRowIndex = (0, vue.computed)(() => {
			const { page, rowsPerPage } = computedPagination.value;
			return page * rowsPerPage;
		});
		const isFirstPage = (0, vue.computed)(() => computedPagination.value.page === 1);
		const pagesNumber = (0, vue.computed)(() => computedPagination.value.rowsPerPage === 0 ? 1 : Math.max(1, Math.ceil(computedRowsNumber.value / computedPagination.value.rowsPerPage)));
		const isLastPage = (0, vue.computed)(() => lastRowIndex.value === 0 ? true : computedPagination.value.page >= pagesNumber.value);
		const computedRowsPerPageOptions = (0, vue.computed)(() => {
			return (props.rowsPerPageOptions.includes(innerPagination.value.rowsPerPage) ? props.rowsPerPageOptions : [innerPagination.value.rowsPerPage, ...props.rowsPerPageOptions]).map((count) => ({
				label: count === 0 ? $q.lang.table.allRows : String(count),
				value: count
			}));
		});
		(0, vue.watch)(pagesNumber, (newLastPage, oldLastPage) => {
			if (newLastPage === oldLastPage) return;
			const currentPage = computedPagination.value.page;
			if (newLastPage && !currentPage) setPagination({ page: 1 });
			else if (newLastPage < currentPage) setPagination({ page: newLastPage });
		});
		function firstPage() {
			setPagination({ page: 1 });
		}
		function prevPage() {
			const { page } = computedPagination.value;
			if (page > 1) setPagination({ page: page - 1 });
		}
		function nextPage() {
			const { page, rowsPerPage } = computedPagination.value;
			if (lastRowIndex.value > 0 && page * rowsPerPage < computedRowsNumber.value) setPagination({ page: page + 1 });
		}
		function lastPage() {
			setPagination({ page: pagesNumber.value });
		}
		if (props["onUpdate:pagination"] !== void 0) emit("update:pagination", { ...computedPagination.value });
		return {
			firstRowIndex,
			lastRowIndex,
			isFirstPage,
			isLastPage,
			pagesNumber,
			computedRowsPerPageOptions,
			computedRowsNumber,
			firstPage,
			prevPage,
			nextPage,
			lastPage
		};
	}
	//#endregion
	//#region src/components/table/table-row-selection.js
	const useTableRowSelectionProps = {
		selection: {
			type: String,
			default: "none",
			validator: (v) => [
				"single",
				"multiple",
				"none"
			].includes(v)
		},
		selected: {
			type: Array,
			default: () => []
		}
	};
	const useTableRowSelectionEmits = ["update:selected", "selection"];
	function useTableRowSelection(props, emit, computedRows, getRowKey) {
		const selectedKeys = (0, vue.computed)(() => new Set(props.selected.map(getRowKey.value)));
		const hasSelectionMode = (0, vue.computed)(() => props.selection !== "none");
		const singleSelection = (0, vue.computed)(() => props.selection === "single");
		const multipleSelection = (0, vue.computed)(() => props.selection === "multiple");
		const allRowsSelected = (0, vue.computed)(() => computedRows.value.length !== 0 && computedRows.value.every((row) => selectedKeys.value.has(getRowKey.value(row))));
		const someRowsSelected = (0, vue.computed)(() => !allRowsSelected.value && computedRows.value.some((row) => selectedKeys.value.has(getRowKey.value(row))));
		const rowsSelectedNumber = (0, vue.computed)(() => props.selected.length);
		function isRowSelected(key) {
			return selectedKeys.value.has(key);
		}
		function clearSelection() {
			emit("update:selected", []);
		}
		function updateSelection(keys, rows, added, evt) {
			emit("selection", {
				rows,
				added,
				keys,
				evt
			});
			emit("update:selected", singleSelection.value ? added ? rows : [] : added ? [...props.selected, ...rows] : props.selected.filter((row) => !keys.includes(getRowKey.value(row))));
		}
		return {
			hasSelectionMode,
			singleSelection,
			multipleSelection,
			allRowsSelected,
			someRowsSelected,
			rowsSelectedNumber,
			isRowSelected,
			clearSelection,
			updateSelection
		};
	}
	//#endregion
	//#region src/components/table/table-row-expand.js
	function getVal(val) {
		return Array.isArray(val) ? [...val] : [];
	}
	const useTableRowExpandProps = { expanded: Array };
	const useTableRowExpandEmits = ["update:expanded"];
	function useTableRowExpand(props, emit) {
		const innerExpanded = (0, vue.ref)(getVal(props.expanded));
		(0, vue.watch)(() => props.expanded, (val) => {
			innerExpanded.value = getVal(val);
		});
		function isRowExpanded(key) {
			return innerExpanded.value.includes(key);
		}
		function setExpanded(val) {
			if (props.expanded !== void 0) emit("update:expanded", val);
			else innerExpanded.value = val;
		}
		function updateExpanded(key, add) {
			const target = [...innerExpanded.value];
			const index = target.indexOf(key);
			if (add) {
				if (index === -1) {
					target.push(key);
					setExpanded(target);
				}
			} else if (index !== -1) {
				target.splice(index, 1);
				setExpanded(target);
			}
		}
		return {
			isRowExpanded,
			setExpanded,
			updateExpanded
		};
	}
	//#endregion
	//#region src/components/table/table-column-selection.js
	const useTableColumnSelectionProps = { visibleColumns: Array };
	function useTableColumnSelection(props, computedPagination, hasSelectionMode) {
		const colList = (0, vue.computed)(() => {
			if (props.columns !== void 0) return props.columns;
			const row = props.rows[0];
			return row !== void 0 ? Object.keys(row).map((name) => ({
				name,
				label: name.toUpperCase(),
				field: name,
				align: isNumber(row[name]) ? "right" : "left",
				sortable: true
			})) : [];
		});
		const computedCols = (0, vue.computed)(() => {
			const { sortBy, descending } = computedPagination.value;
			return (props.visibleColumns !== void 0 ? colList.value.filter((col) => col.required || props.visibleColumns.includes(col.name)) : colList.value).map((col) => {
				const align = col.align || "right";
				const alignClass = `text-${align}`;
				return {
					...col,
					align,
					__iconClass: `q-table__sort-icon q-table__sort-icon--${align}`,
					__ariaSort: col.sortable === true ? col.name === sortBy ? descending ? "descending" : "ascending" : "none" : void 0,
					__thClass: alignClass + (col.headerClasses !== void 0 ? " " + col.headerClasses : "") + (col.sortable ? " sortable" : "") + (col.name === sortBy ? ` sorted ${descending ? "sort-desc" : ""}` : ""),
					__tdStyle: col.style !== void 0 ? typeof col.style !== "function" ? () => col.style : col.style : () => null,
					__tdClass: col.classes !== void 0 ? typeof col.classes !== "function" ? () => alignClass + " " + col.classes : (row) => alignClass + " " + col.classes(row) : () => alignClass
				};
			});
		});
		return {
			colList,
			computedCols,
			computedColsMap: (0, vue.computed)(() => {
				const names = Object.create(null);
				computedCols.value.forEach((col) => {
					names[col.name] = col;
				});
				return names;
			}),
			computedColspan: (0, vue.computed)(() => props.tableColspan !== void 0 ? props.tableColspan : computedCols.value.length + (hasSelectionMode.value ? 1 : 0))
		};
	}
	//#endregion
	//#region src/components/table/QTable.js
	const bottomClass = "q-table__bottom row items-center";
	const virtScrollPassthroughProps = {};
	commonVirtScrollPropsList.forEach((p) => {
		virtScrollPassthroughProps[p] = {};
	});
	function getCellValue(col, row) {
		const val = typeof col.field === "function" ? col.field(row) : row[col.field];
		return col.format !== void 0 ? col.format(val, row) : val;
	}
	var QTable_default = createComponent({
		name: "QTable",
		props: {
			rows: {
				type: Array,
				required: true
			},
			rowKey: {
				type: [String, Function],
				default: "id"
			},
			columns: Array,
			loading: Boolean,
			iconFirstPage: String,
			iconPrevPage: String,
			iconNextPage: String,
			iconLastPage: String,
			title: String,
			hideHeader: Boolean,
			grid: Boolean,
			gridHeader: Boolean,
			dense: Boolean,
			flat: Boolean,
			bordered: Boolean,
			square: Boolean,
			separator: {
				type: String,
				default: "horizontal",
				validator: (v) => [
					"horizontal",
					"vertical",
					"cell",
					"none"
				].includes(v)
			},
			wrapCells: Boolean,
			virtualScroll: Boolean,
			virtualScrollTarget: {},
			...virtScrollPassthroughProps,
			noDataLabel: String,
			noResultsLabel: String,
			loadingLabel: String,
			selectedRowsLabel: Function,
			rowsPerPageLabel: String,
			paginationLabel: Function,
			color: {
				type: String,
				default: "grey-8"
			},
			titleClass: [
				String,
				Array,
				Object
			],
			tableStyle: [
				String,
				Array,
				Object
			],
			tableClass: [
				String,
				Array,
				Object
			],
			tableHeaderStyle: [
				String,
				Array,
				Object
			],
			tableHeaderClass: [
				String,
				Array,
				Object
			],
			tableRowStyleFn: Function,
			tableRowClassFn: Function,
			cardContainerClass: [
				String,
				Array,
				Object
			],
			cardContainerStyle: [
				String,
				Array,
				Object
			],
			cardStyle: [
				String,
				Array,
				Object
			],
			cardClass: [
				String,
				Array,
				Object
			],
			cardStyleFn: Function,
			cardClassFn: Function,
			hideBottom: Boolean,
			hideSelectedBanner: Boolean,
			hideNoData: Boolean,
			hidePagination: Boolean,
			onRowClick: Function,
			onRowDblclick: Function,
			onRowContextmenu: Function,
			...useDarkProps,
			...useFullscreenProps,
			...useTableColumnSelectionProps,
			...useTableFilterProps,
			...useTablePaginationProps,
			...useTableRowExpandProps,
			...useTableRowSelectionProps,
			...useTableSortProps
		},
		emits: [
			"request",
			"virtualScroll",
			...useFullscreenEmits,
			...useTableRowExpandEmits,
			...useTableRowSelectionEmits
		],
		setup(props, { slots, emit }) {
			const vm = (0, vue.getCurrentInstance)();
			const { proxy: { $q } } = vm;
			const isDark = useDark(props, $q);
			const { inFullscreen, toggleFullscreen } = useFullscreen();
			const getRowKey = (0, vue.computed)(() => typeof props.rowKey === "function" ? props.rowKey : (row) => row[props.rowKey]);
			const rootRef = (0, vue.ref)(null);
			const virtScrollRef = (0, vue.ref)(null);
			const hasVirtScroll = (0, vue.computed)(() => !props.grid && props.virtualScroll);
			const cardDefaultClass = (0, vue.computed)(() => " q-table__card" + (isDark.value ? " q-table__card--dark q-dark" : "") + (props.square ? " q-table--square" : "") + (props.flat ? " q-table--flat" : "") + (props.bordered ? " q-table--bordered" : ""));
			const containerClass = (0, vue.computed)(() => `q-table__container q-table--${props.separator}-separator column no-wrap` + (props.grid ? " q-table--grid" : cardDefaultClass.value) + (isDark.value ? " q-table--dark" : "") + (props.dense ? " q-table--dense" : "") + (props.wrapCells ? "" : " q-table--no-wrap") + (inFullscreen.value ? " fullscreen scroll" : ""));
			const rootContainerClass = (0, vue.computed)(() => containerClass.value + (props.loading ? " q-table--loading" : ""));
			(0, vue.watch)([
				() => props.tableStyle,
				() => props.tableClass,
				() => props.tableHeaderStyle,
				() => props.tableHeaderClass,
				containerClass
			], () => {
				if (hasVirtScroll.value) virtScrollRef.value?.reset();
			}, { deep: true });
			const { innerPagination, computedPagination, isServerSide, requestServerInteraction, setPagination } = useTablePaginationState(vm, getCellValue);
			const { computedFilterMethod } = useTableFilter(props, setPagination);
			const { isRowExpanded, setExpanded, updateExpanded } = useTableRowExpand(props, emit);
			const filteredSortedRows = (0, vue.computed)(() => {
				let rows = props.rows;
				if (isServerSide.value || rows.length === 0) return rows;
				const { sortBy, descending } = computedPagination.value;
				if (props.filter) rows = computedFilterMethod.value(rows, props.filter, computedCols.value, getCellValue);
				if (columnToSort.value !== null) rows = computedSortMethod.value(props.rows === rows ? [...rows] : rows, sortBy, descending);
				return rows;
			});
			const filteredSortedRowsNumber = (0, vue.computed)(() => filteredSortedRows.value.length);
			const computedRows = (0, vue.computed)(() => {
				let rows = filteredSortedRows.value;
				if (isServerSide.value) return rows;
				const { rowsPerPage } = computedPagination.value;
				if (rowsPerPage !== 0) if (firstRowIndex.value === 0 && props.rows !== rows) {
					if (rows.length > lastRowIndex.value) rows = rows.slice(0, lastRowIndex.value);
				} else rows = rows.slice(firstRowIndex.value, lastRowIndex.value);
				return rows;
			});
			const { hasSelectionMode, singleSelection, multipleSelection, allRowsSelected, someRowsSelected, rowsSelectedNumber, isRowSelected, clearSelection, updateSelection } = useTableRowSelection(props, emit, computedRows, getRowKey);
			const { colList, computedCols, computedColsMap, computedColspan } = useTableColumnSelection(props, computedPagination, hasSelectionMode);
			const { columnToSort, computedSortMethod, sort } = useTableSort(props, computedPagination, colList, setPagination);
			const { firstRowIndex, lastRowIndex, isFirstPage, isLastPage, pagesNumber, computedRowsPerPageOptions, computedRowsNumber, firstPage, prevPage, nextPage, lastPage } = useTablePagination(vm, innerPagination, computedPagination, isServerSide, setPagination, filteredSortedRowsNumber);
			const nothingToDisplay = (0, vue.computed)(() => computedRows.value.length === 0);
			const virtProps = (0, vue.computed)(() => {
				const acc = {};
				commonVirtScrollPropsList.forEach((p) => {
					acc[p] = props[p];
				});
				if (acc.virtualScrollItemSize === void 0) acc.virtualScrollItemSize = props.dense ? 28 : 48;
				return acc;
			});
			function resetVirtualScroll() {
				if (hasVirtScroll.value) virtScrollRef.value.reset();
			}
			function getBody() {
				if (props.grid) return getGridBody();
				const header = props.hideHeader ? null : getTHead;
				if (hasVirtScroll.value) {
					const topRow = slots["top-row"];
					const bottomRow = slots["bottom-row"];
					const virtSlots = { default: (slotProps) => getTBodyTR(slotProps.item, slots.body, slotProps.index) };
					if (topRow !== void 0) {
						const topContent = (0, vue.h)("tbody", topRow({ cols: computedCols.value }));
						virtSlots.before = header === null ? () => topContent : () => [header(), topContent];
					} else if (header !== null) virtSlots.before = header;
					if (bottomRow !== void 0) virtSlots.after = () => (0, vue.h)("tbody", bottomRow({ cols: computedCols.value }));
					return (0, vue.h)(QVirtualScroll_default, {
						ref: virtScrollRef,
						class: props.tableClass,
						style: props.tableStyle,
						...virtProps.value,
						scrollTarget: props.virtualScrollTarget,
						items: computedRows.value,
						type: "__qtable",
						tableColspan: computedColspan.value,
						onVirtualScroll: onVScroll
					}, virtSlots);
				}
				const child = [getTBody()];
				if (header !== null) child.unshift(header());
				return getTableMiddle({
					class: ["q-table__middle scroll", props.tableClass],
					style: props.tableStyle
				}, child);
			}
			function scrollTo(toIndex, edge) {
				if (virtScrollRef.value !== null) {
					virtScrollRef.value.scrollTo(toIndex, edge);
					return;
				}
				toIndex = Number.parseInt(toIndex, 10);
				const rowEl = rootRef.value.querySelector(`tbody tr:nth-of-type(${toIndex + 1})`);
				if (rowEl !== null) {
					const scrollTarget = rootRef.value.querySelector(".q-table__middle.scroll");
					const offsetTop = rowEl.offsetTop - props.virtualScrollStickySizeStart;
					const direction = offsetTop < scrollTarget.scrollTop ? "decrease" : "increase";
					scrollTarget.scrollTop = offsetTop;
					emit("virtualScroll", {
						index: toIndex,
						from: 0,
						to: innerPagination.value.rowsPerPage - 1,
						direction
					});
				}
			}
			function onVScroll(info) {
				emit("virtualScroll", info);
			}
			function getProgress() {
				return [(0, vue.h)(QLinearProgress_default, {
					class: "q-table__linear-progress",
					color: props.color,
					dark: isDark.value,
					indeterminate: true,
					trackColor: "transparent"
				})];
			}
			function getTBodyTR(row, bodySlot, pageIndex) {
				const key = getRowKey.value(row), selected = isRowSelected(key);
				if (bodySlot !== void 0) {
					const cfg = {
						key,
						row,
						pageIndex,
						__trClass: selected ? "selected" : ""
					};
					if (props.tableRowStyleFn !== void 0) cfg.__trStyle = props.tableRowStyleFn(row);
					if (props.tableRowClassFn !== void 0) {
						const cls = props.tableRowClassFn(row);
						if (cls) cfg.__trClass = `${cls} ${cfg.__trClass}`;
					}
					return bodySlot(getBodyScope(cfg));
				}
				const bodyCell = slots["body-cell"], child = computedCols.value.map((col) => {
					const bodyCellCol = slots[`body-cell-${col.name}`], slot = bodyCellCol !== void 0 ? bodyCellCol : bodyCell;
					return slot !== void 0 ? slot(getBodyCellScope({
						key,
						row,
						pageIndex,
						col
					})) : (0, vue.h)("td", {
						class: col.__tdClass(row),
						style: col.__tdStyle(row)
					}, getCellValue(col, row));
				});
				if (hasSelectionMode.value) {
					const slot = slots["body-selection"];
					const content = slot !== void 0 ? slot(getBodySelectionScope({
						key,
						row,
						pageIndex
					})) : [(0, vue.h)(QCheckbox_default, {
						modelValue: selected,
						color: props.color,
						dark: isDark.value,
						dense: props.dense,
						"onUpdate:modelValue": (adding, evt) => {
							updateSelection([key], [row], adding, evt);
						}
					})];
					child.unshift((0, vue.h)("td", { class: "q-table--col-auto-width" }, content));
				}
				const data = {
					key,
					class: { selected }
				};
				if (props.onRowClick !== void 0) {
					data.class["cursor-pointer"] = true;
					data.onClick = (evt) => {
						emit("rowClick", evt, row, pageIndex);
					};
				}
				if (props.onRowDblclick !== void 0) {
					data.class["cursor-pointer"] = true;
					data.onDblclick = (evt) => {
						emit("rowDblclick", evt, row, pageIndex);
					};
				}
				if (props.onRowContextmenu !== void 0) {
					data.class["cursor-pointer"] = true;
					data.onContextmenu = (evt) => {
						emit("rowContextmenu", evt, row, pageIndex);
					};
				}
				if (props.tableRowStyleFn !== void 0) data.style = props.tableRowStyleFn(row);
				if (props.tableRowClassFn !== void 0) {
					const cls = props.tableRowClassFn(row);
					if (cls) data.class[cls] = true;
				}
				return (0, vue.h)("tr", data, child);
			}
			function getTBody() {
				const body = slots.body, topRow = slots["top-row"], bottomRow = slots["bottom-row"];
				const child = computedRows.value.map((row, pageIndex) => getTBodyTR(row, body, pageIndex));
				return (0, vue.h)("tbody", [
					topRow?.({ cols: computedCols.value }),
					...child,
					bottomRow?.({ cols: computedCols.value })
				].flat());
			}
			function getBodyScope(data) {
				injectBodyCommonScope(data);
				data.cols = data.cols.map((col) => injectProp({ ...col }, "value", () => getCellValue(col, data.row)));
				return data;
			}
			function getBodyCellScope(data) {
				injectBodyCommonScope(data);
				injectProp(data, "value", () => getCellValue(data.col, data.row));
				return data;
			}
			function getBodySelectionScope(data) {
				injectBodyCommonScope(data);
				return data;
			}
			function injectBodyCommonScope(data) {
				Object.assign(data, {
					cols: computedCols.value,
					colsMap: computedColsMap.value,
					sort,
					rowIndex: firstRowIndex.value + data.pageIndex,
					color: props.color,
					dark: isDark.value,
					dense: props.dense
				});
				if (hasSelectionMode.value) injectProp(data, "selected", () => isRowSelected(data.key), (adding, evt) => {
					updateSelection([data.key], [data.row], adding, evt);
				});
				injectProp(data, "expand", () => isRowExpanded(data.key), (adding) => {
					updateExpanded(data.key, adding);
				});
			}
			const marginalsScope = (0, vue.computed)(() => ({
				pagination: computedPagination.value,
				pagesNumber: pagesNumber.value,
				isFirstPage: isFirstPage.value,
				isLastPage: isLastPage.value,
				firstPage,
				prevPage,
				nextPage,
				lastPage,
				inFullscreen: inFullscreen.value,
				toggleFullscreen
			}));
			function getTopDiv() {
				const top = slots.top, topLeft = slots["top-left"], topRight = slots["top-right"], topSelection = slots["top-selection"], hasSelection = hasSelectionMode.value && topSelection !== void 0 && rowsSelectedNumber.value > 0, topClass = "q-table__top relative-position row items-center";
				if (top !== void 0) return (0, vue.h)("div", { class: topClass }, [top(marginalsScope.value)]);
				let child;
				if (hasSelection) child = [topSelection(marginalsScope.value)].flat();
				else {
					child = [];
					if (topLeft !== void 0) child.push((0, vue.h)("div", { class: "q-table__control" }, [topLeft(marginalsScope.value)]));
					else if (props.title) child.push((0, vue.h)("div", { class: "q-table__control" }, [(0, vue.h)("div", { class: ["q-table__title", props.titleClass] }, props.title)]));
				}
				if (topRight !== void 0) child.push((0, vue.h)("div", { class: "q-table__separator col" }), (0, vue.h)("div", { class: "q-table__control" }, [topRight(marginalsScope.value)]));
				if (child.length === 0) return;
				return (0, vue.h)("div", { class: topClass }, child);
			}
			const headerSelectedValue = (0, vue.computed)(() => someRowsSelected.value ? null : allRowsSelected.value);
			function getTHead() {
				const child = getTHeadTR();
				if (props.loading && slots.loading === void 0) child.push((0, vue.h)("tr", { class: "q-table__progress" }, [(0, vue.h)("th", {
					class: "relative-position",
					colspan: computedColspan.value
				}, getProgress())]));
				return (0, vue.h)("thead", child);
			}
			function getTHeadTR() {
				const header = slots.header, headerCell = slots["header-cell"];
				if (header !== void 0) return [header(getHeaderScope({ header: true }))].flat();
				const child = computedCols.value.map((col) => {
					const headerCellCol = slots[`header-cell-${col.name}`], slot = headerCellCol !== void 0 ? headerCellCol : headerCell, slotProps = getHeaderScope({ col });
					return slot !== void 0 ? slot(slotProps) : (0, vue.h)(QTh_default, {
						key: col.name,
						props: slotProps
					}, () => col.label);
				});
				if (singleSelection.value && !props.grid) child.unshift((0, vue.h)("th", { class: "q-table--col-auto-width" }, " "));
				else if (multipleSelection.value) {
					const slot = slots["header-selection"];
					const content = slot !== void 0 ? slot(getHeaderScope({})) : [(0, vue.h)(QCheckbox_default, {
						color: props.color,
						modelValue: headerSelectedValue.value,
						dark: isDark.value,
						dense: props.dense,
						"onUpdate:modelValue": onMultipleSelectionSet
					})];
					child.unshift((0, vue.h)("th", { class: "q-table--col-auto-width" }, content));
				}
				return [(0, vue.h)("tr", {
					class: props.tableHeaderClass,
					style: props.tableHeaderStyle
				}, child)];
			}
			function getHeaderScope(data) {
				Object.assign(data, {
					cols: computedCols.value,
					sort,
					colsMap: computedColsMap.value,
					color: props.color,
					dark: isDark.value,
					dense: props.dense
				});
				if (multipleSelection.value) injectProp(data, "selected", () => headerSelectedValue.value, onMultipleSelectionSet);
				return data;
			}
			function onMultipleSelectionSet(val) {
				if (someRowsSelected.value) val = false;
				updateSelection(computedRows.value.map(getRowKey.value), computedRows.value, val);
			}
			const navIcon = (0, vue.computed)(() => {
				const ico = [
					props.iconFirstPage || $q.iconSet.table.firstPage,
					props.iconPrevPage || $q.iconSet.table.prevPage,
					props.iconNextPage || $q.iconSet.table.nextPage,
					props.iconLastPage || $q.iconSet.table.lastPage
				];
				return $q.lang.rtl ? ico.reverse() : ico;
			});
			function getBottomDiv() {
				if (props.hideBottom) return;
				if (nothingToDisplay.value) {
					if (props.hideNoData) return;
					const message = props.loading ? props.loadingLabel || $q.lang.table.loading : props.filter ? props.noResultsLabel || $q.lang.table.noResults : props.noDataLabel || $q.lang.table.noData;
					const noData = slots["no-data"];
					return (0, vue.h)("div", { class: "q-table__bottom row items-center q-table__bottom--nodata" }, noData !== void 0 ? [noData({
						message,
						icon: $q.iconSet.table.warning,
						filter: props.filter
					})] : [(0, vue.h)(QIcon_default, {
						class: "q-table__bottom-nodata-icon",
						name: $q.iconSet.table.warning
					}), message]);
				}
				const bottom = slots.bottom;
				if (bottom !== void 0) return (0, vue.h)("div", { class: bottomClass }, [bottom(marginalsScope.value)]);
				const child = !props.hideSelectedBanner && hasSelectionMode.value && rowsSelectedNumber.value > 0 ? [(0, vue.h)("div", { class: "q-table__control" }, [(0, vue.h)("div", [(props.selectedRowsLabel || $q.lang.table.selectedRecords)(rowsSelectedNumber.value)])])] : [];
				if (!props.hidePagination) return (0, vue.h)("div", { class: "q-table__bottom row items-center justify-end" }, getPaginationDiv(child));
				if (child.length !== 0) return (0, vue.h)("div", { class: bottomClass }, child);
			}
			function onPagSelection(pag) {
				setPagination({
					page: 1,
					rowsPerPage: pag.value
				});
			}
			function getPaginationDiv(child) {
				let control;
				const { rowsPerPage } = computedPagination.value, paginationLabel = props.paginationLabel || $q.lang.table.pagination, paginationSlot = slots.pagination, hasOpts = props.rowsPerPageOptions.length > 1;
				child.push((0, vue.h)("div", { class: "q-table__separator col" }));
				if (hasOpts) child.push((0, vue.h)("div", { class: "q-table__control" }, [(0, vue.h)("span", { class: "q-table__bottom-item" }, [props.rowsPerPageLabel || $q.lang.table.recordsPerPage]), (0, vue.h)(QSelect_default, {
					class: "q-table__select inline q-table__bottom-item",
					color: props.color,
					modelValue: rowsPerPage,
					options: computedRowsPerPageOptions.value,
					displayValue: rowsPerPage === 0 ? $q.lang.table.allRows : rowsPerPage,
					dark: isDark.value,
					borderless: true,
					dense: true,
					optionsDense: true,
					optionsCover: true,
					"onUpdate:modelValue": onPagSelection
				})]));
				if (paginationSlot !== void 0) control = paginationSlot(marginalsScope.value);
				else {
					control = [(0, vue.h)("span", rowsPerPage !== 0 ? { class: "q-table__bottom-item" } : {}, [rowsPerPage ? paginationLabel(firstRowIndex.value + 1, Math.min(lastRowIndex.value, computedRowsNumber.value), computedRowsNumber.value) : paginationLabel(1, filteredSortedRowsNumber.value, computedRowsNumber.value)])];
					if (rowsPerPage !== 0 && pagesNumber.value > 1) {
						const btnProps = {
							color: props.color,
							round: true,
							dense: true,
							flat: true
						};
						if (props.dense) btnProps.size = "sm";
						if (pagesNumber.value > 2) control.push((0, vue.h)(QBtn_default, {
							key: "pgFirst",
							...btnProps,
							icon: navIcon.value[0],
							disable: isFirstPage.value,
							"aria-label": $q.lang.pagination.first,
							onClick: firstPage
						}));
						control.push((0, vue.h)(QBtn_default, {
							key: "pgPrev",
							...btnProps,
							icon: navIcon.value[1],
							disable: isFirstPage.value,
							"aria-label": $q.lang.pagination.prev,
							onClick: prevPage
						}), (0, vue.h)(QBtn_default, {
							key: "pgNext",
							...btnProps,
							icon: navIcon.value[2],
							disable: isLastPage.value,
							"aria-label": $q.lang.pagination.next,
							onClick: nextPage
						}));
						if (pagesNumber.value > 2) control.push((0, vue.h)(QBtn_default, {
							key: "pgLast",
							...btnProps,
							icon: navIcon.value[3],
							disable: isLastPage.value,
							"aria-label": $q.lang.pagination.last,
							onClick: lastPage
						}));
					}
				}
				child.push((0, vue.h)("div", { class: "q-table__control" }, control));
				return child;
			}
			function getGridHeader() {
				return (0, vue.h)("div", { class: "q-table__middle" }, props.gridHeader ? [(0, vue.h)("table", { class: "q-table" }, [getTHead(vue.h)])] : props.loading && slots.loading === void 0 ? getProgress(vue.h) : void 0);
			}
			function getGridBody() {
				const item = slots.item !== void 0 ? slots.item : (scope) => {
					const child = scope.cols.map((col) => (0, vue.h)("div", { class: "q-table__grid-item-row" }, [(0, vue.h)("div", { class: "q-table__grid-item-title" }, [col.label]), (0, vue.h)("div", { class: "q-table__grid-item-value" }, [col.value])]));
					if (hasSelectionMode.value) {
						const slot = slots["body-selection"];
						const content = slot !== void 0 ? slot(scope) : [(0, vue.h)(QCheckbox_default, {
							modelValue: scope.selected,
							color: props.color,
							dark: isDark.value,
							dense: props.dense,
							"onUpdate:modelValue": (adding, evt) => {
								updateSelection([scope.key], [scope.row], adding, evt);
							}
						})];
						child.unshift((0, vue.h)("div", { class: "q-table__grid-item-row" }, content), (0, vue.h)(QSeparator_default, { dark: isDark.value }));
					}
					const data = {
						class: ["q-table__grid-item-card" + cardDefaultClass.value, props.cardClass],
						style: props.cardStyle
					};
					if (props.cardStyleFn !== void 0) data.style = [data.style, props.cardStyleFn(scope.row)];
					if (props.cardClassFn !== void 0) {
						const cls = props.cardClassFn(scope.row);
						if (cls) data.class[0] += ` ${cls}`;
					}
					if (props.onRowClick !== void 0 || props.onRowDblclick !== void 0 || props.onRowContextmenu !== void 0) {
						data.class[0] += " cursor-pointer";
						if (props.onRowClick !== void 0) data.onClick = (evt) => {
							emit("rowClick", evt, scope.row, scope.pageIndex);
						};
						if (props.onRowDblclick !== void 0) data.onDblclick = (evt) => {
							emit("rowDblclick", evt, scope.row, scope.pageIndex);
						};
						if (props.onRowContextmenu !== void 0) data.onContextmenu = (evt) => {
							emit("rowContextmenu", evt, scope.row, scope.pageIndex);
						};
					}
					return (0, vue.h)("div", { class: "q-table__grid-item col-xs-12 col-sm-6 col-md-4 col-lg-3" + (scope.selected ? " q-table__grid-item--selected" : "") }, [(0, vue.h)("div", data, child)]);
				};
				return (0, vue.h)("div", {
					class: ["q-table__grid-content row", props.cardContainerClass],
					style: props.cardContainerStyle
				}, computedRows.value.map((row, pageIndex) => item(getBodyScope({
					key: getRowKey.value(row),
					row,
					pageIndex
				}))));
			}
			Object.assign(vm.proxy, {
				requestServerInteraction,
				setPagination,
				firstPage,
				prevPage,
				nextPage,
				lastPage,
				isRowSelected,
				clearSelection,
				isRowExpanded,
				setExpanded,
				sort,
				resetVirtualScroll,
				scrollTo,
				getCellValue: (colName, row) => {
					const col = computedColsMap.value[colName];
					if (col !== void 0) return getCellValue(col, row);
				}
			});
			injectMultipleProps(vm.proxy, {
				filteredSortedRows: () => filteredSortedRows.value,
				computedRows: () => computedRows.value,
				computedRowsNumber: () => computedRowsNumber.value
			});
			return () => {
				const child = [getTopDiv()];
				const data = {
					ref: rootRef,
					class: rootContainerClass.value
				};
				if (props.grid) child.push(getGridHeader());
				else Object.assign(data, {
					class: [data.class, props.cardClass],
					style: props.cardStyle
				});
				child.push(getBody(), getBottomDiv());
				if (props.loading && slots.loading !== void 0) child.push(slots.loading());
				return (0, vue.h)("div", data, child);
			};
		}
	});
	//#endregion
	//#region src/components/table/QTr.js
	var QTr_default = createComponent({
		name: "QTr",
		props: {
			props: Object,
			noHover: Boolean
		},
		setup(props, { slots }) {
			const classes = (0, vue.computed)(() => "q-tr" + (props.props === void 0 || props.props.header ? "" : " " + props.props.__trClass) + (props.noHover ? " q-tr--no-hover" : ""));
			return () => (0, vue.h)("tr", {
				style: props.props?.__trStyle,
				class: classes.value
			}, hSlot(slots.default));
		}
	});
	//#endregion
	//#region src/components/table/QTd.js
	var QTd_default = createComponent({
		name: "QTd",
		props: {
			props: Object,
			autoWidth: Boolean,
			noHover: Boolean
		},
		setup(props, { slots }) {
			const vm = (0, vue.getCurrentInstance)();
			const classes = (0, vue.computed)(() => "q-td" + (props.autoWidth ? " q-table--col-auto-width" : "") + (props.noHover ? " q-td--no-hover" : "") + " ");
			return () => {
				if (props.props === void 0) return (0, vue.h)("td", { class: classes.value }, hSlot(slots.default));
				const name = vm.vnode.key;
				const col = (props.props.colsMap !== void 0 ? props.props.colsMap[name] : null) || props.props.col;
				if (col === void 0) return;
				const { row } = props.props;
				return (0, vue.h)("td", {
					class: classes.value + col.__tdClass(row),
					style: col.__tdStyle(row)
				}, hSlot(slots.default));
			};
		}
	});
	//#endregion
	//#region src/components/tabs/QRouteTab.js
	var QRouteTab_default = createComponent({
		name: "QRouteTab",
		props: {
			...useRouterLinkProps,
			...useTabProps
		},
		emits: useTabEmits,
		setup(props, { slots, emit }) {
			const routeData = useRouterLink({ useDisableForRouterLinkProps: false });
			const { renderTab, $tabs } = useTab(props, slots, emit, {
				exact: (0, vue.computed)(() => props.exact),
				...routeData
			});
			(0, vue.watch)(() => `${props.name} | ${props.exact} | ${(routeData.resolvedLink.value || {}).href}`, $tabs.verifyRouteModel);
			return () => renderTab(routeData.linkTag.value, routeData.linkAttrs.value);
		}
	});
	//#endregion
	//#region src/components/time/QTime.js
	const defaultDateRE = /^-?[\d]+\/[0-1]\d\/[0-3]\d$/;
	function getViewByModel(model, withSeconds) {
		if (model.hour !== null) {
			if (model.minute === null) return "minute";
			else if (withSeconds && model.second === null) return "second";
		}
		return "hour";
	}
	function getCurrentTime() {
		const d = /* @__PURE__ */ new Date();
		return {
			hour: d.getHours(),
			minute: d.getMinutes(),
			second: d.getSeconds(),
			millisecond: d.getMilliseconds()
		};
	}
	function preventSpace(e) {
		if (e.keyCode === 32) stopAndPrevent(e);
	}
	function getWheelDist(a, b, threshold) {
		const diff = Math.abs(a - b);
		return Math.min(diff, threshold - diff);
	}
	function getValidValues(start, count, testFn) {
		const values = Array.from({ length: count + 1 }, (_, index) => index + start).filter((i) => testFn(i));
		return {
			min: values[0],
			max: values.at(-1),
			values,
			threshold: count + 1
		};
	}
	var QTime_default = createComponent({
		name: "QTime",
		props: {
			...useDarkProps,
			...useFormProps,
			...useDatetimeProps,
			modelValue: {
				required: true,
				validator: (val) => typeof val === "string" || val === null
			},
			mask: {
				...useDatetimeProps.mask,
				default: null
			},
			format24h: {
				type: Boolean,
				default: null
			},
			defaultDate: {
				type: String,
				validator: (v) => defaultDateRE.test(v)
			},
			options: Function,
			hourOptions: Array,
			minuteOptions: Array,
			secondOptions: Array,
			withSeconds: Boolean,
			nowBtn: Boolean
		},
		emits: useDatetimeEmits,
		setup(props, { slots, emit }) {
			const vm = (0, vue.getCurrentInstance)();
			const { $q } = vm.proxy;
			const isDark = useDark(props, $q);
			const { tabindex, headerClass, getLocale, getCurrentDate } = useDatetime(props, $q);
			const injectFormInput = useFormInject(useFormAttrs(props));
			let draggingClockRect, dragCache;
			const clockRef = (0, vue.ref)(null);
			const mask = (0, vue.computed)(() => getMask());
			const locale = (0, vue.computed)(() => getLocale());
			const defaultDateModel = (0, vue.computed)(() => getDefaultDateModel());
			const model = __splitDate(props.modelValue, mask.value, locale.value, props.calendar, defaultDateModel.value);
			const view = (0, vue.ref)(getViewByModel(model));
			const innerModel = (0, vue.ref)(model);
			const isAM = (0, vue.ref)(model.hour === null || model.hour < 12);
			const computedFormat24h = (0, vue.computed)(() => props.format24h !== null ? props.format24h : $q.lang.date.format24h);
			const classes = (0, vue.computed)(() => `q-time q-time--${props.landscape ? "landscape" : "portrait"}` + (isDark.value ? " q-time--dark q-dark" : "") + (props.disable ? " disabled" : props.readonly ? " q-time--readonly" : "") + (props.bordered ? " q-time--bordered" : "") + (props.square ? " q-time--square no-border-radius" : "") + (props.flat ? " q-time--flat no-shadow" : ""));
			const stringModel = (0, vue.computed)(() => {
				const time = innerModel.value;
				return {
					hour: time.hour === null ? "--" : computedFormat24h.value ? pad(time.hour) : String(isAM.value ? time.hour === 0 ? 12 : time.hour : time.hour > 12 ? time.hour - 12 : time.hour),
					minute: time.minute === null ? "--" : pad(time.minute),
					second: time.second === null ? "--" : pad(time.second)
				};
			});
			const pointerStyle = (0, vue.computed)(() => {
				const forHour = view.value === "hour", divider = forHour ? 12 : 60, amount = innerModel.value[view.value];
				let transform = `rotate(${Math.round(amount * (360 / divider)) - 180}deg) translateX(-50%)`;
				if (forHour && computedFormat24h.value && innerModel.value.hour >= 12) transform += " scale(.7)";
				return { transform };
			});
			const minLink = (0, vue.computed)(() => innerModel.value.hour !== null);
			const secLink = (0, vue.computed)(() => minLink.value && innerModel.value.minute !== null);
			const hourInSelection = (0, vue.computed)(() => props.hourOptions !== void 0 ? (val) => props.hourOptions.includes(val) : props.options !== void 0 ? (val) => props.options(val, null, null) : null);
			const minuteInSelection = (0, vue.computed)(() => props.minuteOptions !== void 0 ? (val) => props.minuteOptions.includes(val) : props.options !== void 0 ? (val) => props.options(innerModel.value.hour, val, null) : null);
			const secondInSelection = (0, vue.computed)(() => props.secondOptions !== void 0 ? (val) => props.secondOptions.includes(val) : props.options !== void 0 ? (val) => props.options(innerModel.value.hour, innerModel.value.minute, val) : null);
			const validHours = (0, vue.computed)(() => {
				if (hourInSelection.value === null) return null;
				const am = getValidValues(0, 11, hourInSelection.value);
				const pm = getValidValues(12, 11, hourInSelection.value);
				return {
					am,
					pm,
					values: [...am.values, ...pm.values]
				};
			});
			const validMinutes = (0, vue.computed)(() => minuteInSelection.value !== null ? getValidValues(0, 59, minuteInSelection.value) : null);
			const validSeconds = (0, vue.computed)(() => secondInSelection.value !== null ? getValidValues(0, 59, secondInSelection.value) : null);
			const viewValidOptions = (0, vue.computed)(() => {
				switch (view.value) {
					case "hour": return validHours.value;
					case "minute": return validMinutes.value;
					case "second": return validSeconds.value;
				}
			});
			const positions = (0, vue.computed)(() => {
				let end, offset = 0, step = 1;
				const values = viewValidOptions.value !== null ? viewValidOptions.value.values : void 0;
				if (view.value === "hour") if (computedFormat24h.value) end = 23;
				else {
					end = 11;
					if (!isAM.value) offset = 12;
				}
				else {
					end = 55;
					step = 5;
				}
				const pos = [];
				for (let val = 0, index = 0; val <= end; val += step, index++) {
					const actualVal = val + offset, disable = values?.includes(actualVal) === false, label = view.value === "hour" && val === 0 ? computedFormat24h.value ? "00" : "12" : val;
					pos.push({
						val: actualVal,
						index,
						disable,
						label
					});
				}
				return pos;
			});
			const clockDirectives = (0, vue.computed)(() => [[
				TouchPan_default,
				onPan,
				void 0,
				{
					stop: true,
					prevent: true,
					mouse: true
				}
			]]);
			(0, vue.watch)(() => props.modelValue, (v) => {
				const val = __splitDate(v, mask.value, locale.value, props.calendar, defaultDateModel.value);
				if (val.dateHash !== innerModel.value.dateHash || val.timeHash !== innerModel.value.timeHash) {
					innerModel.value = val;
					if (val.hour === null) view.value = "hour";
					else isAM.value = val.hour < 12;
				}
			});
			(0, vue.watch)([mask, locale], () => {
				(0, vue.nextTick)(() => {
					updateValue();
				});
			});
			function setNow() {
				const date = {
					...getCurrentDate(),
					...getCurrentTime()
				};
				updateValue(date);
				Object.assign(innerModel.value, date);
				view.value = "hour";
			}
			function getNormalizedClockValue(val, { min, max, values, threshold }) {
				if (val === min) return min;
				if (val < min || val > max) return getWheelDist(val, min, threshold) <= getWheelDist(val, max, threshold) ? min : max;
				const index = values.findIndex((v) => val <= v), before = values[index - 1], after = values[index];
				return val - before <= after - val ? before : after;
			}
			function getMask() {
				return props.calendar !== "persian" && props.mask !== null ? props.mask : `HH:mm${props.withSeconds ? ":ss" : ""}`;
			}
			function getDefaultDateModel() {
				if (typeof props.defaultDate !== "string") {
					const date = getCurrentDate(true);
					date.dateHash = getDayHash(date);
					return date;
				}
				return __splitDate(props.defaultDate, "YYYY/MM/DD", void 0, props.calendar);
			}
			function shouldAbortInteraction() {
				return vmIsDestroyed(vm) || viewValidOptions.value !== null && (viewValidOptions.value.values.length === 0 || view.value === "hour" && !computedFormat24h.value && validHours.value[isAM.value ? "am" : "pm"].values.length === 0);
			}
			function getClockRect() {
				const { top, left, width } = clockRef.value.getBoundingClientRect(), dist = width / 2;
				return {
					top: top + dist,
					left: left + dist,
					dist: dist * .7
				};
			}
			function onPan(event) {
				if (shouldAbortInteraction()) return;
				if (event.isFirst) {
					draggingClockRect = getClockRect();
					dragCache = updateClock(event.evt, draggingClockRect);
					return;
				}
				dragCache = updateClock(event.evt, draggingClockRect, dragCache);
				if (event.isFinal) {
					draggingClockRect = false;
					dragCache = null;
					goToNextView();
				}
			}
			function goToNextView() {
				if (view.value === "hour") view.value = "minute";
				else if (props.withSeconds && view.value === "minute") view.value = "second";
			}
			function updateClock(evt, clockRect, cacheVal) {
				const pos = position(evt), height = Math.abs(pos.top - clockRect.top), distance = Math.hypot(pos.top - clockRect.top, pos.left - clockRect.left);
				let val, angle = Math.asin(height / distance) * (180 / Math.PI);
				if (pos.top < clockRect.top) angle = clockRect.left < pos.left ? 90 - angle : 270 + angle;
				else angle = clockRect.left < pos.left ? angle + 90 : 270 - angle;
				if (view.value === "hour") {
					val = angle / 30;
					if (validHours.value !== null) {
						const am = !computedFormat24h.value ? isAM.value : validHours.value.am.values.length !== 0 && validHours.value.pm.values.length !== 0 ? distance >= clockRect.dist : validHours.value.am.values.length !== 0;
						val = getNormalizedClockValue(val + (am ? 0 : 12), validHours.value[am ? "am" : "pm"]);
					} else {
						val = Math.round(val);
						if (computedFormat24h.value) {
							if (distance < clockRect.dist) {
								if (val < 12) val += 12;
							} else if (val === 12) val = 0;
						} else if (isAM.value && val === 12) val = 0;
						else if (!isAM.value && val !== 12) val += 12;
					}
					if (computedFormat24h.value) isAM.value = val < 12;
				} else {
					val = Math.round(angle / 6) % 60;
					if (view.value === "minute" && validMinutes.value !== null) val = getNormalizedClockValue(val, validMinutes.value);
					else if (view.value === "second" && validSeconds.value !== null) val = getNormalizedClockValue(val, validSeconds.value);
				}
				if (cacheVal !== val) setModel[view.value](val);
				return val;
			}
			const setView = {
				hour() {
					view.value = "hour";
				},
				minute() {
					view.value = "minute";
				},
				second() {
					view.value = "second";
				}
			};
			function setAmOnKey(e) {
				if ([13, 32].includes(e.keyCode)) {
					setAm();
					stopAndPrevent(e);
				}
			}
			function setPmOnKey(e) {
				if ([13, 32].includes(e.keyCode)) {
					setPm();
					stopAndPrevent(e);
				}
			}
			function onClick(evt) {
				if (!shouldAbortInteraction()) {
					if (!$q.platform.is.desktop) updateClock(evt, getClockRect());
					goToNextView();
				}
			}
			function onMousedown(evt) {
				if (!shouldAbortInteraction()) updateClock(evt, getClockRect());
			}
			function onKeyupHour(e) {
				if ([13, 32].includes(e.keyCode)) {
					view.value = "hour";
					stopAndPrevent(e);
				} else if ([37, 39].includes(e.keyCode)) {
					const payload = e.keyCode === 37 ? -1 : 1;
					if (validHours.value !== null) {
						const values = computedFormat24h.value ? validHours.value.values : validHours.value[isAM.value ? "am" : "pm"].values;
						if (values.length === 0) return;
						if (innerModel.value.hour === null) setHour(values[0]);
						else setHour(values[(values.length + values.indexOf(innerModel.value.hour) + payload) % values.length]);
					} else {
						const wrap = computedFormat24h.value ? 24 : 12;
						setHour((!computedFormat24h.value && !isAM.value ? 12 : 0) + (24 + (innerModel.value.hour === null ? -payload : innerModel.value.hour) + payload) % wrap);
					}
				}
			}
			function onKeyupMinute(e) {
				if ([13, 32].includes(e.keyCode)) {
					view.value = "minute";
					stopAndPrevent(e);
				} else if ([37, 39].includes(e.keyCode)) {
					const payload = e.keyCode === 37 ? -1 : 1;
					if (validMinutes.value !== null) {
						const values = validMinutes.value.values;
						if (values.length === 0) return;
						if (innerModel.value.minute === null) setMinute(values[0]);
						else setMinute(values[(values.length + values.indexOf(innerModel.value.minute) + payload) % values.length]);
					} else setMinute((60 + (innerModel.value.minute === null ? -payload : innerModel.value.minute) + payload) % 60);
				}
			}
			function onKeyupSecond(e) {
				if ([13, 32].includes(e.keyCode)) {
					view.value = "second";
					stopAndPrevent(e);
				} else if ([37, 39].includes(e.keyCode)) {
					const payload = e.keyCode === 37 ? -1 : 1;
					if (validSeconds.value !== null) {
						const values = validSeconds.value.values;
						if (values.length === 0) return;
						if (innerModel.value.second === null) setSecond(values[0]);
						else setSecond(values[(values.length + values.indexOf(innerModel.value.second) + payload) % values.length]);
					} else setSecond((60 + (innerModel.value.second === null ? -payload : innerModel.value.second) + payload) % 60);
				}
			}
			function setHour(hour) {
				if (innerModel.value.hour !== hour) {
					innerModel.value.hour = hour;
					verifyAndUpdate();
				}
			}
			function setMinute(minute) {
				if (innerModel.value.minute !== minute) {
					innerModel.value.minute = minute;
					verifyAndUpdate();
				}
			}
			function setSecond(second) {
				if (innerModel.value.second !== second) {
					innerModel.value.second = second;
					verifyAndUpdate();
				}
			}
			const setModel = {
				hour: setHour,
				minute: setMinute,
				second: setSecond
			};
			function setAm() {
				if (!isAM.value) {
					isAM.value = true;
					if (innerModel.value.hour !== null) {
						innerModel.value.hour -= 12;
						verifyAndUpdate();
					}
				}
			}
			function setPm() {
				if (isAM.value) {
					isAM.value = false;
					if (innerModel.value.hour !== null) {
						innerModel.value.hour += 12;
						verifyAndUpdate();
					}
				}
			}
			function goToViewWhenHasModel(newView) {
				const val = props.modelValue;
				if (view.value !== newView && val !== void 0 && val !== null && val !== "" && typeof val !== "string") view.value = newView;
			}
			function verifyAndUpdate() {
				if (hourInSelection.value !== null && !hourInSelection.value(innerModel.value.hour)) {
					innerModel.value = __splitDate();
					goToViewWhenHasModel("hour");
					return;
				}
				if (minuteInSelection.value !== null && !minuteInSelection.value(innerModel.value.minute)) {
					innerModel.value.minute = null;
					innerModel.value.second = null;
					goToViewWhenHasModel("minute");
					return;
				}
				if (props.withSeconds && secondInSelection.value !== null && !secondInSelection.value(innerModel.value.second)) {
					innerModel.value.second = null;
					goToViewWhenHasModel("second");
					return;
				}
				if (innerModel.value.hour === null || innerModel.value.minute === null || props.withSeconds && innerModel.value.second === null) return;
				updateValue();
			}
			function updateValue(obj) {
				const date = {
					...innerModel.value,
					...obj
				};
				const val = props.calendar === "persian" ? pad(date.hour) + ":" + pad(date.minute) + (props.withSeconds ? ":" + pad(date.second) : "") : formatDate(new Date(date.year, date.month === null ? null : date.month - 1, date.day, date.hour, date.minute, date.second, date.millisecond), mask.value, locale.value, date.year, date.timezoneOffset);
				date.changed = val !== props.modelValue;
				emit("update:modelValue", val, date);
			}
			function getHeader() {
				const label = [
					(0, vue.h)("div", {
						class: "q-time__link " + (view.value === "hour" ? "q-time__link--active" : "cursor-pointer"),
						tabindex: tabindex.value,
						role: "button",
						"aria-pressed": view.value === "hour" ? "true" : "false",
						onClick: setView.hour,
						onKeydown: preventSpace,
						onKeyup: onKeyupHour
					}, stringModel.value.hour),
					(0, vue.h)("div", ":"),
					(0, vue.h)("div", minLink.value ? {
						class: "q-time__link " + (view.value === "minute" ? "q-time__link--active" : "cursor-pointer"),
						tabindex: tabindex.value,
						role: "button",
						"aria-pressed": view.value === "minute" ? "true" : "false",
						onKeydown: preventSpace,
						onKeyup: onKeyupMinute,
						onClick: setView.minute
					} : { class: "q-time__link" }, stringModel.value.minute)
				];
				if (props.withSeconds) label.push((0, vue.h)("div", ":"), (0, vue.h)("div", secLink.value ? {
					class: "q-time__link " + (view.value === "second" ? "q-time__link--active" : "cursor-pointer"),
					tabindex: tabindex.value,
					role: "button",
					"aria-pressed": view.value === "second" ? "true" : "false",
					onKeydown: preventSpace,
					onKeyup: onKeyupSecond,
					onClick: setView.second
				} : { class: "q-time__link" }, stringModel.value.second));
				const child = [(0, vue.h)("div", {
					class: "q-time__header-label row items-center no-wrap",
					dir: "ltr"
				}, label)];
				if (!computedFormat24h.value) child.push((0, vue.h)("div", { class: "q-time__header-ampm column items-between no-wrap" }, [(0, vue.h)("div", {
					class: "q-time__link " + (isAM.value ? "q-time__link--active" : "cursor-pointer"),
					tabindex: tabindex.value,
					role: "button",
					"aria-pressed": isAM.value ? "true" : "false",
					onClick: setAm,
					onKeydown: preventSpace,
					onKeyup: setAmOnKey
				}, "AM"), (0, vue.h)("div", {
					class: "q-time__link " + (isAM.value ? "cursor-pointer" : "q-time__link--active"),
					tabindex: tabindex.value,
					role: "button",
					"aria-pressed": isAM.value ? "false" : "true",
					onClick: setPm,
					onKeydown: preventSpace,
					onKeyup: setPmOnKey
				}, "PM")]));
				return (0, vue.h)("div", { class: "q-time__header flex flex-center no-wrap " + headerClass.value }, child);
			}
			function getClock() {
				const current = innerModel.value[view.value];
				return (0, vue.h)("div", { class: "q-time__content col relative-position" }, [(0, vue.h)(vue.Transition, { name: "q-transition--scale" }, () => (0, vue.h)("div", {
					key: "clock" + view.value,
					class: "q-time__container-parent absolute-full"
				}, [(0, vue.h)("div", {
					ref: clockRef,
					class: "q-time__container-child fit overflow-hidden"
				}, [(0, vue.withDirectives)((0, vue.h)("div", {
					class: "q-time__clock cursor-pointer non-selectable",
					onClick,
					onMousedown
				}, [(0, vue.h)("div", { class: "q-time__clock-circle fit" }, [(0, vue.h)("div", {
					class: "q-time__clock-pointer" + (innerModel.value[view.value] === null ? " hidden" : props.color !== void 0 ? ` text-${props.color}` : ""),
					style: pointerStyle.value
				}), positions.value.map((pos) => (0, vue.h)("div", { class: `q-time__clock-position row flex-center q-time__clock-pos-${pos.index}` + (pos.val === current ? " q-time__clock-position--active " + headerClass.value : pos.disable ? " q-time__clock-position--disable" : "") }, [(0, vue.h)("span", pos.label)]))])]), clockDirectives.value)])])), props.nowBtn ? (0, vue.h)(QBtn_default, {
					class: "q-time__now-button absolute",
					icon: $q.iconSet.datetime.now,
					unelevated: true,
					size: "sm",
					round: true,
					color: props.color,
					textColor: props.textColor,
					tabindex: tabindex.value,
					onClick: setNow
				}) : null]);
			}
			vm.proxy.setNow = setNow;
			return () => {
				const child = [getClock()];
				const def = hSlot(slots.default);
				if (def !== void 0) child.push((0, vue.h)("div", { class: "q-time__actions" }, def));
				if (props.name !== void 0 && !props.disable) injectFormInput(child, "push");
				return (0, vue.h)("div", {
					class: classes.value,
					tabindex: -1
				}, [getHeader(), (0, vue.h)("div", { class: "q-time__main col overflow-auto" }, child)]);
			};
		}
	});
	//#endregion
	//#region src/components/timeline/QTimeline.js
	const sideValues = ["left", "right"];
	const layoutValues = [
		"dense",
		"comfortable",
		"loose"
	];
	var QTimeline_default = createComponent({
		name: "QTimeline",
		props: {
			...useDarkProps,
			color: {
				type: String,
				default: "primary"
			},
			side: {
				type: String,
				default: "right",
				validator: (v) => sideValues.includes(v)
			},
			layout: {
				type: String,
				default: "dense",
				validator: (v) => layoutValues.includes(v)
			}
		},
		setup(props, { slots }) {
			const isDark = useDark(props, (0, vue.getCurrentInstance)().proxy.$q);
			(0, vue.provide)(timelineKey, props);
			const classes = (0, vue.computed)(() => `q-timeline q-timeline--${props.layout} q-timeline--${props.layout}--${props.side}` + (isDark.value ? " q-timeline--dark" : ""));
			return () => (0, vue.h)("ul", { class: classes.value }, hSlot(slots.default));
		}
	});
	//#endregion
	//#region src/components/timeline/QTimelineEntry.js
	var QTimelineEntry_default = createComponent({
		name: "QTimelineEntry",
		props: {
			heading: Boolean,
			tag: {
				type: String,
				default: "h3"
			},
			side: {
				type: String,
				default: "right",
				validator: (v) => ["left", "right"].includes(v)
			},
			icon: String,
			avatar: String,
			color: String,
			title: String,
			subtitle: String,
			body: String
		},
		setup(props, { slots }) {
			const $timeline = (0, vue.inject)(timelineKey, emptyRenderFn);
			if ($timeline === emptyRenderFn) {
				console.error("QTimelineEntry needs to be child of QTimeline");
				return emptyRenderFn;
			}
			const classes = (0, vue.computed)(() => `q-timeline__entry q-timeline__entry--${props.side}` + (props.icon !== void 0 || props.avatar !== void 0 ? " q-timeline__entry--icon" : ""));
			const dotClass = (0, vue.computed)(() => `q-timeline__dot text-${props.color || $timeline.color}`);
			const reverse = (0, vue.computed)(() => $timeline.layout === "comfortable" && $timeline.side === "left");
			return () => {
				const child = hUniqueSlot(slots.default, []);
				if (props.body !== void 0) child.unshift(props.body);
				if (props.heading) {
					const content = [
						(0, vue.h)("div"),
						(0, vue.h)("div"),
						(0, vue.h)(props.tag, { class: "q-timeline__heading-title" }, child)
					];
					return (0, vue.h)("div", { class: "q-timeline__heading" }, reverse.value ? content.reverse() : content);
				}
				let dot;
				if (props.icon !== void 0) dot = [(0, vue.h)(QIcon_default, {
					class: "row items-center justify-center",
					name: props.icon
				})];
				else if (props.avatar !== void 0) dot = [(0, vue.h)("img", {
					class: "q-timeline__dot-img",
					src: props.avatar
				})];
				const content = [
					(0, vue.h)("div", { class: "q-timeline__subtitle" }, [(0, vue.h)("span", {}, hSlot(slots.subtitle, [props.subtitle]))]),
					(0, vue.h)("div", { class: dotClass.value }, dot),
					(0, vue.h)("div", { class: "q-timeline__content" }, [(0, vue.h)("h6", { class: "q-timeline__title" }, hSlot(slots.title, [props.title]))].concat(child))
				];
				return (0, vue.h)("li", { class: classes.value }, reverse.value ? content.reverse() : content);
			};
		}
	});
	//#endregion
	//#region src/components/toolbar/QToolbar.js
	var QToolbar_default = createComponent({
		name: "QToolbar",
		props: { inset: Boolean },
		setup(props, { slots }) {
			const classes = (0, vue.computed)(() => "q-toolbar row no-wrap items-center" + (props.inset ? " q-toolbar--inset" : ""));
			return () => (0, vue.h)("div", {
				class: classes.value,
				role: "toolbar"
			}, hSlot(slots.default));
		}
	});
	//#endregion
	//#region src/components/toolbar/QToolbarTitle.js
	var QToolbarTitle_default = createComponent({
		name: "QToolbarTitle",
		props: { shrink: Boolean },
		setup(props, { slots }) {
			const classes = (0, vue.computed)(() => "q-toolbar__title ellipsis" + (props.shrink ? " col-shrink" : ""));
			return () => (0, vue.h)("div", { class: classes.value }, hSlot(slots.default));
		}
	});
	//#endregion
	//#region src/components/tree/QTree.js
	const tickStrategyOptions = [
		"none",
		"strict",
		"leaf",
		"leaf-filtered"
	];
	function getNodeMedia(node) {
		if (node.icon !== void 0) return (0, vue.h)(QIcon_default, {
			class: "q-tree__icon q-mr-sm",
			name: node.icon,
			color: node.iconColor
		});
		const src = node.img || node.avatar;
		if (src) return (0, vue.h)("img", {
			class: `q-tree__${node.img ? "img" : "avatar"} q-mr-sm`,
			src
		});
	}
	var QTree_default = createComponent({
		name: "QTree",
		props: {
			...useDarkProps,
			nodes: {
				type: Array,
				required: true
			},
			nodeKey: {
				type: String,
				required: true
			},
			labelKey: {
				type: String,
				default: "label"
			},
			childrenKey: {
				type: String,
				default: "children"
			},
			dense: Boolean,
			color: String,
			controlColor: String,
			textColor: String,
			selectedColor: String,
			icon: String,
			tickStrategy: {
				type: String,
				default: "none",
				validator: (v) => tickStrategyOptions.includes(v)
			},
			ticked: Array,
			expanded: Array,
			selected: {},
			noSelectionUnset: Boolean,
			defaultExpandAll: Boolean,
			accordion: Boolean,
			filter: String,
			filterMethod: Function,
			duration: {},
			noConnectors: Boolean,
			noTransition: Boolean,
			noNodesLabel: String,
			noResultsLabel: String
		},
		emits: [
			"update:expanded",
			"update:ticked",
			"update:selected",
			"lazyLoad",
			"afterShow",
			"afterHide"
		],
		setup(props, { slots, emit }) {
			const { proxy } = (0, vue.getCurrentInstance)();
			const { $q } = proxy;
			const isDark = useDark(props, $q);
			const lazy = (0, vue.ref)({});
			const innerTicked = (0, vue.ref)(props.ticked || []);
			const innerExpanded = (0, vue.ref)(props.expanded || []);
			const focusedKey = (0, vue.ref)(null);
			let blurTargets = {}, headerTargets = {};
			(0, vue.onBeforeUpdate)(() => {
				blurTargets = {};
				headerTargets = {};
			});
			const classes = (0, vue.computed)(() => `q-tree q-tree--${props.dense ? "dense" : "standard"}` + (props.noConnectors ? " q-tree--no-connectors" : "") + (isDark.value ? " q-tree--dark" : "") + (props.color !== void 0 ? ` text-${props.color}` : ""));
			const hasSelection = (0, vue.computed)(() => props.selected !== void 0);
			const computedIcon = (0, vue.computed)(() => props.icon || $q.iconSet.tree.icon);
			const computedControlColor = (0, vue.computed)(() => props.controlColor || props.color);
			const textColorClass = (0, vue.computed)(() => props.textColor !== void 0 ? ` text-${props.textColor}` : "");
			const selectedColorClass = (0, vue.computed)(() => {
				const color = props.selectedColor || props.color;
				return color ? ` text-${color}` : "";
			});
			const computedFilterMethod = (0, vue.computed)(() => props.filterMethod !== void 0 ? props.filterMethod : (node, filter) => {
				const filt = filter.toLowerCase();
				return node[props.labelKey] && node[props.labelKey].toLowerCase().includes(filt);
			});
			const meta = (0, vue.computed)(() => {
				const acc = {};
				const travel = (node, parent) => {
					const tickStrategy = node.tickStrategy || (parent ? parent.tickStrategy : props.tickStrategy);
					const key = node[props.nodeKey], isParent = node[props.childrenKey] && Array.isArray(node[props.childrenKey]) && node[props.childrenKey].length !== 0, selectable = !node.disabled && hasSelection.value && node.selectable !== false, expandable = !node.disabled && node.expandable !== false, hasTicking = tickStrategy !== "none", strictTicking = tickStrategy === "strict", leafFilteredTicking = tickStrategy === "leaf-filtered", leafTicking = tickStrategy === "leaf" || tickStrategy === "leaf-filtered";
					let tickable = !node.disabled && node.tickable !== false;
					if (leafTicking && tickable === true && parent && parent.tickable !== true) tickable = false;
					let localLazy = node.lazy;
					if (localLazy === true && lazy.value[key] !== void 0 && Array.isArray(node[props.childrenKey])) localLazy = lazy.value[key];
					const m = {
						key,
						parent,
						isParent,
						lazy: localLazy,
						disabled: node.disabled,
						link: !node.disabled && (selectable || expandable && (isParent || localLazy === true)),
						children: [],
						matchesFilter: props.filter ? computedFilterMethod.value(node, props.filter) : true,
						selected: key === props.selected && selectable,
						selectable,
						expanded: isParent ? innerExpanded.value.includes(key) : false,
						expandable,
						noTick: node.noTick === true || !strictTicking && localLazy && localLazy !== "loaded",
						tickable,
						tickStrategy,
						hasTicking,
						strictTicking,
						leafFilteredTicking,
						leafTicking,
						ticked: strictTicking ? innerTicked.value.includes(key) : isParent ? false : innerTicked.value.includes(key)
					};
					acc[key] = m;
					if (isParent) {
						m.children = node[props.childrenKey].map((n) => travel(n, m));
						if (props.filter) {
							if (m.matchesFilter !== true) m.matchesFilter = m.children.some((n) => n.matchesFilter);
							else if (m.noTick !== true && m.disabled !== true && m.tickable === true && leafFilteredTicking && m.children.every((n) => n.matchesFilter !== true || n.noTick === true || n.tickable !== true)) m.tickable = false;
						}
						if (m.matchesFilter === true) {
							if (m.noTick !== true && strictTicking !== true && m.children.every((n) => n.noTick)) m.noTick = true;
							if (leafTicking) {
								m.ticked = false;
								m.indeterminate = m.children.some((entry) => entry.indeterminate === true);
								m.tickable = m.tickable === true && m.children.some((entry) => entry.tickable);
								if (m.indeterminate !== true) {
									const sel = m.children.reduce((localAcc, entry) => entry.ticked === true ? localAcc + 1 : localAcc, 0);
									if (sel === m.children.length) m.ticked = true;
									else if (sel > 0) m.indeterminate = true;
								}
								if (m.indeterminate === true) m.indeterminateNextState = m.children.every((entry) => entry.tickable !== true || entry.ticked !== true);
							}
						}
					}
					return m;
				};
				props.nodes.forEach((node) => travel(node, null));
				return acc;
			});
			const focusableKeys = (0, vue.computed)(() => {
				const acc = [];
				function travel(nodes) {
					nodes.forEach((node) => {
						const localMeta = meta.value[node[props.nodeKey]];
						if (props.filter && localMeta.matchesFilter !== true) return;
						if (localMeta.link === true) acc.push(localMeta.key);
						if (localMeta.expanded === true && Array.isArray(node[props.childrenKey])) travel(node[props.childrenKey]);
					});
				}
				travel(props.nodes);
				return acc;
			});
			const tabKey = (0, vue.computed)(() => {
				const keys = focusableKeys.value;
				if (keys.includes(focusedKey.value)) return focusedKey.value;
				const selected = keys.find((key) => meta.value[key].selected === true);
				return selected !== void 0 ? selected : keys[0];
			});
			(0, vue.watch)(() => props.ticked, (val) => {
				innerTicked.value = val;
			});
			(0, vue.watch)(() => props.expanded, (val) => {
				innerExpanded.value = val;
			});
			function getNodeByKey(key) {
				const find = (result, node) => {
					if (result || !node) return result;
					if (Array.isArray(node)) return node.reduce(find, result);
					if (node[props.nodeKey] === key) return node;
					if (node[props.childrenKey]) return find(null, node[props.childrenKey]);
				};
				return find(null, props.nodes);
			}
			function getTickedNodes() {
				return innerTicked.value.map((key) => getNodeByKey(key));
			}
			function getExpandedNodes() {
				return innerExpanded.value.map((key) => getNodeByKey(key));
			}
			function isExpanded(key) {
				return key && meta.value[key] ? meta.value[key].expanded : false;
			}
			function collapseAll() {
				if (props.expanded !== void 0) emit("update:expanded", []);
				else innerExpanded.value = [];
			}
			function expandAll() {
				const expanded = [];
				const travel = (node) => {
					if (node[props.childrenKey] && node[props.childrenKey].length !== 0 && node.expandable !== false && node.disabled !== true) {
						expanded.push(node[props.nodeKey]);
						node[props.childrenKey].forEach(travel);
					}
				};
				props.nodes.forEach(travel);
				if (props.expanded !== void 0) emit("update:expanded", expanded);
				else innerExpanded.value = expanded;
			}
			function setExpanded(key, state, node = getNodeByKey(key), m = meta.value[key]) {
				if (m.lazy && m.lazy !== "loaded") {
					if (m.lazy === "loading") return;
					lazy.value[key] = "loading";
					if (!Array.isArray(node[props.childrenKey])) node[props.childrenKey] = [];
					emit("lazyLoad", {
						node,
						key,
						done: (children) => {
							lazy.value[key] = "loaded";
							node[props.childrenKey] = Array.isArray(children) ? children : [];
							(0, vue.nextTick)(() => {
								if (meta.value[key]?.isParent === true) localSetExpanded(key, true);
							});
						},
						fail: () => {
							delete lazy.value[key];
							if (node[props.childrenKey].length === 0) delete node[props.childrenKey];
						}
					});
				} else if (m.isParent === true && m.expandable === true) localSetExpanded(key, state);
			}
			function localSetExpanded(key, state) {
				let target = innerExpanded.value;
				const shouldEmit = props.expanded !== void 0;
				if (shouldEmit) target = [...target];
				if (state) {
					if (props.accordion && meta.value[key]) {
						const collapse = [];
						if (meta.value[key].parent) meta.value[key].parent.children.forEach((m) => {
							if (m.key !== key && m.expandable === true) collapse.push(m.key);
						});
						else props.nodes.forEach((node) => {
							const k = node[props.nodeKey];
							if (k !== key) collapse.push(k);
						});
						if (collapse.length !== 0) target = target.filter((k) => !collapse.includes(k));
					}
					target = [...target, key].filter((entryKey, index, self) => self.indexOf(entryKey) === index);
				} else target = target.filter((k) => k !== key);
				if (shouldEmit) emit("update:expanded", target);
				else innerExpanded.value = target;
			}
			function isTicked(key) {
				return key && meta.value[key] ? meta.value[key].ticked : false;
			}
			function setTicked(keys, state) {
				let target = innerTicked.value;
				const shouldEmit = props.ticked !== void 0;
				if (shouldEmit) target = [...target];
				target = state ? [...target, ...keys].filter((key, index, self) => self.indexOf(key) === index) : target.filter((k) => !keys.includes(k));
				if (shouldEmit) emit("update:ticked", target);
			}
			function getSlotScope(node, localMeta, key) {
				const scope = {
					tree: proxy,
					node,
					key,
					color: props.color,
					dark: isDark.value
				};
				injectProp(scope, "expanded", () => localMeta.expanded, (val) => {
					if (val !== localMeta.expanded) setExpanded(key, val);
				});
				injectProp(scope, "ticked", () => localMeta.ticked, (val) => {
					if (val !== localMeta.ticked) setTicked([key], val);
				});
				return scope;
			}
			function getChildren(nodes) {
				return (props.filter ? nodes.filter((n) => meta.value[n[props.nodeKey]].matchesFilter) : nodes).map((child) => getNode(child));
			}
			function onShow() {
				emit("afterShow");
			}
			function onHide() {
				emit("afterHide");
			}
			function getNode(node) {
				const key = node[props.nodeKey], m = meta.value[key], header = node.header ? slots[`header-${node.header}`] || slots["default-header"] : slots["default-header"];
				const children = m.isParent === true ? getChildren(node[props.childrenKey]) : [];
				const isParent = children.length !== 0 || m.lazy && m.lazy !== "loaded";
				let body = node.body ? slots[`body-${node.body}`] || slots["default-body"] : slots["default-body"];
				const slotScope = header !== void 0 || body !== void 0 ? getSlotScope(node, m, key) : null;
				if (body !== void 0) body = (0, vue.h)("div", { class: "q-tree__node-body relative-position" }, [(0, vue.h)("div", { class: textColorClass.value }, [body(slotScope)])]);
				return (0, vue.h)("div", {
					key,
					class: `q-tree__node relative-position q-tree__node--${isParent ? "parent" : "child"}`
				}, [(0, vue.h)("div", {
					class: "q-tree__node-header relative-position row no-wrap items-center" + (m.link === true ? " q-tree__node--link q-hoverable q-focusable" : "") + (m.selected === true ? " q-tree__node--selected" : "") + (m.disabled === true ? " q-tree__node--disabled" : ""),
					ref: (el) => {
						headerTargets[m.key] = el;
					},
					tabindex: m.link === true && m.key === tabKey.value ? 0 : -1,
					"aria-expanded": isParent ? m.expanded ? "true" : "false" : null,
					"aria-selected": m.selectable ? m.selected ? "true" : "false" : null,
					"aria-disabled": m.disabled === true ? "true" : null,
					role: "treeitem",
					onFocus() {
						if (m.link === true) focusedKey.value = m.key;
					},
					onClick: (e) => {
						onClick(node, m, e);
					},
					onKeydown(e) {
						if (shouldIgnoreKey(e) !== true) {
							if (e.keyCode === 13) onClick(node, m, e, true);
							else if (e.keyCode === 32) onExpandClick(node, m, e, true);
							else if (onNavigationKey(m, e.keyCode)) stopAndPrevent(e);
						}
					}
				}, [
					(0, vue.h)("div", {
						class: "q-focus-helper",
						tabindex: -1,
						ref: (el) => {
							blurTargets[m.key] = el;
						}
					}),
					m.lazy === "loading" ? (0, vue.h)(QSpinner_default, {
						class: "q-tree__spinner",
						color: computedControlColor.value
					}) : isParent ? (0, vue.h)(QIcon_default, {
						class: "q-tree__arrow" + (m.expanded === true ? " q-tree__arrow--rotate" : ""),
						name: computedIcon.value,
						onClick(e) {
							onExpandClick(node, m, e);
						}
					}) : null,
					m.hasTicking === true && m.noTick !== true ? (0, vue.h)(QCheckbox_default, {
						class: "q-tree__tickbox",
						modelValue: m.indeterminate === true ? null : m.ticked,
						color: computedControlColor.value,
						dark: isDark.value,
						dense: true,
						keepColor: true,
						disable: m.tickable !== true,
						onKeydown: stopAndPrevent,
						"onUpdate:modelValue": (v) => {
							onTickedClick(m, v);
						}
					}) : null,
					(0, vue.h)("div", { class: "q-tree__node-header-content col row no-wrap items-center" + (m.selected === true ? selectedColorClass.value : textColorClass.value) }, [header ? header(slotScope) : [getNodeMedia(node), (0, vue.h)("div", node[props.labelKey])]])
				]), isParent ? props.noTransition ? m.expanded === true ? (0, vue.h)("div", {
					class: "q-tree__node-collapsible" + textColorClass.value,
					key: `${key}__q`
				}, [body, (0, vue.h)("div", {
					class: "q-tree__children" + (m.disabled === true ? " q-tree__node--disabled" : ""),
					role: "group"
				}, children)]) : null : (0, vue.h)(QSlideTransition_default, {
					duration: props.duration,
					onShow,
					onHide
				}, () => (0, vue.withDirectives)((0, vue.h)("div", {
					class: "q-tree__node-collapsible" + textColorClass.value,
					key: `${key}__q`
				}, [body, (0, vue.h)("div", {
					class: "q-tree__children" + (m.disabled === true ? " q-tree__node--disabled" : ""),
					role: "group"
				}, children)]), [[vue.vShow, m.expanded]])) : body]);
			}
			function blur(key) {
				blurTargets[key]?.focus();
			}
			function focusNode(key) {
				if (key !== void 0) {
					focusedKey.value = key;
					headerTargets[key]?.focus();
				}
			}
			function getFirstFocusableChild(children) {
				for (const child of children) {
					if (props.filter && child.matchesFilter !== true) continue;
					if (child.link === true) return child.key;
					if (child.expanded === true) {
						const key = getFirstFocusableChild(child.children);
						if (key !== void 0) return key;
					}
				}
			}
			function onNavigationKey(localMeta, keyCode) {
				const keys = focusableKeys.value, index = keys.indexOf(localMeta.key);
				if (keyCode === 36) {
					focusNode(keys[0]);
					return true;
				}
				if (keyCode === 35) {
					focusNode(keys.at(-1));
					return true;
				}
				if (keyCode === 38) {
					focusNode(keys[index - 1]);
					return true;
				}
				if (keyCode === 40) {
					focusNode(keys[index + 1]);
					return true;
				}
				if (keyCode === 39) {
					if (localMeta.isParent !== true && !localMeta.lazy) return true;
					if (localMeta.expanded !== true) setExpanded(localMeta.key, true);
					else focusNode(getFirstFocusableChild(localMeta.children));
					return true;
				}
				if (keyCode === 37) {
					if (localMeta.expanded === true) setExpanded(localMeta.key, false);
					else {
						let parent = localMeta.parent;
						while (parent !== null && parent.link !== true) parent = parent.parent;
						focusNode(parent?.key);
					}
					return true;
				}
				return false;
			}
			function onClick(node, localMeta, e, keyboard) {
				if (localMeta.link === true) focusedKey.value = localMeta.key;
				if (keyboard !== true && localMeta.selectable !== false) blur(localMeta.key);
				if (hasSelection.value && localMeta.selectable) {
					if (!props.noSelectionUnset) emit("update:selected", localMeta.key !== props.selected ? localMeta.key : null);
					else if (localMeta.key !== props.selected) emit("update:selected", localMeta.key === void 0 ? null : localMeta.key);
				} else onExpandClick(node, localMeta, e, keyboard);
				if (typeof node.handler === "function") node.handler(node);
			}
			function onExpandClick(node, localMeta, e, keyboard) {
				if (localMeta.link === true) focusedKey.value = localMeta.key;
				if (e !== void 0) stopAndPrevent(e);
				if (keyboard !== true && localMeta.selectable !== false) blur(localMeta.key);
				setExpanded(localMeta.key, !localMeta.expanded, node, localMeta);
			}
			function onTickedClick(localMeta, state) {
				if (localMeta.indeterminate === true) state = localMeta.indeterminateNextState;
				if (localMeta.strictTicking) setTicked([localMeta.key], state);
				else if (localMeta.leafTicking) {
					const keys = [];
					const travel = (nodeMeta) => {
						if (nodeMeta.isParent) {
							if (state !== true && nodeMeta.noTick !== true && nodeMeta.tickable === true) keys.push(nodeMeta.key);
							if (nodeMeta.leafTicking === true) nodeMeta.children.forEach(travel);
						} else if (nodeMeta.noTick !== true && nodeMeta.tickable === true && (nodeMeta.leafFilteredTicking !== true || nodeMeta.matchesFilter === true)) keys.push(nodeMeta.key);
					};
					travel(localMeta);
					setTicked(keys, state);
				}
			}
			if (props.defaultExpandAll) expandAll();
			Object.assign(proxy, {
				getNodeByKey,
				getTickedNodes,
				getExpandedNodes,
				isExpanded,
				collapseAll,
				expandAll,
				setExpanded,
				isTicked,
				setTicked
			});
			return () => {
				const children = getChildren(props.nodes);
				return (0, vue.h)("div", {
					class: classes.value,
					role: "tree"
				}, children.length === 0 ? props.filter ? props.noResultsLabel || $q.lang.tree.noResults : props.noNodesLabel || $q.lang.tree.noNodes : children);
			};
		}
	});
	//#endregion
	//#region src/components/uploader/uploader-core.js
	function getProgressLabel(p) {
		return (p * 100).toFixed(2) + "%";
	}
	const coreProps = {
		...useDarkProps,
		...useFileProps,
		label: String,
		color: String,
		textColor: String,
		square: Boolean,
		flat: Boolean,
		bordered: Boolean,
		noThumbnails: Boolean,
		thumbnailFit: {
			type: String,
			default: "cover"
		},
		autoUpload: Boolean,
		hideUploadBtn: Boolean,
		disable: Boolean,
		readonly: Boolean
	};
	const coreEmits = [
		...useFileEmits,
		"start",
		"finish",
		"added",
		"removed"
	];
	function getRenderer(getPlugin, expose) {
		const vm = (0, vue.getCurrentInstance)();
		const { props, slots, emit, proxy } = vm;
		const { $q } = proxy;
		const isDark = useDark(props, $q);
		function updateFileStatus(file, status, uploadedSize) {
			file.__status = status;
			if (status === "idle") {
				file.__uploaded = 0;
				file.__progress = 0;
				file.__sizeLabel = humanStorageSize(file.size);
				file.__progressLabel = "0.00%";
				return;
			}
			if (status === "failed") {
				proxy.$forceUpdate();
				return;
			}
			file.__uploaded = status === "uploaded" ? file.size : uploadedSize;
			file.__progress = status === "uploaded" ? 1 : file.size === 0 ? 0 : Math.min(.9999, file.__uploaded / file.size);
			file.__progressLabel = getProgressLabel(file.__progress);
			proxy.$forceUpdate();
		}
		const editable = (0, vue.computed)(() => !props.disable && !props.readonly);
		const dnd = (0, vue.ref)(false);
		const rootRef = (0, vue.ref)(null);
		const inputRef = (0, vue.ref)(null);
		const state = {
			files: (0, vue.ref)([]),
			queuedFiles: (0, vue.ref)([]),
			uploadedFiles: (0, vue.ref)([]),
			uploadedSize: (0, vue.ref)(0),
			updateFileStatus,
			isAlive: () => !vmIsDestroyed(vm)
		};
		const { pickFiles, addFiles, onDragover, onDragleave, processFiles, getDndNode, maxFilesNumber, maxTotalSizeNumber } = useFile({
			editable,
			dnd,
			getFileInput,
			addFilesToQueue
		});
		Object.assign(state, getPlugin({
			props,
			slots,
			emit,
			helpers: state,
			exposeApi: (obj) => {
				Object.assign(state, obj);
			}
		}));
		if (state.isBusy === void 0) state.isBusy = (0, vue.ref)(false);
		const uploadSize = (0, vue.ref)(0);
		const uploadProgress = (0, vue.computed)(() => uploadSize.value === 0 ? 0 : state.uploadedSize.value / uploadSize.value);
		const uploadProgressLabel = (0, vue.computed)(() => getProgressLabel(uploadProgress.value));
		const uploadSizeLabel = (0, vue.computed)(() => humanStorageSize(uploadSize.value));
		const canAddFiles = (0, vue.computed)(() => editable.value && !state.isUploading.value && (props.multiple || state.queuedFiles.value.length === 0) && (props.maxFiles === void 0 || state.files.value.length < maxFilesNumber.value) && (props.maxTotalSize === void 0 || uploadSize.value < maxTotalSizeNumber.value));
		const canUpload = (0, vue.computed)(() => editable.value && !state.isBusy.value && !state.isUploading.value && state.queuedFiles.value.length !== 0);
		(0, vue.provide)(uploaderKey, renderInput);
		const classes = (0, vue.computed)(() => "q-uploader column no-wrap" + (isDark.value ? " q-uploader--dark q-dark" : "") + (props.bordered ? " q-uploader--bordered" : "") + (props.square ? " q-uploader--square no-border-radius" : "") + (props.flat ? " q-uploader--flat no-shadow" : "") + (props.disable ? " disabled q-uploader--disable" : "") + (dnd.value ? " q-uploader--dnd" : ""));
		const colorClass = (0, vue.computed)(() => "q-uploader__header" + (props.color !== void 0 ? ` bg-${props.color}` : "") + (props.textColor !== void 0 ? ` text-${props.textColor}` : ""));
		(0, vue.watch)(state.isUploading, (newVal, oldVal) => {
			if (!oldVal && newVal) emit("start");
			else if (oldVal && !newVal) emit("finish");
		});
		function reset() {
			if (!props.disable) {
				state.abort();
				state.uploadedSize.value = 0;
				uploadSize.value = 0;
				revokeImgURLs();
				state.files.value = [];
				state.queuedFiles.value = [];
				state.uploadedFiles.value = [];
			}
		}
		function removeUploadedFiles() {
			if (!props.disable) batchRemoveFiles(["uploaded"], ({ size }) => {
				state.uploadedSize.value -= size;
				uploadSize.value -= size;
				state.uploadedFiles.value = [];
			});
		}
		function removeQueuedFiles() {
			batchRemoveFiles(["idle", "failed"], ({ size }) => {
				uploadSize.value -= size;
				state.queuedFiles.value = [];
			});
		}
		function batchRemoveFiles(statusList, cb) {
			if (props.disable) return;
			const removed = {
				files: [],
				size: 0
			};
			const localFiles = state.files.value.filter((f) => {
				if (!statusList.includes(f.__status)) return true;
				removed.size += f.size;
				removed.files.push(f);
				if (f.__img !== void 0) window.URL.revokeObjectURL(f.__img.src);
				return false;
			});
			if (removed.files.length !== 0) {
				state.files.value = localFiles;
				cb(removed);
				emit("removed", removed.files);
			}
		}
		function removeFile(file) {
			if (props.disable) return;
			const isUploading = file.__status === "uploading";
			if (file.__status === "uploaded") {
				state.uploadedSize.value -= file.size;
				uploadSize.value -= file.size;
				state.uploadedFiles.value = state.uploadedFiles.value.filter((f) => f.__key !== file.__key);
			} else if (isUploading) uploadSize.value -= file.size;
			else uploadSize.value -= file.size;
			state.files.value = state.files.value.filter((f) => {
				if (f.__key !== file.__key) return true;
				if (f.__img !== void 0) window.URL.revokeObjectURL(f.__img.src);
				return false;
			});
			state.queuedFiles.value = state.queuedFiles.value.filter((f) => f.__key !== file.__key);
			if (isUploading) file.__abort();
			emit("removed", [file]);
		}
		function revokeImgURLs() {
			state.files.value.forEach((f) => {
				if (f.__img !== void 0) window.URL.revokeObjectURL(f.__img.src);
			});
		}
		function getFileInput() {
			return inputRef.value || rootRef.value.getElementsByClassName("q-uploader__input")[0];
		}
		function addFilesToQueue(e, fileList) {
			const localFiles = processFiles(e, fileList, state.files.value, true);
			const fileInput = getFileInput();
			if (fileInput !== void 0 && fileInput !== null) fileInput.value = "";
			if (localFiles === void 0) return;
			localFiles.forEach((file) => {
				state.updateFileStatus(file, "idle");
				uploadSize.value += file.size;
				if (!props.noThumbnails && file.type.toUpperCase().startsWith("IMAGE")) {
					const img = new Image();
					img.src = window.URL.createObjectURL(file);
					file.__img = img;
				}
			});
			state.files.value.push(...localFiles);
			state.queuedFiles.value.push(...localFiles);
			emit("added", localFiles);
			if (props.autoUpload) state.upload();
		}
		function upload() {
			if (canUpload.value) state.upload();
		}
		function getBtn(show, icon, fn) {
			if (show) {
				const data = {
					type: "a",
					key: icon,
					icon: $q.iconSet.uploader[icon],
					flat: true,
					dense: true
				};
				let child = void 0;
				if (icon === "add") {
					data.onClick = pickFiles;
					child = renderInput;
				} else data.onClick = fn;
				return (0, vue.h)(QBtn_default, data, child);
			}
		}
		function renderInput() {
			return (0, vue.h)("input", {
				ref: inputRef,
				class: "q-uploader__input overflow-hidden absolute-full",
				tabindex: -1,
				type: "file",
				title: "",
				accept: props.accept,
				multiple: props.multiple ? "multiple" : void 0,
				capture: props.capture,
				onMousedown: stop,
				onClick: pickFiles,
				onChange: addFilesToQueue
			});
		}
		function getHeader() {
			if (slots.header !== void 0) return slots.header(publicApi);
			return [(0, vue.h)("div", { class: "q-uploader__header-content column" }, [(0, vue.h)("div", { class: "flex flex-center no-wrap q-gutter-xs" }, [
				getBtn(state.queuedFiles.value.length !== 0, "removeQueue", removeQueuedFiles),
				getBtn(state.uploadedFiles.value.length !== 0, "removeUploaded", removeUploadedFiles),
				state.isUploading.value ? (0, vue.h)(QSpinner_default, { class: "q-uploader__spinner" }) : null,
				(0, vue.h)("div", { class: "col column justify-center" }, [props.label !== void 0 ? (0, vue.h)("div", { class: "q-uploader__title" }, [props.label]) : null, (0, vue.h)("div", { class: "q-uploader__subtitle" }, [uploadSizeLabel.value + " / " + uploadProgressLabel.value])]),
				getBtn(canAddFiles.value, "add"),
				getBtn(!props.hideUploadBtn && canUpload.value, "upload", state.upload),
				getBtn(state.isUploading.value, "clear", state.abort)
			])])];
		}
		function getList() {
			if (slots.list !== void 0) return slots.list(publicApi);
			return state.files.value.map((file) => (0, vue.h)("div", {
				key: file.__key,
				class: "q-uploader__file relative-position" + (!props.noThumbnails && file.__img !== void 0 ? " q-uploader__file--img" : "") + (file.__status === "failed" ? " q-uploader__file--failed" : file.__status === "uploaded" ? " q-uploader__file--uploaded" : ""),
				style: !props.noThumbnails && file.__img !== void 0 ? {
					backgroundImage: "url(\"" + file.__img.src + "\")",
					backgroundSize: props.thumbnailFit
				} : null
			}, [(0, vue.h)("div", { class: "q-uploader__file-header row flex-center no-wrap" }, [
				file.__status === "failed" ? (0, vue.h)(QIcon_default, {
					class: "q-uploader__file-status",
					name: $q.iconSet.type.negative,
					color: "negative"
				}) : null,
				(0, vue.h)("div", { class: "q-uploader__file-header-content col" }, [(0, vue.h)("div", { class: "q-uploader__title" }, [file.name]), (0, vue.h)("div", { class: "q-uploader__subtitle row items-center no-wrap" }, [file.__sizeLabel + " / " + file.__progressLabel])]),
				file.__status === "uploading" ? (0, vue.h)(QCircularProgress_default, {
					value: file.__progress,
					min: 0,
					max: 1,
					indeterminate: file.__progress === 0
				}) : (0, vue.h)(QBtn_default, {
					round: true,
					dense: true,
					flat: true,
					icon: $q.iconSet.uploader[file.__status === "uploaded" ? "done" : "clear"],
					onClick: () => {
						removeFile(file);
					}
				})
			])]));
		}
		(0, vue.onBeforeUnmount)(() => {
			if (state.isUploading.value) state.abort();
			if (state.files.value.length !== 0) revokeImgURLs();
		});
		const publicApi = {};
		for (const key in state) if ((0, vue.isRef)(state[key])) injectProp(publicApi, key, () => state[key].value);
		else publicApi[key] = state[key];
		Object.assign(publicApi, {
			upload,
			reset,
			removeUploadedFiles,
			removeQueuedFiles,
			removeFile,
			pickFiles,
			addFiles
		});
		injectMultipleProps(publicApi, {
			canAddFiles: () => canAddFiles.value,
			canUpload: () => canUpload.value,
			uploadSizeLabel: () => uploadSizeLabel.value,
			uploadProgressLabel: () => uploadProgressLabel.value
		});
		expose({
			...state,
			upload,
			reset,
			removeUploadedFiles,
			removeQueuedFiles,
			removeFile,
			pickFiles,
			addFiles,
			canAddFiles,
			canUpload,
			uploadSizeLabel,
			uploadProgressLabel
		});
		return () => {
			const children = [
				(0, vue.h)("div", { class: colorClass.value }, getHeader()),
				(0, vue.h)("div", { class: "q-uploader__list scroll" }, getList()),
				getDndNode("uploader")
			];
			if (state.isBusy.value) children.push((0, vue.h)("div", { class: "q-uploader__overlay absolute-full flex flex-center" }, [(0, vue.h)(QSpinner_default)]));
			const data = {
				ref: rootRef,
				class: classes.value
			};
			if (canAddFiles.value) Object.assign(data, {
				onDragover,
				onDragleave
			});
			return (0, vue.h)("div", data, children);
		};
	}
	//#endregion
	//#region src/utils/private.get-emits-object/get-emits-object.js
	const trueFn = () => true;
	function getEmitsObject(emitsArray) {
		const emitsObject = {};
		emitsArray.forEach((val) => {
			emitsObject[val] = trueFn;
		});
		return emitsObject;
	}
	//#endregion
	//#region src/utils/create-uploader-component/create-uploader-component.js
	const coreEmitsObject = getEmitsObject(coreEmits);
	function createUploaderComponent({ name, props, emits, injectPlugin }) {
		return createComponent({
			name,
			props: {
				...coreProps,
				...props
			},
			emits: isObject(emits) ? {
				...coreEmitsObject,
				...emits
			} : [...coreEmits, ...emits],
			setup(_, { expose }) {
				return getRenderer(injectPlugin, expose);
			}
		});
	}
	//#endregion
	//#region src/components/uploader/xhr-uploader-plugin.js
	function getFn(prop) {
		return typeof prop === "function" ? prop : () => prop;
	}
	const name = "QUploader";
	const componentProps = {
		url: [Function, String],
		method: {
			type: [Function, String],
			default: "POST"
		},
		fieldName: {
			type: [Function, String],
			default: () => (file) => file.name
		},
		headers: [Function, Array],
		formFields: [Function, Array],
		withCredentials: [Function, Boolean],
		sendRaw: [Function, Boolean],
		batch: [Function, Boolean],
		factory: Function
	};
	const emits$1 = [
		"factoryFailed",
		"uploaded",
		"failed",
		"uploading"
	];
	function injectPlugin({ props, emit, helpers }) {
		const xhrs = (0, vue.ref)([]);
		const promises = (0, vue.ref)([]);
		const workingThreads = (0, vue.ref)(0);
		const abortedPromises = /* @__PURE__ */ new WeakSet();
		const xhrProps = (0, vue.computed)(() => ({
			url: getFn(props.url),
			method: getFn(props.method),
			headers: getFn(props.headers),
			formFields: getFn(props.formFields),
			fieldName: getFn(props.fieldName),
			withCredentials: getFn(props.withCredentials),
			sendRaw: getFn(props.sendRaw),
			batch: getFn(props.batch)
		}));
		const isUploading = (0, vue.computed)(() => workingThreads.value > 0);
		const isBusy = (0, vue.computed)(() => promises.value.length !== 0);
		const getLiveFiles = (files) => files.filter((file) => helpers.files.value.includes(file));
		function abort() {
			xhrs.value.forEach((x) => {
				x.abort();
			});
			promises.value.forEach((promise) => {
				abortedPromises.add(promise);
			});
		}
		function upload() {
			const queue = [...helpers.queuedFiles.value];
			helpers.queuedFiles.value = [];
			if (xhrProps.value.batch(queue)) runFactory(queue);
			else queue.forEach((file) => {
				runFactory([file]);
			});
		}
		function runFactory(files) {
			workingThreads.value++;
			const failed = (err, promise) => {
				if (helpers.isAlive()) {
					if (promise !== void 0) promises.value = promises.value.filter((p) => p !== promise);
					const liveFiles = getLiveFiles(files);
					if (liveFiles.length !== 0) {
						helpers.queuedFiles.value.push(...liveFiles);
						liveFiles.forEach((f) => {
							helpers.updateFileStatus(f, "failed");
						});
						emit("factoryFailed", err, liveFiles);
					}
					workingThreads.value--;
				}
			};
			if (typeof props.factory !== "function") {
				startUpload({});
				return;
			}
			let res;
			try {
				res = props.factory(files);
			} catch (err) {
				failed(err);
				return;
			}
			if (Object(res) !== res) failed(/* @__PURE__ */ new Error("QUploader: factory() does not return properly"));
			else if (typeof res.catch === "function" && typeof res.then === "function") {
				promises.value.push(res);
				res.then((factory) => {
					if (abortedPromises.has(res)) failed(/* @__PURE__ */ new Error("Aborted"), res);
					else if (Object(factory) !== factory) failed(/* @__PURE__ */ new Error("QUploader: factory() does not return properly"), res);
					else if (helpers.isAlive()) {
						promises.value = promises.value.filter((p) => p !== res);
						startUpload(factory);
					}
				}).catch((err) => {
					failed(err, res);
				});
			} else startUpload(res);
			function startUpload(factory) {
				const liveFiles = getLiveFiles(files);
				if (liveFiles.length === 0) {
					workingThreads.value--;
					return;
				}
				try {
					performUpload(liveFiles, factory);
				} catch (err) {
					failed(err);
				}
			}
		}
		function performUpload(files, factory) {
			const form = new FormData(), xhr = new XMLHttpRequest();
			const getProp = (propName, arg) => factory[propName] !== void 0 ? getFn(factory[propName])(arg) : xhrProps.value[propName](arg);
			const url = getProp("url", files);
			if (!url) {
				console.error("q-uploader: invalid or no URL specified");
				helpers.queuedFiles.value.push(...files);
				files.forEach((f) => {
					helpers.updateFileStatus(f, "failed");
				});
				workingThreads.value--;
				return;
			}
			const fields = getProp("formFields", files);
			if (fields !== void 0) fields.forEach((field) => {
				form.append(field.name, field.value);
			});
			let uploadIndex = 0, uploadIndexSize = 0, localUploadedSize = 0, maxUploadSize = 0, aborted;
			xhr.upload.addEventListener("progress", (e) => {
				if (aborted) return;
				const loaded = Math.min(maxUploadSize, e.loaded);
				helpers.uploadedSize.value += loaded - localUploadedSize;
				localUploadedSize = loaded;
				let size = localUploadedSize - uploadIndexSize;
				for (let i = uploadIndex; size > 0 && i < files.length; i++) {
					const file = files[i];
					if (size >= file.size) {
						size -= file.size;
						uploadIndex++;
						uploadIndexSize += file.size;
						helpers.updateFileStatus(file, "uploading", file.size);
					} else {
						helpers.updateFileStatus(file, "uploading", size);
						return;
					}
				}
			}, false);
			xhr.addEventListener("readystatechange", () => {
				if (xhr.readyState < 4) return;
				if (xhr.status && xhr.status < 400) {
					const liveFiles = getLiveFiles(files);
					const liveUploadSize = liveFiles.reduce((total, file) => total + file.size, 0);
					helpers.uploadedSize.value += liveUploadSize - localUploadedSize;
					if (liveFiles.length !== 0) {
						helpers.uploadedFiles.value.push(...liveFiles);
						liveFiles.forEach((f) => {
							helpers.updateFileStatus(f, "uploaded");
						});
						emit("uploaded", {
							files: liveFiles,
							xhr
						});
					}
				} else {
					aborted = true;
					helpers.uploadedSize.value -= localUploadedSize;
					const liveFiles = getLiveFiles(files);
					if (liveFiles.length !== 0) {
						helpers.queuedFiles.value.push(...liveFiles);
						liveFiles.forEach((f) => {
							helpers.updateFileStatus(f, "failed");
						});
						emit("failed", {
							files: liveFiles,
							xhr
						});
					}
				}
				workingThreads.value--;
				xhrs.value = xhrs.value.filter((x) => x !== xhr);
			});
			xhr.open(getProp("method", files), url);
			if (getProp("withCredentials", files) === true) xhr.withCredentials = true;
			const headers = getProp("headers", files);
			if (headers !== void 0) headers.forEach((head) => {
				xhr.setRequestHeader(head.name, head.value);
			});
			const sendRaw = getProp("sendRaw", files);
			files.forEach((file) => {
				helpers.updateFileStatus(file, "uploading", 0);
				if (sendRaw !== true) form.append(getProp("fieldName", file), file, file.name);
				file.xhr = xhr;
				file.__abort = () => {
					xhr.abort();
				};
				maxUploadSize += file.size;
			});
			emit("uploading", {
				files,
				xhr
			});
			xhrs.value.push(xhr);
			if (sendRaw === true) xhr.send(new Blob(files));
			else xhr.send(form);
		}
		return {
			isUploading,
			isBusy,
			abort,
			upload
		};
	}
	//#endregion
	//#region src/components/uploader/QUploader.js
	var QUploader_default = createUploaderComponent({
		name,
		props: componentProps,
		emits: emits$1,
		injectPlugin
	});
	//#endregion
	//#region src/components/uploader/QUploaderAddTrigger.js
	var QUploaderAddTrigger_default = createComponent({
		name: "QUploaderAddTrigger",
		setup() {
			const $trigger = (0, vue.inject)(uploaderKey, emptyRenderFn);
			if ($trigger === emptyRenderFn) console.error("QUploaderAddTrigger needs to be child of QUploader");
			return $trigger;
		}
	});
	//#endregion
	//#region src/components/video/QVideo.js
	var QVideo_default = createComponent({
		name: "QVideo",
		props: {
			...useRatioProps,
			src: {
				type: String,
				required: true
			},
			title: String,
			fetchpriority: {
				type: String,
				default: "auto"
			},
			loading: {
				type: String,
				default: "eager"
			},
			referrerpolicy: {
				type: String,
				default: "strict-origin-when-cross-origin"
			}
		},
		setup(props) {
			const ratioStyle = useRatio(props);
			const classes = (0, vue.computed)(() => "q-video" + (props.ratio !== void 0 ? " q-video--responsive" : ""));
			return () => (0, vue.h)("div", {
				class: classes.value,
				style: ratioStyle.value
			}, [(0, vue.h)("iframe", {
				src: props.src,
				title: props.title,
				fetchpriority: props.fetchpriority,
				loading: props.loading,
				referrerpolicy: props.referrerpolicy,
				frameborder: "0",
				allowfullscreen: true
			})]);
		}
	});
	//#endregion
	//#region src/components.js
	var components_exports = /* @__PURE__ */ __exportAll({
		QAjaxBar: () => QAjaxBar_default,
		QAvatar: () => QAvatar_default,
		QBadge: () => QBadge_default,
		QBanner: () => QBanner_default,
		QBar: () => QBar_default,
		QBreadcrumbs: () => QBreadcrumbs_default,
		QBreadcrumbsEl: () => QBreadcrumbsEl_default,
		QBtn: () => QBtn_default,
		QBtnDropdown: () => QBtnDropdown_default,
		QBtnGroup: () => QBtnGroup_default,
		QBtnToggle: () => QBtnToggle_default,
		QCard: () => QCard_default,
		QCardActions: () => QCardActions_default,
		QCardSection: () => QCardSection_default,
		QCarousel: () => QCarousel_default,
		QCarouselControl: () => QCarouselControl_default,
		QCarouselSlide: () => QCarouselSlide_default,
		QChatMessage: () => QChatMessage_default,
		QCheckbox: () => QCheckbox_default,
		QChip: () => QChip_default,
		QCircularProgress: () => QCircularProgress_default,
		QColor: () => QColor_default,
		QDate: () => QDate_default,
		QDialog: () => QDialog_default,
		QDrawer: () => QDrawer_default,
		QEditor: () => QEditor_default,
		QExpansionItem: () => QExpansionItem_default,
		QFab: () => QFab_default,
		QFabAction: () => QFabAction_default,
		QField: () => QField_default,
		QFile: () => QFile_default,
		QFooter: () => QFooter_default,
		QForm: () => QForm_default,
		QFormChildMixin: () => QFormChildMixin_default,
		QHeader: () => QHeader_default,
		QIcon: () => QIcon_default,
		QImg: () => QImg_default,
		QInfiniteScroll: () => QInfiniteScroll_default,
		QInnerLoading: () => QInnerLoading_default,
		QInput: () => QInput_default,
		QIntersection: () => QIntersection_default,
		QItem: () => QItem_default,
		QItemLabel: () => QItemLabel_default,
		QItemSection: () => QItemSection_default,
		QKnob: () => QKnob_default,
		QLayout: () => QLayout_default,
		QLinearProgress: () => QLinearProgress_default,
		QList: () => QList_default,
		QMarkupTable: () => QMarkupTable_default,
		QMenu: () => QMenu_default,
		QNoSsr: () => QNoSsr_default,
		QOptionGroup: () => QOptionGroup_default,
		QPage: () => QPage_default,
		QPageContainer: () => QPageContainer_default,
		QPageScroller: () => QPageScroller_default,
		QPageSticky: () => QPageSticky_default,
		QPagination: () => QPagination_default,
		QParallax: () => QParallax_default,
		QPopupEdit: () => QPopupEdit_default,
		QPopupProxy: () => QPopupProxy_default,
		QPullToRefresh: () => QPullToRefresh_default,
		QRadio: () => QRadio_default,
		QRange: () => QRange_default,
		QRating: () => QRating_default,
		QResizeObserver: () => QResizeObserver_default,
		QResponsive: () => QResponsive_default,
		QRouteTab: () => QRouteTab_default,
		QScrollArea: () => QScrollArea_default,
		QScrollObserver: () => QScrollObserver_default,
		QSelect: () => QSelect_default,
		QSeparator: () => QSeparator_default,
		QSkeleton: () => QSkeleton_default,
		QSlideItem: () => QSlideItem_default,
		QSlideTransition: () => QSlideTransition_default,
		QSlider: () => QSlider_default,
		QSpace: () => QSpace_default,
		QSpinner: () => QSpinner_default,
		QSpinnerAudio: () => QSpinnerAudio_default,
		QSpinnerBall: () => QSpinnerBall_default,
		QSpinnerBars: () => QSpinnerBars_default,
		QSpinnerBox: () => QSpinnerBox_default,
		QSpinnerClock: () => QSpinnerClock_default,
		QSpinnerComment: () => QSpinnerComment_default,
		QSpinnerCube: () => QSpinnerCube_default,
		QSpinnerDots: () => QSpinnerDots_default,
		QSpinnerFacebook: () => QSpinnerFacebook_default,
		QSpinnerGears: () => QSpinnerGears_default,
		QSpinnerGrid: () => QSpinnerGrid_default,
		QSpinnerHearts: () => QSpinnerHearts_default,
		QSpinnerHourglass: () => QSpinnerHourglass_default,
		QSpinnerInfinity: () => QSpinnerInfinity_default,
		QSpinnerIos: () => QSpinnerIos_default,
		QSpinnerOrbit: () => QSpinnerOrbit_default,
		QSpinnerOval: () => QSpinnerOval_default,
		QSpinnerPie: () => QSpinnerPie_default,
		QSpinnerPuff: () => QSpinnerPuff_default,
		QSpinnerRadio: () => QSpinnerRadio_default,
		QSpinnerRings: () => QSpinnerRings_default,
		QSpinnerTail: () => QSpinnerTail_default,
		QSplitter: () => QSplitter_default,
		QStep: () => QStep_default,
		QStepper: () => QStepper_default,
		QStepperNavigation: () => QStepperNavigation_default,
		QTab: () => QTab_default,
		QTabPanel: () => QTabPanel_default,
		QTabPanels: () => QTabPanels_default,
		QTable: () => QTable_default,
		QTabs: () => QTabs_default,
		QTd: () => QTd_default,
		QTh: () => QTh_default,
		QTime: () => QTime_default,
		QTimeline: () => QTimeline_default,
		QTimelineEntry: () => QTimelineEntry_default,
		QToggle: () => QToggle_default,
		QToolbar: () => QToolbar_default,
		QToolbarTitle: () => QToolbarTitle_default,
		QTooltip: () => QTooltip_default,
		QTr: () => QTr_default,
		QTree: () => QTree_default,
		QUploader: () => QUploader_default,
		QUploaderAddTrigger: () => QUploaderAddTrigger_default,
		QVideo: () => QVideo_default,
		QVirtualScroll: () => QVirtualScroll_default
	});
	//#endregion
	//#region src/directives/close-popup/ClosePopup.js
	function getDepth(value) {
		if (value === false) return 0;
		if (value === true || value === void 0) return 1;
		return Number.parseInt(value, 10) || 0;
	}
	var ClosePopup_default = createDirective({
		name: "close-popup",
		beforeMount(el, { value }) {
			const ctx = {
				depth: getDepth(value),
				handler(evt) {
					if (ctx.depth !== 0) setTimeout(() => {
						const proxy = getPortalProxy(el);
						if (proxy !== void 0) closePortals(proxy, evt, ctx.depth);
					}, 0);
				},
				handlerKey(evt) {
					if (isKeyCode(evt, 13)) ctx.handler(evt);
				}
			};
			el.__qclosepopup = ctx;
			el.addEventListener("click", ctx.handler);
			el.addEventListener("keyup", ctx.handlerKey);
		},
		updated(el, { value, oldValue }) {
			if (value !== oldValue) el.__qclosepopup.depth = getDepth(value);
		},
		beforeUnmount(el) {
			const ctx = el.__qclosepopup;
			el.removeEventListener("click", ctx.handler);
			el.removeEventListener("keyup", ctx.handlerKey);
			delete el.__qclosepopup;
		}
	});
	//#endregion
	//#region src/utils/morph/morph.js
	let id = 0;
	let offsetBase = void 0;
	function defaultCancel() {
		return false;
	}
	function getAbsolutePosition(el, resize) {
		if (offsetBase === void 0) {
			offsetBase = document.createElement("div");
			offsetBase.style.cssText = "position: absolute; left: 0; top: 0";
			document.body.append(offsetBase);
		}
		const boundingRect = el.getBoundingClientRect();
		const baseRect = offsetBase.getBoundingClientRect();
		const { marginLeft, marginRight, marginTop, marginBottom } = window.getComputedStyle(el);
		const marginH = Number.parseInt(marginLeft, 10) + Number.parseInt(marginRight, 10);
		const marginV = Number.parseInt(marginTop, 10) + Number.parseInt(marginBottom, 10);
		return {
			left: boundingRect.left - baseRect.left,
			top: boundingRect.top - baseRect.top,
			width: boundingRect.right - boundingRect.left,
			height: boundingRect.bottom - boundingRect.top,
			widthM: boundingRect.right - boundingRect.left + (resize ? 0 : marginH),
			heightM: boundingRect.bottom - boundingRect.top + (resize ? 0 : marginV),
			marginH: resize ? marginH : 0,
			marginV: resize ? marginV : 0
		};
	}
	function getAbsoluteSize(el) {
		return {
			width: el.scrollWidth,
			height: el.scrollHeight
		};
	}
	const styleEdges = [
		"Top",
		"Right",
		"Bottom",
		"Left"
	];
	const styleBorderRadiuses = [
		"borderTopLeftRadius",
		"borderTopRightRadius",
		"borderBottomRightRadius",
		"borderBottomLeftRadius"
	];
	const reStyleSkipKey = /-block|-inline|block-|inline-/;
	const reStyleSkipRule = /(-block|-inline|block-|inline-).*:/;
	function getComputedStyle$1(el, props) {
		const style = window.getComputedStyle(el);
		const fixed = {};
		for (let i = 0; i < props.length; i++) {
			const prop = props[i];
			if (style[prop] === "") if (prop === "cssText") {
				const styleLen = style.length;
				let val = "";
				for (let styleIndex = 0; styleIndex < styleLen; styleIndex++) if (!reStyleSkipKey.test(style[styleIndex])) val += style[styleIndex] + ": " + style[style[styleIndex]] + "; ";
				fixed[prop] = val;
			} else if ([
				"borderWidth",
				"borderStyle",
				"borderColor"
			].includes(prop)) {
				const suffix = prop.replace("border", "");
				let val = "";
				for (let j = 0; j < styleEdges.length; j++) {
					const subProp = "border" + styleEdges[j] + suffix;
					val += style[subProp] + " ";
				}
				fixed[prop] = val;
			} else if (prop === "borderRadius") {
				let val1 = "";
				let val2 = "";
				for (let j = 0; j < styleBorderRadiuses.length; j++) {
					const val = style[styleBorderRadiuses[j]].split(" ");
					val1 += val[0] + " ";
					val2 += (val[1] === void 0 ? val[0] : val[1]) + " ";
				}
				fixed[prop] = val1 + "/ " + val2;
			} else fixed[prop] = style[prop];
			else if (prop === "cssText") fixed[prop] = style[prop].split(";").filter((val) => !reStyleSkipRule.test(val)).join(";");
			else fixed[prop] = style[prop];
		}
		return fixed;
	}
	const zIndexPositions = [
		"absolute",
		"fixed",
		"relative",
		"sticky"
	];
	function getMaxZIndex(elStart) {
		let el = elStart;
		let maxIndex = 0;
		while (el !== null && el !== document) {
			const { position, zIndex } = window.getComputedStyle(el);
			const zIndexNum = Number(zIndex);
			if (zIndexNum > maxIndex && (el === elStart || zIndexPositions.includes(position))) maxIndex = zIndexNum;
			el = el.parentNode;
		}
		return maxIndex;
	}
	function normalizeElements(opts) {
		return {
			from: opts.from,
			to: opts.to !== void 0 ? opts.to : opts.from
		};
	}
	function getOpacity(value, fallback) {
		const parsed = Number.parseFloat(value);
		return Number.isFinite(parsed) ? Math.max(0, Math.min(1, parsed)) : fallback;
	}
	function normalizeOptions(options) {
		if (typeof options === "number") options = { duration: options };
		else if (typeof options === "function") options = { onEnd: options };
		const parsedDuration = Number.parseInt(options.duration, 10);
		const parsedDelay = Number.parseInt(options.delay, 10);
		return {
			...options,
			waitFor: options.waitFor === void 0 ? 0 : options.waitFor,
			duration: Number.isNaN(parsedDuration) ? 300 : parsedDuration,
			delay: Number.isNaN(parsedDelay) ? 0 : parsedDelay,
			easing: typeof options.easing === "string" && options.easing.length !== 0 ? options.easing : "ease-in-out",
			fill: typeof options.fill === "string" && options.fill.length !== 0 ? options.fill : "none",
			resize: options.resize === true,
			useCSS: options.useCSS === true || options.usecss === true,
			hideFromClone: options.hideFromClone === true || options.hidefromclone === true,
			keepToClone: options.keepToClone === true || options.keeptoclone === true,
			tween: options.tween === true,
			tweenFromOpacity: getOpacity(options.tweenFromOpacity, .6),
			tweenToOpacity: getOpacity(options.tweenToOpacity, .5)
		};
	}
	function getElement(element) {
		const type = typeof element;
		return type === "function" ? element() : type === "string" ? document.querySelector(element) : element;
	}
	function isValidElement(element) {
		return element && element.ownerDocument === document && element.parentNode !== null;
	}
	function morph(_options) {
		let cancel = defaultCancel;
		let cancelStatus = false;
		let endElementTo = true;
		const elements = normalizeElements(_options);
		const options = normalizeOptions(_options);
		const elFrom = getElement(elements.from);
		if (!isValidElement(elFrom)) return cancel;
		if (typeof elFrom.qMorphCancel === "function") elFrom.qMorphCancel();
		let animationFromClone = void 0;
		let animationFromTween = void 0;
		let animationToClone = void 0;
		let animationTo = void 0;
		const elFromParent = elFrom.parentNode;
		const elFromNext = elFrom.nextElementSibling;
		const elFromPosition = getAbsolutePosition(elFrom, options.resize);
		const { width: elFromParentWidthBefore, height: elFromParentHeightBefore } = getAbsoluteSize(elFromParent);
		const { borderWidth: elFromBorderWidth, borderStyle: elFromBorderStyle, borderColor: elFromBorderColor, borderRadius: elFromBorderRadius, backgroundColor: elFromBackground, transform: elFromTransform, position: elFromPositioningType, cssText: elFromCssText } = getComputedStyle$1(elFrom, [
			"borderWidth",
			"borderStyle",
			"borderColor",
			"borderRadius",
			"backgroundColor",
			"transform",
			"position",
			"cssText"
		]);
		const elFromClassSaved = elFrom.classList.toString();
		const elFromStyleSaved = elFrom.style.cssText;
		const elFromClone = elFrom.cloneNode(true);
		const elFromTween = options.tween === true ? elFrom.cloneNode(true) : void 0;
		if (elFromTween !== void 0) elFromTween.className = elFromTween.classList.toString().split(" ").filter((c) => !c.startsWith("bg-")).join(" ");
		if (options.hideFromClone === true) elFromClone.classList.add("q-morph--internal");
		elFromClone.setAttribute("aria-hidden", "true");
		elFromClone.style.transition = "none";
		elFromClone.style.animation = "none";
		elFromClone.style.pointerEvents = "none";
		elFromParent.insertBefore(elFromClone, elFromNext);
		elFrom.qMorphCancel = () => {
			cancelStatus = true;
			elFromClone.remove();
			elFromTween?.remove();
			if (options.hideFromClone === true) elFromClone.classList.remove("q-morph--internal");
			elFrom.qMorphCancel = void 0;
		};
		const calculateFinalState = () => {
			const elTo = getElement(elements.to);
			if (cancelStatus === true || !isValidElement(elTo)) {
				if (typeof elFrom.qMorphCancel === "function") elFrom.qMorphCancel();
				return;
			}
			if (elFrom !== elTo && typeof elTo.qMorphCancel === "function") elTo.qMorphCancel();
			if (options.keepToClone !== true) elTo.classList.add("q-morph--internal");
			elFromClone.classList.add("q-morph--internal");
			const { width: elFromParentWidthAfter, height: elFromParentHeightAfter } = getAbsoluteSize(elFromParent);
			const { width: elToParentWidthBefore, height: elToParentHeightBefore } = getAbsoluteSize(elTo.parentNode);
			if (options.hideFromClone !== true) elFromClone.classList.remove("q-morph--internal");
			elTo.qMorphCancel = () => {
				cancelStatus = true;
				elFromClone.remove();
				elFromTween?.remove();
				if (options.hideFromClone === true) elFromClone.classList.remove("q-morph--internal");
				if (options.keepToClone !== true) elTo.classList.remove("q-morph--internal");
				elFrom.qMorphCancel = void 0;
				elTo.qMorphCancel = void 0;
			};
			const animate = () => {
				if (cancelStatus === true) {
					if (typeof elTo.qMorphCancel === "function") elTo.qMorphCancel();
					return;
				}
				if (options.hideFromClone !== true) {
					elFromClone.classList.add("q-morph--internal");
					elFromClone.innerHTML = "";
					elFromClone.style.left = 0;
					elFromClone.style.right = "unset";
					elFromClone.style.top = 0;
					elFromClone.style.bottom = "unset";
					elFromClone.style.transform = "none";
				}
				if (options.keepToClone !== true) elTo.classList.remove("q-morph--internal");
				const elToParent = elTo.parentNode;
				const { width: elToParentWidthAfter, height: elToParentHeightAfter } = getAbsoluteSize(elToParent);
				const elToClone = elTo.cloneNode(options.keepToClone);
				elToClone.setAttribute("aria-hidden", "true");
				if (options.keepToClone !== true) {
					elToClone.style.left = 0;
					elToClone.style.right = "unset";
					elToClone.style.top = 0;
					elToClone.style.bottom = "unset";
					elToClone.style.transform = "none";
					elToClone.style.pointerEvents = "none";
				}
				elToClone.classList.add("q-morph--internal");
				const elToNext = elTo === elFrom && elFromParent === elToParent ? elFromClone : elTo.nextElementSibling;
				elToParent.insertBefore(elToClone, elToNext);
				const { borderWidth: elToBorderWidth, borderStyle: elToBorderStyle, borderColor: elToBorderColor, borderRadius: elToBorderRadius, backgroundColor: elToBackground, transform: elToTransform, position: elToPositioningType, cssText: elToCssText } = getComputedStyle$1(elTo, [
					"borderWidth",
					"borderStyle",
					"borderColor",
					"borderRadius",
					"backgroundColor",
					"transform",
					"position",
					"cssText"
				]);
				const elToClassSaved = elTo.classList.toString();
				const elToStyleSaved = elTo.style.cssText;
				elTo.style.cssText = elToCssText;
				elTo.style.transform = "none";
				elTo.style.animation = "none";
				elTo.style.transition = "none";
				elTo.className = elToClassSaved.split(" ").filter((c) => !c.startsWith("bg-")).join(" ");
				const elToPosition = getAbsolutePosition(elTo, options.resize);
				const deltaX = elFromPosition.left - elToPosition.left;
				const deltaY = elFromPosition.top - elToPosition.top;
				const scaleX = elFromPosition.width / (elToPosition.width > 0 ? elToPosition.width : 10);
				const scaleY = elFromPosition.height / (elToPosition.height > 0 ? elToPosition.height : 100);
				const elFromParentWidthDiff = elFromParentWidthBefore - elFromParentWidthAfter;
				const elFromParentHeightDiff = elFromParentHeightBefore - elFromParentHeightAfter;
				const elToParentWidthDiff = elToParentWidthAfter - elToParentWidthBefore;
				const elToParentHeightDiff = elToParentHeightAfter - elToParentHeightBefore;
				const elFromCloneWidth = Math.max(elFromPosition.widthM, elFromParentWidthDiff);
				const elFromCloneHeight = Math.max(elFromPosition.heightM, elFromParentHeightDiff);
				const elToCloneWidth = Math.max(elToPosition.widthM, elToParentWidthDiff);
				const elToCloneHeight = Math.max(elToPosition.heightM, elToParentHeightDiff);
				const elSharedSize = elFrom === elTo && !["absolute", "fixed"].includes(elToPositioningType) && !["absolute", "fixed"].includes(elFromPositioningType);
				let elToNeedsFixedPosition = elToPositioningType === "fixed";
				let parent = elToParent;
				while (!elToNeedsFixedPosition && parent !== document) {
					elToNeedsFixedPosition = window.getComputedStyle(parent).position === "fixed";
					parent = parent.parentNode;
				}
				if (options.hideFromClone !== true) {
					elFromClone.style.display = "block";
					elFromClone.style.flex = "0 0 auto";
					elFromClone.style.opacity = 0;
					elFromClone.style.minWidth = "unset";
					elFromClone.style.maxWidth = "unset";
					elFromClone.style.minHeight = "unset";
					elFromClone.style.maxHeight = "unset";
					elFromClone.classList.remove("q-morph--internal");
				}
				if (options.keepToClone !== true) {
					elToClone.style.display = "block";
					elToClone.style.flex = "0 0 auto";
					elToClone.style.opacity = 0;
					elToClone.style.minWidth = "unset";
					elToClone.style.maxWidth = "unset";
					elToClone.style.minHeight = "unset";
					elToClone.style.maxHeight = "unset";
				}
				elToClone.classList.remove("q-morph--internal");
				if (typeof options.classes === "string") elTo.className += " " + options.classes;
				if (typeof options.style === "string") elTo.style.cssText += " " + options.style;
				else if (isObject(options.style)) for (const prop in options.style) elTo.style[prop] = options.style[prop];
				const elFromZIndex = getMaxZIndex(elFromClone);
				const elToZIndex = getMaxZIndex(elTo);
				const documentScroll = elToNeedsFixedPosition ? document.documentElement : {
					scrollLeft: 0,
					scrollTop: 0
				};
				elTo.style.position = elToNeedsFixedPosition ? "fixed" : "absolute";
				elTo.style.left = `${elToPosition.left - documentScroll.scrollLeft}px`;
				elTo.style.right = "unset";
				elTo.style.top = `${elToPosition.top - documentScroll.scrollTop}px`;
				elTo.style.margin = 0;
				if (options.resize === true) {
					elTo.style.minWidth = "unset";
					elTo.style.maxWidth = "unset";
					elTo.style.minHeight = "unset";
					elTo.style.maxHeight = "unset";
					elTo.style.overflow = "hidden";
					elTo.style.overflowX = "hidden";
					elTo.style.overflowY = "hidden";
				}
				document.body.append(elTo);
				if (elFromTween !== void 0) {
					elFromTween.style.cssText = elFromCssText;
					elFromTween.style.transform = "none";
					elFromTween.style.animation = "none";
					elFromTween.style.transition = "none";
					elFromTween.style.position = elTo.style.position;
					elFromTween.style.left = `${elFromPosition.left - documentScroll.scrollLeft}px`;
					elFromTween.style.right = "unset";
					elFromTween.style.top = `${elFromPosition.top - documentScroll.scrollTop}px`;
					elFromTween.style.margin = 0;
					elFromTween.style.pointerEvents = "none";
					if (options.resize === true) {
						elFromTween.style.minWidth = "unset";
						elFromTween.style.maxWidth = "unset";
						elFromTween.style.minHeight = "unset";
						elFromTween.style.maxHeight = "unset";
						elFromTween.style.overflow = "hidden";
						elFromTween.style.overflowX = "hidden";
						elFromTween.style.overflowY = "hidden";
					}
					document.body.append(elFromTween);
				}
				const commonCleanup = (aborted) => {
					if (elFrom === elTo && endElementTo !== true) {
						elTo.style.cssText = elFromStyleSaved;
						elTo.className = elFromClassSaved;
					} else {
						elTo.style.cssText = elToStyleSaved;
						elTo.className = elToClassSaved;
					}
					if (elToClone.parentNode === elToParent) elToClone.before(elTo);
					elFromClone.remove();
					elToClone.remove();
					elFromTween?.remove();
					cancel = defaultCancel;
					elFrom.qMorphCancel = void 0;
					elTo.qMorphCancel = void 0;
					if (typeof options.onEnd === "function") options.onEnd(endElementTo === true ? "to" : "from", aborted === true);
				};
				if (options.useCSS !== true && typeof elTo.animate === "function") {
					const resizeFrom = options.resize === true ? {
						transform: `translate(${deltaX}px, ${deltaY}px)`,
						width: `${elFromCloneWidth}px`,
						height: `${elFromCloneHeight}px`
					} : { transform: `translate(${deltaX}px, ${deltaY}px) scale(${scaleX}, ${scaleY})` };
					const resizeTo = options.resize === true ? {
						width: `${elToCloneWidth}px`,
						height: `${elToCloneHeight}px`
					} : {};
					const resizeFromTween = options.resize === true ? {
						width: `${elFromCloneWidth}px`,
						height: `${elFromCloneHeight}px`
					} : {};
					const resizeToTween = options.resize === true ? {
						transform: `translate(${-1 * deltaX}px, ${-1 * deltaY}px)`,
						width: `${elToCloneWidth}px`,
						height: `${elToCloneHeight}px`
					} : { transform: `translate(${-1 * deltaX}px, ${-1 * deltaY}px) scale(${1 / scaleX}, ${1 / scaleY})` };
					const tweenFrom = elFromTween !== void 0 ? { opacity: options.tweenToOpacity } : { backgroundColor: elFromBackground };
					const tweenTo = elFromTween !== void 0 ? { opacity: 1 } : { backgroundColor: elToBackground };
					animationTo = elTo.animate([{
						margin: 0,
						borderWidth: elFromBorderWidth,
						borderStyle: elFromBorderStyle,
						borderColor: elFromBorderColor,
						borderRadius: elFromBorderRadius,
						zIndex: elFromZIndex,
						transformOrigin: "0 0",
						...resizeFrom,
						...tweenFrom
					}, {
						margin: 0,
						borderWidth: elToBorderWidth,
						borderStyle: elToBorderStyle,
						borderColor: elToBorderColor,
						borderRadius: elToBorderRadius,
						zIndex: elToZIndex,
						transformOrigin: "0 0",
						transform: elToTransform,
						...resizeTo,
						...tweenTo
					}], {
						duration: options.duration,
						easing: options.easing,
						fill: options.fill,
						delay: options.delay
					});
					animationFromTween = elFromTween === void 0 ? void 0 : elFromTween.animate([{
						opacity: options.tweenFromOpacity,
						margin: 0,
						borderWidth: elFromBorderWidth,
						borderStyle: elFromBorderStyle,
						borderColor: elFromBorderColor,
						borderRadius: elFromBorderRadius,
						zIndex: elFromZIndex,
						transformOrigin: "0 0",
						transform: elFromTransform,
						...resizeFromTween
					}, {
						opacity: 0,
						margin: 0,
						borderWidth: elToBorderWidth,
						borderStyle: elToBorderStyle,
						borderColor: elToBorderColor,
						borderRadius: elToBorderRadius,
						zIndex: elToZIndex,
						transformOrigin: "0 0",
						...resizeToTween
					}], {
						duration: options.duration,
						easing: options.easing,
						fill: options.fill,
						delay: options.delay
					});
					animationFromClone = options.hideFromClone === true || elSharedSize === true ? void 0 : elFromClone.animate([{
						margin: `${elFromParentHeightDiff < 0 ? elFromParentHeightDiff / 2 : 0}px ${elFromParentWidthDiff < 0 ? elFromParentWidthDiff / 2 : 0}px`,
						width: `${elFromCloneWidth + elFromPosition.marginH}px`,
						height: `${elFromCloneHeight + elFromPosition.marginV}px`
					}, {
						margin: 0,
						width: 0,
						height: 0
					}], {
						duration: options.duration,
						easing: options.easing,
						fill: options.fill,
						delay: options.delay
					});
					animationToClone = options.keepToClone === true ? void 0 : elToClone.animate([elSharedSize === true ? {
						margin: `${elFromParentHeightDiff < 0 ? elFromParentHeightDiff / 2 : 0}px ${elFromParentWidthDiff < 0 ? elFromParentWidthDiff / 2 : 0}px`,
						width: `${elFromCloneWidth + elFromPosition.marginH}px`,
						height: `${elFromCloneHeight + elFromPosition.marginV}px`
					} : {
						margin: 0,
						width: 0,
						height: 0
					}, {
						margin: `${elToParentHeightDiff < 0 ? elToParentHeightDiff / 2 : 0}px ${elToParentWidthDiff < 0 ? elToParentWidthDiff / 2 : 0}px`,
						width: `${elToCloneWidth + elToPosition.marginH}px`,
						height: `${elToCloneHeight + elToPosition.marginV}px`
					}], {
						duration: options.duration,
						easing: options.easing,
						fill: options.fill,
						delay: options.delay
					});
					const cleanup = (abort) => {
						animationFromClone?.cancel();
						animationFromTween?.cancel();
						animationToClone?.cancel();
						animationTo.cancel();
						animationTo.removeEventListener("finish", cleanup);
						animationTo.removeEventListener("cancel", cleanup);
						commonCleanup(abort);
						animationFromClone = void 0;
						animationFromTween = void 0;
						animationToClone = void 0;
						animationTo = void 0;
					};
					elFrom.qMorphCancel = () => {
						elFrom.qMorphCancel = void 0;
						cancelStatus = true;
						cleanup();
					};
					elTo.qMorphCancel = () => {
						elTo.qMorphCancel = void 0;
						cancelStatus = true;
						cleanup();
					};
					animationTo.addEventListener("finish", cleanup);
					animationTo.addEventListener("cancel", cleanup);
					cancel = (abort) => {
						if (cancelStatus === true || animationTo === void 0) return false;
						if (abort === true) {
							cleanup(true);
							return true;
						}
						endElementTo = endElementTo !== true;
						animationFromClone?.reverse();
						animationFromTween?.reverse();
						animationToClone?.reverse();
						animationTo.reverse();
						return true;
					};
				} else {
					const qAnimId = `q-morph-anim-${++id}`;
					const style = document.createElement("style");
					const resizeFrom = options.resize === true ? `
            transform: translate(${deltaX}px, ${deltaY}px);
            width: ${elFromCloneWidth}px;
            height: ${elFromCloneHeight}px;
          ` : `transform: translate(${deltaX}px, ${deltaY}px) scale(${scaleX}, ${scaleY});`;
					const resizeTo = options.resize === true ? `
            width: ${elToCloneWidth}px;
            height: ${elToCloneHeight}px;
          ` : "";
					const resizeFromTween = options.resize === true ? `
            width: ${elFromCloneWidth}px;
            height: ${elFromCloneHeight}px;
          ` : "";
					const resizeToTween = options.resize === true ? `
            transform: translate(${-1 * deltaX}px, ${-1 * deltaY}px);
            width: ${elToCloneWidth}px;
            height: ${elToCloneHeight}px;
          ` : `transform: translate(${-1 * deltaX}px, ${-1 * deltaY}px) scale(${1 / scaleX}, ${1 / scaleY});`;
					const tweenFrom = elFromTween !== void 0 ? `opacity: ${options.tweenToOpacity};` : `background-color: ${elFromBackground};`;
					const tweenTo = elFromTween !== void 0 ? "opacity: 1;" : `background-color: ${elToBackground};`;
					const keyframesFromTween = elFromTween === void 0 ? "" : `
            @keyframes ${qAnimId}-from-tween {
              0% {
                opacity: ${options.tweenFromOpacity};
                margin: 0;
                border-width: ${elFromBorderWidth};
                border-style: ${elFromBorderStyle};
                border-color: ${elFromBorderColor};
                border-radius: ${elFromBorderRadius};
                z-index: ${elFromZIndex};
                transform-origin: 0 0;
                transform: ${elFromTransform};
                ${resizeFromTween}
              }

              100% {
                opacity: 0;
                margin: 0;
                border-width: ${elToBorderWidth};
                border-style: ${elToBorderStyle};
                border-color: ${elToBorderColor};
                border-radius: ${elToBorderRadius};
                z-index: ${elToZIndex};
                transform-origin: 0 0;
                ${resizeToTween}
              }
            }
          `;
					const keyframesFrom = options.hideFromClone === true || elSharedSize === true ? "" : `
            @keyframes ${qAnimId}-from {
              0% {
                margin: ${elFromParentHeightDiff < 0 ? elFromParentHeightDiff / 2 : 0}px ${elFromParentWidthDiff < 0 ? elFromParentWidthDiff / 2 : 0}px;
                width: ${elFromCloneWidth + elFromPosition.marginH}px;
                height: ${elFromCloneHeight + elFromPosition.marginV}px;
              }

              100% {
                margin: 0;
                width: 0;
                height: 0;
              }
            }
          `;
					const keyframeToStart = elSharedSize === true ? `
            margin: ${elFromParentHeightDiff < 0 ? elFromParentHeightDiff / 2 : 0}px ${elFromParentWidthDiff < 0 ? elFromParentWidthDiff / 2 : 0}px;
            width: ${elFromCloneWidth + elFromPosition.marginH}px;
            height: ${elFromCloneHeight + elFromPosition.marginV}px;
          ` : `
            margin: 0;
            width: 0;
            height: 0;
          `;
					const keyframesTo = options.keepToClone === true ? "" : `
            @keyframes ${qAnimId}-to {
              0% {
                ${keyframeToStart}
              }

              100% {
                margin: ${elToParentHeightDiff < 0 ? elToParentHeightDiff / 2 : 0}px ${elToParentWidthDiff < 0 ? elToParentWidthDiff / 2 : 0}px;
                width: ${elToCloneWidth + elToPosition.marginH}px;
                height: ${elToCloneHeight + elToPosition.marginV}px;
              }
            }
          `;
					style.innerHTML = `
          @keyframes ${qAnimId} {
            0% {
              margin: 0;
              border-width: ${elFromBorderWidth};
              border-style: ${elFromBorderStyle};
              border-color: ${elFromBorderColor};
              border-radius: ${elFromBorderRadius};
              background-color: ${elFromBackground};
              z-index: ${elFromZIndex};
              transform-origin: 0 0;
              ${resizeFrom}
              ${tweenFrom}
            }

            100% {
              margin: 0;
              border-width: ${elToBorderWidth};
              border-style: ${elToBorderStyle};
              border-color: ${elToBorderColor};
              border-radius: ${elToBorderRadius};
              background-color: ${elToBackground};
              z-index: ${elToZIndex};
              transform-origin: 0 0;
              transform: ${elToTransform};
              ${resizeTo}
              ${tweenTo}
            }
          }

          ${keyframesFrom}

          ${keyframesFromTween}

          ${keyframesTo}
        `;
					document.head.append(style);
					let animationDirection = "normal";
					elFromClone.style.animation = `${options.duration}ms ${options.easing} ${options.delay}ms ${animationDirection} ${options.fill} ${qAnimId}-from`;
					if (elFromTween !== void 0) elFromTween.style.animation = `${options.duration}ms ${options.easing} ${options.delay}ms ${animationDirection} ${options.fill} ${qAnimId}-from-tween`;
					elToClone.style.animation = `${options.duration}ms ${options.easing} ${options.delay}ms ${animationDirection} ${options.fill} ${qAnimId}-to`;
					elTo.style.animation = `${options.duration}ms ${options.easing} ${options.delay}ms ${animationDirection} ${options.fill} ${qAnimId}`;
					const cleanup = (evt) => {
						if (evt === Object(evt) && evt.animationName !== qAnimId) return;
						elTo.removeEventListener("animationend", cleanup);
						elTo.removeEventListener("animationcancel", cleanup);
						commonCleanup();
						style.remove();
					};
					elFrom.qMorphCancel = () => {
						elFrom.qMorphCancel = void 0;
						cancelStatus = true;
						cleanup();
					};
					elTo.qMorphCancel = () => {
						elTo.qMorphCancel = void 0;
						cancelStatus = true;
						cleanup();
					};
					elTo.addEventListener("animationend", cleanup);
					elTo.addEventListener("animationcancel", cleanup);
					cancel = (abort) => {
						if (cancelStatus === true || !elTo || !elFromClone || !elToClone) return false;
						if (abort === true) {
							cleanup();
							return true;
						}
						endElementTo = endElementTo !== true;
						animationDirection = animationDirection === "normal" ? "reverse" : "normal";
						elFromClone.style.animationDirection = animationDirection;
						elFromTween.style.animationDirection = animationDirection;
						elToClone.style.animationDirection = animationDirection;
						elTo.style.animationDirection = animationDirection;
						return true;
					};
				}
			};
			if (options.waitFor > 0 || options.waitFor === "transitionend" || options.waitFor === Object(options.waitFor) && typeof options.waitFor.then === "function") (options.waitFor > 0 ? new Promise((resolve) => {
				setTimeout(resolve, options.waitFor);
			}) : options.waitFor === "transitionend" ? new Promise((resolve) => {
				const endFn = () => {
					if (timer !== null) {
						clearTimeout(timer);
						timer = null;
					}
					if (elTo) {
						elTo.removeEventListener("transitionend", endFn);
						elTo.removeEventListener("transitioncancel", endFn);
					}
					resolve?.();
					resolve = null;
				};
				let timer = setTimeout(endFn, 400);
				elTo.addEventListener("transitionend", endFn);
				elTo.addEventListener("transitioncancel", endFn);
			}) : options.waitFor).then(animate).catch(() => {
				if (typeof elTo.qMorphCancel === "function") elTo.qMorphCancel();
			});
			else animate();
		};
		if (typeof _options.onToggle === "function") _options.onToggle();
		requestAnimationFrame(calculateFinalState);
		return (abort) => cancel(abort);
	}
	//#endregion
	//#region src/directives/morph/Morph.js
	const morphGroups = {};
	const props$1 = [
		"duration",
		"delay",
		"easing",
		"fill",
		"classes",
		"style",
		"duration",
		"resize",
		"useCSS",
		"hideFromClone",
		"keepToClone",
		"tween",
		"tweenFromOpacity",
		"tweenToOpacity",
		"waitFor",
		"onEnd"
	];
	const mods = [
		"resize",
		"useCSS",
		"hideFromClone",
		"keepToClone",
		"tween"
	];
	function changeClass(ctx, action) {
		if (ctx.clsAction !== action) {
			ctx.clsAction = action;
			ctx.el.classList[action]("q-morph--invisible");
		}
	}
	function trigger(group) {
		if (group.animating || group.queue.length < 2) return;
		const [from, to] = group.queue;
		group.animating = true;
		from.animating = true;
		to.animating = true;
		changeClass(from, "remove");
		changeClass(to, "remove");
		const cancelFn = morph({
			from: from.el,
			to: to.el,
			onToggle() {
				changeClass(from, "add");
				changeClass(to, "remove");
			},
			...to.opts,
			onEnd(dir, aborted) {
				to.opts.onEnd?.(dir, aborted);
				if (aborted) return;
				from.animating = false;
				to.animating = false;
				group.animating = false;
				group.cancel = void 0;
				group.queue.shift();
				trigger(group);
			}
		});
		group.cancel = () => {
			cancelFn(true);
			group.cancel = void 0;
		};
	}
	function updateModifiers(mod, ctx) {
		const opts = ctx.opts;
		mods.forEach((name) => {
			opts[name] = mod[name] === true;
		});
	}
	function insertArgs(arg, ctx) {
		const opts = typeof arg === "string" && arg.length !== 0 ? arg.split(":") : [];
		ctx.name = opts[0];
		ctx.group = opts[1];
		const parsedOpt = Number.parseFloat(opts[2]);
		Object.assign(ctx.opts, {
			duration: Number.isFinite(parsedOpt) ? parsedOpt : 300,
			waitFor: opts[3]
		});
	}
	function updateArgs(arg, ctx) {
		if (arg.group !== void 0) ctx.group = arg.group;
		if (arg.name !== void 0) ctx.name = arg.name;
		const opts = ctx.opts;
		props$1.forEach((name) => {
			if (arg[name] !== void 0) opts[name] = arg[name];
		});
	}
	function updateModel(name, ctx) {
		if (ctx.name === name) {
			const group = morphGroups[ctx.group];
			if (group === void 0) {
				morphGroups[ctx.group] = {
					name: ctx.group,
					model: name,
					queue: [ctx],
					animating: false
				};
				changeClass(ctx, "remove");
			} else if (group.model !== name) {
				group.model = name;
				group.queue.push(ctx);
				if (!group.animating && group.queue.length === 2) trigger(group);
			}
			return;
		}
		if (!ctx.animating) changeClass(ctx, "add");
	}
	function updateValue(ctx, value) {
		let model;
		if (Object(value) === value) {
			model = String(value.model);
			updateArgs(value, ctx);
			updateModifiers(value, ctx);
		} else model = String(value);
		if (model !== ctx.model) {
			ctx.model = model;
			updateModel(model, ctx);
		} else if (!ctx.animating && ctx.clsAction !== void 0) ctx.el.classList[ctx.clsAction]("q-morph--invisible");
	}
	var Morph_default = createDirective({
		name: "morph",
		mounted(el, binding) {
			const ctx = {
				el,
				animating: false,
				opts: {}
			};
			updateModifiers(binding.modifiers, ctx);
			insertArgs(binding.arg, ctx);
			updateValue(ctx, binding.value);
			el.__qmorph = ctx;
		},
		updated(el, binding) {
			updateValue(el.__qmorph, binding.value);
		},
		beforeUnmount(el) {
			const ctx = el.__qmorph;
			const group = morphGroups[ctx.group];
			if (group?.queue.includes(ctx)) {
				group.queue = group.queue.filter((item) => item !== ctx);
				if (group.queue.length === 0) {
					group.cancel?.();
					delete morphGroups[ctx.group];
				}
			}
			if (ctx.clsAction === "add") el.classList.remove("q-morph--invisible");
			delete el.__qmorph;
		}
	});
	//#endregion
	//#region src/directives/mutation/Mutation.js
	const defaultCfg = {
		childList: true,
		subtree: true,
		attributes: true,
		characterData: true,
		attributeOldValue: true,
		characterDataOldValue: true
	};
	function update$2(el, ctx, value) {
		ctx.handler = value;
		ctx.observer?.disconnect();
		ctx.observer = new MutationObserver((list) => {
			if (typeof ctx.handler === "function") {
				if (ctx.handler(list) === false || ctx.once === true) destroy(el);
			}
		});
		ctx.observer.observe(el, ctx.opts);
	}
	function destroy(el) {
		const ctx = el.__qmutation;
		if (ctx !== void 0) {
			ctx.observer?.disconnect();
			delete el.__qmutation;
		}
	}
	var Mutation_default = createDirective({
		name: "mutation",
		mounted(el, { modifiers: { once, ...mod }, value }) {
			const ctx = {
				once,
				opts: Object.keys(mod).length === 0 ? defaultCfg : mod
			};
			update$2(el, ctx, value);
			el.__qmutation = ctx;
		},
		updated(el, { oldValue, value }) {
			const ctx = el.__qmutation;
			if (ctx !== void 0 && oldValue !== value) update$2(el, ctx, value);
		},
		beforeUnmount: destroy
	});
	//#endregion
	//#region src/directives/scroll-fire/ScrollFire.js
	const { passive } = listenOpts;
	function update$1(ctx, { value, oldValue }) {
		if (typeof value !== "function") {
			ctx.scrollTarget.removeEventListener("scroll", ctx.scroll, passive);
			return;
		}
		ctx.handler = value;
		if (typeof oldValue !== "function") {
			ctx.scrollTarget.addEventListener("scroll", ctx.scroll, passive);
			ctx.scroll();
		}
	}
	var ScrollFire_default = createDirective({
		name: "scroll-fire",
		mounted(el, binding) {
			const ctx = {
				scrollTarget: getScrollTarget(el),
				scroll: debounce(() => {
					let containerBottom, elBottom;
					if (ctx.scrollTarget === window) {
						elBottom = el.getBoundingClientRect().bottom;
						containerBottom = window.innerHeight;
					} else {
						elBottom = offset(el).top + height(el);
						containerBottom = offset(ctx.scrollTarget).top + height(ctx.scrollTarget);
					}
					if (elBottom > 0 && elBottom < containerBottom) {
						ctx.scrollTarget.removeEventListener("scroll", ctx.scroll, passive);
						ctx.handler(el);
					}
				}, 25)
			};
			update$1(ctx, binding);
			el.__qscrollfire = ctx;
		},
		updated(el, binding) {
			if (binding.value !== binding.oldValue) update$1(el.__qscrollfire, binding);
		},
		beforeUnmount(el) {
			const ctx = el.__qscrollfire;
			ctx.scrollTarget.removeEventListener("scroll", ctx.scroll, passive);
			ctx.scroll.cancel();
			delete el.__qscrollfire;
		}
	});
	//#endregion
	//#region src/directives/scroll/Scroll.js
	function update(ctx, { value, oldValue }) {
		if (typeof value !== "function") {
			ctx.scrollTarget.removeEventListener("scroll", ctx.scroll, listenOpts.passive);
			return;
		}
		ctx.handler = value;
		if (typeof oldValue !== "function") ctx.scrollTarget.addEventListener("scroll", ctx.scroll, listenOpts.passive);
	}
	var Scroll_default = createDirective({
		name: "scroll",
		mounted(el, binding) {
			const ctx = {
				scrollTarget: getScrollTarget(el),
				scroll() {
					ctx.handler(getVerticalScrollPosition(ctx.scrollTarget), getHorizontalScrollPosition(ctx.scrollTarget));
				}
			};
			update(ctx, binding);
			el.__qscroll = ctx;
		},
		updated(el, binding) {
			if (el.__qscroll !== void 0 && binding.oldValue !== binding.value) update(el.__qscroll, binding);
		},
		beforeUnmount(el) {
			const ctx = el.__qscroll;
			ctx.scrollTarget.removeEventListener("scroll", ctx.scroll, listenOpts.passive);
			delete el.__qscroll;
		}
	});
	//#endregion
	//#region src/directives/touch-hold/TouchHold.js
	function removeBodyNonSelectable$1() {
		document.body.classList.remove("non-selectable");
	}
	var TouchHold_default = createDirective({
		name: "touch-hold",
		beforeMount(el, binding) {
			const { modifiers } = binding;
			if (!modifiers.mouse && !client.has.touch) return;
			const ctx = {
				handler: binding.value,
				noop,
				mouseStart(evt) {
					if (typeof ctx.handler === "function" && leftClick(evt)) {
						addEvt(ctx, "temp", [[
							document,
							"mousemove",
							"move",
							"passiveCapture"
						], [
							document,
							"click",
							"end",
							"notPassiveCapture"
						]]);
						ctx.start(evt, true);
					}
				},
				touchStart(evt) {
					if (evt.target !== void 0 && typeof ctx.handler === "function") {
						const target = evt.target;
						addEvt(ctx, "temp", [
							[
								target,
								"touchmove",
								"move",
								"passiveCapture"
							],
							[
								target,
								"touchcancel",
								"end",
								"notPassiveCapture"
							],
							[
								target,
								"touchend",
								"end",
								"notPassiveCapture"
							]
						]);
						ctx.start(evt);
					}
				},
				start(evt, mouseEvent) {
					ctx.origin = position(evt);
					const startTime = Date.now();
					if (client.is.mobile) {
						document.body.classList.add("non-selectable");
						clearSelection();
						ctx.styleCleanup = (withDelay) => {
							ctx.styleCleanup = void 0;
							if (withDelay === true) {
								clearSelection();
								setTimeout(removeBodyNonSelectable$1, 10);
							} else removeBodyNonSelectable$1();
						};
					}
					ctx.triggered = false;
					ctx.sensitivity = mouseEvent ? ctx.mouseSensitivity : ctx.touchSensitivity;
					ctx.timer = setTimeout(() => {
						ctx.timer = void 0;
						clearSelection();
						ctx.triggered = true;
						ctx.handler({
							evt,
							touch: !mouseEvent,
							mouse: mouseEvent === true,
							position: ctx.origin,
							duration: Date.now() - startTime
						});
					}, ctx.duration);
				},
				move(evt) {
					const { top, left } = position(evt);
					if (ctx.timer !== void 0 && (Math.abs(left - ctx.origin.left) >= ctx.sensitivity || Math.abs(top - ctx.origin.top) >= ctx.sensitivity)) {
						clearTimeout(ctx.timer);
						ctx.timer = void 0;
					}
				},
				end(evt) {
					cleanEvt(ctx, "temp");
					ctx.styleCleanup?.(ctx.triggered);
					if (ctx.triggered) {
						if (evt !== void 0) stopAndPrevent(evt);
					} else if (ctx.timer !== void 0) {
						clearTimeout(ctx.timer);
						ctx.timer = void 0;
					}
				}
			};
			const data = [
				600,
				5,
				7
			];
			if (typeof binding.arg === "string" && binding.arg.length !== 0) binding.arg.split(":").forEach((val, index) => {
				const v = Number.parseInt(val, 10);
				if (v) data[index] = v;
			});
			[ctx.duration, ctx.touchSensitivity, ctx.mouseSensitivity] = data;
			el.__qtouchhold = ctx;
			if (modifiers.mouse) addEvt(ctx, "main", [[
				el,
				"mousedown",
				"mouseStart",
				`passive${modifiers.mouseCapture || modifiers.mousecapture ? "Capture" : ""}`
			]]);
			if (client.has.touch) addEvt(ctx, "main", [[
				el,
				"touchstart",
				"touchStart",
				`passive${modifiers.capture ? "Capture" : ""}`
			], [
				el,
				"touchend",
				"noop",
				"notPassiveCapture"
			]]);
		},
		updated(el, binding) {
			const ctx = el.__qtouchhold;
			if (ctx !== void 0 && binding.oldValue !== binding.value) {
				if (typeof binding.value !== "function") ctx.end();
				ctx.handler = binding.value;
			}
		},
		beforeUnmount(el) {
			const ctx = el.__qtouchhold;
			if (ctx !== void 0) {
				cleanEvt(ctx, "main");
				cleanEvt(ctx, "temp");
				if (ctx.timer !== void 0) clearTimeout(ctx.timer);
				ctx.styleCleanup?.();
				delete el.__qtouchhold;
			}
		}
	});
	//#endregion
	//#region src/directives/touch-repeat/TouchRepeat.js
	const keyCodes = {
		esc: 27,
		tab: 9,
		enter: 13,
		space: 32,
		up: 38,
		left: 37,
		right: 39,
		down: 40,
		delete: [8, 46]
	};
	const keyRegex = new RegExp(`^([\\d+]+|${Object.keys(keyCodes).join("|")})$`, "i");
	function shouldEnd(evt, origin) {
		const { top, left } = position(evt);
		return Math.abs(left - origin.left) >= 7 || Math.abs(top - origin.top) >= 7;
	}
	function removeBodyNonSelectable() {
		document.body.classList.remove("non-selectable");
	}
	var TouchRepeat_default = createDirective({
		name: "touch-repeat",
		beforeMount(el, { modifiers, value, arg }) {
			const keyboard = Object.keys(modifiers).reduce((acc, key) => {
				if (keyRegex.test(key)) {
					const parsedKey = Number.parseInt(key, 10);
					const keyCode = Number.isNaN(parsedKey) ? keyCodes[key.toLowerCase()] : parsedKey;
					if (keyCode !== void 0) acc.push(...[keyCode].flat());
				}
				return acc;
			}, []);
			if (!modifiers.mouse && !client.has.touch && keyboard.length === 0) return;
			const durations = typeof arg === "string" && arg.length !== 0 ? arg.split(":").map((val) => Number.parseInt(val, 10)) : [
				0,
				600,
				300
			];
			const durationsLast = durations.length - 1;
			const ctx = {
				keyboard,
				handler: value,
				noop,
				mouseStart(evt) {
					if (ctx.event === void 0 && typeof ctx.handler === "function" && leftClick(evt)) {
						addEvt(ctx, "temp", [[
							document,
							"mousemove",
							"move",
							"passiveCapture"
						], [
							document,
							"click",
							"end",
							"notPassiveCapture"
						]]);
						ctx.start(evt, true);
					}
				},
				keyboardStart(evt) {
					if (typeof ctx.handler === "function" && isKeyCode(evt, keyboard)) {
						if (durations[0] === 0 || ctx.event !== void 0) {
							stopAndPrevent(evt);
							el.focus();
							if (ctx.event !== void 0) return;
						}
						addEvt(ctx, "temp", [[
							document,
							"keyup",
							"end",
							"notPassiveCapture"
						], [
							document,
							"click",
							"end",
							"notPassiveCapture"
						]]);
						ctx.start(evt, false, true);
					}
				},
				touchStart(evt) {
					if (evt.target !== void 0 && typeof ctx.handler === "function") {
						const target = evt.target;
						addEvt(ctx, "temp", [
							[
								target,
								"touchmove",
								"move",
								"passiveCapture"
							],
							[
								target,
								"touchcancel",
								"end",
								"notPassiveCapture"
							],
							[
								target,
								"touchend",
								"end",
								"notPassiveCapture"
							]
						]);
						ctx.start(evt);
					}
				},
				start(evt, mouseEvent, keyboardEvent) {
					if (!keyboardEvent) ctx.origin = position(evt);
					function styleCleanup(withDelay) {
						ctx.styleCleanup = void 0;
						document.documentElement.style.cursor = "";
						if (withDelay === true) {
							clearSelection();
							setTimeout(removeBodyNonSelectable, 10);
						} else removeBodyNonSelectable();
					}
					if (client.is.mobile) {
						document.body.classList.add("non-selectable");
						clearSelection();
						ctx.styleCleanup = styleCleanup;
					}
					ctx.event = {
						touch: !mouseEvent && !keyboardEvent,
						mouse: mouseEvent === true,
						keyboard: keyboardEvent === true,
						startTime: Date.now(),
						repeatCount: 0
					};
					const fn = () => {
						ctx.timer = void 0;
						if (ctx.event === void 0) return;
						if (ctx.event.repeatCount === 0) {
							ctx.event.evt = evt;
							if (keyboardEvent) ctx.event.keyCode = evt.keyCode;
							else ctx.event.position = position(evt);
							if (!client.is.mobile) {
								document.documentElement.style.cursor = "pointer";
								document.body.classList.add("non-selectable");
								clearSelection();
								ctx.styleCleanup = styleCleanup;
							}
						}
						ctx.event.duration = Date.now() - ctx.event.startTime;
						ctx.event.repeatCount += 1;
						ctx.handler(ctx.event);
						const index = durationsLast < ctx.event.repeatCount ? durationsLast : ctx.event.repeatCount;
						ctx.timer = setTimeout(fn, durations[index]);
					};
					if (durations[0] === 0) fn();
					else ctx.timer = setTimeout(fn, durations[0]);
				},
				move(evt) {
					if (ctx.event !== void 0 && ctx.timer !== void 0 && shouldEnd(evt, ctx.origin)) {
						clearTimeout(ctx.timer);
						ctx.timer = void 0;
					}
				},
				end(evt) {
					if (ctx.event === void 0) return;
					ctx.styleCleanup?.(true);
					if (evt !== void 0 && ctx.event.repeatCount > 0) stopAndPrevent(evt);
					cleanEvt(ctx, "temp");
					if (ctx.timer !== void 0) {
						clearTimeout(ctx.timer);
						ctx.timer = void 0;
					}
					ctx.event = void 0;
				}
			};
			el.__qtouchrepeat = ctx;
			if (modifiers.mouse) addEvt(ctx, "main", [[
				el,
				"mousedown",
				"mouseStart",
				`passive${modifiers.mouseCapture || modifiers.mousecapture ? "Capture" : ""}`
			]]);
			if (client.has.touch) addEvt(ctx, "main", [[
				el,
				"touchstart",
				"touchStart",
				`passive${modifiers.capture ? "Capture" : ""}`
			], [
				el,
				"touchend",
				"noop",
				"passiveCapture"
			]]);
			if (keyboard.length !== 0) addEvt(ctx, "main", [[
				el,
				"keydown",
				"keyboardStart",
				`notPassive${modifiers.keyCapture || modifiers.keycapture ? "Capture" : ""}`
			]]);
		},
		updated(el, { oldValue, value }) {
			const ctx = el.__qtouchrepeat;
			if (ctx !== void 0 && oldValue !== value) {
				if (typeof value !== "function") ctx.end();
				ctx.handler = value;
			}
		},
		beforeUnmount(el) {
			const ctx = el.__qtouchrepeat;
			if (ctx !== void 0) {
				if (ctx.timer !== void 0) clearTimeout(ctx.timer);
				cleanEvt(ctx, "main");
				cleanEvt(ctx, "temp");
				ctx.styleCleanup?.();
				delete el.__qtouchrepeat;
			}
		}
	});
	//#endregion
	//#region src/directives.js
	var directives_exports = /* @__PURE__ */ __exportAll({
		ClosePopup: () => ClosePopup_default,
		Intersection: () => Intersection_default,
		Morph: () => Morph_default,
		Mutation: () => Mutation_default,
		Ripple: () => Ripple_default,
		Scroll: () => Scroll_default,
		ScrollFire: () => ScrollFire_default,
		TouchHold: () => TouchHold_default,
		TouchPan: () => TouchPan_default,
		TouchRepeat: () => TouchRepeat_default,
		TouchSwipe: () => TouchSwipe_default
	});
	//#endregion
	//#region src/utils/css-var/get-css-var.js
	function getCssVar(propName, element = document.body) {
		if (typeof propName !== "string") throw new TypeError("Expected a string as propName");
		if (!(element instanceof Element)) throw new TypeError("Expected a DOM element");
		return getComputedStyle(element).getPropertyValue(`--q-${propName}`).trim() || null;
	}
	//#endregion
	//#region src/plugins/addressbar/AddressbarColor.js
	let metaValue;
	function getProp() {
		return client.is.winphone ? "msapplication-navbutton-color" : "theme-color";
	}
	function getMetaTag(v) {
		const els = document.getElementsByTagName("META");
		for (const i in els) if (els[i].name === v) return els[i];
	}
	function setColor(hexColor) {
		if (metaValue === void 0) metaValue = getProp();
		let metaTag = getMetaTag(metaValue);
		const newTag = metaTag === void 0;
		if (newTag) {
			metaTag = document.createElement("meta");
			metaTag.setAttribute("name", metaValue);
		}
		metaTag.setAttribute("content", hexColor);
		if (newTag) document.head.append(metaTag);
	}
	var AddressbarColor_default = {
		set: client.is.mobile && (client.is.nativeMobile || client.is.winphone || client.is.safari || client.is.webkit || client.is.vivaldi) ? (hexColor) => {
			const val = hexColor || getCssVar("primary");
			if (client.is.nativeMobile && window.StatusBar) window.StatusBar.backgroundColorByHexString(val);
			else setColor(val);
		} : noop,
		install({ $q }) {
			$q.addressbarColor = this;
			if ($q.config.addressbarColor) this.set($q.config.addressbarColor);
		}
	};
	//#endregion
	//#region src/plugins/app-fullscreen/AppFullscreen.js
	const prefixes = {};
	function assignFn(fn) {
		Object.assign(Plugin$6, {
			request: fn,
			exit: fn,
			toggle: fn
		});
	}
	function getFullscreenElement() {
		return document.fullscreenElement || document.mozFullScreenElement || document.webkitFullscreenElement || document.msFullscreenElement || null;
	}
	function updateEl() {
		const newEl = Plugin$6.activeEl = Plugin$6.isActive ? getFullscreenElement() : null;
		changeGlobalNodesTarget(newEl === null || newEl === document.documentElement ? document.body : newEl);
	}
	function togglePluginState() {
		Plugin$6.isActive = !Plugin$6.isActive;
		updateEl();
	}
	function promisify(target, fn) {
		try {
			const res = target[fn]();
			return res === void 0 ? Promise.resolve() : res;
		} catch (err) {
			return Promise.reject(err);
		}
	}
	const Plugin$6 = createReactivePlugin({
		isActive: false,
		activeEl: null
	}, {
		isCapable: false,
		install({ $q }) {
			$q.fullscreen = this;
		}
	});
	prefixes.request = [
		"requestFullscreen",
		"msRequestFullscreen",
		"mozRequestFullScreen",
		"webkitRequestFullscreen"
	].find((request) => document.documentElement[request] !== void 0);
	Plugin$6.isCapable = prefixes.request !== void 0;
	if (!Plugin$6.isCapable) assignFn(() => Promise.reject(/* @__PURE__ */ new Error("Not capable")));
	else {
		Object.assign(Plugin$6, {
			request(target) {
				const el = target || document.documentElement;
				const { activeEl } = Plugin$6;
				if (el === activeEl) return Promise.resolve();
				return (activeEl !== null && el.contains(activeEl) ? Plugin$6.exit() : Promise.resolve()).finally(() => promisify(el, prefixes.request));
			},
			exit() {
				return Plugin$6.isActive ? promisify(document, prefixes.exit) : Promise.resolve();
			},
			toggle(target) {
				return Plugin$6.isActive ? Plugin$6.exit() : Plugin$6.request(target);
			}
		});
		prefixes.exit = [
			"exitFullscreen",
			"msExitFullscreen",
			"mozCancelFullScreen",
			"webkitExitFullscreen"
		].find((exit) => document[exit]);
		Plugin$6.isActive = Boolean(getFullscreenElement());
		if (Plugin$6.isActive) updateEl();
		[
			"onfullscreenchange",
			"onmsfullscreenchange",
			"onwebkitfullscreenchange"
		].forEach((evt) => {
			document[evt] = togglePluginState;
		});
	}
	//#endregion
	//#region src/plugins/app-visibility/AppVisibility.js
	const Plugin$5 = createReactivePlugin({ appVisible: true }, { install({ $q }) {
		injectProp($q, "appVisible", () => this.appVisible);
	} });
	{
		let prop, evt;
		if (document.hidden !== void 0) {
			prop = "hidden";
			evt = "visibilitychange";
		} else if (document.msHidden !== void 0) {
			prop = "msHidden";
			evt = "msvisibilitychange";
		} else if (document.webkitHidden !== void 0) {
			prop = "webkitHidden";
			evt = "webkitvisibilitychange";
		}
		if (evt && document[prop] !== void 0) {
			const update = () => {
				Plugin$5.appVisible = !document[prop];
			};
			document.addEventListener(evt, update, false);
		}
	}
	//#endregion
	//#region src/plugins/bottom-sheet/component/BottomSheetComponent.js
	var BottomSheetComponent_default = createComponent({
		name: "BottomSheetComponent",
		props: {
			...useDarkProps,
			title: String,
			message: String,
			actions: Array,
			grid: Boolean,
			cardClass: [
				String,
				Array,
				Object
			],
			cardStyle: [
				String,
				Array,
				Object
			]
		},
		emits: ["ok", "hide"],
		setup(props, { emit }) {
			const { proxy } = (0, vue.getCurrentInstance)();
			const isDark = useDark(props, proxy.$q);
			const dialogRef = (0, vue.ref)(null);
			function show() {
				dialogRef.value.show();
			}
			function hide() {
				dialogRef.value.hide();
			}
			function onOk(action) {
				emit("ok", action);
				hide();
			}
			function onHide() {
				emit("hide");
			}
			function getGrid() {
				return props.actions.map((action) => {
					const img = action.avatar || action.img;
					return action.label === void 0 ? (0, vue.h)(QSeparator_default, {
						class: "col-all",
						dark: isDark.value
					}) : (0, vue.h)("div", {
						class: ["q-bottom-sheet__item q-hoverable q-focusable cursor-pointer relative-position", action.class],
						style: action.style,
						tabindex: 0,
						role: "listitem",
						onClick() {
							onOk(action);
						},
						onKeyup(e) {
							if (e.keyCode === 13) onOk(action);
						}
					}, [
						(0, vue.h)("div", { class: "q-focus-helper" }),
						action.icon ? (0, vue.h)(QIcon_default, {
							name: action.icon,
							color: action.color
						}) : img ? (0, vue.h)("img", {
							class: action.avatar ? "q-bottom-sheet__avatar" : "",
							src: img
						}) : (0, vue.h)("div", { class: "q-bottom-sheet__empty-icon" }),
						(0, vue.h)("div", action.label)
					]);
				});
			}
			function getList() {
				return props.actions.map((action) => {
					const img = action.avatar || action.img;
					return action.label === void 0 ? (0, vue.h)(QSeparator_default, {
						spaced: true,
						dark: isDark.value
					}) : (0, vue.h)(QItem_default, {
						class: ["q-bottom-sheet__item", action.classes],
						style: action.style,
						tabindex: 0,
						clickable: true,
						dark: isDark.value,
						onClick() {
							onOk(action);
						}
					}, () => [(0, vue.h)(QItemSection_default, { avatar: true }, () => action.icon ? (0, vue.h)(QIcon_default, {
						name: action.icon,
						color: action.color
					}) : img ? (0, vue.h)("img", {
						class: action.avatar ? "q-bottom-sheet__avatar" : "",
						src: img
					}) : null), (0, vue.h)(QItemSection_default, () => action.label)]);
				});
			}
			function getCardContent() {
				const child = [];
				if (props.title) child.push((0, vue.h)(QCardSection_default, { class: "q-dialog__title" }, () => props.title));
				if (props.message) child.push((0, vue.h)(QCardSection_default, { class: "q-dialog__message" }, () => props.message));
				child.push(props.grid ? (0, vue.h)("div", {
					class: "row items-stretch justify-start",
					role: "list"
				}, getGrid()) : (0, vue.h)("div", { role: "list" }, getList()));
				return child;
			}
			function getContent() {
				return [(0, vue.h)(QCard_default, {
					class: [`q-bottom-sheet q-bottom-sheet--${props.grid ? "grid" : "list"}` + (isDark.value ? " q-bottom-sheet--dark q-dark" : ""), props.cardClass],
					style: props.cardStyle
				}, getCardContent)];
			}
			Object.assign(proxy, {
				show,
				hide
			});
			return () => (0, vue.h)(QDialog_default, {
				ref: dialogRef,
				position: "bottom",
				onHide
			}, getContent);
		}
	});
	//#endregion
	//#region src/utils/private.dialog/create-dialog.js
	function merge(target, source) {
		for (const key in source) if (key !== "spinner" && Object(source[key]) === source[key]) {
			target[key] = Object(target[key]) !== target[key] ? {} : { ...target[key] };
			merge(target[key], source[key]);
		} else target[key] = source[key];
	}
	function createDialog(DefaultComponent, supportsCustomComponent, parentApp) {
		return (pluginProps) => {
			let DialogComponent, props;
			const isCustom = supportsCustomComponent && pluginProps.component !== void 0;
			if (isCustom) {
				const { component, componentProps } = pluginProps;
				DialogComponent = typeof component === "string" ? parentApp.component(component) : component;
				props = componentProps || {};
			} else {
				const { class: klass, style, ...otherProps } = pluginProps;
				DialogComponent = DefaultComponent;
				props = otherProps;
				if (klass !== void 0) otherProps.cardClass = klass;
				if (style !== void 0) otherProps.cardStyle = style;
			}
			let vm;
			let emittedOK = false;
			const dialogRef = (0, vue.ref)(null);
			const el = createGlobalNode(false, "dialog");
			const applyState = (cmd) => {
				if (dialogRef.value?.[cmd] !== void 0) {
					dialogRef.value[cmd]();
					return;
				}
				const target = vm.$.subTree;
				if (target?.component) {
					if (target.component.proxy && target.component.proxy[cmd]) {
						target.component.proxy[cmd]();
						return;
					}
					if (target.component.subTree && target.component.subTree.component && target.component.subTree.component.proxy && target.component.subTree.component.proxy[cmd]) {
						target.component.subTree.component.proxy[cmd]();
						return;
					}
				}
				console.error("[Quasar] Incorrectly defined Dialog component");
			};
			const okFns = [], cancelFns = [], API = {
				onOk(fn) {
					okFns.push(fn);
					return API;
				},
				onCancel(fn) {
					cancelFns.push(fn);
					return API;
				},
				onDismiss(fn) {
					okFns.push(fn);
					cancelFns.push(fn);
					return API;
				},
				hide() {
					applyState("hide");
					return API;
				},
				update(componentProps) {
					if (vm !== null) {
						if (isCustom) Object.assign(props, componentProps);
						else {
							const { class: klass, style, ...cfg } = componentProps;
							if (klass !== void 0) cfg.cardClass = klass;
							if (style !== void 0) cfg.cardStyle = style;
							merge(props, cfg);
						}
						vm.$forceUpdate();
					}
					return API;
				}
			};
			const onOk = (data) => {
				emittedOK = true;
				okFns.forEach((fn) => {
					fn(data);
				});
			};
			const onHide = () => {
				app.unmount(el);
				removeGlobalNode(el);
				app = null;
				vm = null;
				if (!emittedOK) cancelFns.forEach((fn) => {
					fn();
				});
			};
			let app = createChildApp({
				name: "QGlobalDialog",
				setup: () => () => (0, vue.h)(DialogComponent, {
					...props,
					ref: dialogRef,
					onOk,
					onHide,
					onVnodeMounted(...args) {
						if (typeof props.onVnodeMounted === "function") props.onVnodeMounted(...args);
						(0, vue.nextTick)(() => applyState("show"));
					}
				})
			}, parentApp);
			vm = app.mount(el);
			return API;
		};
	}
	//#endregion
	//#region src/plugins/bottom-sheet/BottomSheet.js
	var BottomSheet_default = { install({ $q, parentApp }) {
		$q.bottomSheet = this.create = createDialog(BottomSheetComponent_default, false, parentApp);
	} };
	//#endregion
	//#region src/plugins/cookies/Cookies.js
	function stringifyCookieValue(value) {
		return encodeURIComponent(value === Object(value) ? JSON.stringify(value) : String(value));
	}
	function read(string) {
		if (string === "") return string;
		if (string.indexOf("\"") === 0) string = string.slice(1, -1).replaceAll(String.raw`\"`, "\"").replaceAll(String.raw`\\`, "\\");
		try {
			string = decodeURIComponent(string.replaceAll("+", " "));
		} catch {
			return;
		}
		try {
			const parsed = JSON.parse(string);
			if (parsed === Object(parsed) || Array.isArray(parsed)) string = parsed;
		} catch {}
		return string;
	}
	const numberUnitRE = /(\d+)([dhms])/g;
	const numberUnitMultiplierMap = {
		d: 86400,
		h: 3600,
		m: 60,
		s: 1
	};
	function parseExpireToSeconds(str) {
		let totalSeconds = 0;
		let hasMatch = false;
		const matches = str.matchAll(numberUnitRE);
		for (const match of matches) {
			hasMatch = true;
			const value = Number.parseInt(match[1], 10);
			const unit = match[2];
			totalSeconds += value * numberUnitMultiplierMap[unit];
		}
		if (hasMatch) return totalSeconds;
		const timestamp = Date.parse(str);
		return Number.isNaN(timestamp) ? void 0 : Math.round((timestamp - Date.now()) / 1e3);
	}
	function set(key, val, opts = {}, ssr) {
		let maxAge;
		let isDeletion = false;
		if (opts.expires !== void 0) {
			if (Number.isFinite(opts.expires)) maxAge = Math.round(opts.expires * 86400);
			else if (opts.expires instanceof Date) {
				const timestamp = opts.expires.getTime();
				if (Number.isFinite(timestamp)) maxAge = Math.round((timestamp - Date.now()) / 1e3);
			} else if (typeof opts.expires === "string") maxAge = parseExpireToSeconds(opts.expires);
			if (maxAge !== void 0) isDeletion = maxAge <= 0;
		}
		const keyValue = `${encodeURIComponent(key)}=${stringifyCookieValue(val)}`;
		const cookie = [
			keyValue,
			maxAge !== void 0 ? `; Max-Age=${maxAge}` : "",
			opts.path ? `; Path=${opts.path}` : "",
			opts.domain ? `; Domain=${opts.domain}` : "",
			opts.sameSite ? `; SameSite=${opts.sameSite}` : "",
			opts.httpOnly ? "; HttpOnly" : "",
			opts.secure ? "; Secure" : "",
			opts.other ? `; ${opts.other}` : ""
		].join("");
		if (ssr) {
			if (ssr.req.qCookies) ssr.req.qCookies.push(cookie);
			else ssr.req.qCookies = [cookie];
			ssr.res.setHeader("Set-Cookie", ssr.req.qCookies);
			let all = ssr.req.headers.cookie || "";
			if (maxAge !== void 0 && isDeletion) {
				const encodedKey = encodeURIComponent(key);
				all = all.split("; ").filter((entry) => entry.split("=", 1)[0] !== encodedKey).join("; ");
			} else all = all ? `${keyValue}; ${all}` : keyValue;
			ssr.req.headers.cookie = all;
		} else document.cookie = cookie;
	}
	function get(key, ssr) {
		const cookieSource = ssr ? ssr.req.headers : document, cookies = cookieSource.cookie ? cookieSource.cookie.split("; ") : [], l = cookies.length;
		let result = key ? null : {}, i = 0, parts, name, cookie;
		for (; i < l; i++) {
			parts = cookies[i].split("=");
			try {
				name = decodeURIComponent(parts.shift());
			} catch {
				continue;
			}
			cookie = parts.join("=");
			if (!key) result[name] = cookie;
			else if (key === name) {
				result = read(cookie) ?? null;
				break;
			}
		}
		return result;
	}
	function remove(key, options, ssr) {
		set(key, "", {
			expires: -1,
			...options
		}, ssr);
	}
	function has(key, ssr) {
		return get(key, ssr) !== null;
	}
	function getObject(ssr) {
		return {
			get: (key) => get(key, ssr),
			set: (key, val, opts) => set(key, val, opts, ssr),
			has: (key) => has(key, ssr),
			remove: (key, options) => remove(key, options, ssr),
			getAll: () => get(null, ssr)
		};
	}
	const Plugin$4 = { install({ $q, ssrContext }) {
		$q.cookies = this;
	} };
	Object.assign(Plugin$4, getObject());
	//#endregion
	//#region src/plugins/dialog/component/DialogPluginComponent.js
	var DialogPluginComponent_default = createComponent({
		name: "DialogPluginComponent",
		props: {
			...useDarkProps,
			title: String,
			message: String,
			prompt: Object,
			options: Object,
			progress: [Boolean, Object],
			html: Boolean,
			ok: {
				type: [
					String,
					Object,
					Boolean
				],
				default: true
			},
			cancel: [
				String,
				Object,
				Boolean
			],
			focus: {
				type: String,
				default: "ok",
				validator: (v) => [
					"ok",
					"cancel",
					"none"
				].includes(v)
			},
			stackButtons: Boolean,
			color: String,
			cardClass: [
				String,
				Array,
				Object
			],
			cardStyle: [
				String,
				Array,
				Object
			]
		},
		emits: ["ok", "hide"],
		setup(props, { emit }) {
			const { proxy } = (0, vue.getCurrentInstance)();
			const { $q } = proxy;
			const isDark = useDark(props, $q);
			const dialogRef = (0, vue.ref)(null);
			const model = (0, vue.ref)(props.prompt !== void 0 ? props.prompt.model : props.options !== void 0 ? props.options.model : void 0);
			const classes = (0, vue.computed)(() => "q-dialog-plugin" + (isDark.value ? " q-dialog-plugin--dark q-dark" : "") + (props.progress !== false ? " q-dialog-plugin--progress" : ""));
			const vmColor = (0, vue.computed)(() => props.color || (isDark.value ? "amber" : "primary"));
			const spinner = (0, vue.computed)(() => props.progress === false ? null : isObject(props.progress) ? {
				component: props.progress.spinner || QSpinner_default,
				props: { color: props.progress.color || vmColor.value }
			} : {
				component: QSpinner_default,
				props: { color: vmColor.value }
			});
			const hasForm = (0, vue.computed)(() => props.prompt !== void 0 || props.options !== void 0);
			const formProps = (0, vue.computed)(() => {
				if (!hasForm.value) return {};
				const { model, isValid, items, ...acc } = props.prompt !== void 0 ? props.prompt : props.options;
				return acc;
			});
			const okLabel = (0, vue.computed)(() => isObject(props.ok) ? $q.lang.label.ok : props.ok === true ? $q.lang.label.ok : props.ok);
			const cancelLabel = (0, vue.computed)(() => isObject(props.cancel) ? $q.lang.label.cancel : props.cancel === true ? $q.lang.label.cancel : props.cancel);
			const okDisabled = (0, vue.computed)(() => {
				if (props.prompt !== void 0) return props.prompt.isValid !== void 0 && !props.prompt.isValid(model.value);
				if (props.options !== void 0) return props.options.isValid !== void 0 && !props.options.isValid(model.value);
				return false;
			});
			const okProps = (0, vue.computed)(() => ({
				color: vmColor.value,
				label: okLabel.value,
				ripple: false,
				disable: okDisabled.value,
				...isObject(props.ok) ? props.ok : { flat: true },
				"data-autofocus": props.focus === "ok" && !hasForm.value || void 0,
				onClick: onOk
			}));
			const cancelProps = (0, vue.computed)(() => ({
				color: vmColor.value,
				label: cancelLabel.value,
				ripple: false,
				...isObject(props.cancel) ? props.cancel : { flat: true },
				"data-autofocus": props.focus === "cancel" && !hasForm.value || void 0,
				onClick: onCancel
			}));
			(0, vue.watch)(() => props.prompt && props.prompt.model, onUpdateModel);
			(0, vue.watch)(() => props.options && props.options.model, onUpdateModel);
			function show() {
				dialogRef.value.show();
			}
			function hide() {
				dialogRef.value.hide();
			}
			function onOk() {
				emit("ok", (0, vue.toRaw)(model.value));
				hide();
			}
			function onCancel() {
				hide();
			}
			function onDialogHide() {
				emit("hide");
			}
			function onUpdateModel(val) {
				model.value = val;
			}
			function onInputKeyup(evt) {
				if (!okDisabled.value && props.prompt.type !== "textarea" && isKeyCode(evt, 13)) onOk();
			}
			function getSection(sectionClass, text) {
				return props.html ? (0, vue.h)(QCardSection_default, {
					class: sectionClass,
					innerHTML: text
				}) : (0, vue.h)(QCardSection_default, { class: sectionClass }, () => text);
			}
			function getPrompt() {
				return [(0, vue.h)(QInput_default, {
					color: vmColor.value,
					dense: true,
					autofocus: true,
					dark: isDark.value,
					...formProps.value,
					modelValue: model.value,
					"onUpdate:modelValue": onUpdateModel,
					onKeyup: onInputKeyup
				})];
			}
			function getOptions() {
				return [(0, vue.h)(QOptionGroup_default, {
					color: vmColor.value,
					options: props.options.items,
					dark: isDark.value,
					...formProps.value,
					modelValue: model.value,
					"onUpdate:modelValue": onUpdateModel
				})];
			}
			function getButtons() {
				const child = [];
				if (props.cancel) child.push((0, vue.h)(QBtn_default, cancelProps.value));
				if (props.ok) child.push((0, vue.h)(QBtn_default, okProps.value));
				return (0, vue.h)(QCardActions_default, {
					class: props.stackButtons ? "items-end" : "",
					vertical: props.stackButtons,
					align: "right"
				}, () => child);
			}
			function getCardContent() {
				const child = [];
				if (props.title) child.push(getSection("q-dialog__title", props.title));
				if (props.progress !== false) child.push((0, vue.h)(QCardSection_default, { class: "q-dialog__progress" }, () => (0, vue.h)(spinner.value.component, spinner.value.props)));
				if (props.message) child.push(getSection("q-dialog__message", props.message));
				if (props.prompt !== void 0) child.push((0, vue.h)(QCardSection_default, { class: "scroll q-dialog-plugin__form" }, getPrompt));
				else if (props.options !== void 0) child.push((0, vue.h)(QSeparator_default, { dark: isDark.value }), (0, vue.h)(QCardSection_default, { class: "scroll q-dialog-plugin__form" }, getOptions), (0, vue.h)(QSeparator_default, { dark: isDark.value }));
				if (props.ok || props.cancel) child.push(getButtons());
				return child;
			}
			function getContent() {
				return [(0, vue.h)(QCard_default, {
					class: [classes.value, props.cardClass],
					style: props.cardStyle,
					dark: isDark.value
				}, getCardContent)];
			}
			Object.assign(proxy, {
				show,
				hide
			});
			return () => (0, vue.h)(QDialog_default, {
				ref: dialogRef,
				onHide: onDialogHide
			}, getContent);
		}
	});
	//#endregion
	//#region src/plugins/dialog/Dialog.js
	var Dialog_default = { install({ $q, parentApp }) {
		$q.dialog = this.create = createDialog(DialogPluginComponent_default, true, parentApp);
	} };
	//#endregion
	//#region src/plugins/loading/Loading.js
	let app;
	let vm;
	let uid$1 = 0;
	let timeout = null;
	let props = {};
	let activeGroups = {};
	const originalDefaults = {
		group: "__default_quasar_group__",
		delay: 0,
		message: false,
		html: false,
		spinnerSize: 80,
		spinnerColor: "",
		messageColor: "",
		backgroundColor: "",
		boxClass: "",
		spinner: QSpinner_default,
		customClass: ""
	};
	const defaults$1 = { ...originalDefaults };
	function registerProps(opts) {
		if (opts?.group !== void 0 && activeGroups[opts.group] !== void 0) return Object.assign(activeGroups[opts.group], opts);
		const newProps = isObject(opts) && opts.ignoreDefaults ? {
			...originalDefaults,
			...opts
		} : {
			...defaults$1,
			...opts
		};
		activeGroups[newProps.group] = newProps;
		return newProps;
	}
	const Plugin$3 = createReactivePlugin({ isActive: false }, {
		show(opts) {
			props = registerProps(opts);
			const { group } = props;
			Plugin$3.isActive = true;
			if (app !== void 0) {
				props.uid = uid$1;
				vm.$forceUpdate();
			} else {
				props.uid = ++uid$1;
				if (timeout !== null) clearTimeout(timeout);
				timeout = setTimeout(() => {
					timeout = null;
					const el = createGlobalNode("q-loading");
					app = createChildApp({
						name: "QLoading",
						setup() {
							(0, vue.onMounted)(() => {
								preventScroll(true);
							});
							function onAfterLeave() {
								if (!Plugin$3.isActive && app !== void 0) {
									preventScroll(false);
									app.unmount(el);
									removeGlobalNode(el);
									app = void 0;
									vm = void 0;
								}
							}
							function getContent() {
								if (!Plugin$3.isActive) return null;
								const content = [(0, vue.h)(props.spinner, {
									class: "q-loading__spinner",
									color: props.spinnerColor,
									size: props.spinnerSize
								})];
								if (props.message) content.push((0, vue.h)("div", {
									class: "q-loading__message" + (props.messageColor ? ` text-${props.messageColor}` : ""),
									[props.html ? "innerHTML" : "textContent"]: props.message
								}));
								return (0, vue.h)("div", {
									class: "q-loading fullscreen flex flex-center z-max " + props.customClass.trim(),
									key: props.uid
								}, [(0, vue.h)("div", { class: "q-loading__backdrop" + (props.backgroundColor ? ` bg-${props.backgroundColor}` : "") }), (0, vue.h)("div", { class: "q-loading__box column items-center " + props.boxClass }, content)]);
							}
							return () => (0, vue.h)(vue.Transition, {
								name: "q-transition--fade",
								appear: true,
								onAfterLeave
							}, getContent);
						}
					}, Plugin$3.__parentApp);
					vm = app.mount(el);
				}, props.delay);
			}
			return (paramProps) => {
				if (paramProps === void 0 || Object(paramProps) !== paramProps) {
					Plugin$3.hide(group);
					return;
				}
				Plugin$3.show({
					...paramProps,
					group
				});
			};
		},
		hide(group) {
			if (Plugin$3.isActive) {
				if (group === void 0) activeGroups = {};
				else if (activeGroups[group] === void 0) return;
				else {
					delete activeGroups[group];
					const keys = Object.keys(activeGroups);
					if (keys.length !== 0) {
						const lastGroup = keys.at(-1);
						Plugin$3.show({ group: lastGroup });
						return;
					}
				}
				if (timeout !== null) {
					clearTimeout(timeout);
					timeout = null;
				}
				Plugin$3.isActive = false;
			}
		},
		setDefaults(opts) {
			if (isObject(opts)) Object.assign(defaults$1, opts);
		},
		install({ $q, parentApp }) {
			$q.loading = this;
			Plugin$3.__parentApp = parentApp;
			if ($q.config.loading !== void 0) this.setDefaults($q.config.loading);
		}
	});
	//#endregion
	//#region src/plugins/loading-bar/LoadingBar.js
	const barRef = (0, vue.ref)(null);
	const Plugin$2 = createReactivePlugin({ isActive: false }, {
		start: noop,
		stop: noop,
		increment: noop,
		setDefaults: noop,
		install({ $q, parentApp }) {
			$q.loadingBar = this;
			if (this.__installed) {
				if ($q.config.loadingBar !== void 0) this.setDefaults($q.config.loadingBar);
				return;
			}
			const props = (0, vue.ref)($q.config.loadingBar !== void 0 ? { ...$q.config.loadingBar } : {});
			function onStart() {
				Plugin$2.isActive = true;
			}
			function onStop() {
				Plugin$2.isActive = false;
			}
			const el = createGlobalNode("q-loading-bar");
			createChildApp({
				name: "LoadingBar",
				devtools: { hide: true },
				setup: () => () => (0, vue.h)(QAjaxBar_default, {
					...props.value,
					onStart,
					onStop,
					ref: barRef
				})
			}, parentApp).mount(el);
			Object.assign(this, {
				start(speed) {
					barRef.value.start(speed);
				},
				stop() {
					barRef.value.stop();
				},
				increment(...args) {
					barRef.value.increment(...args);
				},
				setDefaults(opts) {
					if (isObject(opts)) Object.assign(props.value, opts);
				}
			});
		}
	});
	//#endregion
	//#region src/plugins/meta/Meta.js
	let updateId = null;
	let currentClientMeta;
	String.raw`\u003C`, String.raw`\u003E`, String.raw`\u0026`, String.raw`\u2028`, String.raw`\u2029`;
	const clientList = [];
	function normalize(meta) {
		if (meta.title) {
			meta.title = meta.titleTemplate ? meta.titleTemplate(meta.title) : meta.title;
			delete meta.titleTemplate;
		}
		[["meta", "content"], ["link", "href"]].forEach((type) => {
			const metaType = meta[type[0]], metaProp = type[1];
			for (const name in metaType) {
				const metaLink = metaType[name];
				if (metaLink.template) if (Object.keys(metaLink).length === 1) delete metaType[name];
				else {
					metaLink[metaProp] = metaLink.template(metaLink[metaProp] || "");
					delete metaLink.template;
				}
			}
		});
	}
	function changed(old, def) {
		if (Object.keys(old).length !== Object.keys(def).length) return true;
		for (const key in old) if (old[key] !== def[key]) return true;
	}
	function bodyFilter(name) {
		return !["class", "style"].includes(name);
	}
	function htmlFilter(name) {
		return !["lang", "dir"].includes(name);
	}
	function diff(meta, other) {
		const add = {}, remove = {};
		if (meta === void 0) return {
			add: other,
			remove
		};
		if (meta.title !== other.title) add.title = other.title;
		[
			"meta",
			"link",
			"script",
			"htmlAttr",
			"bodyAttr"
		].forEach((type) => {
			const old = meta[type], cur = other[type];
			remove[type] = [];
			if (old === void 0 || old === null) {
				add[type] = cur;
				return;
			}
			add[type] = {};
			for (const key in old) if (!Object.hasOwn(cur, key)) remove[type].push(key);
			for (const key in cur) if (!Object.hasOwn(old, key)) add[type][key] = cur[key];
			else if (changed(old[key], cur[key])) {
				remove[type].push(key);
				add[type][key] = cur[key];
			}
		});
		return {
			add,
			remove
		};
	}
	function apply({ add, remove }) {
		if (add.title) document.title = add.title;
		if (Object.keys(remove).length !== 0) {
			[
				"meta",
				"link",
				"script"
			].forEach((type) => {
				remove[type].forEach((name) => {
					document.head.querySelector(`${type}[data-qmeta="${name}"]`).remove();
				});
			});
			remove.htmlAttr.filter(htmlFilter).forEach((name) => {
				document.documentElement.removeAttribute(name);
			});
			remove.bodyAttr.filter(bodyFilter).forEach((name) => {
				document.body.removeAttribute(name);
			});
		}
		[
			"meta",
			"link",
			"script"
		].forEach((type) => {
			const metaType = add[type];
			for (const name in metaType) {
				const tag = document.createElement(type);
				for (const att in metaType[name]) if (att !== "innerHTML") tag.setAttribute(att, metaType[name][att]);
				tag.dataset.qmeta = name;
				if (type === "script") tag.innerHTML = metaType[name].innerHTML || "";
				document.head.append(tag);
			}
		});
		Object.keys(add.htmlAttr).filter(htmlFilter).forEach((name) => {
			document.documentElement.setAttribute(name, add.htmlAttr[name] || "");
		});
		Object.keys(add.bodyAttr).filter(bodyFilter).forEach((name) => {
			document.body.setAttribute(name, add.bodyAttr[name] || "");
		});
	}
	function updateClientMeta() {
		updateId = null;
		const data = {
			title: "",
			titleTemplate: null,
			meta: {},
			link: {},
			script: {},
			htmlAttr: {},
			bodyAttr: {}
		};
		for (let i = 0; i < clientList.length; i++) {
			const { active, val } = clientList[i];
			if (active === true) extend(true, data, val);
		}
		normalize(data);
		apply(diff(currentClientMeta, data));
		currentClientMeta = data;
	}
	function planClientUpdate() {
		if (updateId !== null) clearTimeout(updateId);
		updateId = setTimeout(updateClientMeta, 50);
	}
	var Meta_default = { install(opts) {
		if (!this.__installed && isRuntimeSsrPreHydration.value) {
			currentClientMeta = window.__Q_META__;
			document.getElementById("qmeta-init").remove();
		}
	} };
	//#endregion
	//#region src/plugins/notify/Notify.js
	let uid = 0;
	const defaults = {};
	const groups = {};
	const notificationsList = {};
	const positionClass = {};
	const emptyRE = /^\s*$/;
	const notifRefs = [];
	const invalidTimeoutValues = [
		void 0,
		null,
		true,
		false,
		""
	];
	const positionList = [
		"top-left",
		"top-right",
		"bottom-left",
		"bottom-right",
		"top",
		"bottom",
		"left",
		"right",
		"center"
	];
	const badgePositions = [
		"top-left",
		"top-right",
		"bottom-left",
		"bottom-right"
	];
	const notifTypes = {
		positive: {
			icon: ($q) => $q.iconSet.type.positive,
			color: "positive"
		},
		negative: {
			icon: ($q) => $q.iconSet.type.negative,
			color: "negative"
		},
		warning: {
			icon: ($q) => $q.iconSet.type.warning,
			color: "warning",
			textColor: "dark"
		},
		info: {
			icon: ($q) => $q.iconSet.type.info,
			color: "info"
		},
		ongoing: {
			group: false,
			timeout: 0,
			spinner: true,
			color: "grey-8"
		}
	};
	function addNotification(config, $q, originalApi) {
		if (!config) return logError("parameter required");
		let Api;
		const notif = { textColor: "white" };
		if (!config.ignoreDefaults) Object.assign(notif, defaults);
		if (!isObject(config)) {
			if (notif.type) Object.assign(notif, notifTypes[notif.type]);
			config = { message: config };
		}
		Object.assign(notif, notifTypes[config.type || notif.type], config);
		if (typeof notif.icon === "function") notif.icon = notif.icon($q);
		if (!notif.spinner) notif.spinner = false;
		else notif.spinner = notif.spinner === true ? QSpinner_default : (0, vue.markRaw)(notif.spinner);
		notif.meta = {
			hasMedia: Boolean(notif.spinner || notif.icon || notif.avatar),
			hasText: hasContent(notif.message) || hasContent(notif.caption)
		};
		if (notif.position) {
			if (!positionList.includes(notif.position)) return logError("wrong position", config);
		} else notif.position = "bottom";
		if (invalidTimeoutValues.includes(notif.timeout)) notif.timeout = 5e3;
		else {
			const t = Number.parseFloat(notif.timeout);
			if (!Number.isFinite(t) || t < 0) return logError("wrong timeout", config);
			notif.timeout = t;
		}
		if (notif.timeout === 0) notif.progress = false;
		else if (notif.progress) {
			notif.meta.progressClass = "q-notification__progress" + (notif.progressClass ? ` ${notif.progressClass}` : "");
			notif.meta.progressStyle = { animationDuration: `${notif.timeout + 1e3}ms` };
		}
		const actions = [
			...Array.isArray(config.actions) ? config.actions : [],
			...!config.ignoreDefaults && Array.isArray(defaults.actions) ? defaults.actions : [],
			...Array.isArray(notifTypes[config.type]?.actions) ? notifTypes[config.type].actions : []
		];
		const { closeBtn } = notif;
		if (closeBtn) actions.push({ label: typeof closeBtn === "string" ? closeBtn : $q.lang.label.close });
		notif.actions = actions.map(({ handler, noDismiss, ...item }) => ({
			flat: true,
			...item,
			onClick: typeof handler === "function" ? () => {
				handler();
				if (!noDismiss) dismiss();
			} : () => {
				dismiss();
			}
		}));
		if (notif.multiLine === void 0) notif.multiLine = notif.actions.length > 1;
		Object.assign(notif.meta, {
			class: `q-notification row items-stretch q-notification--${notif.multiLine ? "multi-line" : "standard"}` + (notif.color !== void 0 ? ` bg-${notif.color}` : "") + (notif.textColor !== void 0 ? ` text-${notif.textColor}` : "") + (notif.classes !== void 0 ? ` ${notif.classes}` : ""),
			wrapperClass: "q-notification__wrapper col relative-position border-radius-inherit " + (notif.multiLine ? "column no-wrap justify-center" : "row items-center"),
			contentClass: "q-notification__content row items-center" + (notif.multiLine ? "" : " col"),
			leftClass: notif.meta.hasText ? "additional" : "single",
			attrs: {
				role: "alert",
				...notif.attrs
			}
		});
		if (notif.group === false) {
			notif.group = void 0;
			notif.meta.group = void 0;
		} else {
			if (notif.group === void 0 || notif.group === true) notif.group = [
				notif.message,
				notif.caption,
				notif.multiline,
				...notif.actions.map((props) => `${props.label}*${props.icon}`)
			].join("|");
			notif.meta.group = notif.group + "|" + notif.position;
		}
		if (notif.actions.length === 0) notif.actions = void 0;
		else notif.meta.actionsClass = "q-notification__actions row items-center " + (notif.multiLine ? "justify-end" : "col-auto") + (notif.meta.hasMedia ? " q-notification__actions--with-media" : "");
		if (originalApi !== void 0) {
			if (originalApi.notif.meta.timer) {
				clearTimeout(originalApi.notif.meta.timer);
				originalApi.notif.meta.timer = void 0;
			}
			notif.meta.uid = originalApi.notif.meta.uid;
			const index = notificationsList[notif.position].value.indexOf(originalApi.notif);
			notificationsList[notif.position].value[index] = notif;
		} else {
			const original = groups[notif.meta.group];
			if (original === void 0) {
				notif.meta.uid = uid++;
				notif.meta.badge = 1;
				if ([
					"left",
					"right",
					"center"
				].includes(notif.position)) notificationsList[notif.position].value.splice(Math.floor(notificationsList[notif.position].value.length / 2), 0, notif);
				else {
					const action = notif.position.includes("top") ? "unshift" : "push";
					notificationsList[notif.position].value[action](notif);
				}
				if (notif.group !== void 0) groups[notif.meta.group] = notif;
			} else {
				if (original.meta.timer) {
					clearTimeout(original.meta.timer);
					original.meta.timer = void 0;
				}
				if (notif.badgePosition !== void 0) {
					if (!badgePositions.includes(notif.badgePosition)) return logError("wrong badgePosition", config);
				} else notif.badgePosition = `top-${notif.position.includes("left") ? "right" : "left"}`;
				notif.meta.uid = original.meta.uid;
				notif.meta.badge = original.meta.badge + 1;
				notif.meta.badgeClass = `q-notification__badge q-notification__badge--${notif.badgePosition}` + (notif.badgeColor !== void 0 ? ` bg-${notif.badgeColor}` : "") + (notif.badgeTextColor !== void 0 ? ` text-${notif.badgeTextColor}` : "") + (notif.badgeClass ? ` ${notif.badgeClass}` : "");
				const index = notificationsList[notif.position].value.indexOf(original);
				notificationsList[notif.position].value[index] = groups[notif.meta.group] = notif;
			}
		}
		const dismiss = () => {
			removeNotification(notif);
			Api = void 0;
		};
		if (notif.timeout > 0) notif.meta.timer = setTimeout(() => {
			notif.meta.timer = void 0;
			dismiss();
		}, notif.timeout + 1e3);
		if (notif.group !== void 0) return (props) => {
			if (props !== void 0) logError("trying to update a grouped one which is forbidden", config);
			else dismiss();
		};
		Api = {
			dismiss,
			config,
			notif
		};
		if (originalApi !== void 0) {
			Object.assign(originalApi, Api);
			return;
		}
		return (props) => {
			if (Api !== void 0) if (props === void 0) Api.dismiss();
			else addNotification({
				...Api.config,
				...props,
				group: false,
				position: notif.position
			}, $q, Api);
		};
	}
	function removeNotification(notif) {
		if (notif.meta.timer) {
			clearTimeout(notif.meta.timer);
			notif.meta.timer = void 0;
		}
		const index = notificationsList[notif.position].value.indexOf(notif);
		if (index !== -1) {
			if (notif.group !== void 0) delete groups[notif.meta.group];
			const el = notifRefs[String(notif.meta.uid)];
			if (el) {
				const { width, height } = getComputedStyle(el);
				el.style.left = `${el.offsetLeft}px`;
				el.style.width = width;
				el.style.height = height;
			}
			notificationsList[notif.position].value.splice(index, 1);
			if (typeof notif.onDismiss === "function") notif.onDismiss();
		}
	}
	function hasContent(str) {
		return str !== void 0 && str !== null && !emptyRE.test(str);
	}
	function logError(error, config) {
		console.error(`Notify: ${error}`, config);
		return false;
	}
	function getComponent() {
		return createComponent({
			name: "QNotifications",
			devtools: { hide: true },
			setup() {
				return () => (0, vue.h)("div", { class: "q-notifications" }, positionList.map((pos) => (0, vue.h)(vue.TransitionGroup, {
					key: pos,
					class: positionClass[pos],
					tag: "div",
					name: `q-notification--${pos}`
				}, () => notificationsList[pos].value.map((notif) => {
					const meta = notif.meta;
					const mainChild = [];
					if (meta.hasMedia) {
						if (notif.spinner) mainChild.push((0, vue.h)(notif.spinner, {
							class: "q-notification__spinner q-notification__spinner--" + meta.leftClass,
							color: notif.spinnerColor,
							size: notif.spinnerSize
						}));
						else if (notif.icon) mainChild.push((0, vue.h)(QIcon_default, {
							class: "q-notification__icon q-notification__icon--" + meta.leftClass,
							name: notif.icon,
							color: notif.iconColor,
							size: notif.iconSize,
							role: "img"
						}));
						else if (notif.avatar) mainChild.push((0, vue.h)(QAvatar_default, { class: "q-notification__avatar q-notification__avatar--" + meta.leftClass }, () => (0, vue.h)("img", {
							src: notif.avatar,
							"aria-hidden": "true"
						})));
					}
					if (meta.hasText) {
						let msgChild;
						const msgData = { class: "q-notification__message col" };
						if (notif.html) msgData.innerHTML = notif.caption ? `<div>${notif.message}</div><div class="q-notification__caption">${notif.caption}</div>` : notif.message;
						else {
							const msgNode = [notif.message];
							msgChild = notif.caption ? [(0, vue.h)("div", msgNode), (0, vue.h)("div", { class: "q-notification__caption" }, [notif.caption])] : msgNode;
						}
						mainChild.push((0, vue.h)("div", msgData, msgChild));
					}
					const child = [(0, vue.h)("div", { class: meta.contentClass }, mainChild)];
					if (notif.progress) child.push((0, vue.h)("div", {
						key: `${meta.uid}|p|${meta.badge}`,
						class: meta.progressClass,
						style: meta.progressStyle
					}));
					if (notif.actions) child.push((0, vue.h)("div", { class: meta.actionsClass }, notif.actions.map((props) => (0, vue.h)(QBtn_default, props))));
					if (meta.badge > 1) child.push((0, vue.h)("div", {
						key: `${meta.uid}|${meta.badge}`,
						class: notif.meta.badgeClass,
						style: notif.badgeStyle
					}, [meta.badge]));
					return (0, vue.h)("div", {
						ref: (el) => {
							notifRefs[String(meta.uid)] = el;
						},
						key: meta.uid,
						class: meta.class,
						...meta.attrs
					}, [(0, vue.h)("div", { class: meta.wrapperClass }, child)]);
				}))));
			}
		});
	}
	var Notify_default = {
		setDefaults(opts) {
			if (isObject(opts)) Object.assign(defaults, opts);
		},
		registerType(typeName, typeOpts) {
			if (isObject(typeOpts)) notifTypes[typeName] = typeOpts;
		},
		install({ $q, parentApp }) {
			$q.notify = this.create = (opts) => addNotification(opts, $q);
			$q.notify.setDefaults = this.setDefaults;
			$q.notify.registerType = this.registerType;
			if ($q.config.notify !== void 0) this.setDefaults($q.config.notify);
			if (!this.__installed) {
				positionList.forEach((pos) => {
					notificationsList[pos] = (0, vue.ref)([]);
					const vert = pos === "left" || pos === "center" || pos === "right" ? "center" : pos.includes("top") ? "top" : "bottom", align = pos.includes("left") ? "start" : pos.includes("right") ? "end" : "center", classes = pos === "left" || pos === "right" ? `items-${pos === "left" ? "start" : "end"} justify-center` : pos === "center" ? "flex-center" : `items-${align}`;
					positionClass[pos] = `q-notifications__list q-notifications__list--${vert} fixed column no-wrap ${classes}`;
				});
				const el = createGlobalNode("q-notify");
				createChildApp(getComponent(), parentApp).mount(el);
			}
		}
	};
	//#endregion
	//#region src/plugins/storage/engine/web-storage.js
	function encode(value) {
		if (isDate(value)) return "__q_date|" + value.getTime();
		if (isRegexp(value)) return "__q_expr|" + value.source;
		if (typeof value === "number") return "__q_numb|" + value;
		if (typeof value === "boolean") return "__q_bool|" + (value ? "1" : "0");
		if (typeof value === "string") return "__q_strn|" + value;
		if (typeof value === "function") return "__q_strn|" + value.toString();
		if (value === Object(value)) return "__q_objt|" + JSON.stringify(value);
		return value;
	}
	const numberRE = /^-?\d+$/;
	function decode(value) {
		if (value.length < 9) return value;
		const type = value.slice(0, 8);
		const source = value.slice(9);
		switch (type) {
			case "__q_date": return new Date(numberRE.test(source) ? Number.parseInt(source, 10) : source);
			case "__q_expr": return new RegExp(source);
			case "__q_numb": return Number(source);
			case "__q_bool": return Boolean(source === "1");
			case "__q_strn": return String(source);
			case "__q_objt": return JSON.parse(source);
			default: return value;
		}
	}
	function getEmptyStorage() {
		return {
			has: () => false,
			hasItem: () => false,
			getLength: () => 0,
			getItem: () => null,
			getIndex: () => null,
			getKey: () => null,
			getAll: () => ({}),
			getAllKeys: () => [],
			set: noop,
			setItem: noop,
			remove: noop,
			removeItem: noop,
			clear: noop,
			isEmpty: () => true
		};
	}
	function getStorage(type) {
		const webStorage = window[type + "Storage"], get = (key) => {
			const item = webStorage.getItem(key);
			return item ? decode(item) : null;
		};
		const hasItem = (key) => webStorage.getItem(key) !== null;
		const setItem = (key, value) => {
			webStorage.setItem(key, encode(value));
		};
		const removeItem = (key) => {
			webStorage.removeItem(key);
		};
		return {
			has: hasItem,
			hasItem,
			getLength: () => webStorage.length,
			getItem: get,
			getIndex: (index) => index < webStorage.length ? get(webStorage.key(index)) : null,
			getKey: (index) => index < webStorage.length ? webStorage.key(index) : null,
			getAll: () => {
				let key;
				const result = {}, len = webStorage.length;
				for (let i = 0; i < len; i++) {
					key = webStorage.key(i);
					result[key] = get(key);
				}
				return result;
			},
			getAllKeys: () => {
				const result = [], len = webStorage.length;
				for (let i = 0; i < len; i++) result.push(webStorage.key(i));
				return result;
			},
			set: setItem,
			setItem,
			remove: removeItem,
			removeItem,
			clear: () => {
				webStorage.clear();
			},
			isEmpty: () => webStorage.length === 0
		};
	}
	//#endregion
	//#region src/plugins/storage/LocalStorage.js
	const storage$1 = !client.has.webStorage ? getEmptyStorage() : getStorage("local");
	const Plugin$1 = {
		install({ $q }) {
			$q.localStorage = storage$1;
		},
		...storage$1
	};
	//#endregion
	//#region src/plugins/storage/SessionStorage.js
	const storage = !client.has.webStorage ? getEmptyStorage() : getStorage("session");
	const Plugin = {
		install({ $q }) {
			$q.sessionStorage = storage;
		},
		...storage
	};
	//#endregion
	//#region src/plugins.js
	var plugins_exports = /* @__PURE__ */ __exportAll({
		AddressbarColor: () => AddressbarColor_default,
		AppFullscreen: () => Plugin$6,
		AppVisibility: () => Plugin$5,
		BottomSheet: () => BottomSheet_default,
		Cookies: () => Plugin$4,
		Dark: () => Plugin$9,
		Dialog: () => Dialog_default,
		IconSet: () => Plugin$7,
		Lang: () => Plugin$8,
		Loading: () => Plugin$3,
		LoadingBar: () => Plugin$2,
		LocalStorage: () => Plugin$1,
		Meta: () => Meta_default,
		Notify: () => Notify_default,
		Platform: () => Platform,
		Screen: () => Screen_default,
		SessionStorage: () => Plugin
	});
	//#endregion
	//#region src/utils/copy-to-clipboard/copy-to-clipboard.js
	function fallback(text) {
		const area = document.createElement("textarea");
		area.value = text;
		area.contentEditable = "true";
		area.style.position = "fixed";
		const fn = () => {};
		addFocusout(fn);
		document.body.append(area);
		area.focus();
		area.select();
		const res = document.execCommand("copy");
		area.remove();
		removeFocusout(fn);
		return res;
	}
	function copyToClipboard(text) {
		if (navigator.clipboard) return navigator.clipboard.writeText(text);
		const res = fallback(text);
		return res ? Promise.resolve(true) : Promise.reject(res);
	}
	//#endregion
	//#region src/utils/create-meta-mixin/create-meta-mixin.js
	function createMetaMixin(metaOptions) {
		const mixin = {
			activated() {
				this.__qMeta.active = true;
				planClientUpdate();
			},
			deactivated() {
				this.__qMeta.active = false;
				planClientUpdate();
			},
			unmounted() {
				clientList.splice(clientList.indexOf(this.__qMeta), 1);
				planClientUpdate();
				this.__qMeta = void 0;
			}
		};
		if (typeof metaOptions === "function") Object.assign(mixin, {
			computed: { __qMetaOptions() {
				return metaOptions.call(this) || {};
			} },
			watch: { __qMetaOptions(val) {
				this.__qMeta.val = val;
				if (this.__qMeta.active) planClientUpdate();
			} },
			created() {
				this.__qMeta = {
					active: true,
					val: this.__qMetaOptions
				};
				clientList.push(this.__qMeta);
				planClientUpdate();
			}
		});
		else mixin.created = function created() {
			this.__qMeta = {
				active: true,
				val: metaOptions
			};
			clientList.push(this.__qMeta);
			planClientUpdate();
		};
		return mixin;
	}
	//#endregion
	//#region src/utils/EventBus/EventBus.js
	/**
	* Forked from tiny-emitter
	* Copyright (c) 2017 Scott Corgan
	*/
	var EventBus = class {
		constructor() {
			this.__stack = {};
		}
		on(name, callback, ctx) {
			(this.__stack[name] ||= []).push({
				fn: callback,
				ctx
			});
			return this;
		}
		once(name, callback, ctx) {
			const listener = (...args) => {
				this.off(name, listener);
				callback.apply(ctx, args);
			};
			listener.__callback = callback;
			return this.on(name, listener, ctx);
		}
		emit(name, ...args) {
			const list = this.__stack[name];
			if (list !== void 0) list.forEach((entry) => {
				entry.fn.apply(entry.ctx, args);
			});
			return this;
		}
		off(name, callback) {
			const list = this.__stack[name];
			if (list === void 0) return this;
			if (callback === void 0) {
				delete this.__stack[name];
				return this;
			}
			const liveEvents = list.filter((entry) => entry.fn !== callback && entry.fn.__callback !== callback);
			if (liveEvents.length !== 0) this.__stack[name] = liveEvents;
			else delete this.__stack[name];
			return this;
		}
	};
	//#endregion
	//#region src/utils/export-file/export-file.js
	function clean(link) {
		setTimeout(() => {
			window.URL.revokeObjectURL(link.href);
		}, 1e4);
		link.remove();
	}
	/**
	* Forces browser to download file with specified content
	*
	* @param {*} fileName - String
	* @param {*} rawData - String | ArrayBuffer | ArrayBufferView | Blob
	* @param {*} opts - String (mimeType) or Object
	*                   Object form: { mimeType?: String, byteOrderMark?: String | Uint8Array, encoding?: String }
	* @returns Boolean | Error
	*
	* mimeType       - Examples: 'application/octect-stream' (default), 'text/plain', 'application/json',
	*                  'text/plain;charset=UTF-8', 'video/mp4', 'image/png', 'application/pdf'
	*                  https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types
	*
	* byteOrderMark  - (BOM) Example: '\uFEFF'
	*                  https://en.wikipedia.org/wiki/Byte_order_mark
	*
	* encoding       - Performs a TextEncoder.encode() over the rawData;
	*                  Example: 'windows-1252' (ANSI, a subset of ISO-8859-1)
	*                  https://developer.mozilla.org/en-US/docs/Web/API/TextEncoder
	*/
	function exportFile(fileName, rawData, opts = {}) {
		const { mimeType, byteOrderMark, encoding } = typeof opts === "string" ? { mimeType: opts } : opts;
		const data = encoding !== void 0 ? new TextEncoder(encoding).encode([rawData]) : rawData;
		const blob = new Blob(byteOrderMark !== void 0 ? [byteOrderMark, data] : [data], { type: mimeType || "application/octet-stream" });
		const link = document.createElement("a");
		link.href = window.URL.createObjectURL(blob);
		link.setAttribute("download", fileName);
		if (link.download === void 0) link.setAttribute("target", "_blank");
		link.classList.add("hidden");
		link.style.position = "fixed";
		document.body.append(link);
		try {
			link.click();
			clean(link);
			return true;
		} catch (err) {
			clean(link);
			return err;
		}
	}
	//#endregion
	//#region src/utils/open-url/open-url.js
	function parseFeatures(winFeatures) {
		const cfg = {
			noopener: true,
			...winFeatures
		};
		const feat = [];
		for (const key in cfg) {
			const value = cfg[key];
			if (value === true) feat.push(key);
			else if (isNumber(value) || typeof value === "string" && value !== "") feat.push(key + "=" + value);
		}
		return feat.join(",");
	}
	function openWindow(url, reject, windowFeatures) {
		let open = window.open;
		if (Platform.is.cordova) {
			if (cordova?.InAppBrowser?.open !== void 0) open = cordova.InAppBrowser.open;
			else if (navigator?.app !== void 0) return navigator.app.loadUrl(url, { openExternal: true });
		}
		const cfg = {
			noopener: true,
			...windowFeatures
		};
		const hasNoopener = cfg.noopener || cfg.noreferrer;
		const win = open(url, "_blank", parseFeatures(windowFeatures));
		if (win) {
			if (Platform.is.desktop) win.focus();
			return win;
		} else if (!hasNoopener) reject?.();
	}
	function openUrl(url, reject, windowFeatures) {
		if (Platform.is.ios && window.SafariViewController !== void 0) {
			window.SafariViewController.isAvailable((available) => {
				if (available) window.SafariViewController.show({ url }, noop, reject);
				else openWindow(url, reject, windowFeatures);
			});
			return;
		}
		return openWindow(url, reject, windowFeatures);
	}
	//#endregion
	//#region src/utils/run-sequential-promises/run-sequential-promises.js
	function parsePromises(sequentialPromises) {
		if (Array.isArray(sequentialPromises)) {
			const totalJobs = sequentialPromises.length;
			return {
				isList: true,
				totalJobs,
				resultAggregator: Array(totalJobs).fill(null)
			};
		}
		const resultKeys = Object.keys(sequentialPromises);
		const resultAggregator = resultKeys.reduce((acc, key) => {
			acc[key] = null;
			return acc;
		}, {});
		return {
			isList: false,
			totalJobs: resultKeys.length,
			resultAggregator,
			resultKeys
		};
	}
	/**
	* Run a list of Promises sequentially, optionally on multiple threads.
	*
	* @param {*} sequentialPromises - Array of Functions or Object with Functions as values
	*                          Array of Function form: [ (resultAggregator: Array) => Promise<any>, ... ]
	*                          Object form: { [key: string]: (resultAggregator: object) => Promise<any>, ... }
	* @param {*} opts - Optional options Object
	*                   Object form: { threadsNumber?: number, abortOnFail?: boolean }
	*                   Default: { threadsNumber: 1, abortOnFail: true }
	*                   When configuring threadsNumber AND using http requests, be
	*                       aware of the maximum threads that the hosting browser
	*                       supports (usually 5); any number of threads above that
	*                       won't add any real benefits
	* @returns Promise<Array<Object> | Object>
	*    With opts.abortOnFail set to true (which is default):
	*        When sequentialPromises param is Array:
	*          The Promise resolves with an Array of Objects of the following form:
	*             [ { key: number, status: 'fulfilled', value: any }, ... ]
	*          The Promise rejects with an Object of the following form:
	*             { key: number, status: 'rejected', reason: Error, resultAggregator: array }
	*        When sequentialPromises param is Object:
	*          The Promise resolves with an Object of the following form:
	*             { [key: string]: { key: string, status: 'fulfilled', value: any }, ... }
	*          The Promise rejects with an Object of the following form:
	*             { key: string, status: 'rejected', reason: Error, resultAggregator: object }
	*    With opts.abortOnFail set to false:
	*       The Promise is never rejected (no catch() needed)
	*       The Promise resolves with:
	*          An Array of Objects (when sequentialPromises param is also an Array) of the following form:
	*             [ { key: number, status: 'fulfilled', value: any } | { status: 'rejected', reason: Error }, ... ]
	*          An Object (when sequentialPromises param is also an Object) of the following form:
	*             { [key: string]: { key: string, status: 'fulfilled', value: any } | { key: string, status: 'rejected', reason: Error }, ... }
	*/
	function runSequentialPromises(sequentialPromises, { threadsNumber = 1, abortOnFail = true } = {}) {
		let jobIndex = -1, hasAborted = false;
		const { isList, totalJobs, resultAggregator, resultKeys } = parsePromises(sequentialPromises);
		if (totalJobs === 0) return Promise.resolve(resultAggregator);
		const maxJobIndex = totalJobs - 1;
		const runNextPromise = (threadCtx) => {
			if (hasAborted || jobIndex >= maxJobIndex) return threadCtx.resolve();
			const currentJobIndex = ++jobIndex;
			const key = isList ? currentJobIndex : resultKeys[currentJobIndex];
			Promise.resolve().then(() => sequentialPromises[key](resultAggregator)).then((value) => {
				if (!hasAborted) resultAggregator[key] = {
					key,
					status: "fulfilled",
					value
				};
			}).catch((err) => {
				if (hasAborted) return;
				const result = {
					key,
					status: "rejected",
					reason: err
				};
				resultAggregator[key] = result;
				if (abortOnFail) {
					hasAborted = true;
					threadCtx.reject({
						...result,
						resultAggregator
					});
				}
			}).finally(() => {
				if (!hasAborted) runNextPromise(threadCtx);
			});
		};
		const concurrencyLimit = Math.min(totalJobs, Math.max(1, threadsNumber));
		const threads = Array.from({ length: concurrencyLimit }, () => {
			const threadCtx = Promise.withResolvers();
			runNextPromise(threadCtx);
			return threadCtx.promise;
		});
		return Promise.all(threads).then(() => resultAggregator);
	}
	//#endregion
	//#region src/utils.js
	var utils_exports = /* @__PURE__ */ __exportAll({
		EventBus: () => EventBus,
		clone: () => cloneDeep,
		colors: () => colors_default,
		copyToClipboard: () => copyToClipboard,
		createMetaMixin: () => createMetaMixin,
		createUploaderComponent: () => createUploaderComponent,
		date: () => date_default,
		debounce: () => debounce,
		dom: () => dom_default,
		event: () => event_default,
		exportFile: () => exportFile,
		extend: () => extend,
		format: () => format_default,
		frameDebounce: () => frameDebounce,
		getCssVar: () => getCssVar,
		is: () => is_default,
		morph: () => morph,
		noop: () => noop,
		openURL: () => openUrl,
		patterns: () => patterns_default,
		runSequentialPromises: () => runSequentialPromises,
		scroll: () => scroll_default,
		setCssVar: () => setCssVar,
		throttle: () => throttle,
		uid: () => uid_default
	});
	//#endregion
	//#region src/composables/use-dialog-plugin-component/use-dialog-plugin-component.js
	function useDialogPluginComponent() {
		const { emit, proxy } = (0, vue.getCurrentInstance)();
		const dialogRef = (0, vue.ref)(null);
		function show() {
			dialogRef.value.show();
		}
		function hide() {
			dialogRef.value.hide();
		}
		function onDialogOK(payload) {
			emit("ok", payload);
			hide();
		}
		function onDialogHide() {
			emit("hide");
		}
		Object.assign(proxy, {
			show,
			hide
		});
		return {
			dialogRef,
			onDialogHide,
			onDialogOK,
			onDialogCancel: hide
		};
	}
	const emits = ["ok", "hide"];
	useDialogPluginComponent.emits = emits;
	useDialogPluginComponent.emitsObject = getEmitsObject(emits);
	//#endregion
	//#region src/composables/use-meta/use-meta.js
	function useMeta(metaOptions) {
		{
			const meta = { active: true };
			if (typeof metaOptions === "function") {
				const content = (0, vue.computed)(metaOptions);
				meta.val = content.value;
				(0, vue.watch)(content, (val) => {
					meta.val = val;
					if (meta.active) planClientUpdate();
				});
			} else meta.val = metaOptions;
			clientList.push(meta);
			planClientUpdate();
			(0, vue.onActivated)(() => {
				meta.active = true;
				planClientUpdate();
			});
			(0, vue.onDeactivated)(() => {
				meta.active = false;
				planClientUpdate();
			});
			(0, vue.onUnmounted)(() => {
				clientList.splice(clientList.indexOf(meta), 1);
				planClientUpdate();
			});
		}
	}
	//#endregion
	//#region src/composables/use-quasar/use-quasar.js
	/**
	* Returns the $q instance.
	* Equivalent to `this.$q` inside templates.
	*/
	function useQuasar() {
		return (0, vue.inject)("_q_");
	}
	//#endregion
	//#region src/composables/use-interval/use-interval.js
	function useInterval() {
		let timer = null;
		const vm = (0, vue.getCurrentInstance)();
		function removeInterval() {
			if (timer !== null) {
				clearInterval(timer);
				timer = null;
			}
		}
		(0, vue.onDeactivated)(removeInterval);
		(0, vue.onBeforeUnmount)(removeInterval);
		return {
			removeInterval,
			registerInterval(fn, delay) {
				removeInterval();
				if (!vmIsDestroyed(vm)) timer = setInterval(fn, delay);
			}
		};
	}
	//#endregion
	//#region src/composables.js
	var composables_exports = /* @__PURE__ */ __exportAll({
		useDialogPluginComponent: () => useDialogPluginComponent,
		useFormChild: () => useFormChild,
		useHydration: () => useHydration,
		useId: () => useId,
		useInterval: () => useInterval,
		useMeta: () => useMeta,
		useQuasar: () => useQuasar,
		useRenderCache: () => useRenderCache,
		useSplitAttrs: () => useSplitAttrs,
		useTick: () => useTick,
		useTimeout: () => useTimeout
	});
	//#endregion
	//#region src/index.umd.js
	/**
	* UMD entry-point
	*/
	if (window.Vue === void 0) console.error("[ Quasar ] Vue is required to run. Please add a script tag for it before loading Quasar.");
	window.Quasar = {
		version: "2.22.0",
		install(app, opts) {
			install_quasar_default(app, {
				components: components_exports,
				directives: directives_exports,
				plugins: plugins_exports,
				...opts
			});
		},
		lang: Plugin$8,
		iconSet: Plugin$7,
		...components_exports,
		...directives_exports,
		...plugins_exports,
		...composables_exports,
		...utils_exports
	};
	//#endregion
})(window.Vue);
