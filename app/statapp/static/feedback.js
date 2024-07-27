
var feedback_counter = 0;
var sound;

window.addEventListener('load', function () {
    sound = new Audio(audio_url);
})

function send_feedback_request(event_id, operator_id, value) {
    sound.play();
    var request = new XMLHttpRequest();
    request.onload = (response) => {
        if (response.explicitOriginalTarget.status == 200) {
            update_counter();
        } else {
            console.log("feedback could not be submitted")
        }
        
    };
    request.open("GET", `/feedback/send/${event_id}/${operator_id}/${value}`, true);
    request.send();
}

function update_counter() {
    feedback_counter += 1;
    counter = document.getElementById("feedback-count");
    counter.innerHTML = feedback_counter;
}

function enter_fullscreen() {
    let infobox = document.getElementById("info");
    let navbar = document.getElementById("navbar");
    let footer = document.getElementById("footer");
    infobox.style.display = "none";
    navbar.style.display = "none";
    footer.style.visibility = "hidden";

    if ((document.fullScreenElement !== undefined && document.fullScreenElement === null) || (document.msFullscreenElement !== undefined && document.msFullscreenElement === null) || (document.mozFullScreen !== undefined && !document.mozFullScreen) || (document.webkitIsFullScreen !== undefined && !document.webkitIsFullScreen)) {
        if (document.documentElement.requestFullScreen) {  
            document.documentElement.requestFullScreen();  
        } else if (document.documentElement.mozRequestFullScreen) {  
            document.documentElement.mozRequestFullScreen();  
        } else if (document.documentElement.webkitRequestFullScreen) {  
            document.documentElement.webkitRequestFullScreen(Element.ALLOW_KEYBOARD_INPUT);  
        }
    }
}
    

function exit_fullscreen() {
    let infobox = document.getElementById("info");
    let navbar = document.getElementById("navbar");
    let footer = document.getElementById("footer");
    infobox.style.display = "block";
    navbar.style.display = "block";
    footer.style.visibility = "visible";

    if (!((document.fullScreenElement !== undefined && document.fullScreenElement === null) || (document.msFullscreenElement !== undefined && document.msFullscreenElement === null) || (document.mozFullScreen !== undefined && !document.mozFullScreen) || (document.webkitIsFullScreen !== undefined && !document.webkitIsFullScreen))) {
        if (document.cancelFullScreen) {  
            document.cancelFullScreen();  
        } else if (document.mozCancelFullScreen) {  
            document.mozCancelFullScreen();  
        } else if (document.webkitCancelFullScreen) {  
            document.webkitCancelFullScreen();  
        }  
    }
}