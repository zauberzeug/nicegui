<template>
  <div class="q-pa-md relative">
    <q-input v-model="query" dense dark standout>
      <template v-slot:append>
        <q-icon v-if="query === ''" name="search" />
        <q-icon v-else name="clear" class="cursor-pointer" @click="query = ''" />
      </template>
    </q-input>
    <q-list class="bg-primary rounded mt-2 w-64 absolute text-white z-50 max-h-[200px] overflow-y-auto">
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
      keys: [
        { name: "title", weight: 0.7 },
        { name: "content", weight: 0.3 },
      ],
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
