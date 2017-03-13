$(document).ready(function(){
    search_source();

    $.validator.addMethod("isYuan", function(value, element) {
        var length = value.length;
        var yuan  = /^([0-9]{1,6})\.([0-9]{1,2})$/;
        return this.optional(element) || (length && yuan.test(value));
    }, "请正确填写您的价格");

    $('#trainBuyerList').DataTable({
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
            var $trainBuyerList_length = $("#trainBuyerList_length");
            var $trainBuyerList_paginate = $("#trainBuyerList_paginate");
            var $page_top = $('.top');

            $page_top.addClass('row');
            $trainBuyerList_paginate.addClass('col-md-8');
            $trainBuyerList_length.addClass('col-md-4');
            $trainBuyerList_length.prependTo($page_top);
        },
        "ajax": function(data, callback, settings){
            var get_data = {
	           'page': Math.ceil(data.start / data.length) + 1,
	           'maxnum': data.length
            };
            var channel_name = $("#s_channel_name").val();
            if(channel_name){
                get_data.channel_name = channel_name;
            }

            var store_name = $("#s_store_name").val();
            if(store_name){
                get_data.store_name = store_name;
            }

			var consumer_mobile = $('#s_consumer_mobile').val();
			if(consumer_mobile){
				get_data.mobile = consumer_mobile;
			}

            console.log('search data');
            console.log(get_data);
            $.ajax({
	            url: '/channel_op/v1/api/training_op_list',
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
	            }
            });
        },
        'columnDefs': [
            {
                targets: 11,
                data: '操作',
                render: function(data, type, full) {
                    var orderno = full.orderno;
                    var cancel = '<input type="button" class="btn btn-primary btn-sm order-cancel" data-orderno='+orderno+' value=' + '撤销' + '>';
                    return cancel;
                }
            }
        ],
		'columns': [
				{ data: 'id' },
				{ data: 'channel_name' },
				{ data: 'store_name' },
				{ data: 'consumer_id' },
				{ data: 'category' },
				{ data: 'op_type' },
				{ data: 'training_times' },
				{ data: 'training_amt' },
				{ data: 'op_name' },
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

    $("#trainBuyerCreate").click(function(){
        $("#trainBuyerCreateForm").resetForm();
        $('.c_channel_name').html('');
        $('.c_store_name').html('');
        channel_name_select();
        $("#trainBuyerCreateModal").modal();
    });

    $("#trainBuyerSearch").click(function(){
        $('#trainBuyerList').DataTable().draw();
    });

    $("#trainBuyerCreateSubmit").click(function(){
        var post_url = '';
        var buyer_vt = $('#trainBuyerCreateForm').validate({
            rules: {
                busicd: {
                    required: true
                },
                channel_name: {
                    required: true
                },
                category: {
                    required: true
                },
                op_type: {
                    required: true,
                    range: [0, 2]
                },
                training_times: {
                    required: true,
                    digits: true
                },
                training_amt: {
                    required: true,
                    isYuan: '#training_amt'
                }
            },
            messages: {
                busicd: {
                    required: "请选择下单类型"
                },
                channel_name: {
                    required: "请选择渠道"
                },
                category: {
                    required: "请选择类别"
                },
                op_type: {
                    required: "请选择操作类型",
                    range: $.validator.format("请输入一个介于 {0} 和 {1} 之间的值")
                },
                training_times: {
                    required: "请输入训练次数",
                    digits: "只能输入整数"
                },
                training_amt: {
                    required: "请输入训练金额"
                }
            }
        });
        var ok = buyer_vt.form();
        if(!ok){
            return false;
        }
        var post_data = {};
        var se_userid = window.localStorage.getItem('myid');
        post_data.se_userid = se_userid;
        var busicd = $('.c_busicd').val();
        var channel_id = $('.c_channel_name').val();
        var ch_training_amt_per = $('.c_channel_name').val('value2');
        var store_id = $('.c_store_name').val();
        var category = $('#c_category').val();
        var op_type = $('#c_op_type').val();
        var training_times = $('#training_times').val();
        var training_amt = $('#training_amt').val() * 100;
        post_data.channel_id = channel_id.split('|')[0];
        post_data.busicd = busicd;
        post_data.category = category;
        post_data.op_type = op_type;
        post_data.training_times = training_times;
        post_data.training_amt = parseInt(training_amt.toFixed(2));
        post_data.ch_training_amt_per = channel_id.split('|')[1];

        console.log('post_data');
        console.log(post_data);
        if(busicd=='000020'){
            if(!store_id){
                toastr.warning('渠道分配训练点数给门店时请选择门店');
                return false;
            }
            post_data.store_id = store_id.split('|')[0];
            var store_training_amt_per = store_id.split('|')[1];
            post_data.store_training_amt_per = store_training_amt_per;
            post_url = '/channel_op/v1/api/org_allot_to_store_order';
        } else {
            post_url = '/channel_op/v1/api/org_allot_to_chan_order';
        }


        $.ajax({
            url: post_url,
            type: 'POST',
            data: post_data,
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
                    console.log(data.data);
                    $('#trainBuyerCreateForm').resetForm();
                    $('#trainBuyerCreateModal').modal('hide');
                    toastr.success('新增成功');
                }
            },
            error: function(data) {
                toastr.warning('请求异常');
            }
        });
    });

    $('.c_channel_name').change(function () {
        var get_data = {};
        $('.c_store_name').html('');
        var ch_val = $('.c_channel_name').val();
        var channel_id = ch_val.split('|')[0];
        var se_userid = window.localStorage.getItem('myid');
        get_data['se_userid'] = se_userid;
        get_data['channel_id'] = channel_id;
        $.ajax({
            url: '/channel_op/v1/api/chan_store_list',
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
                    console.log(data.data);
                    var c_store_name = $('.c_store_name');
                    for(var i=0; i<data.data.length; i++){
                        var store_id = data.data[i].id;
                        var store_name = data.data[i].store_name;
                        var training_amt_per = data.data[i].training_amt_per;
                        store_id = store_id+'|'+training_amt_per;
                        var option_str = $('<option value='+store_id+'>'+store_name+'</option>');
                        option_str.appendTo(c_store_name);
                    }
                }
            },
            error: function(data) {
                toastr.warning('请求异常');
            }
        });
    });

    $(document).on('click', '.order-cancel', function(){
        alert('准备提交撤销操作');
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
                console.log(data.data);
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
                console.log(data.data);
                $('#s_store_name').typeahead({source: data.data});
            }
        },
        error: function(data) {
            toastr.warning('请求异常');
        }
    });
}

function channel_name_select() {
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
                console.log(data.data);
                var c_channel_name = $('.c_channel_name');
                for(var i=0; i<data.data.length; i++){
                    var channel_id = data.data[i].channel_id;
                    var channel_name = data.data[i].channel_name;
                    var training_amt_per = data.data[i].training_amt_per;
                    channel_id = channel_id+'|'+training_amt_per;
                    var option_str = $('<option value='+channel_id+'>'+channel_name+'</option>');
                    option_str.appendTo(c_channel_name);
                }
            }
        },
        error: function(data) {
            toastr.warning('请求异常');
        }
    });
}

