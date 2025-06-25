import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
stages: [
{ duration: '20s', target: 100 },
{ duration: '40s', target: 100 },
{ duration: '20s', target: 0 },
],
};
export default function () {
  // define URL and payload
  const url = 'http://127.0.0.1:5000/login';
  const payload = "username=aaa&password=aaa";

  const params = {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
  };
  // send a post request and save response as a variable
  const res = http.post(url, payload, params);

  // check that response is 200
  check(res, {
    'response code was 200': (res) => res.status == 200,
  });
}