        // Toast notification function
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

        // Delete confirmation modal
        function confirmDelete(fileId, fileName) {
            const modal = document.getElementById('deleteModal');
            const confirmBtn = document.getElementById('confirmDeleteBtn');
            const message = document.querySelector('.modal-message');
            
            message.textContent = `Are you sure you want to delete "${fileName}"? This action cannot be undone.`;
            modal.style.display = 'flex';
            
            // Update confirm button to handle this specific file
            confirmBtn.onclick = function() {
                deleteVideo(fileId);
                closeModal();
            };
        }

        function closeModal() {
            const modal = document.getElementById('deleteModal');
            modal.style.display = 'none';
        }

        function deleteVideo(fileId) {
            fetch(`/delete/${fileId}`, {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    // Remove the element from the DOM
                    const videoElement = document.querySelector(`.video-item[data-id="${fileId}"]`);
                    if (videoElement) {
                        videoElement.remove();
                    }
                    
                    // Check if there are no more videos
                    const videoGrid = document.querySelector('.video-grid');
                    if (videoGrid && videoGrid.children.length === 0) {
                        const container = document.querySelector('.container');
                        const h2 = document.querySelector('h2');
                        
                        // Create no videos message
                        const noVideos = document.createElement('div');
                        noVideos.className = 'no-videos';
                        noVideos.innerHTML = `
                            <h3>No videos found</h3>
                            <p>Click "Record New Video" to create your first recording</p>
                        `;
                        
                        // Replace video grid with no videos message
                        container.replaceChild(noVideos, videoGrid);
                    }
                    
                    showToast('Video deleted successfully from Google Drive');
                } else {
                    showToast('Error deleting video: ' + data.message, 'error');
                }
            })
            .catch(error => {
                showToast('Error: ' + error, 'error');
            });
        }

        // Record video function
        document.getElementById('recordBtn').addEventListener('click', function() {
            // Disable the button and show recording status
            this.disabled = true;
            document.getElementById('recording-status').style.display = 'block';
            
            // Send AJAX request to record video
            fetch('/record', {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    // Reload the page to show the new video
                    window.location.reload();
                } else {
                    showToast('Error recording video: ' + data.message, 'error');
                    document.getElementById('recordBtn').disabled = false;
                    document.getElementById('recording-status').style.display = 'none';
                }
            })
            .catch(error => {
                showToast('Error: ' + error, 'error');
                document.getElementById('recordBtn').disabled = false;
                document.getElementById('recording-status').style.display = 'none';
            });
        });

        // Close modal when clicking outside
        window.onclick = function(event) {
            const modal = document.getElementById('deleteModal');
            if (event.target === modal) {
                closeModal();
            }
        }