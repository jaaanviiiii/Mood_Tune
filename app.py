import streamlit as st
import pandas as pd
import random
import altair as alt
import os
import html

# ==========================================
# 1. PAGE CONFIGURATION & METADATA
# ==========================================
st.set_page_config(
    page_title="MoodTunes — Mood-Based Hindi Song Recommender",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. CUSTOM SPOTIFY-STYLE DARK THEME CSS
# ==========================================
CUSTOM_CSS = """
<style>
    /* Dark Theme Colors & Base Reset */
    .stApp {
        background-color: #121212;
        color: #FFFFFF;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Main Header Styling */
    .main-title {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #1DB954 0%, #1ed760 50%, #ffffff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }
    
    .tagline {
        font-size: 1.25rem;
        font-weight: 500;
        color: #1DB954;
        margin-top: 0px;
        margin-bottom: 10px;
    }

    .app-description {
        color: #b3b3b3;
        font-size: 0.95rem;
        margin-bottom: 25px;
    }

    /* Spotify-style Elevated Card */
    .song-card {
        background: #181818;
        border: 1px solid #282828;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        transition: transform 0.2s ease, border-color 0.2s ease;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
    }
    
    .song-card:hover {
        border-color: #1DB954;
        transform: translateY(-2px);
    }

    .song-title {
        font-size: 1.35rem;
        font-weight: 700;
        color: #FFFFFF;
        margin-bottom: 6px;
    }

    .song-artist {
        font-size: 1.05rem;
        color: #1DB954;
        font-weight: 600;
        margin-bottom: 12px;
    }

    /* Badges */
    .badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-right: 6px;
        margin-bottom: 10px;
    }
    
    .badge-genre {
        background-color: #282828;
        color: #e0e0e0;
    }
    
    .badge-mood {
        background-color: #2e1f47;
        color: #d8b4fe;
    }
    
    .badge-energy {
        background-color: #4c1d24;
        color: #fca5a5;
    }

    /* Listen Now Button */
    .listen-btn {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        background-color: #1DB954;
        color: #000000 !important;
        font-weight: 700;
        padding: 8px 18px;
        border-radius: 25px;
        text-decoration: none;
        margin-top: 10px;
        transition: background-color 0.2s ease, transform 0.1s ease;
    }
    
    .listen-btn:hover {
        background-color: #1ed760;
        transform: scale(1.03);
    }

    /* Sidebar Customization */
    section[data-testid="stSidebar"] {
        background-color: #0b0b0b;
        border-right: 1px solid #1f1f1f;
    }

    /* Streamlit Button Styling */
    div.stButton > button {
        background: linear-gradient(135deg, #1DB954 0%, #1aa34a 100%);
        color: #000000;
        font-weight: 700;
        border: none;
        border-radius: 30px;
        padding: 10px 24px;
        font-size: 1rem;
        transition: all 0.2s ease;
    }
    
    div.stButton > button:hover {
        background: linear-gradient(135deg, #1ed760 0%, #1DB954 100%);
        box-shadow: 0 4px 15px rgba(29, 185, 84, 0.4);
        transform: translateY(-1px);
        color: #000000;
    }

    /* Metric Cards */
    div[data-testid="stMetric"] {
        background-color: #181818;
        border: 1px solid #282828;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ==========================================
# 3. DATA LOADING & INITIALIZATION
# ==========================================
@st.cache_data
def load_song_dataset():
    """Load and return the songs dataset from CSV."""
    csv_path = "songs.csv"
    if os.path.exists(csv_path):
        try:
            df = pd.read_csv(csv_path)
            # Strip extra whitespaces from string columns
            for col in df.select_dtypes(include=["object", "string"]).columns:
                df[col] = df[col].astype(str).str.strip()
            return df
        except Exception as e:
            st.error(f"Error reading songs.csv: {e}")
            return pd.DataFrame()
    else:
        st.error("songs.csv file not found in directory.")
        return pd.DataFrame()

df_songs = load_song_dataset()

# Initialize Session State Variables
if "history" not in st.session_state:
    st.session_state["history"] = []  # Stores list of dicts: {title, artist, mood, rating}

if "current_recommendations" not in st.session_state:
    st.session_state["current_recommendations"] = []

if "ratings" not in st.session_state:
    st.session_state["ratings"] = {}  # Stores song title -> star rating (1-5)


# ==========================================
# 4. HOME PAGE HEADER
# ==========================================
st.markdown('<div class="main-title">MoodTunes 🎵</div>', unsafe_allow_html=True)
st.markdown('<div class="tagline">"Your mood. Your music."</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="app-description">'
    "Discover popular Hindi songs tailored specifically to how you feel right now. "
    "Select your mood, genre, and favorite singer to get instant personalized recommendations!"
    '</div>',
    unsafe_allow_html=True
)
st.markdown("---")

# ==========================================
# 5. INPUT SELECTION CONTROLS
# ==========================================
st.subheader("🎯 Personalize Your Vibe")

# Mood dictionary mapping Display Name (with Emoji) to raw Dataset Mood string
MOOD_OPTIONS = {
    "Happy 😊": "Happy",
    "Sad 😢": "Sad",
    "Chill 😌": "Chill",
    "Motivated 💪": "Motivated",
    "Romantic ❤️": "Romantic",
    "Party 🥳": "Party",
    "Heartbreak 💔": "Heartbreak",
    "Peaceful 🌙": "Peaceful",
    "Energetic 🔥": "Energetic"
}

if not df_songs.empty and "genre" in df_songs.columns:
    unique_genres = sorted(list(df_songs["genre"].dropna().unique()))
    GENRE_OPTIONS = ["All"] + [g for g in unique_genres if g.lower() != "all"]
else:
    GENRE_OPTIONS = [
        "All", "Bollywood", "Pop", "Romantic", "Sad", "Party", "Punjabi", "Indie", "Classical"
    ]

if not df_songs.empty and "artist" in df_songs.columns:
    artist_set = set()
    for item in df_songs["artist"].dropna():
        for sub_a in str(item).split(","):
            if sub_a.strip():
                artist_set.add(sub_a.strip())
    SINGER_OPTIONS = ["All Singers"] + sorted(list(artist_set))
else:
    SINGER_OPTIONS = [
        "All Singers", "Arijit Singh", "Shreya Ghoshal", "Jubin Nautiyal", "Armaan Malik",
        "Vishal Mishra", "Sonu Nigam", "KK", "Atif Aslam", "Mohit Chauhan", "Neha Kakkar",
        "Darshan Raval", "Amit Trivedi", "Pritam", "A.R. Rahman", "Sunidhi Chauhan",
        "Palak Muchhal", "Tulsi Kumar", "B Praak", "Sachet Tandon", "Parampara Tandon",
        "Vishal Dadlani", "Shekhar Ravjiani", "Badshah", "Diljit Dosanjh"
    ]

def sample_artist_diverse_songs(df_subset, target_count=6):
    """Sample up to target_count songs prioritizing unique artists for maximum diversity."""
    if df_subset.empty:
        return []
    
    unique_artists = list(df_subset["artist"].unique())
    random.shuffle(unique_artists)
    
    selected_indices = []
    # Pick 1 song per artist first
    for artist in unique_artists:
        if len(selected_indices) >= target_count:
            break
        artist_songs = df_subset[df_subset["artist"] == artist]
        chosen_idx = random.choice(artist_songs.index.tolist())
        selected_indices.append(chosen_idx)
        
    # Fill remaining slots if target_count not reached
    if len(selected_indices) < target_count:
        remaining_indices = list(set(df_subset.index) - set(selected_indices))
        fill_count = min(len(remaining_indices), target_count - len(selected_indices))
        if fill_count > 0:
            selected_indices.extend(random.sample(remaining_indices, fill_count))
            
    result_df = df_subset.loc[selected_indices].sample(frac=1.0)
    return result_df.to_dict(orient="records")

col1, col2, col3 = st.columns(3)

with col1:
    selected_mood_label = st.selectbox(
        "😊 Choose your Mood",
        options=list(MOOD_OPTIONS.keys()),
        index=0
    )
    selected_mood_raw = MOOD_OPTIONS[selected_mood_label]

with col2:
    selected_genre = st.selectbox(
        "🎸 Choose Genre",
        options=GENRE_OPTIONS,
        index=0
    )

with col3:
    selected_singer = st.selectbox(
        "🎤 Choose Singer / Artist",
        options=SINGER_OPTIONS,
        index=0
    )

num_songs_to_rec = st.slider("🎶 Number of Songs to Recommend", min_value=3, max_value=10, value=6, step=1)

st.write("") # Spacing

# Recommendation Trigger Button
if st.button("✨ Recommend Songs", use_container_width=True):
    if df_songs.empty:
        st.error("Dataset is empty or could not be loaded.")
    else:
        # Filter Logic
        filtered_df = df_songs.copy()
        
        # 1. Filter by Mood
        filtered_df = filtered_df[filtered_df["mood"].str.strip().str.lower() == selected_mood_raw.lower()]
        
        # 2. Filter by Genre (if not "All")
        if selected_genre != "All":
            filtered_df = filtered_df[filtered_df["genre"].str.strip().str.lower() == selected_genre.lower()]
            
        # 3. Filter by Singer (if not "All Singers")
        if selected_singer != "All Singers":
            filtered_df = filtered_df[filtered_df["artist"].str.contains(selected_singer, case=False, na=False)]

        if filtered_df.empty:
            st.session_state["current_recommendations"] = []
            st.warning("⚠️ No songs found for this combination. Try another mood or genre!")
        else:
            # Pick artist-diverse sample up to num_songs_to_rec
            recommendations = sample_artist_diverse_songs(filtered_df, target_count=num_songs_to_rec)
            st.session_state["current_recommendations"] = recommendations

            # Log into recommendation history avoiding duplicates
            for rec in recommendations:
                title = rec["title"]
                hist_entry = {
                    "title": title,
                    "artist": rec["artist"],
                    "mood": rec["mood"],
                    "rating": st.session_state["ratings"].get(title, 0)
                }
                # Check if exact title already in history
                existing_match = next((h for h in st.session_state["history"] if h["title"] == title), None)
                if not existing_match:
                    st.session_state["history"].append(hist_entry)
                else:
                    # Update rating in history if rating exists
                    existing_match["rating"] = st.session_state["ratings"].get(title, existing_match["rating"])

st.write("")

# Callback function for updating rating in session state and history
def update_song_rating(song_title, select_key):
    val = st.session_state.get(select_key, 0)
    st.session_state["ratings"][song_title] = val
    for h in st.session_state["history"]:
        if h["title"] == song_title:
            h["rating"] = val
    if val > 0:
        st.toast(f"Saved {val}⭐ rating for '{song_title}'!")

# ==========================================
# 6. RECOMMENDATION DISPLAY & RATING
# ==========================================
if st.session_state["current_recommendations"]:
    st.subheader("🎧 Recommended For You")
    
    for idx, song in enumerate(st.session_state["current_recommendations"]):
        title = song.get("title", "Unknown Title")
        artist = song.get("artist", "Unknown Artist")
        genre = song.get("genre", "Bollywood")
        mood = song.get("mood", "Happy")
        energy = song.get("energy", "Medium")
        link = song.get("link", "#")

        # HTML Escaped Card UI
        safe_title = html.escape(str(title))
        safe_artist = html.escape(str(artist))
        safe_genre = html.escape(str(genre))
        safe_mood = html.escape(str(mood))
        safe_energy = html.escape(str(energy))
        safe_link = html.escape(str(link))

        card_html = f"""
        <div class="song-card">
            <div class="song-title">🎵 {safe_title}</div>
            <div class="song-artist">🎤 {safe_artist}</div>
            <div>
                <span class="badge badge-genre">🎸 {safe_genre}</span>
                <span class="badge badge-mood">😊 Mood: {safe_mood}</span>
                <span class="badge badge-energy">⚡ Energy: {safe_energy}</span>
            </div>
            <a href="{safe_link}" target="_blank" class="listen-btn">▶️ Listen Now</a>
        </div>
        """
        
        col_card, col_rate = st.columns([3, 1])
        with col_card:
            st.markdown(card_html, unsafe_allow_html=True)
            
        with col_rate:
            st.markdown("**⭐ Rate this song:**")
            current_rating = st.session_state["ratings"].get(title, 0)
            select_key = f"rating_select_{title}"
            
            # Sync key state with stored rating if not set
            if select_key not in st.session_state:
                st.session_state[select_key] = current_rating
            else:
                st.session_state[select_key] = st.session_state["ratings"].get(title, st.session_state[select_key])

            st.selectbox(
                label=f"Rating for {title}",
                options=[0, 1, 2, 3, 4, 5],
                format_func=lambda x: "Select Rating" if x == 0 else f"{'⭐' * x} ({x}/5)",
                key=select_key,
                on_change=update_song_rating,
                args=(title, select_key),
                label_visibility="collapsed"
            )

st.write("")
st.markdown("---")

# ==========================================
# 7. STATISTICS DASHBOARD & CHARTS
# ==========================================
st.subheader("📊 Session Statistics Dashboard")

history = st.session_state["history"]

if not history:
    st.info("Get some recommendations to see your statistics! 🎵")
else:
    hist_df = pd.DataFrame(history)
    
    # Calculate metrics
    total_recs = len(hist_df)
    
    # Filter rated songs to compute real average rating
    rated_songs = [h["rating"] for h in history if h.get("rating", 0) > 0]
    avg_rating = round(sum(rated_songs) / len(rated_songs), 1) if rated_songs else "N/A"
    
    mood_modes = hist_df["mood"].mode() if "mood" in hist_df.columns else pd.Series()
    most_selected_mood = mood_modes.iloc[0] if not mood_modes.empty else "N/A"
    
    artist_modes = hist_df["artist"].mode() if "artist" in hist_df.columns else pd.Series()
    most_rec_artist = artist_modes.iloc[0] if not artist_modes.empty else "N/A"
    
    # Display Metric Cards
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Recommendations", total_recs)
    m2.metric("Average Rating", f"{avg_rating} ⭐" if avg_rating != "N/A" else "Not rated yet")
    m3.metric("Most Recommended Mood", most_selected_mood)
    m4.metric("Top Recommended Artist", most_rec_artist)
    
    st.write("")
    
    # Dynamic Charts
    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown("### 📊 Mood Distribution")
        mood_counts = hist_df["mood"].value_counts().reset_index()
        mood_counts.columns = ["Mood", "Count"]
        
        mood_chart = (
            alt.Chart(mood_counts)
            .mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6, color="#1DB954")
            .encode(
                x=alt.X("Mood:N", sort=alt.EncodingSortField(field="Count", order="descending"), title="Mood"),
                y=alt.Y("Count:Q", title="Recommendations"),
                tooltip=["Mood", "Count"]
            )
            .properties(height=300)
        )
        st.altair_chart(mood_chart, use_container_width=True)

    with c2:
        st.markdown("### 🎤 Top Recommended Artists")
        artist_counts = hist_df["artist"].value_counts().reset_index().head(5)
        artist_counts.columns = ["Artist", "Count"]
        
        artist_chart = (
            alt.Chart(artist_counts)
            .mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6, color="#1ed760")
            .encode(
                x=alt.X("Count:Q", title="Recommendations"),
                y=alt.Y("Artist:N", sort=alt.EncodingSortField(field="Count", order="descending"), title="Artist"),
                tooltip=["Artist", "Count"]
            )
            .properties(height=300)
        )
        st.altair_chart(artist_chart, use_container_width=True)


# ==========================================
# 8. SIDEBAR - RECOMMENDATION HISTORY
# ==========================================
with st.sidebar:
    st.title("📜 Recommendation History")
    st.caption("Track your session music recommendations")
    
    if st.button("🗑️ Clear History", use_container_width=True):
        st.session_state["history"] = []
        st.session_state["current_recommendations"] = []
        st.session_state["ratings"] = {}
        keys_to_del = [k for k in st.session_state.keys() if k.startswith("rating_select_")]
        for k in keys_to_del:
            del st.session_state[k]
        st.rerun()
        
    st.write("")
    
    if not st.session_state["history"]:
        st.write("No history yet. Start exploring songs!")
    else:
        # Display history items in reverse chronological order
        for idx, item in enumerate(reversed(st.session_state["history"])):
            song_title = html.escape(str(item.get("title", "Unknown")))
            artist_name = html.escape(str(item.get("artist", "Unknown")))
            song_mood = html.escape(str(item.get("mood", "")))
            rating_val = item.get("rating", 0)
            
            rating_str = f"⭐ {rating_val}/5" if rating_val > 0 else "Unrated"
            
            st.markdown(
                f"""
                <div style="background:#181818; padding:10px; border-radius:8px; border-left:4px solid #1DB954; margin-bottom:8px;">
                    <div style="font-weight:bold; color:#fff; font-size:0.9rem;">{song_title}</div>
                    <div style="color:#1DB954; font-size:0.8rem;">{artist_name}</div>
                    <div style="color:#aaa; font-size:0.75rem;">Mood: {song_mood} | {rating_str}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
