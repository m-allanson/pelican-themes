'use strict';

var env = process.env.NODE_ENV || 'development';
var config = require(ROOT + '/config/config')[env];
var client = require(ROOT + '/config/redis');
var repoService = require(ROOT+'/app/service/repoService.js');
var sha = require(ROOT + '/app/models/sha');

module.exports.all = function(callback) {
    sha.current(function(currentSha){
        // console.log('Deleting cached themes');
        // client.del('pt:themes:' + currentSha);

        // getting themes from github is a slow operation, attempt to retrieve from cache first
        client.get('pt:themes:' + currentSha, function(err,reply){
            if (err) { console.log('unable to get themes for sha' + currentSha, err); }

            if (reply === null) {
                console.log('pt:themes:' + currentSha + ' not available, fetching latest from github');

                repoService.getThemes(function(themeList){
                    client.set('pt:themes:' + currentSha, JSON.stringify(themeList));
                    callback(themeList);
                });
            } else {
                console.log('got themes from cache for sha ' + currentSha);
                callback(JSON.parse(reply));
            }
        });
    });
};

module.exports.deleteAll = function() {
    console.log('this is where themes.deleteAll() functionality should go');
};

/*jslint node: true */
/**
 *
 */

// var dataFetcher = require(ROOT+'/service/data-fetcher.js');
// var themes = exports.all = dataFetcher.themes();



// var themeService = require(ROOT+'/service/themes.js');
// var themes = exports.all = themeService.themes();

// themes.all = {
//     'url1': {
//         path: '',
//         url: '',
//         currentSha: '',
//         screenshots: [
//             'https://raw.github.com/getpelican/pelican-themes/master/subtle/screenshot-1-top.png',
//             'https://raw.github.com/getpelican/pelican-themes/master/subtle/screenshot-2-bottom.png'
//         ]
//     },
//     'url2': {
//         path: '',
//         url: '',
//         currentSha: '',
//         screenshots: [
//             'https://raw.github.com/getpelican/pelican-themes/master/subtle/screenshot-1-top.png',
//             'https://raw.github.com/getpelican/pelican-themes/master/subtle/screenshot-2-bottom.png'
//         ]
//     },
// };