'use strict';
console.log('in redis.js');

var env = process.env.NODE_ENV || 'development';
var config = require('./config')[env];
var redis = require('redis');
var client = redis.createClient();
// var github = require(ROOT + '/app/service/github');


client.on('error', function (err) {
    console.log('Redis error: ', err);
});

// client.set('string key', 'string val', redis.print);
// client.get('string key', function(err, reply) {
//     console.log('got string key');
//     console.log(reply.toString());
// });
// client.hset('hash key', 'hashtest 1', 'some value', redis.print);
// client.hset(['hash key', 'hashtest 2', 'some other value'], redis.print);
// client.hkeys('hash key', function (err, replies) {
//     console.log(replies.length + ' replies:');
//     replies.forEach(function (reply, i) {
//         console.log('    ' + i + ': ' + reply);
//     });
// });

module.exports = client;