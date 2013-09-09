
/*
 * GET home page.
 */
global.ROOT = require('path').dirname(require.main.filename);
var dataFetcher = require('../service/data-fetcher.js');

exports.index = function(req, res){
  var themes = dataFetcher.themes();
  res.render('index', { title: 'Pelican Themes', themes: themes });
};
