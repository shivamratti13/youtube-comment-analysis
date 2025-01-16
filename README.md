# YouTube Sentiment Analysis: Decode Viewer Emotions

 **Unlock Insights from YouTube Comments with AI-Powered Sentiment Analysis**

##  Overview
This project provides a **Streamlit-based web application** that analyzes YouTube video comments to decode audience sentiment. Leveraging the **YouTube Data API** and a fine-tuned **DistilBERT model**, it classifies viewer emotions into **Positive, Negative, Neutral, and Undetectable** categories. With dynamic visualizations, this tool helps content creators and marketers understand their audience better.

##  Features
- **Real-time YouTube Comment Analysis**: Fetch comments, likes, and engagement metrics using the YouTube Data API.
- **AI-Powered Sentiment Classification**: Uses a DistilBERT model fine-tuned on the IMDb dataset, achieving **93.45% accuracy** on test data.
- **Interactive Visualizations**: Displays sentiment trends through bar and donut charts for better insights.
- **User-Friendly Interface**: Built with Streamlit for seamless user experience and accessibility.

##  Tech Stack
- **Python**
- **Streamlit** (for the web app)
- **DistilBERT** (for sentiment analysis)
- **YouTube Data API** (to fetch video metrics & comments)
- **Matplotlib & Plotly** (for data visualization)

##  How to Run the Project
### 1️⃣ Clone the Repository
```bash
git clone https://github.com/shivamratti13/youtube-comment-analysis.git
cd youtube-comment-analysis
```
### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```
### 3️⃣ Run the Streamlit App
```bash
streamlit run app.py
```

##  Visualizations
The app presents sentiment analysis results with **dynamic bar and donut charts**, making it easier to interpret audience emotions at a glance.

##  Deployment
The project is designed for seamless deployment, enabling users to analyze YouTube video sentiment in real time.

##  Contributing
Feel free to contribute by submitting **issues** or **pull requests**! 🚀

##  License
This project is licensed under the **MIT License**.

##  Connect
GitHub Repository: [youtube-comment-analysis](https://github.com/shivamratti13/youtube-comment-analysis)
