
/**
 * Server setup
 */
'use strict';
var express = require('express');
var env = process.env.NODE_ENV || 'development';
var config = require('./config/config')[env];
var app = express();

require('./config/express')(app);
require('./config/routes')(app);
require(ROOT + '/app/models/themes');

app.listen(config.port);
console.log('Express app started on port '+ config.port);

// Allows `inspect(object)` in ejs templates
app.locals.inspect = require('util').inspect;

module.exports = app;

var bootstrap = require('./app/bootstrap/index');



// Bootstrap models
// fs.readdirSync(__dirname + '/app/models').forEach(function (file) {
//     if (~file.indexOf('.js')) { require(__dirname + '/app/models/' + file); }
// });
