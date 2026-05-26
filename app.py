import streamlit as st
import pickle
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

st.set_page_config(
    page_title="CineMatch",
    page_icon="🎬",
    layout="wide"
)

# ── GLOBAL STYLES ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #0a0a0f;
    color: #e8e4dc;
}

/* Hide default streamlit elements */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem !important; max-width: 1400px !important; }

/* ── HERO TITLE ── */
.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: clamp(2.5rem, 6vw, 5rem);
    font-weight: 900;
    line-height: 1;
    color: #e8e4dc;
    letter-spacing: -0.02em;
    margin-bottom: 0;
}
.hero-accent {
    color: #c8a96e;
}
.hero-sub {
    font-size: 1rem;
    color: #7a7770;
    font-weight: 300;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-top: 0.75rem;
}

/* ── DIVIDER ── */
.gold-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, #c8a96e55, transparent);
    margin: 2rem 0;
    border: none;
}

/* ── SECTION LABEL ── */
.section-label {
    font-size: 0.7rem;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: #c8a96e;
    font-weight: 500;
    margin-bottom: 1.25rem;
}

/* ── TRENDING CARD ── */
.trend-card {
    position: relative;
    border-radius: 8px;
    overflow: hidden;
    border: 1px solid #1e1e28;
    transition: transform 0.3s ease, border-color 0.3s ease;
    background: #111118;
}
.trend-card:hover {
    transform: translateY(-4px);
    border-color: #c8a96e55;
}
.trend-number {
    position: absolute;
    top: 8px;
    left: 8px;
    font-family: 'Playfair Display', serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: #c8a96e;
    background: #0a0a0fcc;
    padding: 2px 8px;
    border-radius: 4px;
    backdrop-filter: blur(4px);
    line-height: 1.4;
}
.trend-title {
    font-size: 0.78rem;
    font-weight: 500;
    text-align: center;
    padding: 0.5rem 0.4rem;
    color: #c8c4bc;
    line-height: 1.3;
}

/* ── SEARCH AREA ── */
.search-box-label {
    font-size: 0.7rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #7a7770;
    margin-bottom: 0.5rem;
}
div[data-testid="stSelectbox"] > div > div {
    background: #111118 !important;
    border: 1px solid #2a2a38 !important;
    border-radius: 6px !important;
    color: #e8e4dc !important;
    font-family: 'DM Sans', sans-serif !important;
}
div[data-testid="stSelectbox"] > div > div:hover {
    border-color: #c8a96e55 !important;
}

/* ── BUTTONS ── */
div[data-testid="stButton"] > button {
    background: transparent !important;
    border: 1px solid #c8a96e !important;
    color: #c8a96e !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.78rem !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    padding: 0.55rem 1.6rem !important;
    border-radius: 4px !important;
    transition: all 0.25s ease !important;
}
div[data-testid="stButton"] > button:hover {
    background: #c8a96e18 !important;
    border-color: #c8a96e !important;
    color: #e8d4a0 !important;
}

/* ── MOVIE DETAIL PANEL ── */
.detail-panel {
    background: #111118;
    border: 1px solid #1e1e28;
    border-radius: 12px;
    padding: 2rem;
    margin-top: 1.5rem;
}
.detail-title {
    font-family: 'Playfair Display', serif;
    font-size: clamp(1.6rem, 3vw, 2.4rem);
    font-weight: 700;
    color: #e8e4dc;
    line-height: 1.1;
    margin-bottom: 0.4rem;
}
.tagline {
    font-size: 0.9rem;
    font-style: italic;
    color: #7a7770;
    margin-bottom: 1rem;
    border-left: 2px solid #c8a96e;
    padding-left: 0.75rem;
}
.meta-pill {
    display: inline-block;
    background: #1e1e28;
    border: 1px solid #2a2a38;
    border-radius: 20px;
    padding: 3px 12px;
    font-size: 0.72rem;
    color: #a09890;
    margin: 3px 4px 3px 0;
    letter-spacing: 0.05em;
}
.rating-big {
    font-family: 'Playfair Display', serif;
    font-size: 2.5rem;
    font-weight: 700;
    color: #c8a96e;
    line-height: 1;
}
.rating-label {
    font-size: 0.65rem;
    letter-spacing: 0.15em;
    color: #7a7770;
    text-transform: uppercase;
}
.stat-box {
    background: #0d0d14;
    border: 1px solid #1e1e28;
    border-radius: 8px;
    padding: 1rem;
    text-align: center;
}
.stat-val {
    font-family: 'Playfair Display', serif;
    font-size: 1.2rem;
    color: #e8e4dc;
    font-weight: 400;
}
.stat-key {
    font-size: 0.65rem;
    letter-spacing: 0.15em;
    color: #5a5a68;
    text-transform: uppercase;
    margin-top: 4px;
}

