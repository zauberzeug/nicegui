export default {
    template: '<slot></slot>',
    mounted() {
        let router = this;

        function validate_path(path) {
            let href = path.split('?')[0].split('#')[0]
            // check if the link ends with / and remove it
            if (href.endsWith('/')) href = href.slice(0, -1);
            // for all valid path masks
            for (let mask of router.valid_path_masks) {
                // apply filename matching with * and ? wildcards
                let regex = new RegExp(mask.replace(/\?/g, '.').replace(/\*/g, '.*'));
                if (!regex.test(href)) continue;
                return true;
            }
            return false;
        }

        const connectInterval = setInterval(async () => {
            if (window.socket.id === undefined) return;
            let target = window.location.pathname;
            if (window.location.hash !== '') target += window.location.hash;
            this.$emit('open', target);
            clearInterval(connectInterval);
        }, 10);
        document.addEventListener('click', function (e) {
            // Check if the clicked element is a link
            if (e.target.tagName === 'A') {
                let href = e.target.getAttribute('href'); // Get the link's href value
                // remove query and anchor
                if (validate_path(href)) {
                    e.preventDefault(); // Prevent the default link behavior
                    if (router.use_browser_history) window.history.pushState({page: href}, '', href);
                    // TODO BUG: Path is valid for the root router and the sub router for /.
                    // Only one of both is allowed to push the state, otherwise the browser history is broken.
                    router.$emit('open', href);
                }
            }
        });
        window.addEventListener('popstate', (event) => {
            let new_page = window.location.pathname;
            if (validate_path(new_page)) {
                this.$emit('open', new_page);
            }
        });
    },
    props: {
        valid_path_masks: [],
        use_browser_history: {type: Boolean, default: true}
    },
};
