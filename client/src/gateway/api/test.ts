import axios from 'axios';

export default {
  test: () => axios.get('http://127.0.0.1:5000/api/test')
    .then((response) => response.data),
};
