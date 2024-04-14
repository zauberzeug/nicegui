export default {
    template: '<slot></slot>',
    mounted() {
        let router = this;
        document.addEventListener('click', function (e) {
            // Check if the clicked element is a link
            if (e.target.tagName === 'A') {
                let href = e.target.getAttribute('href'); // Get the link's href value
                // remove query and anchor
                const org_href = href;
                href = href.split('?')[0].split('#')[0]
                // check if the link ends with / and remove it
                if (href.endsWith('/')) href = href.slice(0, -1);
                // for all valid path masks
                for (let mask of router.valid_path_masks) {
                    // apply filename matching with * and ? wildcards
                    let regex = new RegExp(mask.replace(/\?/g, '.').replace(/\*/g, '.*'));
                    if (!regex.test(href)) continue;
                    e.preventDefault(); // Prevent the default link behavior
                    if (router.use_browser_history) window.history.pushState({page: org_href}, '', org_href);
                    router.$emit('open', org_href);
                    return
                }
            }
        });
        window.addEventListener('popstate', (event) => {
            let new_page = window.location.pathname;
            this.$emit('open', new_page);
        });
        const connectInterval = setInterval(async () => {
            if (window.socket.id === undefined) return;
            let target = window.location.pathname;
            if (window.location.hash !== '') target += window.location.hash;
            this.$emit('open', target);
            clearInterval(connectInterval);
        }, 10);
    },
    props: {
        valid_path_masks: [],
        use_browser_history: {type: Boolean, default: true}
    },
};
