
function showComments(comments){
    var div = document.getElementById("no-comments");
    div.innerHTML = ""

    var table = document.getElementById("comments_table")
    table.innerHTML = "";

    var header = table.createTHead();
    header.style.color = "#FFFFFF";
    var row = header.insertRow(0);
    row.style.backgroundColor ="#000000";
    var cell = row.insertCell(0);
    cell.innerHTML = "";
    cell.colSpan = 20

    cell = row.insertCell(1);
    cell.innerHTML = "<b>Comments</b>";
    cell.colSpan = 80

    var tbody = document.createElement("TBODY");
    table.appendChild(tbody);

    for (i=comments.length-1; i>=0;i--) {
        //adding comments
        if (! comments[i].fields.is_reply){
            row = tbody.insertRow(0);
            row.id = "comment_header"
            row.style.backgroundColor = "azure"
            cell = row.insertCell(0);
            cell.colSpan = 20
            cell.innerHTML = "<i class='showMore fa fa-angle-double-right'></i>"

            cell =row.insertCell(1);
            cell.innerHTML = comments[i].fields.body
            cell.colSpan = 80

            row = tbody.insertRow(1);
            row.className = "display-none"
            row.id = comments[i].pk;
            row.style.backgroundColor = "light"

            cell = row.insertCell(0);
             cell.innerHTML = ""
            cell.colSpan = 30

            cell = row.insertCell(1);
             cell.innerHTML = "<b>Replies</b>"
            cell.colSpan = 70;

             row = tbody.insertRow(2);
             row.className = "display-none"
            row.style.backgroundColor = "light"
            cell = row.insertCell(0);
             cell.innerHTML = "<button type='submit' class='btn btn-primary' , name='save comment'>Replay</button>"
            cell.colSpan = 20

            cell = row.insertCell(1);
             cell.innerHTML ="<input type='text' name='body' class='form-control' required>"


            cell.colSpan = 80;
        }
    }

    for (i=comments.length-1; i>=0;i--){
        //adding replies
        var parent_id
        var comment_tr
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
            cell.colSpan = 30

            cell = newrow.insertCell(1);
            cell.innerHTML = comments[i].fields.body
            cell.colSpan = 70

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
}


function commentForm(tag_id){
    var div = document.getElementById("add-comments");
    div.classList.remove("display-none");
    form = document.getElementById("form-comments");


    var input_id = document.createElement("input") ;
    input_id.type = "hidden";
    input_id.name = "tag_id";
    input_id.value = tag_id;

    form.appendChild(input_id)



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
                 console.log(data.responseJSON.comments_list)
                var comments = JSON.parse(data.responseJSON.comments_list)
                showComments(comments)
                console.log("tag_id: "+data.responseJSON.tag_id)
                commentForm(data.responseJSON.tag_id)
            }
            if (statusCode === 204) {
                noComments()
                commentForm()
            }

        }
        })
}
