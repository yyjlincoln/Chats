$(document).ready(() => {
    document.ok = true
    $("#chat").fadeIn()
    initok((okornot) => {
        if (!okornot) {
            top.location = "/"
        }
    })
    setInterval(() => {
        if (document.ok) {
            ajaxaskmsg(newmsg)
        }
    }, 500);
    getnickname((d) => {
        document.nickname = d
    })
    getid((d) => {
        document.id = d
    })
})

getnickname((username) => {
    $("#chat-left-top-text").text($("#chat-left-top-text").text().replace("$Username$", username))
})

function newmsg(msg) {
    if (msg == -1) {
        $("#chat-area").append("<div class='.system'><b>Session Expired, please <a href='/'>log in again</a>!</b></div>")
        document.ok = false
    } else if (msg != 0) {
        // console.log('New Msg', msg, side)
        if (msg.id == document.id) {
            drawmsg(msg.message, 1)
        } else {
            drawmsg(msg.nickname + ': ' + msg.message, 0)
        }
    }
    // } else {
    //     // console.log(msg)
    //     if (msg == -1) {
    //         $("#chat-area").append("<div><b>Session Expired, please <a href='/'>log in again</a>!</b></div>")
    //     }
    // }
}

function drawmsg(msg, side) {
    // console.log(msg, side)
    // $("")
    var msgbubbleRight = '<div class="msgcardr"><div id="speech" class="speech-bubbler">$msg$</div></div>'
    var msgbubbleLeft = '<div class="msgcard"><div id="speech" class="speech-bubble">$msg$</div></div>'
    if (side == 0) {
        // $("#chat-area").html($("#chat-area").html() + msgbubbleLeft.replace("$msg$", msg))
        mprc=msg.split('\n')
        var msgp=''
        for(var x=0;x<mprc.length;x++){
            msgp=msgp+"<p>"+mprc[x]+"</p>"
        }
        $("#chat-area").append(msgbubbleLeft.replace("$msg$", msgp))
    } else {
        // $("#chat-area").html($("#chat-area").html() + msgbubbleRight.replace("$msg$", msg))
        mprc=msg.split('\n')
        var msgp=''
        for(var x=0;x<mprc.length;x++){
            msgp=msgp+"<p class='nop'>"+mprc[x]+"</p>"
        }
        $("#chat-area").append(msgbubbleRight.replace("$msg$", msgp))
    }
    $("#chat-area").animate({
        scrollTop: $("#chat-area")[0].scrollHeight
    }, 200);
}

function msgsent(result) {
    // console.log(result)
    if (result < -1) {
        // newmsg('[SYSTEM] Message Sent failed.', 1)
        $("#chat-area").append("<div class='.system'><b>Message send failed</b></div>")
    }
    if (result == -1) {
        $("#chat-area").append("<div class='.system'><b>Session Expired, please <a href='/'>log in again</a>!</b></div>")
    }
}

function keyd(k) {
    if (k.keyCode == 13) {
        sendmsg(inputform.input.value, msgsent)
        inputform.input.value = ''
        return false
    }
}