import os
import tempfile
from flask import Flask, request, send_file, render_template_string
from PIL import Image
from pydub import AudioSegment
import subprocess

app = Flask(__name__)

# mapping for extension groups
IMAGE_EXT = {'png','jpg','jpeg','gif','bmp','webp','tiff'}
AUDIO_EXT = {'mp3','wav','ogg','flac','aac'}
VIDEO_EXT = {'mp4','avi','mov','mkv','webm','flv','gif'}

INDEX_HTML = open('web/index.html').read()

@app.route('/')
def index():
    return render_template_string(INDEX_HTML)

@app.route('/convert', methods=['POST'])
def convert():
    if 'file' not in request.files or 'target_format' not in request.form:
        return 'Missing data', 400
    file = request.files['file']
    target_format = request.form['target_format'].lower()
    ext = file.filename.rsplit('.',1)[-1].lower()

    src_fd, src_path = tempfile.mkstemp(suffix='.'+ext)
    os.close(src_fd)
    file.save(src_path)

    dest_fd, dest_path = tempfile.mkstemp(suffix='.'+target_format)
    os.close(dest_fd)

    try:
        if ext in IMAGE_EXT and target_format in IMAGE_EXT:
            img = Image.open(src_path)
            img.save(dest_path, target_format.upper())
        elif ext in AUDIO_EXT and target_format in AUDIO_EXT:
            audio = AudioSegment.from_file(src_path)
            audio.export(dest_path, format=target_format)
        elif ext in VIDEO_EXT and target_format in VIDEO_EXT:
            cmd = [
                'ffmpeg', '-y', '-i', src_path,
                '-c:v', 'libx264', '-c:a', 'aac',
                dest_path
            ]
            subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            return 'Conversion not supported', 400
        return send_file(dest_path, as_attachment=True, download_name=f'converted.{target_format}')
    finally:
        os.remove(src_path)
        if os.path.exists(dest_path):
            os.remove(dest_path)

if __name__ == '__main__':
    app.run(debug=True)
