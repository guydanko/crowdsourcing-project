function updateTagCount(toClick, toDisable, counter, rating) {
    console.log()
    counter.innerText = rating
    console.log(toClick)
    if (toClick.classList.contains("active")){
        toClick.classList.remove("active")
    }
    else {
         toClick.classList.add("active")
    }
    toDisable.classList.remove("active")
}

function sendVoteRequest(tagId, isUpvote, row) {
    const cols = document.getElementById("row-" + row).getElementsByTagName("td")
    const toClick = isUpvote ? cols[cols.length - 3].getElementsByTagName("i")[0] : cols[cols.length - 2].getElementsByTagName("i")[0]
    const toDisable = isUpvote ? cols[cols.length - 2].getElementsByTagName("i")[0] : cols[cols.length - 3].getElementsByTagName("i")[0]
    const counter = cols[cols.length - 1]

    if (toClick.classList.contains("active")) {
        isUpvote = !isUpvote
    }

    $.ajax({
        url: '/videos/vote/',
        type: 'POST',
        data: {
            csrfmiddlewaretoken: window.CSRF_TOKEN,
            'tag_id': tagId,
            'is_upvote': isUpvote
        },
        dataType: 'json',
        complete: function (data) {
            console.log(Object.keys(data))
            switch (data.status) {
                case 200:
                    updateTagCount(toClick, toDisable, counter, data.responseJSON.tag_rating)
                    break
                case 405:
                    alert("Method Not Allowed")
            }

        }
    });


}