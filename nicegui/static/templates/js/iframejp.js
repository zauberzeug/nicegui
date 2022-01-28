// {* raw *}


Vue.component('iframejp', {
    template:
        `<div v-bind:id="jp_props.id" :class="jp_props.classes"  :style="jp_props.style + '; position: relative'">
            <iframe  v-bind:id="'frame0'+jp_props.id"  style="width: 100%; height: 100%; position: absolute; top: 0; left: 0;" ></iframe>
            <iframe  v-bind:id="'frame1'+jp_props.id"  style="visibility: hidden;: none; width: 100%; height: 100%; position: absolute; top: 0; left: 0;"></iframe>
        </div>`,
    data: function () {
        return {
            src_data_current: '',
            active_frame: 0,
            inactive_frame: 1
        }
    },
    methods: {
        inject_deck() {
            const el_active = document.getElementById('frame' + this.active_frame.toString() + this.$props.jp_props.id.toString());
            const el_inactive = document.getElementById('frame' + this.inactive_frame.toString() + this.$props.jp_props.id.toString());
            const src_data_new = decodeURIComponent(this.$props.jp_props.attrs.srcdoc);
            const view_delay = this.$props.jp_props.view_delay;
            const transition_duration = this.$props.jp_props.transition_duration;
            el_active.onload = null;
            el_inactive.onload = null;

            if (src_data_new != this.src_data_current) {
                this.src_data_current = src_data_new;

                el_active.onload = async function (event) {
                    // Sleep this function for view_delay milliseconds
                   // await new Promise(r => setTimeout(r, view_delay));

                    el_active.style.transition = `width ${transition_duration}s ease-out`;
                    el_inactive.style.transition = `width ${transition_duration}s ease-out`;

                    el_active.style.visibility = 'visible';

                    el_active.style.width = '100%';
                    el_inactive.style.width = '0%';
                    await new Promise(r => setTimeout(r, transition_duration * 1000));
                    el_inactive.style.visibility = 'hidden';
                };

                el_active.setAttribute("srcdoc", this.src_data_current);

                this.active_frame = (this.active_frame + 1) % 2;
                this.inactive_frame = (this.inactive_frame + 1) % 2;

            }

        }
    },
    mounted() {
        this.inject_deck();
    },
    updated() {
        this.inject_deck();
    },
    props: {
        jp_props: Object
    }
});

// {* endraw *}