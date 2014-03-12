'use strict';

/**
 * Module dependencies.
 */
var express = require('express');
var env = process.env.NODE_ENV || 'development';
var config = require('./config')[env];


/**
 * Expose.
 */

module.exports = function(app) {

    app.set('views', config.viewsDir);
    app.set('view engine', 'ejs');

    app.use(express.favicon());
    app.use(express.logger('dev'));
    app.use(express.bodyParser());
    app.use(express.methodOverride());
    app.use(require('less-middleware')(config.staticDir));
    app.use(express.static(config.staticDir));
    app.use(app.router);

    // development only
    // if ('development' === app.get('env')) {
    //     app.use(express.errorHandler());
    // }
};
