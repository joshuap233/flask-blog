const prerender = require('prerender');
const server = prerender({
  logRequests: true,
  port: 8888,
  // chromeLocation:'/usr/bin/google-chrome',
  // chromeFlags: ["--no-sandbox", "--hide-scrollbars", "--headless", "--disable-gpu", "--remote-debugging-address=0.0.0.0", "--remote-debugging-port=8888"]
});
server.start();

