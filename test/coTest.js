'use strict';
global.ROOT = '/vagrant';

var co = require('co');
var _ = require('underscore');
var thunkify = require('thunkify');

var env = process.env.NODE_ENV || 'development';
var config = require(ROOT + '/config/config')[env];
var client = require(ROOT + '/config/redis');
var sha = require(ROOT + '/app/models/sha');
var repoService = require(ROOT + '/app/service/repoService');
var currentSha;

client.get = thunkify(client.get);

var getImage = function(repo, callback) {
    repoService.getRepoContent(repo, function(err, res){
        var regex = /^(screenshot)([\w-_]*).(png)$/i;

        // use regex to filter down to screenshot pngs
        var data = _.filter(res, function(item){
            return regex.test(item.name);
        });

        // now just extract the html url from the screenshot data
        data = _.map(data, function(item){
            // html_url is actually the link to the page, bodge in conversion to raw url;
            var url = item['html_url'].replace('https://github', 'https://raw.github');
            return url.replace('blob/', '');
        });

        callback(null, data);
    });
};

getImage = thunkify(getImage);
// Equivalent to doing this:
// var getImages = function(repo){
//     return function(callback){
//         console.log('in the thunk');
//         getImage(repo, callback);
//     };
// };


co(function *returnSha(){
    var sha = yield client.get('pt:currentSha');
    var repos = yield client.get('pt:themes:' + sha);
    repos = JSON.parse(repos);
    // console.log('yielded sha', sha);
    // console.log('repo length is', repos.length);

    for (var i = repos.length - 1; i >= 0; i--) {
        repos[i].images = yield getImage(repos[i]);
    }
    console.log('logging repos', repos);

    process.kill();
})();
