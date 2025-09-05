export default {
    template: `<div><slot></slot></div>`,
    data() {
        return {
            shouldScroll: true,
        };
    },
    beforeUpdate() {
        if (this.$el) {
            this.shouldScroll = this.$el.scrollTop + this.$el.clientHeight >= this.$el.scrollHeight;
        }
    },
    updated() {
        if (this.$el && this.shouldScroll) {
            this.$el.scrollTop = this.$el.scrollHeight;
        }
    }
};
