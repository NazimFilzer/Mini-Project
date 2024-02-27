from flask import Flask, request
from youtube_transcript_api import YouTubeTranscriptApi
from transformers import pipeline
import nltk

# Install additional requirements (optional):
# pip install tqdm

app = Flask(__name__)

@app.get('/summary')
def summary_api():
    url = request.args.get('url', '')
    video_id = url.split('=')[1]

    # Optionally use tqdm for progress bar (requires tqdm installation)
    # from tqdm import tqdm

    summary = ""
    sentences = get_transcript(video_id)

    # Splitting based on sentences improves context
    summarizer = pipeline("summarization", model="t5-small")  # Smaller model alternative

    # Consider pre-processing to reduce transcript length (optional)
    # preprocessed_sentences = preprocess_transcript(sentences)

    # Summarize sentences while keeping context with sliding window
    window_size = 5  # Adjust window size based on model capabilities and desired summary length
    for i in range(0, len(sentences), window_size):
        window = sentences[i:i + window_size]
        window_summary = summarizer(window)[0]["summary_text"]
        summary += window_summary + " "

        # Optional progress bar using tqdm (requires installation)
        # print(f"Summarized {i // window_size + 1} out of {len(sentences) // window_size + 1} windows")

    return summary, 200


def get_transcript(video_id):
    transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
    transcript = " ".join([d["text"] for d in transcript_list])
    sentences = nltk.sent_tokenize(transcript)
    return sentences


# Optional pre-processing function (example)
def preprocess_transcript(sentences):
    # Implement your pre-processing logic here (e.g., remove greetings, simplify sentences)
    # Replace with your pre-processing code
    return sentences


if __name__ == "__main__":
    app.run()
