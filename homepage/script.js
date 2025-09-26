const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const captureBtn = document.getElementById('scanBtn');
const sendBtn = document.getElementById('sendBtn');
const reloadBtn = document.getElementById('reloadBtn');
let stream = null;

function initCamera() {
    //ICI CA SERT A INITIALISER LA CAMERA
    const constraints = { video: true, audio: false };
    
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia(constraints)
            .then((mediaStream) => {
                stream = mediaStream;
                video.srcObject = stream;
                video.play();
                captureBtn.disabled = false;
                console.log('Caméra initialisée');
            })
            .catch((err) => {
                console.error('Erreur caméra:', err);
                alert('Impossible d\'accéder à la caméra : ' + err.message);
            });
    } else {
        console.error('getUserMedia non supporté');
        alert('Votre navigateur ne supporte pas l\'accès à la caméra');
    }
}

document.addEventListener('DOMContentLoaded', function() {
    initCamera();
});
//ICI CA SERT A CAPTURER L'IMAGE

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
    reloadBtn.style.display = 'inline';
    document.querySelector(".output").style.display = "none";
    
});
//ICI CA SERT A ENVOYER L'IMAGE
sendBtn.addEventListener('click', () => {
    
    const canvas = document.getElementById('canvas');
    if (!canvas || canvas.width === 0) {
        console.error("Aucune photo capturée.");
        const resultElement = document.querySelector('.objet');
        resultElement.textContent = "Aucune photo capturée";
        resultElement.style.color = '#ff4444';
        return;
    }
    
    const dataUrl = canvas.toDataURL('image/png');
    
    const resultElement = document.querySelector('.objet');
    resultElement.textContent = "Analyse en cours...";
    resultElement.style.color = '#54FE55';
    
    fetch('/upload', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ image: dataUrl }),
    })
    //ICI CA SERT A RECEVOIR LA REPONSE DE L'API
    .then(response => {
        if (!response.ok) {
            throw new Error(`Erreur HTTP: ${response.status}`);
        }
        return response.json();
    })
    //ICI CA SERT A AFFICHER LE RESULTAT DE L'ANALYSE
    .then(data => {
        console.log("Résultat de l'analyse :", data);
        if (data.success) {
            resultElement.textContent = `${data.result.object} (${data.result.confidence * 100}% de confiance) - +${data.result.credits_earned} crédits`;
            resultElement.style.color = '#54FE55';
            resultElement.style.fontWeight = 'bold';
            
            //ICI CA SERT A REINITIALISER L'INTERFACE
            video.style.display = 'inline';
            canvas.style.display = 'none';
            sendBtn.style.display = 'none';
            reloadBtn.style.display = 'none';
            document.querySelector(".output").style.display = "block";
        } else {
            resultElement.textContent = `Erreur: ${data.error}`;
            resultElement.style.color = '#ff4444';
        }
    })
    .catch(error => {
        console.error("Erreur lors de l'analyse :", error);
        resultElement.textContent = `Erreur lors de l'analyse: ${error.message}`;
        resultElement.style.color = '#ff4444';
    });
});

//ICI CA SERT A RELANCER LA CAMERA
reloadBtn.addEventListener('click', () => {
    
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
    }
    
    video.style.display = 'inline';
    canvas.style.display = 'none';
    sendBtn.style.display = 'none';
    reloadBtn.style.display = 'none';
    document.querySelector(".output").style.display = "block";
    
    initCamera();
});

// libérer la caméra (optionnel)
// window.addEventListener('beforeunload', () => {
//   if (stream) {
//     stream.getTracks().forEach(t => t.stop());
//   }
// });