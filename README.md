# 🎵 MoodTunes — Mood-Based Hindi Song Recommender

> **"Your mood. Your music."**

**MoodTunes** is a modern, Spotify-inspired web application built with Python and Streamlit. It recommends popular Hindi and Bollywood songs based on your current mood, preferred genre, and favorite artists.

---

## 🌟 Key Features

- **😊 Emoji-Based Mood Selection**: Choose from 9 distinct moods (*Happy, Sad, Chill, Motivated, Romantic, Party, Heartbreak, Peaceful, Energetic*).
- **🎸 Genre Filtering**: Filter songs by genre (*Bollywood, Pop, Romantic, Sad, Party, Punjabi, Indie, Classical, or All*).
- **🎤 Singer Selection**: Explore iconic hits from top Hindi music artists (*Arijit Singh, Shreya Ghoshal, Jubin Nautiyal, Atif Aslam, Neha Kakkar, Diljit Dosanjh, Badshah, and more*).
- **🎧 Spotify-Style Dark UI**: High-contrast dark theme UI with sleek cards, badges, and responsive layouts.
- **▶️ Direct Listen Links**: One-click links to play recommended tracks on YouTube.
- **⭐ Interactive Song Rating System**: Rate recommended songs from 1 to 5 stars stored in session state.
- **📜 Recommendation History**: Keep track of your session recommendations in a dedicated sidebar log.
- **📊 Real-time Statistics Dashboard**: Track session statistics including total recommendations, average rating, top mood, top artist, and dynamic bar charts.

---

## 📸 Application Preview

*(Add your application screenshots here)*

```text
+-----------------------------------------------------------------------+
|  MoodTunes 🎵                                                         |
|  "Your mood. Your music."                                             |
|                                                                       |
|  [😊 Mood: Romantic ❤️]   [🎸 Genre: Bollywood]  [🎤 Singer: Arijit]  |
|                                                                       |
|  +-----------------------------------------------------------------+  |
|  | 🎵 Kesariya                                                     |  |
|  | 🎤 Artist: Arijit Singh                                         |  |
|  | 🎸 Genre: Romantic | 😊 Mood: Romantic | ⚡ Energy: High       |  |
|  | ▶️ Listen Now  |  ⭐ Rate: [⭐⭐⭐⭐⭐ (5/5)]                  |  |
|  +-----------------------------------------------------------------+  |
+-----------------------------------------------------------------------+
```

---

## 🛠️ Tech Stack

- **Frontend / Framework**: [Streamlit](https://streamlit.io/)
- **Data Handling**: [Pandas](https://pandas.pydata.org/)
- **Visualizations**: [Altair](https://altair-viz.github.io/)
- **Data Format**: CSV (`songs.csv`)
- **Language**: Python 3.9+

---

## 📁 Project Structure

```text
MoodTunes/
│
├── app.py              # Main Streamlit application & UI logic
├── songs.csv           # Dataset containing 110+ Hindi songs
├── requirements.txt    # Required Python packages
├── README.md           # Documentation & beginner guide
├── .gitignore          # Git ignore configuration
└── assets/             # Directory for screenshots and images
```

---

## 🚀 Quick Start Guide

### Prerequisites
Make sure you have **Python 3.9+** installed on your system.

### 1. Clone or Download the Repository
```bash
git clone https://github.com/your-username/MoodTunes.git
cd MoodTunes
```

### 2. (Optional) Create a Virtual Environment
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Launch the Web Application
```bash
streamlit run app.py
```

The app will open automatically in your default web browser at `http://localhost:8501`.

---

## 🧠 How the Recommendation Engine Works

1. **User Filtering**: When you pick a Mood, Genre, and Singer, the dataset (`songs.csv`) is queried using Pandas conditional matching.
2. **Flexible Rules**:
   - Mood filter is strictly matched.
   - Selecting "All" or "All Singers" bypasses specific filters.
3. **Randomized Sampling**: Between **3 and 5 matching songs** are randomly sampled to prevent repetitive recommendations.
4. **Session Management**: All recommendations, custom ratings, and history log persist throughout your session in `st.session_state`.

---

## 🚀 Future Roadmap & Enhancements

- 🎵 **Official Spotify API Integration**: Fetch live preview audio snippets and user playlists.
- 📺 **Embedded YouTube Player**: Play video tracks directly inside the application.
- 🤖 **AI-Based Mood Detection**: Analyze facial expressions via webcam or user prompt text sentiment to detect mood automatically.
- 👤 **User Accounts & Database Integration**: Save history and favorite playlists permanently using SQLite / Firebase.
- 🔮 **Machine Learning Recommender**: Implement Collaborative Filtering and Content-Based ML models.

---

## 👨‍💻 Author

Created with ❤️ for Hindi music lovers!

Feel free to star ⭐ this repository if you enjoyed MoodTunes!
