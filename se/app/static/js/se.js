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

function search() {

    var url = window.location.href;
    var flag = 0;
    var newurl = ''
    for (i = 0;i < url.length ; i = i + 1) {

        if (url[i] != '?') {

            newurl = newurl + url[i];
        }
        else {

            break;
        }
    }
    if ($('#q').val().length > 2) {

        newurl = newurl + '?q=' + $('#q').val();
        window.open(newurl)
    }
    else {
        return false;
    }
}

window.setInterval(function() {
    $('.gsc-above-wrapper-area').remove();
    $('.gcsc-branding').remove();
    $('.gsc-orderby').remove();
}, 1);
