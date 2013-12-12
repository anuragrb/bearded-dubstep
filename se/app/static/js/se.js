(function() {

        var cx = '000248085842428281046:dgcmn_4tj-k';
        var gcse = document.createElement('script');
        gcse.type = 'text/javascript';
        gcse.async = true;
        gcse.src = (document.location.protocol == 'https:' ? 'https:' : 'http:') +
            '//www.google.com/cse/cse.js?cx=' + cx;
        var s = document.getElementsByTagName('script')[0];
        s.parentNode.insertBefore(gcse, s);
  })();

function executeQuery() {
    var input = document.getElementById('cse-search-input-box-id');
    var element = google.search.cse.element.getElement('searchresults-only0');
    if (input.value == '') {
      element.clearAllResults();
    } else {
      element.execute(input.value);
    }
    return false;
}

window.setInterval(function() {
    $('.gsc-above-wrapper-area').remove();
    $('.gcsc-branding').remove();
    $('.gsc-orderby').remove();
    $('#results').find('a').className = 'informal';
}, 1);

$(document).ready(function() {
    $('#results').on('click', 'a', function (event) {
        alert($(this).attr('href'));
    });
});
