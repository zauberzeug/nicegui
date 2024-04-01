export default {
    template: "<div><slot></slot></div>",
    mounted() {
        let router = this;
        document.addEventListener('click', function (e) {
            // Check if the clicked element is a link
            if (e.target.tagName === 'A') {
                const href = e.target.getAttribute('href'); // Get the link's href value
                if (href.startsWith('/')) {
                    e.preventDefault(); // Prevent the default link behavior
                    window.history.pushState({page: href}, "", href);
                    router.$emit("open", href);
                }
            }
        });
        window.addEventListener("popstate", (event) => {
            if (event.state?.page) {
                this.$emit("open", event.state.page);
            }
        });
        const connectInterval = setInterval(async () => {
            if (window.socket.id === undefined) return;
            this.$emit("open", window.location.pathname);
            clearInterval(connectInterval);
        }, 10);
    },
    props: {},
};
