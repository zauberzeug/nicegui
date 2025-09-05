export default {
    template: `<div class="nicegui-log" ref="logContainer"><slot></slot></div>`,
    data() {
        return {
            shouldScroll: true,
        };
    },
    beforeUpdate() {
        const container = this.$refs.logContainer;
        if (container) {
            this.shouldScroll = container.scrollTop + container.clientHeight >= container.scrollHeight;
        }
    },
    updated() {
        const container = this.$refs.logContainer;
        if (container && this.shouldScroll) {
            container.scrollTop = container.scrollHeight;
        }
    }
};
