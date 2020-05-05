if (window.localStorage.teacher_account) {
var loginName = window.localStorage.teacher_account
var teacher_token = window.localStorage.teacher_token
console.log(loginName)
if (loginName !== "undefined") {
    $("#login").html("欢迎!" + " " + loginName + " " + "老师")
    $("#register").html("退出")
}
if (loginName !== "undefined") {
    $('#register').html("退出").on('click', (e) => {
        e.preventDefault()
        window.localStorage.removeItem('teacher_account');
        window.localStorage.removeItem('teacher_token');
        alert('退出登录')
        $("#login").html("")
        $("#register").html("")
        window.location.href = 'index.html'

    })
    $("#login").html("欢迎!" + " " + loginName + " " + "老师").on("click", function () {
        window.location.href = 'teacher_center.html'
    })
    // 如果登录成功提示用户不能再注册
    $("#log").on("click", function (e) {
        e.preventDefault();
        alert("您已注册登录,如需注册请退出登录,再进行注册");
        window.location.href = 'index.html'
    })
    $("#zc").on("click", function (e) {
        e.preventDefault();
        alert("您已注册登录,如需注册请退出登录,再进行注册");
        window.location.href = 'index.html'
    })
}
}






if (window.localStorage.user_account) {
    var loginName = window.localStorage.user_account
    var logintoken = window.localStorage.user_token
    console.log(loginName)
    if (loginName !== "undefined") {
        $("#login").html("欢迎!" + " " + loginName + " " + "学生/家长")
        $("#register").html("退出")
    }
    if (loginName !== "undefined") {
        $('#register').html("退出").on('click', (e) => {
            e.preventDefault()
            window.localStorage.removeItem('user_account');
            window.localStorage.removeItem('user_token');
            alert('退出登录')
            $("#login").html("")
            $("#register").html("")
            window.location.href = 'index.html'

        })
        $("#login").html("欢迎!" + " " + loginName + " " + "学生/家长").on("click", function () {

            window.location.href = 'user_center.html'
        })
        // 如果登录成功提示用户不能再注册
        $("#log").on("click", function (e) {
            e.preventDefault();
            alert("您已注册登录,如需注册请退出登录,再进行注册");
            window.location.href = 'index.html'
        })
        $("#zc").on("click", function (e) {
            e.preventDefault();
            alert("您已注册登录,如需注册请退出登录,再进行注册");
            window.location.href = 'index.html'
        })
    }

};

