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
            var channel_name = $("#channelName").val();
            var store_name = $("#storeName").val();
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
                    var status = full.is_valid;
                    var uid =full.userid;
                    var store_id =full.id;
                    var msg = status ? '打开' : '关闭';
                    var op = "<input type='button' class='btn btn-info btn-sm setStatus' data-uid="+uid+" value="+msg+ " data-status="+status+">";
                    var view ="<input type='button' class='btn btn-primary btn-sm viewEyesight' data-uid="+uid+" value="+'查看'+ " data-storeid="+store_id+">";
                    return op+view;
                }
            }
        ],
		'columns': [
				{ data: 'id' },
				{ data: 'channel_name' },
				{ data: 'nick_name' },
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
        var se_userid = window.localStorage.getItem('myid');
        var queryString = $('#storeCreateForm').formSerialize();
        var post_data = query_to_obj(queryString);
        post_data['se_userid'] = se_userid;
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

    $(document).on('click', '.viewEyesight', function(){
        var uid = $(this).data('uid');
        var store_id = $(this).data('storeid');
        var se_userid = window.localStorage.getItem('myid');
        var get_data = {
            'userid': uid,
            'se_userid': se_userid,
            'store_id': store_id,
        }
        $.ajax({
	        url: '/channel_op/v1/api/eyesight_list',
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
                    toastr.success('ok');
                    var sight_data = data.data.info;
                    var table = $('#EyeSightList');
                    for(var i=0; i<sight_data.length; i++){
                        var index = i+1;
                        var nick_name = sight_data[i].nick_name;
                        var phone_num = sight_data[i].phone_num;
                        var ctime = sight_data[i].ctime;
                        var is_valid = sight_data[i].is_valid;
                        var row = '<td>'+index+'</td>';
                        row += '<td>'+nick_name+'</td>';
                        row += '<td>'+phone_num+'</td>';
                        row += '<td>'+ctime+'</td>';
                        row += '<td>'+is_valid+'</td>';
                        var btn = '<button type="button" class="btn btn-primary btn-sm">删除</button>';
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


});
