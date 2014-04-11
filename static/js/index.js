$(document).ready(function(){
    $(".btn").click(function(){
        text = editor.getValue();
        $.ajax({
            url:"/edit_hosts",
            data:"text=" + text,
            type:"post",
            success:onSuccess
        });
    });
    
    CodeMirror.commands.save = function(){ 
        $(".btn").removeAttr("disabled");
    };
    window.editor = CodeMirror.fromTextArea(document.getElementsByTagName("textarea")[0], {
        lineNumbers: true,
        mode: "markdown",
        vimMode: true,
        showCursorWhenSelecting: true
    });
    $("textarea").bind("input propertychange", function(){
        $(".btn").removeAttr("disabled");
    });
    $(".CodeMirror").bind("change", function(){
        $(".btn").removeAttr("disabled");
    })

    window.ws = new WebSocket("ws://" + ip + ":" + port + "/soc");
    setTimeout(function(){
        if (ws.readyState == 3) {
            $(".alert").text("warning: Websocket connection failed! You can not be received a notice while file was modified! Ensure if you are online and not using a proxy.").css("opacity", 1);
        }
    }, 1000);

    ws.onmessage = function(event){
        var data = JSON.parse(event.data);
        if (data._flag != getCookie("_flag") && true == confirm("hosts已被" + data.user + "修改，是否重新加载")) {
            editor.setValue(data.text);
        }
    }
});

function onSuccess(msg) {
    $(".btn").attr("disabled", true);
    if (msg.code == 0) {
        setTimeout(function(){
            $(".textarea").css("-webkit-animation-play-state", "running");
            $(".textarea").css("-o-animation-play-state", "running");
            $(".textarea").css("-moz-animation-play-state", "running");
            $(".textarea").css("animation-play-state", "running");
        }, 0);
        setTimeout(function(){
            $(".textarea").css("-webkit-animation-play-state", "paused");
            $(".textarea").css("-o-animation-play-state", "paused");
            $(".textarea").css("-moz-animation-play-state", "paused");
            $(".textarea").css("animation-play-state", "paused");
        }, 2000);
    }
}
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
