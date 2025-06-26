import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
stages: [
{ duration: '40s', target: 200 },
],
};
function makeid(length) {
    var result           = '';
    var characters       = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    var charactersLength = characters.length;
    for ( var i = 0; i < length; i++ ) {
        result += characters.charAt(Math.floor(Math.random() * charactersLength));
    }
    return result;
}
export default function () {
    /******************************************************
     *  Testing for simulating stress on the server
     * should emulate above the max stress that the server 
     * would experince during the competition.
     * Works by just sending a shit ton of requests to the 
     * server as 3 different users.
     ******************************************************/
  
  
  const loginUrl = 'http://127.0.0.1:5000/login';
  const userA = "username=aaa&password=aaa";
  const userB = "username=bbb&password=bbb";
  const userC = "username=ccc&password=ccc";
  const userToFail = "username=fail&password=fail";

  var loginParams = {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
  };

  const res4 = http.post(loginUrl,
    userToFail,
    loginParams,);
    sleep(1)

  // add auth headers to cookie jar
  const jar = http.cookieJar();
  const cookiesForFail = jar.cookiesForURL(res4.url);


  // post to database
  var climberIdUrl = 'http://127.0.0.1:5000/climber_id'
  const res1 = http.post(
     loginUrl,
     userA,
     loginParams);
    sleep(1)
  const cookiesForA = jar.cookiesForURL(res1.url);
  const res5 = http.post(
     climberIdUrl,
     "navn=aTest:"+makeid(8)+"&gender=None",
     {
        headers: {
        'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8", 
        "Cookie": cookiesForA,
    }
    },);
    sleep(1)
  const res2 = http.post(
     loginUrl,
     userB,
     loginParams);
    sleep(1)
  const cookiesForB = jar.cookiesForURL(res2.url);
  const res6 = http.post(
     climberIdUrl,
     "navn=bTest:"+makeid(8)+"&gender=None",
     {
        headers: {
        'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8", 
        "Cookie": cookiesForB,
    }
    },);
    sleep(1)
  const res3 = http.post(
    loginUrl,
    userC,
    loginParams);
    sleep(1)
  const cookiesForC = jar.cookiesForURL(res3.url);
  const res7 = http.post(
    climberIdUrl,
     "navn=cTest:"+makeid(8)+"&gender=None",
    {
        headers: {
        'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8", 
        "Cookie": cookiesForC,
    }
    },);

    
  check(res1, {
    'main page status was 200': (r) => r.status === 200,
    'authentication successful': cookiesForA["session"] != "",
  });
  check(res3, {
    'main page status was 200': (r) => r.status === 200,
    'authentication failed': (r) => r.url == "http://127.0.0.1:5000/routes",
  });
  check(res4, {
    'main page status was 200': (r) => r.status === 200,
    'authentication failed': (r) => r.url == "http://127.0.0.1:5000/login",
  });
}