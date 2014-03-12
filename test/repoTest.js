
/**
 * Module dependencies.
 */
'use strict';

// global.ROOT = require('path').dirname(require.main.filename);
global.ROOT = '/vagrant/app';

var repoService = require(ROOT+'/service/repoService.js');

repoService.getThemes(function(themeList) {
    console.log('Fetched repos from service', themeList);
});

