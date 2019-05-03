$(document).ready(() => {
    $("#chat").fadeIn()
    initok((okornot) => {
        if (!okornot) {
            top.location = "index.html"
        }
    })
    setInterval(() => {
        ajaxaskmsg(newmsg)
    }, 500);
    getusername((d) => {
        document.id = d
    })
})

getusername((username) => {
    $("#chat-left-top-text").text($("#chat-left-top-text").text().replace("$Username$", username))
})

function newmsg(msg) {
    if (msg != -1) {
        // console.log('New Msg', msg, side)
        if (msg.id == document.id) {
            drawmsg(msg.message, 1)
        } else {
            drawmsg(msg.nickname + ': ' + msg.message, 0)
        }
    }
}

function drawmsg(msg, side) {
    console.log(msg, side)
    // $("")
    var msgbubbleRight = '<div class="msgcardr"><div id="speech" class="speech-bubbler">$msg$</div></div>'
    var msgbubbleLeft = '<div class="msgcard"><div id="speech" class="speech-bubble">$msg$</div></div>'
    if (side == 0) {
        // $("#chat-area").html($("#chat-area").html() + msgbubbleLeft.replace("$msg$", msg))
        $("#chat-area").append(msgbubbleLeft.replace("$msg$", msg))
    } else {
        // $("#chat-area").html($("#chat-area").html() + msgbubbleRight.replace("$msg$", msg))
        $("#chat-area").append(msgbubbleRight.replace("$msg$", msg))
    }
    $("#chat-area").animate({ scrollTop: $("#chat-area")[0].scrollHeight }, 200);
}

function msgsent(result) {
    if (!result) {
        newmsg('[SYSTEM] Message Sent failed.', 1)
    }
}

function keyd(k) {
    if (k.keyCode == 13) {
        sendmsg(inputform.input.value, msgsent)
        inputform.input.value = ''
        return false
    }
}