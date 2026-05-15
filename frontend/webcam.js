const video = document.getElementById("video");
const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");

let stream = null;

// Start webcam when page loads
async function startCamera() {
    try {
        stream = await navigator.mediaDevices.getUserMedia({
            video: {
                width: { ideal: 640 },
                height: { ideal: 480 }
            },
            audio: false
        });

        video.srcObject = stream;

        // IMPORTANT: wait until metadata is loaded
        video.onloadedmetadata = () => {
            video.play();
        };

    } catch (err) {
        alert("❌ Error accessing webcam: " + err.message);
        console.error(err);
    }
}

// Capture current frame from video
async function captureFrame() {
    if (!video.videoWidth || !video.videoHeight) {
        throw new Error("Video not ready");
    }

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    return new Promise(resolve => {
        canvas.toBlob(
            blob => resolve(blob),
            "image/jpeg",
            0.95   // quality
        );
    });
}

// Stop webcam (optional)
function stopCamera() {
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
        stream = null;
    }
}

// Start camera immediately
window.addEventListener("load", startCamera);
