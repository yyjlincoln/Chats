function activateW(windowName) {
    $('#' + windowName + '.window').fadeIn()
}
function deactivateW(windowName) {
    $('#' + windowName + '.window').fadeOut()
}
$(document).ready(() => {
    activateW('login')
})

function login_operation() {
    $('#dtext2').fadeOut()
    $('#loginform').fadeOut()
    $('#dtext3').fadeOut()
    setTimeout(() => {
        $('#loading').fadeIn()

    }, 300)
    // Loading
    init(loginform.username.value, loginform.password.value, (tf) => {
        if (tf) {
            processed=true
            $('#loading').html('<b>Login Successfully</b>')
            $('#login.window').fadeOut()
            setTimeout(() => {
                top.location='main.html'                
            }, 500);

        } else {
            processed=true
            $('#loading').html('<b>Login Failed, please check your password & remote server address and <a href="" onclick="top.location=top.location">try again</a>!</b>')
        }
    })

    setTimeout(() => {
        if (!processed) {
            $('#loading').html('<b>Don\'t close me, I\'m still here!</b>')
        }
    }, 5000)

    setTimeout(() => {
        if (!processed) {
            $('#loading').html('<b>Login Timeout! Wanna <a href="" onclick="top.location=top.location">try again</a>?</b>')
        }
    }, 10000)

    return false
}