/* ── CAST CARD ── */
.cast-name {
    font-size: 0.75rem;
    font-weight: 500;
    color: #c8c4bc;
    text-align: center;
    margin-top: 5px;
}
.cast-char {
    font-size: 0.65rem;
    color: #5a5a68;
    text-align: center;
    font-style: italic;
}

/* ── REC CARD ── */
.rec-card {
    background: #111118;
    border: 1px solid #1e1e28;
    border-radius: 10px;
    overflow: hidden;
    transition: border-color 0.3s ease, transform 0.3s ease;
}
.rec-card:hover {
    border-color: #c8a96e55;
    transform: translateY(-3px);
}
.rec-title {
    font-size: 0.82rem;
    font-weight: 500;
    color: #c8c4bc;
    padding: 0.6rem 0.75rem 0.4rem;
    line-height: 1.3;
}

/* ── SIDEBAR ── */
section[data-testid="stSidebar"] {
    background: #0d0d14 !important;
    border-right: 1px solid #1e1e28 !important;
}
section[data-testid="stSidebar"] .block-container {
    padding: 1.5rem 1rem !important;
}

/* ── EXPANDER (trailer) ── */
div[data-testid="stExpander"] {
    background: #0d0d14 !important;
    border: 1px solid #1e1e28 !important;
    border-radius: 6px !important;
}
div[data-testid="stExpander"] summary {
    color: #7a7770 !important;
    font-size: 0.78rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
}

