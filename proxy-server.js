var http = require('http'), httpProxy = require('http-proxy');

// .................. Proxy Server ......
var proxy = httpProxy.createProxyServer({});

// ............
proxy.on('error', function (err, req, res) {
  res.writeHead(500, {
    'Content-Type': 'text/plain'
  });
  res.end('Something went wrong. And we are reporting a custom error message.');
});

// ........................... proxy.web(req, res config) ........................
var server = require('http').createServer(function(req, res) {
  // ..........................................
  var host = req.headers.host, ip = req.headers['x-forwarded-for'] || req.connection.remoteAddress;
  console.log("client ip:" + ip + ", host:" + host);
  var reqUrl = req.url.substr(1);
  console.log("req.url: " + req.url);
  console.log("reqUrl: " + reqUrl);

  switch(true){
    case /stress-test.*/.test(reqUrl):
        console.log("proxy to stress-test port at 5312");
        if(false && reqUrl != 'stress-test/app.js') {
          prefixLength = "stress-test".length;
          req.url = "/" + reqUrl.substr(prefixLength + 1);
        }
        console.log("real req url is:" + req.url);
        proxy.web(req, res, { target: 'http://localhost:5312' });
    break;
    case /proxy/.test(reqUrl):
        res.writeHead(200, {
            'Content-Type': 'text/plain'
        });
        res.end('Welcome to my server!');
    break;
    case /workflow_server.*/.test(reqUrl):
        prefixLength = "workflow_server".length;
        req.url = "/" + reqUrl.substr(prefixLength + 1)
        console.log("real req url is:" + req.url)
        proxy.web(req, res, { target: 'http://localhost:5201' });
    break;
    default:
        console.log("real req url is:" + req.url)
        proxy.web(req, res, { target: 'http://localhost:5200' });
  }
});

var PORT = 5311;
console.log("proxy-server is listening on port:" + PORT);
server.listen(PORT);