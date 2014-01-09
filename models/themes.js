/*jslint node: true */
/**
 * 
 */

var dataFetcher = require(ROOT+'/service/data-fetcher.js');

var themes = exports.all = dataFetcher.themes();
