
$(document).ready(() => {
    activateW('login')
    initok((loggedin) => {
        if (loggedin) {
            $('#dtext2').fadeOut()
            $('#loginform').fadeOut()
            $('#dtext3').fadeOut()
            processed = true
            $('#loading').html('<b>Welcome back!</b>')
            setTimeout(() => {
                $('#loading').fadeIn()

            }, 300)
            setTimeout(() => {
                $('#login.window').fadeOut()
            }, 1000);
            setTimeout(() => {
                top.location = 'main.html'
            }, 1500);
        }
    })
})

function login_operation() {
    $('#dtext2').fadeOut()
    $('#loginform').fadeOut()
    $('#dtext3').fadeOut()
    setTimeout(() => {
        $('#loading').fadeIn()

    }, 300)
    // Loading
    init(loginform.username.value, loginform.password.value, loginform.remoteaddr.value, loginform.remoteport.value, (tf) => {
        if (tf) {
            processed = true
            $('#loading').html('<b>Login Successfully</b>')
            setTimeout(() => {
                $('#login.window').fadeOut()
            }, 1000);
            setTimeout(() => {
                top.location = 'main.html'
            }, 1500);

        } else {
            processed = true
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