const videoPlayer = document.getElementById('videoPlayer');
const videoError = document.getElementById('videoError');

videoPlayer.addEventListener('error', function() {
    console.error('Video error:', videoPlayer.error);
    videoError.style.display = 'block';
});

videoPlayer.addEventListener('loadeddata', function() {
    console.log('Video loaded successfully');
});

function showToast(message, type = 'success') {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = 'toast ' + type;
    toast.style.display = 'block';

    setTimeout(() => {
        toast.style.opacity = '0';
        setTimeout(() => {
            toast.style.display = 'none';
            toast.style.opacity = '1';
        }, 300);
    }, 3000);
}

function confirmDelete(file_id) {
    const modal = document.getElementById('deleteModal');
    const confirmBtn = document.getElementById('confirmDeleteBtn');

    modal.style.display = 'flex';

    confirmBtn.onclick = function() {
        deleteVideo(file_id);
        closeModal();
    };
}

function closeModal() {
    const modal = document.getElementById('deleteModal');
    modal.style.display = 'none';
}

function deleteVideo(file_id) {
    fetch(`/delete/${file_id}`, {
        method: 'POST',
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            showToast('Video deleted successfully');
            setTimeout(() => {
                window.location.href = "/"; // Index
            }, 1000);
        } else {
            showToast('Error deleting video: ' + data.message, 'error');
        }
    })
    .catch(error => {
        showToast('Error: ' + error, 'error');
    });
}

window.onclick = function(event) {
    const modal = document.getElementById('deleteModal');
    if (event.target === modal) {
        closeModal();
    }
}
