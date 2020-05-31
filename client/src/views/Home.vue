<template>
  <form>
    <h1>New prediction :</h1>
    <b-field label="Birthday">
      <b-datepicker
        ref="datepicker"
        expanded
        placeholder="Select your birthday"
        v-model="birthday"
        icon-right="calendar-today"
      >
      </b-datepicker>
    </b-field>
    <b-field label="Experience">
      <b-numberinput controls-position="compact" v-model="experience" min="0"></b-numberinput>
    </b-field>
    <b-field label="Annual income">
      <b-input
        :value="income"
        @input="onIncomeChanged"
        type="number"
        min="0"
        step="any"
        icon-right="currency-usd"
      ></b-input>
    </b-field>
    <b-field label="Zip code">
      <b-input v-model="zipCode" placeholder="Home address zip code"></b-input>
    </b-field>
    <b-field label="Family size">
      <b-numberinput controls-position="compact" v-model="familySize" min="1"></b-numberinput>
    </b-field>
    <b-field label="Average spending on credit cards per month">
      <b-input
        :value="ccAvg"
        @input="onCcAvgChanged"
        type="number"
        min="0"
        step="any"
        icon-right="currency-usd"
      ></b-input>
    </b-field>
    <b-field label="Education">
      <b-select placeholder="Select your education" v-model="education">
        <option
          v-for="option in options"
          :value="option.id"
          :key="option.id">
          {{option.label}}
        </option>
      </b-select>
    </b-field>
    <b-field label="Value of house mortgage">
      <b-input
        :value="mortgage"
        @input="onMortgageChanged"
        type="number"
        min="0"
        step="any"
        icon-right="currency-usd"
        placeholder="Mortgage..."
      ></b-input>
    </b-field>
    <b-field label="Do you have a securities account with the bank?">
      <b-checkbox v-model="securitiesAccount">{{ securitiesAccountLabel }}</b-checkbox>
    </b-field>
    <b-field label="Do you have a certificate of deposit with the bank?">
      <b-checkbox v-model="cdAccount">{{ cdAccountLabel }}</b-checkbox>
    </b-field>
    <b-field label="Do you use Internet banking facilities?">
      <b-checkbox v-model="online">{{ onlineLabel }}</b-checkbox>
    </b-field>
    <b-field label="Do you use a credit card issued by Universal Bank?">
      <b-checkbox v-model="creditCard">{{ creditCardLabel }}</b-checkbox>
    </b-field>
  </form>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

  @Component
export default class Home extends Vue {
    options = [
      {
        id: 1,
        label: 'Undergraduate',
      },
      {
        id: 2,
        label: 'Graduate',
      },
      {
        id: 3,
        label: 'Advanced/Professional',
      },
    ];

    birthday: Date | null = null;

    experience = 0;

    income = 0;

    zipCode = '';

    familySize = 1;

    ccAvg = 0;

    education: number | null = null;

    mortgage = 0;

    securitiesAccount = false;

    cdAccount = false;

    online = false;

    creditCard = false;

    get securitiesAccountLabel() {
      return this.securitiesAccount ? 'Yes' : 'No';
    }

    get cdAccountLabel() {
      return this.cdAccount ? 'Yes' : 'No';
    }

    get onlineLabel() {
      return this.online ? 'Yes' : 'No';
    }

    get creditCardLabel() {
      return this.creditCard ? 'Yes' : 'No';
    }

    onIncomeChanged(newVal: string) {
      // eslint-disable-next-line radix
      this.income = parseFloat(newVal) || 0;
    }

    onCcAvgChanged(newVal: string) {
      // eslint-disable-next-line radix
      this.ccAvg = parseFloat(newVal) || 0;
    }

    onMortgageChanged(newVal: string) {
      // eslint-disable-next-line radix
      this.mortgage = parseFloat(newVal) || 0;
    }
}
</script>

<style lang="scss">
  form {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    width: 80%;
    margin: 0 auto;
    padding: 30px;

    h1 {
      margin-bottom: 0.75rem;
      font-weight: bold;
      font-size: 1.8rem;
    }

    .field {
      width: 100%;

      input, .b-numberinput div.control, .select, select {
        width: 100%;
      }

      .b-checkbox.checkbox input[type=checkbox]:not(:checked) + .check {
        background: white;
      }
    }
  }
</style>