/* ── SPINNER ── */
div[data-testid="stSpinner"] { color: #c8a96e !important; }

/* ── OVERVIEW TEXT ── */
.overview-text {
    font-size: 0.92rem;
    line-height: 1.8;
    color: #a09890;
    font-weight: 300;
}
</style>
""", unsafe_allow_html=True)

# ── SESSION STATE ──────────────────────────────────────────────────────────────
for key, val in [("history", []), ("mode", None), ("selected_movie", None), ("random_movie", None)]:
    if key not in st.session_state:
        st.session_state[key] = val

TMDB_API_KEY = st.secrets["tmdb"]["api_key"]

# ── HELPERS ───────────────────────────────────────────────────────────────────
def _session():
    s = requests.Session()
    retry = Retry(total=5, backoff_factor=1, status_forcelist=(500, 502, 504))
    s.mount("https://", HTTPAdapter(max_retries=retry))
    return s

def fetch_poster(movie_id):
    try:
        r = _session().get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}")
        if r.status_code == 200:
            p = r.json().get("poster_path")
            if p:
                return f"https://image.tmdb.org/t/p/w500{p}"
    except: pass
    return None

def fetch_trailer(movie_id):
    try:
        r = _session().get(f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={TMDB_API_KEY}")
        if r.status_code == 200:
            for v in r.json().get("results", []):
                if v.get("type") == "Trailer" and v.get("site") == "YouTube":
                    return f"https://youtu.be/{v['key']}"
    except: pass
    return None

def get_movie_details(movie_id):
    try:
        r = _session().get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&append_to_response=credits,videos")
        if r.status_code == 200:
            d = r.json()
            directors = [c["name"] for c in d.get("credits", {}).get("crew", []) if c.get("job") == "Director"]
            cast = [{"name": a.get("name"), "character": a.get("character"),
                     "profile": f"https://image.tmdb.org/t/p/w500{a['profile_path']}" if a.get("profile_path") else None}
                    for a in d.get("credits", {}).get("cast", [])[:5]]
            return {
                "rating": d.get("vote_average"),
                "vote_count": d.get("vote_count"),
                "release_date": d.get("release_date"),
                "runtime": d.get("runtime"),
                "tagline": d.get("tagline"),
                "overview": d.get("overview"),
                "director": ", ".join(directors) if directors else "N/A",
                "cast": cast,
                "genres": ", ".join([g["name"] for g in d.get("genres", [])]) or "N/A",
                "budget": f"${d.get('budget', 0):,}" if d.get("budget", 0) > 0 else "N/A",
                "revenue": f"${d.get('revenue', 0):,}" if d.get("revenue", 0) > 0 else "N/A",
                "available_in": ", ".join([l["english_name"] for l in d.get("spoken_languages", [])]) or "N/A",
            }
    except: pass
    return None

def recommend(movie):
    idx = movies[movies["title"] == movie].index[0]
    distances = sorted(enumerate(similarity[idx]), reverse=True, key=lambda x: x[1])
    recs = []
    for i, _ in distances[1:8]:
        mid = movies.iloc[i].movie_id
        poster = fetch_poster(mid)
        if poster:
            recs.append({"title": movies.iloc[i].title, "poster": poster, "trailer": fetch_trailer(mid)})
        if len(recs) == 5:
            break
    return recs

def get_random_movie():
    row = movies.sample(1).iloc[0]
    return {"title": row["title"], "poster": fetch_poster(row["movie_id"]),
            "trailer": fetch_trailer(row["movie_id"]), "movie_id": row["movie_id"]}

def update_history(movie_id):
    if not st.session_state.history or st.session_state.history[-1] != movie_id:
        st.session_state.history.append(movie_id)
        if len(st.session_state.history) > 5:
            st.session_state.history.pop(0)

def get_trending_movies():
    try:
        r = _session().get(f"https://api.themoviedb.org/3/trending/movie/week?api_key={TMDB_API_KEY}")
        if r.status_code == 200:
            return [{"title": m.get("title"),
                     "poster": f"https://image.tmdb.org/t/p/w500{m['poster_path']}" if m.get("poster_path") else None,
                     "movie_id": m.get("id")}
                    for m in r.json().get("results", [])[:5]]
    except: pass
    return []

# ── LOAD DATA ─────────────────────────────────────────────────────────────────
movies = pickle.load(open("model_files/movie_list.pkl", "rb"))
similarity = pickle.load(open("model_files/similarity.pkl", "rb"))

# ── HERO ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="padding: 2.5rem 0 1rem;">
    <p class="hero-sub">— Your personal film curator</p>
    <h1 class="hero-title">Cine<span class="hero-accent">Match</span></h1>
    <p style="font-size:0.9rem; color:#5a5a68; margin-top:0.75rem; font-weight:300; max-width:480px;">
        Discover films that resonate. Powered by similarity — refined by taste.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="gold-divider">', unsafe_allow_html=True)

# ── TRENDING ──────────────────────────────────────────────────────────────────
st.markdown('<p class="section-label">▸ Trending this week</p>', unsafe_allow_html=True)

trending_movies = get_trending_movies()
t_cols = st.columns(5, gap="small")
for i, movie in enumerate(trending_movies):
    with t_cols[i]:
        if movie.get("poster"):
            st.markdown(f"""
            <div class="trend-card">
                <span class="trend-number">0{i+1}</span>
                <img src="{movie['poster']}" style="width:100%; display:block; border-radius:8px 8px 0 0;" />
                <div class="trend-title">{movie['title']}</div>
            </div>
            """, unsafe_allow_html=True)

st.markdown('<hr class="gold-divider">', unsafe_allow_html=True)

# ── SEARCH + SURPRISE ─────────────────────────────────────────────────────────
col_search, col_gap, col_surprise = st.columns([5, 1, 3])

with col_search:
    st.markdown('<p class="section-label">▸ Search by title</p>', unsafe_allow_html=True)
    selected_movie = st.selectbox(
        "Search",
        movies["title"].values,
        key="select_movie",
        label_visibility="collapsed"
    )
    c1, c2 = st.columns([2, 3])
    with c1:
        if st.button("Find & Recommend", key="show_details"):
            st.session_state.mode = "search"
            st.session_state.selected_movie = selected_movie
            st.balloons()

with col_surprise:
    st.markdown('<p class="section-label">▸ Let fate decide</p>', unsafe_allow_html=True)
    st.markdown("""
    <p style="font-size:0.85rem; color:#5a5a68; font-weight:300; margin-bottom:1rem; line-height:1.6;">
        Not sure what to watch?<br>Let the algorithm surprise you.
    </p>
    """, unsafe_allow_html=True)
    if st.button("✦ Surprise Me", key="surprise_me"):
        st.session_state.mode = "surprise"
        st.session_state.random_movie = get_random_movie()
        st.balloons()

st.markdown("<br>", unsafe_allow_html=True)

# ── DETAIL RENDERER ───────────────────────────────────────────────────────────
def render_movie(movie_title, movie_id):
    details = get_movie_details(movie_id)
    trailer_url = fetch_trailer(movie_id)
    poster = fetch_poster(movie_id)

    st.markdown('<hr class="gold-divider">', unsafe_allow_html=True)

    left, right = st.columns([1, 2.4], gap="large")

    with left:
        if poster:
            st.markdown(f"""
            <div style="border-radius:10px; overflow:hidden; border:1px solid #1e1e28;">
                <img src="{poster}" style="width:100%; display:block;" />
            </div>
            """, unsafe_allow_html=True)
        if trailer_url:
            st.markdown("<br>", unsafe_allow_html=True)
            with st.expander("▶  Watch Trailer"):
                st.video(trailer_url)

    with right:
        if details:
            tagline = details.get("tagline") or ""
            st.markdown(f'<h2 class="detail-title">{movie_title}</h2>', unsafe_allow_html=True)
            if tagline:
                st.markdown(f'<p class="tagline">{tagline}</p>', unsafe_allow_html=True)

            # Genre pills
            genres = details.get("genres", "")
            if genres and genres != "N/A":
                pills = "".join(f'<span class="meta-pill">{g.strip()}</span>' for g in genres.split(","))
                st.markdown(f'<div style="margin-bottom:1.25rem;">{pills}</div>', unsafe_allow_html=True)

            # Rating + quick stats
            r1, r2, r3, r4 = st.columns(4)
            with r1:
                rating = details.get("rating", "N/A")
                st.markdown(f"""
                <div class="stat-box">
                    <div class="rating-big">{rating}</div>
                    <div class="rating-label">/ 10 rating</div>
                </div>
                """, unsafe_allow_html=True)
            with r2:
                runtime = f"{details.get('runtime', '—')} min" if details.get("runtime") else "—"
                st.markdown(f'<div class="stat-box"><div class="stat-val">{runtime}</div><div class="stat-key">Runtime</div></div>', unsafe_allow_html=True)
            with r3:
                rd = details.get("release_date", "N/A")
                year = rd[:4] if rd and rd != "N/A" else "N/A"
                st.markdown(f'<div class="stat-box"><div class="stat-val">{year}</div><div class="stat-key">Released</div></div>', unsafe_allow_html=True)
            with r4:
                votes = f"{details.get('vote_count', 0):,}" if details.get("vote_count") else "N/A"
                st.markdown(f'<div class="stat-box"><div class="stat-val">{votes}</div><div class="stat-key">Votes</div></div>', unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # Overview
            st.markdown('<p class="section-label">Synopsis</p>', unsafe_allow_html=True)
            st.markdown(f'<p class="overview-text">{details.get("overview", "N/A")}</p>', unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # Crew + financials
            fa, fb, fc = st.columns(3)
            with fa:
                st.markdown(f'<div class="stat-box"><div class="stat-val" style="font-size:0.85rem;">{details.get("director","N/A")}</div><div class="stat-key">Director</div></div>', unsafe_allow_html=True)
            with fb:
                st.markdown(f'<div class="stat-box"><div class="stat-val" style="font-size:0.85rem;">{details.get("budget","N/A")}</div><div class="stat-key">Budget</div></div>', unsafe_allow_html=True)
            with fc:
                st.markdown(f'<div class="stat-box"><div class="stat-val" style="font-size:0.85rem;">{details.get("revenue","N/A")}</div><div class="stat-key">Box Office</div></div>', unsafe_allow_html=True)

            # Cast
            if details.get("cast"):
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown('<p class="section-label">Cast</p>', unsafe_allow_html=True)
                cast_cols = st.columns(len(details["cast"]))
                for ci, actor in enumerate(details["cast"]):
                    with cast_cols[ci]:
                        if actor.get("profile"):
                            st.markdown(f"""
                            <div style="border-radius:8px; overflow:hidden; border:1px solid #1e1e28;">
                                <img src="{actor['profile']}" style="width:100%; display:block;" />
                            </div>
                            """, unsafe_allow_html=True)
                        st.markdown(f'<div class="cast-name">{actor.get("name","")}</div>', unsafe_allow_html=True)
                        st.markdown(f'<div class="cast-char">{actor.get("character","")}</div>', unsafe_allow_html=True)
        else:
            st.error("Could not retrieve movie details. Please try another movie.")

    # Recommendations
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<hr class="gold-divider">', unsafe_allow_html=True)
    st.markdown('<p class="section-label">▸ You might also like</p>', unsafe_allow_html=True)

    with st.spinner("Curating recommendations..."):
        recs = recommend(movie_title)

    if recs:
        rec_cols = st.columns(len(recs), gap="small")
        for ri, rec in enumerate(recs):
            with rec_cols[ri]:
                st.markdown(f"""
                <div class="rec-card">
                    <img src="{rec['poster']}" style="width:100%; display:block; border-radius:10px 10px 0 0;" />
                    <div class="rec-title">{rec['title']}</div>
                </div>
                """, unsafe_allow_html=True)
                if rec.get("trailer"):
                    with st.expander("▶ Trailer"):
                        st.video(rec["trailer"])

# ── CONTENT ───────────────────────────────────────────────────────────────────
if st.session_state.mode == "search" and st.session_state.selected_movie:
    movie_title = st.session_state.selected_movie
    row = movies[movies["title"] == movie_title].iloc[0]
    movie_id = row.movie_id
    update_history(movie_id)
    render_movie(movie_title, movie_id)

elif st.session_state.mode == "surprise" and st.session_state.random_movie:
    data = st.session_state.random_movie
    movie_title = data["title"]
    movie_id = data.get("movie_id") or movies[movies["title"] == movie_title].iloc[0].movie_id
    update_history(movie_id)
    st.markdown(f"""
    <div style="display:inline-block; background:#1e1e10; border:1px solid #c8a96e44;
         border-radius:4px; padding:4px 14px; margin-bottom:0.5rem;">
        <span style="font-size:0.7rem; letter-spacing:0.15em; color:#c8a96e; text-transform:uppercase;">
            ✦ Tonight's pick
        </span>
    </div>
    """, unsafe_allow_html=True)
    render_movie(movie_title, movie_id)

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <p style="font-size:0.65rem; letter-spacing:0.2em; color:#c8a96e;
       text-transform:uppercase; margin-bottom:1.25rem; font-weight:500;">
        Recently Viewed
    </p>
    """, unsafe_allow_html=True)

    if st.session_state.history:
        for i, hist_id in enumerate(reversed(st.session_state.history)):
            row = movies[movies["movie_id"] == hist_id].iloc[0]
            hist_title = row["title"]
            hist_poster = fetch_poster(hist_id)
            with st.container():
                if hist_poster:
                    st.markdown(f"""
                    <div style="border-radius:6px; overflow:hidden; border:1px solid #1e1e28; margin-bottom:6px;">
                        <img src="{hist_poster}" style="width:100%; display:block;" />
                    </div>
                    """, unsafe_allow_html=True)
                if st.button(hist_title, key=f"hist_{hist_id}_{i}", use_container_width=True):
                    st.session_state.mode = "search"
                    st.session_state.selected_movie = hist_title
                    st.balloons()
                    st.rerun()
                st.markdown('<div style="height:8px;"></div>', unsafe_allow_html=True)
    else:
        st.markdown('<p style="font-size:0.8rem; color:#3a3a48;">No history yet</p>', unsafe_allow_html=True)

# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown('<hr class="gold-divider">', unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center; padding:0.5rem 0 1.5rem;">
    <span style="font-size:0.65rem; letter-spacing:0.2em; color:#3a3a48; text-transform:uppercase;">
        Made with ♥ by Atif Yousafzai &nbsp;·&nbsp; Powered by TMDB
    </span>
</div>
""", unsafe_allow_html=True)