function print_object(obj){
    var temp = ""
    for(var key in obj){
        temp += key + ":" + obj[key] + "\n";
    }
}

function query_to_obj(queryString){
    console.log('base ');
    console.log(queryString);
    var arr = queryString.split('&');
    var post_data = new Object();
    for(var i=0; i<arr.length; i++){
        var tmp = arr[i].split('=');
        post_data[tmp[0]] = tmp[1];
    }
    return post_data;
}

function check_obj_val(obj){
    for(var key in obj){
        var value = obj[key];
        if(!value){
            return false;
        }
    }
    return true;
}
