var localServURL = "http://localhost:8099"
var remoteServAddr = "localhost"
var remoteServPort = "8088"
var initStat = false

function init(user, pass, callback) {
    $.get(localServURL + "/$api/init/" + remoteServAddr + "/" + remoteServPort + "/" + user + "/" + pass, (data) => {
        console.log(data)
        try {
            djson = JSON.parse(data)
            if (djson.success == true) {
                console.log('Login Success')
                callback(true)
            } else {
                console.log('Login Failed, code ' + djson.code)
                callback(false)
            }
        } catch (error) {

        }
    })
}

function sendmsg(msg,callback){
    msgobj={
        msg: msg
    }
    $.get(localServURL+"/$api/send/"+btoa(JSON.stringify(msgobj)),(data)=>{
        console.log(data)
        jd=JSON.parse(data)
        callback(jd.success)
    })
}

function ajaxaskmsg(callback){
    $.get(localServURL+"/$api/getmsg",(data)=>{
        d=JSON.parse(data)
        if(d.success){
            console.log(d,d.message)
            for(var e=0;e<d.message.length;e++){
                callback(d.message[e])
            }
        } else {
            callback(-1)
        }
    })
}

function getusername(callback){
    $.get(localServURL+"/$api/getusername",(data)=>{
        d=JSON.parse(data)
        if(d.success){
            callback(d.message)
        } else {
            callback("<You are not logged in>")
        }
    })
}

function initok(callback){
    $.get(localServURL+"/$api/initstat",(data)=>{
        d=JSON.parse(data)
        callback(d.success)
    })
}