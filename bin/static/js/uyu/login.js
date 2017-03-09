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
                        window.localStorage.setItem('myid', userid);
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

	$("#findPassWordBtn").click(function(){
        $("#findPassWordForm").resetForm();
	    $("#findPassWord").modal();
	});

    $("#send_vcode").click(function(){
        var mobile = $("#findMobile").val();
        console.log('mobile:' + mobile);
        if(mobile==''||mobile==undefined){
            toastr.warning('请输入手机号');
            return false;
        }
        var post_data = {
            'mobile': mobile,
        }
        $.ajax({
	        url: '/channel_op/v1/api/sms_send',
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
                    $("#send_vcode").attr('disabled', true);
                    timedCount();
                }
	        },
	        error: function(data) {
                toastr.warning('请求数据异常');
	        },
        });

    });

    $(".saveNewPassword").click(function(){
        var mobile = $("#findMobile").val();
        var code = $("#vcode").val();
        var password = $("#newPassword").val();
        var passwordConfirm = $("#newPasswordConfirm").val();
        if(!mobile||!code||!password||!passwordConfirm||password!=passwordConfirm){
            toastr.warning('请检查验证码和密码');
            return false;
        }
        var post_data = {
            'mobile': mobile,
            'vcode': code,
            'password': password
        }
        $.ajax({
	        url: '/channel_op/v1/api/passwd_change',
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
                    $("#findPassWord").modal('hide');
                }
	        },
	        error: function(data) {
                toastr.warning('请求数据异常');
	        },
        });
    });
});

function timedCount()
 {
    var time0=$('.time_60s i').text();
    $('.time_60s i').text(time0-1);
    t=setTimeout("timedCount()",1000);
    if(time0==0){
        clearTimeout(t);
        $('.time_60s i').text(60);
        $('#send_vcode').attr('disabled', false);
    }
 }
