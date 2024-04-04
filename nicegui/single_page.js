export default {
    template: "<slot></slot>",
    mounted() {
        let router = this;
        document.addEventListener('click', function (e) {
            // Check if the clicked element is a link
            if (e.target.tagName === 'A') {
                const href = e.target.getAttribute('href'); // Get the link's href value
                if (href.startsWith(router.base_path)) { // internal links only
                    e.preventDefault(); // Prevent the default link behavior
                    window.history.pushState({page: href}, '', href);
                    router.$emit("open", href, false);
                }
            }
        });
        window.addEventListener("popstate", (event) => {
            let new_page = window.location.pathname;
            this.$emit("open", new_page, false);
        });
        const connectInterval = setInterval(async () => {
            if (window.socket.id === undefined) return;
            this.$emit("open", window.location.pathname, false);
            clearInterval(connectInterval);
        }, 10);
    },
    props: {
        base_path: String
    },
};
