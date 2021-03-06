<template>
  <div v-if="loaded" class="portfolio">
    <div>
      <Search @search="addSymbol($event)" v-bind:search-layout="'box'" v-bind:placeholder="'Add symbol'"></Search>
    </div>
    <div style="md-layout md-size-100">
      <h3 class="md-title md-layout-item md-alignment-center-center">
        Portfolio: <strong>{{ portfolio.name }}</strong>
      </h3>
    </div>
    <md-tabs :md-active-tab="'tab-' + path" md-sync-route md-alignment="fixed">
      <md-tab id="tab-summary" md-label="Summary" :to="`/portfolios/${portfolio.id}/summary`">
        <md-empty-state
          v-if="portfolio.stocks.length == 0"
          md-description="Your list is empty. Add symbols to get relevant info."
        >
        </md-empty-state>
        <Summary v-else :stocks="portfolio.stocks"></Summary>
      </md-tab>

      <md-tab id="tab-holdings" md-label="Holdings" :to="`/portfolios/${portfolio.id}/holdings`">
        <md-empty-state
          v-if="portfolio.stocks.length === 0"
          md-description="Your list is empty. Add symbols to get relevant info."
        >
        </md-empty-state>
        <Holdings @deletedSymbol="onDelete" v-else :portfolio="portfolio"></Holdings>
      </md-tab>

      <md-tab id="tab-news" md-label="News" :to="`/portfolios/${portfolio.id}/news`">
        <md-empty-state
          v-if="portfolio.stocks.length === 0"
          md-description="Your list is empty. Add symbols to get relevant info."
        >
        </md-empty-state>
        <News v-else :tickers="tickers"></News>
      </md-tab>
    </md-tabs>
  </div>
</template>

<script>
import Search from './Search.vue';
import Holdings from './portfolio/Holdings.vue';
import Summary from './portfolio/Summary.vue';
import News from './portfolio/News.vue';

export default {
  name: 'Portfolio',
  components: {
    Holdings,
    Summary,
    Search,
    News,
  },
  data() {
    return {
      open: false,
      valid: false,
      portfolio: {},
      newSymbol: null,
      loaded: false,
      tickers: [],
      path: 'summary',
    };
  },
  created() {
    this.portfolioId = this.$route.params.portfolioId;
    this.path = this.$route.path.slice(1);
  },
  async mounted() {
    this.$store.commit('setLoading', true);
    this.portfolio = await this.$store.dispatch('getPortfolio', this.portfolioId);
    this.getTickers();
    if (this.tickers.length > 0) {
      await this.$store.dispatch('getLatestStockPrices', { symbols: this.tickers.join() });
    }
    this.$store.commit('setLoading', false);
    this.loaded = true;
  },
  methods: {
    getTickers() {
      const tickers = this.portfolio.stocks.map((stock) => stock.ticker);
      this.tickers = tickers;
    },
    async createPortfolio() {
      this.open = false;
      this.$store.commit('setLoading', true);
      await this.$store.dispatch('submitNewPortfolio', { name: this.portfolioName, info: this.info });
      this.portfolioName = '';
      this.info = '';
      this.$store.commit('setLoading', false);
    },
    submit() {
      if (this.valid) {
        this.createPortfolio();
      }
    },
    validName(value) {
      return value.length > 1;
    },
    async addSymbol(payload) {
      this.$store.commit('setLoading', true);
      await this.$store.dispatch('addSymbol', {
        portfolio: this.portfolio.id,
        payload: {
          symbol: payload.symbol,
          short_name: payload.short_name,
        },
      });
      this.portfolio = await this.$store.dispatch('getPortfolio', this.portfolioId);
      this.$store.dispatch('successMessage');
      this.$store.commit('setLoading', false);
    },
    onDelete() {
      this.getTickers();
    },
  },
  watch: {
    portfolio: function portfolio(val) {
      this.portfolio = val;
    },
    tickers: function tickers(val) {
      this.tickers = val;
    },
  },
};
</script>
<style scoped>
iframe {
  border: 0px none;
  height: 500px;
  width: 100%;
  overflow: hidden;
  margin-right: -40px;
  margin-top: -150px;
}
iframe html {
  overflow: hidden;
}

.md-content {
  width: 100%;
  display: flex;
  padding: 10px;
  justify-content: left;
  align-items: left;
}

.md-tab {
  padding: 0;
}
</style>
