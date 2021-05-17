function updateTagCount(toClick, toDisable, counter, rating) {
    counter.innerText = rating
    if (toClick.classList.contains("active")) {
        toClick.classList.remove("active")
    } else {
        toClick.classList.add("active")
    }
    toDisable.classList.remove("active")
}

function sendVoteRequest(tagId, isUpvote, row) {
    const cols = document.getElementById("row-" + row).getElementsByClassName("vote-bar")[0].getElementsByTagName("td")
    const toClick = isUpvote ? cols[cols.length - 3].getElementsByTagName("i")[0] : cols[cols.length - 2].getElementsByTagName("i")[0]
    const toDisable = isUpvote ? cols[cols.length - 2].getElementsByTagName("i")[0] : cols[cols.length - 3].getElementsByTagName("i")[0]
    const counter = cols[cols.length - 1]

    if (toClick.classList.contains("active")) {
        isUpvote = "delete"
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
            const statusCode = data.status
            if (statusCode === 200 || statusCode == 201) {
                updateTagCount(toClick, toDisable, counter, data.responseJSON.tag_rating)
            }
            if (statusCode === 405) {
                alert("Method Not Allowed")
            }

        }
    });


}


var deleteTag = function (tagId) {
    console.log("Trying to delete tag: " + tagId)
    $(document).on("click", ".clickable.delete-tag", function (e) {
        bootbox.confirm("Are you sure you want to delete this tag?", function (result) {
            if (result) {
                $.ajax({
                    url: '/videos/delete_tag/',
                    type: 'POST',
                    data: {
                        csrfmiddlewaretoken: window.CSRF_TOKEN,
                        'tag_id': tagId,
                    },
                    dataType: 'json',
                    complete: function (data) {
                        const statusCode = data.status
                        if (statusCode == 200) {
                            if (document.getElementById("myTags").classList.contains("active")) {
                                location = window.location + "?showAllTags=False"
                            } else {
                                location = window.location + "?showAllTags=True"
                            }

                        }

                    }
                });
            }
        });
    });
}

document.getElementById("myTags").addEventListener("click", function () {
    if (!this.classList.contains("active")) {
        console.log("here")
        document.getElementById("allTags").classList.remove('active')
        document.getElementById("allTagBody").className = "inactive"
        this.classList.add("active")
        document.getElementById("myTagBody").className = "active"
        document.getElementById("id_showAllTags").value = "False"
    }

});

document.getElementById("allTags").addEventListener("click", function () {
    if (!this.classList.contains("active")) {
        document.getElementById("myTags").classList.remove('active')
        document.getElementById("myTagBody").className = "inactive"
        this.classList.add("active")
        document.getElementById("allTagBody").className = "active"
        document.getElementById("id_showAllTags").value = "True"
    }

});

