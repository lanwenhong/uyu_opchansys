$(document).ready(function(){
    $(".do-submit").click(function(){
        var mobile = $('input[name=mobile]').val();
        var password = $('[name=password]').val();
        if(mobile&&password){
		    var post_data = {
				'mobile': mobile,
				'password': password,
			}
            $.ajax({
	            url: '/channel_op/v1/api/login',
	            type: 'POST',
	            dataType: 'json',
	            data: post_data,
	            success: function(data) {
                    var respcd = data.respcd;
                    if(respcd != '0000'){
                        var resperr = data.resperr;
                        var respmsg = data.resmsg;
                        var msg = resperr ? resperr : resmsg;
                        toastr.warning(msg);
                        return false;
                    } else {
						toastr.info('ok');
					}
	            },
	            error: function(data) {
	            },
            });
        }else{
            toastr.warning('请输入手机号和密码');
            return false;
		}
    });
});
