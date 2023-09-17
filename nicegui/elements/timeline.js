export default {
    template: `
    <div class="q-px-lg q-py-md">
      <q-timeline :color="timelinecolor">
        <q-timeline-entry v-for="item in items" :key="item.id" 
                            :title="item.title"
                            :subtitle="item.subtitle"
                            :icon="item.icon">
              <div v-if="item.body">
                {{item.body}}
              </div>
            </q-timeline-entry>
          </q-timeline>
        </div>`,
    props: {
      initialItems: Array,
      timelinecolor: String,
    },
    data() {
      return {
        items: []
      };
    },
    
    mounted() {
      if (this.initialItems && this.initialItems.length > 0) {
        this.items = this.initialItems;
      }
    },
    };
  