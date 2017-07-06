$(document).ready(function(){
    $.validator.addMethod("PositiveNumber", function(value, element) {
        if(value <=0){
            return false;
        }
        else {
            return true;
        }
    }, "请正确填写您的次数");


    /*
    $("#training_times").bind('input propertychange', function () {
        var amount_per = 0;
        var order_type = $('.c_busicd').val();
        //
        //if(order_type == 'ORG_ALLOT_TO_CHAN') {
        //    amount_per = $('.c_channel_name').val().split('|')[1];
        //    amount_per = (amount_per / 100).toFixed(2);
        //}
        //else {
        //    amount_per = $('.c_store_name').val().split('|')[1];
        //    amount_per = (amount_per / 100).toFixed(2);
        //}
        //
        amount_per = $('.c_channel_name').val().split('|')[1];
        amount_per = (amount_per / 100).toFixed(2);

        $('#training_amt').val(($(this).val() * amount_per).toFixed(2));
    });
    */

    search_source();

    $.validator.addMethod("isYuan", function(value, element) {
        var length = value.length;
        if(value <=0){
            return false;
        }
        else {
            var yuan = /^([0-9]{1,8})(.([0-9]{1,2})){0,1}$/;
            return this.optional(element) || (length && yuan.test(value) && parseFloat(value) > 0);
        }
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
        "lengthMenu": [[10, 40, 100],[10, 40, 100]],
        "dom": 'l<"top"p>rt',
        // "bAutoWidth": true,
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

             var se_userid = window.localStorage.getItem('myid');
             get_data.se_userid = se_userid;

             var channel_name = $("#s_channel_name").val();
             if(channel_name){
                 get_data.channel_name = channel_name;
             }

             var store_name = $("#s_store_name").val();
             if(store_name){
                 get_data.store_name = store_name;
             }

			 var consumer_id = $('#s_consumer_id').val();
			 if(consumer_id){
			 	get_data.consumer_id = consumer_id;
			 }

			 var order_status = $(".s_status").val();
			 if(order_status != '-1'){
			     get_data.status = order_status;
			 }

             var start_time = $("#start_time").val();
             var end_time = $("#end_time").val();
             if(start_time && end_time){
                 var start_date = new Date(start_time);
                 var end_date = new Date(end_time);
                 if(end_date <= start_date){
                     toastr.warning('请核实时间范围');
                     return false;
                 }
                 get_data.start_time = start_time;
                 get_data.end_time = end_time;
             }


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
            /*
            {
                targets: 4,
                render: function(data, type, full) {
                    var tmp = '';
                    var len = data.length;
                    if(len==33){
                        tmp += data.slice(0,14) + '<br>'+ data.slice(14, len);
                        return tmp;
                    }
                    return data;
                }
            },
            */
            {
                targets: 0,
                render: function(data, type, full){
                    var tmp = '';
                    var busicd = full.busicd;
                    var buyer = full.buyer;
                    var buyer_id = full.buyer_id;

                    if(busicd === 'ORG_ALLOT_TO_CHAN' || busicd === 'CHAN_BUY') {
                        tmp = '<span class="buyer-name" data-buyer_id='+buyer_id+'>'+buyer+'</span>';
                    } else {
                        tmp = '<span>'+buyer+'</span>';
                    }
                    return tmp;
                }
            },
            {
                targets: 12,
                data: '操作',
                render: function(data, type, full) {
                    var orderno = full.orderno;
                    var is_valid = full.is_valid;
                    var busicd = full.busicd;
                    var create_time = full.create_time;
                    create_time = Date.parse(create_time.replace(/-/g,"/"));
                    var now = new Date();
                    var compare_time = new Date(Year=now.getFullYear(), Months=now.getMonth(), Day=now.getDate(), Hours=0, Minutes=0, senconds=0);
                    if(is_valid==0 && create_time >= compare_time){
                        var cancel = '<input type="button" class="btn btn-primary btn-sm order-cancel" data-busicd='+busicd+' data-orderno='+orderno+' value=' + '撤销' + '>';
                    } else {
                        // var cancel = '<input type="button" class="btn btn-primary btn-sm order-cancel" data-busicd='+busicd+' disabled data-orderno='+orderno+' value=' + '撤销' + '>';
                        var cancel = '<input type="button" class="btn btn-primary btn-sm order-cancel" data-busicd='+busicd+' data-orderno='+orderno+' value=' + '撤销' + '>';
                    }
                    if(is_valid == 2) {
                        var cancel = '<input type="button" class="btn btn-primary btn-sm order-cancel" data-busicd='+busicd+' disabled data-orderno='+orderno+' value=' + '撤销' + '>';

                    }
                    if(busicd == 'CHAN_BUY' && is_valid == 1){
                        var confirm = '<input type="button" class="btn btn-primary btn-sm order-confirm" data-busicd='+busicd+' data-orderno='+orderno+' value=' + '确认' + '>';
                    } else {
                        var confirm = '';
                    }

                    return cancel + confirm;
                }
            }
        ],
		'columns': [
				// { data: 'busicd_name' },
				{ data: 'buyer' },
				{ data: 'seller' },
				{ data: 'category' },
				{ data: 'op_type' },
				{ data: 'orderno' },
				{ data: 'training_times' },
				{ data: 'training_amt' },
				{ data: 'op_name' },
				{ data: 'status' },
				{ data: 'create_time' },
				{ data: 'update_time' },
				{ data: 'remark' }

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
        $('.c_rules').html('');
        // $('.c_store_name').html('');
        $("label.error").remove();
        var order_type = $("#c_busicd").val();
        /*
        if(order_type == 'ORG_ALLOT_TO_CHAN'){
            $('.create_order_store_name').hide();
        } else {
            $('.create_order_store_name').show();
        }
        */
        channel_name_select();
        $("#trainBuyerCreateModal").modal();
    });

    $("#trainBuyerSearch").click(function(){
        var buyer_query_vt = $('#buyer_query').validate({
            rules: {
                q_channel_name: {
                    required: false,
                    maxlength: 256
                },
                q_store_name: {
                    required: false,
                    maxlength: 256
                },
                q_consumer_id: {
                    required: false,
                    digits:true,
                    max: 2147483647
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
                },
                q_consumer_id: {
                    digits: "只能输入整数",
                    max: $.validator.format("请输入一个最大为{0} 的值")
                }
            },
            errorPlacement: function(error, element){
                var $error_element = element.parent().parent().next();
                $error_element.text('');
                error.appendTo($error_element);
            }
        });
        var ok = buyer_query_vt.form();
        if(!ok){
            $("#query_label_error").show();
            $("#query_label_error").fadeOut(1400);
            return false;
        }
        $('#trainBuyerList').DataTable().draw();
    });

    $("#trainBuyerCreateSubmit").click(function(){
        var post_url = '/channel_op/v1/api/org_allot_to_chan_order';
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
                    digits: true,
                    PositiveNumber: '#training_times'
                },
                training_amt: {
                    required: true,
                    number: true,
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
                    required: "请输入训练金额",
                    number: "请输入合法的数字"
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
        var is_prepayment = $('.c_channel_name').find("option:selected").data('is_prepayment');
        // var store_id = $('.c_store_name').val();
        var category = $('#c_category').val();
        var op_type = $('#c_op_type').val();
        var training_times = $('#training_times').val();
        var training_amt = $('#training_amt').val() * 100;
        var remark = $("#remark").val();
        var rule_id = $(".c_rules").val();
        post_data.channel_id = channel_id.split('|')[0];
        post_data.busicd = busicd;
        post_data.category = category;
        post_data.op_type = op_type;
        post_data.training_times = training_times;
        post_data.training_amt = parseInt(training_amt.toFixed(2));
        post_data.ch_training_amt_per = channel_id.split('|')[1];
        post_data.remark = remark;
        if(is_prepayment == 0){
            post_data.rule_id = rule_id;
        }


        /*
        if(busicd=='CHAN_ALLOT_TO_STORE'){
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
        */


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
                    $('#trainBuyerCreateForm').resetForm();
                    $('#trainBuyerCreateModal').modal('hide');
                    toastr.success('新增成功');
                    $('#trainBuyerList').DataTable().draw();
                }
            },
            error: function(data) {
                toastr.warning('请求异常');
            }
        });
    });

    /*
    $(".c_busicd").change(function () {
        var order_type = $('.c_busicd').val();
        $('#training_times').val('');
        $('#training_amt').val('');
        if(order_type == 'ORG_ALLOT_TO_CHAN') {
            $('.create_order_store_name').hide();
            $('#training_times').attr('readonly', false);
            $('#trainBuyerCreateSubmit').attr('disabled', false);
        } else {
            var channel_val = $('.c_channel_name').val();
            var channel_id = channel_val.split('|')[0];
            do_first_select(channel_id, '#c_store_name');
            $('.create_order_store_name').show();
        }
    });
    */


    $(".c_channel_name").change(function () {
        // var order_type = $("#c_busicd").val();
        //$('#training_times').val('');
        //$('#training_amt').val('');
        $('#remark').val('');
        /*
        if(order_type == 'ORG_ALLOT_TO_CHAN'){
            return false;
        }

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
                    var c_store_name = $('.c_store_name');
                    if(data.data.length==0){
                        $('#training_amt').val('');
                        //$('#training_times').val('');
                        $('#training_times').val('').attr('readonly', true);
                        $('#trainBuyerCreateSubmit').attr('disabled', true);
                        return false;
                    } else {
                        $('#training_times').attr('readonly', false);
                        $('#trainBuyerCreateSubmit').attr('disabled', false);
                    }
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
        */

        $('#training_times').val('').attr('readonly', false);
        $('#training_amt').val('').attr('readonly', false);
        var channel_id = $(this).val().split('|')[0];
        var is_prepayment = $('.c_channel_name').find("option:selected").data('is_prepayment');
        // var is_prepayment = $(this).data('is_prepayment');
        console.log('channel_id= '+channel_id+' is_prepayment='+is_prepayment);
        if(is_prepayment == 0){
            //次卡模式
            chan_rule_select(channel_id);
            $("#bind_rules").show();
            $("#rule_description").show();

        } else {
            //分成模式
            $("#bind_rules").hide();
            $("#rule_description").hide();
        }
    });

    $(document).on('click', '.buyer-name', function(){
        $("#channel_info").resetForm();
        var buyer_id = $(this).data('buyer_id');
        var se_userid = window.localStorage.getItem('myid');
        var get_data = {};
        get_data.userid = buyer_id;
        get_data.se_userid = se_userid;
        $.ajax({
            url: '/channel_op/v1/api/channel',
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
                    var chn_data = data.data.chn_data;
                    var profile = data.data.profile;
                    var u_data = data.data.u_data;
                    // console.dir(chn_data);
                    // console.dir(profile);
                    // console.dir(u_data);
                    $("#channel_name").text(chn_data.channel_name);
                    $("#contact_name").text(profile.contact_name);
                    $("#contact_phone").text(profile.contact_phone);
                    $("#remain_times").text(chn_data.remain_times);
                    $("#channelInfoModal").modal();
                }
            },
            error: function(data) {
                toastr.warning('请求异常');
            }
        });
        console.log('buyer_id: '+ buyer_id);
    });


    $(document).on('click', '.order-cancel', function(){
        var orderno = $(this).data('orderno');
        var se_userid = window.localStorage.getItem('myid');
        if(!orderno){
            toastr.warning('请确认订单号');
            return false;
        }
        var post_data = {};
        post_data.se_userid = se_userid;
        post_data.order_no = orderno;

        $.confirm({
            title: '请确认取消',
            content: '撤销将把次数从对方扣回，确认是否撤销？',
            type: 'blue',
            typeAnimated: true,
            buttons: {
                confirm: {
                    text: '确认',
                    btnClass: 'btn-red',
                    action: function() {
                        $.ajax({
                            url: '/channel_op/v1/api/order_cancel',
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
                                    toastr.success('撤销成功');
                                    $('#trainBuyerList').DataTable().draw();
                                }
                            },
                            error: function(data) {
                                toastr.warning('请求异常');
                            }
                        });
                    }
                },
                cancel: {
                    text: '取消',
                    action: function() {
                        console.log('clicked cancel');
                    }
                }
            }
        });
    });


    $(document).on('click', '.order-confirm', function(){

        var orderno = $(this).data('orderno');
        var se_userid = window.localStorage.getItem('myid');
        if(!orderno){
            toastr.warning('请确认订单号');
            return false;
        }
        var post_data = {};
        post_data.se_userid = se_userid;
        post_data.order_no = orderno;

        $.confirm({
            title: '请确认购买',
            content: '确认要求该次购买资金已经到账，资金是否已经到账？',
            type: 'blue',
            typeAnimated: true,
            buttons: {
                confirm: {
                    text: '确认',
                    btnClass: 'btn-red',
                    action: function() {
                        $.ajax({
                            url: '/channel_op/v1/api/order_confirm',
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
                                    toastr.success('确认成功');
                                    $('#trainBuyerList').DataTable().draw();
                                }
                            },
                            error: function(data) {
                                toastr.warning('请求异常');
                            }
                        });
                    }
                },
                cancel: {
                    text: '取消',
                    action: function() {
                        console.log('clicked cancel');
                    }
                }

            }
        });
    });


    $(".c_rules").change(function () {
        var rule_id = $(".c_rules").val();
        if(rule_id != 0){
            var total_amt = $(".c_rules option:selected").data('total_amt');
            var training_times = $(".c_rules option:selected").data('training_times');
            var description = $(".c_rules option:selected").data('description');
            $("#training_times").val(training_times).attr("readonly", "readonly");
            $("#training_amt").val(total_amt).attr("readonly", "readonly");
            $("#description").val(description).attr("readonly", "readonly");
        } else {
            $("#training_times").val('').removeAttr("readonly");
            $("#training_amt").val('').removeAttr("readonly");
            $("#description").val('').removeAttr("readonly");
        }
    })

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
                var c_channel_name = $('.c_channel_name');
                for(var i=0; i<data.data.length; i++){
                    var channel_id = data.data[i].channel_id;
                    var channel_name = data.data[i].channel_name;
                    var training_amt_per = data.data[i].training_amt_per;
					var is_prepayment = data.data[i].is_prepayment;
                    channel_id = channel_id+'|'+training_amt_per;
                    var option_str = $('<option value='+channel_id+' data-is_prepayment='+is_prepayment+'>'+channel_name+'</option>');
                    option_str.appendTo(c_channel_name);
                    if(i==0){
                        if(is_prepayment == 0){
                            chan_id = channel_id.split('|')[0];
                            chan_rule_select(chan_id);
                        } else {
                            $("#bind_rules").hide();
                            $("#rule_description").hide();
                        }
                    }
                }
            }
        },
        error: function(data) {
            toastr.warning('请求异常');
        }
    });
}


