
// Message/Notification timer

// var message_timeout = document.getElementById('message-timer');

// setTimeout(function() {
//     message_timeout.style.display = 'none';
// }, 5000);
document.addEventListener("DOMContentLoaded", function () {
        setTimeout(function () {
            const messages = document.querySelectorAll(".message-timer");
            messages.forEach(function (msg) {
                msg.style.display = "none";
            });
        }, 5000);
    });