/*
 * Routes.
 */
'use strict';
var themes = require(ROOT + '/app/controllers/themes');

module.exports = function(app) {
    app.get('/', themes.index);
    app.get('/refresh', themes.refresh);
    app.get('/theme-list', themes.list);
};