function do_first_select(channel_id, store_name_tag_id) {
    $(store_name_tag_id).html('');
    var get_data = {};
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
                if(data.data.length==0){
                    //$('#training_times').val('');
                    $('#training_amt').val('');
                    $('#training_times').val('').attr('readonly', true);
                    $('#trainBuyerCreateSubmit').attr('disabled', true);
                    return false;
                }  else {
                    $('#training_times').attr('readonly', false);
                    $('#trainBuyerCreateSubmit').attr('disabled', false);

                    var c_store_name = $(store_name_tag_id);
                    for(var i=0; i<data.data.length; i++){
                        var store_id = data.data[i].id;
                        var store_name = data.data[i].store_name;
                        var training_amt_per = data.data[i].training_amt_per;
                        store_id = store_id+'|'+training_amt_per;
                        var option_str = $('<option value='+store_id+'>'+store_name+'</option>');
                        option_str.appendTo(c_store_name);
                    }
                }
            }
        },
        error: function(data) {
            toastr.warning('请求异常');
        }
    });
}


function chan_rule_select(channel_id) {
    var get_data = {};
    var se_userid = window.localStorage.getItem('myid');
    get_data['se_userid'] = se_userid;
	get_data['channel_id'] = channel_id;
    $(".c_rules").html('');
    $.ajax({
        url: '/channel_op/v1/api/chan_rule_info',
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
                if(data.data.length==0){
                    //if this channel not binded rules should hava define
                    var c_rules = $("#c_rules");
                    var option_str = $('<option value="0">自定义</option>');
                    option_str.prependTo(c_rules);
                }  else {

                    var c_rules = $("#c_rules");
                    var option_str = $('<option value="0">自定义</option>');
                    option_str.prependTo(c_rules);
                    for(var i=0; i<data.data.length; i++){
                        var rule_id = data.data[i].rule_id;
                        var rule_name = data.data[i].name;
                        var rule_total_amt = data.data[i].total_amt;
                        var rule_training_times = data.data[i].training_times;
                        var rule_description = data.data[i].description;

                        var option_str = $('<option value='+rule_id+' data-total_amt='+rule_total_amt+' data-training_times='+rule_training_times+ ' data-description='+rule_description+'>'+rule_name+'</option>');
                        option_str.prependTo(c_rules);
                    }
                    $("#c_rules option:first").prop("selected", 'selected');
                    var rule_id = $(".c_rules option:selected").val();
                    if(rule_id != 0){
                        var total_amt = $(".c_rules option:selected").data('total_amt');
                        var training_times = $(".c_rules option:selected").data('training_times');
                        var description = $(".c_rules option:selected").data('description');
                        $("#training_times").val(training_times).attr("readonly", "readonly");
                        $("#training_amt").val(total_amt).attr("readonly", "readonly");
                        $("#description").val(description).attr("readonly", "readonly");
                    }
                }
            }
        },
        error: function(data) {
            toastr.warning('请求异常');
        }
    });

}
