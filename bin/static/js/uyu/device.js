$(document).ready(function(){
    $('#deviceList').DataTable({
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
            var $deviceList_length = $("#deviceList_length");
            var $deviceList_paginate = $("#deviceList_paginate");
            var $page_top = $('.top');

            $page_top.addClass('row');
            $deviceList_paginate.addClass('col-md-8');
            $deviceList_length.addClass('col-md-4');
            $deviceList_length.prependTo($page_top);
        },
        "ajax": function(data, callback, settings){
            var get_data = {
	           'page': Math.ceil(data.start / data.length) + 1,
	           'maxnum': data.length
            };

            var serial_number = $("#s_device_serial_nu").val();
            if(serial_number){
                get_data.serial_number = serial_number;
            }

            var channel_name = $('#s_channel_name').val();
            if(channel_name){
                get_data.channel_name = channel_name;
            }

            var store_name = $('#s_store_name').val();
            if(store_name){
                get_data.store_name = store_name;
            }

            $.ajax({
	            url: '/channel_op/v1/api/devinfo_pagelist',
	            type: 'GET',
	            dataType: 'json',
	            data: get_data,
	            success: function(data) {
                    var respcd = data.respcd;
                    if(respcd != '0000'){
                        $processing = $("#deviceList_processing");
                        $processing.css('display', 'none');
                        var resperr = data.resperr;
                        var respmsg = data.respmsg;
                        var msg = resperr ? resperr : respmsg;
                        toastr.warning(msg);
                        return false;
                    }
	                var detail_data = data.data;
	                var num = detail_data.num;
                    console.log('num:'+num);
                    console.log('info:'+detail_data.info);
	                callback({
	                    recordsTotal: num,
	                    recordsFiltered: num,
	                    data: detail_data.info
	                });
	            },
	            error: function(data) {
	                toastr.warning('请求数据异常');
	            }

            });
        },
		'columns': [
				{ data: 'id' },
				{ data: 'device_name' },
				{ data: 'serial_number' },
				{ data: 'hd_version' },
				{ data: 'blooth_tag' },
				{ data: 'scm_tag' },
				{ data: 'status' },
				{ data: 'channel_name' },
				{ data: 'store_name' },
				{ data: 'training_nums' },
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

    $("#deviceCreate").click(function(){
        $('#channel_name').html('');
        $("#deviceCreateForm").resetForm();
        channel_name_select();
        $("#deviceCreateModal").modal();
    });

    $("#deviceSearch").click(function(){
        $('#deviceList').DataTable().draw();
    });

    $("#deviceCreateSubmit").click(function(){
        var device_vt = $('#deviceCreateForm').validate({
            rules: {
                device_name: {
                    required: true,
                    maxlength: 256
                },
                hd_version: {
                    required: true,
                    maxlength: 128
                },
                blooth_tag: {
                    required: true,
                    maxlength: 128
                }
            },
            messages: {
                device_name: {
                    required: '请输入设备名称',
                    maxlength: $.validator.format("请输入一个 长度最多是 {0} 的字符串")
                },
                hd_version: {
                    required: '请输入硬件版本',
                    maxlength: $.validator.format("请输入一个 长度最多是 {0} 的字符串")
                },
                blooth_tag: {
                    required: '请输入蓝牙版本s',
                    maxlength: $.validator.format("请输入一个 长度最多是 {0} 的字符串")
                }
            }
        });

        var ok = device_vt.form();
        if(!ok){
            return false;
        }

        var post_data = {};
        var se_userid = window.localStorage.getItem('myid');
        post_data.se_userid = se_userid;
        post_data.device_name = $('#device_name').val();
        post_data.hd_version = $('#hd_version').val();
        post_data.blooth_tag = $('#blooth_tag').val();
        post_data.scm_tag = $('#scm_tag').val();
        post_data.status = $('#status').val();
        post_data.channel_id = $('#channel_name').val();
        post_data.store_id = $('#store_name').val();

        $.ajax({
            url: '/channel_op/v1/api/create_device',
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
                    toastr.success('新建设备成功');
                    $("#deviceCreateModal").modal('hide');
                    $('#deviceList').DataTable().draw();
                }
            },
            error: function(data) {
                toastr.warning('请求异常');
            }
        });

    });

    $('#channel_name').change(function () {
        var get_data = {};
        var channel_id = $('#channel_name').val();
        var se_userid = window.localStorage.getItem('myid');
        get_data['se_userid'] = se_userid;
        get_data['channel_id'] = channel_id;
        $.ajax({
            url: '/channel_op/v1/api/chan_store_list',
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
                    var c_store_name = $('#store_name');
                    c_store_name.html('');
                    for(var i=0; i<data.data.length; i++){
                        var store_id = data.data[i].id;
                        var store_name = data.data[i].store_name;
                        var option_str = $('<option value='+store_id+'>'+store_name+'</option>');
                        option_str.appendTo(c_store_name);
                    }
                }
            },
            error: function(data) {
                toastr.warning('请求异常');
            }
        });
    });

});


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
                console.log(data.data);
                var c_channel_name = $('#channel_name');
                for(var i=0; i<data.data.length; i++){
                    var channel_id = data.data[i].channel_id;
                    var channel_name = data.data[i].channel_name;
                    var option_str = $('<option value='+channel_id+'>'+channel_name+'</option>');
                    option_str.appendTo(c_channel_name);
                    if(i==0){
                        do_first_select(channel_id);
                    }
                }
            }
        },
        error: function(data) {
            toastr.warning('请求异常');
        }
    });
}

function do_first_select(channel_id) {
    $('#store_name').html('');
    var get_data = {};
    var se_userid = window.localStorage.getItem('myid');
    get_data['se_userid'] = se_userid;
    get_data['channel_id'] = channel_id;
    $.ajax({
        url: '/channel_op/v1/api/chan_store_list',
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
                console.log(data.data);
                var c_store_name = $('#store_name');
                for(var i=0; i<data.data.length; i++){
                    var store_id = data.data[i].id;
                    var store_name = data.data[i].store_name;
                    var option_str = $('<option value='+store_id+'>'+store_name+'</option>');
                    option_str.appendTo(c_store_name);
                }
            }
        },
        error: function(data) {
            toastr.warning('请求异常');
        }
    });
}
