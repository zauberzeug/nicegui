<template>
  <div class="q-pa-md relative">
    <q-input input-class="text-white" v-model="query" color="white" placeholder="Search ..." />
    <q-list class="bg-primary absolute text-white w-full z-50 max-h-[200px] overflow-y-auto">
      <q-item clickable v-for="result in results" :key="result.item.title" @click="goTo(result.item.url)">
        <q-item-section>
          <q-item-label>{{ result.item.title }}</q-item-label>
        </q-item-section>
      </q-item>
    </q-list>
  </div>
</template>

<script>
export default {
  data() {
    return {
      query: "",
      results: [],
      searchData: [],
      fuse: null,
    };
  },

  watch: {
    query() {
      this.search();
    },
  },

  async created() {
    let response = await fetch("/static/search_data.json");
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    this.searchData = await response.json();
    let options = {
      keys: ["title", "content"],
    };
    this.fuse = new Fuse(this.searchData, options);
  },

  methods: {
    search() {
      this.results = this.fuse.search(this.query);
    },
    goTo(url) {
      window.location.href = url;
    },
  },
};
</script>
