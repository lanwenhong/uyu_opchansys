$(document).ready(function(){
    $('#trainUseList').DataTable({
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
            var $trainUseList_length = $("#trainUseList_length");
            var $trainUseList_paginate = $("#trainUseList_paginate");
            var $page_top = $('.top');

            $page_top.addClass('row');
            $trainUseList_paginate.addClass('col-md-8');
            $trainUseList_length.addClass('col-md-4');
            $trainUseList_length.prependTo($page_top);
        },
        "ajax": function(data, callback, settings){
            var get_data = {
	           'page': Math.ceil(data.start / data.length) + 1,
	           'maxnum': data.length,
            }
            var channel_name = $("#channelName").val();
            if(channel_name!=''&&channel_name!=undefined){
                get_data.channel_name = channel_name;
            }

            var store_name = $("#storeName").val();
            if(store_name!=''&&store_name!=undefined){
                get_data.store_name = store_name;
            }

            var consumer_mobile = $("#consumerMobile").val();
            if(consumer_mobile!=''&&consumer_mobile!=undefined){
                get_data.consumer_mobile = consumer_mobile;
            }

            var eyesight = $("#eyeSight").val();
            if(eyesight!=''&&eyesight!=undefined){
                get_data.eyesight = eyesight;
            }

            var create_time = $("#createTime").val();
            if(create_time!=''&&create_time!=undefined){
                get_data.create_time = create_time;
            }

            $.ajax({
	            url: '/channel_op/v1/api/training_use_list',
	            type: 'GET',
	            dataType: 'json',
	            data: get_data,
	            success: function(data) {
                    var respcd = data.respcd;
                    if(respcd != '0000'){
                        $processing = $("#trainBuyerList_processing");
                        $processing.css('display', 'none');
                        var resperr = data.resperr;
                        var respmsg = data.resmsg;
                        var msg = resperr ? resperr : resmsg;
                        toastr.warning(msg);
                        return false;
                    }
	                detail_data = data.data;
	                num = detail_data.num;
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
				{ data: 'channel_name' },
				{ data: 'store_name' },
				{ data: 'device_name' },
				{ data: 'consumer_id' },
				{ data: 'eyesight_name' },
				{ data: 'comsumer_nums' },
				{ data: 'create_time' },
				{ data: 'status' },
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

    $("#useSearch").click(function(){
        $('#trainUseList').DataTable().draw();
    });
});
