
var youtubeVideoId; // replace with your own video id

var tag = document.createElement('script');
tag.src = "https://www.youtube.com/iframe_api";

var firstScriptTag = document.getElementById("youtube-tracking-script");
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

var video;

function setVideoId() {
    const iframe = document.getElementsByTagName('iframe')[0];
    console.log(iframe)
    youtubeVideoId = iframe['src'].split('/')[4].split("?")[0]
}

setVideoId()

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

function setToTime(duration) {
    const durations = duration.split(':');
    const hours = parseInt(durations[0]);
    const minutes = parseInt(durations[1]);
    const seconds = parseInt(durations[2]);
    const total_seconds = (hours * 3600) + (minutes * 60) + (seconds);
    video.seekTo(total_seconds, true);
}