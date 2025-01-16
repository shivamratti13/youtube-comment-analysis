import streamlit as st
import helperfunctions
import googleapiclient.discovery
import googleapiclient.errors
import pandas as pd
from transformers import pipeline
import os

api_service_name = "youtube"
api_version = "v3"
api_key = "AIzaSyB-N3AxiJ_WudM-MwJw_PMAP4Y1kB1HSeY"

classifier = pipeline("sentiment-analysis", model="shivamratti/my_fine_tuned_model")

youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey = api_key)

st.title("YouTube Video Comment Sentiment Analysis")

# Input for YouTube video link
video_url = st.text_input("Enter YouTube video URL:")


if st.button("Analyze"):
    if video_url:
        # Extract video ID
        video_id = helperfunctions.extract_video_id(video_url)
        if video_id:
            st.info("Fetching comments...")

            # api_key = st.text_input("Enter your YouTube Data API key:", type="password")

            if api_key:
                video_details = helperfunctions.get_video_details(video_id, api_key)

                if video_details:
                    # Display the video title and thumbnail
                    st.subheader(video_details["title"])
                    thumbnail_url = f"https://img.youtube.com/vi/{video_id}/0.jpg"
                    st.image(thumbnail_url, caption="YouTube Thumbnail")
                    
                    # Display details in columns
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Likes", video_details["likes"], border=True)
                    col2.metric("Comments", video_details["comments"], border=True)
                    col3.metric("Duration", helperfunctions.format_duration(video_details["duration"]), border=True)

                    # Getting Top Level Comments
                    top_level_comments = helperfunctions.get_top_level_comments(video_id, youtube)
                    df = pd.DataFrame(top_level_comments, columns=['Top-Level Comment'])
                    
                    # Preprocessing
                    df['new_comment'] = df['Top-Level Comment'].apply(helperfunctions.clean_data)

                    sentiments = []
                    for text in df["new_comment"]:
                        sentiment = classifier(str(text))[0]
                        pos_count,neg_count,neu_count = 0,0,0
                        if sentiment['score'] < 0.7:
                            sentiment['label'] = "NEUTRAL"
                        elif sentiment['score'] >= 0.7 and sentiment['label'] == 'POSITIVE':
                            sentiment['label'] = "POSITIVE"
                        elif sentiment['score'] >= 0.7 and sentiment['label'] == 'NEGATIVE':
                            sentiment['label'] = "NEGATIVE"
                        else:
                            sentiment['label'] = "CAN'T DETECT"

                        sentiments.append(sentiment['label'])

                    df['Sentiments'] = sentiments

                    # Displaying Charts
                    helperfunctions.plot_sentiment_graphs(df)

                    new_df = df[["Top-Level Comment","Sentiments"]]

                    st.dataframe(new_df)

            else:
                st.subheader("Error Fetching Video Details")
        else:
            st.subheader("Incorrect Video Id or Error Fetching the details")
    else:
        st.subheader("Please Enter Video URL")
                