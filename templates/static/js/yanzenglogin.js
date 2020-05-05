



if (window.localStorage.teacher_account) {
    var teacher_loginName = window.localStorage.teacher_account
    var teacher_token = window.localStorage.teacher_token
    $.ajax({
        url: "http://127.0.0.1:8000/teacher/login_check",
        data: JSON.stringify({ "teacher_token": teacher_token }),
        type: 'POST',
        dataType: "json",
        contentType: "Aplcation/json",
        //后端给的数据是{"code":200,"data":{}}
        success: function (data) {
            if (data.code == 200) {
                if (teacher_loginName !== "undefined") {
                    $("#login").html("欢迎!" + " " + teacher_loginName + " " + "老师")
                    $("#register").html("退出")
                }
                if (teacher_loginName !== "undefined") {
                    $('#register').html("退出").on('click', (e) => {
                        e.preventDefault()
                        window.localStorage.removeItem('teacher_account');
                        window.localStorage.removeItem('teacher_token');
                        alert('退出登录')
                        $("#login").html("")
                        $("#register").html("")
                        window.location.href = 'index.html'

                    })
                    $("#login").html("欢迎!" + " " + teacher_loginName + " " + "老师").on("click", function () {
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
            else if (data.code == 10115 || data.code == 10116 || data.code == 10118) {
                alert(data.error);
                window.localStorage.removeItem('teacher_account');
                window.localStorage.removeItem('teacher_token');
                window.location.href = "login.html";
            } else {
                alert(data.error);
            }

        },
        error: function (data) {
            alert(data.error);
            return
        },
    })
} else if (window.localStorage.user_account) {
    var user_account = window.localStorage.user_account
    var user_token = window.localStorage.user_token
    console.log(user_account)
    if (user_account !== "undefined") {
        $("#login").html("欢迎!" + " " + user_account + " " + "学生/家长")
        $("#register").html("退出")
    }
    if (user_account !== "undefined") {
        $('#register').html("退出").on('click', (e) => {
            e.preventDefault()
            window.localStorage.removeItem('user_account');
            window.localStorage.removeItem('user_token');
            alert('退出登录')
            $("#login").html("")
            $("#register").html("")
            window.location.href = 'index.html'

        })
        $("#login").html("欢迎!" + " " + user_account + " " + "学生/家长").on("click", function () {

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

