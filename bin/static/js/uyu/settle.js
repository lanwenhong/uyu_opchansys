$(document).ready(function(){
    $('#settleList').DataTable({
        "autoWidth": false,     //通常被禁用作为优化
        "processing": true,
        // "serverSide": true,
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
        'oLanguage': {
            'sProcessing': '<span style="color:red;">加载中....</span>',
            'sLengthMenu': '每页显示_MENU_条记录',
            "sInfo": '显示 _START_到_END_ 的 _TOTAL_条数据',
            'oPaginate': {
                'sFirst': '首页',
                'sPrevious': '前一页',
                'sNext': '后一页',
                'sLast': '尾页'
            }
        }

    });
});
