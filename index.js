/*jslint node: true */
"use strict";

global.ROOT = require('path').dirname(require.main.filename);
var dataFetcher = require('./app/data-fetcher.js');
var express = require('express');
var http = require('http');
var port = 8081;

// gets and stores data
dataFetcher.init();

// express for routing and index.html
var app = express();
app.use(app.router);
app.use(express.favicon());
app.use(express.static(__dirname + "/public"));

// serve the results
app.get('/json', function (request, response) {
    response.writeHead(200, {"Content-Type": "application/json"});
    response.end(dataFetcher.themes());
});

console.log('running server on port: ', port);
app.listen(port);
