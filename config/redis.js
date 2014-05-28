'use strict';

var env = process.env.NODE_ENV || 'development';
var config = require('./config')[env];
var redis = require('redis');
var redisURL = config.redisURL;
var client;

if (env === 'production') {
    // Heroku Redis Cloud setup
    client = redis.createClient(redisURL.port, redisURL.hostname, {'no_ready_check': true});
    client.auth(redisURL.auth.split(':')[1]);
} else {
    client = redis.createClient();
}

client.on('error', function (err) {
    console.log('Redis error: ', err);
});

module.exports = client;