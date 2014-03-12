'use strict';
var themes = require(ROOT + '/app/models/themes');

exports.index = function(req, res) {
    console.log('index route');
    themes.all(function(themeList){
        res.render('index', {
            title: 'Pelican Themes',
            themes: themeList
        });
    });

};

exports.refresh = function(req, res) {
    console.log('refresh route');
};
exports.list = function(req, res) {
    console.log('list route');
    themes.all(function(themeList){
        console.log('got themeList', themeList);
        res.render('theme-list', {
            title: 'Repo List',
            themes: themeList
        });
    });
};