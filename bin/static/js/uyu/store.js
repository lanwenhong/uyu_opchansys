$(document).ready(function(){
    search_source();

    $.validator.addMethod("isMobile", function(value, element) {
        var length = value.length;
        var mobile = /^(1\d{10})$/;
        return this.optional(element) || (length == 11 && mobile.test(value));
    }, "请正确填写您的手机号码");

    $.validator.addMethod("isYuan", function(value, element) {
        var length = value.length;
        var yuan  = /^([0-9]{1,6})\.([0-9]{1,2})$/;
        return this.optional(element) || (length && yuan.test(value));
    }, "请正确填写您的价格");

    $.validator.addMethod("isLessOne", function(value, element) {
        var length = value.length;
        var less_one  = /^(0)\.([0-9]{1,2})$/;
        return this.optional(element) || (length && less_one.test(value));
    }, "请正确填写您的比例");

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
        "lengthMenu": [[10, 40, 100],[10, 40, 100]],
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
	           'maxnum': data.length
            };
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
                        var respmsg = data.respmsg;
                        var msg = resperr ? resperr : respmsg;
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
	                toastr.warning('获取数据异常');
	                return false;
	            }

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
                    var is_prepayment = full.is_prepayment;
                    var msg = status ? '打开' : '关闭';
                    var op = "<input type='button' class='btn btn-info btn-sm setStatus' data-uid="+uid+" value="+msg+ " data-status="+status+">";
                    var view ="<input type='button' class='btn btn-primary btn-sm viewStore' data-uid="+uid+" value="+'查看门店'+ " data-storeid="+store_id+ " data-is_prepayment="+is_prepayment+ ">";
                    var view_eye ="<input type='button' class='btn btn-primary btn-sm viewEyesight' data-uid="+uid+" value="+'查看视光师'+ " data-storeid="+store_id+ " data-channel_id="+channel_id+ ">";
                    var add_eye ="<input type='button' class='btn btn-primary btn-sm addEyesight' data-channelid="+channel_id+" value="+'添加视光师'+ " data-storeid="+store_id+">";
                    return op+view+view_eye+add_eye;
                }
            }
        ],
		'columns': [
				{ data: 'id' },
				{ data: 'channel_name' },
                { data: 'phone_num' },
				{ data: 'store_name' },
				{ data: 'store_type' },
				{ data: 'store_contacter' },
				{ data: 'store_addr' },
				{ data: 'training_amt_per' },
				{ data: 'divide_percent' },
				{ data: 'remain_times' },
				{ data: 'is_valid' },
				{ data: 'create_time' }
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

    $("#storeCreate").click(function(){
        $("#storeCreateForm").resetForm();
        $("#c_channel_name").html('');
        $("label.error").remove();
        channel_name_select();
        $("#storeCreateModal").modal();
    });

    $("#storeSearch").click(function(){
        $('#storeList').DataTable().draw();
    });

    $("#storeCreateSubmit").click(function(){

        var store_create_vt = $('#storeCreateForm').validate({
            rules: {
                channel_name: {
                    required: true,
                    maxlength: 256
                },
                phone_num: {
                    required: true,
                    isMobile: '#phone_num'
                },
                address: {
                    required: true,
                    maxlength: 256
                },
                contact_name: {
                    required: true,
                    maxlength: 128
                },
                contact_phone: {
                    required: true,
                    isMobile: '#contact_phone'
                },
                contact_email: {
				    required: false,
                    email: true
                },
                training_amt_per: {
                    required: true,
                    isYuan: '#training_amt_per'
                },
                store_name: {
                    required: true,
                    maxlength: 128
                },
                store_contacter: {
                    required: true,
                    maxlength: 128
                },
                store_mobile: {
                    required: true,
                    isMobile: '#store_mobile'
                },
                store_addr: {
                    required: true,
                    maxlength: 128
                },
                email: {
                    required: false,
                    email: true
                },
                divide_percent: {
                    required: true,
                    isLessOne: '#divide_percent'
                }
            },
            messages: {
                channel_name: {
                    required: '请选择渠道名称',
                    maxlength: $.validator.format("请输入一个 长度最多是 {0} 的字符串")
                },
                phone_num: {
                    required: '请输入手机号'
                },
                address: {
                    required: '请输入地址',
                    maxlength: $.validator.format("请输入一个 长度最多是 {0} 的字符串")
                },
                contact_name: {
                    required: '请输入联系人姓名',
                    maxlength: $.validator.format("请输入一个 长度最多是 {0} 的字符串")
                },
                contact_phone: {
                    required: '请输入联系人手机号'
                },
                contact_email: {
                    email: "请输入正确格式的电子邮件"
                },
                training_amt_per: {
                    required: '请输入单次训练价格',
                    digits: "只能输入整数"
                },
                store_name: {
                    required: '请输入门店名称',
                    maxlength: $.validator.format("请输入一个 长度最多是 {0} 的字符串")
                },
                store_contacter: {
                    required: '请输入门店联系人',
                    maxlength: $.validator.format("请输入一个 长度最多是 {0} 的字符串")
                },
                store_mobile: {
                    required: '请输入门店手机号',
                },
                store_addr: {
                    required: '请输入门店地址',
                    maxlength: $.validator.format("请输入一个 长度最多是 {0} 的字符串")
                },
                email: {
                    email: "请输入正确格式的电子邮件"
                },
                divide_percent: {
                    required: '请输入分成比例',
                }
            }
        });
        var ok = store_create_vt.form();
        if(!ok){
            return false;
        }

        var post_data = {};
        var se_userid = window.localStorage.getItem('myid');
        post_data['se_userid'] = se_userid;
        var phone_num = $('#phone_num').val();
		var login_name = phone_num;
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
        var store_name = $('#c_store_name').val();
        var store_contacter = $('#store_contacter').val();
        var store_mobile = $('#store_mobile').val();
        var store_addr = $('#store_addr').val();
		var training_amt_per= $('#training_amt_per').val() * 100;
		var divide_percent= $('#divide_percent').val();
		var business = $('#business').val();
		var front_business = $('#front_business').val();
		var channel_val = $('.c_channel_name').val();

		channel_id = channel_val.split('|')[0];
		is_prepayment = channel_val.split('|')[1];

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
		post_data['business'] = business;
		post_data['front_business'] = front_business;
		post_data['channel_id'] = channel_id;

        if(is_prepayment == 1){
            if(!divide_percent){
                toastr.warning('分成模式分成比例必填');
                return false;
            }
            post_data['divide_percent'] = divide_percent;
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
                    var respmsg = data.respmsg;
                    var msg = resperr ? resperr : respmsg;
                    toastr.warning(msg);
                    return false;
                }
                else {
                    toastr.success('新建成功');
                    search_source();
                    $("#storeCreateForm").resetForm();
                    $("#storeCreateModal").modal('hide');
                    $('#storeList').DataTable().draw();
                }
	        },
	        error: function(data) {
                toastr.warning('请求异常');
	        }
         });
    });

    $(document).on('click', '.setStatus', function(){
        var uid = $(this).data('uid');
        var status = $(this).data('status');
        var value = status ? 0 : 1;
        var se_userid = window.localStorage.getItem('myid');
        var post_data = {
            'userid': uid,
            'state': value,
            'se_userid': se_userid
        };
        $.ajax({
	        url: '/channel_op/v1/api/store_set_state',
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
                }
                else {
                    $('#storeList').DataTable().draw();
                    toastr.success('操作成功');
                }
	        },
	        error: function(data) {
                toastr.warning('请求异常');
	        }
        });
    });

    $(document).on('click', '.viewStore', function(){
        $("label.error").remove();
        var uid = $(this).data('uid');
        var is_prepayment = $(this).data('is_prepayment');
        $('#prepayment').text(is_prepayment);
        var se_userid = window.localStorage.getItem('myid');
        var get_data = {
            'userid': uid,
            'se_userid': se_userid
        };
        $.ajax({
	        url: '/channel_op/v1/api/store',
	        type: 'GET',
	        dataType: 'json',
	        data: get_data,
	        success: function(data) {
                var respcd = data.respcd;
                if(respcd != '0000'){
                    var resperr = data.resperr;
                    var respmsg = data.respmsg;
                    var msg = resperr ? resperr : respmsg;
                    toastr.warning(msg);
                }
                else {
                    var p_data = data.data.profile;
                    var ch_data = data.data.chn_data;
                    var u_data = data.data.u_data;

                    $('#uid').text(uid);
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
                    $('#e_training_amt_per').val(ch_data.training_amt_per / 100.0);
                    $('#e_is_prepayment').val(ch_data.is_prepayment);
                    if(is_prepayment == 0){
                        $('#edit_store_divide_percent').hide();
                    } else {
                        $('#e_divide_percent').val(ch_data.divide_percent);
                        $('#edit_store_divide_percent').show();
                    }
                    $('#e_store_name').val(ch_data.store_name);
                    $('#e_store_contacter').val(ch_data.store_contacter);
                    $('#e_store_mobile').val(ch_data.store_mobile);
                    $('#e_store_addr').val(ch_data.store_addr);
                    $('#storeEditModal').modal();
                }
	        },
	        error: function(data) {
                toastr.warning('请求数据异常');
	        }
        });

    });

    $(document).on('click', '.addEyesight', function(){
        $('#eye_phone_num').val('');
        $('#nick_name').val('');
        $('#username').val('');
        var channel_id = $(this).data('channelid');
        var store_id = $(this).data('storeid');
        $('#span_channel_id').text(channel_id);
        $('#span_store_id').text(store_id);
        $('#addEyesight').modal();
    });

    $(document).on('click', '.viewEyesight', function(){
        var uid = $(this).data('uid');
        var store_id = $(this).data('storeid');
        var channel_id = $(this).data('channel_id');
        var se_userid = window.localStorage.getItem('myid');
        var get_data = {
            'userid': uid,
            'se_userid': se_userid,
            'store_id': store_id,
            'channel_id': channel_id
        };

        $.ajax({
	        url: '/channel_op/v1/api/eyesight_info',
	        type: 'GET',
	        dataType: 'json',
	        data: get_data,
	        success: function(data) {
                var respcd = data.respcd;
                if(respcd != '0000'){
                    var resperr = data.resperr;
                    var respmsg = data.respmsg;
                    var msg = resperr ? resperr : respmsg;
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

                        var btn = '<button type="button" class="btn btn-primary btn-sm" id="deleteEyesight" data-eyeid="'+eyeid+'" data-storeid="'+storeid+'" data-channel_id="'+channel_id+'" >删除</button>'
                        row += '<td>'+btn+'</td>';
                        var tr = $('<tr>'+row+'</tr>');

                        tr.appendTo(table);
                        row = '';
                    }
                }
	        },
	        error: function(data) {
                toastr.warning('请求异常');
	        }
        });
        $("#viewEyeSightModal").modal();
    });


    $('#storeEditSubmit').click(function(){

        var store_edit_vt = $('#storeEditForm').validate({
            rules: {
                phone_num: {
                    required: true,
                    isMobile: '#phone_num'
                },
                address: {
                    required: true,
                    maxlength: 256
                },
                contact_name: {
                    required: true,
                    maxlength: 128
                },
                contact_phone: {
                    required: true,
                    isMobile: '#e_contact_phone'
                },
                contact_email: {
                    required: false,
                    email: true
                },
                training_amt_per: {
                    required: true,
                    isYuan: '#e_training_amt_per'
                },
                store_name: {
                    required: true,
                    maxlength: 128
                },
                store_contacter: {
                    required: true,
                    maxlength: 128
                },
                store_mobile: {
                    required: true,
                    isMobile: '#store_mobile'
                },
                store_addr: {
                    required: true,
                    maxlength: 128
                },
                email: {
                    required: false,
                    email: true
                },
                divide_percent: {
                    required: true,
                    isLessOne: '#e_divide_percent'
                }
            },
            messages: {
                phone_num: {
                    required: '请输入手机号'
                },
                address: {
                    required: '请输入地址',
                    maxlength: $.validator.format("请输入一个 长度最多是 {0} 的字符串")
                },
                contact_name: {
                    required: '请输入联系人姓名',
                    maxlength: $.validator.format("请输入一个 长度最多是 {0} 的字符串")
                },
                contact_phone: {
                    required: '请输入联系人手机号'
                },
                contact_email: {
                    email: "请输入正确格式的电子邮件"
                },
                training_amt_per: {
                    required: '请输入单次训练价格',
                    digits: "只能输入整数"
                },
                store_name: {
                    required: '请输入门店名称',
                    maxlength: $.validator.format("请输入一个 长度最多是 {0} 的字符串")
                },
                store_contacter: {
                    required: '请输入门店联系人',
                    maxlength: $.validator.format("请输入一个 长度最多是 {0} 的字符串")
                },
                store_mobile: {
                    required: '请输入门店手机号',
                },
                store_addr: {
                    required: '请输入门店地址',
                    maxlength: $.validator.format("请输入一个 长度最多是 {0} 的字符串")
                },
                email: {
                    email: "请输入正确格式的电子邮件"
                },
                divide_percent: {
                    required: '请输入正确的比例'
                }
            }
        });
        var ok = store_edit_vt.form();
        if(!ok){
            return false;
        }

        var post_data = {};
        var uid = $('#uid').text();
        var is_prepayment = $('#prepayment').text();
        var se_userid = window.localStorage.getItem('myid');
        post_data['se_userid'] = se_userid;
        post_data['userid'] = uid;
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
		var training_amt_per= $('#e_training_amt_per').val() * 100;
		var divide_percent= $('#e_divide_percent').val();
		var business = $('#e_business').val();
		var front_business = $('#e_front_business').val();


        post_data['se_userid'] = se_userid;
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

		post_data['business'] = business;
		post_data['front_business'] = front_business;

		if(is_prepayment==1){
		    if(!divide_percent){
                toastr.warning('分成模式分成比例必填');
                return false;
            }
            post_data['divide_percent'] = divide_percent;
        }

        $.ajax({
	        url: '/channel_op/v1/api/store',
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
	        }
        });
    });

    $(document).on('click', '#deleteEyesight', function(){
        var se_userid = window.localStorage.getItem('myid');
        var eyesight_id = $(this).data('eyeid');
        var store_id = $(this).data('storeid');
        var channel_id = $(this).data('channel_id');
        var post_data = {};
        post_data['se_userid'] = se_userid;
        post_data['userid'] = eyesight_id;
        post_data['store_id'] = store_id;
        post_data['channel_id'] = channel_id;

        $.ajax({
	        url: '/channel_op/v1/api/eyesight_info',
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
                }
                else {
                    $('#viewEyeSightModal').modal('hide');
                    toastr.success('解绑成功');
                }
	        },
	        error: function(data) {
                toastr.success('请求异常');
	        }
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
            'se_userid': se_userid
        };
        $.ajax({
	        url: '/channel_op/v1/api/store_eye',
	        type: 'GET',
	        dataType: 'json',
	        data: get_data,
	        success: function(data) {
                var respcd = data.respcd;
                if(respcd != '0000'){
                    var resperr = data.resperr;
                    var respmsg = data.respmsg;
                    var msg = resperr ? resperr : respmsg;
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
                toastr.warning('请求异常');
	        }
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
        };
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
                    var respmsg = data.respmsg;
                    var msg = resperr ? resperr : respmsg;
                    toastr.warning(msg);
                }
                else {
                    $('#addEyesight').modal('hide');
                    toastr.success('添加成功');
                }
	        },
	        error: function(data) {
                toastr.success('请求异常');
	        }
        });
    });

    $('.c_channel_name').change(function () {
        $("label.error").remove();
        var channel_val = $('.c_channel_name').val();
        var is_prepayment = channel_val.split('|')[1];
        if(is_prepayment == 0){
            $('#divide_percent').next('label').remove();
            $('#create_store_divide_percent').hide();
        } else {
            $('#create_store_divide_percent').show();
        }
    });


});

