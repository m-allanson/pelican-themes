/**
 * Repo Service.
 *
 * Connects to the pelican-themes github repo, getting a list of all available
 * themes.  Themes may be a directory or a submodule in the pelican-themes
 * repo.

[ { user: 'KenMercusLai',
    repo: 'BT3-Flat',
    sha: '656296ab29a76d980155427f1f1ffe1892966a2a',
    path: '',
    name: 'BT3-Flat' },
  { user: 'getpelican',
    repo: 'pelican-themes',
    sha: '4e93de4a8f12eeaa77f2b03026d583bc423721eb',
    path: 'Just-Read',
    name: 'Just-Read' } ]
 *
 */

'use strict';

var _ = require('underscore');
var fs = require('fs');
var GitHubApi = require('github');
var co = require('co');
var thunkify = require('thunkify');

var apiKey = process.env.GITHUB_API_KEY;

var github = new GitHubApi({
    version: '3.0.0',
    timeout: 5000
});

// uses personal api key
github.authenticate({
    type: 'oauth',
    token: apiKey
});


// Thin wrapper around getContent that sets overridable defaults
// typically response will look like: https://api.github.com/repos/getpelican/pelican-themes/contents/
function getRepoContent(msg, callback) {
    msg = _.extend({
        user: 'getpelican',
        repo: 'pelican-themes',
        path: ''
    },msg);
    github.repos.getContent(msg, callback);
}

// get the sha of the latest commit on the repo
function getLatestSha(callback) {
    github.repos.getCommits({
        user: 'getpelican',
        repo: 'pelican-themes',
        page: 0,
        'per_page': 1
    }, callback);
}

// Expose method that returns latest sha
function getSha(callback) {
    return getLatestSha(function(err, res){
        if (err !== null) {
            console.log('error retrieving latest sha', err);
        } else {
            callback(res[0].sha);
        }
    });
}

// Themes may be contained in a directory or submodule.  An alternate way to do
// this would be to strip any valid files from the repo - which would leave just
// theme folders and theme submodules.
//
// submodules erroneously have a type of 'file', but can be detected by
// their null size.  See http://developer.github.com/v3/repos/contents/#response-if-content-is-a-directory
function getThemeLocationsFromRepo(repoContents) {
    return _.filter(repoContents, function(item){
        var valid = false;
        if (item.type === 'dir') { valid = true; }
        if (item.type === 'file' && item.size === 0) { valid = true; }
        return valid;
    });
}

// Convert github data into the minimum useful info needed to get screenshots
function mapThemeLocations(locations) {
    return _.map(locations, function(location){
        var path = '';
        if (location.type === 'dir') { path = location.path; }

        var repoInfo = location['html_url'].replace('https://github.com/', '');
        repoInfo = repoInfo.split('/');

        return {
            user: repoInfo[0],
            repo: repoInfo[1],
            sha: location.sha,
            path: path,
            name: location.name
        };
    });
}

function getImagesFromThemeRepo (repo, callback) {
    getRepoContent(repo, function(err, res){
        var regex = /(screenshot|preview)([\w-_]*).(png|jpg)$/i;

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

        console.log('Fetching images for repo', data);

        callback(null, data);
    });
}

var getImagesFromThemeRepoThunk = thunkify(getImagesFromThemeRepo);

function getThemes (callback) {
    return getRepoContent({}, function (err, res) {
        if (err) {
            console.log(err);
            process.exit('1');
        }

        var themeLocations;
        themeLocations = getThemeLocationsFromRepo(res);
        themeLocations = mapThemeLocations(themeLocations);

        // temp
        console.log('There are ', themeLocations.length, ' themes for Pelican.');
        // console.log('Truncating themes for testing');
        // themeLocations = themeLocations.slice(0,8);

        // Use a generator to get all the image urls from each repo.
        co(function *getThemeImages(){
            for (var i = themeLocations.length - 1; i >= 0; i--) {
                themeLocations[i].images = yield getImagesFromThemeRepoThunk(themeLocations[i]);
            }

            callback(themeLocations);
        })();
    });
}

exports.getThemes = getThemes;
exports.getRepoContent = getRepoContent;
exports.getSha = getSha;