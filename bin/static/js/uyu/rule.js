/**
 * Created by admin on 2017/7/4.
 */
$(document).ready(function () {

    $('#ruleList').DataTable({
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
            var $ruleList_length = $("#ruleList_length");
            var $ruleList_paginate = $("#ruleList_paginate");
            var $page_top = $('.top');

            $page_top.addClass('row');
            $ruleList_paginate.addClass('col-md-8');
            $ruleList_length.addClass('col-md-4');
            $ruleList_length.prependTo($page_top);
        },
        "ajax": function(data, callback, settings){
            var get_data = {
                'page': Math.ceil(data.start / data.length) + 1,
                'maxnum': data.length
            };

            var se_userid = window.localStorage.getItem('myid');
            get_data.se_userid = se_userid;

            var name = $("#ruleName").val();

            if(name){
                get_data.name = name;
            }

            $.ajax({
                url: '/channel_op/v1/api/ruleinfo_pagelist',
                type: 'GET',
                dataType: 'json',
                data: get_data,
                success: function(data) {
                    var respcd = data.respcd;
                    if(respcd != '0000'){
                        $processing = $("#ruleList_processing");
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
        /*
        'columnDefs': [
            {
                targets: 9,
                data: '操作',
                render: function(data, type, full) {
                    var status = full.status;
                    var uid =full.userid;
                    var channel_id =full.id;
                    var msg = status ? '打开' : '关闭';
                    // var op = "<input type='button' class='btn btn-primary btn-sm setStatus' data-channelid="+uid+" value="+msg+ " data-status="+status+">";
                    var op = "<button type='button' class='btn btn-success btn-sm setStatus' data-channelid="+uid+" data-status="+status+">"+msg+"</button>";
                    // var view ="<input type='button' class='btn btn-info btn-sm viewEdit' data-uid="+uid+" value="+'查看'+ " data-channelid="+channel_id+">";
                    var view ="<button type='button' class='btn btn-warning btn-sm viewEdit' data-uid="+uid+" data-channelid="+channel_id+">"+'查看'+"</button>";
                    return op+view;
                }
            }
        ],
        */
        'columns': [
            { data: 'id' },
            { data: 'name' },
            { data: 'total_amt' },
            { data: 'training_times' },
            { data: 'description' },
            { data: 'state' },
            { data: 'ctime' }
        ],
        'oLanguage': {
            'sProcessing': '<span style="color:red;">加载中....</span>',
            'sLengthMenu': '每页显示_MENU_条记录',
            'sInfo': '显示 _START_到_END_ 的 _TOTAL_条数据',
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