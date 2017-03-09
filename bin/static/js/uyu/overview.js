$(document).ready(function(){
    var myid = window.localStorage.getItem('myid');
    var get_data = {'se_userid': myid}
    $.ajax({
	    url: '/channel_op/v1/api/chan_store_total',
	    type: 'GET',
	    dataType: 'json',
	    data: get_data,
	    success: function(data) {
            var respcd = data.respcd;
            if(respcd != '0000'){
                var resperr = data.resperr;
                var respmsg = data.resmsg;
                var msg = resperr ? resperr : resmsg;
                toastr.warning(msg);
                return false;
			} else {
                var channel_total = data.data.channel_total;
                var store_total = data.data.store_total;
                $('.channel_total').text(channel_total);
                $('.store_total').text(store_total);
            }
	    },
	    error: function(data) {
            toastr.warning('请求数据异常');
	    },
    });
});
