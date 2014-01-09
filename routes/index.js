
/*
 * GET home page.
 */
var themes = require(ROOT+'/models/themes.js');

exports.index = function(req, res){
  res.render('index', { title: 'Pelican Themes', themes: themes.all });
};
