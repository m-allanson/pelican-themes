'use strict';
var path = require('path');
var port = process.env.PORT || 3000;

global.ROOT = path.resolve(__dirname + '../..');

module.exports = {
    development: {
        root: ROOT,
        staticDir: path.resolve(ROOT + '/public'),
        viewsDir: path.resolve(ROOT + '/app/views'),
        port: port
    }

};