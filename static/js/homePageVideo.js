function appendNotFoundMessage() {
    document.getElementById("video-container").innerHTML =
        "Sorry, no videos were found"
}

function get_video_html(video) {


    const vid_wrapper = document.createElement("div")
    vid_wrapper.className = "bg-light border rounded"
    vid_wrapper.id = "video"

    // first child

    const first_child = document.createElement("h1");
    const vid_link = document.createElement("a")
    vid_link.className = "btn btn-link"
    vid_link.href = "/videos/" + video.pk
    vid_link.text = video.fields.name
    first_child.appendChild(vid_link)

    //second child

    const second_child = document.createElement("div")
    second_child.className = "video-responsive"
    const iframe = document.createElement("iframe")
    iframe.width = "480"
    iframe.height = "360"
    const videoId = video.fields.video.split('&')[0]
    iframe.src = videoId.replace("watch?v=","embed/") + "?wmode=opaque"
    iframe.loading = "lazy"
    iframe.setAttribute("allowfullscreen", '')
    second_child.appendChild(iframe)

    vid_wrapper.appendChild(first_child)
    vid_wrapper.appendChild(second_child)
    return vid_wrapper
}

function appendVideos(videos) {

    console.log(typeof(videos))

    document.getElementById("video-container").innerHTML = "";

    videos.forEach(function (vid) {
        console.log(vid)
        const col = document.createElement("div");
        col.className = "col-md-6 content-center"
        col.id = "video-column"
        col.appendChild(get_video_html(vid))
        document.getElementById("video-container").appendChild(col)
    })
}

function sendSearchRequest() {

    const searchTerm = document.getElementById("search-bar").value;

    console.log("Search term is: " + searchTerm)

    $.ajax({
        url: '/videos/search/',
        type: 'GET',
        data: {
            csrfmiddlewaretoken: window.CSRF_TOKEN,
            'search_term': searchTerm,
        },
        dataType: 'json',
        complete: function (data) {
            const statusCode = data.status
            if (statusCode === 200) {
                appendVideos(JSON.parse(data.responseJSON.videos))
            }
            if (statusCode === 204) {
                appendNotFoundMessage()
            }

        }
    });


}