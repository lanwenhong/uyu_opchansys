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

var date = function() {
    //日期初始化------------------------------------------------------------------------------------------
    $('.form_date').datetimepicker({
        icons: {
            time: "fa fa-clock-o",
            date: "fa fa-calendar",
            up: "fa fa-arrow-up",
            down: "fa fa-arrow-down"
        },
        format: 'YYYY-MM-DD HH:mm:ss',
        //showClose: true,
        sideBySide: true
    });
    $(".form_date input.sea_date").on({
        'mouseenter': function() {
            $(this).attr('readonly', 'readonly');
        },
        'mouseleave': function() {
            $(this).removeAttr('readonly');
        }
    });
    $("#datetimepicker1").on("dp.change", function(e) {
        $("#start_time").val(date_trans(e.date));
    });
    $("#start_time").val(get_date_str(-1));
    $("#starttime").val(get_date_str(-1));
}

//获取日期
function get_date_str(add_day) {
    var dd = new Date();
    dd.setDate(dd.getDate() + add_day);
    var month_val0 = dd.getMonth() + 1;
    var month_val = get_time2(month_val0);
    var date_val = get_time2(dd.getDate());
    var hours_val = get_time2(dd.getHours());
    var minutes_val = get_time2(dd.getMinutes());
    var seconds_val = get_time2(dd.getSeconds());
    return dd.getFullYear() + "-" + month_val + "-" + date_val + ' ' + hours_val + ':' + minutes_val + ':' + seconds_val;
}

function date_trans(date) {
    var dd = new Date(date);
    var month_val0 = dd.getMonth() + 1;
    var month_val = get_time2(month_val0);
    var date_val = get_time2(dd.getDate());
    var hours_val = get_time2(dd.getHours());
    var minutes_val = get_time2(dd.getMinutes());
    var seconds_val = get_time2(dd.getSeconds());
    return dd.getFullYear() + "-" + month_val + "-" + date_val + ' ' + hours_val + ':' + minutes_val + ':' + seconds_val;
}

function get_time2(val) {
    if (val < 10) {
        return '0' + val;
    } else {
        return val;
    }
}
