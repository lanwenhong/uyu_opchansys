$(document).ready(function(){
    $("#verify_form").validate({
        rules: {
            email: {
                required: true,
                email: true
            },
            password: {
                required: true,
                minlength: 6

            }
        },
        messages: {
            email: {
                required: '<span class="btn-warning">请输入邮箱</span>',
                email: '<span class="btn-warning">请检查电子邮件的格式</span>'
            },
            password: {
                required: '<span class="btn-warning">请输入密码</span>',
                minlength: '<span class="btn-warning">请至少输入6个字符</span>'
            }
        }
    });
})
