$(document).ready(function(){
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
});
