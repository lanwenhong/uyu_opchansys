/**
 * Created by admin on 2017/7/4.
 */
$(document).ready(function () {

    search_source();

    $.validator.addMethod("isYuan", function(value, element) {
        var length = value.length;
        // var yuan  = /^([0-9]{1,6})\.([0-9]{1,2})$/;
        var yuan = /^([0-9]{1,8})(.([0-9]{1,2})){0,1}$/;
        return this.optional(element) || (length && yuan.test(value) && parseFloat(value) > 0);
    }, "请正确填写您的总金额");

    $("#ruleList").DataTable({
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

        'columnDefs': [
            {
                targets: 7,
                data: '操作',
                render: function(data, type, full) {
                    var rule_id =full.id;
                    var view ="<button type='button' class='btn btn-warning btn-sm viewEdit' data-rule_id="+rule_id+">"+'查看'+"</button>";
                    return view;
                }
            }
        ],

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

    $("#ruleNameSearch").click(function () {
        $('#ruleList').DataTable().draw();
    });
    
    $("#ruleCreate").click(function () {
        $("label.error").remove();
        $("#ruleCreateForm").resetForm();
        $("#ruleCreateModal").modal();
    });

    $("#ruleCreateSubmit").click(function () {
        var rule_create_vt = $("#ruleCreateForm").validate({
            rules:{
                name: {
                    required: true,
                    maxlength: 128
                },
                total_amt: {
                    required: true,
                    isYuan: '#total_amt'
                },
                training_times: {
                    required: true,
                    digits:true,
                    min:1
                }
            },
            messages: {
                name: {
                    required: "请输入套餐名称",
                    maxlength: $.validator.format("请输入一个 长度最多是 {0} 的字符串")
                },
                total_amt: {
                    required: "请填写总金额"
                },
                training_times: {
                    required: "请填写训练次数",
                    digits: "只能输入整数",
                    min: $.validator.format("请输入一个最小为{0} 的值")
                }
            }
        });

        var ok = rule_create_vt.form();
        if(!ok){
            return false;
        }

        var post_data = {};
        var se_userid = window.localStorage.getItem('myid');
        name = $("#name").val();
        total_amt = $("#total_amt").val() * 100;
        training_times = $("#training_times").val();
        description = $("#description").val();

        post_data.se_userid = se_userid;
        post_data.name = name;
        post_data.total_amt = total_amt;
        post_data.training_times = training_times;
        post_data.description = description;

        $.ajax({
            url: '/channel_op/v1/api/rule_create',
            type: 'POST',
            dataType: 'json',
            data: post_data,
            success: function(data) {
                var respcd = data.respcd;
                if(respcd != '0000'){
                    var resperr = data.resperr;
                    var respmsg = data.respmsg;
                    var msg = resperr ? resperr : respmsg;
                    toastr.warning(msg);
                    return false;
                }
                else {
                    toastr.success('新建套餐成功');
                    search_source();
                    $("#ruleCreateModal").modal('hide');
                    location.reload();
                    $('#ruleList').DataTable().draw();
                }
            },
            error: function(data) {
                toastr.warning('请求异常');
            }
        });

    });

    $(document).on('click', '.viewEdit', function () {
        $("label.error").remove();
        $("#ruleEditForm").resetForm();
        var rule_id = $(this).data('rule_id');
        $("#rule_id").text(rule_id);
        var se_userid = window.localStorage.getItem('myid');
        var get_data = {};
        get_data.rule_id = rule_id;
        get_data.se_userid = se_userid;

        $.ajax({
            url: '/channel_op/v1/api/rule',
            type: 'GET',
            dataType: 'json',
            data: get_data,
            success: function(data) {
                var respcd = data.respcd;
                if(respcd != '0000'){
                    var resperr = data.resperr;
                    var respmsg = data.respmsg;
                    var msg = resperr ? resperr : respmsg;
                    toastr.warning(msg);
                }
                else {
                    var data = data.data;
                    console.log('rule data :'+ data);
                    var name = data.name;
                    var total_amt = data.total_amt;
                    var training_times = data.training_times;
                    var description = data.description;

                    $("#edit_name").val(name);
                    $("#edit_total_amt").val(total_amt);
                    $("#edit_training_times").val(training_times);
                    $("#edit_description").val(description);

                    $("#ruleEidtModal").modal();
                }
            },
            error: function(data) {
                toastr.warning('请求异常');
            }
        });
    });

    $("#ruleEditSubmit").click(function(){
        var rule_edit_vt = $("#ruleEditForm").validate({
            rules:{
                edit_name: {
                    required: true,
                    maxlength: 128
                },
                edit_total_amt: {
                    required: true,
                    isYuan: '#edit_total_amt'
                },
                edit_training_times: {
                    required: true,
                    digits:true,
                    min:1
                }
            },
            messages: {
                edit_name: {
                    required: "请输入套餐名称",
                    maxlength: $.validator.format("请输入一个 长度最多是 {0} 的字符串")
                },
                edit_total_amt: {
                    required: "请填写总金额"
                },
                edit_training_times: {
                    required: "请填写训练次数",
                    digits: "只能输入整数",
                    min: $.validator.format("请输入一个最小为{0} 的值")
                }
            }
        });

        var ok = rule_edit_vt.form();
        if(!ok){
            return false;
        }

        var rule_id = $("#rule_id").text();
        var name = $("#edit_name").val();
        var total_amt = $("#edit_total_amt").val() * 100;
        var training_times = $("#edit_training_times").val();
        var description = $("#edit_description").val();

        var post_data = {};
        var se_userid = window.localStorage.getItem('myid');
        post_data['se_userid'] = se_userid;
        post_data['rule_id'] = rule_id;
        post_data['name'] = name;
        post_data['total_amt'] = total_amt;
        post_data['training_times'] = training_times;
        post_data['description'] = description;

        $.ajax({
            url: '/channel_op/v1/api/rule_edit',
            type: 'POST',
            dataType: 'json',
            data: post_data,
            success: function(data) {
                var respcd = data.respcd;
                if(respcd != '0000'){
                    var resperr = data.resperr;
                    var respmsg = data.respmsg;
                    var msg = resperr ? resperr : respmsg;
                    toastr.warning(msg);
                    return false;
                }
                else {
                    toastr.success('修改套餐成功');
                    $("#ruleEidtModal").modal('hide');
                    $('#ruleList').DataTable().draw();
                }
            },
            error: function(data) {
                toastr.warning('请求异常');
            }
        });

    });
});


function search_source() {
    var get_data = {};
    var se_userid = window.localStorage.getItem('myid');
    get_data['se_userid'] = se_userid;
    $.ajax({
        url: '/channel_op/v1/api/rule_name_list',
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
                console.log('subjects: ');
                console.log(data.data);
                for(var i=0; i<data.data.length; i++){
                    subjects.push(data.data[i].name)
                }
                $('#ruleName').typeahead({source: subjects});
            }
        },
        error: function(data) {
            toastr.warning('请求异常');
        }
    });
}