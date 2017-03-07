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
	           'maxnum': data.length,
            }
            var device_name = $("#deviceName").val();
            if(device_name!=''&&device_name!=undefined){
                get_data.device_name = device_name;
            }

            var serial_number = $("#deviceSerialNu").val();
            if(serial_number!=''&&serial_number!=undefined){
                get_data.serial_number = serial_number;
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
                        var respmsg = data.resmsg;
                        var msg = resperr ? resperr : resmsg;
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
	            },

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

    $("#deviceCreate").click(function(){
        $("#deviceCreateForm").resetForm();
        $("#deviceCreateModal").modal();
    });

    $("#deviceSearch").click(function(){
        $('#deviceList').DataTable().draw();
    });

    $("#deviceCreateSubmit").click(function(){
       var queryString = $('#deviceCreateForm').formSerialize();
       alert(queryString);
    });

});
