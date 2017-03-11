$(document).ready(function(){
    $('#storeList').DataTable({
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
            var $storeList_length = $("#storeList_length");
            var $storeList_paginate = $("#storeList_paginate");
            var $page_top = $('.top');

            $page_top.addClass('row');
            $storeList_paginate.addClass('col-md-8');
            $storeList_length.addClass('col-md-4');
            $storeList_length.prependTo($page_top);
        },
        "ajax": function(data, callback, settings){
            var get_data = {
	           'page': Math.ceil(data.start / data.length) + 1,
	           'maxnum': data.length,
            }
            var channel_name = $("#channel_name").val();
            var store_name = $("#store_name").val();
            if(channel_name!=''&&channel_name!=undefined){
                get_data.channel_name = channel_name;
            }
            if(store_name!=''&&store_name!=undefined){
                get_data.store_name = store_name;
            }
            $.ajax({
	            url: '/channel_op/v1/api/storeinfo_pagelist',
	            type: 'GET',
	            dataType: 'json',
	            data: get_data,
	            success: function(data) {
                    var respcd = data.respcd;
                    if(respcd != '0000'){
                        $processing = $("#storeList_processing");
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
                targets: 12,
                data: '操作',
                render: function(data, type, full) {
                    var status = full.status;
                    var uid =full.userid;
                    var store_id =full.id;
                    var channel_id =full.channel_id;
                    var msg = status ? '打开' : '关闭';
                    var op = "<input type='button' class='btn btn-info btn-sm setStatus' data-uid="+uid+" value="+msg+ " data-status="+status+">";
                    var view ="<input type='button' class='btn btn-primary btn-sm viewStore' data-uid="+uid+" value="+'查看门店'+ " data-storeid="+store_id+">";
                    var view_eye ="<input type='button' class='btn btn-primary btn-sm viewEyesight' data-uid="+uid+" value="+'查看视光师'+ " data-storeid="+store_id+ " data-channel_id="+channel_id+ ">";
                    var add_eye ="<input type='button' class='btn btn-primary btn-sm addEyesight' data-channelid="+channel_id+" value="+'添加视光师'+ " data-storeid="+store_id+">";
                    return op+view+view_eye+add_eye;
                }
            }
        ],
		'columns': [
				{ data: 'id' },
				{ data: 'channel_name' },
				{ data: 'store_name' },
				{ data: 'store_type' },
				{ data: 'contact_name' },
				{ data: 'store_mobile' },
				{ data: 'store_addr' },
				{ data: 'training_amt_per' },
				{ data: 'divide_percent' },
				{ data: 'remain_times' },
				{ data: 'is_valid' },
				{ data: 'create_time' },
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
                'sLast': '尾页',
            },
        }

    });

    $("#storeCreate").click(function(){
        $("#storeCreateForm").resetForm();
        $("#storeCreateModal").modal();
    });

    $("#storeSearch").click(function(){
        $('#storeList').DataTable().draw();
    });

    $("#storeCreateSubmit").click(function(){
        var post_data = {}
        var se_userid = window.localStorage.getItem('myid');
        post_data['se_userid'] = se_userid;
		var login_name = $('#login_name').val();
		var phone_num = $('#phone_num').val();
		var email = $('#email').val();
		var org_code = $('#org_code').val();
		var license_id = $('#license_id').val();
		var legal_person = $('#legal_person').val();
		var account_name = $('#account_name').val();
		var bank_name = $('#bank_name').val();
		var bank_account = $('#bank_account').val();
		var contact_name= $('#contact_name').val();
		var contact_phone= $('#contact_phone').val();
		var contact_email= $('#contact_email').val();
		var address= $('#address').val();
        var store_name = $('#store_name').val();
        var store_contacter = $('#store_contacter').val();
        var store_mobile = $('#store_mobile').val();
        var store_addr = $('#store_addr').val();
		var training_amt_per= $('#training_amt_per').val();
		var divide_percent= $('#divide_percent').val();
		var business = $('#business').val();
		var front_business = $('#front_business').val();
		var channel_id = $('#channel_id').val();
        post_data['se_userid'] = se_userid;
		post_data['login_name'] = login_name;
		post_data['phone_num'] = phone_num;
		post_data['email'] = email;
		post_data['org_code'] = org_code;
		post_data['license_id'] = license_id;
		post_data['legal_person'] = legal_person;
		post_data['account_name'] = account_name;
		post_data['bank_name'] = bank_name;
		post_data['bank_account'] = bank_account;
		post_data['contact_name'] = contact_name;
		post_data['contact_phone'] = contact_phone;
		post_data['contact_email'] = contact_email;
		post_data['address'] = address;
		post_data['store_name'] = store_name;
		post_data['store_contacter'] = store_contacter;
		post_data['store_mobile'] = store_mobile;
		post_data['store_addr'] = store_addr;
		post_data['training_amt_per'] = training_amt_per;
		post_data['divide_percent'] = divide_percent;
		post_data['business'] = business;
		post_data['front_business'] = front_business;
		post_data['channel_id'] = channel_id;
        var flag = check_obj_val(post_data);
        if(!flag){
            toastr.warning('请核实输入字段内容');
            return false;
        }
        $.ajax({
	        url: '/channel_op/v1/api/store_create',
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
                    toastr.success('新建成功');
                    $("#storeCreateForm").resetForm();
                    $("#storeCreateModal").modal('hide');
                    $('#storeList').DataTable().draw();
                }
	        },
	        error: function(data) {
                toastr.warning('请求异常');
	        },
         });
    });

    $(document).on('click', '.setStatus', function(){
        var uid = $(this).data('uid');
        var status = $(this).data('status');
        var value = status ? 0 : 1
        var se_userid = window.localStorage.getItem('myid');
        var post_data = {
            'userid': uid,
            'state': value,
            'se_userid': se_userid,
        }
        $.ajax({
	        url: '/channel_op/v1/api/store_set_state',
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
                    $('#storeList').DataTable().draw();
                    toastr.success('操作成功');
                }
	        },
	        error: function(data) {
                toastr.warning('请求异常');
	        },
        });
    });

    $(document).on('click', '.viewStore', function(){
        var uid = $(this).data('uid');
        var store_id = $(this).data('storeid');
        var se_userid = window.localStorage.getItem('myid');
        var get_data = {
            'userid': uid,
            'se_userid': se_userid,
        }
        $.ajax({
	        url: '/channel_op/v1/api/store',
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
                    console.log(data.data);
                    var p_data = data.data.profile;
                    var ch_data = data.data.chn_data;
                    var u_data = data.data.u_data;
                    console.log(p_data);
                    console.log(ch_data);
                    console.log(u_data);
                    $('#uid').text(uid);
                    $('#e_login_name').val(u_data.phone_num);
                    $('#e_phone_num').val(u_data.phone_num);
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
                    $('#e_store_name').val(ch_data.store_name);
                    $('#e_store_contacter').val(ch_data.store_contacter);
                    $('#e_store_mobile').val(ch_data.store_mobile);
                    $('#e_store_addr').val(ch_data.store_addr);
                    $('#storeEditModal').modal();
                }
	        },
	        error: function(data) {
                toastr.warning('请求数据异常');
	        },

        });

    })

    $(document).on('click', '.addEyesight', function(){
        $('#eye_phone_num').val('');
        $('#nick_name').val('');
        $('#username').val('');
        var channel_id = $(this).data('channelid');
        var store_id = $(this).data('storeid');
        console.log('channelid: '+channel_id);
        console.log('storeid: '+store_id);
        $('#span_channel_id').text(channel_id);
        $('#span_store_id').text(store_id);
        $('#addEyesight').modal();
    })

    $(document).on('click', '.viewEyesight', function(){
        var uid = $(this).data('uid');
        var store_id = $(this).data('storeid');
        var channel_id = $(this).data('channel_id');
        var se_userid = window.localStorage.getItem('myid');
        var get_data = {
            'userid': uid,
            'se_userid': se_userid,
            'store_id': store_id,
            'channel_id': channel_id,
        }
        console.log('get_data');
        console.log(get_data);
        $.ajax({
	        url: '/channel_op/v1/api/eyesight_info',
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
                    var sight_data = data.data.info;
                    var table = $('#EyeSightList');
                    var tbody = $('#EyeSightList tbody');
                    tbody.html("");
                    for(var i=0; i<sight_data.length; i++){
                        var index = i+1;
                        var nick_name = sight_data[i].nick_name;
                        var phone_num = sight_data[i].phone_num;
                        var ctime = sight_data[i].ctime;
                        var is_valid = sight_data[i].is_valid;
                        var eyeid = sight_data[i].eyesight_id;
                        var storeid = sight_data[i].store_id;
                        var row = '<td>'+index+'</td>';
                        row += '<td>'+nick_name+'</td>';
                        row += '<td>'+phone_num+'</td>';
                        row += '<td>'+ctime+'</td>';
                        row += '<td>'+is_valid+'</td>';
                        // var btn = '<button type="button" class="btn btn-primary btn-sm" id="deleteEyesight">删除</button>';
                        // var btn = '<button type="button" class="btn btn-primary btn-sm" id="deleteEyesight" data-eyeid="'+eyeid+'" data-storeid="'+storeid+'">删除</button>'
                        var btn = '<button type="button" class="btn btn-primary btn-sm" id="deleteEyesight" data-eyeid="'+eyeid+'" data-storeid="'+storeid+'" data-channel_id="'+channel_id+'" >删除</button>'
                        row += '<td>'+btn+'</td>';
                        var tr = $('<tr>'+row+'</tr>');
                        console.log(tr);
                        tr.appendTo(table);
                        row = '';
                    }
                }
	        },
	        error: function(data) {
                toastr.warning('请求异常');
	        },
        });
        $("#viewEyeSightModal").modal();
    });


    $('#storeEditSubmit').click(function(){
        var post_data = {}
        var uid = $('#uid').text();
        var se_userid = window.localStorage.getItem('myid');
        post_data['se_userid'] = se_userid;
        post_data['userid'] = uid;
		var login_name = $('#e_login_name').val();
		var phone_num = $('#e_phone_num').val();
		var email = $('#e_email').val();
		var org_code = $('#e_org_code').val();
		var license_id = $('#e_license_id').val();
		var legal_person = $('#e_legal_person').val();
		var account_name = $('#e_account_name').val();
		var bank_name = $('#e_bank_name').val();
		var bank_account = $('#e_bank_account').val();
		var contact_name= $('#e_contact_name').val();
		var contact_phone= $('#e_contact_phone').val();
		var contact_email= $('#e_contact_email').val();
		var address= $('#e_address').val();
        var store_name = $('#e_store_name').val();
        var store_contacter = $('#e_store_contacter').val();
        var store_mobile = $('#e_store_mobile').val();
        var store_addr = $('#e_store_addr').val();
		var training_amt_per= $('#e_training_amt_per').val();
		var divide_percent= $('#e_divide_percent').val();
		var business = $('#e_business').val();
		var front_business = $('#e_front_business').val();
        post_data['se_userid'] = se_userid;
		post_data['login_name'] = login_name;
		post_data['phone_num'] = phone_num;
		post_data['email'] = email;
		post_data['org_code'] = org_code;
		post_data['license_id'] = license_id;
		post_data['legal_person'] = legal_person;
		post_data['account_name'] = account_name;
		post_data['bank_name'] = bank_name;
		post_data['bank_account'] = bank_account;
		post_data['contact_name'] = contact_name;
		post_data['contact_phone'] = contact_phone;
		post_data['contact_email'] = contact_email;
		post_data['address'] = address;
		post_data['store_name'] = store_name;
		post_data['store_contacter'] = store_contacter;
		post_data['store_mobile'] = store_mobile;
		post_data['store_addr'] = store_addr;
		post_data['training_amt_per'] = training_amt_per;
		post_data['divide_percent'] = divide_percent;
		post_data['business'] = business;
		post_data['front_business'] = front_business;
        var flag = check_obj_val(post_data);
        if(!flag){
            toastr.warning('请核实输入字段内容');
            return false;
        }
        console.log('post data');
        console.log(post_data);
        $.ajax({
	        url: '/channel_op/v1/api/store',
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
                }
                else {
                    toastr.success('修改成功');
                    $('#storeEditModal').modal('hide');
                    $("#storeEditForm").resetForm();
                    $('#storeList').DataTable().draw();
                }
	        },
	        error: function(data) {
                toastr.success('请求异常');
	        },

        });
    });

    $(document).on('click', '#deleteEyesight', function(){
        var se_userid = window.localStorage.getItem('myid');
        var eyesight_id = $(this).data('eyeid');
        var store_id = $(this).data('storeid');
        var channel_id = $(this).data('channel_id');
        var post_data = {}
        post_data['se_userid'] = se_userid;
        post_data['userid'] = eyesight_id;
        post_data['store_id'] = store_id;
        post_data['channel_id'] = channel_id;
        console.log('delete ...');
        console.log(post_data);
        $.ajax({
	        url: '/channel_op/v1/api/eyesight_info',
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
                }
                else {
                    $('#viewEyeSightModal').modal('hide');
                    toastr.success('解绑成功');
                }
	        },
	        error: function(data) {
                toastr.success('请求异常');
	        },
        });
    });

    $('#find_phone').click(function(){
        var se_userid = window.localStorage.getItem('myid');
        var phone_num = $('#eye_phone_num').val();
        if(!phone_num){
            toastr.warning('请输入手机号');
        }
        var get_data = {
            'phone_num': phone_num,
            'se_userid': se_userid,
        }
        $.ajax({
	        url: '/channel_op/v1/api/store_eye',
	        type: 'GET',
	        dataType: 'json',
	        data: get_data,
	        success: function(data) {
                var respcd = data.respcd;
                if(respcd != '0000'){
                    var resperr = data.resperr;
                    var respmsg = data.resmsg;
                    var msg = resperr ? resperr : resmsg;
                    $('#eyesight_id').text('');
                    $('#nick_name').val('');
                    $('#username').val('');
                    toastr.warning(msg);
                }
                else {
                    var u_data = data.data;
                    var nick_name= u_data.nick_name;
                    var username = u_data.username;
                    var eyesight_id = u_data.id;
                    $('#eyesight_id').text(eyesight_id);
                    $('#nick_name').val(nick_name);
                    $('#username').val(username);
                }
	        },
	        error: function(data) {
                toastr.success('请求异常');
	        },

        });
    });

    $('#addEyesightSubmit').click(function(){
        var se_userid = window.localStorage.getItem('myid');
        var channel_id = $('#span_channel_id').text();
        var store_id = $('#span_store_id').text();
        var eyesight_id = $('#eyesight_id').text();
        var post_data = {
            'channel_id': channel_id,
            'store_id': store_id,
            'userid': eyesight_id,
            'se_userid': se_userid
        }
        var phone_num = $('#eye_phone_num').val();
        var nick_name = $('#nick_name').val();
        if(!phone_num || !nick_name){
            toastr.warning('请核实手机号和昵称');
            return false;
        }
        $.ajax({
	        url: '/channel_op/v1/api/store_eye',
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
                }
                else {
                    $('#addEyesight').modal('hide');
                    toastr.success('添加成功');
                }
	        },
	        error: function(data) {
                toastr.success('请求异常');
	        },

        });
    })
});
