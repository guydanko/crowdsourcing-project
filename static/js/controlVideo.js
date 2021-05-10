var youtubeVideoId; // replace with your own video id

var tag = document.createElement('script');
tag.src = "https://www.youtube.com/iframe_api";

var firstScriptTag = document.getElementById("youtube-tracking-script");
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

var video;


function setVideoId() {
    const iframe = document.getElementsByTagName('iframe')[0];
    youtubeVideoId = iframe['src'].split('/')[4].split("?")[0]
    console.log(youtubeVideoId)
}

function onYouTubeIframeAPIReady() {
    video = new YT.Player('video-youtube', {
        height: '700',
        width: '700',
        videoId: youtubeVideoId,
        playerVars: {rel: 0, showinfo: 0},
        events: {
            'onStateChange': videoPlay
        }
    });
}

function videoPlay(event) {
    if (event.data == YT.PlayerState.PLAYING) {
        console.log("YouTube Video is PLAYING!!");
    }
    if (event.data == YT.PlayerState.PAUSED) {
        console.log("YouTube Video is PAUSED!!");
    }
    if (event.data == YT.PlayerState.ENDED) {
        console.log("YouTube Video is ENDING!!");
    }
}

function playVideo() {
    video.playVideo();
}

setVideoId()

var tableBodies = document.getElementsByClassName("set-time-click");

var setDuration = function () {
    const duration = this.textContent;
    const durations = duration.split(':');
    if (durations.length == 3) {
        var hours = parseInt(durations[0]);
        var minutes = parseInt(durations[1]);
        var seconds = parseInt(durations[2]);
    } else {
        var hours = 0;
        var minutes = parseInt(durations[0]);
        var seconds = parseInt(durations[1]);
    }
    const total_seconds = (hours * 3600) + (minutes * 60) + (seconds);
    const play = video.getDuration();
    video.seekTo(total_seconds, true);

};

for (var i = 0; i < tableBodies.length; i++) {
    tableBodies[i].addEventListener('click', setDuration, false);
}
