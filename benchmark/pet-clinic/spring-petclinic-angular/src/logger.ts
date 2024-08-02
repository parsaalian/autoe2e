import axios from 'axios';


export function logToServer(message: string): void {
  console.log(message);
  axios.post('http://127.0.0.1:5000/log', { message })
    .then(response => console.log(response.data))
    .catch(error => console.error(error));
}
