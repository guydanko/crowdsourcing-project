
//post request for replies on comments
function create_reply(oForm) {

    var body = oForm.elements["body"].value;
    var tag_id = oForm.elements["tag_id"].value;
    var parent_id = oForm.elements["parent_id"].value;

    $.ajax({
        url: '/videos/create_comment/',
        type: 'POST',
        data: {
            csrfmiddlewaretoken: window.CSRF_TOKEN,
            'tag_id': tag_id,
            'body': body,
            'parent_id': parent_id
        },
        dataType: 'json',
        complete: function (data) {
            const statusCode = data.status

            if (statusCode === 200 || statusCode == 201) {
                var comments = JSON.parse(data.responseJSON.comments_list);
                showComments(comments, tag_id);
                commentForm(tag_id);

            }
            if (statusCode === 204) {
                noComments()
                commentForm(tag_id)
            }
            displayErrors(JSON.parse(data.responseJSON.errors))
            document.getElementById("reply-body").value = ""

        }
    })
}

//post request for deleting a comment on a tag
function delete_comment(tag_id, comment_id) {

    $.ajax({
        url: '/videos/delete_comment/',
        type: 'POST',
        data: {
            csrfmiddlewaretoken: window.CSRF_TOKEN,
            'tag_id': tag_id,
            'comment_id': comment_id
        },
        dataType: 'json',
        complete: function (data) {
            const statusCode = data.status

            if (statusCode === 200 || statusCode == 201) {
                var comments = JSON.parse(data.responseJSON.comments_list);
                showComments(comments, tag_id);
                commentForm(tag_id);
            }
            if (statusCode === 204) {
                noComments()
                commentForm(tag_id)
            }

        }
    });

}

//build dynamically the comments table for a tag
function showComments(comments, tag_id) {

    var div = document.getElementById("no-comments");
    div.innerHTML = ""

    var table = document.getElementById("comments_table")
    table.innerHTML = "";

    var header = table.createTHead();
    header.style.color = "#FFFFFF";

    var row = header.insertRow(0);
    row.style.backgroundColor = "#000000";

    var cell = row.insertCell(0);
    cell.innerHTML = "<b>Comments</b>";
    cell.colSpan = 10

    cell = row.insertCell(1);
    cell.innerHTML = "";
    cell.colSpan = 90;

    var tbody = document.createElement("TBODY");
    table.appendChild(tbody);

    var input_tag_id = document.getElementById("input_tag_id");
    input_tag_id.setAttribute("value", tag_id);
    input_tag_id.id = "input_tag_id-" + tag_id;

    var parent_id;
    var div_form_replay;
    var form_replay;
    var div_delete;
    var table_comment;
    var row_comment;
    var cell_comment;

    for (i = comments.length - 1; i >= 0; i--) {
        //adding comments
        if (!comments[i].fields.is_reply) {
            var form_id = comments[i].pk;
            row = tbody.insertRow(0);
            row.id = "comment_header"
            row.style.backgroundColor = "azure"

            cell = row.insertCell(0);
            table_comment = document.createElement("table");
            table_comment.className = "table table-borderless table-sm"
            row_comment = table_comment.insertRow(0);
            cell_comment = row_comment.insertCell(0);
            cell_comment.innerHTML = "<b>" + comments[i].fields.creator_name + "</b>";

            row_comment = table_comment.insertRow(1);
            cell_comment = row_comment.insertCell(0);
            cell_comment.innerHTML = comments[i].fields.body;
            cell_comment.style.wordWrap = "break-word";

            cell.appendChild(table_comment);
            cell.colSpan = 68;

            cell = row.insertCell(1);
            cell.colSpan = 22;
            cell.style.padding = "30px";
            cell.innerHTML = "Replies  " + "<i class='showMore fa fa-angle-double-right'></i>"

            cell = row.insertCell(2);
            div_delete = document.createElement("div");
            div_delete.className = "clickable";

            var num = tag_id
            if (user_id == comments[i].fields.creator) {
                div_delete.innerHTML = "<i class='fa fa-trash' aria-hidden='true' onclick='delete_comment(" + num + "," + form_id + ")'></i>"
            } else {
                div_delete.innerHTML = ""
            }
            cell.appendChild(div_delete);
            cell.colSpan = 10;
            cell.style.paddingTop = "30px";

            row = tbody.insertRow(1);
            row.className = "display-none"
            row.id = comments[i].pk;
            row.style.backgroundColor = "light"


            parent_id = document.getElementById("parent_id");
            parent_id.setAttribute("value", row.id);
            parent_id.id = "parent_id-" + form_id

            form_replay = document.getElementById("form-replies");
            form_replay.id = "reply-" + row.id;
            div_form_replay = document.getElementById("div_form_replay");

            row = tbody.insertRow(2);
            row.className = "display-none";
            row.style.backgroundColor = "light";

            cell = row.insertCell(0);
            cell.colSpan = 10;
            cell.innerHTML = ""

            cell = row.insertCell(1);
            cell.innerHTML = div_form_replay.innerHTML;
            form_replay.id = "form-replies";
            input_tag_id.id = "input_tag_id";
            parent_id.id = "parent_id";
            cell.colSpan = 90;
        }
    }

    var comment_tr;
    var newrow;
    var replay_id;

    for (i = comments.length - 1; i >= 0; i--) {
        //adding replies

        if (comments[i].fields.is_reply) {
            replay_id = comments[i].pk
            parent_id = comments[i].fields.parent;
            comment_tr = document.getElementById(parent_id);
            newrow = document.createElement("tr")
            newrow.className = "display-none"
            newrow.style.backgroundColor = "light"
            cell = newrow.insertCell(0);
            cell.innerHTML = ""
            cell.className = "spacer header"
            cell.colSpan = 10

            cell = newrow.insertCell(1);
            table_comment = document.createElement("table");
            table_comment.className = "table table-borderless table-sm"
            row_comment = table_comment.insertRow(0);
            cell_comment = row_comment.insertCell(0);
            cell_comment.innerHTML = "<b>" + comments[i].fields.creator_name + "</b>";

            row_comment = table_comment.insertRow(1);
            cell_comment = row_comment.insertCell(0);
            cell_comment.innerHTML = comments[i].fields.body;
            cell_comment.style.wordWrap = "break-word";

            cell.appendChild(table_comment)
            cell.colSpan = 80

            cell = newrow.insertCell(2);
            div_delete = document.createElement("div");
            div_delete.className = "clickable";

            var num = tag_id
            if (user_id == comments[i].fields.creator) {
                div_delete.innerHTML = "<i class='fa fa-trash' aria-hidden='true' onclick='delete_comment(" + num + "," + replay_id + ")'></i>"
            } else {
                div_delete.innerHTML = ""
            }

            cell.appendChild(div_delete);
            cell.colSpan = 10;
            cell.style.paddingTop = "30px";

            comment_tr.parentNode.insertBefore(newrow, comment_tr.nextSibling);

        }

    }

    $(".showMore").click(function () {
        var tr = $(this).parent().parent().nextUntil('#comment_header');
        $(this).toggleClass('fa-angle-double-right fa-angle-double-down')
        if (tr.is(".display-none")) {
            tr.removeClass('display-none');
        } else {
            tr.addClass('display-none');
        }
    })

}

