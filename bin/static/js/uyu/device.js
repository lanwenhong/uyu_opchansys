$(document).ready(function(){
    $('#deviceList').DataTable({
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
        'oLanguage': {
            'sProcessing': '<span style="color:red;">加载中....</span>',
            'sLengthMenu': '每页显示_MENU_条记录',
            "sInfo": '显示 _START_到_END_ 的 _TOTAL_条数据',
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

    $("#deviceCreateSubmit").click(function(){
       var queryString = $('#deviceCreateForm').formSerialize();
       alert(queryString);
    });

});