function search_source() {
    var get_data = {};
    var se_userid = window.localStorage.getItem('myid');
    get_data['se_userid'] = se_userid;
    $.ajax({
        url: '/channel_op/v1/api/chan_name_list',
        type: 'GET',
        data: get_data,
        dataType: 'json',
        success: function(data) {
            var respcd = data.respcd;
            if(respcd != '0000'){
                var resperr = data.resperr;
                var respmsg = data.respmsg;
                var msg = resperr ? resperr : respmsg;
                toastr.warning(msg);
            }
            else {
                var subjects = new Array();
                for(var i=0; i<data.data.length; i++){
                    subjects.push(data.data[i].channel_name)
                }
                $('#channel_name').typeahead({source: subjects});
            }
        },
        error: function(data) {
            toastr.warning('请求异常');
        }
    });
    $.ajax({
        url: '/channel_op/v1/api/store_name_list',
        type: 'GET',
        data: get_data,
        dataType: 'json',
        success: function(data) {
            var respcd = data.respcd;
            if(respcd != '0000'){
                var resperr = data.resperr;
                var respmsg = data.respmsg;
                var msg = resperr ? resperr : respmsg;
                toastr.warning(msg);
            }
            else {
                $('#store_name').typeahead({source: data.data});
            }
        },
        error: function(data) {
            toastr.warning('请求异常');
        }
    });
}

