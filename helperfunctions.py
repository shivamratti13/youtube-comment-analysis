import requests
import re
from transformers import pipeline
import plotly.express as px
import streamlit as st

# Extract Video ID
def extract_video_id(url):
    parts = url.split('=')
    video_id = ''
    for i in range(1,len(parts)):
        video_id += parts[i]
        if i!=(len(parts)-1):
            video_id += '='
    return video_id

def get_video_title(video_id, api_key):
    url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data["items"][0]["snippet"]["title"]
    else:
        return "Title not found"
    
def get_video_details(video_id, api_key):
    url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet,contentDetails,statistics&id={video_id}&key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if "items" in data and len(data["items"]) > 0:
            video_data = data["items"][0]
            snippet = video_data["snippet"]
            content_details = video_data["contentDetails"]
            statistics = video_data["statistics"]
            
            details = {
                "title": snippet["title"],
                "upload_date": snippet["publishedAt"].split("T")[0],  # Extract date
                "duration": content_details["duration"],
                "likes": statistics.get("likeCount", "N/A"),
                "comments": statistics.get("commentCount", "N/A")
            }
            return details
    return None

def format_duration(iso_duration):
    import isodate
    duration = isodate.parse_duration(iso_duration)
    return str(duration)

def get_top_level_comments(video_id,youtube):
    comments = []
    request = youtube.commentThreads().list(
        part='snippet',
        videoId=video_id,
        maxResults=100  # Maximum allowed per request
    )

    while request:
        response = request.execute()

        for item in response.get('items', []):
            top_level_comment = item['snippet']['topLevelComment']['snippet']
            comment_text = top_level_comment['textDisplay']
            comments.append(comment_text)

        # Get the next page of comments
        request = youtube.commentThreads().list_next(request, response)

    return comments

def clean_data(text):
    """
    Clean Twitter data by removing usernames, emojis, URLs, and HTML tags.

    Parameters:
    text (str): The text to clean.

    Returns:
    str: The cleaned text.
    """

    # Remove usernames (e.g., @username)
    text = re.sub(r"@\w+", "", text)

    # Remove emojis
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # Emoticons
        "\U0001F300-\U0001F5FF"  # Symbols & Pictographs
        "\U0001F680-\U0001F6FF"  # Transport & Map Symbols
        "\U0001F1E0-\U0001F1FF"  # Flags (iOS)
        "\U00002702-\U000027B0"  # Dingbats
        "\U000024C2-\U0001F251"  # Enclosed characters
        "]+",
        flags=re.UNICODE,
    )
    text = emoji_pattern.sub(r"", text)

    # Remove URLs
    text = re.sub(r"http\S+|www\S+|https\S+", "", text, flags=re.MULTILINE)

    # Remove HTML tags
    text = re.sub(r"<.*?>", "", text)

    # Remove extra whitespaces
    text = re.sub(r"\s+", " ", text).strip()

    return text


def plot_sentiment_graphs(df):
    # Sentiment counts
    sentiment_counts = df['Sentiments'].value_counts().reset_index()
    sentiment_counts.columns = ['Sentiment', 'Count']
    
    # Define colors
    colors = {'POSITIVE': '#4C78A3', 'NEUTRAL': '#BAB0AC', 'NEGATIVE': '#E45756', "CAN'T DETECT": '#9D755D'}
    
    # Bar Graph
    fig_bar = px.bar(
        sentiment_counts,
        x='Sentiment',
        y='Count',
        color='Sentiment',
        color_discrete_map=colors,
        title='Sentiment Count Bar Graph'
    )
    
    st.plotly_chart(fig_bar)
    
    # Donut Chart
    fig_donut = px.pie(
        sentiment_counts,
        values='Count',
        names='Sentiment',
        color='Sentiment',
        color_discrete_map=colors,
        hole=0.4,
        title='Sentiment Distribution Donut Chart'
    )
    st.plotly_chart(fig_donut)
