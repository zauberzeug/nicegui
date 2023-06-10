<template>
  <div class="q-pa-md relative">
    <q-input
      v-model="query"
      dense
      dark
      standout
      :input-class="inputClass"
      @focus="focused = true"
      @blur="focused = false"
    >
      <template v-slot:append>
        <q-icon v-if="query === ''" name="search" :class="{ 'text-primary': focused }" />
        <q-icon v-else name="clear" class="cursor-pointer" @click="query = ''" :class="{ 'text-primary': focused }" />
      </template>
    </q-input>
    <q-list class="bg-primary shadow-lg rounded mt-5 w-64 absolute text-white z-50 max-h-[200px] overflow-y-auto">
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
      focused: false,
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

  computed: {
    inputClass() {
      return this.focused ? "text-primary" : "";
    },
  },

  async created() {
    let response = await fetch("/static/search_index.json");
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    this.searchData = await response.json();
    let options = {
      keys: [
        { name: "title", weight: 0.7 },
        { name: "content", weight: 0.3 },
      ],
      tokenize: true, // each word is ranked individually
      threshold: 0.3,
      location: 0,
      distance: 10000,
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
