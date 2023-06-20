let input_field = document.getElementById("message_input")
let outer_div = document.getElementById("message-input-area")
outer_div.style.transition = "all 0.3s"

let icon_send = document.getElementById("send_message_icon")
icon_send.style.transition = "all 0.3s"

let btn_send = document.getElementById("send_message_btn")
btn_send.style.transition = "all 0.3s"

let orange = '#FF710F';
let black = '#101010';

input_field.onfocus = function () {
    icon_send.style.color = orange;
    outer_div.style.borderColor = orange;
    btn_send.style.background = 'transparent';
}
input_field.onblur = function () {
    icon_send.style.color = 'white';
    outer_div.style.borderColor = 'white';
    btn_send.style.background = orange;
}

document.getElementById("send_message_btn").addEventListener("click", show_message)
document.getElementById("message_input").addEventListener("keypress", function (event) {
    if (event.key == "Enter") {
        show_message()
    }
})
menu_btn = document.getElementById("menu-btn")
menu_btn.addEventListener('click', show_menu)

function show_menu() {
    menu = document.getElementById('menu')
    menu_btn.classList.add('rotate')
    setInterval(function () { menu_btn.classList.remove('rotate') }, 500)

    if (menu.classList.contains('show')) {
        menu.classList.remove('show')
        menu_btn.classList.replace('fa-xmark', 'fa-bars')
    }
    else {
        menu_btn.classList.replace('fa-bars', 'fa-xmark')
        menu.classList.add('show')
    }
}


function show_message() {
    let message = document.getElementById("message_input").value
    if (message.length == 0) {
        return;
    }

    let chat_area = document.getElementById("chat-area")
    let message_div = document.createElement("div")
    message_div.className += " message my-message"

    let message_para = document.createElement("p")
    message_para.textContent = message
    message_para.style.color = black

    let time = document.createElement("div")
    time.className += " time"
    let time_String = new Date().toLocaleTimeString().toString();
    time.textContent = time_String.replace(time_String.slice(4, 7), '')
    time.style.color = black

    message_div.appendChild(message_para)
    message_div.appendChild(time)

    chat_area.appendChild(message_div)
    chat_area.scrollTop = chat_area.scrollHeight
    document.getElementById("message_input").value = ''

    if ((document.getElementsByClassName("time")).length == 1) {
        greet = document.getElementById("greet")
        greet.className += " hide"
        setTimeout(function () {
            greet.style.display = "none"
            chat_area.style.justifyContent = "flex-start";
            chat_area.style.paddingTop = "2rem";
            document.getElementById("bot-info").className += " show"
        }, 200)
    }
    get_bot_response(message);
}

function show_bot_response(response) {
    if (response.length == 0) {
        return;
    }
    let message_div = document.createElement("div")
    message_div.className += " message other-message"

    let message_para = document.createElement("p")
    message_para.textContent = response

    let time = document.createElement("div")
    time.className += " time"
    let time_String = new Date().toLocaleTimeString().toString();
    time.textContent = time_String.replace(time_String.slice(4, 7), '')

    message_div.appendChild(message_para)
    message_div.appendChild(time)

    let chat_area = document.getElementById("chat-area")
    chat_area.appendChild(message_div)
    chat_area.scrollTop = chat_area.scrollHeight
}