function channel_name_select() {
    var get_data = {};
    var se_userid = window.localStorage.getItem('myid');
    get_data['se_userid'] = se_userid;
    $.ajax({
        url: '/channel_op/v1/api/chan_name_list',
        type: 'GET',
        data: get_data,
        dataType: 'json',
        success: function(data) {
            var respcd = data.respcd;
            if(respcd != '0000'){
                var resperr = data.resperr;
                var respmsg = data.respmsg;
                var msg = resperr ? resperr : respmsg;
                toastr.warning(msg);
            }
            else {
                var c_channel_name = $('.c_channel_name');
                for(var i=0; i<data.data.length; i++){
                    var channel_id = data.data[i].channel_id;
                    var channel_name = data.data[i].channel_name;
                    var is_prepayment = data.data[i].is_prepayment;
                    channel_id = channel_id + '|' + is_prepayment;
                    var option_str = $('<option value='+channel_id+'>'+channel_name+'</option>');
                    option_str.appendTo(c_channel_name);
                    if(i==0){
                        if(is_prepayment == 0){
                            $('#create_store_divide_percent').hide();
                        } else {
                            $('#create_store_divide_percent').show();
                        }
                    }
                }
            }
        },
        error: function(data) {
            toastr.warning('请求异常');
        }
    });
}