//adding dynamically form for adding comments on a tag
function commentForm(tag_id) {

    var input_id = document.getElementById("input_id")
    input_id.setAttribute("value", tag_id)
    var div = document.getElementById("add-comments");
    div.classList.remove("display-none");
}

//adding dynamically message - "No comments for this tag"
function noComments() {
    var table = document.getElementById("comments_table");
    table.innerHTML = "";
    var div = document.getElementById("no-comments");
    div.innerHTML = "No comments for this tag";
}

// post request for the comments on a tag
function sendCommentsRequest(tagId) {

    $.ajax({
        url: '/videos/comments/',
        type: 'POST',
        data: {
            csrfmiddlewaretoken: window.CSRF_TOKEN,
            'tag_id': tagId,
        },
        dataType: 'json',
        complete: function (data) {
            const statusCode = data.status
            if (statusCode === 200 || statusCode == 201) {
                var comments = JSON.parse(data.responseJSON.comments_list)
                //adding the comment form and the comments on the tag
                showComments(comments, data.responseJSON.tag_id)
                commentForm(tagId)
            }
            if (statusCode === 204) {
                //if there are no comments, show a message and the comment form
                noComments()
                commentForm(tagId)
            }

        }
    })
}

function displayErrors(errors) {
    if (errors.length > 0) {
        const err_string = errors.join('\n');
        bootbox.alert({

            message: err_string,
            centerVertical: true

        }).find("div.modal-content").addClass("confirmWidth");
    }

}

//submitting comment on a tag
$(function () {
    $('form[name=form-comments]').submit(function () {
        $.post($(this).attr('action'), $(this).serialize(), function (jsonData) {
            showComments(JSON.parse(jsonData.comments_list), jsonData.tag_id)
            document.getElementById("new-comment-body").value = ""
            commentForm(jsonData.tag_id)
            displayErrors(JSON.parse(jsonData.errors))
        }, "json");
        return false;
    });
})


