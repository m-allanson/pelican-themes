/*jslint node: true */
/**
 * Keeps theme data up to date
 */

// var config = require("../config");
// var restify = require("restify");
// var EventEmitter = require("events").EventEmitter;


var fs = require('fs');
var _ = require('underscore');
var async = require('async');
var EventEmitter = require('events').EventEmitter;
var GitHubApi = require("github");


module.exports = function () {

    "use strict";
    
    var themeList = {};
    var latestSha = '';
    var shaFile = ROOT+'/data/pelican-sha';
    var jsonFile = ROOT+'/data/themes.json';
    var previousSha = fs.readFileSync(shaFile, {encoding: 'utf8'});
    var savedThemes = fs.readFileSync(jsonFile, {encoding: 'utf8'});
    var apiKey = process.env.GITHUB_API_KEY;

    var events = new EventEmitter();
    var github = new GitHubApi({
        version: "3.0.0",
        timeout: 5000
    });

    /**
     * 
     */
    function init () {

        // events
        events.on('gotThemes', fetchScreenshots);
        events.on('updateContent', fetchContent);

        if (typeof apiKey === 'undefined') {
            console.log('Env var GITHUB_API_KEY must be valid, currently: ', apiKey);
            console.log('Exiting...');
            process.exit(1);
        }

        getSha();
    }

    // get the latest sha from github
    function getSha() {
        // read in sha
        fs.readFile(shaFile, 'utf8', function(err, data) {
          if (err) throw err;
          console.log('OK: ' + shaFile);
          console.log(data);
        });

        // uses personal api key
        github.authenticate({
            type: 'oauth',
            token: apiKey
        });

        // get latest commit sha
        github.repos.getCommits({
            user: 'getpelican',
            repo: 'pelican-themes',
            page: 0,
            per_page: 1
        }, function(err, res){
            if (err !== null) {
                console.log('error retrieving latest sha', err);
            } else {
                compareSha(res[0].sha);
            }
        });
    }

    // Save the sha to a file
    function saveSha(sha){
        fs.writeFile(shaFile, sha, {encoding: 'utf8'}, function(err) {
            if(err) {
                console.log(err);
            } else {
                console.log("The file was saved with sha ", sha);
            }
        }); 
    }

    function compareSha(sha) {
        console.log('Comparing shas', sha, previousSha);
        if (sha !== previousSha) {
            console.log('Shas are different, repos have been updated');
            previousSha = sha;
            saveSha(previousSha);
            
            // trigger an update event
            events.emit('updateContent', '', filterThemes); 
            
        } else {
            console.log('Shas match, no changes to repo');
        }
    }


    // uses github api to fetch the content at the given path, then runs callback
    function fetchContent(path, callback) {
        console.log('fetching content');
        github.repos.getContent({
            user: 'getpelican',
            repo: 'pelican-themes', 
            path: path
        }, function(err, res){
            if (err !== null) {
                console.log('error retrieving content', err);
            } else {
                callback(res, path);
            }
        });
    }

    function filterThemes(themes){
        // filter down to directories
        themes = _.filter(themes, function(theme){
            return theme.type === 'dir';
            // return theme.type === 'dir' || theme.type == 'submodule';
        });

        // just need the name and path
        themes = _.map(themes, function(theme){
            return {
                path: theme.path
            };
        });

        // temporarily cut down to just 2 themes to preserve api limits in testing
        // themes = themes.splice(0, 2);

        // save to an object keyed to theme.path
        _.each(themes, function(theme){
            themeList[theme.path] = theme;
        });

        console.log('filtered themes down to ', themeList);
        events.emit('gotThemes', themeList);
    }

    // async queue
    var q = async.queue(function (task, callback) {
        fetchContent(task.path, function(data, themePath){
            saveScreenshot(data, themePath, callback);
        });
    }, 8);


    // given a list of themes, gets screenshot urls
    function fetchScreenshots(themes){
        console.log('fetching screenshots for', themes);
        var queue = async.queue;

        q.drain = function() {
            updateComplete();
        };

        _.each(themes, function(theme){
            // get a list of files in the theme
            q.push({path: theme.path}, function (err) {
                console.log('finished processing once');
            });
        });
    }


    // given a list of files / folders in a theme, extract the screenshots
    function saveScreenshot(data, themePath, callback) {
        var regex = /^(screenshot)([\w-_]*).(png)$/i;

        // use regex to filter down to screenshot pngs
        data = _.filter(data, function(item){
            return regex.test(item.name);
        });

        // now just extract the html url from the screenshot data
        data = _.map(data, function(item){
            // html_url is actually the link to the page, bodge in conversion
            // to raw url;
            var url = item.html_url.replace('https://github', 'https://raw.github');
            return url.replace('blob/', '');
        });

        // add screenshot(s) to themeList
        themeList[themePath].screenshots = data;

        callback();
    }

    function updateComplete() {
        console.log('updated all screenshots!', themeList);
        savedThemes = JSON.stringify(themeList); // savedThemes is returned by the http server 
        var themeString = JSON.stringify(themeList);

        fs.writeFile(jsonFile, themeString, {encoding: 'utf8'}, function(err) {
            if(err) {
                console.log(err);
            } else {
                console.log('Saved data to theme file');
            }
        }); 
    }

    function getThemes() {
        console.log('requested', savedThemes);
        return savedThemes;
    }

    return {
        init: init,
        themes: getThemes
    };
}();
