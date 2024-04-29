from flask import Flask, request
from youtube_transcript_api import YouTubeTranscriptApi
from transformers import pipeline
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
summarizer = pipeline('summarization')

@app.get('/summary')
def summary_api():
    url = request.args.get('url', '')
    video_id = url.split('=')[1]
    transcript = get_transcript(video_id)
    summary = get_summary(transcript)
    return summary, 200

@app.get('/article')
def article_api():
    url = request.args.get('url', '')
    article_text = scrape_article(url)
    summary = get_summary(article_text)
    return summary, 200

def get_transcript(video_id):
    transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
    transcript = ' '.join([d['text'] for d in transcript_list])
    return transcript

def scrape_article(url):
    # Scrape article data from URL
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    article_text = ' '.join([p.get_text() for p in soup.find_all('p')])
    return article_text

def get_summary(text):
    # Split text into smaller chunks
    chunk_size = 500  # You can adjust the chunk size as needed
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    
    # Generate summary for each chunk
    summary = ''
    for chunk in chunks:
        summary_text = summarizer(chunk)[0]['summary_text']
        summary += summary_text + ' '
    
    return summary

if __name__ == '__main__':
    app.run()
