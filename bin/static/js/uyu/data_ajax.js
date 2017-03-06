$(document).ready(function(){
    // 服务器端方法一
    $('#example').DataTable({
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
        // "dom": '<"#example_paginate"p>rt',
        "dom": 'l<"top"p>rt',
        "fnInitComplete": function(){
            //var $new_div = $('<div class="row inline-block" id="new_div_id"></div>');
            var $example_length = $("#example_length");
            var $example_paginate = $("#example_paginate");
            var $page_top = $('.top');

            $page_top.addClass('row');
            $example_paginate.addClass('col-md-8');
            $example_length.addClass('col-md-4');
            $example_length.prependTo($page_top);
            // var $pObj = $("#example_paginate > div[id$=_paginate]").addClass('left');
        },
        "ajax": function(data, callback, settings){
            $.ajax({
	            url: '/api/mydata',
	            type: 'GET',
	            dataType: 'json',
	            data: {
	                'page': Math.ceil(data.start / data.length) + 1,
	                'maxnum': data.length,
	            },
	            success: function(data) {
	                detail_data = data.data;
	                num = data.num;
	                callback({
	                    recordsTotal: num,
	                    recordsFiltered: num,
	                    data: detail_data
	                });
	            },
	            error: function(data) {
	            },

            });
        },
        'columnDefs': [
            {
                width: '10%',
                targets: 3
            },
            {   targets: 0,
                data: 'name',
                render: function(data, type, full){
                    return "<span style='color:red;'>" + data + "</span>";
                }
            },
            {
                targets: 6,
                data: '操作',
                render: function(data, type, full) {
                    return "<a href='/delete?name=" + data + "'>删除</a>&nbsp;<a href='/update?name=" + data + "'>更新</a>";
                }
            }
        ],
		'columns': [
				{ data: 'name' },
				{ data: 'position' },
				{ data: 'salary' },
				{ data: 'start_date' },
				{ data: 'office' },
				{ data: 'extn' },
				// { data: 'id', visible: false }
				{ data: 'id' }
		],
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

    /*
     * 本地处理
	var table = $('#example').DataTable({
		'paging': true,
		'ajax': {
			'url': '/api/mydata',
			'dataSrc': ''
		},
		'columns': [
				{ data: 'name' },
				{ data: 'position' },
				{ data: 'salary' },
				{ data: 'start_date' },
				{ data: 'office' },
				{ data: 'extn' }
		]
	});
    */

    /*
    // 服务器端方法二
	$('#example').dataTable({
	    serverSide: true,
        bAutoWidth: true,
        bFilter: true,
        binfo: true,
        bPaginage: true,
	    ajax: function(data, callback, setting){
	        // alert(data.start + ':'+ data.length);
	        $.ajax({
	            url: '/api/mydata',
	            type: 'GET',
	            dataType: 'json',
	            data: {
	                'page': Math.ceil(data.start / data.length) + 1,
	                'maxnum': data.length,
	            },
	            success: function(data) {
	                detail_data = data.data;
	                num = data.num;
	                callback({
	                    recordsTotal: num,
	                    recordsFiltered: num,
	                    data: detail_data
	                });
	            },
	            error: function(data) {
	            },
	        });
	    },
	    aoColumns: [
	        {'mDataProp': 'name', "sDefaultContent": ""},
	        {'mDataProp': 'position', "sDefaultContent": ""},
	        {'mDataProp': 'salary', "sDefaultContent": ""},
	        {'mDataProp': 'start_date', "sDefaultContent": ""},
	        {'mDataProp': 'office', "sDefaultContent": ""},
	        {'mDataProp': 'extn', "sDefaultContent": ""},
	    ],
	    ordering: false
	});
	*/
});


function print_object(obj){
    console.log('print object start');
    var temp = ""
    for(var key in obj){
        temp += key + ":" + obj[key] + "\n";
    }
    console.log(temp)
}
