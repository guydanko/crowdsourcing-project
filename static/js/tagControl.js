


function sendVoteRequest(tag_id, is_upvote) {
    console.log("No was here")
    $.ajax({
        url: '/videos/vote/',
        type: 'POST',
        data: {csrfmiddlewaretoken: window.CSRF_TOKEN,
            'tag_id': tag_id,
            'is_upvote': is_upvote},
        dataType: 'json',
        success: function (data) {

            alert("We made a vote.");

        }
    });
}