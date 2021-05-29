$(document).ready(function () {
    const err_string = user_messages.join('\n');
    bootbox.alert({

        message: err_string,
        centerVertical: true

    }).find("div.modal-content").addClass("confirmWidth");
})
