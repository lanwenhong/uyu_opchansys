$(document).ready(function(){

    search_source();

    $('#settleList').DataTable({
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
            var $settleList_length = $("#settleList_length");
            var $settleList_paginate = $("#settleList_paginate");
            var $page_top = $('.top');

            $page_top.addClass('row');
            $settleList_paginate.addClass('col-md-8');
            $settleList_length.addClass('col-md-4');
            $settleList_length.prependTo($page_top);
        },
        "ajax": function (data, callback, settings) {
            var get_data = {
                'page': Math.ceil(data.start / data.length) + 1,
                'maxnum': data.length
            };

            var channel_name = $('#channel_name').val();
            if(channel_name){
                get_data.channel_name = channel_name;
            }

            var store_name = $('#store_name').val();
            if(store_name){
                get_data.store_name = store_name;
            }

            var start_time = $('#start_time').val();
            if(start_time){
                get_data.start_time = start_time;
            }

            var se_userid = window.localStorage.getItem('myid');
            get_data.se_userid = se_userid;

            $.ajax({
                url: '/channel_op/v1/api/settle_list',
                type: 'GET',
                dataType: 'json',
                data: get_data,
                success: function(data) {
                    var respcd = data.respcd;
                    if(respcd != '0000'){
                        $processing = $("#settleList_processing");
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
        "columns": [
            { data: 'id' },
            { data: 'buyer_type' },
            { data: 'channel_name' },
            { data: 'store_name' },
            { data: 'settle_cycle' },
            { data: 'settle_time' },
            { data: 'settle_trainning_nums' },
            { data: 'settle_amt' },
            { data: 'channel_divide_amt' },
            { data: 'store_divide_amt' },
            { data: 'company_divide_amt' }
        ],
        "oLanguage": {
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

    $("#settleSearch").click(function(){
        var settle_query_vt = $('#settle_query').validate({
            rules: {
                q_channel_name: {
                    required: false,
                    maxlength: 256
                },
                q_store_name: {
                    required: false,
                    maxlength: 256
                }
            },
            messages: {
                q_channel_name: {
                    required: '请输入渠道名称',
                    maxlength: $.validator.format("请输入一个长度最多是 {0} 的字符串")
                },
                q_store_name: {
                    required: '请输入门店名称',
                    maxlength: $.validator.format("请输入一个长度最多是 {0} 的字符串")
                }
            },
            errorPlacement: function(error, element){
                var $error_element = element.parent().parent().next();
                $error_element.text('');
                error.appendTo($error_element);
            }
        });
        var ok = settle_query_vt.form();
        if(!ok){
            $("#query_label_error").show();
            $("#query_label_error").fadeOut(1400);
            return false;
        }

        $("#settleList").DataTable().draw();
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
