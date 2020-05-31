import axios from 'axios';
import { PredictionPayload } from '@/gateway/payloads/PredictionPayload';
import { PredictionResponse } from '@/gateway/responses/PredictionResponse';

export default {
  newPrediction: (payload: PredictionPayload): Promise<PredictionResponse> => axios.post('/api/prediction', payload)
    .then((response) => response.data),
};
