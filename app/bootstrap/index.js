'use strict';
var client = require(ROOT + '/config/redis');
var themes = require(ROOT + '/app/models/themes');
var sha = require(ROOT + '/app/models/sha');
var currentSha = null;
var allThemes = null;

sha.refresh();
sha.current(function(res){
    currentSha = res;
    console.log('current sha is', currentSha);
});

console.log('in bootstrap.js');
themes.all(function(themeList){
    console.log('in bootstrap, got themeList');
});