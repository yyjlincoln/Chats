function sub() {
    command = i.stdin.value
    pushOut(command)
    i.stdin.value=""
    $.get("/$api/send/"+command,(data)=>{
        pushOut(data)
    })
    return false
}

function pushOut(data, nxtline = true, d = false) {
    if (!d) {
        data = data.split("\n")
        for (var i = 0; i < data.length; i++) {
            pushOut(data[i], true, true)
        }
    } else {
        if (nxtline) {
            $('#stdout').html($('#stdout').html() + '<p>' + data + '</p>')
        }
    }
}

$(document).ready(() => {
    pushOut('Server connecting...')
    hideIn()
    $.get("/$api/init",(data)=>{
        pushOut('Connection Established.')
        pushOut(data)
        showIn()
    })
})

function hideIn(){
    $('#stdin').hide()
}

function showIn(){
    $('#stdin').show()
}
