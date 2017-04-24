/**
 * Created by admin on 2017/4/20.
 */
$(document).ready(function(){

    $.validator.addMethod("isMobile", function(value, element) {
        var length = value.length;
        var mobile = /^(1\d{10})$/;
        return this.optional(element) || (length == 11 && mobile.test(value));
    }, "请正确填写您的手机号码");


    $.validator.addMethod("isElevenNum", function(value, element) {
        var length = value.length;
        var mobile = /^([0-9]{11})$/;
        return this.optional(element) || (length == 11 && mobile.test(value));
    }, "请正确填写您的手机号码");


    $('#userList').DataTable({
        "autoWidth": false,     //通常被禁用作为优化
        "processing": true,
        "serverSide": true,
        "paging": true,         //制指定它才能显示表格底部的分页按钮
        "info": true,
        "ordering": false,
        "searching": false,
        "lengthChange": true,
        "deferRender": true,
        "iDisplayLength": 10,
        "sPaginationType": "full_numbers",
        "lengthMenu": [[10, 40, 100],[10, 40, 100]],
        "dom": 'l<"top"p>rt',
        "fnInitComplete": function(){
            var $userList_length = $("#userList_length");
            var $userList_paginate = $("#userList_paginate");
            var $page_top = $('.top');

            $page_top.addClass('row');
            $userList_paginate.addClass('col-md-8');
            $userList_length.addClass('col-md-4');
            $userList_length.prependTo($page_top);
        },
        "ajax": function(data, callback, settings){
            var get_data = {
                'page': Math.ceil(data.start / data.length) + 1,
                'maxnum': data.length
            };

            var se_userid = window.localStorage.getItem('myid');
            get_data.se_userid = se_userid;
            var phone_num = $("#s_phone_num").val();

            if(phone_num){
                get_data.phone_num = phone_num;
            }

            $.ajax({
                url: '/channel_op/v1/api/user_list',
                type: 'GET',
                dataType: 'json',
                data: get_data,
                success: function(data) {
                    var respcd = data.respcd;
                    if(respcd != '0000'){
                        $processing = $("#userList_processing");
                        $processing.css('display', 'none');
                        var resperr = data.resperr;
                        var respmsg = data.respmsg;
                        var msg = resperr ? resperr : respmsg;
                        toastr.warning(msg);
                        return false;
                    } else {
                        detail_data = data.data;
                        num = detail_data.num;
                        callback({
                            recordsTotal: num,
                            recordsFiltered: num,
                            data: detail_data.info
                        });
                    }
                },
                error: function(data) {
                    toastr.warning('请求数据异常');
                }

            });
        },
        'columnDefs': [
            {
                targets: 8,
                data: '操作',
                render: function(data, type, full) {
                    var userid = full.id;
                    var msg = '修改密码';
                    var op = "<button type='button' class='btn btn-success btn-sm modify-password' data-userid="+userid+">"+msg+"</button>";
                    return op;
                }
            }
        ],
        'columns': [
            { data: 'id' },
            { data: 'phone_num' },
            { data: 'username' },
            { data: 'nick_name' },
            { data: 'state' },
            { data: 'user_type' },
            { data: 'remain_times' },
            { data: 'ctime' }
        ],
        'oLanguage': {
            'sProcessing': '<span style="color:red;">加载中....</span>',
            'sLengthMenu': '每页显示_MENU_条记录',
            "sInfo": '显示 _START_到_END_ 的 _TOTAL_条数据',
            'sInfoEmpty': '没有匹配的数据',
            'sZeroRecords': '没有找到匹配的数据',
            'oPaginate': {
                'sFirst': '首页',
                'sPrevious': '前一页',
                'sNext': '后一页',
                'sLast': '尾页'
            }
        }
    });

    $("#userSearch").click(function(){

        var user_query_vt = $('#users_query').validate({
            rules: {
                q_phone_num: {
                    required: false,
                    isElevenNum: '#s_phone_num'
                }
            },
            messages: {
                q_phone_num: {
                    required: '请输入手机号'
                }
            },
            errorPlacement: function(error, element){
                var $error_element = element.parent().parent().next();
                $error_element.text('');
                error.appendTo($error_element);
            }
        });
        var ok = user_query_vt.form();
        if(!ok){
            $("#query_label_error").show();
            $("#query_label_error").fadeOut(1400);
            return false;
        }
        $('#userList').DataTable().draw();
    });

    $(document).on('click', '.modify-password', function(){
        var userid = $(this).data('userid');
        $('#modify_userid').text(userid);
        $('#ModifyPassWordForm').resetForm();
        $('#ModifyPassWord').modal();
    });

    $('.saveNewPassword').click(function () {
        var userid = $('#modify_userid').text();
        var new_password = $('#newPassword').val();
        var new_password_confirm = $('#newPasswordConfirm').val();
        console.log(new_password);
        console.log(new_password_confirm);

        if(new_password.length < 6 || new_password_confirm.length < 6){
            toastr.warning('密码长度至少六位');
            return false;
        }

        if(!new_password||!new_password_confirm||new_password!=new_password_confirm){
            toastr.warning('请检查密码');
            return false;
        }
        var se_userid = window.localStorage.getItem('myid');
        var post_data = {
            'se_userid': se_userid,
            'userid': userid,
            'password': md5(new_password)
        };
        $.ajax({
            url: '/channel_op/v1/api/user_change_password',
            type: 'POST',
            dataType: 'json',
            data: post_data,
            success: function(data) {
                var respcd = data.respcd;
                if(respcd != '0000'){
                    var resperr = data.resperr;
                    var respmsg = data.respmsg;
                    var msg = resperr ? resperr : respmsg;
                    toastr.warning(msg);
                    return false;
                } else {
                    $("#ModifyPassWord").modal('hide');
                    toastr.success('修改密码成功');
                }
            },
            error: function(data) {
                toastr.warning('请求数据异常');
            }
        });

    })
});
