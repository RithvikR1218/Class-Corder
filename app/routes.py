from flask import Blueprint, render_template, request, redirect, url_for, Response, session, jsonify
from datetime import datetime
import subprocess
import os
import logging
import io
import pickle
import traceback
from googleapiclient.http import MediaIoBaseDownload

from .utils.drive import (
    get_drive_service,
    get_or_create_folder,
    upload_video_to_drive,
    list_videos_from_drive,
    delete_video_from_drive
)

main = Blueprint('main', __name__)

VIDEO_DIR = "public/video/"
GDRIVE_FOLDER_NAME = "FlaskVideoRecorder"
os.makedirs(VIDEO_DIR, exist_ok=True)

@main.route('/')
def index():
    try:
        service = get_drive_service()
        if isinstance(service, Response):
            return service

        folder_id = get_or_create_folder(service, GDRIVE_FOLDER_NAME)
        gdrive_videos = list_videos_from_drive(service, folder_id)

        videos = [
            {
                'id': v['id'],
                'name': v['name'],
                'date': datetime.fromisoformat(v['createdTime'].replace('Z', '+00:00')).strftime('%Y-%m-%d %H:%M:%S'),
                'link': v.get('webContentLink', '')
            }
            for v in gdrive_videos
        ]

        videos.sort(key=lambda x: x['date'], reverse=True)
        return render_template('index.html', videos=videos)

    except Exception as e:
        logging.exception("Error in index route")
        return render_template('error.html', error=str(e))

@main.route('/play/<file_id>')
def play_video(file_id):
    try:
        service = get_drive_service()
        if isinstance(service, Response):
            return service

        file = service.files().get(fileId=file_id, fields='name').execute()
        return render_template('play.html', video_id=file_id, video_name=file['name'])

    except Exception as e:
        return render_template('error.html', error=str(e))

@main.route('/stream/<file_id>')
def stream_video(file_id):
    try:
        service = get_drive_service()
        if isinstance(service, Response):
            return service

        file = service.files().get(fileId=file_id, fields='name,mimeType').execute()
        buffer = io.BytesIO()
        request = service.files().get_media(fileId=file_id)
        downloader = MediaIoBaseDownload(buffer, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
        buffer.seek(0)

        return Response(
            buffer.read(),
            mimetype=file.get('mimeType', 'video/mp4'),
            headers={'Content-Disposition': f'inline; filename="{file['name']}"'}
        )
    except Exception as e:
        print("STREAMING ERROR:", traceback.format_exc())  # ← Add this
        return jsonify({"error": str(e)}), 500

@main.route('/record', methods=['POST'])
def record_video():
    try:
        service = get_drive_service()
        if isinstance(service, Response):
            return service

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        video_name = f"class_{timestamp}.mp4"
        output_path = os.path.join(VIDEO_DIR, video_name)

        subprocess.run([
            'ffmpeg',
            '-f', 'v4l2',
            '-input_format', 'mjpeg',
            '-video_size', '1920x1080',
            '-framerate', '30',
            '-t', '5',
            '-i', '/dev/video0',
            '-c:v', 'libx265',
            '-preset', 'slow',
            '-crf', '26',
            '-pix_fmt', 'yuv420p',
            '-movflags', '+faststart',
            output_path
        ], check=True)

        folder_id = get_or_create_folder(service, GDRIVE_FOLDER_NAME)
        uploaded_file = upload_video_to_drive(service, output_path, video_name, folder_id)
        os.remove(output_path)

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({
                "status": "success",
                "message": "Video uploaded to Google Drive",
                "file_id": uploaded_file['id'],
                "filename": uploaded_file['name']
            })
        else:
            return redirect(url_for('main.index'))

    except subprocess.CalledProcessError as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@main.route('/delete/<file_id>', methods=['POST'])
def delete_video(file_id):
    try:
        service = get_drive_service()
        if isinstance(service, Response):
            return service

        delete_video_from_drive(service, file_id)
        return jsonify({"status": "success", "message": "Video deleted successfully"})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@main.route('/auth/google/callback')
def oauth2callback():
    try:
        state = session.get('state')
        from .utils.drive import create_flow
        flow = create_flow()
        flow._state = state
        flow.fetch_token(authorization_response=request.url)

        credentials = flow.credentials
        with open('token.pickle', 'wb') as token:
            pickle.dump(credentials, token)

        return redirect(url_for('main.index'))
    except Exception as e:
        logging.exception("Error in OAuth callback")
        return render_template('error.html', error=str(e))