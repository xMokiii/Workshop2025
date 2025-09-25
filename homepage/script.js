const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const captureBtn = document.getElementById('scanBtn');
const sendBtn = document.getElementById('sendBtn');
let stream = null;

const constraints = { video: true, audio: false };
navigator.mediaDevices.getUserMedia(constraints)
  .then((stream) => {
    video.srcObject = stream;
    captureBtn.disabled = false;
  })
  .catch ((err) => {
    alert('Impossible d’accéder à la caméra : ' + err.message);
    console.error(err);
  });


captureBtn.addEventListener('click', () => {
  // réglage canvas sur la taille vidéo réelle
  const w = video.videoWidth;
  const h = video.videoHeight;
  canvas.width = w;
  canvas.height = h;
  const ctx = canvas.getContext('2d');
  video.style.display = 'none';
  // flip horizontal si selfie souhaité : ctx.translate(w,0); ctx.scale(-1,1);
  ctx.drawImage(video, 0, 0, w, h);

  // obtenir dataURL (PNG) et proposer le téléchargement
  const dataUrl = canvas.toDataURL('image/png');
  // captureBtn.href = dataUrl;
  // captureBtn.download = 'capture.png';
  canvas.style.display = 'inline';
  sendBtn.style.display = 'inline';
  document.querySelector(".output").style.display="none";
  sendBtn.addEventListener('click', () => {
    if (!dataUrl) {
        console.error("Aucune photo capturée.");
        return;
    } else {
        fetch('/upload', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ image: dataUrl }),
        })
        .then(response => response.json())
        .then(data => {
            console.log("Réponse du serveur :", data);
        })
        .catch(error => {
            console.error("Erreur lors de l'envoi :", error);
        });
    }
  });
});

// libérer la caméra (optionnel)
// window.addEventListener('beforeunload', () => {
//   if (stream) {
//     stream.getTracks().forEach(t => t.stop());
//   }
// });