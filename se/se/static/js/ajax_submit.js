$(document).ready(function() {

    $.ajaxSetup({ 
         beforeSend: function(xhr, settings) {
             function getCookie(name) {
                 var cookieValue = null;
                 if (document.cookie && document.cookie != '') {
                     var cookies = document.cookie.split(';');
                     for (var i = 0; i < cookies.length; i++) {
                         var cookie = jQuery.trim(cookies[i]);
                         // Does this cookie string begin with the name we want?
                     if (cookie.substring(0, name.length + 1) == (name + '=')) {
                         cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                         break;
                     }
                 }
             }
             return cookieValue;
             }
             if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                 // Only send the token to relative URLs i.e. locally.
                 xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
             }
         } 
    });

    $.ajax({
         type:"POST",
         url:"/",
         data: {
                resolution: window.screen.width + 'x' + window.screen.height
                // all of this data is submitted via POST to your view.
                // in django, request.POST['background-color'] 
         },
         success: function(data){
            
         }
    });


});

function submit_query() {

    $.ajax({
         type:"POST",
         url:"/save",
         data: {
                value: $('#cse-search-input-box-id').val(),
                // all of this data is submitted via POST to your view.
                // in django, request.POST['background-color'] 
         },
         success: function(data){
            
         }
    });
}

function submit_time() {

    $.ajax({
         type:"POST",
         url:"/save",
         data: {
                // all of this data is submitted via POST to your view.
                // in django, request.POST['background-color'] 
         },
         success: function(data){
            
         }
    });
}

function submit_privacy() {

    $.ajax({
         type:"POST",
         url:"/save",
         data: {
                privacy: 1,
                // all of this data is submitted via POST to your view.
                // in django, request.POST['background-color'] 
         },
         success: function(data){
            
         }
    });
}

