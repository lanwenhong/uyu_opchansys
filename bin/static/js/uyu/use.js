$(document).ready(function(){

    search_source();

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
        "lengthMenu": [[10, 40, 100],[10, 40, 100]],
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
            };

            var se_userid = window.localStorage.getItem('myid');
            get_data.se_userid = se_userid;

            var channel_name = $("#s_channel_name").val();
            if(channel_name){
                get_data.channel_name = channel_name;
            }

            var store_name = $("#s_store_name").val();
            if(store_name){
                get_data.store_name = store_name;
            }

            var consumer_mobile = $("#s_consumer").val();
            if(consumer_mobile){
                get_data.consumer_mobile = consumer_mobile;
            }

            var eyesight = $("#s_eyesight").val();
            if(eyesight){
                get_data.eyesight = eyesight;
            }

            var create_time = $("#start_time").val();
            if(create_time){
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
		'columns': [
				{ data: 'id' },
				{ data: 'channel_name' },
				{ data: 'store_name' },
				{ data: 'device_name' },
				{ data: 'consumer_id' },
				{ data: 'eyesight_name' },
				{ data: 'comsumer_nums' },
				{ data: 'create_time' },
				{ data: 'status' }
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

    $("#useSearch").click(function(){
        $('#trainUseList').DataTable().draw();
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
                $('#s_channel_name').typeahead({source: subjects});
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
                $('#s_store_name').typeahead({source: data.data});
            }
        },
        error: function(data) {
            toastr.warning('请求异常');
        }
    });
}
