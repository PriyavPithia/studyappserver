from flask import Flask, request, jsonify
from flask_cors import CORS
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

app = Flask(__name__)
CORS(app)  # This enables CORS for all routes

@app.route("/api/home", methods=['GET'])
def return_home():
    return jsonify({
        'message': "Home Page"
    })

@app.route('/transcribe', methods=['POST'])
def transcribe():
    data = request.json
    print("Received data:", data)  # Debugging line
    video_url = data.get('url')
    print("Video URL:", video_url)  # Debugging line

    # Extract video ID from the URL
    video_id = video_url.split('v=')[-1].split('&')[0]

    try:
        # Fetch the transcript
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        
        # Optionally format the transcript
        formatter = TextFormatter()
        formatted_transcript = formatter.format_transcript(transcript)

        return jsonify({'transcript': formatted_transcript}), 200
    except Exception as e:
        print("Error:", str(e))  # Debugging line
        return jsonify({'error': str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)