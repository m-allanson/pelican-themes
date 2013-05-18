/**
 * Build an html string from the themes json, then chuck it onto the page.
 */
function output(data) {
    var html = '';
    var screenshots;
    data = JSON.parse(data);

    for (var theme in data) {
        screenshots = data[theme].screenshots;
       
        html += '<div class="theme">';
        html += '<h2>' + data[theme].path + '</h2>';

        if (screenshots.length > 0) {
           for (var i = 0; i < screenshots.length; i++) {
                html += '<img src="' + screenshots[i] + '" alt="'+data[theme].path+'">';
            }
        } else {
            html += '<p>There aren\'t any screenshots for this theme :(</p>';
        }
       
        html += '</div>';
    }

    // nothing fancy
    document.getElementById('themes').innerHTML = html;
}

domready(function () {
    microAjax("/json", function (res) {
        output(res);
    });
});
