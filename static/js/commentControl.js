
function showComments(){
    // for (a_comment in comments){
    //     const Creator = a_comment.creator
    //
    // }

    txt='comments lists'
    document.getElementById('comments').innerHTML =txt
}

function noComments(){
    txt = "No comments for this tag"
    document.getElementById("comments").innerHTML =txt
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
            // console.log(data.responseType)
             const comments = JSON.parse(data.responseData.comments_list)
            if (statusCode === 204) {
                showComments()
            }
            if (statusCode === 200) {
                noComments()
            }

        }
        })
}
