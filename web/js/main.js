$(document).ready(()=>{
    $("#chat").fadeIn()
})
getusername((username)=>{
    $("#chat-left-top-text").text($("#chat-left-top-text").text().replace("$Username$",username))
})