const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const captureBtn = document.getElementById('scanBtn');
const sendBtn = document.getElementById('sendBtn');
let stream = null;

document.addEventListener('DOMContentLoaded', function() {
    
    const constraints = { video: true, audio: false };
    
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia(constraints)
            .then((mediaStream) => {
                stream = mediaStream;
                video.srcObject = stream;
                video.play();
                captureBtn.disabled = false;
            })
            .catch((err) => {
                console.error('Erreur caméra:', err);
                alert('Impossible d\'accéder à la caméra : ' + err.message);
            });
    } else {
        console.error('getUserMedia non supporté');
        alert('Votre navigateur ne supporte pas l\'accès à la caméra');
    }
});


captureBtn.addEventListener('click', () => {
    
    if (!video.videoWidth || !video.videoHeight) {
        alert('La vidéo n\'est pas encore prête');
        return;
    }
    
    const w = video.videoWidth;
    const h = video.videoHeight;
    canvas.width = w;
    canvas.height = h;
    const ctx = canvas.getContext('2d');
    
    video.style.display = 'none';
    ctx.drawImage(video, 0, 0, w, h);

    const dataUrl = canvas.toDataURL('image/png');
    canvas.style.display = 'inline';
    sendBtn.style.display = 'inline';
    document.querySelector(".output").style.display = "none";
    
});

sendBtn.addEventListener('click', () => {
    
    const canvas = document.getElementById('canvas');
    if (!canvas || canvas.width === 0) {
        console.error("Aucune photo capturée.");
        return;
    }
    
    const dataUrl = canvas.toDataURL('image/png');
    
    fetch('/upload', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ image: dataUrl }),
    })
    .then(response => response.json())
    .then(data => {
    })
    .catch(error => {
        console.error("Erreur lors de l'envoi :", error);
    });
});

// libérer la caméra (optionnel)
// window.addEventListener('beforeunload', () => {
//   if (stream) {
//     stream.getTracks().forEach(t => t.stop());
//   }
// });