export default {
    template: '<slot></slot>',
    mounted() {
        if (this._debug) console.log('Mounted RouterFrame ' + this.base_path);

        let router = this;

        function validate_path(path) {
            let href = path.split('?')[0].split('#')[0]
            // check if the link ends with / and remove it
            if (href.endsWith('/')) href = href.slice(0, -1);
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
            for (let frame of router.child_frame_paths) {
                if (path.startsWith(frame + '/') || (path === frame)) {
                    console.log(path + ' handled by child RouterFrame ' + frame + ', skipping...');
                    return true;
                }
            }
            return false;
        }

        const connectInterval = setInterval(async () => {
            if (window.socket.id === undefined) return;
            let target = router.initial_path
            this.$emit('open', target);
            clearInterval(connectInterval);
        }, 10);

        this.clickEventListener = function (e) {
            // Check if the clicked element is a link
            if (e.target.tagName === 'A') {
                let href = e.target.getAttribute('href'); // Get the link's href value
                if (href === "#") {
                    e.preventDefault();
                    return;
                }
                // remove query and anchor
                if (validate_path(href)) {
                    e.preventDefault(); // Prevent the default link behavior
                    if (!is_handled_by_child_frame(href)) {
                        if (router.use_browser_history) {
                            window.history.pushState({page: href}, '', href);
                            if (router._debug) console.log('RouterFrame pushing state ' + href + ' by ' + router.base_path);
                        }
                        router.$emit('open', href);
                        if (router._debug) console.log('Opening ' + href + ' by ' + router.base_path);
                    }
                }
            }
        };
        this.popstateEventListener = function (event) {
            let href = window.location.pathname;
            if (validate_path(href) && !is_handled_by_child_frame(href)) {
                router.$emit('open', href);
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
        initial_path: {type: String},
        included_path_masks: [],
        excluded_path_masks: [],
        use_browser_history: {type: Boolean, default: true},
        child_frame_paths: [],
        _debug: {type: Boolean, default: true},
    },
};
