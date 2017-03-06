$(document).ready(function(){
    $(".do-submit").click(function(){
        var name = $('input[name=email]').val();
        var password = $('[name=password]').val();
        if(password!='111'){
            toastr.warning('pass fail');
            return false;
        }
    });
});