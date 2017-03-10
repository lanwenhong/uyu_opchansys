$(document).ready(function(){
    var table = $('#channelList').DataTable({
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
        "lengthMenu": [[10, 20, 40, 80, 100, -1],[10, 20, 40, 80, 100, '所有']],
        "dom": 'l<"top"p>rt',
        "fnInitComplete": function(){
            var $channelList_length = $("#channelList_length");
            var $channelList_paginate = $("#channelList_paginate");
            var $page_top = $('.top');

            $page_top.addClass('row');
            $channelList_paginate.addClass('col-md-8');
            $channelList_length.addClass('col-md-4');
            $channelList_length.prependTo($page_top);
        },
        "ajax": function(data, callback, settings){
            var get_data = {
	           'page': Math.ceil(data.start / data.length) + 1,
	           'maxnum': data.length,
            }
            var nick_name = $("#channelName").val();
            if(nick_name!=''&&nick_name!=undefined){
                get_data.nick_name = nick_name;
            }
            $.ajax({
	            url: '/channel_op/v1/api/chninfo_pagelist',
	            type: 'GET',
	            dataType: 'json',
	            data: get_data,
	            success: function(data) {
                    var respcd = data.respcd;
                    if(respcd != '0000'){
                        $processing = $("#channelList_processing");
                        $processing.css('display', 'none');
                        var resperr = data.resperr;
                        var respmsg = data.resmsg;
                        var msg = resperr ? resperr : resmsg;
                        toastr.warning(msg);
                        return false;
                    }
	                detail_data = data.data;
	                num = detail_data.num;
	                callback({
	                    recordsTotal: num,
	                    recordsFiltered: num,
	                    data: detail_data.info
	                });
	            },
	            error: function(data) {
	            },

            });
        },
        'columnDefs': [
            {
                targets: 9,
                data: '操作',
                render: function(data, type, full) {
                    var status = full.is_valid;
                    var uid =full.userid;
                    var channel_id =full.id;
                    var msg = status ? '打开' : '关闭';
                    var op = "<input type='button' class='btn btn-info btn-sm setStatus' data-channelid="+uid+" value="+msg+ " data-status="+status+">";
                    var view ="<input type='button' class='btn btn-primary btn-sm viewEdit' data-uid="+uid+" value="+'查看'+ " data-channelid="+channel_id+">";
                    return op+view;
                }
            }
        ],
		'columns': [
				{ data: 'id' },
				{ data: 'nick_name' },
				{ data: 'contact_name' },
				{ data: 'contact_phone' },
				{ data: 'training_amt_per' },
				{ data: 'divide_percent' },
				{ data: 'remain_times' },
				{ data: 'is_valid' },
				{ data: 'ctime' },
		],
        'oLanguage': {
            'sProcessing': '<span style="color:red;">加载中....</span>',
            'sLengthMenu': '每页显示_MENU_条记录',
            'sInfo': '显示 _START_到_END_ 的 _TOTAL_条数据',
            'sInfoEmpty': '没有匹配的数据',
            'sZeroRecords': '没有找到匹配的数据',
            'oPaginate': {
                'sFirst': '首页',
                'sPrevious': '前一页',
                'sNext': '后一页',
                'sLast': '尾页',
            },
        },
    });


	$("#channelCreate").click(function(){
        $("#channelCreateForm").resetForm();
		$("#channelCreateModal").modal();
	});

    $("#channelNameSearch").click(function(){
        $('#channelList').DataTable().draw();
    });

    $("#channelCreateSubmit").click(function(){
        var se_userid = window.localStorage.getItem('myid');
        var queryString = $('#channelCreateForm').formSerialize();
        var post_data = query_to_obj(queryString);
        post_data['se_userid'] = se_userid;
        $.ajax({
	        url: '/channel_op/v1/api/channel_create',
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
                }
                else {
                    toastr.success('新建渠道成功');
		            $("#channelCreateModal").modal('hide');
                    $('#channelList').DataTable().draw();
                }
	        },
	        error: function(data) {
                toastr.warning('请求异常');
	        },
        });
    });


    $(document).on('click', '.viewEdit', function(){
        var uid = $(this).data('uid');
        var channel_id = $(this).data('channelid');
        var se_userid = window.localStorage.getItem('myid');
        var get_data = {
            'userid': uid,
            'se_userid': se_userid,
        }
        $.ajax({
	        url: '/channel_op/v1/api/channel',
	        type: 'GET',
	        dataType: 'json',
	        data: get_data,
	        success: function(data) {
                var respcd = data.respcd;
                if(respcd != '0000'){
                    var resperr = data.resperr;
                    var respmsg = data.resmsg;
                    var msg = resperr ? resperr : resmsg;
                    toastr.warning(msg);
                }
                else {
                    toastr.success('get data ok');
                    var p_data = data.data.profile;
                    var ch_data = data.data.chn_data;
                    var u_data = data.data.u_data;
                    console.log('U_data');
                    console.log(u_data);
                    $('#uid').text(uid);
                    $('#e_channel_id').val(channel_id);
                    $('#e_login_name').val(u_data.login_name);
                    $('#e_phone_num').val(u_data.phone_num);
                    $('#e_channel_name').val(ch_data.channel_name);
                    $('#e_create_time').val(ch_data.ctime);
                    $('#e_legal_person').val(p_data.legal_person);
                    $('#e_org_code').val(p_data.org_code);
                    $('#e_license_id').val(p_data.license_id);
                    $('#e_email').val(u_data.email);
                    $('#e_business').val(p_data.business);
                    $('#e_front_business').val(p_data.front_business);
                    $('#e_account_name').val(p_data.account_name);
                    $('#e_bank_account').val(p_data.bank_account);
                    $('#e_bank_name').val(p_data.bank_name);
                    $('#e_contact_name').val(p_data.contact_name);
                    $('#e_contact_phone').val(p_data.contact_phone);
                    $('#e_contact_email').val(p_data.contact_email);
                    $('#e_address').val(p_data.address);
                    $('#e_training_amt_per').val(ch_data.training_amt_per);
                    $('#e_is_prepayment').val(ch_data.is_prepayment);
                    $('#e_divide_percent').val(ch_data.divide_percent);
                    $("#channelEditModal").modal();
                }
	        },
	        error: function(data) {
                toastr.warning('请求异常');
	        },
        });
    });


    $(document).on('click', '.setStatus', function(){
        var uid = $(this).data('channelid');
        var status = $(this).data('status');
        var value = status ? 0 : 1
        var se_userid = window.localStorage.getItem('myid');
        var post_data = {
            'userid': uid,
            'state': value,
            'se_userid': se_userid,
        }
        $.ajax({
	        url: '/channel_op/v1/api/channel_set_state',
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
                }
                else {
                    $('#channelList').DataTable().draw();
                    toastr.success('ok');
                }
	        },
	        error: function(data) {
                toastr.warning('请求异常');
	        },
        });

    });

    $('#channelEditSubmit').click(function(){
        var uid = $('#uid').text();
        var se_userid = window.localStorage.getItem('myid');
        var queryString = $('#channelEditForm').formSerialize();
        var post_data = query_to_obj(queryString);
        post_data['se_userid'] = se_userid;
        post_data['userid'] = uid;
        $.ajax({
	        url: '/channel_op/v1/api/channel',
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
                }
                else {
                    toastr.success('保存修改成功');
                    $("#channelEditForm").resetForm();
                    $("#channelEditModal").modal('hide');
                    $('#channelList').DataTable().draw();
                }
	        },
	        error: function(data) {
                toastr.warning('请求异常');
	        },
        });
    });

});


function print_object(obj){
    var temp = ""
    for(var key in obj){
        temp += key + ":" + obj[key] + "\n";
    }
}


function query_to_obj(queryString){
    var arr = queryString.split('&');
    var post_data = new Object();
    for(var i=0; i<arr.length; i++){
        var tmp = arr[i].split('=');
        post_data[tmp[0]] = tmp[1];
    }
    return post_data;
}
