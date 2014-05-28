'use strict';
var path = require('path');
var port = process.env.PORT || 3000;
var url = require('url');

global.ROOT = path.resolve(__dirname + '../..');

module.exports = {
    development: {
        root: ROOT,
        staticDir: path.resolve(ROOT + '/public'),
        viewsDir: path.resolve(ROOT + '/app/views'),
        port: port,
        redisURL: false
    },
    production: {
        root: ROOT,
        staticDir: path.resolve(ROOT + '/public'),
        viewsDir: path.resolve(ROOT + '/app/views'),
        port: port,
        redisURL: url.parse(process.env.REDISCLOUD_URL)
    }

};