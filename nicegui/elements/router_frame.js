export default {
    template: '<slot></slot>',
    mounted() {
        if (this._debug) console.log('Mounted RouterFrame ' + this.base_path);

        let router = this;

        function normalize_path(path) {
            let href = path.split('?')[0].split('#')[0]
            if (href.endsWith('/')) href = href.slice(0, -1);
            return href;
        }

        function validate_path(path) {
            let href = normalize_path(path);
            // for all excluded path masks
            for (let mask of router.excluded_path_masks) {
                // apply filename matching with * and ? wildcards
                let regex = new RegExp(mask.replace(/\?/g, '.').replace(/\*/g, '.*'));
                if (!regex.test(href)) continue;
                return false;
            }
            // for all included path masks
            for (let mask of router.included_path_masks) {
                // apply filename matching with * and ? wildcards
                let regex = new RegExp(mask.replace(/\?/g, '.').replace(/\*/g, '.*'));
                if (!regex.test(href)) continue;
                return true;
            }
            return false;
        }

        function is_handled_by_child_frame(path) {
            // check child frames
            let href = normalize_path(path);
            for (let frame of router.child_frame_paths) {
                if (path.startsWith(frame + '/') || (href === frame)) {
                    if (router._debug) console.log(href + ' handled by child RouterFrame ' + frame + ', skipping...');
                    return true;
                }
            }
            return false;
        }

        this.clickEventListener = function (e) {
            // Check if the clicked element is a link
            // Use closest to find the nearest parent <a> tag
            let link = e.target.closest('a');

            // ignore link if its opened in a new tab
            if (link && link.getAttribute('target') === '_blank') return;

            // If there's no <a> tag, or the <a> tag has no href attribute, do nothing
            if (!link || !link.hasAttribute('href')) return;
            let href = link.getAttribute('href');
            if (href === '#') {
                e.preventDefault();
                return;
            }
            // remove query and anchor
            if (validate_path(href)) {
                e.preventDefault(); // Prevent the default link behavior
                if (!is_handled_by_child_frame(href)) {
                    router.$emit('open', href, true);
                    if (router._debug) console.log('Opening ' + href + ' by ' + router.base_path);
                }
            }
        };
        this.popstateEventListener = function (event) {
            let href = window.location.pathname + window.location.search;
            event.preventDefault();
            if (window.location.hash) {
                return;
            }
            if (validate_path(href) && !is_handled_by_child_frame(href)) {
                router.$emit('open', href, false);
                if (router._debug) console.log('Pop opening ' + href + ' by ' + router.base_path);
            }
        };

        document.addEventListener('click', this.clickEventListener);
        window.addEventListener('popstate', this.popstateEventListener);
    },
    unmounted() {
        document.removeEventListener('click', this.clickEventListener);
        window.removeEventListener('popstate', this.popstateEventListener);
        if (this._debug) console.log('Unmounted RouterFrame ' + this.base_path);
    },
    props: {
        base_path: {type: String},
        target_url: {type: String},
        included_path_masks: [],
        excluded_path_masks: [],
        use_browser_history: {type: Boolean, default: true},
        child_frame_paths: [],
        _debug: {type: Boolean, default: false},
    },
};
