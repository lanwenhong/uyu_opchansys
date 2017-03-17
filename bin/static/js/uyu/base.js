function print_object(obj){
    var temp = ""
    for(var key in obj){
        temp += key + ":" + obj[key] + "\n";
    }
}


function check_obj_val(obj){
    for(var key in obj){
        var value = obj[key];
        if(!value){
            console.log('key: '+key);
            return false;
        }
    }
    return true;
}
