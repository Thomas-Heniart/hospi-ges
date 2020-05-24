<template>
  <div class="home">
    <img alt="Vue logo" src="../assets/logo.png">
    <p>{{test.test}}</p>
  </div>
</template>

<script>
// @ is an alias to /src


import { Component, Vue } from 'vue-property-decorator';
import testApi from '@/gateway/api/test';

@Component
export default class Home extends Vue {
  test = { test: 'Not OK' };

  async mounted() {
    this.test = await testApi.test();
  }
}
</script>
