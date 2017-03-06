$(document).ready(function(){
    $('#channelList').DataTable({
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
            var $channelList_length = $("#channelList_length");
            var $channelList_paginate = $("#channelList_paginate");
            var $page_top = $('.top');

            $page_top.addClass('row');
            $channelList_paginate.addClass('col-md-8');
            $channelList_length.addClass('col-md-4');
            $channelList_length.prependTo($page_top);
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

	$("#channelCreate").click(function(){
        $("#channelCreateForm").resetForm();
		$("#channelCreateModal").modal();
	});

    $("#channelCreateSubmit").click(function(){
        var queryString = $('#channelCreateForm').formSerialize();
        alert(queryString);
        return false;
    });
});
