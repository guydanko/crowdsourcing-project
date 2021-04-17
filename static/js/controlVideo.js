console.log('what')
var youtubeVideoId = 'u3A7bmEOtaU'; // replace with your own video id

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
        height: '352',
        width: '100%',
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
    console.log(typeof (duration));
    durations = duration.split(':');
    const minutes = parseInt(durations[0])
    const seconds = parseInt(durations[1])
    const total_seconds = minutes*60 + seconds
    video.seekTo(total_seconds, true);
}