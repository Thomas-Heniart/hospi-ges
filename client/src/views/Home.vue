<template>
  <div>
    <form>
      <b-field label="Education">
        <b-select placeholder="Select your education">
          <option
            v-for="option in options"
            :value="option.id"
            :key="option.id">
            {{option.label}}
          </option>
        </b-select>
      </b-field>
    </form>
  </div>
</template>

<script>
import { Component, Vue } from 'vue-property-decorator';

@Component
export default class Home extends Vue {
    options = [
      {
        id: 0,
        label: 'Low school',
      },
      {
        id: 1,
        label: 'High school',
      },
    ]
}
</script>
