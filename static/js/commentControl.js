function create_reply(oForm){
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
            console.log(statusCode)
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
        })
}

function delete_comment(tag_id, comment_id){
    console.log("in delete_comment!!")
    console.log("tag_id: "+tag_id)
    console.log("comment_id: "+ comment_id)
    $.ajax({
        url: '/videos/delete_comment/',
        type: 'POST',
        data: {
            csrfmiddlewaretoken: window.CSRF_TOKEN,
            'tag_id': tag_id,
            'comment_id' : comment_id
        },
        dataType: 'json',
        complete: function (data) {
            const statusCode = data.status
            console.log(statusCode)
            if (statusCode === 200 || statusCode == 201) {
                 // console.log(data.responseJSON.comments_list)
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



function showComments(comments, tag_id){

    var div = document.getElementById("no-comments");
    div.innerHTML = ""

    var table = document.getElementById("comments_table")
    table.innerHTML = "";

    var header = table.createTHead();
    header.style.color = "#FFFFFF";

    var row = header.insertRow(0);
    row.style.backgroundColor ="#000000";

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
    console.log("input_tag_id.value: "+input_tag_id.value);
    input_tag_id.id = "input_tag_id-"+tag_id;

    var parent_id;
    var div_form_replay;
    var form_replay;
    var div_delete;

    for (i=comments.length-1; i>=0;i--) {
        //adding comments
        if (! comments[i].fields.is_reply){
            var form_id = comments[i].pk;
            console.log("start show comment "+i+" body: "+comments[i].fields.body)
            row = tbody.insertRow(0);
            row.id = "comment_header"
            row.style.backgroundColor = "azure"
            cell = row.insertCell(0);
            cell.colSpan = 5
            cell.innerHTML = "<i class='showMore fa fa-angle-double-right'></i>"

            cell =row.insertCell(1);
            cell.innerHTML = comments[i].fields.body;
            cell.colSpan = 65;
            cell.style.wordWrap = "break-word";

            cell =row.insertCell(2);
            cell.innerHTML = comments[i].fields.creator_name;
            cell.colSpan = 20;
            cell.style.wordWrap = "break-word";

            cell =row.insertCell(3);
            cell.colSpan = 10;
            div_delete = document.createElement("div");
            div_delete.className = "clickable";
            div_delete.onclick = function (){
                delete_comment(tag_id,form_id);
            }


            if(user_id == comments[i].fields.creator){
                div_delete.innerHTML = "<i class='fa fa-trash' aria-hidden='true'></i>"
                console.log("Im the creator!!");
            }else{
                console.log("Im not the creator!!");
                div_delete.innerHTML = ""

            }
            console.log(div_delete.innerHTML)
            cell.appendChild(div_delete) ;
            cell.colSpan = 10;

            row = tbody.insertRow(1);
            row.className = "display-none"
            row.id = comments[i].pk;
            row.style.backgroundColor = "light"

            cell = row.insertCell(0);
             cell.innerHTML = "";
            cell.colSpan = 10;

            cell = row.insertCell(1);
             cell.innerHTML = "<b>Replies</b>"
            cell.colSpan = 90;

             parent_id = document.getElementById("parent_id") ;
             parent_id.setAttribute("value", row.id);
              // console.log("parent_id.value: "+parent_id.value)
            parent_id.id = "parent_id-"+form_id

            form_replay = document.getElementById("form-replies");
            form_replay.id = "reply-"+row.id;
             div_form_replay = document.getElementById("div_form_replay");

             row = tbody.insertRow(2);
             row.className = "display-none";
             row.style.backgroundColor = "light";

             cell = row.insertCell(0);
             cell.innerHTML = div_form_replay.innerHTML;
             form_replay.id = "form-replies";
             input_tag_id.id = "input_tag_id";
            parent_id.id = "parent_id";
             cell.colSpan = 100;

            console.log("finish show comment______");

    }}

    var comment_tr;
    var newrow;
    var replay_id;

    for (i=comments.length-1; i>=0;i--){
        //adding replies
        console.log("start show replay "+i+" body: "+comments[i].fields.body)
        if ( comments[i].fields.is_reply ){
            replay_id = comments[i].pk
            parent_id = comments[i].fields.parent;
            // console.log("parent_id: "+parent_id)
            comment_tr = document.getElementById(parent_id);
            newrow = document.createElement("tr")
            newrow.className = "display-none"
            newrow.style.backgroundColor = "light"
            cell = newrow.insertCell(0);
            cell.innerHTML = ""
            cell.className = "spacer header"
            cell.colSpan = 10

            cell = newrow.insertCell(1);
            cell.innerHTML = comments[i].fields.body
            cell.style.wordWrap = "break-word"
            cell.colSpan = 80

            cell = newrow.insertCell(2);
            div_delete = document.createElement("div");
            div_delete.className = "clickable";
            div_delete.onclick = function (){
                delete_comment(tag_id,replay_id);
            }
            if(user_id == comments[i].fields.creator){
                console.log("Im the creator!!")
                div_delete.innerHTML = "<i class='fa fa-trash' aria-hidden='true'></i>"
            }else{
                console.log("Im not the creator!!")
                div_delete.innerHTML = ""
            }

            cell.appendChild(div_delete) ;
            cell.colSpan = 10;

             comment_tr.parentNode.insertBefore(newrow, comment_tr.nextSibling);
            console.log("finish show replay______")

        }

    }

    $(".showMore").click(function() {
        var tr = $(this).parent().parent().nextUntil('#comment_header');
        $(this).toggleClass('fa-angle-double-right fa-angle-double-down')
        if (tr.is(".display-none")) {
        tr.removeClass('display-none');
        } else {
            tr.addClass('display-none');
        }
    })

    console.log("finish show comment!");
}


function commentForm(tag_id){

    var input_id = document.getElementById("input_id")
    input_id.setAttribute("value", tag_id)
    var div = document.getElementById("add-comments");
    div.classList.remove("display-none");
}

function noComments(){
    var table = document.getElementById("comments_table");
    table.innerHTML = "";
    var div = document.getElementById("no-comments");
    div.innerHTML = "No comments for this tag";
}

function sendCommentsRequest(tagId){

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
            console.log(statusCode)
            if (statusCode === 200 || statusCode == 201) {
                 // console.log(data.responseJSON.comments_list)
                var comments = JSON.parse(data.responseJSON.comments_list)
                showComments(comments, data.responseJSON.tag_id)
                // console.log("tag_id: "+data.responseJSON.tag_id)
                commentForm(tagId)
            }
            if (statusCode === 204) {
                noComments()
                commentForm(tagId)
            }

        }
        })
}
$(function(){
  $('form[name=form-comments]').submit(function(){
    $.post($(this).attr('action'), $(this).serialize(), function(jsonData) {
        showComments(JSON.parse(jsonData.comments_list),jsonData.tag_id)
        commentForm(jsonData.tag_id)
    }, "json");
    return false;
  });
})


