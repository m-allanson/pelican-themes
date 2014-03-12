'use strict';

var env = process.env.NODE_ENV || 'development';
var config = require(ROOT + '/config/config')[env];
var client = require(ROOT + '/config/redis');
var repoService = require(ROOT+'/app/service/repoService.js');
var themes = require(ROOT + '/app/models/themes');

var setNewSha = function(sha) {
    client.set('pt:currentSha', sha);
    console.log('set sha to ', sha);
    themes.all();
};

var refresh = function() {
    client.get('pt:currentSha', function(err,reply){
        if (err) { console.log('unable to get sha', err); }

        if (reply === null) {
            // purge stored themes
            console.log('sha not set, deleting all stored themes');
            themes.deleteAll();

            // get latest sha from github
            console.log('sha not set, fetching latest from github');
            repoService.getSha(setNewSha);
        } else {
            console.log('sha already exists as', reply);
            return reply;
        }
    });
};

var current = function(cb) {
    client.get('pt:currentSha', function(err,reply){
        if (err) {
            console.log('unable to get sha', err);
        } else {
            console.log('got sha', reply);
        }
        cb(reply);
    });
};

module.exports.refresh = refresh;
module.exports.current = current;
