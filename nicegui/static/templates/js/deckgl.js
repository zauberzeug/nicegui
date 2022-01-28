// {* raw *}

// Work in progress. Does not work well for all decks
// Use the iframejp component instead for now

var cached_deckgl_def = {};

Vue.component('deckgl', {
    template:
        `<div  v-bind:id="jp_props.id" :class="jp_props.classes"  :style="jp_props.style"  ></div>`,
    data: function () {
        return {
            deck_def: {},
            deckInstance: null
        }
    },
    methods: {
        deck_create() {
            const tooltip = true;
            const customLibraries = null;
            this.deck_def = this.$props.jp_props.deck;
            jsonInput = JSON.parse(this.deck_def);
            this.$nextTick(function () {
                this.deckInstance = createDeck({
                    mapboxApiKey: this.$props.jp_props.mapbox_key,
                    container: document.getElementById(this.$props.jp_props.id.toString()),
                    jsonInput,
                    tooltip,
                    customLibraries
                });
            });
        }
    },
    mounted() {
        this.deck_create();
    },
    updated() {
        updateDeck('', this.deckInstance);
        updateDeck(this.$props.jp_props.deck, this.deckInstance);
        this.deckInstance.redraw(true);
        this.deck_def = this.$props.jp_props.deck;
    },
    props: {
        jp_props: Object
    }
});

// {* endraw *}