
function showComments(comments, tag_id){
    console.log("1 tag_id: "+tag_id)
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
    cell.colSpan = 90

    var tbody = document.createElement("TBODY");
    table.appendChild(tbody);

    var input_tag_id = document.getElementById("input_tag_id") ;
    input_tag_id.setAttribute("value", tag_id);
    var parent_id;
    var div_form_replay;

    for (i=comments.length-1; i>=0;i--) {
        //adding comments
        if (! comments[i].fields.is_reply){
            row = tbody.insertRow(0);
            row.id = "comment_header"
            row.style.backgroundColor = "azure"
            cell = row.insertCell(0);
            cell.colSpan = 5
            cell.innerHTML = "<i class='showMore fa fa-angle-double-right'></i>"

            cell =row.insertCell(1);
            cell.innerHTML = comments[i].fields.body
            cell.colSpan = 95
            cell.style.wordWrap = "break-word"

            row = tbody.insertRow(1);
            row.className = "display-none"
            row.id = comments[i].pk;
            row.style.backgroundColor = "light"

            cell = row.insertCell(0);
             cell.innerHTML = ""
            cell.colSpan = 20

            cell = row.insertCell(1);
             cell.innerHTML = "<b>Replies</b>"
            cell.colSpan = 80;

             console.log("row.id: "+row.id)
             parent_id = document.getElementById("parent_id") ;
             parent_id.setAttribute("value", row.id);
             console.log("parent_id.value: "+parent_id.value)

             div_form_replay = document.getElementById("div_form_replay");
             console.log(div_form_replay.innerHTML);


             row = tbody.insertRow(2);
             row.className = "display-none"
            row.style.backgroundColor = "light"
            row.innerHTML = div_form_replay.innerHTML;

        }

        // console.log(row.innerHTML);

    }

    for (i=comments.length-1; i>=0;i--){
        //adding replies
        var parent_id;
        var comment_tr;
        var newrow;
        if ( comments[i].fields.is_reply ){
            parent_id = comments[i].fields.parent;
            comment_tr = document.getElementById(parent_id);
            newrow = document.createElement("tr")
            newrow.className = "display-none"
            newrow.style.backgroundColor = "light"
            cell = newrow.insertCell(0);
            cell.innerHTML = ""
            cell.className = "spacer header"
            cell.colSpan = 20

            cell = newrow.insertCell(1);
            cell.innerHTML = comments[i].fields.body
            cell.style.wordWrap = "break-word"
            cell.colSpan = 80

             comment_tr.parentNode.insertBefore(newrow, comment_tr.nextSibling);

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
    console.log("finish show comment!")
}


function commentForm(tag_id){

    var input_id = document.getElementById("input_id")
    input_id.setAttribute("value", tag_id)
    var div = document.getElementById("add-comments");
    div.classList.remove("display-none");
    // console.log(div.innerHTML)



}

function noComments(){
    var table = document.getElementById("comments_table")
    table.innerHTML = "";
    var div = document.getElementById("no-comments");
    div.innerHTML = "No comments for this tag"

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
                commentForm(data.responseJSON.tag_id)
            }
            if (statusCode === 204) {
                noComments()
                commentForm(data.responseJSON.tag_id)
            }

        }
        })
}
$(function(){
  $('form[name=form-comments]').submit(function(){
    $.post($(this).attr('action'), $(this).serialize(), function(jsonData) {
        showComments(JSON.parse(jsonData.comments_list))
    }, "json");
    return false;
  });
});

$(function(){
  $('form[name=form-replies]').submit(function(){
      console.log("before response!!!")
    $.post($(this).attr('action'), $(this).serialize(), function(jsonData) {
        console.log("after response!!!")
        showComments(JSON.parse(jsonData.comments_list), jsonData.tag_id)
    }, "json");
    return false;
  });
});