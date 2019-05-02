$(document).ready(()=>{
    $("#chat").fadeIn()
})
getusername((username)=>{
    $("#chat-left-top-text").text($("#chat-left-top-text").text().replace("$Username$",username))
})

function newmsg(msg,side){
    console.log('New Msg',msg,side)
}

function msgsent(result){
    if(!result){
        newmsg('[SYSTEM] Message Sent failed.',1)
    }
}