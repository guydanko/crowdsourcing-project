
function showComments(comments){
     txt=comments[0].fields.body
    console.log(comments[0].fields.body)
     document.getElementById('comments_div').innerHTML =txt
}

function noComments(){
    txt = "No comments for this tag"
    document.getElementById("comments_div").innerHTML =txt
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
                // console.log('hello')
                 console.log(data.responseJSON.comments_list)
                showComments(JSON.parse(data.responseJSON.comments_list))
            }
            if (statusCode === 204) {
                noComments()
            }

        }
        })
}
