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
                        var userid = data.data.userid;
                        window.location.href="/channel_op/v1/page/overview.html";
					}
	            },
	            error: function(data) {
                    toastr.warning('请求数据异常');
	            },
            });
        }else{
            toastr.warning('请输入手机号和密码');
            return false;
		}
    });
});
