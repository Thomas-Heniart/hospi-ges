<template>
  <div>
    <form @submit.prevent="onSubmit">
      <h1>New prediction :</h1>
      <b-field label="Birthday">
        <b-datepicker
          ref="datepicker"
          expanded
          placeholder="Select your birthday"
          v-model="birthday"
          icon-right="calendar-today"
          required
        >
        </b-datepicker>
      </b-field>
      <b-field label="Experience">
        <b-numberinput controls-position="compact" v-model="experience" min="0"
                       required></b-numberinput>
      </b-field>
      <b-field label="Annual income">
        <b-input
          :value="income"
          @input="onIncomeChanged"
          type="number"
          min="0"
          step="any"
          icon-right="currency-usd"
          required
        ></b-input>
      </b-field>
      <b-field label="Zip code">
        <b-input v-model="zipCode" placeholder="Home address zip code" required></b-input>
      </b-field>
      <b-field label="Family size">
        <b-numberinput controls-position="compact" v-model="familySize" min="1"
                       required></b-numberinput>
      </b-field>
      <b-field label="Average spending on credit cards per month">
        <b-input
          :value="ccAvg"
          @input="onCcAvgChanged"
          type="number"
          min="0"
          step="any"
          icon-right="currency-usd"
          required
        ></b-input>
      </b-field>
      <b-field label="Education">
        <b-select placeholder="Select your education" v-model="education" required>
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
          required
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
      <b-button expanded
                type="is-primary"
                native-type="submit"
                :loading="isLoading">
        Submit
      </b-button>
    </form>
    <b-message id="result"
               title="Prediction result"
               :active.sync="predictionEnded"
               :type="predictionType"
               has-icon
    >
      {{predictionResult}}
    </b-message>
    <b-loading :is-full-page="true" :active.sync="isLoading"></b-loading>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import * as predictionAPI from '@/gateway/api/prediction';
import moment from 'moment';

  @Component
export default class Home extends Vue {
    isLoading = false;

    accepted: boolean | null = null;

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

    get predictionEnded() {
      return this.accepted !== null;
    }

    get predictionType() {
      let res = 'is-warning';

      if (this.accepted) {
        res = 'is-success';
      } else if (this.accepted === false) {
        res = 'is-danger';
      }

      return res;
    }

    get predictionResult() {
      return this.accepted ? 'You can make a loan to your client' : 'We advise you to refuse the loan to your client';
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

    async onSubmit() {
      this.accepted = null;
      this.isLoading = true;

      try {
        let age = 0;

        if (this.birthday) {
          age = moment().diff(moment(this.birthday), 'years');
        }

        const predictionResponse = await predictionAPI.default.newPrediction({
          age,
          ccAvg: this.ccAvg,
          cdAccount: this.cdAccount,
          creditCard: this.creditCard,
          education: this.education || 1,
          experience: this.experience,
          family: this.familySize,
          income: this.income,
          mortgage: this.mortgage,
          online: this.online,
          securities: this.securitiesAccount,
          zipCode: this.zipCode,
        });
        this.accepted = predictionResponse.accepted;
      } catch (e) {
        console.error(e);
      } finally {
        setTimeout(() => {
          const container = this.$el.querySelector('#result');
          if (container) {
            container.scrollIntoView();
          }
          this.isLoading = false;
        }, 100);
      }
    }
}
</script>

<style lang="scss">
  form {
    position: relative;
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

  #result {
    width: 50%;
    margin: 0 auto;
  }
</style>
