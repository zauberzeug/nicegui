import mermaid from 'mermaid';
export default {
  template: `<div class="mermaid">{{ content }}</div>`,
  mounted() {
    mermaid.initialize({ startOnLoad: false, theme: 'default' });
    this.update()
  },
  methods: {
    async update(content) {
      await mermaid.run({querySelector: '.mermaid'})
    },
  },
  props: {
    content: String,
  },
};
