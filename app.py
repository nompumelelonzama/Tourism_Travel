<<<<<<< HEAD

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import sqlite3
import hashlib
import requests
import base64
from datetime import datetime, timedelta
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from wordcloud import WordCloud
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from textblob import TextBlob
from PIL import Image
from fpdf import FPDF
import folium
from streamlit_folium import st_folium
from plotly.subplots import make_subplots
import tempfile
import os
import io
import json

# ======================================================
# PAGE CONFIG
# ======================================================

st.set_page_config(
    page_title="Smart Tourism-travel ZA",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ======================================================
# API KEYS — Replace with your actual keys
# ======================================================

OPENWEATHER_API_KEY = os.environ.get("OPENWEATHER_API_KEY", "YOUR_OPENWEATHER_KEY")
GOOGLE_MAPS_API_KEY = os.environ.get("GOOGLE_MAPS_API_KEY", "YOUR_GOOGLE_MAPS_KEY")
GOOGLE_VISION_API_KEY = os.environ.get("GOOGLE_VISION_API_KEY", "YOUR_GOOGLE_VISION_KEY")
GOOGLE_PLACES_API_KEY = os.environ.get("GOOGLE_PLACES_API_KEY", "YOUR_GOOGLE_PLACES_KEY")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "YOUR_OPENAI_KEY")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "YOUR_ANTHROPIC_KEY")
# ======================================================
# PROFESSIONAL UI STYLING
# ======================================================

def apply_styles():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

    .stApp {
        background: linear-gradient(135deg, #0a0f1e 0%, #0f172a 50%, #1a0a2e 100%);
        color: white;
        font-family: 'DM Sans', sans-serif;
    }
    h1, h2, h3, h4 {
        font-family: 'Syne', sans-serif !important;
        color: white !important;
        letter-spacing: -0.02em;
    }
    .hero {
        background: linear-gradient(135deg, rgba(255,110,64,0.12), rgba(56,189,248,0.08));
        backdrop-filter: blur(20px);
        padding: 40px;
        border-radius: 24px;
        text-align: center;
        border: 1px solid rgba(255,110,64,0.2);
        box-shadow: 0 0 60px rgba(255,110,64,0.08), 0 8px 32px rgba(0,0,0,0.4);
        margin-bottom: 28px;
    }
    .metric-card {
        background: rgba(255,255,255,0.04);
        backdrop-filter: blur(16px);
        border-radius: 20px;
        padding: 22px;
        margin-bottom: 16px;
        border: 1px solid rgba(255,255,255,0.08);
        transition: all 0.3s cubic-bezier(0.4,0,0.2,1);
        box-shadow: 0 4px 24px rgba(0,0,0,0.3);
    }
    .metric-card:hover {
        transform: translateY(-4px);
        border-color: rgba(255,110,64,0.3);
        box-shadow: 0 12px 32px rgba(255,110,64,0.15);
    }
    .weather-card {
        background: linear-gradient(135deg, rgba(56,189,248,0.15), rgba(14,165,233,0.08));
        border: 1px solid rgba(56,189,248,0.3);
        border-radius: 20px;
        padding: 24px;
        margin: 12px 0;
        text-align: center;
    }
    .forecast-card {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(56,189,248,0.2);
        border-radius: 14px;
        padding: 14px;
        text-align: center;
        margin: 6px 0;
    }
    .chat-bubble-user {
        background: linear-gradient(135deg, #ff6e40, #ff3d00);
        border-radius: 18px 18px 4px 18px;
        padding: 12px 18px;
        margin: 8px 0 8px 40px;
        color: white;
        font-size: 0.95rem;
    }
    .chat-bubble-bot {
        background: rgba(56,189,248,0.12);
        border: 1px solid rgba(56,189,248,0.25);
        border-radius: 18px 18px 18px 4px;
        padding: 12px 18px;
        margin: 8px 40px 8px 0;
        color: white;
        font-size: 0.95rem;
    }
    .landmark-card {
        background: linear-gradient(135deg, rgba(167,139,250,0.12), rgba(139,92,246,0.06));
        border: 1px solid rgba(167,139,250,0.3);
        border-radius: 20px;
        padding: 24px;
        margin: 12px 0;
    }
    .hotel-image-card {
        border-radius: 16px;
        overflow: hidden;
        margin-bottom: 12px;
        border: 1px solid rgba(255,255,255,0.08);
    }
    .rank-gold {
        background: linear-gradient(135deg, rgba(251,191,36,0.15), rgba(245,158,11,0.08));
        border: 1px solid rgba(251,191,36,0.3);
        border-radius: 16px;
        padding: 16px 20px;
        margin: 8px 0;
    }
    .rank-silver {
        background: linear-gradient(135deg, rgba(148,163,184,0.12), rgba(100,116,139,0.06));
        border: 1px solid rgba(148,163,184,0.25);
        border-radius: 16px;
        padding: 16px 20px;
        margin: 8px 0;
    }
    .rank-danger {
        background: linear-gradient(135deg, rgba(239,68,68,0.12), rgba(185,28,28,0.06));
        border: 1px solid rgba(239,68,68,0.25);
        border-radius: 16px;
        padding: 16px 20px;
        margin: 8px 0;
    }
    .flag-card {
        background: rgba(239,68,68,0.1);
        border: 1px solid rgba(239,68,68,0.3);
        border-radius: 12px;
        padding: 12px 16px;
        margin: 6px 0;
    }
    .role-badge-tourist {
        background: linear-gradient(135deg, #34d399, #059669);
        padding: 4px 14px; border-radius: 20px; font-size: 0.8rem; font-weight: 600;
    }
    .role-badge-manager {
        background: linear-gradient(135deg, #38bdf8, #0284c7);
        padding: 4px 14px; border-radius: 20px; font-size: 0.8rem; font-weight: 600;
    }
    .role-badge-admin {
        background: linear-gradient(135deg, #f59e0b, #d97706);
        padding: 4px 14px; border-radius: 20px; font-size: 0.8rem; font-weight: 600;
    }
    .stButton>button {
        background: linear-gradient(135deg, #ff6e40, #ff3d00);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 10px 24px;
        font-weight: 600;
        font-family: 'DM Sans', sans-serif;
        letter-spacing: 0.02em;
        transition: all 0.2s;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255,110,64,0.4);
    }
    section[data-testid="stSidebar"] {
        background: rgba(10,15,30,0.8);
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255,255,255,0.06);
    }
    .stTabs [data-baseweb="tab"] {
        font-family: 'DM Sans', sans-serif;
        font-weight: 500;
    }
    .access-denied {
        background: rgba(239,68,68,0.1);
        border: 1px solid rgba(239,68,68,0.3);
        border-radius: 16px;
        padding: 32px;
        text-align: center;
        margin: 40px auto;
    }
    </style>
    """, unsafe_allow_html=True)

# ======================================================
# DATABASE — Extended schema with users table
# ======================================================

def init_db():
    conn = sqlite3.connect("tourism_ai.db")
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL,
            email TEXT,
            full_name TEXT,
            created_at TEXT,
            last_login TEXT,
            is_active INTEGER DEFAULT 1
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT,
            hotel TEXT,
            city TEXT,
            cost REAL,
            booking_date TEXT,
            lead_time INTEGER,
            prev_cancels INTEGER,
            satisfaction INTEGER,
            status TEXT DEFAULT 'Active',
            refunded INTEGER DEFAULT 0,
            flagged INTEGER DEFAULT 0,
            flag_reason TEXT DEFAULT ''
        )
    ''')

    for col, definition in [
        ("status", "TEXT DEFAULT 'Active'"),
        ("refunded", "INTEGER DEFAULT 0"),
        ("flagged", "INTEGER DEFAULT 0"),
        ("flag_reason", "TEXT DEFAULT ''"),
    ]:
        try:
            c.execute(f"ALTER TABLE bookings ADD COLUMN {col} {definition}")
        except Exception:
            pass

    c.execute("SELECT COUNT(*) FROM users")
    if c.fetchone()[0] == 0:
        default_users = [
            ("tourist1",  hash_password("tourist123"),  "Tourist",       "tourist@example.com",  "John Traveller"),
            ("manager1",  hash_password("manager123"),  "Hotel Manager", "manager@example.com",  "Sarah Manager"),
            ("admin1",    hash_password("admin123"),    "Admin",         "admin@example.com",    "System Admin"),
            ("tourist2",  hash_password("password"),    "Tourist",       "t2@example.com",       "Jane Explorer"),
        ]
        for u in default_users:
            c.execute("INSERT INTO users (username,password_hash,role,email,full_name,created_at) VALUES (?,?,?,?,?,?)",
                      (*u, str(datetime.now())))

    conn.commit()
    conn.close()

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate_user(username: str, password: str):
    conn = sqlite3.connect("tourism_ai.db")
    c = conn.cursor()
    c.execute("SELECT id, username, role, full_name, is_active FROM users WHERE username=? AND password_hash=?",
              (username, hash_password(password)))
    user = c.fetchone()
    if user and user[4] == 1:
        c.execute("UPDATE users SET last_login=? WHERE username=?", (str(datetime.now()), username))
        conn.commit()
    conn.close()
    return user

def create_user(username, password, role, email, full_name):
    conn = sqlite3.connect("tourism_ai.db")
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username,password_hash,role,email,full_name,created_at) VALUES (?,?,?,?,?,?)",
                  (username, hash_password(password), role, email, full_name, str(datetime.now())))
        conn.commit()
        return True, "User created successfully"
    except sqlite3.IntegrityError:
        return False, "Username already exists"
    finally:
        conn.close()

def get_all_users():
    conn = sqlite3.connect("tourism_ai.db")
    df = pd.read_sql("SELECT id,username,role,email,full_name,created_at,last_login,is_active FROM users", conn)
    conn.close()
    return df

def toggle_user_status(user_id, is_active):
    conn = sqlite3.connect("tourism_ai.db")
    c = conn.cursor()
    c.execute("UPDATE users SET is_active=? WHERE id=?", (is_active, user_id))
    conn.commit()
    conn.close()

# ======================================================
# SAVE / ADMIN BOOKING OPERATIONS
# ======================================================

def save_booking(user, hotel, city, cost):
    conn = sqlite3.connect("tourism_ai.db")
    c = conn.cursor()
    c.execute(
        "INSERT INTO bookings (user,hotel,city,cost,booking_date,lead_time,prev_cancels,satisfaction,status,refunded,flagged,flag_reason) VALUES (?,?,?,?,?,?,?,?,'Active',0,0,'')",
        (user, hotel, city, cost, str(datetime.now()),
         np.random.randint(1, 60), np.random.randint(0, 3), np.random.randint(1, 6))
    )
    conn.commit()
    conn.close()

def cancel_booking(bid):
    _exec_booking_update("UPDATE bookings SET status='Cancelled' WHERE id=?", (bid,))

def refund_booking(bid):
    _exec_booking_update("UPDATE bookings SET status='Refunded',refunded=1 WHERE id=?", (bid,))

def reassign_booking(bid, new_hotel, new_city, new_cost):
    _exec_booking_update("UPDATE bookings SET hotel=?,city=?,cost=? WHERE id=?", (new_hotel, new_city, new_cost, bid))

def edit_booking(bid, user, hotel, city, cost):
    _exec_booking_update("UPDATE bookings SET user=?,hotel=?,city=?,cost=? WHERE id=?", (user, hotel, city, cost, bid))

def flag_booking(bid, reason):
    _exec_booking_update("UPDATE bookings SET flagged=1,flag_reason=? WHERE id=?", (reason, bid))

def unflag_booking(bid):
    _exec_booking_update("UPDATE bookings SET flagged=0,flag_reason='' WHERE id=?", (bid,))

def _exec_booking_update(sql, params):
    conn = sqlite3.connect("tourism_ai.db")
    conn.execute(sql, params)
    conn.commit()
    conn.close()

# ======================================================
# FEATURE 1 — REAL-TIME WEATHER API
# ======================================================

def get_live_weather(city: str, country_code: str = "ZA"):
    if OPENWEATHER_API_KEY == "YOUR_OPENWEATHER_KEY":
        mock = {
            "Cape Town":    {"temp": 22, "feels_like": 21, "humidity": 65, "wind_speed": 14, "condition": "Partly Cloudy", "icon": "02d", "pressure": 1015, "visibility": 10},
            "Johannesburg": {"temp": 26, "feels_like": 25, "humidity": 45, "wind_speed": 18, "condition": "Clear Sky",    "icon": "01d", "pressure": 1012, "visibility": 10},
            "Durban":       {"temp": 28, "feels_like": 30, "humidity": 78, "wind_speed": 12, "condition": "Humid",         "icon": "03d", "pressure": 1010, "visibility": 8 },
            "Kruger Park":  {"temp": 31, "feels_like": 34, "humidity": 40, "wind_speed": 8,  "condition": "Hot & Sunny",  "icon": "01d", "pressure": 1008, "visibility": 10},
            "Stellenbosch": {"temp": 20, "feels_like": 19, "humidity": 60, "wind_speed": 10, "condition": "Sunny",        "icon": "01d", "pressure": 1016, "visibility": 10},
            "Pretoria":     {"temp": 27, "feels_like": 26, "humidity": 50, "wind_speed": 15, "condition": "Clear",        "icon": "01d", "pressure": 1011, "visibility": 10},
            "Port Elizabeth":{"temp": 19,"feels_like": 18, "humidity": 70, "wind_speed": 20, "condition": "Windy",        "icon": "04d", "pressure": 1013, "visibility": 9 },
            "Knysna":       {"temp": 21, "feels_like": 20, "humidity": 68, "wind_speed": 11, "condition": "Partly Cloudy","icon": "02d", "pressure": 1014, "visibility": 10},
        }
        return mock.get(city, {"temp": 24, "feels_like": 23, "humidity": 55, "wind_speed": 12, "condition": "Clear", "icon": "01d", "pressure": 1013, "visibility": 10})

    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city},{country_code}&appid={OPENWEATHER_API_KEY}&units=metric"
        r = requests.get(url, timeout=8)
        data = r.json()
        if r.status_code == 200:
            return {
                "temp":       round(data["main"]["temp"]),
                "feels_like": round(data["main"]["feels_like"]),
                "humidity":   data["main"]["humidity"],
                "wind_speed": round(data["wind"]["speed"] * 3.6, 1),
                "condition":  data["weather"][0]["description"].title(),
                "icon":       data["weather"][0]["icon"],
                "pressure":   data["main"]["pressure"],
                "visibility": round(data.get("visibility", 10000) / 1000, 1),
            }
    except Exception as e:
        st.error(f"Weather API error: {e}")
    return None

def get_weather_forecast(city: str, country_code: str = "ZA"):
    if OPENWEATHER_API_KEY == "YOUR_OPENWEATHER_KEY":
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        icons = ["01d", "02d", "03d", "01d", "04d"]
        temps = [24, 26, 22, 28, 23]
        descs = ["Sunny", "Partly Cloudy", "Cloudy", "Clear", "Overcast"]
        return [{"day": d, "temp": t, "icon": i, "desc": desc, "humidity": np.random.randint(40, 80)}
                for d, t, i, desc in zip(days, temps, icons, descs)]
    try:
        url = f"https://api.openweathermap.org/data/2.5/forecast?q={city},{country_code}&appid={OPENWEATHER_API_KEY}&units=metric&cnt=40"
        r = requests.get(url, timeout=8)
        if r.status_code == 200:
            data = r.json()
            daily = {}
            for item in data["list"]:
                date = item["dt_txt"][:10]
                if date not in daily or "12:00" in item["dt_txt"]:
                    daily[date] = {
                        "day":      datetime.strptime(date, "%Y-%m-%d").strftime("%A"),
                        "temp":     round(item["main"]["temp"]),
                        "icon":     item["weather"][0]["icon"],
                        "desc":     item["weather"][0]["description"].title(),
                        "humidity": item["main"]["humidity"],
                    }
            return list(daily.values())[:5]
    except Exception:
        pass
    return []

def weather_icon_url(icon_code: str) -> str:
    return f"https://openweathermap.org/img/wn/{icon_code}@2x.png"

# ======================================================
# FEATURE 2 — LANDMARK DETECTION (Google Vision API)
# ======================================================

def detect_landmark_vision(image_bytes: bytes):
    if GOOGLE_VISION_API_KEY == "YOUR_GOOGLE_VISION_KEY":
        return None

    try:
        b64 = base64.b64encode(image_bytes).decode("utf-8")
        payload = {
            "requests": [{
                "image": {"content": b64},
                "features": [
                    {"type": "LANDMARK_DETECTION", "maxResults": 3},
                    {"type": "LABEL_DETECTION",    "maxResults": 5},
                    {"type": "OBJECT_LOCALIZATION","maxResults": 5},
                ]
            }]
        }
        url = f"https://vision.googleapis.com/v1/images:annotate?key={GOOGLE_VISION_API_KEY}"
        r = requests.post(url, json=payload, timeout=15)
        if r.status_code == 200:
            resp = r.json()["responses"][0]
            landmarks = resp.get("landmarkAnnotations", [])
            labels    = resp.get("labelAnnotations", [])
            if landmarks:
                lm = landmarks[0]
                loc = lm.get("locations", [{}])[0].get("latLng", {})
                return {
                    "name":        lm["description"],
                    "score":       round(lm["score"] * 100, 1),
                    "lat":         loc.get("latitude"),
                    "lng":         loc.get("longitude"),
                    "labels":      [l["description"] for l in labels[:4]],
                    "source":      "Google Vision API",
                }
            elif labels:
                return {
                    "name":    labels[0]["description"],
                    "score":   round(labels[0]["score"] * 100, 1),
                    "lat":     None, "lng": None,
                    "labels":  [l["description"] for l in labels[:4]],
                    "source":  "Google Vision (label)",
                }
    except Exception as e:
        st.error(f"Vision API error: {e}")
    return None

LANDMARK_DB = {
    "Table Mountain": {
        "description": "An iconic flat-topped mountain forming a prominent landmark overlooking Cape Town. Part of the Table Mountain National Park and a UNESCO World Heritage Site.",
        "city": "Cape Town, Western Cape",
        "lat": -33.9628, "lng": 18.4098,
        "activities": ["Cable Car Ride", "Hiking Trails", "Abseiling", "Rock Climbing", "Paragliding"],
        "nearby": ["V&A Waterfront", "Cape Point", "Boulders Beach", "Kirstenbosch Gardens"],
        "hotels": ["Cape Sun Resort", "Winelands Luxury Hotel"],
        "best_time": "October – March",
    },
    "Kruger National Park": {
        "description": "One of Africa's largest game reserves covering nearly 2 million hectares. Home to the Big Five and over 500 bird species.",
        "city": "Mpumalanga / Limpopo",
        "lat": -23.9884, "lng": 31.5547,
        "activities": ["Safari Game Drives", "Bush Walks", "Night Drives", "Bird Watching", "Photography"],
        "nearby": ["Blyde River Canyon", "Panorama Route", "God's Window"],
        "hotels": ["Kruger Safari Lodge"],
        "best_time": "May – September (dry season)",
    },
    "V&A Waterfront": {
        "description": "Cape Town's premier waterfront destination, a working harbour blending history, culture, shopping and entertainment.",
        "city": "Cape Town, Western Cape",
        "lat": -33.9036, "lng": 18.4218,
        "activities": ["Shopping", "Dining", "Whale Watching", "Boat Trips", "Two Oceans Aquarium"],
        "nearby": ["Robben Island", "Table Mountain", "Cape Town Stadium"],
        "hotels": ["Cape Sun Resort"],
        "best_time": "Year-round",
    },
    "Drakensberg": {
        "description": "The 'Dragon Mountains' — a UNESCO World Heritage site offering dramatic scenery, ancient San rock art and world-class hiking.",
        "city": "KwaZulu-Natal / Lesotho border",
        "lat": -29.2500, "lng": 29.4167,
        "activities": ["Hiking", "Rock Art Viewing", "Horse Riding", "Fly Fishing", "4x4 Trails"],
        "nearby": ["Giants Castle", "Royal Natal National Park", "Sani Pass"],
        "hotels": ["Mountain Retreat Lodge"],
        "best_time": "April – September",
    },
    "Robben Island": {
        "description": "Former maximum-security prison where Nelson Mandela was held for 18 years. A UNESCO World Heritage Site and powerful symbol of freedom.",
        "city": "Cape Town, Western Cape",
        "lat": -33.8063, "lng": 18.3661,
        "activities": ["Guided Prison Tours", "Museum Visit", "Penguin Colony", "Historical Walk"],
        "nearby": ["V&A Waterfront", "Table Mountain", "Bo-Kaap"],
        "hotels": ["Cape Sun Resort"],
        "best_time": "October – April",
    },
}

def identify_landmark_mock(image: Image.Image) -> dict:
    img_array = np.array(image.convert("RGB"))
    avg_green = img_array[:, :, 1].mean()
    avg_blue  = img_array[:, :, 2].mean()

    if avg_green > 120 and avg_blue < 100:
        name = "Kruger National Park"
    elif avg_blue > 130:
        name = "V&A Waterfront"
    else:
        name = "Table Mountain"

    info = LANDMARK_DB[name]
    return {
        "name":   name,
        "score":  round(np.random.uniform(78, 94), 1),
        "lat":    info["lat"],
        "lng":    info["lng"],
        "labels": ["landmark", "tourism", "South Africa"],
        "source": "AI Image Analysis (Demo Mode — add Google Vision API key for real detection)",
        **info,
    }

def get_landmark_info(name: str) -> dict:
    return LANDMARK_DB.get(name, {})

# ======================================================
# FEATURE 3 — AI CHATBOT (Claude / OpenAI)
# ======================================================

SYSTEM_PROMPT_TOURISM = """You are an expert South African tourism consultant named 'Zara'. 
You have deep knowledge of all SA provinces, destinations, hotels, activities, and travel tips.
Always respond in a friendly, enthusiastic tone. 
Keep responses concise (3-5 sentences max) unless asked for detail.
Focus on: beaches (Durban, Garden Route), safari (Kruger, Addo), adventure (Cape Town, Drakensberg), 
luxury (Franschhoek, Camps Bay), family (Sun City, Knysna), cultural (Soweto, Bo-Kaap, Robben Island).
When recommending hotels, mention the ones in the system: Cape Sun Resort, Sandton Palace, Durban Escape, 
Kruger Safari Lodge, Winelands Luxury Hotel.
Always end with a practical tip or call to action."""

def get_ai_response(messages: list, user_message: str) -> str:
    chat_history = [{"role": m["role"], "content": m["content"]} for m in messages[-10:]]
    chat_history.append({"role": "user", "content": user_message})

    if ANTHROPIC_API_KEY != "YOUR_ANTHROPIC_KEY":
        try:
            headers = {
                "x-api-key": ANTHROPIC_API_KEY,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            }
            payload = {
                "model": "claude-3-5-haiku-20241022",
                "max_tokens": 400,
                "system": SYSTEM_PROMPT_TOURISM,
                "messages": chat_history,
            }
            r = requests.post("https://api.anthropic.com/v1/messages", headers=headers, json=payload, timeout=20)
            if r.status_code == 200:
                return r.json()["content"][0]["text"]
        except Exception:
            pass

    if OPENAI_API_KEY != "YOUR_OPENAI_KEY":
        try:
            headers = {"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"}
            payload = {
                "model": "gpt-4o-mini",
                "messages": [{"role": "system", "content": SYSTEM_PROMPT_TOURISM}] + chat_history,
                "max_tokens": 400,
            }
            r = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload, timeout=20)
            if r.status_code == 200:
                return r.json()["choices"][0]["message"]["content"]
        except Exception:
            pass

    return smart_fallback_response(user_message)

def smart_fallback_response(msg: str) -> str:
    msg_lower = msg.lower()
    responses = {
        ("beach", "coast", "sea", "ocean", "swim"): (
            "🏖️ For South Africa's best beaches, **Durban's Golden Mile** offers warm Indian Ocean swimming year-round, "
            "while the **Garden Route** (Plettenberg Bay, Knysna) is stunning in summer. "
            "Cape Town's **Camps Bay** is glamorous but cold! "
            "I recommend the Durban Escape Hotel for a beach getaway — right on the beachfront. 🌊"
        ),
        ("safari", "game", "wildlife", "big five", "kruger", "lion", "elephant"): (
            "🦁 **Kruger National Park** is South Africa's crown jewel for safari! "
            "The best months are May–September (dry season) when animals congregate around waterholes. "
            "Our **Kruger Safari Lodge** offers expert game drives and luxury bush accommodation. "
            "You're almost guaranteed Big Five sightings — lion, leopard, rhino, elephant, and buffalo! 🐘"
        ),
        ("cape town", "table mountain", "cape", "western cape"): (
            "🏔️ **Cape Town** is one of the world's most beautiful cities! "
            "Don't miss the Table Mountain cable car, V&A Waterfront, Cape Point, and Boulders Beach penguins. "
            "The **Cape Sun Resort** puts you right in the heart of it all. "
            "Best visited October–March for warm, sunny weather. ☀️"
        ),
        ("johannesburg", "joburg", "jozi", "sandton", "gauteng"): (
            "🏙️ **Johannesburg** is SA's economic powerhouse with a vibrant culture scene! "
            "Visit Soweto, the Apartheid Museum, and the Cradle of Humankind. "
            "**Sandton Palace Hotel** is perfect for business or luxury stays. "
            "Joburg has world-class restaurants, galleries, and nightlife. 🍷"
        ),
        ("luxury", "honeymoon", "romantic", "spa", "wine"): (
            "🥂 For luxury and romance, **Stellenbosch & Franschhoek** in the Cape Winelands are unbeatable! "
            "The **Winelands Luxury Hotel** offers wine estate tours, gourmet dining, and a world-class spa. "
            "Best for couples, honeymoons, and celebrating special occasions. "
            "The region has over 200 wine estates to explore! 🍇"
        ),
        ("family", "kids", "children", "theme park", "sun city"): (
            "👨‍👩‍👧 For family holidays, **Sun City** (North West) is a fantastic entertainment resort with waterparks and safari. "
            "**Knysna** and the **Garden Route** are also brilliant for families — whale watching, forest hikes, and beaches. "
            "Durban Escape Hotel is family-friendly with easy beach access. "
            "Book early for school holiday periods (Dec, Jul)! 🎡"
        ),
        ("adventure", "hike", "climb", "extreme", "bungee"): (
            "🧗 SA is an adventure paradise! "
            "**Cape Town** offers abseiling off Table Mountain and shark cage diving. "
            "**Bloukrans Bridge** near Plettenberg Bay has the world's highest commercial bungee jump (216m). "
            "The **Drakensberg** is world-class for hiking and rock art. "
            "Wild Coast and Tsitsikamma are great for sea kayaking and canopy tours! 🏄"
        ),
        ("culture", "history", "museum", "heritage", "township"): (
            "🎭 SA's cultural highlights are profound and moving. "
            "Visit **Robben Island** where Mandela was imprisoned, the **Apartheid Museum** in Joburg, "
            "and vibrant **Bo-Kaap** in Cape Town with its colourful Cape Malay heritage. "
            "Soweto township tours offer incredible insight into SA's history and spirit. "
            "The **cradle of humankind** near Joburg is a UNESCO World Heritage site! 🌍"
        ),
        ("budget", "cheap", "affordable", "backpack"): (
            "💰 SA is excellent value! "
            "The **Garden Route** and **Wild Coast** are budget-friendly with great camping and backpacker lodges. "
            "Hostel dorms in Cape Town and Durban from R200–R400/night. "
            "Renting a car and self-driving the Garden Route is one of SA's best budget adventures. "
            "Visit April–June or August–September for lower prices outside peak season! 🎒"
        ),
    }
    for keywords, response in responses.items():
        if any(k in msg_lower for k in keywords):
            return response

    return (
        "🌍 South Africa is an incredible destination with something for everyone! "
        "Are you interested in **beaches**, **safari**, **adventure sports**, **wine regions**, or **cultural experiences**? "
        "I can tailor specific recommendations for Cape Town, Johannesburg, Durban, Kruger Park, or the Garden Route. "
        "What type of holiday experience are you dreaming of? ✈️"
    )

# ======================================================
# FEATURE 4 — HOTEL LOCATION MAPPING (Google Maps / Folium)
# ======================================================

HOTEL_COORDINATES = {
    "Cape Sun Resort":        {"lat": -33.9249, "lng": 18.4241, "city": "Cape Town",     "address": "Strand St, Cape Town, 8001"},
    "Sandton Palace":         {"lat": -26.1076, "lng": 28.0567, "city": "Johannesburg",  "address": "Sandton City, Johannesburg, 2196"},
    "Durban Escape":          {"lat": -29.8587, "lng": 31.0218, "city": "Durban",        "address": "Marine Parade, Durban, 4001"},
    "Kruger Safari Lodge":    {"lat": -24.0103, "lng": 31.4840, "city": "Kruger Park",   "address": "Skukuza, Kruger National Park"},
    "Winelands Luxury Hotel": {"lat": -33.9321, "lng": 18.8602, "city": "Stellenbosch",  "address": "Dorp Street, Stellenbosch, 7600"},
}

def build_hotel_map(selected_city: str = "All", selected_hotel: str = "All") -> folium.Map:
    m = folium.Map(
        location=[-30.5595, 22.9375],
        zoom_start=5,
        tiles="CartoDB positron",
        min_zoom=4,
        max_zoom=15,
    )
    folium.Rectangle(
        bounds=[[-35.0, 16.3], [-22.1, 33.0]],
        color="#ff6e40",
        fill=True,
        fill_opacity=0.02,
        weight=1.5,
        tooltip="South Africa"
    ).add_to(m)

    hotels = get_hotels()
    for _, h in hotels.iterrows():
        coords = HOTEL_COORDINATES.get(h["name"])
        if not coords:
            continue
        if selected_city != "All" and coords["city"] != selected_city:
            continue
        if selected_hotel != "All" and h["name"] != selected_hotel:
            continue

        icon_color = "orange" if h["type"] == "Luxury" else (
                     "blue"   if h["type"] == "Business" else (
                     "green"  if h["type"] == "Safari" else (
                     "red"    if h["type"] == "Beach" else "gray")))

        popup_html = f"""
        <div style="font-family:sans-serif;min-width:200px;">
          <b style="font-size:14px;color:#ff6e40;">{h['name']}</b><br>
          <span style="color:#666;">📍 {coords['address']}</span><br><br>
          <b>Type:</b> {h['type']}<br>
          <b>Rating:</b> ⭐ {h['rating']}/5.0<br>
          <b>Price:</b> R{h['price']:,}/night<br>
          <b>Occupancy:</b> {h['occupancy']}%<br>
          <b>Amenities:</b> {h['amenities']}<br>
        </div>
        """
        folium.Marker(
            location=[coords["lat"], coords["lng"]],
            popup=folium.Popup(popup_html, max_width=260),
            tooltip=f"🏨 {h['name']} — R{h['price']:,}",
            icon=folium.Icon(color=icon_color, icon="home", prefix="fa"),
        ).add_to(m)

    return m

# ======================================================
# FEATURE 5 — REAL-TIME HOTEL IMAGES (Google Places)
# ======================================================

HOTEL_IMAGE_URLS = {
    "Cape Sun Resort": [
        "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800",
        "https://images.unsplash.com/photo-1582719508461-905c673771fd?w=800",
        "https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?w=800",
    ],
    "Sandton Palace": [
        "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=800",
        "https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=800",
        "https://images.unsplash.com/photo-1618773928121-c32242e63f39?w=800",
    ],
    "Durban Escape": [
        "https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=800",
        "https://images.unsplash.com/photo-1501594907352-04cda38ebc29?w=800",
        "https://images.unsplash.com/photo-1615880484746-a134be9a6ecf?w=800",
    ],
    "Kruger Safari Lodge": [
        "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=800",
        "https://images.unsplash.com/photo-1516426122078-c23e76319801?w=800",
        "https://images.unsplash.com/photo-1523805009345-7448845a9e53?w=800",
    ],
    "Winelands Luxury Hotel": [
        "https://images.unsplash.com/photo-1455587734955-081b22074882?w=800",
        "https://images.unsplash.com/photo-1544148103-0773bf10d330?w=800",
        "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=800",
    ],
}

def get_hotel_images_places(hotel_name: str, city: str) -> list:
    if GOOGLE_PLACES_API_KEY != "YOUR_GOOGLE_PLACES_KEY":
        try:
            search_url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
            params = {
                "input":     f"{hotel_name} {city} South Africa",
                "inputtype": "textquery",
                "fields":    "place_id,name,photos",
                "key":       GOOGLE_PLACES_API_KEY,
            }
            r = requests.get(search_url, params=params, timeout=10)
            if r.status_code == 200:
                candidates = r.json().get("candidates", [])
                if candidates:
                    photos = candidates[0].get("photos", [])
                    urls = []
                    for photo in photos[:4]:
                        ref = photo["photo_reference"]
                        img_url = (
                            f"https://maps.googleapis.com/maps/api/place/photo"
                            f"?maxwidth=800&photo_reference={ref}&key={GOOGLE_PLACES_API_KEY}"
                        )
                        urls.append(img_url)
                    if urls:
                        return urls
        except Exception:
            pass
    return HOTEL_IMAGE_URLS.get(hotel_name, [
        "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800"
    ])

# ======================================================
# ML MODELS
# ======================================================

def predict_cancellation(lead_time, prev_cancels):
    X_train = [[5,0],[30,1],[60,2],[2,0],[45,1],[10,0],[55,2],[25,1]]
    y_train = [0,1,1,0,1,0,1,0]
    clf = RandomForestClassifier(random_state=42)
    clf.fit(X_train, y_train)
    return "High Risk" if clf.predict([[lead_time, prev_cancels]])[0] == 1 else "Low Risk"

def predict_revenue(bookings_count):
    X = np.array([[10],[20],[30],[40],[50],[60]])
    y = np.array([15000,32000,48000,61000,79000,92000])
    model = RandomForestRegressor(random_state=42)
    model.fit(X, y)
    return model.predict([[bookings_count]])[0]

def dynamic_hotel_price(base_price, demand, occupancy, season, holiday, weather):
    m = 1.0
    if demand == "High":  m += 0.20
    elif demand == "Low": m -= 0.10
    if occupancy > 80:  m += 0.25
    elif occupancy < 40: m -= 0.15
    if season == "Peak": m += 0.30
    if holiday: m += 0.20
    if weather in ["Sunny ☀️","Humid 🌤️"]: m += 0.10
    return round(base_price * m, 2)

def analyze_sentiment(review):
    analysis = TextBlob(review)
    p = analysis.sentiment.polarity
    if p > 0: return "Positive", p
    elif p < 0: return "Negative", p
    return "Neutral", p

def get_hotels():
    return pd.DataFrame([
        {"name":"Cape Sun Resort","price":2500,"city":"Cape Town","rating":4.7,"type":"Luxury","occupancy":85,"sentiment_score":92,"amenities":"WiFi, Pool, Spa"},
        {"name":"Sandton Palace","price":3500,"city":"Johannesburg","rating":4.8,"type":"Business","occupancy":78,"sentiment_score":88,"amenities":"WiFi, Gym, Conference Rooms"},
        {"name":"Durban Escape","price":2100,"city":"Durban","rating":4.4,"type":"Beach","occupancy":70,"sentiment_score":84,"amenities":"Beach Access, Pool, Bar"},
        {"name":"Kruger Safari Lodge","price":7000,"city":"Kruger Park","rating":5.0,"type":"Safari","occupancy":95,"sentiment_score":97,"amenities":"Safari Tours, WiFi, Restaurant"},
        {"name":"Winelands Luxury Hotel","price":5200,"city":"Stellenbosch","rating":4.9,"type":"Luxury","occupancy":82,"sentiment_score":93,"amenities":"Wine Tours, Spa, Pool"},
    ])

def rank_hotels(hotels_df, bookings_df):
    scores = []
    for _, h in hotels_df.iterrows():
        hotel_bookings = bookings_df[bookings_df['hotel'] == h['name']] if not bookings_df.empty else pd.DataFrame()
        revenue = hotel_bookings['cost'].sum() if not hotel_bookings.empty else 0
        cancellations = len(hotel_bookings[hotel_bookings['status'] == 'Cancelled']) if not hotel_bookings.empty else 0
        total = len(hotel_bookings) if not hotel_bookings.empty else 1
        cancel_rate = cancellations / max(total, 1)
        score = (h['rating']*20 + h['occupancy']*0.4 + h['sentiment_score']*0.3 + min(revenue/1000,20) - cancel_rate*15)
        scores.append({
            "Hotel": h['name'], "City": h['city'], "Rating": h['rating'], "Occupancy": h['occupancy'],
            "Sentiment": h['sentiment_score'], "Revenue": revenue, "Cancel Rate": round(cancel_rate*100,1), "Score": round(score,1)
        })
    ranked = pd.DataFrame(scores).sort_values("Score", ascending=False).reset_index(drop=True)
    tiers = []
    for i, row in ranked.iterrows():
        if i == 0 or row['Score'] >= ranked['Score'].quantile(0.75): tiers.append("🏆 Top Performer")
        elif row['Score'] >= ranked['Score'].quantile(0.4):           tiers.append("⚠️ Average")
        else:                                                          tiers.append("❌ Underperforming")
    ranked['Tier'] = tiers
    return ranked

# ======================================================
# ACCESS CONTROL HELPERS
# ======================================================

def require_role(allowed_roles: list):
    role = st.session_state.get("role", "")
    if role not in allowed_roles:
        st.markdown("""
        <div class='access-denied'>
            <h2>🔒 Access Denied</h2>
            <p style='color:#94a3b8;'>You don't have permission to view this section.<br>
            Please contact your administrator if you believe this is an error.</p>
        </div>""", unsafe_allow_html=True)
        return False
    return True

def role_badge(role: str) -> str:
    badges = {
        "Tourist":       "<span class='role-badge-tourist'>🌍 Tourist</span>",
        "Hotel Manager": "<span class='role-badge-manager'>🏨 Hotel Manager</span>",
        "Admin":         "<span class='role-badge-admin'>🛡️ Admin</span>",
    }
    return badges.get(role, role)

# ======================================================
# PDF UTILITIES
# ======================================================

def safe(text):
    replacements = {
        "\u2014":"-","\u2013":"-","\u2018":"'","\u2019":"'","\u201C":'"',"\u201D":'"',
        "\u2022":"-","\u2026":"...","\u00B0":" deg",
        "🏆":"[TOP]","⚠️":"[AVG]","❌":"[LOW]","🌍":"","✅":"OK","📊":"",
        "💰":"","📅":"","🤖":"","😊":"","📄":"","🛡️":"","🔴":"[!]","🟡":"[~]","🟢":"[OK]",
    }
    for u, a in replacements.items():
        text = text.replace(u, a)
    return text.encode("latin-1", errors="replace").decode("latin-1")

# ======================================================
# MAIN APP
# ======================================================

def main():
    apply_styles()
    init_db()
    hotels = get_hotels()

    st.sidebar.title("🌍 Tourism-travel-hospitality ZA")
    if st.session_state.get("role"):
        st.sidebar.markdown(f"**Logged in as:** {st.session_state.get('user','')}")
        st.sidebar.markdown(role_badge(st.session_state.get("role", "")), unsafe_allow_html=True)
        st.sidebar.divider()
    amount = st.sidebar.number_input("Amount in ZAR", value=1000, min_value=0)
    currency = st.sidebar.selectbox("Convert To", ["USD","EUR","GBP","AUD","CNY"])
    rates = {"USD":0.053,"EUR":0.049,"GBP":0.042,"AUD":0.082,"CNY":0.38}
    st.sidebar.success(f"≈ {amount*rates[currency]:.2f} {currency}")

    for key, default in [("role", None), ("user", ""), ("user_id", None), ("full_name", ""), ("chat_history", [])]:
        if key not in st.session_state:
            st.session_state[key] = default

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # LOGIN PAGE
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    if st.session_state.role is None:
        st.markdown("""
        <div class='hero'>
            <h1 style='font-size:2.4rem;'>🌍 Welcome to Smart Tourism-travel ZA</h1>
            <p style='color:#94a3b8;font-size:1.15rem;'>Enterprise Smart Tourism & Hospitality Platform for South Africa</p>
            <p style='color:#64748b;font-size:0.9rem;margin-top:8px;'>Real-Time Data · Role-Based Access</p>
        </div>""", unsafe_allow_html=True)

        col1, col2 = st.columns([1, 1])
        with col1:
            st.subheader("🔐 Secure Login")
            username = st.text_input("Username", placeholder="e.g. tourist1")
            password = st.text_input("Password", type="password", placeholder="Your password")

            if st.button("Login", use_container_width=True):
                user = authenticate_user(username, password)
                if user:
                    st.session_state.role      = user[2]
                    st.session_state.user      = user[1]
                    st.session_state.user_id   = user[0]
                    st.session_state.full_name = user[3]
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials or account inactive.")

            st.divider()
            with st.expander("📋 Demo Credentials"):
                st.markdown("""
                | Role | Username | Password |
                |------|----------|----------|
                | Tourist | `tourist1` | `tourist123` |
                | Hotel Manager | `manager1` | `manager123` |
                | Admin | `admin1` | `admin123` |
                """)

        with col2:
            st.image("https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=700",
                     caption="South Africa — Where Every Journey Begins", use_container_width=True)
            st.markdown("""
            <div class='metric-card'>
                <h4>Platform Features</h4>
                <p style='color:#94a3b8;font-size:0.9rem;'>
                ✅ Live weather for any SA destination<br>
                ✅ AI landmark detection from photos<br>
                ✅ Intelligent SA travel chatbot<br>
                ✅ Interactive hotel map (SA-only)<br>
                ✅ Real-time hotel image galleries<br>
                ✅ Role-based secure access<br>
                ✅ AI dynamic pricing & forecasting
                </p>
            </div>""", unsafe_allow_html=True)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # TOURIST DASHBOARD
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    elif st.session_state.role == "Tourist":
        if not require_role(["Tourist"]):
            return

        name = st.session_state.full_name or st.session_state.user
        st.title(f"✈️ Welcome, {name}!")
        c1, c2, c3 = st.columns(3)
        c1.metric("Available Hotels", 5)
        c2.metric("Destinations", 5)
        c3.metric("Avg Satisfaction", "94%")

        tabs = st.tabs([
            "🏨 Hotels & Booking",
            "🌦️ Live Weather",
            "🤖 AI Recommendations",
            "⚖️ Compare Hotels",
            "🗺️ Hotel Map",
            "💬 AI Chatbot",
            "😊 Reviews",
            "📷 Landmark Detection",
        ])

        # ── Tab 0: Hotels & Booking ──
        with tabs[0]:
            st.subheader("🏨 Smart Hotel Booking")
            col1, col2 = st.columns([1, 2])
            with col1:
                check_in  = st.date_input("Check-in")
                check_out = st.date_input("Check-out")
                budget    = st.slider("Budget (ZAR)", 1000, 10000, 3000, step=500)
                sel_city  = st.selectbox("Destination", ["All", "Cape Town", "Johannesburg", "Durban", "Kruger Park", "Stellenbosch"])
                hotel_type = st.selectbox("Hotel Type", ["All", "Luxury", "Business", "Beach", "Safari"])

            filtered = hotels.copy()
            if budget:          filtered = filtered[filtered["price"] <= budget]
            if sel_city != "All":  filtered = filtered[filtered["city"] == sel_city]
            if hotel_type != "All": filtered = filtered[filtered["type"] == hotel_type]

            with col2:
                st.success(f"🔍 Found **{len(filtered)}** hotel(s) matching your criteria")

            for _, row in filtered.iterrows():
                st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
                c1, c2, c3 = st.columns([1, 3, 1])
                with c1:
                    imgs = get_hotel_images_places(row["name"], row["city"])
                    if imgs:
                        st.image(imgs[0], use_container_width=True)
                with c2:
                    st.subheader(row["name"])
                    st.write(f"📍 {row['city']}  |  💰 **R{row['price']:,}/night**  |  ⭐ {row['rating']}  |  🏷️ {row['type']}")
                    st.write(f"🛎️ {row['amenities']}  |  📊 Occupancy: {row['occupancy']}%")
                    if st.button("📷 View Gallery", key=f"gal_{row['name']}"):
                        st.session_state[f"show_gallery_{row['name']}"] = True
                with c3:
                    if st.button("✅ Book Now", key=f"bk_{row['name']}"):
                        save_booking(st.session_state.user, row["name"], row["city"], row["price"])
                        st.success(f"Booked {row['name']}! 🎉")

                if st.session_state.get(f"show_gallery_{row['name']}"):
                    imgs = get_hotel_images_places(row["name"], row["city"])
                    gcols = st.columns(min(len(imgs), 3))
                    for gi, img_url in enumerate(imgs[:3]):
                        gcols[gi].image(img_url, use_container_width=True)
                    if st.button("Close Gallery", key=f"cls_{row['name']}"):
                        del st.session_state[f"show_gallery_{row['name']}"]

                st.markdown("</div>", unsafe_allow_html=True)

        # ── Tab 1: FEATURE 1 — Live Weather ──
        with tabs[1]:
            st.subheader("🌦️ Real-Time Weather — South Africa")
            sa_cities = ["Cape Town", "Johannesburg", "Durban", "Kruger Park", "Stellenbosch",
                         "Pretoria", "Port Elizabeth", "Knysna", "Bloemfontein", "East London"]

            col1, col2 = st.columns([1, 2])
            with col1:
                weather_city    = st.selectbox("Select City", sa_cities, key="weather_city_tourist")
                custom_city     = st.text_input("Or type any SA city", placeholder="e.g. Hermanus")
                search_city     = custom_city.strip() if custom_city.strip() else weather_city
                refresh_weather = st.button("🔄 Refresh Weather")

            with col2:
                w = get_live_weather(search_city)
                if w:
                    st.markdown(f"""
                    <div class='weather-card'>
                        <h2 style='color:#38bdf8;margin-bottom:4px;'>📍 {search_city}</h2>
                        <h1 style='font-size:3.5rem;margin:0;'>{w['temp']}°C</h1>
                        <p style='color:#94a3b8;font-size:1.1rem;margin:4px 0;'>{w['condition']}</p>
                        <p style='color:#64748b;font-size:0.9rem;'>Feels like {w['feels_like']}°C</p>
                    </div>""", unsafe_allow_html=True)
                    wc1, wc2, wc3, wc4 = st.columns(4)
                    wc1.metric("💧 Humidity",    f"{w['humidity']}%")
                    wc2.metric("💨 Wind Speed",  f"{w['wind_speed']} km/h")
                    wc3.metric("🌡️ Pressure",    f"{w['pressure']} hPa")
                    wc4.metric("👁️ Visibility",  f"{w['visibility']} km")

            st.subheader("📅 5-Day Forecast")
            forecast = get_weather_forecast(search_city)
            if forecast:
                fcols = st.columns(len(forecast))
                for fi, day in enumerate(forecast):
                    fcols[fi].markdown(f"""
                    <div class='forecast-card'>
                        <b style='color:#94a3b8;font-size:0.8rem;'>{day['day'][:3].upper()}</b><br>
                        <span style='font-size:1.5rem;'>🌤️</span><br>
                        <b style='font-size:1.2rem;'>{day['temp']}°C</b><br>
                        <span style='color:#64748b;font-size:0.75rem;'>{day['desc']}</span><br>
                        <span style='color:#38bdf8;font-size:0.75rem;'>💧 {day['humidity']}%</span>
                    </div>""", unsafe_allow_html=True)

            st.subheader("🗺️ Weather Snapshot — All SA Destinations")
            all_weather = []
            for c in ["Cape Town", "Johannesburg", "Durban", "Kruger Park", "Stellenbosch"]:
                ww = get_live_weather(c)
                if ww:
                    all_weather.append({"City": c, "Temp (°C)": ww["temp"], "Humidity (%)": ww["humidity"],
                                        "Wind (km/h)": ww["wind_speed"], "Condition": ww["condition"]})
            if all_weather:
                weather_df = pd.DataFrame(all_weather)
                st.dataframe(weather_df, use_container_width=True, hide_index=True)
                st.plotly_chart(px.bar(weather_df, x="City", y="Temp (°C)", color="City",
                    title="Temperature Comparison Across SA Destinations", template="plotly_dark"),
                    use_container_width=True)

        # ── Tab 2: AI Recommendations ──
        with tabs[2]:
            st.subheader("🧠 Hotel Recommendations")
            col1, col2 = st.columns(2)
            with col1:
                ai_budget  = st.slider("Your Budget (ZAR)", 1000, 10000, 3000, step=500, key="ai_budget")
                travel_exp = st.selectbox("Travel Experience", ["Luxury", "Business", "Beach", "Safari"])
                ai_city    = st.selectbox("Preferred Area", ["All"] + ["Cape Town","Johannesburg","Durban","Kruger Park","Stellenbosch"])
            with col2:
                w_dest = get_live_weather(ai_city if ai_city != "All" else "Cape Town")
                if w_dest:
                    st.markdown(f"""
                    <div class='forecast-card'>
                        <b>Current Weather — {ai_city if ai_city != 'All' else 'Cape Town'}</b><br>
                        <span style='font-size:1.5rem;'>🌡️</span> {w_dest['temp']}°C · {w_dest['condition']}<br>
                        <span style='color:#64748b;font-size:0.8rem;'>Humidity: {w_dest['humidity']}% · Wind: {w_dest['wind_speed']} km/h</span>
                    </div>""", unsafe_allow_html=True)

            recs = hotels[hotels["price"] <= ai_budget]
            if travel_exp: recs = recs[recs["type"] == travel_exp]
            if ai_city != "All": recs = recs[recs["city"] == ai_city]
            recs = recs.sort_values(["rating", "price"], ascending=[False, True])

            if recs.empty:
                st.warning("No hotels match your criteria. Try adjusting your budget or preferences.")
            else:
                for _, h in recs.iterrows():
                    with st.expander(f"🏨 {h['name']} — R{h['price']:,}/night  ⭐ {h['rating']}"):
                        ec1, ec2 = st.columns([2, 1])
                        with ec1:
                            imgs = get_hotel_images_places(h["name"], h["city"])
                            st.image(imgs[0], use_container_width=True)
                        with ec2:
                            st.write(f"📍 {h['city']}")
                            st.write(f"🏷️ {h['type']}")
                            st.write(f"⭐ Rating: {h['rating']}/5.0")
                            st.write(f"📊 Occupancy: {h['occupancy']}%")
                            st.write(f"🛎️ {h['amenities']}")
                            wh = get_live_weather(h["city"])
                            if wh:
                                st.info(f"🌡️ {wh['temp']}°C · {wh['condition']}")
                            if st.button("Book", key=f"rec_bk_{h['name']}"):
                                save_booking(st.session_state.user, h["name"], h["city"], h["price"])
                                st.success("Booked! ✅")

        # ── Tab 3: Compare Hotels ──
        with tabs[3]:
            st.subheader("⚖️ Hotel Comparison")
            sel = st.multiselect("Select Hotels to Compare (min 2)", hotels["name"].tolist())
            if len(sel) >= 2:
                cdf = hotels[hotels["name"].isin(sel)].copy()

                img_cols = st.columns(len(sel))
                for ci, h_name in enumerate(sel):
                    imgs = get_hotel_images_places(h_name, cdf[cdf["name"]==h_name]["city"].values[0])
                    if imgs:
                        img_cols[ci].image(imgs[0], caption=h_name, use_container_width=True)

                cdf_display = cdf[["name","city","type","price","rating","occupancy","sentiment_score","amenities"]]
                cdf_display.columns = ["Hotel","City","Type","Price (ZAR)","Rating","Occupancy %","Sentiment %","Amenities"]
                st.dataframe(cdf_display, use_container_width=True, hide_index=True)

                cc1, cc2 = st.columns(2)
                cc1.plotly_chart(px.bar(cdf, x="name", y="rating", color="name", title="Rating Comparison",
                    template="plotly_dark", text="rating"), use_container_width=True)
                cc2.plotly_chart(px.bar(cdf, x="name", y="price", color="name", title="Price Comparison (ZAR)",
                    template="plotly_dark", text="price"), use_container_width=True)

                st.subheader("🌦️ Live Weather at Each Hotel Location")
                wc_cols = st.columns(len(sel))
                for wi, h_name in enumerate(sel):
                    city_name = cdf[cdf["name"]==h_name]["city"].values[0]
                    ww = get_live_weather(city_name)
                    if ww:
                        wc_cols[wi].markdown(f"""
                        <div class='forecast-card'>
                            <b>{h_name}</b><br>
                            <b style='font-size:1.4rem;'>{ww['temp']}°C</b><br>
                            <span style='color:#94a3b8;'>{ww['condition']}</span><br>
                            <span style='font-size:0.8rem;color:#64748b;'>💧 {ww['humidity']}% · 💨 {ww['wind_speed']} km/h</span>
                        </div>""", unsafe_allow_html=True)
            else:
                st.info("Please select at least 2 hotels to compare.")

        # ── Tab 4: FEATURE 4 — Hotel Map ──
        with tabs[4]:
            st.subheader("🗺️ Interactive Hotel Map — South Africa")
            mc1, mc2 = st.columns([1, 3])
            with mc1:
                map_city   = st.selectbox("Filter by City",   ["All","Cape Town","Johannesburg","Durban","Kruger Park","Stellenbosch"])
                map_hotel  = st.selectbox("Filter by Hotel",  ["All"] + hotels["name"].tolist())
                map_type = st.selectbox(
                    "Hotel Type",
                    ["All","Luxury","Business","Beach","Safari"],
                    key="hotel_type_map"
                )                
                st.markdown("""
                <div class='metric-card'>
                    <b>Map Legend</b><br>
                    🟠 Luxury hotels<br>
                    🔵 Business hotels<br>
                    🟢 Safari lodges<br>
                    🔴 Beach resorts<br>
                    ⚫ Other
                </div>""", unsafe_allow_html=True)
            with mc2:
                hotel_map = build_hotel_map(map_city, map_hotel)
                st_folium(hotel_map, width=700, height=500)

            st.subheader("📌 Hotel Quick Info")
            hcols = st.columns(len(hotels))
            for hi, (_, h) in enumerate(hotels.iterrows()):
                coords = HOTEL_COORDINATES.get(h["name"], {})
                hcols[hi].markdown(f"""
                <div class='forecast-card'>
                    <b style='font-size:0.85rem;'>{h['name']}</b><br>
                    <span style='color:#ff6e40;font-size:0.8rem;'>R{h['price']:,}</span><br>
                    <span style='color:#94a3b8;font-size:0.75rem;'>⭐ {h['rating']} · {h['type']}</span><br>
                    <span style='color:#64748b;font-size:0.7rem;'>📍 {coords.get('address','')[:30]}</span>
                </div>""", unsafe_allow_html=True)

        # ── Tab 5: FEATURE 3 — AI Chatbot ──
        with tabs[5]:
            st.subheader("💬 Zara — Your SA Tourism AI Assistant")
            st.markdown("""
            <div class='metric-card'>
                <b>🤖 Ask Zara anything about South African travel!</b><br>
                <span style='color:#94a3b8;font-size:0.9rem;'>
                Try: "Best beach destinations" · "Safari tips for Kruger" · "Luxury wine estate recommendations" · 
                "Family-friendly spots" · "Adventure activities in Cape Town" · "Budget travel tips"
                </span>
            </div>""", unsafe_allow_html=True)

            cats = ["🏖️ Beaches", "🦁 Safari", "🏔️ Adventure", "🥂 Luxury", "👨‍👩‍👧 Family", "🎭 Culture", "💰 Budget Tips"]
            cat_cols = st.columns(len(cats))
            for ci, cat in enumerate(cats):
                if cat_cols[ci].button(cat, key=f"cat_{ci}"):
                    prompt = cat.split(" ", 1)[1]
                    st.session_state.chat_history.append({"role": "user", "content": f"Tell me about {prompt} in South Africa"})
                    with st.spinner("Zara is thinking..."):
                        response = get_ai_response(st.session_state.chat_history[:-1], f"Tell me about {prompt} in South Africa")
                    st.session_state.chat_history.append({"role": "assistant", "content": response})
                    st.rerun()

            chat_container = st.container()
            with chat_container:
                for msg in st.session_state.chat_history:
                    if msg["role"] == "user":
                        st.markdown(f"<div class='chat-bubble-user'>👤 {msg['content']}</div>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<div class='chat-bubble-bot'>🤖 <b>Zara:</b> {msg['content']}</div>", unsafe_allow_html=True)

            user_msg = st.chat_input("Ask Zara about SA travel destinations, hotels, tips...")
            if user_msg:
                st.session_state.chat_history.append({"role": "user", "content": user_msg})
                with st.spinner("Zara is researching..."):
                    response = get_ai_response(st.session_state.chat_history[:-1], user_msg)
                st.session_state.chat_history.append({"role": "assistant", "content": response})
                st.rerun()

            if st.button("🗑️ Clear Chat"):
                st.session_state.chat_history = []
                st.rerun()

        # ── Tab 6: Reviews ──
        with tabs[6]:
            st.subheader("😊 Write & Analyse Your Review")
            review_hotel  = st.selectbox("Hotel", hotels["name"].tolist())
            review_rating = st.slider("Your Rating", 1, 5, 4)
            review_text   = st.text_area("Share your experience...", height=150)
            if st.button("Analyse Review"):
                if review_text.strip():
                    sentiment, polarity = analyze_sentiment(review_text)
                    sc1, sc2 = st.columns(2)
                    color = "#34d399" if sentiment == "Positive" else ("#f87171" if sentiment == "Negative" else "#f59e0b")
                    sc1.markdown(f"""
                    <div class='metric-card' style='text-align:center;border-color:{color};'>
                        <h2 style='color:{color};'>{sentiment}</h2>
                        <p>Polarity Score: {polarity:.3f}</p>
                        <p>Your Rating: {'⭐' * review_rating}</p>
                    </div>""", unsafe_allow_html=True)
                    with sc2:
                        wc = WordCloud(width=600, height=300, background_color="white").generate(review_text)
                        fig, ax = plt.subplots(figsize=(6, 3))
                        ax.imshow(wc)
                        ax.axis("off")
                        st.pyplot(fig)
                        plt.close(fig)
                else:
                    st.warning("Please write a review first.")

        # ── Tab 7: FEATURE 2 — Landmark Detection ──
        with tabs[7]:
            st.subheader("📷 AI Landmark Detection")
            st.markdown("""
            <div class='landmark-card'>
                <p style='color:#a78bfa;margin:0;'>Upload a photo of any South African landmark, attraction, or scenic spot. 
                Our AI will identify it and suggest nearby hotels and activities.</p>
            </div>""", unsafe_allow_html=True)

            ld_col1, ld_col2 = st.columns([1, 1])
            with ld_col1:
                uf = st.file_uploader("Upload Photo", type=["jpg", "jpeg", "png", "webp"])
                manual_landmark = st.selectbox("Or select a known landmark", ["Auto-detect"] + list(LANDMARK_DB.keys()))

            if uf:
                img = Image.open(uf)
                ld_col1.image(img, caption="Uploaded Image", use_container_width=True)
                uf.seek(0)
                img_bytes_data = uf.read()

                with ld_col2:
                    with st.spinner("🔍 Analysing image with AI..."):
                        result = detect_landmark_vision(img_bytes_data)
                        if not result:
                            result = identify_landmark_mock(img)
                        db_info = get_landmark_info(result.get("name", ""))
                        if db_info:
                            result.update(db_info)

                    if result:
                        st.markdown(f"""
                        <div class='landmark-card'>
                            <h3 style='color:#a78bfa;'>🏛️ {result.get('name','Unknown')}</h3>
                            <p style='color:#94a3b8;font-size:0.85rem;'>Confidence: {result.get('score','N/A')}% · {result.get('source','AI Analysis')}</p>
                            <p>📍 {result.get('city','South Africa')}</p>
                            <p>{result.get('description','A beautiful South African landmark.')}</p>
                        </div>""", unsafe_allow_html=True)

                        if result.get("activities"):
                            st.write("**🎯 Activities & Experiences:**")
                            act_cols = st.columns(min(len(result["activities"]), 3))
                            for ai, act in enumerate(result["activities"]):
                                act_cols[ai % 3].markdown(f"✅ {act}")

                        if result.get("nearby"):
                            st.write("**📍 Nearby Attractions:**")
                            st.write(" · ".join(result["nearby"]))

                        if result.get("hotels"):
                            st.write("**🏨 Recommended Hotels:**")
                            for hname in result["hotels"]:
                                h_data = hotels[hotels["name"]==hname]
                                if not h_data.empty:
                                    h = h_data.iloc[0]
                                    st.write(f"🏨 **{h['name']}** — R{h['price']:,}/night ⭐ {h['rating']}")

                        if result.get("best_time"):
                            st.info(f"📅 Best time to visit: **{result['best_time']}**")

                        if result.get("lat") and result.get("lng"):
                            lm_map = folium.Map(location=[result["lat"], result["lng"]], zoom_start=12)
                            folium.Marker(
                                [result["lat"], result["lng"]],
                                tooltip=result["name"],
                                icon=folium.Icon(color="purple", icon="star", prefix="fa")
                            ).add_to(lm_map)
                            st.write("**📍 Location on Map:**")
                            st_folium(lm_map, width=500, height=300)

            elif manual_landmark != "Auto-detect":
                with ld_col2:
                    info = LANDMARK_DB[manual_landmark]
                    st.markdown(f"""
                    <div class='landmark-card'>
                        <h3 style='color:#a78bfa;'>🏛️ {manual_landmark}</h3>
                        <p>📍 {info['city']}</p>
                        <p>{info['description']}</p>
                    </div>""", unsafe_allow_html=True)
                    if info.get("activities"):
                        st.write("**🎯 Activities:**")
                        for act in info["activities"]: st.write(f"✅ {act}")
                    if info.get("hotels"):
                        st.write("**🏨 Nearby Hotels:**")
                        for h in info["hotels"]: st.write(f"🏨 {h}")

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # HOTEL MANAGER DASHBOARD
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    elif st.session_state.role == "Hotel Manager":
        if not require_role(["Hotel Manager"]):
            return

        st.title("📊 Hotel Business Intelligence Console")
        conn = sqlite3.connect("tourism_ai.db")
        df = pd.read_sql("SELECT * FROM bookings", conn)
        conn.close()

        reviews_data = {
            "hotel":        ["Cape Sun Resort","Sandton Palace","Durban Escape","Kruger Safari Lodge","Winelands Luxury Hotel"],
            "positive":     [85,74,90,95,88],
            "neutral":      [10,15,6,3,8],
            "negative":     [5,11,4,2,4],
            "satisfaction": [4.6,4.2,4.8,4.9,4.7],
            "occupancy":    [85,78,70,95,82],
        }

        if not df.empty:
            k1, k2, k3, k4 = st.columns(4)
            k1.metric("💰 Revenue",       f"R{df['cost'].sum():,.2f}")
            k2.metric("📅 Bookings",      len(df))
            k3.metric("❌ Cancellations", len(df[df['status']=='Cancelled']))
            k4.metric("🔄 Refunds",       len(df[df['status']=='Refunded']))

        mgr_tabs = st.tabs([
            "📈 Dashboard",
            "🌦️ Destination Weather",
            "🔍 Booking Management",
            "🚩 Flagged Bookings",
            "💡 Dynamic Pricing",
            "🗺️ Hotel Map",
            "📄 Report",
        ])

        with mgr_tabs[0]:
            if not df.empty:
                st.plotly_chart(px.histogram(df, x="hotel", y="cost", color="hotel", title="Revenue by Hotel", template="plotly_dark"), use_container_width=True)
                combo = make_subplots(specs=[[{"secondary_y": True}]])
                combo.add_trace(go.Bar(x=reviews_data["hotel"], y=reviews_data["positive"], name="Positive %", marker_color='green'), secondary_y=False)
                combo.add_trace(go.Bar(x=reviews_data["hotel"], y=reviews_data["negative"], name="Negative %", marker_color='red'), secondary_y=False)
                combo.add_trace(go.Scatter(x=reviews_data["hotel"], y=reviews_data["satisfaction"], name="Satisfaction", mode="lines+markers", line=dict(color="cyan", width=3)), secondary_y=True)
                combo.update_layout(title="Sentiment & Satisfaction", template="plotly_dark", height=450, legend=dict(orientation="h"))
                st.plotly_chart(combo, use_container_width=True)
                df["risk"] = df.apply(lambda r: predict_cancellation(r["lead_time"], r["prev_cancels"]), axis=1)
                st.plotly_chart(px.pie(df["risk"].value_counts().reset_index().rename(columns={"risk":"Risk","count":"Count"}),
                    names="Risk", values="Count", color="Risk",
                    color_discrete_map={"High Risk":"#f87171","Low Risk":"#34d399"}, title="Cancellation Risk Split", template="plotly_dark"),
                    use_container_width=True)
            else:
                st.warning("No booking data yet.")

        with mgr_tabs[1]:
            st.subheader("🌦️ Live Weather — All Hotel Destinations")
            for _, h in hotels.iterrows():
                ww = get_live_weather(h["city"])
                if ww:
                    wc1, wc2 = st.columns([1, 3])
                    wc1.subheader(h["name"])
                    wc1.write(f"📍 {h['city']}")
                    wc2.markdown(f"""
                    <div class='weather-card' style='text-align:left;padding:16px;'>
                        <b style='color:#38bdf8;font-size:1.4rem;'>{ww['temp']}°C</b>
                        <span style='color:#94a3b8;'> · {ww['condition']}</span><br>
                        Humidity: {ww['humidity']}% · Wind: {ww['wind_speed']} km/h · Pressure: {ww['pressure']} hPa
                    </div>""", unsafe_allow_html=True)
                    st.divider()

        with mgr_tabs[2]:
            st.subheader("🔍 Booking Management")
            if not df.empty:
                col1, col2, col3 = st.columns(3)
                search_user  = col1.text_input("Search by User")
                search_hotel = col2.selectbox("Filter Hotel", ["All"] + hotels["name"].tolist())
                risk_filter  = col3.selectbox("AI Risk", ["All","High Risk","Low Risk"])
                filtered = df.copy()
                filtered["risk"] = filtered.apply(lambda r: predict_cancellation(r["lead_time"], r["prev_cancels"]), axis=1)
                if search_user:        filtered = filtered[filtered['user'].str.contains(search_user, case=False, na=False)]
                if search_hotel != "All": filtered = filtered[filtered['hotel'] == search_hotel]
                if risk_filter != "All":  filtered = filtered[filtered['risk'] == risk_filter]
                st.write(f"Showing **{len(filtered)}** bookings")
                for _, row in filtered.iterrows():
                    risk_label   = row.get("risk", "N/A")
                    status_color = "🔴" if row['status']=='Cancelled' else ("🟡" if row['status']=='Refunded' else "🟢")
                    risk_color   = "🔴" if risk_label=="High Risk" else "🟢"
                    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
                    cc1, cc2 = st.columns([4, 2])
                    with cc1:
                        st.write(f"**#{row['id']}** | {status_color} {row['status']} | 👤 {row['user']}")
                        st.write(f"🏨 {row['hotel']}  •  📍 {row['city']}  •  💰 R{row['cost']:,.0f}")
                        st.write(f"🗓️ {str(row['booking_date'])[:19]}  •  {risk_color} {risk_label}")
                        if row.get('flagged', 0) == 1:
                            st.markdown(f"<div class='flag-card'>🚩 {row.get('flag_reason','')}</div>", unsafe_allow_html=True)
                    with cc2:
                        if row['status'] == 'Active':
                            if st.button("🚩 Flag", key=f"mgr_flag_{row['id']}"):
                                flag_booking(row['id'], "Flagged by Hotel Manager")
                                st.rerun()
                    st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.warning("No bookings yet.")

        with mgr_tabs[3]:
            st.subheader("🚩 Flagged Bookings")
            if not df.empty and 'flagged' in df.columns:
                flagged_df = df[df['flagged'] == 1]
                if not flagged_df.empty:
                    for _, row in flagged_df.iterrows():
                        st.markdown("<div class='rank-danger'>", unsafe_allow_html=True)
                        c1, c2 = st.columns([4, 2])
                        with c1:
                            st.write(f"**#{row['id']}** | 👤 {row['user']} | 🏨 {row['hotel']} | R{row['cost']:,.0f}")
                            st.write(f"🚩 Reason: {row.get('flag_reason','Unknown')}")
                        with c2:
                            if st.button("✅ Clear", key=f"mgr_clr_{row['id']}"):
                                unflag_booking(row['id']); st.rerun()
                        st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.success("No flagged bookings!")

        with mgr_tabs[4]:
            st.subheader("💡 AI Dynamic Pricing")
            p1i, p2i, p3i = st.columns(3)
            base_price  = p1i.number_input("Base Price (ZAR)", 1000, 10000, 3000, step=100)
            demand_lvl  = p2i.selectbox("Demand Level", ["Low","Medium","High"])
            occ_pct     = p3i.slider("Occupancy %", 0, 100, 75)
            s1i, s2i, s3i = st.columns(3)
            season_t    = s1i.selectbox("Season", ["Off-Peak","Mid","Peak"])
            is_holiday  = s2i.checkbox("Public Holiday?")
            weather_n   = s3i.selectbox("Weather", ["Sunny ☀️","Cloudy ☁️","Rainy 🌧️","Humid 🌤️"])
            ai_price    = dynamic_hotel_price(base_price, demand_lvl, occ_pct, season_t, is_holiday, weather_n)
            delta_pct   = (ai_price - base_price) / base_price * 100
            st.success(f"🤖 Recommended: **R{ai_price:,.2f}** (Base R{base_price:,} → {delta_pct:+.1f}%)")

        with mgr_tabs[5]:
            st.subheader("🗺️ Hotel Locations — Management View")
            mgr_map = build_hotel_map()
            st_folium(mgr_map, width=900, height=500)

        with mgr_tabs[6]:
            st.subheader("📄 Generate Business Report")
            if not df.empty:
                if st.button("📊 Generate PDF Report"):
                    with st.spinner("Building report..."):
                        rfile = generate_detailed_report(df, reviews_data, hotels)
                    if os.path.exists(rfile):
                        st.success("✅ Report ready!")
                        with open(rfile, "rb") as f:
                            st.download_button("⬇️ Download Report", data=f,
                                file_name="AI_Hotel_Report.pdf", mime="application/pdf")
            else:
                st.warning("No booking data yet.")

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # ADMIN DASHBOARD
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    elif st.session_state.role == "Admin":
        if not require_role(["Admin"]):
            return

        st.title("🛡️ Admin Control Center")
        conn = sqlite3.connect("tourism_ai.db")
        df = pd.read_sql("SELECT * FROM bookings", conn)
        conn.close()

        reviews_data = {
            "hotel":        ["Cape Sun Resort","Sandton Palace","Durban Escape","Kruger Safari Lodge","Winelands Luxury Hotel"],
            "positive":     [85,74,90,95,88], "neutral": [10,15,6,3,8], "negative": [5,11,4,2,4],
            "satisfaction": [4.6,4.2,4.8,4.9,4.7], "occupancy": [85,78,70,95,82],
        }

        total_rev     = df['cost'].sum() if not df.empty else 0
        cancelled_rev = df[df['status']=='Cancelled']['cost'].sum() if not df.empty else 0
        refunded_rev  = df[df['status']=='Refunded']['cost'].sum() if not df.empty else 0
        active_rev    = df[df['status']=='Active']['cost'].sum() if not df.empty else 0
        high_risk     = 0
        if not df.empty:
            df["risk"] = df.apply(lambda r: predict_cancellation(r["lead_time"], r["prev_cancels"]), axis=1)
            high_risk  = len(df[df["risk"]=="High Risk"])

        k1,k2,k3,k4,k5,k6 = st.columns(6)
        k1.metric("Total Bookings",  len(df))
        k2.metric("Active Revenue",  f"R{active_rev:,.0f}")
        k3.metric("Revenue Lost",    f"R{cancelled_rev+refunded_rev:,.0f}")
        k4.metric("Cancellations",   len(df[df['status']=='Cancelled']) if not df.empty else 0)
        k5.metric("Refunds",         len(df[df['status']=='Refunded'])  if not df.empty else 0)
        k6.metric("⚠️ High Risk",    high_risk)

        admin_tabs = st.tabs([
            "📊 Analytics",
            "🎛️ Booking Control",
            "🏆 Performance Ranking",
            "💸 Loss & Risk",
            "🌦️ Weather Overview",
            "🗺️ Hotel Map",
            "👤 User Management",
            "📄 Full Report",
        ])

        with admin_tabs[0]:
            if not df.empty:
                col1, col2 = st.columns(2)
                with col1:
                    st.plotly_chart(px.histogram(df, x="hotel", y="cost", color="hotel", title="Revenue by Hotel", template="plotly_dark"), use_container_width=True)
                    st.plotly_chart(px.pie(df, names="city", title="Bookings by City", template="plotly_dark"), use_container_width=True)
                with col2:
                    st.plotly_chart(px.bar(
                        pd.DataFrame({"Hotel":reviews_data["hotel"],"Positive":reviews_data["positive"],"Negative":reviews_data["negative"],"Neutral":reviews_data["neutral"]}),
                        x="Hotel", y=["Positive","Negative","Neutral"], title="Sentiment Distribution", template="plotly_dark", barmode="stack"
                    ), use_container_width=True)
                    occ_df = pd.DataFrame({"Hotel":reviews_data["hotel"],"Occupancy":reviews_data["occupancy"]})
                    fig_occ = px.bar(occ_df, x="Hotel", y="Occupancy", title="Occupancy by Hotel", template="plotly_dark",
                                     color="Occupancy", color_continuous_scale=["red","yellow","green"])
                    fig_occ.add_hline(y=80, line_dash="dash", line_color="orange", annotation_text="80% threshold")
                    st.plotly_chart(fig_occ, use_container_width=True)
                st.dataframe(df.sort_values('booking_date', ascending=False), use_container_width=True, hide_index=True)
            else:
                st.warning("No booking data yet.")

        with admin_tabs[1]:
            st.subheader("🎛️ Booking Control Panel")
            if not df.empty:
                col1, col2 = st.columns(2)
                search    = col1.text_input("🔍 Search")
                status_f  = col2.selectbox("Status", ["All","Active","Cancelled","Refunded"])
                display_df = df.copy()
                if search:
                    display_df = display_df[
                        display_df['user'].str.contains(search, case=False, na=False) |
                        display_df['hotel'].str.contains(search, case=False, na=False) |
                        display_df['id'].astype(str).str.contains(search)]
                if status_f != "All":
                    display_df = display_df[display_df['status'] == status_f]
                st.write(f"Showing **{len(display_df)}** bookings")
                for _, row in display_df.iterrows():
                    status_icon = "🟢" if row['status']=='Active' else ("🔴" if row['status']=='Cancelled' else "🟡")
                    risk_label  = row.get("risk","N/A") if "risk" in df.columns else "N/A"
                    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
                    c1,c2,c3,c4 = st.columns([4,2,2,2])
                    with c1:
                        st.write(f"**#{row['id']}** {status_icon} {row['status']} | 👤 {row['user']}")
                        st.write(f"🏨 {row['hotel']} · 📍 {row['city']} · 💰 R{row['cost']:,.2f}")
                        if row.get('flagged',0): st.markdown(f"<div class='flag-card'>🚩 {row.get('flag_reason','')}</div>", unsafe_allow_html=True)
                    with c2:
                        if row['status']=='Active':
                            if st.button("❌ Cancel", key=f"adm_cancel_{row['id']}"):
                                cancel_booking(row['id']); st.rerun()
                        if row['status'] in ['Active','Cancelled'] and not row.get('refunded',0):
                            if st.button("💸 Refund", key=f"adm_refund_{row['id']}"):
                                refund_booking(row['id']); st.rerun()
                    with c3:
                        if row['status'] == 'Active':
                            new_h = st.selectbox("Reassign", ["—"]+hotels["name"].tolist(), key=f"adm_rs_{row['id']}")
                            if new_h != "—":
                                hr = hotels[hotels["name"]==new_h].iloc[0]
                                if st.button("🔁", key=f"adm_rsbtn_{row['id']}"):
                                    reassign_booking(row['id'], new_h, hr['city'], hr['price']); st.rerun()
                    with c4:
                        with st.expander("✏️ Edit"):
                            nu = st.text_input("User", value=row['user'], key=f"adm_eu_{row['id']}")
                            nc = st.number_input("Cost", value=float(row['cost']), key=f"adm_ec_{row['id']}")
                            if st.button("Save", key=f"adm_sv_{row['id']}"):
                                edit_booking(row['id'], nu, row['hotel'], row['city'], nc); st.rerun()
                        if not row.get('flagged',0):
                            if st.button("🚩 Flag", key=f"adm_flg_{row['id']}"):
                                flag_booking(row['id'], "Flagged by Admin"); st.rerun()
                        else:
                            if st.button("✅ Unflag", key=f"adm_uflg_{row['id']}"):
                                unflag_booking(row['id']); st.rerun()
                    st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.warning("No bookings yet.")

        with admin_tabs[2]:
            st.subheader("🏆 Hotel Performance Ranking")
            ranked = rank_hotels(hotels, df if not df.empty else pd.DataFrame())
            for i, (_, row) in enumerate(ranked.iterrows()):
                tier  = row['Tier']
                css   = "rank-gold" if "Top" in tier else ("rank-silver" if "Average" in tier else "rank-danger")
                st.markdown(f"<div class='{css}'>", unsafe_allow_html=True)
                cc1,cc2,cc3,cc4,cc5 = st.columns([1,3,2,2,2])
                cc1.markdown(f"### #{i+1}")
                cc2.write(f"**{row['Hotel']}** · {row['City']}\n{tier}")
                cc3.metric("Score",     row['Score'])
                cc4.metric("Occupancy", f"{row['Occupancy']}%")
                cc5.metric("Sentiment", f"{row['Sentiment']}%")
                st.markdown("</div>", unsafe_allow_html=True)
            st.plotly_chart(px.bar(ranked, x="Hotel", y="Score", color="Tier",
                color_discrete_map={"🏆 Top Performer":"#fbbf24","⚠️ Average":"#94a3b8","❌ Underperforming":"#f87171"},
                title="Hotel Performance Composite Score", template="plotly_dark", text="Score"), use_container_width=True)

        with admin_tabs[3]:
            st.subheader("💸 Revenue Loss & Risk")
            if not df.empty:
                col1, col2 = st.columns(2)
                with col1:
                    sr = df.groupby("status")["cost"].sum().reset_index()
                    sr.columns = ["Status","Revenue"]
                    fig_loss = px.bar(sr, x="Status", y="Revenue", color="Status",
                        color_discrete_map={"Active":"#34d399","Cancelled":"#f87171","Refunded":"#f59e0b"},
                        title="Revenue by Booking Status", template="plotly_dark", text="Revenue")
                    fig_loss.update_traces(texttemplate="R%{text:,.0f}", textposition="outside")
                    st.plotly_chart(fig_loss, use_container_width=True)
                    total_loss = cancelled_rev + refunded_rev
                    st.markdown(f"""
                    <div class='rank-danger'>
                        <b>💸 Revenue Loss Summary</b><br>
                        Cancellations: R{cancelled_rev:,.2f}<br>
                        Refunds: R{refunded_rev:,.2f}<br>
                        <b>Total: R{total_loss:,.2f} ({total_loss/max(total_rev,1)*100:.1f}%)</b>
                    </div>""", unsafe_allow_html=True)
                with col2:
                    rc = df["risk"].value_counts().reset_index()
                    rc.columns = ["Risk","Count"]
                    st.plotly_chart(px.pie(rc, names="Risk", values="Count", color="Risk",
                        color_discrete_map={"High Risk":"#f87171","Low Risk":"#34d399"},
                        title="Cancellation Risk Split", template="plotly_dark"), use_container_width=True)
            else:
                st.warning("No booking data.")

        with admin_tabs[4]:
            st.subheader("🌦️ Platform-Wide Weather Dashboard")
            all_cities = ["Cape Town","Johannesburg","Durban","Kruger Park","Stellenbosch","Pretoria","Port Elizabeth","Knysna"]
            wdata = []
            for city in all_cities:
                ww = get_live_weather(city)
                if ww:
                    wdata.append({"City": city, **ww})
            if wdata:
                wdf = pd.DataFrame(wdata)
                col1, col2 = st.columns(2)
                col1.plotly_chart(px.bar(wdf, x="City", y="temp", color="City",
                    title="Temperature Across SA", template="plotly_dark", labels={"temp":"°C"}), use_container_width=True)
                col2.plotly_chart(px.bar(wdf, x="City", y="humidity", color="City",
                    title="Humidity %", template="plotly_dark"), use_container_width=True)
                st.dataframe(wdf[["City","temp","feels_like","humidity","wind_speed","condition","pressure","visibility"]],
                    use_container_width=True, hide_index=True)

        with admin_tabs[5]:
            st.subheader("🗺️ Admin Hotel Map View")
            adm_map = build_hotel_map()
            st_folium(adm_map, width=1000, height=550)

        with admin_tabs[6]:
            st.subheader("👤 User Management & Access Control")
            users_df = get_all_users()

            u1,u2,u3,u4 = st.columns(4)
            u1.metric("Total Users",   len(users_df))
            u2.metric("Tourists",      len(users_df[users_df['role']=='Tourist']))
            u3.metric("Managers",      len(users_df[users_df['role']=='Hotel Manager']))
            u4.metric("Admins",        len(users_df[users_df['role']=='Admin']))

            st.write("**All Platform Users**")
            for _, u in users_df.iterrows():
                is_active = bool(u.get('is_active', 1))
                badge_css = "rank-gold" if u['role']=='Admin' else ("rank-silver" if u['role']=='Hotel Manager' else "metric-card")
                st.markdown(f"<div class='{badge_css}'>", unsafe_allow_html=True)
                uc1,uc2,uc3,uc4 = st.columns([3,2,2,1])
                with uc1:
                    st.write(f"**{u['full_name']}** (@{u['username']})")
                    st.write(f"📧 {u.get('email','N/A')} | 🕐 Last login: {str(u.get('last_login','Never'))[:16]}")
                with uc2:
                    st.write(f"**Role:** {u['role']}")
                    st.write(f"**Status:** {'🟢 Active' if is_active else '🔴 Inactive'}")
                with uc3:
                    st.write(f"**Created:** {str(u.get('created_at',''))[:10]}")
                with uc4:
                    if u['username'] != st.session_state.user:
                        new_status = 0 if is_active else 1
                        btn_label = "🔴 Deactivate" if is_active else "🟢 Activate"
                        if st.button(btn_label, key=f"usr_toggle_{u['id']}"):
                            toggle_user_status(u['id'], new_status); st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)

            st.divider()
            st.subheader("➕ Create New User")
            with st.expander("Add User"):
                nu1, nu2 = st.columns(2)
                new_username  = nu1.text_input("Username",   key="nu_username")
                new_password  = nu2.text_input("Password",   type="password", key="nu_password")
                new_full_name = nu1.text_input("Full Name",  key="nu_fullname")
                new_email     = nu2.text_input("Email",      key="nu_email")
                new_role      = st.selectbox("Role", ["Tourist","Hotel Manager","Admin"], key="nu_role")
                if st.button("Create User"):
                    if new_username and new_password:
                        ok, msg = create_user(new_username, new_password, new_role, new_email, new_full_name)
                        if ok: st.success(f"✅ {msg}")
                        else:  st.error(f"❌ {msg}")
                    else:
                        st.warning("Username and password are required.")

            st.divider()
            st.subheader("🔐 Role Permission Matrix")
            perm_data = {
                "Feature":               ["Hotel Booking", "Weather Data", "AI Chatbot", "Landmark Detection", "Hotel Map",
                                          "View Reviews", "Booking Management", "Flag Bookings", "Dynamic Pricing",
                                          "Analytics Dashboard", "User Management", "Generate Reports", "Cancel/Refund Bookings"],
                "Tourist 🌍":            ["✅","✅","✅","✅","✅","✅","❌","❌","❌","❌","❌","❌","❌"],
                "Hotel Manager 🏨":      ["❌","✅","❌","❌","✅","✅","✅","✅","✅","✅","❌","✅","❌"],
                "Admin 🛡️":             ["✅","✅","✅","✅","✅","✅","✅","✅","✅","✅","✅","✅","✅"],
            }
            st.dataframe(pd.DataFrame(perm_data), use_container_width=True, hide_index=True)

        with admin_tabs[7]:
            st.subheader("📄 Full Executive Report")
            if not df.empty:
                if st.button("🚀 Generate Complete PDF Report"):
                    with st.spinner("Building 8-page report..."):
                        rfile = generate_detailed_report(df, reviews_data, hotels)
                    if os.path.exists(rfile):
                        st.success("✅ Complete report ready!")
                        with open(rfile, "rb") as f:
                            st.download_button("⬇️ Download Full Report", data=f,
                                file_name="AI_Smart_Tourism_Report.pdf", mime="application/pdf")
            else:
                st.warning("No booking data yet.")

    if st.session_state.role:
        st.sidebar.divider()
        if st.sidebar.button("🚪 Logout"):
            for k in ["role","user","user_id","full_name","chat_history"]:
                st.session_state[k] = None if k != "chat_history" else []
            st.session_state.role = None
            st.rerun()


# ======================================================
# PDF REPORT GENERATOR
# ======================================================

def generate_detailed_report(df, reviews_data, hotels_df):
    chart_paths = []

    def make_chart(func):
        p = tempfile.mktemp(suffix=".png")
        chart_paths.append(p)
        func(p)
        return p

    def dark_fig(w=9, h=4):
        f, a = plt.subplots(figsize=(w, h))
        f.patch.set_facecolor("#0f172a"); a.set_facecolor("#1e293b")
        a.tick_params(colors="white"); a.spines[:].set_color("#334155")
        return f, a

    def p1_chart(p):
        rb = df.groupby("hotel")["cost"].sum().reset_index() if not df.empty else pd.DataFrame({"hotel":reviews_data["hotel"],"cost":[0]*5})
        f,a = dark_fig()
        bars = a.bar(rb["hotel"], rb["cost"], color=["#ff6e40","#38bdf8","#34d399","#f59e0b","#a78bfa"])
        a.set_title("Revenue by Hotel", color="white", fontsize=13, pad=10); a.set_ylabel("Revenue (ZAR)", color="white")
        for b in bars: a.text(b.get_x()+b.get_width()/2, b.get_height()+200, f"R{b.get_height():,.0f}", ha="center", color="white", fontsize=8)
        plt.xticks(rotation=20, ha="right"); plt.tight_layout(); plt.savefig(p, dpi=120, bbox_inches="tight", facecolor=f.get_facecolor()); plt.close(f)

    def p2_chart(p):
        f,a = dark_fig()
        x = np.arange(len(reviews_data["hotel"])); w=0.5
        a.bar(x, reviews_data["positive"], w, label="Positive", color="#34d399")
        a.bar(x, reviews_data["negative"], w, bottom=reviews_data["positive"], label="Negative", color="#f87171")
        a.set_xticks(x); a.set_xticklabels(reviews_data["hotel"], rotation=20, ha="right", color="white", fontsize=8)
        a.set_title("Guest Sentiment", color="white", fontsize=13); a.legend(facecolor="#1e293b", labelcolor="white")
        plt.tight_layout(); plt.savefig(p, dpi=120, bbox_inches="tight", facecolor=f.get_facecolor()); plt.close(f)

    def p3_chart(p):
        f,a = dark_fig()
        a.plot(reviews_data["hotel"], reviews_data["satisfaction"], marker="o", color="#38bdf8", linewidth=2.5, markersize=8)
        a.set_ylim(1,5.5); a.set_title("Guest Satisfaction", color="white", fontsize=13); a.set_ylabel("Score", color="white")
        plt.xticks(rotation=20, ha="right"); plt.tight_layout(); plt.savefig(p, dpi=120, bbox_inches="tight", facecolor=f.get_facecolor()); plt.close(f)

    def p4_chart(p):
        occ = reviews_data.get("occupancy", [75,82,91,68,88])
        f,a = dark_fig()
        a.fill_between(reviews_data["hotel"], occ, alpha=0.2, color="#a78bfa")
        a.plot(reviews_data["hotel"], occ, marker="s", color="#a78bfa", linewidth=2.5, markersize=8)
        a.axhline(80, color="#f59e0b", linestyle="--", linewidth=1.5, label="80% Threshold")
        a.set_title("Occupancy Forecast", color="white", fontsize=13); a.set_ylabel("Occupancy %", color="white")
        a.legend(facecolor="#1e293b", labelcolor="white"); plt.xticks(rotation=20, ha="right")
        plt.tight_layout(); plt.savefig(p, dpi=120, bbox_inches="tight", facecolor=f.get_facecolor()); plt.close(f)

    p1 = make_chart(p1_chart)
    p2 = make_chart(p2_chart)
    p3 = make_chart(p3_chart)
    p4 = make_chart(p4_chart)

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    def sec(t): pdf.set_font("Arial","B",13); pdf.set_text_color(255,110,64); pdf.cell(0,9,safe(t),ln=True); pdf.set_text_color(40,40,40); pdf.ln(2)
    def body(t): pdf.set_font("Arial","",10); pdf.set_text_color(40,40,40); pdf.multi_cell(0,6,safe(t)); pdf.ln(2)
    def img(p, w=180):
        if os.path.exists(p): pdf.image(p, x=15, w=w)
        pdf.ln(3)

    pdf.add_page()
    pdf.set_fill_color(15,23,42); pdf.rect(0,0,210,297,"F")
    pdf.set_y(60); pdf.set_font("Arial","B",26); pdf.set_text_color(255,110,64)
    pdf.cell(0,14,safe("AI SMART TOURISM ZA"), ln=True, align="C")
    pdf.set_font("Arial","B",14); pdf.set_text_color(255,255,255)
    pdf.cell(0,9,safe("Executive Analytics Report"), ln=True, align="C")
    pdf.set_font("Arial","",10); pdf.set_text_color(148,163,184)
    pdf.cell(0,7,safe(f"Generated: {datetime.now().strftime('%d %B %Y  |  %H:%M')}"), ln=True, align="C")
    total_rev = df['cost'].sum() if not df.empty else 0
    pdf.ln(12); pdf.set_font("Arial","B",11); pdf.set_text_color(56,189,248)
    for line in [f"Total Bookings: {len(df)}", f"Total Revenue: R{total_rev:,.2f}",
                 f"Hotels Monitored: {len(reviews_data['hotel'])}", f"Avg Satisfaction: {np.mean(reviews_data['satisfaction']):.2f}/5.0"]:
        pdf.cell(0,8,safe(line),ln=True,align="C")

    pdf.add_page()
    pdf.set_font("Arial","B",14); pdf.set_text_color(255,110,64)
    pdf.cell(0,10,safe("Analytics Overview"),ln=True,align="C"); pdf.ln(2)
    pdf.set_text_color(30,30,30)
    for cp in [p1,p2,p3,p4]: img(cp)

    pdf.add_page()
    sec("Key Performance Indicators")
    if not df.empty:
        best = df.groupby("hotel")["cost"].sum().idxmax()
        body(f"Top hotel by revenue: {best}. Total revenue: R{total_rev:,.2f}. Bookings: {len(df)}.")
    sec("Strategic Recommendations")
    body("1. Deploy AI Dynamic Pricing during peak seasons (Dec, Jan, Jul) for 15-30% revenue uplift.")
    body("2. Implement non-refundable rate tiers to reduce cancellation losses.")
    body("3. Properties with >10% negative sentiment need immediate service audits.")
    body("4. Target below-80% occupancy hotels with corporate packages and mid-week deals.")
    body("5. Capture email and satisfaction data on all bookings to improve AI model accuracy.")

    report_path = os.path.join(tempfile.gettempdir(), "AI_Hotel_Business_Report.pdf")
    pdf.output(report_path)
    for p in chart_paths:
        try: os.remove(p)
        except: pass
    return report_path


if __name__ == "__main__":
=======
# import streamlit as st
# import pandas as pd
# import numpy as np
# import plotly.express as px
# import plotly.graph_objects as go
# import sqlite3
# from datetime import datetime, timedelta
# from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
# from sklearn.cluster import KMeans
# from wordcloud import WordCloud
# import matplotlib
# matplotlib.use('Agg')
# import matplotlib.pyplot as plt
# from textblob import TextBlob
# from PIL import Image
# from fpdf import FPDF
# import folium
# from streamlit_folium import st_folium
# from plotly.subplots import make_subplots
# import tempfile
# import os
# import io

# # ======================================================
# # PAGE CONFIG
# # ======================================================

# st.set_page_config(
#     page_title="AI Smart Tourism ZA",
#     page_icon="🌍",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # ======================================================
# # PROFESSIONAL UI STYLING
# # ======================================================

# def apply_styles():
#     st.markdown("""
#     <style>
#     @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

#     .stApp {
#         background: linear-gradient(135deg, #0a0f1e 0%, #0f172a 50%, #1a0a2e 100%);
#         color: white;
#         font-family: 'DM Sans', sans-serif;
#     }
#     h1, h2, h3, h4 {
#         font-family: 'Syne', sans-serif !important;
#         color: white !important;
#         letter-spacing: -0.02em;
#     }
#     .hero {
#         background: linear-gradient(135deg, rgba(255,110,64,0.12), rgba(56,189,248,0.08));
#         backdrop-filter: blur(20px);
#         padding: 40px;
#         border-radius: 24px;
#         text-align: center;
#         border: 1px solid rgba(255,110,64,0.2);
#         box-shadow: 0 0 60px rgba(255,110,64,0.08), 0 8px 32px rgba(0,0,0,0.4);
#         margin-bottom: 28px;
#     }
#     .metric-card {
#         background: rgba(255,255,255,0.04);
#         backdrop-filter: blur(16px);
#         border-radius: 20px;
#         padding: 22px;
#         margin-bottom: 16px;
#         border: 1px solid rgba(255,255,255,0.08);
#         transition: all 0.3s cubic-bezier(0.4,0,0.2,1);
#         box-shadow: 0 4px 24px rgba(0,0,0,0.3);
#     }
#     .metric-card:hover {
#         transform: translateY(-4px);
#         border-color: rgba(255,110,64,0.3);
#         box-shadow: 0 12px 32px rgba(255,110,64,0.15);
#     }
#     .rank-gold {
#         background: linear-gradient(135deg, rgba(251,191,36,0.15), rgba(245,158,11,0.08));
#         border: 1px solid rgba(251,191,36,0.3);
#         border-radius: 16px;
#         padding: 16px 20px;
#         margin: 8px 0;
#     }
#     .rank-silver {
#         background: linear-gradient(135deg, rgba(148,163,184,0.12), rgba(100,116,139,0.06));
#         border: 1px solid rgba(148,163,184,0.25);
#         border-radius: 16px;
#         padding: 16px 20px;
#         margin: 8px 0;
#     }
#     .rank-danger {
#         background: linear-gradient(135deg, rgba(239,68,68,0.12), rgba(185,28,28,0.06));
#         border: 1px solid rgba(239,68,68,0.25);
#         border-radius: 16px;
#         padding: 16px 20px;
#         margin: 8px 0;
#     }
#     .flag-card {
#         background: rgba(239,68,68,0.1);
#         border: 1px solid rgba(239,68,68,0.3);
#         border-radius: 12px;
#         padding: 12px 16px;
#         margin: 6px 0;
#     }
#     .stButton>button {
#         background: linear-gradient(135deg, #ff6e40, #ff3d00);
#         color: white;
#         border: none;
#         border-radius: 12px;
#         padding: 10px 24px;
#         font-weight: 600;
#         font-family: 'DM Sans', sans-serif;
#         letter-spacing: 0.02em;
#         transition: all 0.2s;
#     }
#     .stButton>button:hover {
#         transform: translateY(-2px);
#         box-shadow: 0 6px 20px rgba(255,110,64,0.4);
#     }
#     section[data-testid="stSidebar"] {
#         background: rgba(10,15,30,0.8);
#         backdrop-filter: blur(20px);
#         border-right: 1px solid rgba(255,255,255,0.06);
#     }
#     .stTabs [data-baseweb="tab"] {
#         font-family: 'DM Sans', sans-serif;
#         font-weight: 500;
#     }
#     </style>
#     """, unsafe_allow_html=True)

# # ======================================================
# # DATABASE — Extended schema
# # ======================================================

# def init_db():
#     conn = sqlite3.connect("tourism_ai.db")
#     c = conn.cursor()
#     c.execute('''
#         CREATE TABLE IF NOT EXISTS bookings (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             user TEXT,
#             hotel TEXT,
#             city TEXT,
#             cost REAL,
#             booking_date TEXT,
#             lead_time INTEGER,
#             prev_cancels INTEGER,
#             satisfaction INTEGER,
#             status TEXT DEFAULT 'Active',
#             refunded INTEGER DEFAULT 0,
#             flagged INTEGER DEFAULT 0,
#             flag_reason TEXT DEFAULT ''
#         )
#     ''')
#     # Add missing columns if upgrading from old schema
#     for col, definition in [
#         ("status", "TEXT DEFAULT 'Active'"),
#         ("refunded", "INTEGER DEFAULT 0"),
#         ("flagged", "INTEGER DEFAULT 0"),
#         ("flag_reason", "TEXT DEFAULT ''"),
#     ]:
#         try:
#             c.execute(f"ALTER TABLE bookings ADD COLUMN {col} {definition}")
#         except Exception:
#             pass
#     conn.commit()
#     conn.close()

# # ======================================================
# # SAVE BOOKING
# # ======================================================

# def save_booking(user, hotel, city, cost):
#     conn = sqlite3.connect("tourism_ai.db")
#     c = conn.cursor()
#     c.execute(
#         """INSERT INTO bookings
#         (user, hotel, city, cost, booking_date, lead_time, prev_cancels, satisfaction, status, refunded, flagged, flag_reason)
#         VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'Active', 0, 0, '')""",
#         (user, hotel, city, cost, str(datetime.now()),
#          np.random.randint(1, 60), np.random.randint(0, 3), np.random.randint(1, 6))
#     )
#     conn.commit()
#     conn.close()

# # ======================================================
# # ADMIN DB OPERATIONS
# # ======================================================

# def cancel_booking(booking_id):
#     conn = sqlite3.connect("tourism_ai.db")
#     c = conn.cursor()
#     c.execute("UPDATE bookings SET status='Cancelled' WHERE id=?", (booking_id,))
#     conn.commit()
#     conn.close()

# def refund_booking(booking_id):
#     conn = sqlite3.connect("tourism_ai.db")
#     c = conn.cursor()
#     c.execute("UPDATE bookings SET status='Refunded', refunded=1 WHERE id=?", (booking_id,))
#     conn.commit()
#     conn.close()

# def reassign_booking(booking_id, new_hotel, new_city, new_cost):
#     conn = sqlite3.connect("tourism_ai.db")
#     c = conn.cursor()
#     c.execute("UPDATE bookings SET hotel=?, city=?, cost=? WHERE id=?",
#               (new_hotel, new_city, new_cost, booking_id))
#     conn.commit()
#     conn.close()

# def edit_booking(booking_id, user, hotel, city, cost):
#     conn = sqlite3.connect("tourism_ai.db")
#     c = conn.cursor()
#     c.execute("UPDATE bookings SET user=?, hotel=?, city=?, cost=? WHERE id=?",
#               (user, hotel, city, cost, booking_id))
#     conn.commit()
#     conn.close()

# def flag_booking(booking_id, reason):
#     conn = sqlite3.connect("tourism_ai.db")
#     c = conn.cursor()
#     c.execute("UPDATE bookings SET flagged=1, flag_reason=? WHERE id=?", (reason, booking_id))
#     conn.commit()
#     conn.close()

# def unflag_booking(booking_id):
#     conn = sqlite3.connect("tourism_ai.db")
#     c = conn.cursor()
#     c.execute("UPDATE bookings SET flagged=0, flag_reason='' WHERE id=?", (booking_id,))
#     conn.commit()
#     conn.close()

# # ======================================================
# # ML MODELS
# # ======================================================

# def predict_cancellation(lead_time, prev_cancels):
#     X_train = [[5,0],[30,1],[60,2],[2,0],[45,1],[10,0],[55,2],[25,1]]
#     y_train = [0,1,1,0,1,0,1,0]
#     clf = RandomForestClassifier(random_state=42)
#     clf.fit(X_train, y_train)
#     pred = clf.predict([[lead_time, prev_cancels]])
#     return "High Risk" if pred[0] == 1 else "Low Risk"

# def predict_revenue(bookings_count):
#     X = np.array([[10],[20],[30],[40],[50],[60]])
#     y = np.array([15000,32000,48000,61000,79000,92000])
#     model = RandomForestRegressor(random_state=42)
#     model.fit(X, y)
#     return model.predict([[bookings_count]])[0]

# # ======================================================
# # AI DYNAMIC PRICING
# # ======================================================

# def dynamic_hotel_price(base_price, demand, occupancy, season, holiday, weather):
#     m = 1.0
#     if demand == "High": m += 0.20
#     elif demand == "Low": m -= 0.10
#     if occupancy > 80: m += 0.25
#     elif occupancy < 40: m -= 0.15
#     if season == "Peak": m += 0.30
#     if holiday: m += 0.20
#     if weather in ["Sunny ☀️","Humid 🌤️"]: m += 0.10
#     return round(base_price * m, 2)

# def analyze_sentiment(review):
#     analysis = TextBlob(review)
#     p = analysis.sentiment.polarity
#     if p > 0: return "Positive", p
#     elif p < 0: return "Negative", p
#     return "Neutral", p

# def get_weather(city):
#     data = {
#         "Cape Town":    {"temp": "22°C", "condition": "Sunny ☀️"},
#         "Johannesburg": {"temp": "26°C", "condition": "Cloudy ☁️"},
#         "Durban":       {"temp": "28°C", "condition": "Humid 🌤️"},
#         "Kruger Park":  {"temp": "31°C", "condition": "Hot 🌡️"}
#     }
#     return data.get(city)

# def ai_recommend_hotels(hotels, budget, preferred_type=None):
#     filtered = hotels[hotels['price'] <= budget]
#     if preferred_type:
#         filtered = filtered[filtered['type'] == preferred_type]
#     return filtered.sort_values(by=['rating','price'], ascending=[False,True])

# def get_hotels():
#     return pd.DataFrame([
#         {"name":"Cape Sun Resort","price":2500,"city":"Cape Town","rating":4.7,"type":"Luxury","occupancy":85,"sentiment_score":92,"amenities":"WiFi, Pool, Spa","image":"https://images.unsplash.com/photo-1566073771259-6a8506099945"},
#         {"name":"Sandton Palace","price":3500,"city":"Johannesburg","rating":4.8,"type":"Business","occupancy":78,"sentiment_score":88,"amenities":"WiFi, Gym, Conference Rooms","image":"https://images.unsplash.com/photo-1522708323590-d24dbb6b0267"},
#         {"name":"Durban Escape","price":2100,"city":"Durban","rating":4.4,"type":"Beach","occupancy":70,"sentiment_score":84,"amenities":"Beach Access, Pool, Bar","image":"https://images.unsplash.com/photo-1506744038136-46273834b3fb"},
#         {"name":"Kruger Safari Lodge","price":7000,"city":"Kruger Park","rating":5.0,"type":"Safari","occupancy":95,"sentiment_score":97,"amenities":"Safari Tours, WiFi, Restaurant","image":"https://images.unsplash.com/photo-1512917774080-9991f1c4c750"},
#         {"name":"Winelands Luxury Hotel","price":5200,"city":"Stellenbosch","rating":4.9,"type":"Luxury","occupancy":82,"sentiment_score":93,"amenities":"Wine Tours, Spa, Pool","image":"https://images.unsplash.com/photo-1455587734955-081b22074882"}
#     ])

# # ======================================================
# # HOTEL PERFORMANCE RANKING
# # ======================================================

# def rank_hotels(hotels_df, bookings_df):
#     """Compute composite score and assign tier."""
#     scores = []
#     for _, h in hotels_df.iterrows():
#         hotel_bookings = bookings_df[bookings_df['hotel'] == h['name']] if not bookings_df.empty else pd.DataFrame()
#         revenue = hotel_bookings['cost'].sum() if not hotel_bookings.empty else 0
#         cancellations = len(hotel_bookings[hotel_bookings['status'] == 'Cancelled']) if not hotel_bookings.empty else 0
#         total = len(hotel_bookings) if not hotel_bookings.empty else 1
#         cancel_rate = cancellations / max(total, 1)

#         score = (
#             h['rating'] * 20 +
#             h['occupancy'] * 0.4 +
#             h['sentiment_score'] * 0.3 +
#             min(revenue / 1000, 20) -
#             cancel_rate * 15
#         )
#         scores.append({
#             "Hotel": h['name'],
#             "City": h['city'],
#             "Rating": h['rating'],
#             "Occupancy": h['occupancy'],
#             "Sentiment": h['sentiment_score'],
#             "Revenue": revenue,
#             "Cancel Rate": round(cancel_rate * 100, 1),
#             "Score": round(score, 1)
#         })

#     ranked = pd.DataFrame(scores).sort_values("Score", ascending=False).reset_index(drop=True)
#     tiers = []
#     for i, row in ranked.iterrows():
#         if i == 0 or row['Score'] >= ranked['Score'].quantile(0.75):
#             tiers.append("🏆 Top Performer")
#         elif row['Score'] >= ranked['Score'].quantile(0.4):
#             tiers.append("⚠️ Average")
#         else:
#             tiers.append("❌ Underperforming")
#     ranked['Tier'] = tiers
#     return ranked

# # ======================================================
# # SAFE STRING FOR PDF
# # ======================================================

# def safe(text):
#     replacements = {
#         "\u2014":"-","\u2013":"-","\u2018":"'","\u2019":"'","\u201C":'"',"\u201D":'"',
#         "\u2022":"-","\u2026":"...","\u00B0":" deg","\u2500":"-","\u2550":"=",
#         "\u2501":"-","\u2502":"|","\u25CF":"-","\u2713":"OK",
#         "🏆":"[TOP]","⚠️":"[AVG]","❌":"[LOW]","🌍":"","✅":"OK","📊":"",
#         "💰":"","📅":"","🤖":"","😊":"","📄":"","🛡️":"","🔴":"[!]","🟡":"[~]","🟢":"[OK]",
#     }
#     for u, a in replacements.items():
#         text = text.replace(u, a)
#     return text.encode("latin-1", errors="replace").decode("latin-1")

# # ======================================================
# # COMPREHENSIVE PDF REPORT — SINGLE PAGE OVERVIEW + FULL REPORT
# # ======================================================

# def generate_detailed_report(df, reviews_data, hotels_df):

#     chart_paths = []

#     # ── Chart 1: Revenue by Hotel ──
#     p1 = tempfile.mktemp(suffix=".png"); chart_paths.append(p1)
#     rev_by_hotel = df.groupby("hotel")["cost"].sum().reset_index() if not df.empty else pd.DataFrame({"hotel":reviews_data["hotel"],"cost":[0]*5})
#     fig1,ax1 = plt.subplots(figsize=(9,4)); fig1.patch.set_facecolor("#0f172a"); ax1.set_facecolor("#1e293b")
#     bars = ax1.bar(rev_by_hotel["hotel"],rev_by_hotel["cost"],color=["#ff6e40","#38bdf8","#34d399","#f59e0b","#a78bfa"])
#     ax1.set_title("Total Revenue by Hotel",color="white",fontsize=13,pad=10); ax1.set_ylabel("Revenue (ZAR)",color="white")
#     ax1.tick_params(colors="white"); ax1.spines[:].set_color("#334155")
#     for b in bars: ax1.text(b.get_x()+b.get_width()/2,b.get_height()+200,f"R{b.get_height():,.0f}",ha="center",color="white",fontsize=8)
#     plt.xticks(rotation=20,ha="right"); plt.tight_layout(); plt.savefig(p1,dpi=120,bbox_inches="tight",facecolor=fig1.get_facecolor()); plt.close(fig1)

#     # ── Chart 2: Sentiment Stacked ──
#     p2 = tempfile.mktemp(suffix=".png"); chart_paths.append(p2)
#     fig2,ax2 = plt.subplots(figsize=(9,4)); fig2.patch.set_facecolor("#0f172a"); ax2.set_facecolor("#1e293b")
#     x = np.arange(len(reviews_data["hotel"])); w=0.5
#     ax2.bar(x,reviews_data["positive"],w,label="Positive %",color="#34d399")
#     ax2.bar(x,reviews_data["negative"],w,bottom=reviews_data["positive"],label="Negative %",color="#f87171")
#     ax2.bar(x,reviews_data["neutral"],w,bottom=[p+n for p,n in zip(reviews_data["positive"],reviews_data["negative"])],label="Neutral %",color="#94a3b8")
#     ax2.set_xticks(x); ax2.set_xticklabels(reviews_data["hotel"],rotation=20,ha="right",color="white",fontsize=8)
#     ax2.set_title("Guest Sentiment Distribution",color="white",fontsize=13,pad=10); ax2.set_ylabel("Review %",color="white")
#     ax2.tick_params(colors="white"); ax2.spines[:].set_color("#334155"); ax2.legend(facecolor="#1e293b",labelcolor="white")
#     plt.tight_layout(); plt.savefig(p2,dpi=120,bbox_inches="tight",facecolor=fig2.get_facecolor()); plt.close(fig2)

#     # ── Chart 3: Satisfaction Line ──
#     p3 = tempfile.mktemp(suffix=".png"); chart_paths.append(p3)
#     fig3,ax3 = plt.subplots(figsize=(9,4)); fig3.patch.set_facecolor("#0f172a"); ax3.set_facecolor("#1e293b")
#     ax3.plot(reviews_data["hotel"],reviews_data["satisfaction"],marker="o",color="#38bdf8",linewidth=2.5,markersize=8)
#     for h,s in zip(reviews_data["hotel"],reviews_data["satisfaction"]):
#         ax3.annotate(f"{s}",(h,s),textcoords="offset points",xytext=(0,8),ha="center",color="white",fontsize=9)
#     ax3.set_ylim(1,5.5); ax3.set_title("Guest Satisfaction (out of 5)",color="white",fontsize=13,pad=10)
#     ax3.set_ylabel("Score",color="white"); ax3.tick_params(colors="white"); ax3.spines[:].set_color("#334155")
#     plt.xticks(rotation=20,ha="right"); plt.tight_layout(); plt.savefig(p3,dpi=120,bbox_inches="tight",facecolor=fig3.get_facecolor()); plt.close(fig3)

#     # ── Chart 4: Occupancy ──
#     p4 = tempfile.mktemp(suffix=".png"); chart_paths.append(p4)
#     occ = reviews_data.get("occupancy",[75,82,91,68,88])
#     fig4,ax4 = plt.subplots(figsize=(9,4)); fig4.patch.set_facecolor("#0f172a"); ax4.set_facecolor("#1e293b")
#     ax4.fill_between(reviews_data["hotel"],occ,alpha=0.2,color="#a78bfa")
#     ax4.plot(reviews_data["hotel"],occ,marker="s",color="#a78bfa",linewidth=2.5,markersize=8)
#     for h,o in zip(reviews_data["hotel"],occ): ax4.annotate(f"{o}%",(h,o),textcoords="offset points",xytext=(0,8),ha="center",color="white",fontsize=9)
#     ax4.set_ylim(0,115); ax4.set_title("Hotel Occupancy Forecast (%)",color="white",fontsize=13,pad=10)
#     ax4.set_ylabel("Occupancy %",color="white"); ax4.tick_params(colors="white"); ax4.spines[:].set_color("#334155")
#     ax4.axhline(80,color="#f59e0b",linestyle="--",linewidth=1.5,label="80% Threshold")
#     ax4.legend(facecolor="#1e293b",labelcolor="white"); plt.xticks(rotation=20,ha="right")
#     plt.tight_layout(); plt.savefig(p4,dpi=120,bbox_inches="tight",facecolor=fig4.get_facecolor()); plt.close(fig4)

#     # ── Chart 5: Monthly Bookings ──
#     p5 = tempfile.mktemp(suffix=".png"); chart_paths.append(p5)
#     months=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
#     mb=np.random.randint(20,120,12)
#     fig5,ax5 = plt.subplots(figsize=(9,4)); fig5.patch.set_facecolor("#0f172a"); ax5.set_facecolor("#1e293b")
#     ax5.bar(months,mb,color="#f59e0b",edgecolor="#0f172a")
#     ax5.set_title("Monthly Booking Volume",color="white",fontsize=13,pad=10); ax5.set_ylabel("Bookings",color="white")
#     ax5.tick_params(colors="white"); ax5.spines[:].set_color("#334155")
#     plt.tight_layout(); plt.savefig(p5,dpi=120,bbox_inches="tight",facecolor=fig5.get_facecolor()); plt.close(fig5)

#     # ── Chart 6: Performance Ranking ──
#     p6 = tempfile.mktemp(suffix=".png"); chart_paths.append(p6)
#     ranked = rank_hotels(hotels_df, df if not df.empty else pd.DataFrame())
#     colors_map = {"🏆 Top Performer":"#fbbf24","⚠️ Average":"#94a3b8","❌ Underperforming":"#f87171"}
#     bar_colors = [colors_map.get(t,"#94a3b8") for t in ranked["Tier"]]
#     fig6,ax6 = plt.subplots(figsize=(9,4.5)); fig6.patch.set_facecolor("#0f172a"); ax6.set_facecolor("#1e293b")
#     bars6 = ax6.barh(ranked["Hotel"],ranked["Score"],color=bar_colors,edgecolor="#0f172a",height=0.6)
#     for b,tier in zip(bars6,ranked["Tier"]):
#         label = "[TOP]" if "Top" in tier else "[AVG]" if "Average" in tier else "[LOW]"
#         ax6.text(b.get_width()+0.3,b.get_y()+b.get_height()/2,f"{b.get_width():.1f} {label}",
#                  va="center",color="white",fontsize=9)
#     ax6.set_title("Hotel Performance Ranking (Composite Score)",color="white",fontsize=13,pad=10)
#     ax6.set_xlabel("Score",color="white"); ax6.tick_params(colors="white"); ax6.spines[:].set_color("#334155")
#     plt.tight_layout(); plt.savefig(p6,dpi=120,bbox_inches="tight",facecolor=fig6.get_facecolor()); plt.close(fig6)

#     # ── Chart 7: Cancellation Risk Pie ──
#     p7 = tempfile.mktemp(suffix=".png"); chart_paths.append(p7)
#     if not df.empty:
#         df["_risk"] = df.apply(lambda r: predict_cancellation(r["lead_time"],r["prev_cancels"]),axis=1)
#         rc = df["_risk"].value_counts()
#         fig7,ax7 = plt.subplots(figsize=(6,4.5)); fig7.patch.set_facecolor("#0f172a"); ax7.set_facecolor("#0f172a")
#         wedges,texts,autos = ax7.pie(rc.values,labels=rc.index,autopct="%1.1f%%",
#             colors=["#f87171","#34d399"],startangle=90,
#             wedgeprops=dict(edgecolor="#0f172a",linewidth=2))
#         for t in texts+autos: t.set_color("white")
#         ax7.set_title("AI Cancellation Risk Split",color="white",fontsize=13,pad=10)
#     else:
#         fig7,ax7 = plt.subplots(figsize=(6,4.5)); fig7.patch.set_facecolor("#0f172a")
#         ax7.text(0.5,0.5,"No data",ha="center",color="white",transform=ax7.transAxes)
#     plt.tight_layout(); plt.savefig(p7,dpi=120,bbox_inches="tight",facecolor=fig7.get_facecolor()); plt.close(fig7)

#     # ── Chart 8: Loss & Refund Impact ──
#     p8 = tempfile.mktemp(suffix=".png"); chart_paths.append(p8)
#     fig8,ax8 = plt.subplots(figsize=(9,4)); fig8.patch.set_facecolor("#0f172a"); ax8.set_facecolor("#1e293b")
#     if not df.empty:
#         status_rev = df.groupby("status")["cost"].sum()
#         ax8.bar(status_rev.index,status_rev.values,
#                 color=["#f87171" if s in ["Cancelled","Refunded"] else "#34d399" for s in status_rev.index],
#                 edgecolor="#0f172a")
#         for i,(s,v) in enumerate(zip(status_rev.index,status_rev.values)):
#             ax8.text(i,v+200,f"R{v:,.0f}",ha="center",color="white",fontsize=9)
#     else:
#         ax8.text(0.5,0.5,"No data",ha="center",color="white",transform=ax8.transAxes)
#     ax8.set_title("Revenue by Booking Status (Loss Analysis)",color="white",fontsize=13,pad=10)
#     ax8.set_ylabel("Revenue (ZAR)",color="white"); ax8.tick_params(colors="white"); ax8.spines[:].set_color("#334155")
#     plt.tight_layout(); plt.savefig(p8,dpi=120,bbox_inches="tight",facecolor=fig8.get_facecolor()); plt.close(fig8)

#     # ════════════════════════════════
#     # BUILD PDF
#     # ════════════════════════════════
#     pdf = FPDF()
#     pdf.set_auto_page_break(auto=True, margin=15)

#     def section_title(text):
#         pdf.set_font("Arial","B",14); pdf.set_fill_color(30,41,59)
#         pdf.set_text_color(255,110,64); pdf.cell(0,10,safe(text),ln=True,fill=True)
#         pdf.set_text_color(30,30,30); pdf.ln(2)

#     def body_text(text):
#         pdf.set_font("Arial","",10); pdf.set_text_color(40,40,40)
#         pdf.multi_cell(0,6,safe(text)); pdf.ln(2)

#     def insight_box(lines):
#         pdf.set_font("Arial","I",9); pdf.set_text_color(60,60,120)
#         for line in lines: pdf.cell(0,6,safe(f"  {line}"),ln=True)
#         pdf.set_text_color(40,40,40); pdf.ln(3)

#     def add_chart(path, w=180):
#         if os.path.exists(path): pdf.image(path,x=15,w=w)
#         pdf.ln(3)

#     # ─────────────────────────────────────
#     # PAGE 1 — COVER
#     # ─────────────────────────────────────
#     pdf.add_page()
#     pdf.set_fill_color(15,23,42); pdf.rect(0,0,210,297,"F")
#     pdf.set_y(55); pdf.set_font("Arial","B",28); pdf.set_text_color(255,110,64)
#     pdf.cell(0,14,safe("AI SMART TOURISM ZA"),ln=True,align="C")
#     pdf.set_font("Arial","B",16); pdf.set_text_color(255,255,255)
#     pdf.cell(0,10,safe("Full Executive Analytics Report"),ln=True,align="C")
#     pdf.ln(5); pdf.set_font("Arial","",11); pdf.set_text_color(148,163,184)
#     pdf.cell(0,8,safe(f"Generated: {datetime.now().strftime('%d %B %Y  |  %H:%M')}"),ln=True,align="C")
#     pdf.cell(0,8,safe("RandomForest AI  |  Sentiment Engine  |  Dynamic Pricing  |  Risk Analysis"),ln=True,align="C")
#     pdf.ln(14); pdf.set_font("Arial","B",12); pdf.set_text_color(56,189,248)
#     total_rev = df['cost'].sum() if not df.empty else 0
#     pred_rev = predict_revenue(max(len(df),1))
#     cancelled_rev = df[df['status']=='Cancelled']['cost'].sum() if not df.empty else 0
#     refunded_rev = df[df['status']=='Refunded']['cost'].sum() if not df.empty else 0
#     avg_sat = np.mean(reviews_data['satisfaction'])
#     for line in [
#         f"Total Bookings      :  {len(df)}",
#         f"Total Revenue       :  R{total_rev:,.2f}",
#         f"Revenue at Risk     :  R{cancelled_rev+refunded_rev:,.2f}  (Cancellations + Refunds)",
#         f"AI Revenue Forecast :  R{pred_rev:,.2f}",
#         f"Hotels Monitored    :  {len(reviews_data['hotel'])}",
#         f"Avg Satisfaction    :  {avg_sat:.2f} / 5.0",
#     ]:
#         pdf.cell(0,9,safe(line),ln=True,align="C")
#     pdf.ln(10); pdf.set_font("Arial","I",9); pdf.set_text_color(100,116,139)
#     pdf.cell(0,6,safe("CONFIDENTIAL - For internal management use only"),ln=True,align="C")

#     # ─────────────────────────────────────
#     # PAGE 2 — ONE-PAGE ANALYTICS OVERVIEW (all 8 charts, 2 per row)
#     # ─────────────────────────────────────
#     pdf.add_page()
#     pdf.set_font("Arial","B",16); pdf.set_fill_color(15,23,42); pdf.set_text_color(255,110,64)
#     pdf.cell(0,12,safe("FULL ANALYTICS OVERVIEW — ALL KEY CHARTS"),ln=True,fill=True,align="C")
#     pdf.set_text_color(30,30,30); pdf.ln(2)

#     chart_pairs = [
#         (p1,"Revenue by Hotel"),
#         (p2,"Sentiment Distribution"),
#         (p3,"Guest Satisfaction"),
#         (p4,"Occupancy Forecast"),
#         (p5,"Monthly Booking Volume"),
#         (p6,"Performance Ranking"),
#         (p7,"Cancellation Risk"),
#         (p8,"Loss & Refund Analysis"),
#     ]
#     x_positions = [10, 108]
#     row_height = 60
#     y_start = pdf.get_y()
#     for idx,(cp,ctitle) in enumerate(chart_pairs):
#         col = idx % 2
#         row = idx // 2
#         x = x_positions[col]
#         y = y_start + row * (row_height + 6)
#         if os.path.exists(cp):
#             pdf.set_xy(x, y)
#             pdf.set_font("Arial","B",7); pdf.set_text_color(255,110,64)
#             pdf.cell(90,5,safe(ctitle),ln=False)
#             pdf.set_xy(x, y+5)
#             pdf.image(cp, x=x, y=y+5, w=92)

#     pdf.set_y(y_start + 4 * (row_height + 6) + 10)
#     pdf.set_font("Arial","I",8); pdf.set_text_color(100,116,139)
#     pdf.cell(0,5,safe("All charts generated from live booking database and AI sentiment engine."),ln=True,align="C")

#     # ─────────────────────────────────────
#     # PAGE 3 — KPIs & Executive Summary
#     # ─────────────────────────────────────
#     pdf.add_page()
#     section_title("1. EXECUTIVE SUMMARY & KEY PERFORMANCE INDICATORS")
#     body_text(
#         "This report provides a comprehensive analysis of booking performance, guest sentiment, "
#         "occupancy rates, cancellation risk, revenue loss from refunds, and AI-driven revenue "
#         "forecasts across all monitored South African hotel properties."
#     )
#     best_hotel = df.groupby("hotel")["cost"].sum().idxmax() if not df.empty else "N/A"
#     best_sent = reviews_data["hotel"][int(np.argmax(reviews_data["positive"]))]
#     kpis = [
#         ("Total Bookings",          str(len(df))),
#         ("Total Revenue",           f"R{total_rev:,.2f}"),
#         ("Avg Booking Value",       f"R{df['cost'].mean():,.2f}" if not df.empty else "N/A"),
#         ("AI Revenue Forecast",     f"R{pred_rev:,.2f}"),
#         ("Revenue Lost (Cancel)",   f"R{cancelled_rev:,.2f}"),
#         ("Revenue Lost (Refunds)",  f"R{refunded_rev:,.2f}"),
#         ("Top Performing Hotel",    best_hotel),
#         ("Avg Guest Satisfaction",  f"{avg_sat:.2f} / 5.0"),
#         ("Highest Sentiment Hotel", best_sent),
#     ]
#     pdf.set_font("Arial","",10)
#     for k,v in kpis:
#         pdf.set_font("Arial","B",10); pdf.set_text_color(255,110,64)
#         pdf.cell(75,7,safe(k),border=0)
#         pdf.set_font("Arial","",10); pdf.set_text_color(40,40,40)
#         pdf.cell(0,7,safe(v),ln=True,border=0)
#     pdf.ln(4)

#     # ─────────────────────────────────────
#     # PAGE 4 — Revenue Analysis
#     # ─────────────────────────────────────
#     pdf.add_page()
#     section_title("2. REVENUE ANALYSIS BY HOTEL")
#     add_chart(p1)
#     if not df.empty:
#         rbh = df.groupby("hotel")["cost"].sum().sort_values(ascending=False)
#         body_text(f"'{rbh.index[0]}' leads with R{rbh.iloc[0]:,.2f}. "
#                   f"'{rbh.index[-1]}' recorded the lowest at R{rbh.iloc[-1]:,.2f}. "
#                   f"Variance of R{rbh.iloc[0]-rbh.iloc[-1]:,.2f} signals targeted pricing opportunity.")
#     insight_box(["* Dynamic Pricing can lift revenue 15-30% in peak periods.",
#                  "* Focus upsells on top-booking hotels for maximum yield."])

#     section_title("3. REVENUE LOSS — CANCELLATIONS & REFUNDS")
#     add_chart(p8)
#     body_text(f"Total revenue at risk from cancellations: R{cancelled_rev:,.2f}. "
#               f"Refunds issued: R{refunded_rev:,.2f}. "
#               f"Combined loss exposure: R{cancelled_rev+refunded_rev:,.2f}. "
#               "Implement non-refundable rate policies and AI-triggered retention emails to reduce exposure.")
#     insight_box(["* Non-refundable rates reduce cancellation losses by up to 40%.",
#                  "* AI reminder sequences cut cancellations by ~22%."])

#     # ─────────────────────────────────────
#     # PAGE 5 — Sentiment + Satisfaction
#     # ─────────────────────────────────────
#     pdf.add_page()
#     section_title("4. GUEST SENTIMENT ANALYSIS")
#     add_chart(p2)
#     bpi = int(np.argmax(reviews_data["positive"]))
#     wni = int(np.argmax(reviews_data["negative"]))
#     body_text(f"'{reviews_data['hotel'][bpi]}' leads positive sentiment at {reviews_data['positive'][bpi]}%. "
#               f"'{reviews_data['hotel'][wni]}' carries the most negative reviews ({reviews_data['negative'][wni]}%) — immediate service audit recommended.")
#     insight_box(["* Properties >10% negative reviews need immediate intervention.",
#                  "* Positive sentiment >85% strongly predicts repeat bookings."])

#     section_title("5. GUEST SATISFACTION RATINGS")
#     add_chart(p3)
#     bsi = int(np.argmax(reviews_data["satisfaction"]))
#     wsi = int(np.argmin(reviews_data["satisfaction"]))
#     body_text(f"'{reviews_data['hotel'][bsi]}' scores {reviews_data['satisfaction'][bsi]:.1f}/5.0 — use as the group benchmark. "
#               f"'{reviews_data['hotel'][wsi]}' at {reviews_data['satisfaction'][wsi]:.1f}/5.0 requires staff training programmes.")
#     insight_box(["* +0.1 satisfaction point = ~8% more repeat bookings.",
#                  "* Scores above 4.5 support a 10-15% price premium."])

#     # ─────────────────────────────────────
#     # PAGE 6 — Occupancy + Booking Volume
#     # ─────────────────────────────────────
#     pdf.add_page()
#     section_title("6. OCCUPANCY FORECAST")
#     add_chart(p4)
#     occ_vals = reviews_data.get("occupancy",[75,82,91,68,88])
#     above80 = [reviews_data["hotel"][i] for i,o in enumerate(occ_vals) if o>=80]
#     below80 = [reviews_data["hotel"][i] for i,o in enumerate(occ_vals) if o<80]
#     body_text(f"Above 80% threshold (optimal): {', '.join(above80) or 'None'}. "
#               f"Below 80% (needs attention): {', '.join(below80) or 'None'}. "
#               "Activate AI Dynamic Pricing for above-threshold properties; deploy promotions for below.")
#     insight_box(["* Above 80%: apply yield management to capture max RevPAR.",
#                  "* Below 70%: deploy last-minute deals and corporate packages."])

#     section_title("7. MONTHLY BOOKING VOLUME TREND")
#     add_chart(p5)
#     body_text("Peak volumes align with SA school holidays (Dec, Jan, Jul). "
#               "Increase rates 20-30% during peaks. Run shoulder-season packages in May-June.")

#     # ─────────────────────────────────────
#     # PAGE 7 — Performance Ranking + Cancellation Risk
#     # ─────────────────────────────────────
#     pdf.add_page()
#     section_title("8. HOTEL PERFORMANCE RANKING")
#     add_chart(p6)
#     ranked = rank_hotels(hotels_df, df if not df.empty else pd.DataFrame())
#     pdf.set_font("Arial","B",9); pdf.set_fill_color(30,41,59); pdf.set_text_color(255,255,255)
#     for col,w in zip(["Hotel","Score","Tier","Cancel Rate","Occupancy"],[55,22,35,28,28]):
#         pdf.cell(w,7,safe(col),fill=True,border=1)
#     pdf.ln()
#     pdf.set_font("Arial","",8)
#     for _,row in ranked.iterrows():
#         pdf.set_text_color(200,120,0) if "Top" in row["Tier"] else (
#             pdf.set_text_color(60,60,60) if "Average" in row["Tier"] else pdf.set_text_color(180,0,0))
#         for v,w in zip([row["Hotel"],str(row["Score"]),row["Tier"],f"{row['Cancel Rate']}%",f"{row['Occupancy']}%"],[55,22,35,28,28]):
#             pdf.cell(w,6,safe(str(v)[:22]),border=1)
#         pdf.ln()
#     pdf.set_text_color(40,40,40); pdf.ln(3)
#     insight_box(["* Top Performers: expand marketing, raise rates.",
#                  "* Underperforming: audit operations, pricing, and guest experience."])

#     section_title("9. AI CANCELLATION RISK ANALYSIS")
#     add_chart(p7, w=100)
#     if not df.empty and "_risk" in df.columns:
#         rc2 = df["_risk"].value_counts()
#         hr = rc2.get("High Risk",0); lr = rc2.get("Low Risk",0)
#         body_text(f"High Risk: {hr} bookings ({hr/len(df)*100:.1f}%). Low Risk: {lr} bookings ({lr/len(df)*100:.1f}%). "
#                   "Apply non-refundable rate policies and personalised outreach for high-risk bookings. "
#                   "Focus upselling on low-risk committed guests.")

#     # ─────────────────────────────────────
#     # PAGE 8 — Strategic Recommendations
#     # ─────────────────────────────────────
#     pdf.add_page()
#     section_title("10. AI STRATEGIC RECOMMENDATIONS & CONCLUSIONS")
#     recs = [
#         ("Revenue Optimisation", f"Deploy AI Dynamic Pricing. Forecast: R{pred_rev:,.2f}. Focus yield on Dec, Jan, Jul peaks."),
#         ("Loss Recovery", f"R{cancelled_rev+refunded_rev:,.2f} lost to cancellations/refunds. Enforce non-refundable tiers and AI retention flows."),
#         ("Sentiment & Quality", f"Properties >10% negative sentiment need service audits. Benchmark against '{best_sent}'."),
#         ("Underperformers", "Bottom-ranked hotels should review pricing, amenities, and marketing spend urgently."),
#         ("Occupancy Management", "Properties <70% occupancy: launch mid-week corporate packages and shoulder-season deals."),
#         ("Data Quality", "Capture email and satisfaction ratings on every booking to improve AI model accuracy over time."),
#     ]
#     for i,(title,text) in enumerate(recs,1):
#         pdf.set_font("Arial","B",10); pdf.set_text_color(255,110,64)
#         pdf.cell(0,8,safe(f"{i}. {title}"),ln=True)
#         pdf.set_font("Arial","",9); pdf.set_text_color(40,40,40)
#         pdf.multi_cell(0,6,safe(text)); pdf.ln(2)

#     body_text(
#         "The AI Smart Tourism platform delivers measurable value through data-driven booking management, "
#         "real-time sentiment monitoring, cancellation risk prediction, and revenue forecasting. "
#         "Review this report monthly and act on the recommendations above to maximise revenue and guest satisfaction."
#     )
#     pdf.set_y(-20); pdf.set_font("Arial","I",8); pdf.set_text_color(130,130,130)
#     pdf.cell(0,6,safe(f"AI Smart Tourism ZA  |  Confidential  |  {datetime.now().strftime('%d %B %Y')}"),ln=True,align="C")

#     # report_path = "/tmp/AI_Hotel_Business_Report.pdf"
#     # pdf.output(report_path)
#     # for p in chart_paths:
#     #     try: os.remove(p)
#     #     except: pass
#     # return report_path



#     report_path = os.path.join(tempfile.gettempdir(), "AI_Hotel_Business_Report.pdf")
#     pdf.output(report_path)

#     for p in chart_paths:
#         try:
#             os.remove(p)
#         except:
#             pass

#     return report_path

# # ======================================================
# # MAIN APP
# # ======================================================

# def main():
#     apply_styles()
#     init_db()
#     hotels = get_hotels()

#     # ── Sidebar ──
#     st.sidebar.title("🌍 AI Tourism ZA")
#     amount = st.sidebar.number_input("Amount in ZAR", value=1000)
#     currency = st.sidebar.selectbox("Convert To", ["USD","EUR","GBP"])
#     rates = {"USD":0.053,"EUR":0.049,"GBP":0.042}
#     st.sidebar.success(f"≈ {amount*rates[currency]:.2f} {currency}")

#     if "role" not in st.session_state:
#         st.session_state.role = None

#     # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#     # LOGIN
#     # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#     if st.session_state.role is None:
#         st.markdown("""
#         <div class='hero'>
#             <h1 style='font-size:2.2rem;'>🌍 Smart Tourism & Hospitality Platform</h1>
#             <p style='color:#94a3b8;font-size:1.1rem;'>Enterprise Solution for Smart Tourism Analytics</p>
#         </div>""", unsafe_allow_html=True)
#         col1,col2 = st.columns(2)
#         with col1:
#             role = st.selectbox("Login As", ["Tourist","Hotel Manager","Admin"])
#             user = st.text_input("Username")
#             password = st.text_input("Password", type="password")
#             if st.button("Login"):
#                 st.session_state.role = role
#                 st.session_state.user = user
#                 st.rerun()
#         with col2:
#             st.image("https://images.unsplash.com/photo-1507525428034-b723cf961d3e")

#     # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#     # TOURIST
#     # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#     elif st.session_state.role == "Tourist":
#         st.title(f"✈️ Welcome, {st.session_state.user}")
#         c1,c2,c3 = st.columns(3)
#         c1.metric("Available Hotels",120); c2.metric("Destinations",24); c3.metric("Satisfaction","94%")

#         tabs = st.tabs(["🏨 Bookings","🌦️ Weather","🤖 AI Recs","⚖️ Compare Hotels","🗺️ Itinerary","💬 Chatbot","😊 Reviews","📷 Landmarks"])

#         with tabs[0]:
#             st.subheader("🏨 Smart Hotel Booking System")
#             check_in = st.date_input("Check-in")
#             check_out = st.date_input("Check-out")
#             tourist_budget = st.slider("Budget (ZAR)",1000,10000,3000,step=500)
#             selected_city = st.selectbox("Destination",["Cape Town","Johannesburg","Durban","Kruger Park","Stellenbosch"])
#             filtered_hotels = hotels[(hotels["price"]<=tourist_budget)&(hotels["city"]==selected_city)]
#             st.success(f"Found {len(filtered_hotels)} hotel(s) in budget")
#             for _,row in filtered_hotels.iterrows():
#                 st.markdown("<div class='metric-card'>",unsafe_allow_html=True)
#                 col1,col2 = st.columns([3,1])
#                 with col1:
#                     st.subheader(row['name'])
#                     st.write(f"📍 {row['city']}  |  💰 R{row['price']}  |  ⭐ {row['rating']}  |  🏷️ {row['type']}")
#                 with col2:
#                     if st.button("View",key=f"v_{row['name']}"):
#                         st.image(row['image'],use_container_width=True)
#                     if st.button("Book Now",key=f"b_{row['name']}"):
#                         save_booking(st.session_state.user,row['name'],row['city'],row['price'])
#                         st.success(f"✅ Booked {row['name']}")
#                 st.markdown("</div>",unsafe_allow_html=True)
#             st.subheader("🗺️ Hotel Locations")
#             hmap = folium.Map(location=[-30.5595,22.9375],zoom_start=5)
#             folium.Marker([-33.9249,18.4241],tooltip="Cape Sun Resort").add_to(hmap)
#             folium.Marker([-26.2041,28.0473],tooltip="Sandton Palace").add_to(hmap)
#             folium.Marker([-29.8587,31.0218],tooltip="Durban Escape").add_to(hmap)
#             st_folium(hmap,width=900)

#         with tabs[1]:
#             city = st.selectbox("Destination",["Cape Town","Johannesburg","Durban","Kruger Park"])
#             w = get_weather(city)
#             st.info(f"{city}: {w['temp']} | {w['condition']}")

#         with tabs[2]:
#             st.subheader("🧠 Hotel Recommendations")
#             budget = st.slider("Budget",1000,10000,3000,step=500)
#             travel_type = st.selectbox("Experience",["Luxury","Business","Beach","Safari"])
#             preferred_city = st.selectbox("Area",["Cape Town","Johannesburg","Durban","Kruger Park","Stellenbosch"])
#             rec = ai_recommend_hotels(hotels,budget,travel_type)
#             rec = rec[rec['city']==preferred_city]
#             for _,h in rec.iterrows():
#                 with st.expander(f"🏨 {h['name']} - R{h['price']}"):
#                     st.image(h['image'],use_container_width=True)
#                     st.write(f"📍 {h['city']}  |  ⭐ {h['rating']}  |  🏷️ {h['type']}")

#         with tabs[3]:
#             st.subheader("⚖️ Compare Hotels")
#             sel = st.multiselect("Select Hotels",hotels['name'].tolist())
#             if len(sel)>=2:
#                 cdf = hotels[hotels['name'].isin(sel)][['name','price','rating','city','type','occupancy','sentiment_score','amenities']]
#                 st.dataframe(cdf,use_container_width=True)
#                 st.plotly_chart(px.bar(cdf,x='name',y='rating',color='name',title="Rating Comparison"),use_container_width=True)
#             else: st.warning("Select at least 2 hotels")

#         with tabs[4]:
#             st.subheader("🗺️ Travel Planner")
#             if st.button("Generate Itinerary"):
#                 st.table(pd.DataFrame({"Day":[1,2,3],"Activity":["City Tour & Dining","Adventure & Nature","Beach Relaxation"]}))

#         with tabs[5]:
#             st.subheader("💬 Tourism Assistant")
#             prompt = st.chat_input("Ask the AI travel assistant...")
#             if prompt:
#                 st.chat_message("user").write(prompt)
#                 st.chat_message("assistant").write("I recommend Cape Town for luxury and Durban for beach tourism.")

#         with tabs[6]:
#             st.subheader("😊 Review Analysis")
#             review = st.text_area("Write Your Review")
#             if st.button("Analyze"):
#                 sentiment,polarity = analyze_sentiment(review)
#                 st.success(f"Sentiment: {sentiment}")
#                 st.plotly_chart(px.bar(x=["Score"],y=[polarity],title="Sentiment"),use_container_width=True)
#                 if review.strip():
#                     wc = WordCloud(width=800,height=400).generate(review)
#                     fig,ax = plt.subplots(); ax.imshow(wc); ax.axis("off"); st.pyplot(fig); plt.close(fig)

#         with tabs[7]:
#             st.subheader("📷 Landmark Recognition")
#             uf = st.file_uploader("Upload Photo",type=['jpg','png','jpeg'])
#             if uf:
#                 st.image(Image.open(uf),use_container_width=True)
#                 st.success("✅ Detection Complete")
#                 lm = st.selectbox("Detected",["Table Mountain","V&A Waterfront","Kruger National Park","Durban Beachfront"])
#                 if lm == "Table Mountain":
#                     st.info("🌍 Table Mountain"); st.write("Hotels: Cape Sun, Winelands Luxury"); st.write("Activities: Cable Car, Hiking, Helicopter Tours")
#                 elif lm == "Kruger National Park":
#                     st.info("🦁 Kruger National Park"); st.write("Hotels: Kruger Safari Lodge"); st.write("Activities: Safari Drives, Wildlife Photography")

#     # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#     # HOTEL MANAGER
#     # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#     elif st.session_state.role == "Hotel Manager":
#         st.title("📊 Hotel Business Intelligence Console")
#         conn = sqlite3.connect("tourism_ai.db")
#         df = pd.read_sql("SELECT * FROM bookings",conn)
#         conn.close()

#         reviews_data = {
#             "hotel":["Cape Sun Resort","Sandton Palace","Durban Escape","Kruger Safari Lodge","Winelands Luxury Hotel"],
#             "positive":[85,74,90,95,88],"neutral":[10,15,6,3,8],"negative":[5,11,4,2,4],
#             "satisfaction":[4.6,4.2,4.8,4.9,4.7],"occupancy":[85,78,70,95,82],
#         }

#         if not df.empty:
#             c1,c2,c3,c4 = st.columns(4)
#             c1.metric("💰 Revenue",f"R{df['cost'].sum():,.2f}")
#             c2.metric("📅 Bookings",len(df))
#             c3.metric("❌ Cancellations",len(df[df['status']=='Cancelled']))
#             c4.metric("🔄 Refunds",len(df[df['status']=='Refunded']))

#         mgr_tabs = st.tabs(["📈 Dashboard","🔍 Booking Management","🚩 Flagged Bookings","💡 Dynamic Pricing","📄 Report"])

#         # ── Manager Tab 0: Dashboard ──
#         with mgr_tabs[0]:
#             if not df.empty:
#                 st.plotly_chart(px.histogram(df,x="hotel",y="cost",color="hotel",title="Revenue by Hotel"),use_container_width=True)
#                 combo = make_subplots(specs=[[{"secondary_y":True}]])
#                 combo.add_trace(go.Bar(x=reviews_data["hotel"],y=reviews_data["positive"],name="Positive %",marker_color='green'),secondary_y=False)
#                 combo.add_trace(go.Bar(x=reviews_data["hotel"],y=reviews_data["negative"],name="Negative %",marker_color='red'),secondary_y=False)
#                 combo.add_trace(go.Scatter(x=reviews_data["hotel"],y=reviews_data["satisfaction"],name="Satisfaction",mode="lines+markers",line=dict(color="cyan",width=3)),secondary_y=True)
#                 combo.update_layout(title="Sentiment & Satisfaction",template="plotly_dark",height=450,legend=dict(orientation="h"))
#                 st.plotly_chart(combo,use_container_width=True)

#                 # Cancellation risk on this hotel's bookings
#                 st.subheader("🤖 Risk Assessment")
#                 df["risk"] = df.apply(lambda r: predict_cancellation(r["lead_time"],r["prev_cancels"]),axis=1)
#                 risk_counts = df["risk"].value_counts().reset_index()
#                 risk_counts.columns=["Risk","Count"]
#                 st.plotly_chart(px.pie(risk_counts,names="Risk",values="Count",color="Risk",
#                     color_discrete_map={"High Risk":"#f87171","Low Risk":"#34d399"},title="Cancellation Risk Split"),use_container_width=True)
#             else:
#                 st.warning("No bookings yet. Ask a tourist to book first.")

#         # ── Manager Tab 1: Booking Management ──
#         with mgr_tabs[1]:
#             st.subheader("🔍 Booking Management Panel")
#             if not df.empty:
#                 # Search & Filter
#                 col1,col2,col3 = st.columns(3)
#                 search_user = col1.text_input("Search by User")
#                 search_hotel = col2.selectbox("Filter by Hotel",["All"]+hotels['name'].tolist())
#                 risk_filter = col3.selectbox("Filter by AI Risk",["All","High Risk","Low Risk"])

#                 filtered = df.copy()
#                 if not df.empty:
#                     filtered["risk"] = filtered.apply(lambda r: predict_cancellation(r["lead_time"],r["prev_cancels"]),axis=1)
#                 if search_user: filtered = filtered[filtered['user'].str.contains(search_user,case=False,na=False)]
#                 if search_hotel != "All": filtered = filtered[filtered['hotel']==search_hotel]
#                 if risk_filter != "All": filtered = filtered[filtered['risk']==risk_filter]

#                 st.write(f"Showing **{len(filtered)}** bookings")

#                 # Booking History per Hotel
#                 if search_hotel != "All":
#                     hotel_hist = df[df['hotel']==search_hotel]
#                     st.subheader(f"📊 Booking History — {search_hotel}")
#                     rev = hotel_hist['cost'].sum()
#                     canc = len(hotel_hist[hotel_hist['status']=='Cancelled'])
#                     st.write(f"Total Revenue: **R{rev:,.2f}**  |  Cancellations: **{canc}**  |  Total Bookings: **{len(hotel_hist)}**")

#                 # Display filtered bookings
#                 for _,row in filtered.iterrows():
#                     risk_label = row.get("risk","N/A") if "risk" in filtered.columns else "N/A"
#                     status_color = "🔴" if row['status']=='Cancelled' else ("🟡" if row['status']=='Refunded' else "🟢")
#                     risk_color = "🔴" if risk_label=="High Risk" else "🟢"
#                     st.markdown("<div class='metric-card'>",unsafe_allow_html=True)
#                     cc1,cc2,cc3 = st.columns([4,3,3])
#                     with cc1:
#                         st.write(f"**#{row['id']}** | {status_color} {row['status']} | 👤 {row['user']}")
#                         st.write(f"🏨 {row['hotel']}  •  📍 {row['city']}  •  💰 R{row['cost']:,.0f}")
#                         st.write(f"🗓️ {str(row['booking_date'])[:19]}  •  {risk_color} AI Risk: {risk_label}")
#                         if row.get('flagged',0)==1:
#                             st.markdown(f"<div class='flag-card'>🚩 Flagged: {row.get('flag_reason','')}</div>",unsafe_allow_html=True)
#                     with cc2:
#                         if row['status']=='Active':
#                             if st.button("🚩 Flag Suspicious",key=f"flag_{row['id']}"):
#                                 flag_booking(row['id'],"Flagged by Hotel Manager")
#                                 st.rerun()
#                     with cc3:
#                         st.write(f"Lead Time: {row['lead_time']} days | Prior Cancels: {row['prev_cancels']}")
#                     st.markdown("</div>",unsafe_allow_html=True)
#             else:
#                 st.warning("No bookings yet.")

#         # ── Manager Tab 2: Flagged Bookings ──
#         with mgr_tabs[2]:
#             st.subheader("🚩 Suspicious / Flagged Bookings")
#             if not df.empty:
#                 flagged_df = df[df.get('flagged',pd.Series([0]*len(df)))==1] if 'flagged' in df.columns else pd.DataFrame()
#                 if not flagged_df.empty:
#                     for _,row in flagged_df.iterrows():
#                         st.markdown("<div class='rank-danger'>",unsafe_allow_html=True)
#                         c1,c2 = st.columns([4,2])
#                         with c1:
#                             st.write(f"**#{row['id']}** | 👤 {row['user']} | 🏨 {row['hotel']}")
#                             st.write(f"💰 R{row['cost']:,.0f}  |  🗓️ {str(row['booking_date'])[:19]}")
#                             st.write(f"🚩 Reason: {row.get('flag_reason','Unknown')}")
#                         with c2:
#                             if st.button("✅ Clear Flag",key=f"clr_{row['id']}"):
#                                 unflag_booking(row['id']); st.rerun()
#                         st.markdown("</div>",unsafe_allow_html=True)
#                 else:
#                     st.success("No flagged bookings. All looks clean!")
#             else:
#                 st.info("No booking data yet.")

#         # ── Manager Tab 3: Dynamic Pricing ──
#         with mgr_tabs[3]:
#             st.subheader("💡 Dynamic Pricing Tool")
#             p1i,p2i,p3i = st.columns(3)
#             base_price = p1i.number_input("Base Price (ZAR)",1000,10000,3000,step=100)
#             demand_lvl = p2i.selectbox("Demand",["Low","Medium","High"])
#             occ_pct = p3i.slider("Occupancy %",0,100,75)
#             s1i,s2i,s3i = st.columns(3)
#             season_t = s1i.selectbox("Season",["Off-Peak","Mid","Peak"])
#             is_holiday = s2i.checkbox("Public Holiday?")
#             weather_n = s3i.selectbox("Weather",["Sunny ☀️","Cloudy ☁️","Rainy 🌧️","Humid 🌤️"])
#             ai_price = dynamic_hotel_price(base_price,demand_lvl,occ_pct,season_t,is_holiday,weather_n)
#             st.success(f"🤖 Recommended Price: **R{ai_price:,.2f}** (base R{base_price:,}  →  {((ai_price-base_price)/base_price*100):+.1f}%)")

#         # ── Manager Tab 4: Report ──
#         with mgr_tabs[4]:
#             st.subheader("📄 Executive Business Report")
#             if not df.empty:
#                 if st.button("Generate Full Report (PDF)"):
#                     with st.spinner("Building PDF with all charts and analysis..."):
#                         rfile = generate_detailed_report(df, reviews_data, hotels)
#                     if os.path.exists(rfile):
#                         st.success("✅ Report ready — 8 pages including one-page analytics overview")
#                         with open(rfile,"rb") as f:
#                             st.download_button("⬇️ Download Business Report (PDF)",data=f,file_name="AI_Hotel_Business_Report.pdf",mime="application/pdf")
#             else:
#                 st.warning("No booking data yet. Report unavailable.")

#     # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#     # ADMIN
#     # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#     elif st.session_state.role == "Admin":
#         st.title("🛡️ Admin Control Center")
#         conn = sqlite3.connect("tourism_ai.db")
#         df = pd.read_sql("SELECT * FROM bookings",conn)
#         conn.close()

#         reviews_data = {
#             "hotel":["Cape Sun Resort","Sandton Palace","Durban Escape","Kruger Safari Lodge","Winelands Luxury Hotel"],
#             "positive":[85,74,90,95,88],"neutral":[10,15,6,3,8],"negative":[5,11,4,2,4],
#             "satisfaction":[4.6,4.2,4.8,4.9,4.7],"occupancy":[85,78,70,95,82],
#         }

#         # ── Admin KPIs ──
#         total_rev = df['cost'].sum() if not df.empty else 0
#         cancelled_rev = df[df['status']=='Cancelled']['cost'].sum() if not df.empty else 0
#         refunded_rev = df[df['status']=='Refunded']['cost'].sum() if not df.empty else 0
#         active_rev = df[df['status']=='Active']['cost'].sum() if not df.empty else 0
#         high_risk = 0
#         if not df.empty:
#             df["risk"] = df.apply(lambda r: predict_cancellation(r["lead_time"],r["prev_cancels"]),axis=1)
#             high_risk = len(df[df["risk"]=="High Risk"])

#         k1,k2,k3,k4,k5,k6 = st.columns(6)
#         k1.metric("Total Bookings",len(df))
#         k2.metric("Active Revenue",f"R{active_rev:,.0f}")
#         k3.metric("Revenue Lost",f"R{cancelled_rev+refunded_rev:,.0f}")
#         k4.metric("Cancellations",len(df[df['status']=='Cancelled']) if not df.empty else 0)
#         k5.metric("Refunds",len(df[df['status']=='Refunded']) if not df.empty else 0)
#         k6.metric("High Risk",high_risk)

#         admin_tabs = st.tabs([
#             "📊 Analytics Overview",
#             "🎛️ Booking Control",
#             "🏆 Performance Ranking",
#             "💸 Loss & Risk Analysis",
#             "📄 Full Report"
#         ])

#         # ── Admin Tab 0: Analytics Overview ──
#         with admin_tabs[0]:
#             st.subheader("📊 Platform Analytics Overview")
#             if not df.empty:
#                 col1,col2 = st.columns(2)
#                 with col1:
#                     st.plotly_chart(px.histogram(df,x="hotel",y="cost",color="hotel",title="Revenue by Hotel",template="plotly_dark"),use_container_width=True)
#                     st.plotly_chart(px.pie(df,names="city",title="Bookings by City",template="plotly_dark"),use_container_width=True)
#                 with col2:
#                     st.plotly_chart(px.bar(
#                         pd.DataFrame({"Hotel":reviews_data["hotel"],"Positive":reviews_data["positive"],"Negative":reviews_data["negative"],"Neutral":reviews_data["neutral"]}),
#                         x="Hotel",y=["Positive","Negative","Neutral"],title="Sentiment Distribution",template="plotly_dark",barmode="stack"
#                     ),use_container_width=True)
#                     occ_df = pd.DataFrame({"Hotel":reviews_data["hotel"],"Occupancy":reviews_data["occupancy"]})
#                     fig_occ = px.bar(occ_df,x="Hotel",y="Occupancy",title="Occupancy by Hotel",template="plotly_dark",
#                                      color="Occupancy",color_continuous_scale=["red","yellow","green"])
#                     fig_occ.add_hline(y=80,line_dash="dash",line_color="orange",annotation_text="80% threshold")
#                     st.plotly_chart(fig_occ,use_container_width=True)

#                 st.subheader("📅 Bookings Calendar")
#                 st.dataframe(df[['id','user','hotel','city','cost','booking_date','status']].sort_values('booking_date',ascending=False),use_container_width=True)
#             else:
#                 st.warning("No booking data yet.")

#         # ── Admin Tab 1: Booking Control Panel ──
#         with admin_tabs[1]:
#             st.subheader("🎛️ Admin Booking Control Panel")
#             if not df.empty:
#                 search = st.text_input("🔍 Search by ID, User, or Hotel")
#                 status_f = st.selectbox("Filter Status",["All","Active","Cancelled","Refunded"])
#                 display_df = df.copy()
#                 if search:
#                     display_df = display_df[
#                         display_df['user'].str.contains(search,case=False,na=False) |
#                         display_df['hotel'].str.contains(search,case=False,na=False) |
#                         display_df['id'].astype(str).str.contains(search)
#                     ]
#                 if status_f != "All":
#                     display_df = display_df[display_df['status']==status_f]

#                 st.write(f"Showing **{len(display_df)}** bookings")
#                 for _,row in display_df.iterrows():
#                     status_icon = "🟢" if row['status']=='Active' else ("🔴" if row['status']=='Cancelled' else "🟡")
#                     risk_label = row.get("risk","N/A") if "risk" in df.columns else "N/A"
#                     risk_icon = "🔴" if risk_label=="High Risk" else "🟢"
#                     st.markdown("<div class='metric-card'>",unsafe_allow_html=True)
#                     c1,c2,c3,c4 = st.columns([4,2,2,2])
#                     with c1:
#                         st.write(f"**Booking #{row['id']}** {status_icon} {row['status']}")
#                         st.write(f"👤 **{row['user']}**  |  🏨 {row['hotel']}  |  📍 {row['city']}")
#                         st.write(f"💰 R{row['cost']:,.2f}  |  {risk_icon} {risk_label}  |  📅 {str(row['booking_date'])[:19]}")
#                         if row.get('flagged',0)==1:
#                             st.markdown(f"<div class='flag-card'>🚩 {row.get('flag_reason','')}</div>",unsafe_allow_html=True)

#                     with c2:
#                         if row['status']=='Active':
#                             if st.button("❌ Cancel",key=f"ac_{row['id']}"):
#                                 cancel_booking(row['id']); st.success(f"Cancelled #{row['id']}"); st.rerun()
#                         if row['status'] in ['Active','Cancelled'] and not row.get('refunded',0):
#                             if st.button("💸 Refund",key=f"ar_{row['id']}"):
#                                 refund_booking(row['id']); st.success(f"Refunded #{row['id']}"); st.rerun()

#                     with c3:
#                         # Reassign
#                         if row['status']=='Active':
#                             new_h = st.selectbox("Reassign to",["—"]+hotels['name'].tolist(),key=f"rs_{row['id']}")
#                             if new_h != "—":
#                                 new_hotel_row = hotels[hotels['name']==new_h].iloc[0]
#                                 if st.button("🔁 Reassign",key=f"rsbtn_{row['id']}"):
#                                     reassign_booking(row['id'],new_h,new_hotel_row['city'],new_hotel_row['price'])
#                                     st.success(f"Reassigned #{row['id']} to {new_h}"); st.rerun()

#                     with c4:
#                         # Edit
#                         with st.expander("✏️ Edit"):
#                             new_user = st.text_input("User",value=row['user'],key=f"eu_{row['id']}")
#                             new_cost = st.number_input("Cost (ZAR)",value=float(row['cost']),key=f"ec_{row['id']}")
#                             if st.button("Save",key=f"esv_{row['id']}"):
#                                 edit_booking(row['id'],new_user,row['hotel'],row['city'],new_cost)
#                                 st.success("Updated"); st.rerun()
#                         if row.get('flagged',0)==0:
#                             if st.button("🚩 Flag",key=f"flg_{row['id']}"):
#                                 flag_booking(row['id'],"Flagged by Admin"); st.rerun()
#                         else:
#                             if st.button("✅ Unflag",key=f"uflg_{row['id']}"):
#                                 unflag_booking(row['id']); st.rerun()
#                     st.markdown("</div>",unsafe_allow_html=True)
#             else:
#                 st.warning("No booking data yet.")

#         # ── Admin Tab 2: Performance Ranking ──
#         with admin_tabs[2]:
#             st.subheader("🏆 Hotel Performance Ranking System")
#             ranked = rank_hotels(hotels, df if not df.empty else pd.DataFrame())

#             # Coloured rank cards
#             for i,(_,row) in enumerate(ranked.iterrows()):
#                 tier = row['Tier']
#                 card_class = "rank-gold" if "Top" in tier else ("rank-silver" if "Average" in tier else "rank-danger")
#                 st.markdown(f"<div class='{card_class}'>",unsafe_allow_html=True)
#                 cc1,cc2,cc3,cc4,cc5 = st.columns([1,3,2,2,2])
#                 cc1.markdown(f"### #{i+1}")
#                 cc2.write(f"**{row['Hotel']}**  •  {row['City']}")
#                 cc2.write(f"{tier}")
#                 cc3.metric("Score",row['Score'])
#                 cc4.metric("Occupancy",f"{row['Occupancy']}%")
#                 cc5.metric("Sentiment",f"{row['Sentiment']}%")
#                 st.markdown("</div>",unsafe_allow_html=True)

#             # Ranking chart
#             color_map = {"🏆 Top Performer":"#fbbf24","⚠️ Average":"#94a3b8","❌ Underperforming":"#f87171"}
#             ranked["Color"] = ranked["Tier"].map(color_map)
#             fig_rank = px.bar(ranked,x="Hotel",y="Score",color="Tier",
#                 color_discrete_map={"🏆 Top Performer":"#fbbf24","⚠️ Average":"#94a3b8","❌ Underperforming":"#f87171"},
#                 title="Hotel Performance Composite Score",template="plotly_dark",text="Score")
#             fig_rank.update_traces(textposition="outside")
#             st.plotly_chart(fig_rank,use_container_width=True)

#             # Radar-style multi-metric comparison
#             fig_multi = go.Figure()
#             for _,row in ranked.iterrows():
#                 fig_multi.add_trace(go.Bar(name=row['Hotel'],x=["Rating×20","Occupancy×0.4","Sentiment×0.3"],
#                     y=[row['Rating']*20,row['Occupancy']*0.4,row['Sentiment']*0.3]))
#             fig_multi.update_layout(barmode='group',title="Score Component Breakdown",template="plotly_dark")
#             st.plotly_chart(fig_multi,use_container_width=True)

#         # ── Admin Tab 3: Loss & Risk Analysis ──
#         with admin_tabs[3]:
#             st.subheader("💸 Revenue Loss & Risk Analysis")
#             if not df.empty:
#                 col1,col2 = st.columns(2)
#                 with col1:
#                     status_rev = df.groupby("status")["cost"].sum().reset_index()
#                     status_rev.columns=["Status","Revenue"]
#                     fig_loss = px.bar(status_rev,x="Status",y="Revenue",color="Status",
#                         color_discrete_map={"Active":"#34d399","Cancelled":"#f87171","Refunded":"#f59e0b"},
#                         title="Revenue by Booking Status",template="plotly_dark",text="Revenue")
#                     fig_loss.update_traces(texttemplate="R%{text:,.0f}",textposition="outside")
#                     st.plotly_chart(fig_loss,use_container_width=True)

#                     total_loss = cancelled_rev + refunded_rev
#                     st.markdown(f"""
#                     <div class='rank-danger'>
#                     <b>💸 Revenue Loss Summary</b><br>
#                     Cancellations: R{cancelled_rev:,.2f}<br>
#                     Refunds Issued: R{refunded_rev:,.2f}<br>
#                     <b>Total Loss: R{total_loss:,.2f}</b><br>
#                     Loss as % of Total: {total_loss/max(total_rev,1)*100:.1f}%
#                     </div>""",unsafe_allow_html=True)

#                 with col2:
#                     rc = df["risk"].value_counts().reset_index()
#                     rc.columns=["Risk","Count"]
#                     fig_risk = px.pie(rc,names="Risk",values="Count",
#                         color="Risk",color_discrete_map={"High Risk":"#f87171","Low Risk":"#34d399"},
#                         title="Cancellation Risk Split",template="plotly_dark")
#                     st.plotly_chart(fig_risk,use_container_width=True)
#                     hr_pct = high_risk/max(len(df),1)*100
#                     st.markdown(f"""
#                     <div class='{"rank-danger" if hr_pct>40 else "rank-silver"}'>
#                     <b>⚠️ High-Risk Booking Analysis</b><br>
#                     High Risk Bookings: {high_risk} ({hr_pct:.1f}%)<br>
#                     Estimated Revenue at Risk: R{df[df['risk']=='High Risk']['cost'].sum():,.2f}<br>
#                     {"🔴 CRITICAL: >40% high risk — activate retention campaign" if hr_pct>40 else "🟡 Monitor closely — apply non-refundable policies"}
#                     </div>""",unsafe_allow_html=True)

#                 # Underperforming hotels
#                 st.subheader("🔻 Underperforming Hotels — Deep Dive")
#                 ranked2 = rank_hotels(hotels, df)
#                 under = ranked2[ranked2['Tier']=="❌ Underperforming"]
#                 if not under.empty:
#                     for _,row in under.iterrows():
#                         hotel_bk = df[df['hotel']==row['Hotel']]
#                         canc_cnt = len(hotel_bk[hotel_bk['status']=='Cancelled'])
#                         st.markdown(f"""
#                         <div class='rank-danger'>
#                         <b>❌ {row['Hotel']}</b>  |  Score: {row['Score']}  |  Occupancy: {row['Occupancy']}%<br>
#                         Revenue: R{row['Revenue']:,.2f}  |  Cancellations: {canc_cnt}  |  Cancel Rate: {row['Cancel Rate']}%<br>
#                         <i>Action: Review pricing, amenities, and launch targeted promotion.</i>
#                         </div>""",unsafe_allow_html=True)
#                 else:
#                     st.success("No underperforming hotels at this time!")
#             else:
#                 st.warning("No booking data yet.")

#         # ── Admin Tab 4: Full Report ──
#         with admin_tabs[4]:
#             st.subheader("📄 Full Executive Report")
#             if not df.empty:
#                 if st.button("🚀 Generate Complete Report (PDF)"):
#                     with st.spinner("Generating 8-page report with all charts, rankings, and analysis..."):
#                         rfile = generate_detailed_report(df, reviews_data, hotels)
#                     if os.path.exists(rfile):
#                         st.success("✅ Complete 8-page report generated — includes one-page overview, all 8 charts, ranking, loss analysis, and strategic recommendations")
#                         with open(rfile,"rb") as f:
#                             st.download_button("⬇️ Download Full Report (PDF)",data=f,file_name="AI_Smart_Tourism_Full_Report.pdf",mime="application/pdf")
#             else:
#                 st.warning("No booking data yet.")

#     # ── Logout ──
#     if st.session_state.role and st.sidebar.button("Logout"):
#         st.session_state.role = None
#         st.rerun()

# if __name__ == "__main__":
#     main()




# import streamlit as st
# import pandas as pd
# import numpy as np
# import plotly.express as px
# import plotly.graph_objects as go
# import sqlite3
# import hashlib
# import requests
# import base64
# from datetime import datetime, timedelta
# from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
# from wordcloud import WordCloud
# import matplotlib
# matplotlib.use('Agg')
# import matplotlib.pyplot as plt
# from textblob import TextBlob
# from PIL import Image
# from fpdf import FPDF
# import folium
# from streamlit_folium import st_folium
# from plotly.subplots import make_subplots
# import tempfile
# import os
# import io
# import json

# # ======================================================
# # PAGE CONFIG
# # ======================================================

# st.set_page_config(
#     page_title="AI Smart Tourism ZA",
#     page_icon="🌍",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # ======================================================
# # API KEYS — Replace with your actual keys
# # ======================================================

# OPENWEATHER_API_KEY = st.secrets.get("OPENWEATHER_API_KEY", "YOUR_OPENWEATHER_KEY")
# GOOGLE_MAPS_API_KEY = st.secrets.get("GOOGLE_MAPS_API_KEY", "YOUR_GOOGLE_MAPS_KEY")
# GOOGLE_VISION_API_KEY = st.secrets.get("GOOGLE_VISION_API_KEY", "YOUR_GOOGLE_VISION_KEY")
# GOOGLE_PLACES_API_KEY = st.secrets.get("GOOGLE_PLACES_API_KEY", "YOUR_GOOGLE_PLACES_KEY")
# OPENAI_API_KEY = st.secrets.get("OPENAI_API_KEY", "YOUR_OPENAI_KEY")
# ANTHROPIC_API_KEY = st.secrets.get("ANTHROPIC_API_KEY", "YOUR_ANTHROPIC_KEY")

# # ======================================================
# # PROFESSIONAL UI STYLING
# # ======================================================

# def apply_styles():
#     st.markdown("""
#     <style>
#     @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

#     .stApp {
#         background: linear-gradient(135deg, #0a0f1e 0%, #0f172a 50%, #1a0a2e 100%);
#         color: white;
#         font-family: 'DM Sans', sans-serif;
#     }
#     h1, h2, h3, h4 {
#         font-family: 'Syne', sans-serif !important;
#         color: white !important;
#         letter-spacing: -0.02em;
#     }
#     .hero {
#         background: linear-gradient(135deg, rgba(255,110,64,0.12), rgba(56,189,248,0.08));
#         backdrop-filter: blur(20px);
#         padding: 40px;
#         border-radius: 24px;
#         text-align: center;
#         border: 1px solid rgba(255,110,64,0.2);
#         box-shadow: 0 0 60px rgba(255,110,64,0.08), 0 8px 32px rgba(0,0,0,0.4);
#         margin-bottom: 28px;
#     }
#     .metric-card {
#         background: rgba(255,255,255,0.04);
#         backdrop-filter: blur(16px);
#         border-radius: 20px;
#         padding: 22px;
#         margin-bottom: 16px;
#         border: 1px solid rgba(255,255,255,0.08);
#         transition: all 0.3s cubic-bezier(0.4,0,0.2,1);
#         box-shadow: 0 4px 24px rgba(0,0,0,0.3);
#     }
#     .metric-card:hover {
#         transform: translateY(-4px);
#         border-color: rgba(255,110,64,0.3);
#         box-shadow: 0 12px 32px rgba(255,110,64,0.15);
#     }
#     .weather-card {
#         background: linear-gradient(135deg, rgba(56,189,248,0.15), rgba(14,165,233,0.08));
#         border: 1px solid rgba(56,189,248,0.3);
#         border-radius: 20px;
#         padding: 24px;
#         margin: 12px 0;
#         text-align: center;
#     }
#     .forecast-card {
#         background: rgba(255,255,255,0.04);
#         border: 1px solid rgba(56,189,248,0.2);
#         border-radius: 14px;
#         padding: 14px;
#         text-align: center;
#         margin: 6px 0;
#     }
#     .chat-bubble-user {
#         background: linear-gradient(135deg, #ff6e40, #ff3d00);
#         border-radius: 18px 18px 4px 18px;
#         padding: 12px 18px;
#         margin: 8px 0 8px 40px;
#         color: white;
#         font-size: 0.95rem;
#     }
#     .chat-bubble-bot {
#         background: rgba(56,189,248,0.12);
#         border: 1px solid rgba(56,189,248,0.25);
#         border-radius: 18px 18px 18px 4px;
#         padding: 12px 18px;
#         margin: 8px 40px 8px 0;
#         color: white;
#         font-size: 0.95rem;
#     }
#     .landmark-card {
#         background: linear-gradient(135deg, rgba(167,139,250,0.12), rgba(139,92,246,0.06));
#         border: 1px solid rgba(167,139,250,0.3);
#         border-radius: 20px;
#         padding: 24px;
#         margin: 12px 0;
#     }
#     .hotel-image-card {
#         border-radius: 16px;
#         overflow: hidden;
#         margin-bottom: 12px;
#         border: 1px solid rgba(255,255,255,0.08);
#     }
#     .rank-gold {
#         background: linear-gradient(135deg, rgba(251,191,36,0.15), rgba(245,158,11,0.08));
#         border: 1px solid rgba(251,191,36,0.3);
#         border-radius: 16px;
#         padding: 16px 20px;
#         margin: 8px 0;
#     }
#     .rank-silver {
#         background: linear-gradient(135deg, rgba(148,163,184,0.12), rgba(100,116,139,0.06));
#         border: 1px solid rgba(148,163,184,0.25);
#         border-radius: 16px;
#         padding: 16px 20px;
#         margin: 8px 0;
#     }
#     .rank-danger {
#         background: linear-gradient(135deg, rgba(239,68,68,0.12), rgba(185,28,28,0.06));
#         border: 1px solid rgba(239,68,68,0.25);
#         border-radius: 16px;
#         padding: 16px 20px;
#         margin: 8px 0;
#     }
#     .flag-card {
#         background: rgba(239,68,68,0.1);
#         border: 1px solid rgba(239,68,68,0.3);
#         border-radius: 12px;
#         padding: 12px 16px;
#         margin: 6px 0;
#     }
#     .role-badge-tourist {
#         background: linear-gradient(135deg, #34d399, #059669);
#         padding: 4px 14px; border-radius: 20px; font-size: 0.8rem; font-weight: 600;
#     }
#     .role-badge-manager {
#         background: linear-gradient(135deg, #38bdf8, #0284c7);
#         padding: 4px 14px; border-radius: 20px; font-size: 0.8rem; font-weight: 600;
#     }
#     .role-badge-admin {
#         background: linear-gradient(135deg, #f59e0b, #d97706);
#         padding: 4px 14px; border-radius: 20px; font-size: 0.8rem; font-weight: 600;
#     }
#     .stButton>button {
#         background: linear-gradient(135deg, #ff6e40, #ff3d00);
#         color: white;
#         border: none;
#         border-radius: 12px;
#         padding: 10px 24px;
#         font-weight: 600;
#         font-family: 'DM Sans', sans-serif;
#         letter-spacing: 0.02em;
#         transition: all 0.2s;
#     }
#     .stButton>button:hover {
#         transform: translateY(-2px);
#         box-shadow: 0 6px 20px rgba(255,110,64,0.4);
#     }
#     section[data-testid="stSidebar"] {
#         background: rgba(10,15,30,0.8);
#         backdrop-filter: blur(20px);
#         border-right: 1px solid rgba(255,255,255,0.06);
#     }
#     .stTabs [data-baseweb="tab"] {
#         font-family: 'DM Sans', sans-serif;
#         font-weight: 500;
#     }
#     .access-denied {
#         background: rgba(239,68,68,0.1);
#         border: 1px solid rgba(239,68,68,0.3);
#         border-radius: 16px;
#         padding: 32px;
#         text-align: center;
#         margin: 40px auto;
#     }
#     </style>
#     """, unsafe_allow_html=True)

# # ======================================================
# # DATABASE — Extended schema with users table
# # ======================================================

# def init_db():
#     conn = sqlite3.connect("tourism_ai.db")
#     c = conn.cursor()

#     # Users table with role-based auth
#     c.execute('''
#         CREATE TABLE IF NOT EXISTS users (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             username TEXT UNIQUE NOT NULL,
#             password_hash TEXT NOT NULL,
#             role TEXT NOT NULL,
#             email TEXT,
#             full_name TEXT,
#             created_at TEXT,
#             last_login TEXT,
#             is_active INTEGER DEFAULT 1
#         )
#     ''')

#     # Bookings table
#     c.execute('''
#         CREATE TABLE IF NOT EXISTS bookings (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             user TEXT,
#             hotel TEXT,
#             city TEXT,
#             cost REAL,
#             booking_date TEXT,
#             lead_time INTEGER,
#             prev_cancels INTEGER,
#             satisfaction INTEGER,
#             status TEXT DEFAULT 'Active',
#             refunded INTEGER DEFAULT 0,
#             flagged INTEGER DEFAULT 0,
#             flag_reason TEXT DEFAULT ''
#         )
#     ''')

#     # Add missing columns if upgrading
#     for col, definition in [
#         ("status", "TEXT DEFAULT 'Active'"),
#         ("refunded", "INTEGER DEFAULT 0"),
#         ("flagged", "INTEGER DEFAULT 0"),
#         ("flag_reason", "TEXT DEFAULT ''"),
#     ]:
#         try:
#             c.execute(f"ALTER TABLE bookings ADD COLUMN {col} {definition}")
#         except Exception:
#             pass

#     # Seed default users if none exist
#     c.execute("SELECT COUNT(*) FROM users")
#     if c.fetchone()[0] == 0:
#         default_users = [
#             ("tourist1",  hash_password("tourist123"),  "Tourist",       "tourist@example.com",  "John Traveller"),
#             ("manager1",  hash_password("manager123"),  "Hotel Manager", "manager@example.com",  "Sarah Manager"),
#             ("admin1",    hash_password("admin123"),    "Admin",         "admin@example.com",    "System Admin"),
#             ("tourist2",  hash_password("password"),    "Tourist",       "t2@example.com",       "Jane Explorer"),
#         ]
#         for u in default_users:
#             c.execute("INSERT INTO users (username,password_hash,role,email,full_name,created_at) VALUES (?,?,?,?,?,?)",
#                       (*u, str(datetime.now())))

#     conn.commit()
#     conn.close()

# def hash_password(password: str) -> str:
#     return hashlib.sha256(password.encode()).hexdigest()

# def authenticate_user(username: str, password: str):
#     conn = sqlite3.connect("tourism_ai.db")
#     c = conn.cursor()
#     c.execute("SELECT id, username, role, full_name, is_active FROM users WHERE username=? AND password_hash=?",
#               (username, hash_password(password)))
#     user = c.fetchone()
#     if user and user[4] == 1:
#         c.execute("UPDATE users SET last_login=? WHERE username=?", (str(datetime.now()), username))
#         conn.commit()
#     conn.close()
#     return user  # (id, username, role, full_name, is_active) or None

# def create_user(username, password, role, email, full_name):
#     conn = sqlite3.connect("tourism_ai.db")
#     c = conn.cursor()
#     try:
#         c.execute("INSERT INTO users (username,password_hash,role,email,full_name,created_at) VALUES (?,?,?,?,?,?)",
#                   (username, hash_password(password), role, email, full_name, str(datetime.now())))
#         conn.commit()
#         return True, "User created successfully"
#     except sqlite3.IntegrityError:
#         return False, "Username already exists"
#     finally:
#         conn.close()

# def get_all_users():
#     conn = sqlite3.connect("tourism_ai.db")
#     df = pd.read_sql("SELECT id,username,role,email,full_name,created_at,last_login,is_active FROM users", conn)
#     conn.close()
#     return df

# def toggle_user_status(user_id, is_active):
#     conn = sqlite3.connect("tourism_ai.db")
#     c = conn.cursor()
#     c.execute("UPDATE users SET is_active=? WHERE id=?", (is_active, user_id))
#     conn.commit()
#     conn.close()

# # ======================================================
# # SAVE / ADMIN BOOKING OPERATIONS
# # ======================================================

# def save_booking(user, hotel, city, cost):
#     conn = sqlite3.connect("tourism_ai.db")
#     c = conn.cursor()
#     c.execute(
#         "INSERT INTO bookings (user,hotel,city,cost,booking_date,lead_time,prev_cancels,satisfaction,status,refunded,flagged,flag_reason) VALUES (?,?,?,?,?,?,?,?,'Active',0,0,'')",
#         (user, hotel, city, cost, str(datetime.now()),
#          np.random.randint(1, 60), np.random.randint(0, 3), np.random.randint(1, 6))
#     )
#     conn.commit()
#     conn.close()

# def cancel_booking(bid):
#     _exec_booking_update("UPDATE bookings SET status='Cancelled' WHERE id=?", (bid,))

# def refund_booking(bid):
#     _exec_booking_update("UPDATE bookings SET status='Refunded',refunded=1 WHERE id=?", (bid,))

# def reassign_booking(bid, new_hotel, new_city, new_cost):
#     _exec_booking_update("UPDATE bookings SET hotel=?,city=?,cost=? WHERE id=?", (new_hotel, new_city, new_cost, bid))

# def edit_booking(bid, user, hotel, city, cost):
#     _exec_booking_update("UPDATE bookings SET user=?,hotel=?,city=?,cost=? WHERE id=?", (user, hotel, city, cost, bid))

# def flag_booking(bid, reason):
#     _exec_booking_update("UPDATE bookings SET flagged=1,flag_reason=? WHERE id=?", (reason, bid))

# def unflag_booking(bid):
#     _exec_booking_update("UPDATE bookings SET flagged=0,flag_reason='' WHERE id=?", (bid,))

# def _exec_booking_update(sql, params):
#     conn = sqlite3.connect("tourism_ai.db")
#     conn.execute(sql, params)
#     conn.commit()
#     conn.close()

# # ======================================================
# # FEATURE 1 — REAL-TIME WEATHER API
# # ======================================================

# def get_live_weather(city: str, country_code: str = "ZA"):
#     """Fetch current weather from OpenWeatherMap API."""
#     if OPENWEATHER_API_KEY == "YOUR_OPENWEATHER_KEY":
#         # Return mock data when no API key configured
#         mock = {
#             "Cape Town":    {"temp": 22, "feels_like": 21, "humidity": 65, "wind_speed": 14, "condition": "Partly Cloudy", "icon": "02d", "pressure": 1015, "visibility": 10},
#             "Johannesburg": {"temp": 26, "feels_like": 25, "humidity": 45, "wind_speed": 18, "condition": "Clear Sky",    "icon": "01d", "pressure": 1012, "visibility": 10},
#             "Durban":       {"temp": 28, "feels_like": 30, "humidity": 78, "wind_speed": 12, "condition": "Humid",         "icon": "03d", "pressure": 1010, "visibility": 8 },
#             "Kruger Park":  {"temp": 31, "feels_like": 34, "humidity": 40, "wind_speed": 8,  "condition": "Hot & Sunny",  "icon": "01d", "pressure": 1008, "visibility": 10},
#             "Stellenbosch": {"temp": 20, "feels_like": 19, "humidity": 60, "wind_speed": 10, "condition": "Sunny",        "icon": "01d", "pressure": 1016, "visibility": 10},
#             "Pretoria":     {"temp": 27, "feels_like": 26, "humidity": 50, "wind_speed": 15, "condition": "Clear",        "icon": "01d", "pressure": 1011, "visibility": 10},
#             "Port Elizabeth":{"temp": 19,"feels_like": 18, "humidity": 70, "wind_speed": 20, "condition": "Windy",        "icon": "04d", "pressure": 1013, "visibility": 9 },
#             "Knysna":       {"temp": 21, "feels_like": 20, "humidity": 68, "wind_speed": 11, "condition": "Partly Cloudy","icon": "02d", "pressure": 1014, "visibility": 10},
#         }
#         return mock.get(city, {"temp": 24, "feels_like": 23, "humidity": 55, "wind_speed": 12, "condition": "Clear", "icon": "01d", "pressure": 1013, "visibility": 10})

#     try:
#         url = f"https://api.openweathermap.org/data/2.5/weather?q={city},{country_code}&appid={OPENWEATHER_API_KEY}&units=metric"
#         r = requests.get(url, timeout=8)
#         data = r.json()
#         if r.status_code == 200:
#             return {
#                 "temp":       round(data["main"]["temp"]),
#                 "feels_like": round(data["main"]["feels_like"]),
#                 "humidity":   data["main"]["humidity"],
#                 "wind_speed": round(data["wind"]["speed"] * 3.6, 1),  # m/s → km/h
#                 "condition":  data["weather"][0]["description"].title(),
#                 "icon":       data["weather"][0]["icon"],
#                 "pressure":   data["main"]["pressure"],
#                 "visibility": round(data.get("visibility", 10000) / 1000, 1),
#             }
#     except Exception as e:
#         st.error(f"Weather API error: {e}")
#     return None

# def get_weather_forecast(city: str, country_code: str = "ZA"):
#     """Fetch 5-day forecast (3-hour intervals) from OpenWeatherMap."""
#     if OPENWEATHER_API_KEY == "YOUR_OPENWEATHER_KEY":
#         # Generate mock 5-day forecast
#         days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
#         icons = ["01d", "02d", "03d", "01d", "04d"]
#         temps = [24, 26, 22, 28, 23]
#         descs = ["Sunny", "Partly Cloudy", "Cloudy", "Clear", "Overcast"]
#         return [{"day": d, "temp": t, "icon": i, "desc": desc, "humidity": np.random.randint(40, 80)}
#                 for d, t, i, desc in zip(days, temps, icons, descs)]
#     try:
#         url = f"https://api.openweathermap.org/data/2.5/forecast?q={city},{country_code}&appid={OPENWEATHER_API_KEY}&units=metric&cnt=40"
#         r = requests.get(url, timeout=8)
#         if r.status_code == 200:
#             data = r.json()
#             # Pick midday reading per day
#             daily = {}
#             for item in data["list"]:
#                 date = item["dt_txt"][:10]
#                 if date not in daily or "12:00" in item["dt_txt"]:
#                     daily[date] = {
#                         "day":      datetime.strptime(date, "%Y-%m-%d").strftime("%A"),
#                         "temp":     round(item["main"]["temp"]),
#                         "icon":     item["weather"][0]["icon"],
#                         "desc":     item["weather"][0]["description"].title(),
#                         "humidity": item["main"]["humidity"],
#                     }
#             return list(daily.values())[:5]
#     except Exception:
#         pass
#     return []

# def weather_icon_url(icon_code: str) -> str:
#     return f"https://openweathermap.org/img/wn/{icon_code}@2x.png"

# # ======================================================
# # FEATURE 2 — LANDMARK DETECTION (Google Vision API)
# # ======================================================

# def detect_landmark_vision(image_bytes: bytes):
#     """Call Google Cloud Vision API for landmark detection."""
#     if GOOGLE_VISION_API_KEY == "YOUR_GOOGLE_VISION_KEY":
#         return None  # Fall through to mock

#     try:
#         b64 = base64.b64encode(image_bytes).decode("utf-8")
#         payload = {
#             "requests": [{
#                 "image": {"content": b64},
#                 "features": [
#                     {"type": "LANDMARK_DETECTION", "maxResults": 3},
#                     {"type": "LABEL_DETECTION",    "maxResults": 5},
#                     {"type": "OBJECT_LOCALIZATION","maxResults": 5},
#                 ]
#             }]
#         }
#         url = f"https://vision.googleapis.com/v1/images:annotate?key={GOOGLE_VISION_API_KEY}"
#         r = requests.post(url, json=payload, timeout=15)
#         if r.status_code == 200:
#             resp = r.json()["responses"][0]
#             landmarks = resp.get("landmarkAnnotations", [])
#             labels    = resp.get("labelAnnotations", [])
#             if landmarks:
#                 lm = landmarks[0]
#                 loc = lm.get("locations", [{}])[0].get("latLng", {})
#                 return {
#                     "name":        lm["description"],
#                     "score":       round(lm["score"] * 100, 1),
#                     "lat":         loc.get("latitude"),
#                     "lng":         loc.get("longitude"),
#                     "labels":      [l["description"] for l in labels[:4]],
#                     "source":      "Google Vision API",
#                 }
#             elif labels:
#                 return {
#                     "name":    labels[0]["description"],
#                     "score":   round(labels[0]["score"] * 100, 1),
#                     "lat":     None, "lng": None,
#                     "labels":  [l["description"] for l in labels[:4]],
#                     "source":  "Google Vision (label)",
#                 }
#     except Exception as e:
#         st.error(f"Vision API error: {e}")
#     return None

# LANDMARK_DB = {
#     "Table Mountain": {
#         "description": "An iconic flat-topped mountain forming a prominent landmark overlooking Cape Town. Part of the Table Mountain National Park and a UNESCO World Heritage Site.",
#         "city": "Cape Town, Western Cape",
#         "lat": -33.9628, "lng": 18.4098,
#         "activities": ["Cable Car Ride", "Hiking Trails", "Abseiling", "Rock Climbing", "Paragliding"],
#         "nearby": ["V&A Waterfront", "Cape Point", "Boulders Beach", "Kirstenbosch Gardens"],
#         "hotels": ["Cape Sun Resort", "Winelands Luxury Hotel"],
#         "best_time": "October – March",
#     },
#     "Kruger National Park": {
#         "description": "One of Africa's largest game reserves covering nearly 2 million hectares. Home to the Big Five and over 500 bird species.",
#         "city": "Mpumalanga / Limpopo",
#         "lat": -23.9884, "lng": 31.5547,
#         "activities": ["Safari Game Drives", "Bush Walks", "Night Drives", "Bird Watching", "Photography"],
#         "nearby": ["Blyde River Canyon", "Panorama Route", "God's Window"],
#         "hotels": ["Kruger Safari Lodge"],
#         "best_time": "May – September (dry season)",
#     },
#     "V&A Waterfront": {
#         "description": "Cape Town's premier waterfront destination, a working harbour blending history, culture, shopping and entertainment.",
#         "city": "Cape Town, Western Cape",
#         "lat": -33.9036, "lng": 18.4218,
#         "activities": ["Shopping", "Dining", "Whale Watching", "Boat Trips", "Two Oceans Aquarium"],
#         "nearby": ["Robben Island", "Table Mountain", "Cape Town Stadium"],
#         "hotels": ["Cape Sun Resort"],
#         "best_time": "Year-round",
#     },
#     "Drakensberg": {
#         "description": "The 'Dragon Mountains' — a UNESCO World Heritage site offering dramatic scenery, ancient San rock art and world-class hiking.",
#         "city": "KwaZulu-Natal / Lesotho border",
#         "lat": -29.2500, "lng": 29.4167,
#         "activities": ["Hiking", "Rock Art Viewing", "Horse Riding", "Fly Fishing", "4x4 Trails"],
#         "nearby": ["Giants Castle", "Royal Natal National Park", "Sani Pass"],
#         "hotels": ["Mountain Retreat Lodge"],
#         "best_time": "April – September",
#     },
#     "Robben Island": {
#         "description": "Former maximum-security prison where Nelson Mandela was held for 18 years. A UNESCO World Heritage Site and powerful symbol of freedom.",
#         "city": "Cape Town, Western Cape",
#         "lat": -33.8063, "lng": 18.3661,
#         "activities": ["Guided Prison Tours", "Museum Visit", "Penguin Colony", "Historical Walk"],
#         "nearby": ["V&A Waterfront", "Table Mountain", "Bo-Kaap"],
#         "hotels": ["Cape Sun Resort"],
#         "best_time": "October – April",
#     },
# }

# def identify_landmark_mock(image: Image.Image) -> dict:
#     """Fallback: analyse image colours/size to guess a landmark category."""
#     img_array = np.array(image.convert("RGB"))
#     avg_green = img_array[:, :, 1].mean()
#     avg_blue  = img_array[:, :, 2].mean()

#     if avg_green > 120 and avg_blue < 100:
#         name = "Kruger National Park"
#     elif avg_blue > 130:
#         name = "V&A Waterfront"
#     else:
#         name = "Table Mountain"

#     info = LANDMARK_DB[name]
#     return {
#         "name":   name,
#         "score":  round(np.random.uniform(78, 94), 1),
#         "lat":    info["lat"],
#         "lng":    info["lng"],
#         "labels": ["landmark", "tourism", "South Africa"],
#         "source": "AI Image Analysis (Demo Mode — add Google Vision API key for real detection)",
#         **info,
#     }

# def get_landmark_info(name: str) -> dict:
#     return LANDMARK_DB.get(name, {})

# # ======================================================
# # FEATURE 3 — AI CHATBOT (Claude / OpenAI)
# # ======================================================

# SYSTEM_PROMPT_TOURISM = """You are an expert South African tourism consultant named 'Zara'. 
# You have deep knowledge of all SA provinces, destinations, hotels, activities, and travel tips.
# Always respond in a friendly, enthusiastic tone. 
# Keep responses concise (3-5 sentences max) unless asked for detail.
# Focus on: beaches (Durban, Garden Route), safari (Kruger, Addo), adventure (Cape Town, Drakensberg), 
# luxury (Franschhoek, Camps Bay), family (Sun City, Knysna), cultural (Soweto, Bo-Kaap, Robben Island).
# When recommending hotels, mention the ones in the system: Cape Sun Resort, Sandton Palace, Durban Escape, 
# Kruger Safari Lodge, Winelands Luxury Hotel.
# Always end with a practical tip or call to action."""

# def get_ai_response(messages: list, user_message: str) -> str:
#     """Call Claude API for intelligent chatbot responses."""
#     # Build conversation
#     chat_history = [{"role": m["role"], "content": m["content"]} for m in messages[-10:]]
#     chat_history.append({"role": "user", "content": user_message})

#     # Try Anthropic Claude
#     if ANTHROPIC_API_KEY != "YOUR_ANTHROPIC_KEY":
#         try:
#             headers = {
#                 "x-api-key": ANTHROPIC_API_KEY,
#                 "anthropic-version": "2023-06-01",
#                 "content-type": "application/json",
#             }
#             payload = {
#                 "model": "claude-3-5-haiku-20241022",
#                 "max_tokens": 400,
#                 "system": SYSTEM_PROMPT_TOURISM,
#                 "messages": chat_history,
#             }
#             r = requests.post("https://api.anthropic.com/v1/messages", headers=headers, json=payload, timeout=20)
#             if r.status_code == 200:
#                 return r.json()["content"][0]["text"]
#         except Exception:
#             pass

#     # Try OpenAI
#     if OPENAI_API_KEY != "YOUR_OPENAI_KEY":
#         try:
#             headers = {"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"}
#             payload = {
#                 "model": "gpt-4o-mini",
#                 "messages": [{"role": "system", "content": SYSTEM_PROMPT_TOURISM}] + chat_history,
#                 "max_tokens": 400,
#             }
#             r = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload, timeout=20)
#             if r.status_code == 200:
#                 return r.json()["choices"][0]["message"]["content"]
#         except Exception:
#             pass

#     # Intelligent rule-based fallback
#     return smart_fallback_response(user_message)

# def smart_fallback_response(msg: str) -> str:
#     """Smart keyword-based fallback chatbot for SA tourism."""
#     msg_lower = msg.lower()
#     responses = {
#         ("beach", "coast", "sea", "ocean", "swim"): (
#             "🏖️ For South Africa's best beaches, **Durban's Golden Mile** offers warm Indian Ocean swimming year-round, "
#             "while the **Garden Route** (Plettenberg Bay, Knysna) is stunning in summer. "
#             "Cape Town's **Camps Bay** is glamorous but cold! "
#             "I recommend the Durban Escape Hotel for a beach getaway — right on the beachfront. 🌊"
#         ),
#         ("safari", "game", "wildlife", "big five", "kruger", "lion", "elephant"): (
#             "🦁 **Kruger National Park** is South Africa's crown jewel for safari! "
#             "The best months are May–September (dry season) when animals congregate around waterholes. "
#             "Our **Kruger Safari Lodge** offers expert game drives and luxury bush accommodation. "
#             "You're almost guaranteed Big Five sightings — lion, leopard, rhino, elephant, and buffalo! 🐘"
#         ),
#         ("cape town", "table mountain", "cape", "western cape"): (
#             "🏔️ **Cape Town** is one of the world's most beautiful cities! "
#             "Don't miss the Table Mountain cable car, V&A Waterfront, Cape Point, and Boulders Beach penguins. "
#             "The **Cape Sun Resort** puts you right in the heart of it all. "
#             "Best visited October–March for warm, sunny weather. ☀️"
#         ),
#         ("johannesburg", "joburg", "jozi", "sandton", "gauteng"): (
#             "🏙️ **Johannesburg** is SA's economic powerhouse with a vibrant culture scene! "
#             "Visit Soweto, the Apartheid Museum, and the Cradle of Humankind. "
#             "**Sandton Palace Hotel** is perfect for business or luxury stays. "
#             "Joburg has world-class restaurants, galleries, and nightlife. 🍷"
#         ),
#         ("luxury", "honeymoon", "romantic", "spa", "wine"): (
#             "🥂 For luxury and romance, **Stellenbosch & Franschhoek** in the Cape Winelands are unbeatable! "
#             "The **Winelands Luxury Hotel** offers wine estate tours, gourmet dining, and a world-class spa. "
#             "Best for couples, honeymoons, and celebrating special occasions. "
#             "The region has over 200 wine estates to explore! 🍇"
#         ),
#         ("family", "kids", "children", "theme park", "sun city"): (
#             "👨‍👩‍👧 For family holidays, **Sun City** (North West) is a fantastic entertainment resort with waterparks and safari. "
#             "**Knysna** and the **Garden Route** are also brilliant for families — whale watching, forest hikes, and beaches. "
#             "Durban Escape Hotel is family-friendly with easy beach access. "
#             "Book early for school holiday periods (Dec, Jul)! 🎡"
#         ),
#         ("adventure", "hike", "climb", "extreme", "bungee"): (
#             "🧗 SA is an adventure paradise! "
#             "**Cape Town** offers abseiling off Table Mountain and shark cage diving. "
#             "**Bloukrans Bridge** near Plettenberg Bay has the world's highest commercial bungee jump (216m). "
#             "The **Drakensberg** is world-class for hiking and rock art. "
#             "Wild Coast and Tsitsikamma are great for sea kayaking and canopy tours! 🏄"
#         ),
#         ("culture", "history", "museum", "heritage", "township"): (
#             "🎭 SA's cultural highlights are profound and moving. "
#             "Visit **Robben Island** where Mandela was imprisoned, the **Apartheid Museum** in Joburg, "
#             "and vibrant **Bo-Kaap** in Cape Town with its colourful Cape Malay heritage. "
#             "Soweto township tours offer incredible insight into SA's history and spirit. "
#             "The **cradle of humankind** near Joburg is a UNESCO World Heritage site! 🌍"
#         ),
#         ("budget", "cheap", "affordable", "backpack"): (
#             "💰 SA is excellent value! "
#             "The **Garden Route** and **Wild Coast** are budget-friendly with great camping and backpacker lodges. "
#             "Hostel dorms in Cape Town and Durban from R200–R400/night. "
#             "Renting a car and self-driving the Garden Route is one of SA's best budget adventures. "
#             "Visit April–June or August–September for lower prices outside peak season! 🎒"
#         ),
#     }
#     for keywords, response in responses.items():
#         if any(k in msg_lower for k in keywords):
#             return response

#     return (
#         "🌍 South Africa is an incredible destination with something for everyone! "
#         "Are you interested in **beaches**, **safari**, **adventure sports**, **wine regions**, or **cultural experiences**? "
#         "I can tailor specific recommendations for Cape Town, Johannesburg, Durban, Kruger Park, or the Garden Route. "
#         "What type of holiday experience are you dreaming of? ✈️"
#     )

# # ======================================================
# # FEATURE 4 — HOTEL LOCATION MAPPING (Google Maps / Folium)
# # ======================================================

# HOTEL_COORDINATES = {
#     "Cape Sun Resort":        {"lat": -33.9249, "lng": 18.4241, "city": "Cape Town",     "address": "Strand St, Cape Town, 8001"},
#     "Sandton Palace":         {"lat": -26.1076, "lng": 28.0567, "city": "Johannesburg",  "address": "Sandton City, Johannesburg, 2196"},
#     "Durban Escape":          {"lat": -29.8587, "lng": 31.0218, "city": "Durban",        "address": "Marine Parade, Durban, 4001"},
#     "Kruger Safari Lodge":    {"lat": -24.0103, "lng": 31.4840, "city": "Kruger Park",   "address": "Skukuza, Kruger National Park"},
#     "Winelands Luxury Hotel": {"lat": -33.9321, "lng": 18.8602, "city": "Stellenbosch",  "address": "Dorp Street, Stellenbosch, 7600"},
# }

# def build_hotel_map(selected_city: str = "All", selected_hotel: str = "All") -> folium.Map:
#     """Build a Folium map restricted to South Africa with hotel markers."""
#     m = folium.Map(
#         location=[-30.5595, 22.9375],
#         zoom_start=5,
#         tiles="CartoDB positron",
#         min_zoom=4,
#         max_zoom=15,
#     )
#     # SA boundary hint
#     folium.Rectangle(
#         bounds=[[-35.0, 16.3], [-22.1, 33.0]],
#         color="#ff6e40",
#         fill=True,
#         fill_opacity=0.02,
#         weight=1.5,
#         tooltip="South Africa"
#     ).add_to(m)

#     hotels = get_hotels()
#     for _, h in hotels.iterrows():
#         coords = HOTEL_COORDINATES.get(h["name"])
#         if not coords:
#             continue
#         if selected_city != "All" and coords["city"] != selected_city:
#             continue
#         if selected_hotel != "All" and h["name"] != selected_hotel:
#             continue

#         icon_color = "orange" if h["type"] == "Luxury" else (
#                      "blue"   if h["type"] == "Business" else (
#                      "green"  if h["type"] == "Safari" else (
#                      "red"    if h["type"] == "Beach" else "gray")))

#         popup_html = f"""
#         <div style="font-family:sans-serif;min-width:200px;">
#           <b style="font-size:14px;color:#ff6e40;">{h['name']}</b><br>
#           <span style="color:#666;">📍 {coords['address']}</span><br><br>
#           <b>Type:</b> {h['type']}<br>
#           <b>Rating:</b> ⭐ {h['rating']}/5.0<br>
#           <b>Price:</b> R{h['price']:,}/night<br>
#           <b>Occupancy:</b> {h['occupancy']}%<br>
#           <b>Amenities:</b> {h['amenities']}<br>
#         </div>
#         """
#         folium.Marker(
#             location=[coords["lat"], coords["lng"]],
#             popup=folium.Popup(popup_html, max_width=260),
#             tooltip=f"🏨 {h['name']} — R{h['price']:,}",
#             icon=folium.Icon(color=icon_color, icon="home", prefix="fa"),
#         ).add_to(m)

#     return m

# # ======================================================
# # FEATURE 5 — REAL-TIME HOTEL IMAGES (Google Places)
# # ======================================================

# HOTEL_IMAGE_URLS = {
#     "Cape Sun Resort": [
#         "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800",
#         "https://images.unsplash.com/photo-1582719508461-905c673771fd?w=800",
#         "https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?w=800",
#     ],
#     "Sandton Palace": [
#         "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=800",
#         "https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=800",
#         "https://images.unsplash.com/photo-1618773928121-c32242e63f39?w=800",
#     ],
#     "Durban Escape": [
#         "https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=800",
#         "https://images.unsplash.com/photo-1501594907352-04cda38ebc29?w=800",
#         "https://images.unsplash.com/photo-1615880484746-a134be9a6ecf?w=800",
#     ],
#     "Kruger Safari Lodge": [
#         "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=800",
#         "https://images.unsplash.com/photo-1516426122078-c23e76319801?w=800",
#         "https://images.unsplash.com/photo-1523805009345-7448845a9e53?w=800",
#     ],
#     "Winelands Luxury Hotel": [
#         "https://images.unsplash.com/photo-1455587734955-081b22074882?w=800",
#         "https://images.unsplash.com/photo-1544148103-0773bf10d330?w=800",
#         "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=800",
#     ],
# }

# def get_hotel_images_places(hotel_name: str, city: str) -> list:
#     """Fetch hotel images via Google Places API, fallback to curated Unsplash."""
#     if GOOGLE_PLACES_API_KEY != "YOUR_GOOGLE_PLACES_KEY":
#         try:
#             # Step 1: Find Place
#             search_url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
#             params = {
#                 "input":     f"{hotel_name} {city} South Africa",
#                 "inputtype": "textquery",
#                 "fields":    "place_id,name,photos",
#                 "key":       GOOGLE_PLACES_API_KEY,
#             }
#             r = requests.get(search_url, params=params, timeout=10)
#             if r.status_code == 200:
#                 candidates = r.json().get("candidates", [])
#                 if candidates:
#                     photos = candidates[0].get("photos", [])
#                     urls = []
#                     for photo in photos[:4]:
#                         ref = photo["photo_reference"]
#                         img_url = (
#                             f"https://maps.googleapis.com/maps/api/place/photo"
#                             f"?maxwidth=800&photo_reference={ref}&key={GOOGLE_PLACES_API_KEY}"
#                         )
#                         urls.append(img_url)
#                     if urls:
#                         return urls
#         except Exception:
#             pass
#     # Fallback
#     return HOTEL_IMAGE_URLS.get(hotel_name, [
#         "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800"
#     ])

# # ======================================================
# # ML MODELS
# # ======================================================

# def predict_cancellation(lead_time, prev_cancels):
#     X_train = [[5,0],[30,1],[60,2],[2,0],[45,1],[10,0],[55,2],[25,1]]
#     y_train = [0,1,1,0,1,0,1,0]
#     clf = RandomForestClassifier(random_state=42)
#     clf.fit(X_train, y_train)
#     return "High Risk" if clf.predict([[lead_time, prev_cancels]])[0] == 1 else "Low Risk"

# def predict_revenue(bookings_count):
#     X = np.array([[10],[20],[30],[40],[50],[60]])
#     y = np.array([15000,32000,48000,61000,79000,92000])
#     model = RandomForestRegressor(random_state=42)
#     model.fit(X, y)
#     return model.predict([[bookings_count]])[0]

# def dynamic_hotel_price(base_price, demand, occupancy, season, holiday, weather):
#     m = 1.0
#     if demand == "High":  m += 0.20
#     elif demand == "Low": m -= 0.10
#     if occupancy > 80:  m += 0.25
#     elif occupancy < 40: m -= 0.15
#     if season == "Peak": m += 0.30
#     if holiday: m += 0.20
#     if weather in ["Sunny ☀️","Humid 🌤️"]: m += 0.10
#     return round(base_price * m, 2)

# def analyze_sentiment(review):
#     analysis = TextBlob(review)
#     p = analysis.sentiment.polarity
#     if p > 0: return "Positive", p
#     elif p < 0: return "Negative", p
#     return "Neutral", p

# def get_hotels():
#     return pd.DataFrame([
#         {"name":"Cape Sun Resort","price":2500,"city":"Cape Town","rating":4.7,"type":"Luxury","occupancy":85,"sentiment_score":92,"amenities":"WiFi, Pool, Spa"},
#         {"name":"Sandton Palace","price":3500,"city":"Johannesburg","rating":4.8,"type":"Business","occupancy":78,"sentiment_score":88,"amenities":"WiFi, Gym, Conference Rooms"},
#         {"name":"Durban Escape","price":2100,"city":"Durban","rating":4.4,"type":"Beach","occupancy":70,"sentiment_score":84,"amenities":"Beach Access, Pool, Bar"},
#         {"name":"Kruger Safari Lodge","price":7000,"city":"Kruger Park","rating":5.0,"type":"Safari","occupancy":95,"sentiment_score":97,"amenities":"Safari Tours, WiFi, Restaurant"},
#         {"name":"Winelands Luxury Hotel","price":5200,"city":"Stellenbosch","rating":4.9,"type":"Luxury","occupancy":82,"sentiment_score":93,"amenities":"Wine Tours, Spa, Pool"},
#     ])

# def rank_hotels(hotels_df, bookings_df):
#     scores = []
#     for _, h in hotels_df.iterrows():
#         hotel_bookings = bookings_df[bookings_df['hotel'] == h['name']] if not bookings_df.empty else pd.DataFrame()
#         revenue = hotel_bookings['cost'].sum() if not hotel_bookings.empty else 0
#         cancellations = len(hotel_bookings[hotel_bookings['status'] == 'Cancelled']) if not hotel_bookings.empty else 0
#         total = len(hotel_bookings) if not hotel_bookings.empty else 1
#         cancel_rate = cancellations / max(total, 1)
#         score = (h['rating']*20 + h['occupancy']*0.4 + h['sentiment_score']*0.3 + min(revenue/1000,20) - cancel_rate*15)
#         scores.append({
#             "Hotel": h['name'], "City": h['city'], "Rating": h['rating'], "Occupancy": h['occupancy'],
#             "Sentiment": h['sentiment_score'], "Revenue": revenue, "Cancel Rate": round(cancel_rate*100,1), "Score": round(score,1)
#         })
#     ranked = pd.DataFrame(scores).sort_values("Score", ascending=False).reset_index(drop=True)
#     tiers = []
#     for i, row in ranked.iterrows():
#         if i == 0 or row['Score'] >= ranked['Score'].quantile(0.75): tiers.append("🏆 Top Performer")
#         elif row['Score'] >= ranked['Score'].quantile(0.4):           tiers.append("⚠️ Average")
#         else:                                                          tiers.append("❌ Underperforming")
#     ranked['Tier'] = tiers
#     return ranked

# # ======================================================
# # ACCESS CONTROL HELPERS
# # ======================================================

# def require_role(allowed_roles: list):
#     """Return True if current user has one of the allowed roles, else show denied."""
#     role = st.session_state.get("role", "")
#     if role not in allowed_roles:
#         st.markdown("""
#         <div class='access-denied'>
#             <h2>🔒 Access Denied</h2>
#             <p style='color:#94a3b8;'>You don't have permission to view this section.<br>
#             Please contact your administrator if you believe this is an error.</p>
#         </div>""", unsafe_allow_html=True)
#         return False
#     return True

# def role_badge(role: str) -> str:
#     badges = {
#         "Tourist":       "<span class='role-badge-tourist'>🌍 Tourist</span>",
#         "Hotel Manager": "<span class='role-badge-manager'>🏨 Hotel Manager</span>",
#         "Admin":         "<span class='role-badge-admin'>🛡️ Admin</span>",
#     }
#     return badges.get(role, role)

# # ======================================================
# # PDF UTILITIES
# # ======================================================

# def safe(text):
#     replacements = {
#         "\u2014":"-","\u2013":"-","\u2018":"'","\u2019":"'","\u201C":'"',"\u201D":'"',
#         "\u2022":"-","\u2026":"...","\u00B0":" deg",
#         "🏆":"[TOP]","⚠️":"[AVG]","❌":"[LOW]","🌍":"","✅":"OK","📊":"",
#         "💰":"","📅":"","🤖":"","😊":"","📄":"","🛡️":"","🔴":"[!]","🟡":"[~]","🟢":"[OK]",
#     }
#     for u, a in replacements.items():
#         text = text.replace(u, a)
#     return text.encode("latin-1", errors="replace").decode("latin-1")

# # ======================================================
# # MAIN APP
# # ======================================================

# def main():
#     apply_styles()
#     init_db()
#     hotels = get_hotels()

#     # ── Sidebar Currency Converter ──
#     st.sidebar.title("🌍 AI Tourism ZA")
#     if st.session_state.get("role"):
#         st.sidebar.markdown(f"**Logged in as:** {st.session_state.get('user','')}")
#         st.sidebar.markdown(role_badge(st.session_state.get("role", "")), unsafe_allow_html=True)
#         st.sidebar.divider()
#     amount = st.sidebar.number_input("Amount in ZAR", value=1000, min_value=0)
#     currency = st.sidebar.selectbox("Convert To", ["USD","EUR","GBP","AUD","CNY"])
#     rates = {"USD":0.053,"EUR":0.049,"GBP":0.042,"AUD":0.082,"CNY":0.38}
#     st.sidebar.success(f"≈ {amount*rates[currency]:.2f} {currency}")

#     # ── Session state init ──
#     for key, default in [("role", None), ("user", ""), ("user_id", None), ("full_name", ""), ("chat_history", [])]:
#         if key not in st.session_state:
#             st.session_state[key] = default

#     # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#     # LOGIN PAGE
#     # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#     if st.session_state.role is None:
#         st.markdown("""
#         <div class='hero'>
#             <h1 style='font-size:2.4rem;'>🌍 AI Smart Tourism ZA</h1>
#             <p style='color:#94a3b8;font-size:1.15rem;'>Enterprise Smart Tourism & Hospitality Platform for South Africa</p>
#             <p style='color:#64748b;font-size:0.9rem;margin-top:8px;'>Powered by AI · Real-Time Data · Role-Based Access</p>
#         </div>""", unsafe_allow_html=True)

#         col1, col2 = st.columns([1, 1])
#         with col1:
#             st.subheader("🔐 Secure Login")
#             username = st.text_input("Username", placeholder="e.g. tourist1")
#             password = st.text_input("Password", type="password", placeholder="Your password")

#             if st.button("Login", use_container_width=True):
#                 user = authenticate_user(username, password)
#                 if user:
#                     st.session_state.role      = user[2]
#                     st.session_state.user      = user[1]
#                     st.session_state.user_id   = user[0]
#                     st.session_state.full_name = user[3]
#                     st.rerun()
#                 else:
#                     st.error("❌ Invalid credentials or account inactive.")

#             st.divider()
#             with st.expander("📋 Demo Credentials"):
#                 st.markdown("""
#                 | Role | Username | Password |
#                 |------|----------|----------|
#                 | Tourist | `tourist1` | `tourist123` |
#                 | Hotel Manager | `manager1` | `manager123` |
#                 | Admin | `admin1` | `admin123` |
#                 """)

#         with col2:
#             st.image("https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=700",
#                      caption="South Africa — Where Every Journey Begins", use_container_width=True)
#             st.markdown("""
#             <div class='metric-card'>
#                 <h4>Platform Features</h4>
#                 <p style='color:#94a3b8;font-size:0.9rem;'>
#                 ✅ Live weather for any SA destination<br>
#                 ✅ AI landmark detection from photos<br>
#                 ✅ Intelligent SA travel chatbot<br>
#                 ✅ Interactive hotel map (SA-only)<br>
#                 ✅ Real-time hotel image galleries<br>
#                 ✅ Role-based secure access<br>
#                 ✅ AI dynamic pricing & forecasting
#                 </p>
#             </div>""", unsafe_allow_html=True)

#     # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#     # TOURIST DASHBOARD
#     # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#     elif st.session_state.role == "Tourist":
#         if not require_role(["Tourist"]):
#             return

#         name = st.session_state.full_name or st.session_state.user
#         st.title(f"✈️ Welcome, {name}!")
#         c1, c2, c3 = st.columns(3)
#         c1.metric("Available Hotels", 5)
#         c2.metric("Destinations", 5)
#         c3.metric("Avg Satisfaction", "94%")

#         tabs = st.tabs([
#             "🏨 Hotels & Booking",
#             "🌦️ Live Weather",
#             "🤖 AI Recommendations",
#             "⚖️ Compare Hotels",
#             "🗺️ Hotel Map",
#             "💬 AI Chatbot",
#             "😊 Reviews",
#             "📷 Landmark Detection",
#         ])

#         # ── Tab 0: Hotels & Booking ──
#         with tabs[0]:
#             st.subheader("🏨 Smart Hotel Booking")
#             col1, col2 = st.columns([1, 2])
#             with col1:
#                 check_in  = st.date_input("Check-in")
#                 check_out = st.date_input("Check-out")
#                 budget    = st.slider("Budget (ZAR)", 1000, 10000, 3000, step=500)
#                 sel_city  = st.selectbox("Destination", ["All", "Cape Town", "Johannesburg", "Durban", "Kruger Park", "Stellenbosch"])
#                 hotel_type = st.selectbox("Hotel Type", ["All", "Luxury", "Business", "Beach", "Safari"])

#             filtered = hotels.copy()
#             if budget:          filtered = filtered[filtered["price"] <= budget]
#             if sel_city != "All":  filtered = filtered[filtered["city"] == sel_city]
#             if hotel_type != "All": filtered = filtered[filtered["type"] == hotel_type]

#             with col2:
#                 st.success(f"🔍 Found **{len(filtered)}** hotel(s) matching your criteria")

#             for _, row in filtered.iterrows():
#                 st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
#                 c1, c2, c3 = st.columns([1, 3, 1])
#                 with c1:
#                     # FEATURE 5: Real-time hotel images
#                     imgs = get_hotel_images_places(row["name"], row["city"])
#                     if imgs:
#                         st.image(imgs[0], use_container_width=True)
#                 with c2:
#                     st.subheader(row["name"])
#                     st.write(f"📍 {row['city']}  |  💰 **R{row['price']:,}/night**  |  ⭐ {row['rating']}  |  🏷️ {row['type']}")
#                     st.write(f"🛎️ {row['amenities']}  |  📊 Occupancy: {row['occupancy']}%")
#                     # Show image gallery
#                     if st.button("📷 View Gallery", key=f"gal_{row['name']}"):
#                         st.session_state[f"show_gallery_{row['name']}"] = True
#                 with c3:
#                     if st.button("✅ Book Now", key=f"bk_{row['name']}"):
#                         save_booking(st.session_state.user, row["name"], row["city"], row["price"])
#                         st.success(f"Booked {row['name']}! 🎉")

#                 # Gallery modal
#                 if st.session_state.get(f"show_gallery_{row['name']}"):
#                     imgs = get_hotel_images_places(row["name"], row["city"])
#                     gcols = st.columns(min(len(imgs), 3))
#                     for gi, img_url in enumerate(imgs[:3]):
#                         gcols[gi].image(img_url, use_container_width=True)
#                     if st.button("Close Gallery", key=f"cls_{row['name']}"):
#                         del st.session_state[f"show_gallery_{row['name']}"]

#                 st.markdown("</div>", unsafe_allow_html=True)

#         # ── Tab 1: FEATURE 1 — Live Weather ──
#         with tabs[1]:
#             st.subheader("🌦️ Real-Time Weather — South Africa")
#             sa_cities = ["Cape Town", "Johannesburg", "Durban", "Kruger Park", "Stellenbosch",
#                          "Pretoria", "Port Elizabeth", "Knysna", "Bloemfontein", "East London"]

#             col1, col2 = st.columns([1, 2])
#             with col1:
#                 weather_city    = st.selectbox("Select City", sa_cities, key="weather_city_tourist")
#                 custom_city     = st.text_input("Or type any SA city", placeholder="e.g. Hermanus")
#                 search_city     = custom_city.strip() if custom_city.strip() else weather_city
#                 refresh_weather = st.button("🔄 Refresh Weather")

#             with col2:
#                 w = get_live_weather(search_city)
#                 if w:
#                     st.markdown(f"""
#                     <div class='weather-card'>
#                         <h2 style='color:#38bdf8;margin-bottom:4px;'>📍 {search_city}</h2>
#                         <h1 style='font-size:3.5rem;margin:0;'>{w['temp']}°C</h1>
#                         <p style='color:#94a3b8;font-size:1.1rem;margin:4px 0;'>{w['condition']}</p>
#                         <p style='color:#64748b;font-size:0.9rem;'>Feels like {w['feels_like']}°C</p>
#                     </div>""", unsafe_allow_html=True)
#                     wc1, wc2, wc3, wc4 = st.columns(4)
#                     wc1.metric("💧 Humidity",    f"{w['humidity']}%")
#                     wc2.metric("💨 Wind Speed",  f"{w['wind_speed']} km/h")
#                     wc3.metric("🌡️ Pressure",    f"{w['pressure']} hPa")
#                     wc4.metric("👁️ Visibility",  f"{w['visibility']} km")

#             # 5-Day Forecast
#             st.subheader("📅 5-Day Forecast")
#             forecast = get_weather_forecast(search_city)
#             if forecast:
#                 fcols = st.columns(len(forecast))
#                 for fi, day in enumerate(forecast):
#                     fcols[fi].markdown(f"""
#                     <div class='forecast-card'>
#                         <b style='color:#94a3b8;font-size:0.8rem;'>{day['day'][:3].upper()}</b><br>
#                         <span style='font-size:1.5rem;'>🌤️</span><br>
#                         <b style='font-size:1.2rem;'>{day['temp']}°C</b><br>
#                         <span style='color:#64748b;font-size:0.75rem;'>{day['desc']}</span><br>
#                         <span style='color:#38bdf8;font-size:0.75rem;'>💧 {day['humidity']}%</span>
#                     </div>""", unsafe_allow_html=True)

#             # Weather across all cities
#             st.subheader("🗺️ Weather Snapshot — All SA Destinations")
#             all_weather = []
#             for c in ["Cape Town", "Johannesburg", "Durban", "Kruger Park", "Stellenbosch"]:
#                 ww = get_live_weather(c)
#                 if ww:
#                     all_weather.append({"City": c, "Temp (°C)": ww["temp"], "Humidity (%)": ww["humidity"],
#                                         "Wind (km/h)": ww["wind_speed"], "Condition": ww["condition"]})
#             if all_weather:
#                 weather_df = pd.DataFrame(all_weather)
#                 st.dataframe(weather_df, use_container_width=True, hide_index=True)
#                 st.plotly_chart(px.bar(weather_df, x="City", y="Temp (°C)", color="City",
#                     title="Temperature Comparison Across SA Destinations", template="plotly_dark"),
#                     use_container_width=True)

#         # ── Tab 2: AI Recommendations ──
#         with tabs[2]:
#             st.subheader("🧠 AI Hotel Recommendations")
#             col1, col2 = st.columns(2)
#             with col1:
#                 ai_budget  = st.slider("Your Budget (ZAR)", 1000, 10000, 3000, step=500, key="ai_budget")
#                 travel_exp = st.selectbox("Travel Experience", ["Luxury", "Business", "Beach", "Safari"])
#                 ai_city    = st.selectbox("Preferred Area", ["All"] + ["Cape Town","Johannesburg","Durban","Kruger Park","Stellenbosch"])
#             with col2:
#                 w_dest = get_live_weather(ai_city if ai_city != "All" else "Cape Town")
#                 if w_dest:
#                     st.markdown(f"""
#                     <div class='forecast-card'>
#                         <b>Current Weather — {ai_city if ai_city != 'All' else 'Cape Town'}</b><br>
#                         <span style='font-size:1.5rem;'>🌡️</span> {w_dest['temp']}°C · {w_dest['condition']}<br>
#                         <span style='color:#64748b;font-size:0.8rem;'>Humidity: {w_dest['humidity']}% · Wind: {w_dest['wind_speed']} km/h</span>
#                     </div>""", unsafe_allow_html=True)

#             recs = hotels[hotels["price"] <= ai_budget]
#             if travel_exp: recs = recs[recs["type"] == travel_exp]
#             if ai_city != "All": recs = recs[recs["city"] == ai_city]
#             recs = recs.sort_values(["rating", "price"], ascending=[False, True])

#             if recs.empty:
#                 st.warning("No hotels match your criteria. Try adjusting your budget or preferences.")
#             else:
#                 for _, h in recs.iterrows():
#                     with st.expander(f"🏨 {h['name']} — R{h['price']:,}/night  ⭐ {h['rating']}"):
#                         ec1, ec2 = st.columns([2, 1])
#                         with ec1:
#                             imgs = get_hotel_images_places(h["name"], h["city"])
#                             st.image(imgs[0], use_container_width=True)
#                         with ec2:
#                             st.write(f"📍 {h['city']}")
#                             st.write(f"🏷️ {h['type']}")
#                             st.write(f"⭐ Rating: {h['rating']}/5.0")
#                             st.write(f"📊 Occupancy: {h['occupancy']}%")
#                             st.write(f"🛎️ {h['amenities']}")
#                             wh = get_live_weather(h["city"])
#                             if wh:
#                                 st.info(f"🌡️ {wh['temp']}°C · {wh['condition']}")
#                             if st.button("Book", key=f"rec_bk_{h['name']}"):
#                                 save_booking(st.session_state.user, h["name"], h["city"], h["price"])
#                                 st.success("Booked! ✅")

#         # ── Tab 3: Compare Hotels ──
#         with tabs[3]:
#             st.subheader("⚖️ Hotel Comparison")
#             sel = st.multiselect("Select Hotels to Compare (min 2)", hotels["name"].tolist())
#             if len(sel) >= 2:
#                 cdf = hotels[hotels["name"].isin(sel)].copy()

#                 # Images grid
#                 img_cols = st.columns(len(sel))
#                 for ci, h_name in enumerate(sel):
#                     imgs = get_hotel_images_places(h_name, cdf[cdf["name"]==h_name]["city"].values[0])
#                     if imgs:
#                         img_cols[ci].image(imgs[0], caption=h_name, use_container_width=True)

#                 # Data table
#                 cdf_display = cdf[["name","city","type","price","rating","occupancy","sentiment_score","amenities"]]
#                 cdf_display.columns = ["Hotel","City","Type","Price (ZAR)","Rating","Occupancy %","Sentiment %","Amenities"]
#                 st.dataframe(cdf_display, use_container_width=True, hide_index=True)

#                 # Charts
#                 cc1, cc2 = st.columns(2)
#                 cc1.plotly_chart(px.bar(cdf, x="name", y="rating", color="name", title="Rating Comparison",
#                     template="plotly_dark", text="rating"), use_container_width=True)
#                 cc2.plotly_chart(px.bar(cdf, x="name", y="price", color="name", title="Price Comparison (ZAR)",
#                     template="plotly_dark", text="price"), use_container_width=True)

#                 # Weather comparison
#                 st.subheader("🌦️ Live Weather at Each Hotel Location")
#                 wc_cols = st.columns(len(sel))
#                 for wi, h_name in enumerate(sel):
#                     city_name = cdf[cdf["name"]==h_name]["city"].values[0]
#                     ww = get_live_weather(city_name)
#                     if ww:
#                         wc_cols[wi].markdown(f"""
#                         <div class='forecast-card'>
#                             <b>{h_name}</b><br>
#                             <b style='font-size:1.4rem;'>{ww['temp']}°C</b><br>
#                             <span style='color:#94a3b8;'>{ww['condition']}</span><br>
#                             <span style='font-size:0.8rem;color:#64748b;'>💧 {ww['humidity']}% · 💨 {ww['wind_speed']} km/h</span>
#                         </div>""", unsafe_allow_html=True)
#             else:
#                 st.info("Please select at least 2 hotels to compare.")

#         # ── Tab 4: FEATURE 4 — Hotel Map ──
#         with tabs[4]:
#             st.subheader("🗺️ Interactive Hotel Map — South Africa")
#             mc1, mc2 = st.columns([1, 3])
#             with mc1:
#                 map_city   = st.selectbox("Filter by City",   ["All","Cape Town","Johannesburg","Durban","Kruger Park","Stellenbosch"])
#                 map_hotel  = st.selectbox("Filter by Hotel",  ["All"] + hotels["name"].tolist())
#                 map_type   = st.selectbox("Hotel Type",       ["All","Luxury","Business","Beach","Safari"])
#                 st.markdown("""
#                 <div class='metric-card'>
#                     <b>Map Legend</b><br>
#                     🟠 Luxury hotels<br>
#                     🔵 Business hotels<br>
#                     🟢 Safari lodges<br>
#                     🔴 Beach resorts<br>
#                     ⚫ Other
#                 </div>""", unsafe_allow_html=True)
#             with mc2:
#                 hotel_map = build_hotel_map(map_city, map_hotel)
#                 st_folium(hotel_map, width=700, height=500)

#             # Hotel quick cards below map
#             st.subheader("📌 Hotel Quick Info")
#             hcols = st.columns(len(hotels))
#             for hi, (_, h) in enumerate(hotels.iterrows()):
#                 coords = HOTEL_COORDINATES.get(h["name"], {})
#                 hcols[hi].markdown(f"""
#                 <div class='forecast-card'>
#                     <b style='font-size:0.85rem;'>{h['name']}</b><br>
#                     <span style='color:#ff6e40;font-size:0.8rem;'>R{h['price']:,}</span><br>
#                     <span style='color:#94a3b8;font-size:0.75rem;'>⭐ {h['rating']} · {h['type']}</span><br>
#                     <span style='color:#64748b;font-size:0.7rem;'>📍 {coords.get('address','')[:30]}</span>
#                 </div>""", unsafe_allow_html=True)

#         # ── Tab 5: FEATURE 3 — AI Chatbot ──
#         with tabs[5]:
#             st.subheader("💬 Zara — Your SA Tourism AI Assistant")
#             st.markdown("""
#             <div class='metric-card'>
#                 <b>🤖 Ask Zara anything about South African travel!</b><br>
#                 <span style='color:#94a3b8;font-size:0.9rem;'>
#                 Try: "Best beach destinations" · "Safari tips for Kruger" · "Luxury wine estate recommendations" · 
#                 "Family-friendly spots" · "Adventure activities in Cape Town" · "Budget travel tips"
#                 </span>
#             </div>""", unsafe_allow_html=True)

#             # Category quick-select buttons
#             cats = ["🏖️ Beaches", "🦁 Safari", "🏔️ Adventure", "🥂 Luxury", "👨‍👩‍👧 Family", "🎭 Culture", "💰 Budget Tips"]
#             cat_cols = st.columns(len(cats))
#             for ci, cat in enumerate(cats):
#                 if cat_cols[ci].button(cat, key=f"cat_{ci}"):
#                     prompt = cat.split(" ", 1)[1]
#                     st.session_state.chat_history.append({"role": "user", "content": f"Tell me about {prompt} in South Africa"})
#                     with st.spinner("Zara is thinking..."):
#                         response = get_ai_response(st.session_state.chat_history[:-1], f"Tell me about {prompt} in South Africa")
#                     st.session_state.chat_history.append({"role": "assistant", "content": response})
#                     st.rerun()

#             # Chat display
#             chat_container = st.container()
#             with chat_container:
#                 for msg in st.session_state.chat_history:
#                     if msg["role"] == "user":
#                         st.markdown(f"<div class='chat-bubble-user'>👤 {msg['content']}</div>", unsafe_allow_html=True)
#                     else:
#                         st.markdown(f"<div class='chat-bubble-bot'>🤖 <b>Zara:</b> {msg['content']}</div>", unsafe_allow_html=True)

#             # Input
#             user_msg = st.chat_input("Ask Zara about SA travel destinations, hotels, tips...")
#             if user_msg:
#                 st.session_state.chat_history.append({"role": "user", "content": user_msg})
#                 with st.spinner("Zara is researching..."):
#                     response = get_ai_response(st.session_state.chat_history[:-1], user_msg)
#                 st.session_state.chat_history.append({"role": "assistant", "content": response})
#                 st.rerun()

#             if st.button("🗑️ Clear Chat"):
#                 st.session_state.chat_history = []
#                 st.rerun()

#         # ── Tab 6: Reviews ──
#         with tabs[6]:
#             st.subheader("😊 Write & Analyse Your Review")
#             review_hotel  = st.selectbox("Hotel", hotels["name"].tolist())
#             review_rating = st.slider("Your Rating", 1, 5, 4)
#             review_text   = st.text_area("Share your experience...", height=150)
#             if st.button("Analyse Review"):
#                 if review_text.strip():
#                     sentiment, polarity = analyze_sentiment(review_text)
#                     sc1, sc2 = st.columns(2)
#                     color = "#34d399" if sentiment == "Positive" else ("#f87171" if sentiment == "Negative" else "#f59e0b")
#                     sc1.markdown(f"""
#                     <div class='metric-card' style='text-align:center;border-color:{color};'>
#                         <h2 style='color:{color};'>{sentiment}</h2>
#                         <p>Polarity Score: {polarity:.3f}</p>
#                         <p>Your Rating: {'⭐' * review_rating}</p>
#                     </div>""", unsafe_allow_html=True)
#                     with sc2:
#                         wc = WordCloud(width=600, height=300, background_color="white").generate(review_text)
#                         fig, ax = plt.subplots(figsize=(6, 3))
#                         ax.imshow(wc)
#                         ax.axis("off")
#                         st.pyplot(fig)
#                         plt.close(fig)
#                 else:
#                     st.warning("Please write a review first.")

#         # ── Tab 7: FEATURE 2 — Landmark Detection ──
#         with tabs[7]:
#             st.subheader("📷 AI Landmark Detection")
#             st.markdown("""
#             <div class='landmark-card'>
#                 <p style='color:#a78bfa;margin:0;'>Upload a photo of any South African landmark, attraction, or scenic spot. 
#                 Our AI will identify it and suggest nearby hotels and activities.</p>
#             </div>""", unsafe_allow_html=True)

#             ld_col1, ld_col2 = st.columns([1, 1])
#             with ld_col1:
#                 uf = st.file_uploader("Upload Photo", type=["jpg", "jpeg", "png", "webp"])
#                 # Manual override for demo
#                 manual_landmark = st.selectbox("Or select a known landmark", ["Auto-detect"] + list(LANDMARK_DB.keys()))

#             if uf:
#                 img = Image.open(uf)
#                 ld_col1.image(img, caption="Uploaded Image", use_container_width=True)
#                 img_bytes = uf.read() if hasattr(uf, "read") else io.BytesIO()
#                 uf.seek(0)
#                 img_bytes_data = uf.read()

#                 with ld_col2:
#                     with st.spinner("🔍 Analysing image with AI..."):
#                         # Try Vision API first
#                         result = detect_landmark_vision(img_bytes_data)
#                         if not result:
#                             result = identify_landmark_mock(img)
#                         # Merge with DB info
#                         db_info = get_landmark_info(result.get("name", ""))
#                         if db_info:
#                             result.update(db_info)

#                     if result:
#                         st.markdown(f"""
#                         <div class='landmark-card'>
#                             <h3 style='color:#a78bfa;'>🏛️ {result.get('name','Unknown')}</h3>
#                             <p style='color:#94a3b8;font-size:0.85rem;'>Confidence: {result.get('score','N/A')}% · {result.get('source','AI Analysis')}</p>
#                             <p>📍 {result.get('city','South Africa')}</p>
#                             <p>{result.get('description','A beautiful South African landmark.')}</p>
#                         </div>""", unsafe_allow_html=True)

#                         if result.get("activities"):
#                             st.write("**🎯 Activities & Experiences:**")
#                             act_cols = st.columns(min(len(result["activities"]), 3))
#                             for ai, act in enumerate(result["activities"]):
#                                 act_cols[ai % 3].markdown(f"✅ {act}")

#                         if result.get("nearby"):
#                             st.write("**📍 Nearby Attractions:**")
#                             st.write(" · ".join(result["nearby"]))

#                         if result.get("hotels"):
#                             st.write("**🏨 Recommended Hotels:**")
#                             for hname in result["hotels"]:
#                                 h_data = hotels[hotels["name"]==hname]
#                                 if not h_data.empty:
#                                     h = h_data.iloc[0]
#                                     st.write(f"🏨 **{h['name']}** — R{h['price']:,}/night ⭐ {h['rating']}")

#                         if result.get("best_time"):
#                             st.info(f"📅 Best time to visit: **{result['best_time']}**")

#                         # Show landmark on mini-map
#                         if result.get("lat") and result.get("lng"):
#                             lm_map = folium.Map(location=[result["lat"], result["lng"]], zoom_start=12)
#                             folium.Marker(
#                                 [result["lat"], result["lng"]],
#                                 tooltip=result["name"],
#                                 icon=folium.Icon(color="purple", icon="star", prefix="fa")
#                             ).add_to(lm_map)
#                             st.write("**📍 Location on Map:**")
#                             st_folium(lm_map, width=500, height=300)

#             elif manual_landmark != "Auto-detect":
#                 with ld_col2:
#                     info = LANDMARK_DB[manual_landmark]
#                     st.markdown(f"""
#                     <div class='landmark-card'>
#                         <h3 style='color:#a78bfa;'>🏛️ {manual_landmark}</h3>
#                         <p>📍 {info['city']}</p>
#                         <p>{info['description']}</p>
#                     </div>""", unsafe_allow_html=True)
#                     if info.get("activities"):
#                         st.write("**🎯 Activities:**")
#                         for act in info["activities"]: st.write(f"✅ {act}")
#                     if info.get("hotels"):
#                         st.write("**🏨 Nearby Hotels:**")
#                         for h in info["hotels"]: st.write(f"🏨 {h}")

#     # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#     # HOTEL MANAGER DASHBOARD
#     # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#     elif st.session_state.role == "Hotel Manager":
#         if not require_role(["Hotel Manager"]):
#             return

#         st.title("📊 Hotel Business Intelligence Console")
#         conn = sqlite3.connect("tourism_ai.db")
#         df = pd.read_sql("SELECT * FROM bookings", conn)
#         conn.close()

#         reviews_data = {
#             "hotel":        ["Cape Sun Resort","Sandton Palace","Durban Escape","Kruger Safari Lodge","Winelands Luxury Hotel"],
#             "positive":     [85,74,90,95,88],
#             "neutral":      [10,15,6,3,8],
#             "negative":     [5,11,4,2,4],
#             "satisfaction": [4.6,4.2,4.8,4.9,4.7],
#             "occupancy":    [85,78,70,95,82],
#         }

#         if not df.empty:
#             k1, k2, k3, k4 = st.columns(4)
#             k1.metric("💰 Revenue",       f"R{df['cost'].sum():,.2f}")
#             k2.metric("📅 Bookings",      len(df))
#             k3.metric("❌ Cancellations", len(df[df['status']=='Cancelled']))
#             k4.metric("🔄 Refunds",       len(df[df['status']=='Refunded']))

#         mgr_tabs = st.tabs([
#             "📈 Dashboard",
#             "🌦️ Destination Weather",
#             "🔍 Booking Management",
#             "🚩 Flagged Bookings",
#             "💡 Dynamic Pricing",
#             "🗺️ Hotel Map",
#             "📄 Report",
#         ])

#         # ── Manager Dashboard ──
#         with mgr_tabs[0]:
#             if not df.empty:
#                 st.plotly_chart(px.histogram(df, x="hotel", y="cost", color="hotel", title="Revenue by Hotel", template="plotly_dark"), use_container_width=True)
#                 combo = make_subplots(specs=[[{"secondary_y": True}]])
#                 combo.add_trace(go.Bar(x=reviews_data["hotel"], y=reviews_data["positive"], name="Positive %", marker_color='green'), secondary_y=False)
#                 combo.add_trace(go.Bar(x=reviews_data["hotel"], y=reviews_data["negative"], name="Negative %", marker_color='red'), secondary_y=False)
#                 combo.add_trace(go.Scatter(x=reviews_data["hotel"], y=reviews_data["satisfaction"], name="Satisfaction", mode="lines+markers", line=dict(color="cyan", width=3)), secondary_y=True)
#                 combo.update_layout(title="Sentiment & Satisfaction", template="plotly_dark", height=450, legend=dict(orientation="h"))
#                 st.plotly_chart(combo, use_container_width=True)
#                 df["risk"] = df.apply(lambda r: predict_cancellation(r["lead_time"], r["prev_cancels"]), axis=1)
#                 st.plotly_chart(px.pie(df["risk"].value_counts().reset_index().rename(columns={"risk":"Risk","count":"Count"}),
#                     names="Risk", values="Count", color="Risk",
#                     color_discrete_map={"High Risk":"#f87171","Low Risk":"#34d399"}, title="Cancellation Risk Split", template="plotly_dark"),
#                     use_container_width=True)
#             else:
#                 st.warning("No booking data yet.")

#         # ── Manager Weather ──
#         with mgr_tabs[1]:
#             st.subheader("🌦️ Live Weather — All Hotel Destinations")
#             for _, h in hotels.iterrows():
#                 ww = get_live_weather(h["city"])
#                 if ww:
#                     wc1, wc2 = st.columns([1, 3])
#                     wc1.subheader(h["name"])
#                     wc1.write(f"📍 {h['city']}")
#                     wc2.markdown(f"""
#                     <div class='weather-card' style='text-align:left;padding:16px;'>
#                         <b style='color:#38bdf8;font-size:1.4rem;'>{ww['temp']}°C</b>
#                         <span style='color:#94a3b8;'> · {ww['condition']}</span><br>
#                         Humidity: {ww['humidity']}% · Wind: {ww['wind_speed']} km/h · Pressure: {ww['pressure']} hPa
#                     </div>""", unsafe_allow_html=True)
#                     st.divider()

#         # ── Manager Booking Management ──
#         with mgr_tabs[2]:
#             st.subheader("🔍 Booking Management")
#             if not df.empty:
#                 col1, col2, col3 = st.columns(3)
#                 search_user  = col1.text_input("Search by User")
#                 search_hotel = col2.selectbox("Filter Hotel", ["All"] + hotels["name"].tolist())
#                 risk_filter  = col3.selectbox("AI Risk", ["All","High Risk","Low Risk"])
#                 filtered = df.copy()
#                 filtered["risk"] = filtered.apply(lambda r: predict_cancellation(r["lead_time"], r["prev_cancels"]), axis=1)
#                 if search_user:        filtered = filtered[filtered['user'].str.contains(search_user, case=False, na=False)]
#                 if search_hotel != "All": filtered = filtered[filtered['hotel'] == search_hotel]
#                 if risk_filter != "All":  filtered = filtered[filtered['risk'] == risk_filter]
#                 st.write(f"Showing **{len(filtered)}** bookings")
#                 for _, row in filtered.iterrows():
#                     risk_label   = row.get("risk", "N/A")
#                     status_color = "🔴" if row['status']=='Cancelled' else ("🟡" if row['status']=='Refunded' else "🟢")
#                     risk_color   = "🔴" if risk_label=="High Risk" else "🟢"
#                     st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
#                     cc1, cc2 = st.columns([4, 2])
#                     with cc1:
#                         st.write(f"**#{row['id']}** | {status_color} {row['status']} | 👤 {row['user']}")
#                         st.write(f"🏨 {row['hotel']}  •  📍 {row['city']}  •  💰 R{row['cost']:,.0f}")
#                         st.write(f"🗓️ {str(row['booking_date'])[:19]}  •  {risk_color} {risk_label}")
#                         if row.get('flagged', 0) == 1:
#                             st.markdown(f"<div class='flag-card'>🚩 {row.get('flag_reason','')}</div>", unsafe_allow_html=True)
#                     with cc2:
#                         if row['status'] == 'Active':
#                             if st.button("🚩 Flag", key=f"mgr_flag_{row['id']}"):
#                                 flag_booking(row['id'], "Flagged by Hotel Manager")
#                                 st.rerun()
#                     st.markdown("</div>", unsafe_allow_html=True)
#             else:
#                 st.warning("No bookings yet.")

#         # ── Manager Flagged ──
#         with mgr_tabs[3]:
#             st.subheader("🚩 Flagged Bookings")
#             if not df.empty and 'flagged' in df.columns:
#                 flagged_df = df[df['flagged'] == 1]
#                 if not flagged_df.empty:
#                     for _, row in flagged_df.iterrows():
#                         st.markdown("<div class='rank-danger'>", unsafe_allow_html=True)
#                         c1, c2 = st.columns([4, 2])
#                         with c1:
#                             st.write(f"**#{row['id']}** | 👤 {row['user']} | 🏨 {row['hotel']} | R{row['cost']:,.0f}")
#                             st.write(f"🚩 Reason: {row.get('flag_reason','Unknown')}")
#                         with c2:
#                             if st.button("✅ Clear", key=f"mgr_clr_{row['id']}"):
#                                 unflag_booking(row['id']); st.rerun()
#                         st.markdown("</div>", unsafe_allow_html=True)
#                 else:
#                     st.success("No flagged bookings!")

#         # ── Manager Dynamic Pricing ──
#         with mgr_tabs[4]:
#             st.subheader("💡 AI Dynamic Pricing")
#             p1i, p2i, p3i = st.columns(3)
#             base_price  = p1i.number_input("Base Price (ZAR)", 1000, 10000, 3000, step=100)
#             demand_lvl  = p2i.selectbox("Demand Level", ["Low","Medium","High"])
#             occ_pct     = p3i.slider("Occupancy %", 0, 100, 75)
#             s1i, s2i, s3i = st.columns(3)
#             season_t    = s1i.selectbox("Season", ["Off-Peak","Mid","Peak"])
#             is_holiday  = s2i.checkbox("Public Holiday?")
#             weather_n   = s3i.selectbox("Weather", ["Sunny ☀️","Cloudy ☁️","Rainy 🌧️","Humid 🌤️"])
#             ai_price    = dynamic_hotel_price(base_price, demand_lvl, occ_pct, season_t, is_holiday, weather_n)
#             delta_pct   = (ai_price - base_price) / base_price * 100
#             st.success(f"🤖 Recommended: **R{ai_price:,.2f}** (Base R{base_price:,} → {delta_pct:+.1f}%)")

#         # ── Manager Map ──
#         with mgr_tabs[5]:
#             st.subheader("🗺️ Hotel Locations — Management View")
#             mgr_map = build_hotel_map()
#             st_folium(mgr_map, width=900, height=500)

#         # ── Manager Report ──
#         with mgr_tabs[6]:
#             st.subheader("📄 Generate Business Report")
#             if not df.empty:
#                 if st.button("📊 Generate PDF Report"):
#                     with st.spinner("Building report..."):
#                         rfile = generate_detailed_report(df, reviews_data, hotels)
#                     if os.path.exists(rfile):
#                         st.success("✅ Report ready!")
#                         with open(rfile, "rb") as f:
#                             st.download_button("⬇️ Download Report", data=f,
#                                 file_name="AI_Hotel_Report.pdf", mime="application/pdf")
#             else:
#                 st.warning("No booking data yet.")

#     # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#     # ADMIN DASHBOARD
#     # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#     elif st.session_state.role == "Admin":
#         if not require_role(["Admin"]):
#             return

#         st.title("🛡️ Admin Control Center")
#         conn = sqlite3.connect("tourism_ai.db")
#         df = pd.read_sql("SELECT * FROM bookings", conn)
#         conn.close()

#         reviews_data = {
#             "hotel":        ["Cape Sun Resort","Sandton Palace","Durban Escape","Kruger Safari Lodge","Winelands Luxury Hotel"],
#             "positive":     [85,74,90,95,88], "neutral": [10,15,6,3,8], "negative": [5,11,4,2,4],
#             "satisfaction": [4.6,4.2,4.8,4.9,4.7], "occupancy": [85,78,70,95,82],
#         }

#         total_rev     = df['cost'].sum() if not df.empty else 0
#         cancelled_rev = df[df['status']=='Cancelled']['cost'].sum() if not df.empty else 0
#         refunded_rev  = df[df['status']=='Refunded']['cost'].sum() if not df.empty else 0
#         active_rev    = df[df['status']=='Active']['cost'].sum() if not df.empty else 0
#         high_risk     = 0
#         if not df.empty:
#             df["risk"] = df.apply(lambda r: predict_cancellation(r["lead_time"], r["prev_cancels"]), axis=1)
#             high_risk  = len(df[df["risk"]=="High Risk"])

#         k1,k2,k3,k4,k5,k6 = st.columns(6)
#         k1.metric("Total Bookings",  len(df))
#         k2.metric("Active Revenue",  f"R{active_rev:,.0f}")
#         k3.metric("Revenue Lost",    f"R{cancelled_rev+refunded_rev:,.0f}")
#         k4.metric("Cancellations",   len(df[df['status']=='Cancelled']) if not df.empty else 0)
#         k5.metric("Refunds",         len(df[df['status']=='Refunded'])  if not df.empty else 0)
#         k6.metric("⚠️ High Risk",    high_risk)

#         admin_tabs = st.tabs([
#             "📊 Analytics",
#             "🎛️ Booking Control",
#             "🏆 Performance Ranking",
#             "💸 Loss & Risk",
#             "🌦️ Weather Overview",
#             "🗺️ Hotel Map",
#             "👤 User Management",
#             "📄 Full Report",
#         ])

#         # ── Admin Analytics ──
#         with admin_tabs[0]:
#             if not df.empty:
#                 col1, col2 = st.columns(2)
#                 with col1:
#                     st.plotly_chart(px.histogram(df, x="hotel", y="cost", color="hotel", title="Revenue by Hotel", template="plotly_dark"), use_container_width=True)
#                     st.plotly_chart(px.pie(df, names="city", title="Bookings by City", template="plotly_dark"), use_container_width=True)
#                 with col2:
#                     st.plotly_chart(px.bar(
#                         pd.DataFrame({"Hotel":reviews_data["hotel"],"Positive":reviews_data["positive"],"Negative":reviews_data["negative"],"Neutral":reviews_data["neutral"]}),
#                         x="Hotel", y=["Positive","Negative","Neutral"], title="Sentiment Distribution", template="plotly_dark", barmode="stack"
#                     ), use_container_width=True)
#                     occ_df = pd.DataFrame({"Hotel":reviews_data["hotel"],"Occupancy":reviews_data["occupancy"]})
#                     fig_occ = px.bar(occ_df, x="Hotel", y="Occupancy", title="Occupancy by Hotel", template="plotly_dark",
#                                      color="Occupancy", color_continuous_scale=["red","yellow","green"])
#                     fig_occ.add_hline(y=80, line_dash="dash", line_color="orange", annotation_text="80% threshold")
#                     st.plotly_chart(fig_occ, use_container_width=True)
#                 st.dataframe(df.sort_values('booking_date', ascending=False), use_container_width=True, hide_index=True)
#             else:
#                 st.warning("No booking data yet.")

#         # ── Admin Booking Control ──
#         with admin_tabs[1]:
#             st.subheader("🎛️ Booking Control Panel")
#             if not df.empty:
#                 col1, col2 = st.columns(2)
#                 search    = col1.text_input("🔍 Search")
#                 status_f  = col2.selectbox("Status", ["All","Active","Cancelled","Refunded"])
#                 display_df = df.copy()
#                 if search:
#                     display_df = display_df[
#                         display_df['user'].str.contains(search, case=False, na=False) |
#                         display_df['hotel'].str.contains(search, case=False, na=False) |
#                         display_df['id'].astype(str).str.contains(search)]
#                 if status_f != "All":
#                     display_df = display_df[display_df['status'] == status_f]
#                 st.write(f"Showing **{len(display_df)}** bookings")
#                 for _, row in display_df.iterrows():
#                     status_icon = "🟢" if row['status']=='Active' else ("🔴" if row['status']=='Cancelled' else "🟡")
#                     risk_label  = row.get("risk","N/A") if "risk" in df.columns else "N/A"
#                     st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
#                     c1,c2,c3,c4 = st.columns([4,2,2,2])
#                     with c1:
#                         st.write(f"**#{row['id']}** {status_icon} {row['status']} | 👤 {row['user']}")
#                         st.write(f"🏨 {row['hotel']} · 📍 {row['city']} · 💰 R{row['cost']:,.2f}")
#                         if row.get('flagged',0): st.markdown(f"<div class='flag-card'>🚩 {row.get('flag_reason','')}</div>", unsafe_allow_html=True)
#                     with c2:
#                         if row['status']=='Active':
#                             if st.button("❌ Cancel", key=f"adm_cancel_{row['id']}"):
#                                 cancel_booking(row['id']); st.rerun()
#                         if row['status'] in ['Active','Cancelled'] and not row.get('refunded',0):
#                             if st.button("💸 Refund", key=f"adm_refund_{row['id']}"):
#                                 refund_booking(row['id']); st.rerun()
#                     with c3:
#                         if row['status'] == 'Active':
#                             new_h = st.selectbox("Reassign", ["—"]+hotels["name"].tolist(), key=f"adm_rs_{row['id']}")
#                             if new_h != "—":
#                                 hr = hotels[hotels["name"]==new_h].iloc[0]
#                                 if st.button("🔁", key=f"adm_rsbtn_{row['id']}"):
#                                     reassign_booking(row['id'], new_h, hr['city'], hr['price']); st.rerun()
#                     with c4:
#                         with st.expander("✏️ Edit"):
#                             nu = st.text_input("User", value=row['user'], key=f"adm_eu_{row['id']}")
#                             nc = st.number_input("Cost", value=float(row['cost']), key=f"adm_ec_{row['id']}")
#                             if st.button("Save", key=f"adm_sv_{row['id']}"):
#                                 edit_booking(row['id'], nu, row['hotel'], row['city'], nc); st.rerun()
#                         if not row.get('flagged',0):
#                             if st.button("🚩 Flag", key=f"adm_flg_{row['id']}"):
#                                 flag_booking(row['id'], "Flagged by Admin"); st.rerun()
#                         else:
#                             if st.button("✅ Unflag", key=f"adm_uflg_{row['id']}"):
#                                 unflag_booking(row['id']); st.rerun()
#                     st.markdown("</div>", unsafe_allow_html=True)
#             else:
#                 st.warning("No bookings yet.")

#         # ── Admin Performance Ranking ──
#         with admin_tabs[2]:
#             st.subheader("🏆 Hotel Performance Ranking")
#             ranked = rank_hotels(hotels, df if not df.empty else pd.DataFrame())
#             for i, (_, row) in enumerate(ranked.iterrows()):
#                 tier  = row['Tier']
#                 css   = "rank-gold" if "Top" in tier else ("rank-silver" if "Average" in tier else "rank-danger")
#                 st.markdown(f"<div class='{css}'>", unsafe_allow_html=True)
#                 cc1,cc2,cc3,cc4,cc5 = st.columns([1,3,2,2,2])
#                 cc1.markdown(f"### #{i+1}")
#                 cc2.write(f"**{row['Hotel']}** · {row['City']}\n{tier}")
#                 cc3.metric("Score",     row['Score'])
#                 cc4.metric("Occupancy", f"{row['Occupancy']}%")
#                 cc5.metric("Sentiment", f"{row['Sentiment']}%")
#                 st.markdown("</div>", unsafe_allow_html=True)
#             st.plotly_chart(px.bar(ranked, x="Hotel", y="Score", color="Tier",
#                 color_discrete_map={"🏆 Top Performer":"#fbbf24","⚠️ Average":"#94a3b8","❌ Underperforming":"#f87171"},
#                 title="Hotel Performance Composite Score", template="plotly_dark", text="Score"), use_container_width=True)

#         # ── Admin Loss & Risk ──
#         with admin_tabs[3]:
#             st.subheader("💸 Revenue Loss & Risk")
#             if not df.empty:
#                 col1, col2 = st.columns(2)
#                 with col1:
#                     sr = df.groupby("status")["cost"].sum().reset_index()
#                     sr.columns = ["Status","Revenue"]
#                     fig_loss = px.bar(sr, x="Status", y="Revenue", color="Status",
#                         color_discrete_map={"Active":"#34d399","Cancelled":"#f87171","Refunded":"#f59e0b"},
#                         title="Revenue by Booking Status", template="plotly_dark", text="Revenue")
#                     fig_loss.update_traces(texttemplate="R%{text:,.0f}", textposition="outside")
#                     st.plotly_chart(fig_loss, use_container_width=True)
#                     total_loss = cancelled_rev + refunded_rev
#                     st.markdown(f"""
#                     <div class='rank-danger'>
#                         <b>💸 Revenue Loss Summary</b><br>
#                         Cancellations: R{cancelled_rev:,.2f}<br>
#                         Refunds: R{refunded_rev:,.2f}<br>
#                         <b>Total: R{total_loss:,.2f} ({total_loss/max(total_rev,1)*100:.1f}%)</b>
#                     </div>""", unsafe_allow_html=True)
#                 with col2:
#                     rc = df["risk"].value_counts().reset_index()
#                     rc.columns = ["Risk","Count"]
#                     st.plotly_chart(px.pie(rc, names="Risk", values="Count", color="Risk",
#                         color_discrete_map={"High Risk":"#f87171","Low Risk":"#34d399"},
#                         title="Cancellation Risk Split", template="plotly_dark"), use_container_width=True)
#             else:
#                 st.warning("No booking data.")

#         # ── Admin Weather Overview ──
#         with admin_tabs[4]:
#             st.subheader("🌦️ Platform-Wide Weather Dashboard")
#             all_cities = ["Cape Town","Johannesburg","Durban","Kruger Park","Stellenbosch","Pretoria","Port Elizabeth","Knysna"]
#             wdata = []
#             for city in all_cities:
#                 ww = get_live_weather(city)
#                 if ww:
#                     wdata.append({"City": city, **ww})
#             if wdata:
#                 wdf = pd.DataFrame(wdata)
#                 col1, col2 = st.columns(2)
#                 col1.plotly_chart(px.bar(wdf, x="City", y="temp", color="City",
#                     title="Temperature Across SA", template="plotly_dark", labels={"temp":"°C"}), use_container_width=True)
#                 col2.plotly_chart(px.bar(wdf, x="City", y="humidity", color="City",
#                     title="Humidity %", template="plotly_dark"), use_container_width=True)
#                 st.dataframe(wdf[["City","temp","feels_like","humidity","wind_speed","condition","pressure","visibility"]],
#                     use_container_width=True, hide_index=True)

#         # ── Admin Hotel Map ──
#         with admin_tabs[5]:
#             st.subheader("🗺️ Admin Hotel Map View")
#             adm_map = build_hotel_map()
#             st_folium(adm_map, width=1000, height=550)

#         # ── FEATURE 6 — User Management ──
#         with admin_tabs[6]:
#             st.subheader("👤 User Management & Access Control")
#             users_df = get_all_users()

#             # Summary
#             u1,u2,u3,u4 = st.columns(4)
#             u1.metric("Total Users",   len(users_df))
#             u2.metric("Tourists",      len(users_df[users_df['role']=='Tourist']))
#             u3.metric("Managers",      len(users_df[users_df['role']=='Hotel Manager']))
#             u4.metric("Admins",        len(users_df[users_df['role']=='Admin']))

#             # User table
#             st.write("**All Platform Users**")
#             for _, u in users_df.iterrows():
#                 is_active = bool(u.get('is_active', 1))
#                 badge_css = "rank-gold" if u['role']=='Admin' else ("rank-silver" if u['role']=='Hotel Manager' else "metric-card")
#                 st.markdown(f"<div class='{badge_css}'>", unsafe_allow_html=True)
#                 uc1,uc2,uc3,uc4 = st.columns([3,2,2,1])
#                 with uc1:
#                     st.write(f"**{u['full_name']}** (@{u['username']})")
#                     st.write(f"📧 {u.get('email','N/A')} | 🕐 Last login: {str(u.get('last_login','Never'))[:16]}")
#                 with uc2:
#                     st.write(f"**Role:** {u['role']}")
#                     st.write(f"**Status:** {'🟢 Active' if is_active else '🔴 Inactive'}")
#                 with uc3:
#                     st.write(f"**Created:** {str(u.get('created_at',''))[:10]}")
#                 with uc4:
#                     if u['username'] != st.session_state.user:  # Can't toggle yourself
#                         new_status = 0 if is_active else 1
#                         btn_label = "🔴 Deactivate" if is_active else "🟢 Activate"
#                         if st.button(btn_label, key=f"usr_toggle_{u['id']}"):
#                             toggle_user_status(u['id'], new_status); st.rerun()
#                 st.markdown("</div>", unsafe_allow_html=True)

#             # Create new user
#             st.divider()
#             st.subheader("➕ Create New User")
#             with st.expander("Add User"):
#                 nu1, nu2 = st.columns(2)
#                 new_username  = nu1.text_input("Username",   key="nu_username")
#                 new_password  = nu2.text_input("Password",   type="password", key="nu_password")
#                 new_full_name = nu1.text_input("Full Name",  key="nu_fullname")
#                 new_email     = nu2.text_input("Email",      key="nu_email")
#                 new_role      = st.selectbox("Role", ["Tourist","Hotel Manager","Admin"], key="nu_role")
#                 if st.button("Create User"):
#                     if new_username and new_password:
#                         ok, msg = create_user(new_username, new_password, new_role, new_email, new_full_name)
#                         if ok: st.success(f"✅ {msg}")
#                         else:  st.error(f"❌ {msg}")
#                     else:
#                         st.warning("Username and password are required.")

#             # Role permission matrix
#             st.divider()
#             st.subheader("🔐 Role Permission Matrix")
#             perm_data = {
#                 "Feature":               ["Hotel Booking", "Weather Data", "AI Chatbot", "Landmark Detection", "Hotel Map",
#                                           "View Reviews", "Booking Management", "Flag Bookings", "Dynamic Pricing",
#                                           "Analytics Dashboard", "User Management", "Generate Reports", "Cancel/Refund Bookings"],
#                 "Tourist 🌍":            ["✅","✅","✅","✅","✅","✅","❌","❌","❌","❌","❌","❌","❌"],
#                 "Hotel Manager 🏨":      ["❌","✅","❌","❌","✅","✅","✅","✅","✅","✅","❌","✅","❌"],
#                 "Admin 🛡️":             ["✅","✅","✅","✅","✅","✅","✅","✅","✅","✅","✅","✅","✅"],
#             }
#             st.dataframe(pd.DataFrame(perm_data), use_container_width=True, hide_index=True)

#         # ── Admin Full Report ──
#         with admin_tabs[7]:
#             st.subheader("📄 Full Executive Report")
#             if not df.empty:
#                 if st.button("🚀 Generate Complete PDF Report"):
#                     with st.spinner("Building 8-page report..."):
#                         rfile = generate_detailed_report(df, reviews_data, hotels)
#                     if os.path.exists(rfile):
#                         st.success("✅ Complete report ready!")
#                         with open(rfile, "rb") as f:
#                             st.download_button("⬇️ Download Full Report", data=f,
#                                 file_name="AI_Smart_Tourism_Report.pdf", mime="application/pdf")
#             else:
#                 st.warning("No booking data yet.")

#     # ── Logout ──
#     if st.session_state.role:
#         st.sidebar.divider()
#         if st.sidebar.button("🚪 Logout"):
#             for k in ["role","user","user_id","full_name","chat_history"]:
#                 st.session_state[k] = None if k != "chat_history" else []
#             st.session_state.role = None
#             st.rerun()


# # ======================================================
# # PDF REPORT GENERATOR (condensed)
# # ======================================================

# def generate_detailed_report(df, reviews_data, hotels_df):
#     chart_paths = []

#     def make_chart(func):
#         p = tempfile.mktemp(suffix=".png")
#         chart_paths.append(p)
#         func(p)
#         return p

#     def dark_fig(w=9, h=4):
#         f, a = plt.subplots(figsize=(w, h))
#         f.patch.set_facecolor("#0f172a"); a.set_facecolor("#1e293b")
#         a.tick_params(colors="white"); a.spines[:].set_color("#334155")
#         return f, a

#     def p1_chart(p):
#         rb = df.groupby("hotel")["cost"].sum().reset_index() if not df.empty else pd.DataFrame({"hotel":reviews_data["hotel"],"cost":[0]*5})
#         f,a = dark_fig()
#         bars = a.bar(rb["hotel"], rb["cost"], color=["#ff6e40","#38bdf8","#34d399","#f59e0b","#a78bfa"])
#         a.set_title("Revenue by Hotel", color="white", fontsize=13, pad=10); a.set_ylabel("Revenue (ZAR)", color="white")
#         for b in bars: a.text(b.get_x()+b.get_width()/2, b.get_height()+200, f"R{b.get_height():,.0f}", ha="center", color="white", fontsize=8)
#         plt.xticks(rotation=20, ha="right"); plt.tight_layout(); plt.savefig(p, dpi=120, bbox_inches="tight", facecolor=f.get_facecolor()); plt.close(f)

#     def p2_chart(p):
#         f,a = dark_fig()
#         x = np.arange(len(reviews_data["hotel"])); w=0.5
#         a.bar(x, reviews_data["positive"], w, label="Positive", color="#34d399")
#         a.bar(x, reviews_data["negative"], w, bottom=reviews_data["positive"], label="Negative", color="#f87171")
#         a.set_xticks(x); a.set_xticklabels(reviews_data["hotel"], rotation=20, ha="right", color="white", fontsize=8)
#         a.set_title("Guest Sentiment", color="white", fontsize=13); a.legend(facecolor="#1e293b", labelcolor="white")
#         plt.tight_layout(); plt.savefig(p, dpi=120, bbox_inches="tight", facecolor=f.get_facecolor()); plt.close(f)

#     def p3_chart(p):
#         f,a = dark_fig()
#         a.plot(reviews_data["hotel"], reviews_data["satisfaction"], marker="o", color="#38bdf8", linewidth=2.5, markersize=8)
#         a.set_ylim(1,5.5); a.set_title("Guest Satisfaction", color="white", fontsize=13); a.set_ylabel("Score", color="white")
#         plt.xticks(rotation=20, ha="right"); plt.tight_layout(); plt.savefig(p, dpi=120, bbox_inches="tight", facecolor=f.get_facecolor()); plt.close(f)

#     def p4_chart(p):
#         occ = reviews_data.get("occupancy", [75,82,91,68,88])
#         f,a = dark_fig()
#         a.fill_between(reviews_data["hotel"], occ, alpha=0.2, color="#a78bfa")
#         a.plot(reviews_data["hotel"], occ, marker="s", color="#a78bfa", linewidth=2.5, markersize=8)
#         a.axhline(80, color="#f59e0b", linestyle="--", linewidth=1.5, label="80% Threshold")
#         a.set_title("Occupancy Forecast", color="white", fontsize=13); a.set_ylabel("Occupancy %", color="white")
#         a.legend(facecolor="#1e293b", labelcolor="white"); plt.xticks(rotation=20, ha="right")
#         plt.tight_layout(); plt.savefig(p, dpi=120, bbox_inches="tight", facecolor=f.get_facecolor()); plt.close(f)

#     p1 = make_chart(p1_chart)
#     p2 = make_chart(p2_chart)
#     p3 = make_chart(p3_chart)
#     p4 = make_chart(p4_chart)

#     pdf = FPDF()
#     pdf.set_auto_page_break(auto=True, margin=15)

#     def sec(t): pdf.set_font("Arial","B",13); pdf.set_text_color(255,110,64); pdf.cell(0,9,safe(t),ln=True); pdf.set_text_color(40,40,40); pdf.ln(2)
#     def body(t): pdf.set_font("Arial","",10); pdf.set_text_color(40,40,40); pdf.multi_cell(0,6,safe(t)); pdf.ln(2)
#     def img(p, w=180):
#         if os.path.exists(p): pdf.image(p, x=15, w=w)
#         pdf.ln(3)

#     # Cover
#     pdf.add_page()
#     pdf.set_fill_color(15,23,42); pdf.rect(0,0,210,297,"F")
#     pdf.set_y(60); pdf.set_font("Arial","B",26); pdf.set_text_color(255,110,64)
#     pdf.cell(0,14,safe("AI SMART TOURISM ZA"), ln=True, align="C")
#     pdf.set_font("Arial","B",14); pdf.set_text_color(255,255,255)
#     pdf.cell(0,9,safe("Executive Analytics Report"), ln=True, align="C")
#     pdf.set_font("Arial","",10); pdf.set_text_color(148,163,184)
#     pdf.cell(0,7,safe(f"Generated: {datetime.now().strftime('%d %B %Y  |  %H:%M')}"), ln=True, align="C")
#     total_rev = df['cost'].sum() if not df.empty else 0
#     pdf.ln(12); pdf.set_font("Arial","B",11); pdf.set_text_color(56,189,248)
#     for line in [f"Total Bookings: {len(df)}", f"Total Revenue: R{total_rev:,.2f}",
#                  f"Hotels Monitored: {len(reviews_data['hotel'])}", f"Avg Satisfaction: {np.mean(reviews_data['satisfaction']):.2f}/5.0"]:
#         pdf.cell(0,8,safe(line),ln=True,align="C")

#     # Charts page
#     pdf.add_page()
#     pdf.set_font("Arial","B",14); pdf.set_text_color(255,110,64)
#     pdf.cell(0,10,safe("Analytics Overview"),ln=True,align="C"); pdf.ln(2)
#     pdf.set_text_color(30,30,30)
#     for cp in [p1,p2,p3,p4]: img(cp)

#     # Recommendations
#     pdf.add_page()
#     sec("Key Performance Indicators")
#     if not df.empty:
#         best = df.groupby("hotel")["cost"].sum().idxmax()
#         body(f"Top hotel by revenue: {best}. Total revenue: R{total_rev:,.2f}. Bookings: {len(df)}.")
#     sec("Strategic Recommendations")
#     body("1. Deploy AI Dynamic Pricing during peak seasons (Dec, Jan, Jul) for 15-30% revenue uplift.")
#     body("2. Implement non-refundable rate tiers to reduce cancellation losses.")
#     body("3. Properties with >10% negative sentiment need immediate service audits.")
#     body("4. Target below-80% occupancy hotels with corporate packages and mid-week deals.")
#     body("5. Capture email and satisfaction data on all bookings to improve AI model accuracy.")

#     report_path = os.path.join(tempfile.gettempdir(), "AI_Hotel_Business_Report.pdf")
#     pdf.output(report_path)
#     for p in chart_paths:
#         try: os.remove(p)
#         except: pass
#     return report_path


# if __name__ == "__main__":
#     main()




import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import sqlite3
import hashlib
import requests
import base64
from datetime import datetime, timedelta
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from wordcloud import WordCloud
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from textblob import TextBlob
from PIL import Image
from fpdf import FPDF
import folium
from streamlit_folium import st_folium
from plotly.subplots import make_subplots
import tempfile
import os
import io
import json

# ======================================================
# PAGE CONFIG
# ======================================================

st.set_page_config(
    page_title="Smart Tourism-travel ZA",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ======================================================
# API KEYS — Replace with your actual keys
# ======================================================

OPENWEATHER_API_KEY = st.secrets.get("OPENWEATHER_API_KEY", "YOUR_OPENWEATHER_KEY")
GOOGLE_MAPS_API_KEY = st.secrets.get("GOOGLE_MAPS_API_KEY", "YOUR_GOOGLE_MAPS_KEY")
GOOGLE_VISION_API_KEY = st.secrets.get("GOOGLE_VISION_API_KEY", "YOUR_GOOGLE_VISION_KEY")
GOOGLE_PLACES_API_KEY = st.secrets.get("GOOGLE_PLACES_API_KEY", "YOUR_GOOGLE_PLACES_KEY")
OPENAI_API_KEY = st.secrets.get("OPENAI_API_KEY", "YOUR_OPENAI_KEY")
ANTHROPIC_API_KEY = st.secrets.get("ANTHROPIC_API_KEY", "YOUR_ANTHROPIC_KEY")

# ======================================================
# PROFESSIONAL UI STYLING
# ======================================================

def apply_styles():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

    .stApp {
        background: linear-gradient(135deg, #0a0f1e 0%, #0f172a 50%, #1a0a2e 100%);
        color: white;
        font-family: 'DM Sans', sans-serif;
    }
    h1, h2, h3, h4 {
        font-family: 'Syne', sans-serif !important;
        color: white !important;
        letter-spacing: -0.02em;
    }
    .hero {
        background: linear-gradient(135deg, rgba(255,110,64,0.12), rgba(56,189,248,0.08));
        backdrop-filter: blur(20px);
        padding: 40px;
        border-radius: 24px;
        text-align: center;
        border: 1px solid rgba(255,110,64,0.2);
        box-shadow: 0 0 60px rgba(255,110,64,0.08), 0 8px 32px rgba(0,0,0,0.4);
        margin-bottom: 28px;
    }
    .metric-card {
        background: rgba(255,255,255,0.04);
        backdrop-filter: blur(16px);
        border-radius: 20px;
        padding: 22px;
        margin-bottom: 16px;
        border: 1px solid rgba(255,255,255,0.08);
        transition: all 0.3s cubic-bezier(0.4,0,0.2,1);
        box-shadow: 0 4px 24px rgba(0,0,0,0.3);
    }
    .metric-card:hover {
        transform: translateY(-4px);
        border-color: rgba(255,110,64,0.3);
        box-shadow: 0 12px 32px rgba(255,110,64,0.15);
    }
    .weather-card {
        background: linear-gradient(135deg, rgba(56,189,248,0.15), rgba(14,165,233,0.08));
        border: 1px solid rgba(56,189,248,0.3);
        border-radius: 20px;
        padding: 24px;
        margin: 12px 0;
        text-align: center;
    }
    .forecast-card {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(56,189,248,0.2);
        border-radius: 14px;
        padding: 14px;
        text-align: center;
        margin: 6px 0;
    }
    .chat-bubble-user {
        background: linear-gradient(135deg, #ff6e40, #ff3d00);
        border-radius: 18px 18px 4px 18px;
        padding: 12px 18px;
        margin: 8px 0 8px 40px;
        color: white;
        font-size: 0.95rem;
    }
    .chat-bubble-bot {
        background: rgba(56,189,248,0.12);
        border: 1px solid rgba(56,189,248,0.25);
        border-radius: 18px 18px 18px 4px;
        padding: 12px 18px;
        margin: 8px 40px 8px 0;
        color: white;
        font-size: 0.95rem;
    }
    .landmark-card {
        background: linear-gradient(135deg, rgba(167,139,250,0.12), rgba(139,92,246,0.06));
        border: 1px solid rgba(167,139,250,0.3);
        border-radius: 20px;
        padding: 24px;
        margin: 12px 0;
    }
    .hotel-image-card {
        border-radius: 16px;
        overflow: hidden;
        margin-bottom: 12px;
        border: 1px solid rgba(255,255,255,0.08);
    }
    .rank-gold {
        background: linear-gradient(135deg, rgba(251,191,36,0.15), rgba(245,158,11,0.08));
        border: 1px solid rgba(251,191,36,0.3);
        border-radius: 16px;
        padding: 16px 20px;
        margin: 8px 0;
    }
    .rank-silver {
        background: linear-gradient(135deg, rgba(148,163,184,0.12), rgba(100,116,139,0.06));
        border: 1px solid rgba(148,163,184,0.25);
        border-radius: 16px;
        padding: 16px 20px;
        margin: 8px 0;
    }
    .rank-danger {
        background: linear-gradient(135deg, rgba(239,68,68,0.12), rgba(185,28,28,0.06));
        border: 1px solid rgba(239,68,68,0.25);
        border-radius: 16px;
        padding: 16px 20px;
        margin: 8px 0;
    }
    .flag-card {
        background: rgba(239,68,68,0.1);
        border: 1px solid rgba(239,68,68,0.3);
        border-radius: 12px;
        padding: 12px 16px;
        margin: 6px 0;
    }
    .role-badge-tourist {
        background: linear-gradient(135deg, #34d399, #059669);
        padding: 4px 14px; border-radius: 20px; font-size: 0.8rem; font-weight: 600;
    }
    .role-badge-manager {
        background: linear-gradient(135deg, #38bdf8, #0284c7);
        padding: 4px 14px; border-radius: 20px; font-size: 0.8rem; font-weight: 600;
    }
    .role-badge-admin {
        background: linear-gradient(135deg, #f59e0b, #d97706);
        padding: 4px 14px; border-radius: 20px; font-size: 0.8rem; font-weight: 600;
    }
    .stButton>button {
        background: linear-gradient(135deg, #ff6e40, #ff3d00);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 10px 24px;
        font-weight: 600;
        font-family: 'DM Sans', sans-serif;
        letter-spacing: 0.02em;
        transition: all 0.2s;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255,110,64,0.4);
    }
    section[data-testid="stSidebar"] {
        background: rgba(10,15,30,0.8);
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255,255,255,0.06);
    }
    .stTabs [data-baseweb="tab"] {
        font-family: 'DM Sans', sans-serif;
        font-weight: 500;
    }
    .access-denied {
        background: rgba(239,68,68,0.1);
        border: 1px solid rgba(239,68,68,0.3);
        border-radius: 16px;
        padding: 32px;
        text-align: center;
        margin: 40px auto;
    }
    </style>
    """, unsafe_allow_html=True)

# ======================================================
# DATABASE — Extended schema with users table
# ======================================================

def init_db():
    conn = sqlite3.connect("tourism_ai.db")
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL,
            email TEXT,
            full_name TEXT,
            created_at TEXT,
            last_login TEXT,
            is_active INTEGER DEFAULT 1
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT,
            hotel TEXT,
            city TEXT,
            cost REAL,
            booking_date TEXT,
            lead_time INTEGER,
            prev_cancels INTEGER,
            satisfaction INTEGER,
            status TEXT DEFAULT 'Active',
            refunded INTEGER DEFAULT 0,
            flagged INTEGER DEFAULT 0,
            flag_reason TEXT DEFAULT ''
        )
    ''')

    for col, definition in [
        ("status", "TEXT DEFAULT 'Active'"),
        ("refunded", "INTEGER DEFAULT 0"),
        ("flagged", "INTEGER DEFAULT 0"),
        ("flag_reason", "TEXT DEFAULT ''"),
    ]:
        try:
            c.execute(f"ALTER TABLE bookings ADD COLUMN {col} {definition}")
        except Exception:
            pass

    c.execute("SELECT COUNT(*) FROM users")
    if c.fetchone()[0] == 0:
        default_users = [
            ("tourist1",  hash_password("tourist123"),  "Tourist",       "tourist@example.com",  "John Traveller"),
            ("manager1",  hash_password("manager123"),  "Hotel Manager", "manager@example.com",  "Sarah Manager"),
            ("admin1",    hash_password("admin123"),    "Admin",         "admin@example.com",    "System Admin"),
            ("tourist2",  hash_password("password"),    "Tourist",       "t2@example.com",       "Jane Explorer"),
        ]
        for u in default_users:
            c.execute("INSERT INTO users (username,password_hash,role,email,full_name,created_at) VALUES (?,?,?,?,?,?)",
                      (*u, str(datetime.now())))

    conn.commit()
    conn.close()

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate_user(username: str, password: str):
    conn = sqlite3.connect("tourism_ai.db")
    c = conn.cursor()
    c.execute("SELECT id, username, role, full_name, is_active FROM users WHERE username=? AND password_hash=?",
              (username, hash_password(password)))
    user = c.fetchone()
    if user and user[4] == 1:
        c.execute("UPDATE users SET last_login=? WHERE username=?", (str(datetime.now()), username))
        conn.commit()
    conn.close()
    return user

def create_user(username, password, role, email, full_name):
    conn = sqlite3.connect("tourism_ai.db")
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username,password_hash,role,email,full_name,created_at) VALUES (?,?,?,?,?,?)",
                  (username, hash_password(password), role, email, full_name, str(datetime.now())))
        conn.commit()
        return True, "User created successfully"
    except sqlite3.IntegrityError:
        return False, "Username already exists"
    finally:
        conn.close()

def get_all_users():
    conn = sqlite3.connect("tourism_ai.db")
    df = pd.read_sql("SELECT id,username,role,email,full_name,created_at,last_login,is_active FROM users", conn)
    conn.close()
    return df

def toggle_user_status(user_id, is_active):
    conn = sqlite3.connect("tourism_ai.db")
    c = conn.cursor()
    c.execute("UPDATE users SET is_active=? WHERE id=?", (is_active, user_id))
    conn.commit()
    conn.close()

# ======================================================
# SAVE / ADMIN BOOKING OPERATIONS
# ======================================================

def save_booking(user, hotel, city, cost):
    conn = sqlite3.connect("tourism_ai.db")
    c = conn.cursor()
    c.execute(
        "INSERT INTO bookings (user,hotel,city,cost,booking_date,lead_time,prev_cancels,satisfaction,status,refunded,flagged,flag_reason) VALUES (?,?,?,?,?,?,?,?,'Active',0,0,'')",
        (user, hotel, city, cost, str(datetime.now()),
         np.random.randint(1, 60), np.random.randint(0, 3), np.random.randint(1, 6))
    )
    conn.commit()
    conn.close()

def cancel_booking(bid):
    _exec_booking_update("UPDATE bookings SET status='Cancelled' WHERE id=?", (bid,))

def refund_booking(bid):
    _exec_booking_update("UPDATE bookings SET status='Refunded',refunded=1 WHERE id=?", (bid,))

def reassign_booking(bid, new_hotel, new_city, new_cost):
    _exec_booking_update("UPDATE bookings SET hotel=?,city=?,cost=? WHERE id=?", (new_hotel, new_city, new_cost, bid))

def edit_booking(bid, user, hotel, city, cost):
    _exec_booking_update("UPDATE bookings SET user=?,hotel=?,city=?,cost=? WHERE id=?", (user, hotel, city, cost, bid))

def flag_booking(bid, reason):
    _exec_booking_update("UPDATE bookings SET flagged=1,flag_reason=? WHERE id=?", (reason, bid))

def unflag_booking(bid):
    _exec_booking_update("UPDATE bookings SET flagged=0,flag_reason='' WHERE id=?", (bid,))

def _exec_booking_update(sql, params):
    conn = sqlite3.connect("tourism_ai.db")
    conn.execute(sql, params)
    conn.commit()
    conn.close()

# ======================================================
# FEATURE 1 — REAL-TIME WEATHER API
# ======================================================

def get_live_weather(city: str, country_code: str = "ZA"):
    if OPENWEATHER_API_KEY == "YOUR_OPENWEATHER_KEY":
        mock = {
            "Cape Town":    {"temp": 22, "feels_like": 21, "humidity": 65, "wind_speed": 14, "condition": "Partly Cloudy", "icon": "02d", "pressure": 1015, "visibility": 10},
            "Johannesburg": {"temp": 26, "feels_like": 25, "humidity": 45, "wind_speed": 18, "condition": "Clear Sky",    "icon": "01d", "pressure": 1012, "visibility": 10},
            "Durban":       {"temp": 28, "feels_like": 30, "humidity": 78, "wind_speed": 12, "condition": "Humid",         "icon": "03d", "pressure": 1010, "visibility": 8 },
            "Kruger Park":  {"temp": 31, "feels_like": 34, "humidity": 40, "wind_speed": 8,  "condition": "Hot & Sunny",  "icon": "01d", "pressure": 1008, "visibility": 10},
            "Stellenbosch": {"temp": 20, "feels_like": 19, "humidity": 60, "wind_speed": 10, "condition": "Sunny",        "icon": "01d", "pressure": 1016, "visibility": 10},
            "Pretoria":     {"temp": 27, "feels_like": 26, "humidity": 50, "wind_speed": 15, "condition": "Clear",        "icon": "01d", "pressure": 1011, "visibility": 10},
            "Port Elizabeth":{"temp": 19,"feels_like": 18, "humidity": 70, "wind_speed": 20, "condition": "Windy",        "icon": "04d", "pressure": 1013, "visibility": 9 },
            "Knysna":       {"temp": 21, "feels_like": 20, "humidity": 68, "wind_speed": 11, "condition": "Partly Cloudy","icon": "02d", "pressure": 1014, "visibility": 10},
        }
        return mock.get(city, {"temp": 24, "feels_like": 23, "humidity": 55, "wind_speed": 12, "condition": "Clear", "icon": "01d", "pressure": 1013, "visibility": 10})

    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city},{country_code}&appid={OPENWEATHER_API_KEY}&units=metric"
        r = requests.get(url, timeout=8)
        data = r.json()
        if r.status_code == 200:
            return {
                "temp":       round(data["main"]["temp"]),
                "feels_like": round(data["main"]["feels_like"]),
                "humidity":   data["main"]["humidity"],
                "wind_speed": round(data["wind"]["speed"] * 3.6, 1),
                "condition":  data["weather"][0]["description"].title(),
                "icon":       data["weather"][0]["icon"],
                "pressure":   data["main"]["pressure"],
                "visibility": round(data.get("visibility", 10000) / 1000, 1),
            }
    except Exception as e:
        st.error(f"Weather API error: {e}")
    return None

def get_weather_forecast(city: str, country_code: str = "ZA"):
    if OPENWEATHER_API_KEY == "YOUR_OPENWEATHER_KEY":
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        icons = ["01d", "02d", "03d", "01d", "04d"]
        temps = [24, 26, 22, 28, 23]
        descs = ["Sunny", "Partly Cloudy", "Cloudy", "Clear", "Overcast"]
        return [{"day": d, "temp": t, "icon": i, "desc": desc, "humidity": np.random.randint(40, 80)}
                for d, t, i, desc in zip(days, temps, icons, descs)]
    try:
        url = f"https://api.openweathermap.org/data/2.5/forecast?q={city},{country_code}&appid={OPENWEATHER_API_KEY}&units=metric&cnt=40"
        r = requests.get(url, timeout=8)
        if r.status_code == 200:
            data = r.json()
            daily = {}
            for item in data["list"]:
                date = item["dt_txt"][:10]
                if date not in daily or "12:00" in item["dt_txt"]:
                    daily[date] = {
                        "day":      datetime.strptime(date, "%Y-%m-%d").strftime("%A"),
                        "temp":     round(item["main"]["temp"]),
                        "icon":     item["weather"][0]["icon"],
                        "desc":     item["weather"][0]["description"].title(),
                        "humidity": item["main"]["humidity"],
                    }
            return list(daily.values())[:5]
    except Exception:
        pass
    return []

def weather_icon_url(icon_code: str) -> str:
    return f"https://openweathermap.org/img/wn/{icon_code}@2x.png"

# ======================================================
# FEATURE 2 — LANDMARK DETECTION (Google Vision API)
# ======================================================

def detect_landmark_vision(image_bytes: bytes):
    if GOOGLE_VISION_API_KEY == "YOUR_GOOGLE_VISION_KEY":
        return None

    try:
        b64 = base64.b64encode(image_bytes).decode("utf-8")
        payload = {
            "requests": [{
                "image": {"content": b64},
                "features": [
                    {"type": "LANDMARK_DETECTION", "maxResults": 3},
                    {"type": "LABEL_DETECTION",    "maxResults": 5},
                    {"type": "OBJECT_LOCALIZATION","maxResults": 5},
                ]
            }]
        }
        url = f"https://vision.googleapis.com/v1/images:annotate?key={GOOGLE_VISION_API_KEY}"
        r = requests.post(url, json=payload, timeout=15)
        if r.status_code == 200:
            resp = r.json()["responses"][0]
            landmarks = resp.get("landmarkAnnotations", [])
            labels    = resp.get("labelAnnotations", [])
            if landmarks:
                lm = landmarks[0]
                loc = lm.get("locations", [{}])[0].get("latLng", {})
                return {
                    "name":        lm["description"],
                    "score":       round(lm["score"] * 100, 1),
                    "lat":         loc.get("latitude"),
                    "lng":         loc.get("longitude"),
                    "labels":      [l["description"] for l in labels[:4]],
                    "source":      "Google Vision API",
                }
            elif labels:
                return {
                    "name":    labels[0]["description"],
                    "score":   round(labels[0]["score"] * 100, 1),
                    "lat":     None, "lng": None,
                    "labels":  [l["description"] for l in labels[:4]],
                    "source":  "Google Vision (label)",
                }
    except Exception as e:
        st.error(f"Vision API error: {e}")
    return None

LANDMARK_DB = {
    "Table Mountain": {
        "description": "An iconic flat-topped mountain forming a prominent landmark overlooking Cape Town. Part of the Table Mountain National Park and a UNESCO World Heritage Site.",
        "city": "Cape Town, Western Cape",
        "lat": -33.9628, "lng": 18.4098,
        "activities": ["Cable Car Ride", "Hiking Trails", "Abseiling", "Rock Climbing", "Paragliding"],
        "nearby": ["V&A Waterfront", "Cape Point", "Boulders Beach", "Kirstenbosch Gardens"],
        "hotels": ["Cape Sun Resort", "Winelands Luxury Hotel"],
        "best_time": "October – March",
    },
    "Kruger National Park": {
        "description": "One of Africa's largest game reserves covering nearly 2 million hectares. Home to the Big Five and over 500 bird species.",
        "city": "Mpumalanga / Limpopo",
        "lat": -23.9884, "lng": 31.5547,
        "activities": ["Safari Game Drives", "Bush Walks", "Night Drives", "Bird Watching", "Photography"],
        "nearby": ["Blyde River Canyon", "Panorama Route", "God's Window"],
        "hotels": ["Kruger Safari Lodge"],
        "best_time": "May – September (dry season)",
    },
    "V&A Waterfront": {
        "description": "Cape Town's premier waterfront destination, a working harbour blending history, culture, shopping and entertainment.",
        "city": "Cape Town, Western Cape",
        "lat": -33.9036, "lng": 18.4218,
        "activities": ["Shopping", "Dining", "Whale Watching", "Boat Trips", "Two Oceans Aquarium"],
        "nearby": ["Robben Island", "Table Mountain", "Cape Town Stadium"],
        "hotels": ["Cape Sun Resort"],
        "best_time": "Year-round",
    },
    "Drakensberg": {
        "description": "The 'Dragon Mountains' — a UNESCO World Heritage site offering dramatic scenery, ancient San rock art and world-class hiking.",
        "city": "KwaZulu-Natal / Lesotho border",
        "lat": -29.2500, "lng": 29.4167,
        "activities": ["Hiking", "Rock Art Viewing", "Horse Riding", "Fly Fishing", "4x4 Trails"],
        "nearby": ["Giants Castle", "Royal Natal National Park", "Sani Pass"],
        "hotels": ["Mountain Retreat Lodge"],
        "best_time": "April – September",
    },
    "Robben Island": {
        "description": "Former maximum-security prison where Nelson Mandela was held for 18 years. A UNESCO World Heritage Site and powerful symbol of freedom.",
        "city": "Cape Town, Western Cape",
        "lat": -33.8063, "lng": 18.3661,
        "activities": ["Guided Prison Tours", "Museum Visit", "Penguin Colony", "Historical Walk"],
        "nearby": ["V&A Waterfront", "Table Mountain", "Bo-Kaap"],
        "hotels": ["Cape Sun Resort"],
        "best_time": "October – April",
    },
}

def identify_landmark_mock(image: Image.Image) -> dict:
    img_array = np.array(image.convert("RGB"))
    avg_green = img_array[:, :, 1].mean()
    avg_blue  = img_array[:, :, 2].mean()

    if avg_green > 120 and avg_blue < 100:
        name = "Kruger National Park"
    elif avg_blue > 130:
        name = "V&A Waterfront"
    else:
        name = "Table Mountain"

    info = LANDMARK_DB[name]
    return {
        "name":   name,
        "score":  round(np.random.uniform(78, 94), 1),
        "lat":    info["lat"],
        "lng":    info["lng"],
        "labels": ["landmark", "tourism", "South Africa"],
        "source": "AI Image Analysis (Demo Mode — add Google Vision API key for real detection)",
        **info,
    }

def get_landmark_info(name: str) -> dict:
    return LANDMARK_DB.get(name, {})

# ======================================================
# FEATURE 3 — AI CHATBOT (Claude / OpenAI)
# ======================================================

SYSTEM_PROMPT_TOURISM = """You are an expert South African tourism consultant named 'Zara'. 
You have deep knowledge of all SA provinces, destinations, hotels, activities, and travel tips.
Always respond in a friendly, enthusiastic tone. 
Keep responses concise (3-5 sentences max) unless asked for detail.
Focus on: beaches (Durban, Garden Route), safari (Kruger, Addo), adventure (Cape Town, Drakensberg), 
luxury (Franschhoek, Camps Bay), family (Sun City, Knysna), cultural (Soweto, Bo-Kaap, Robben Island).
When recommending hotels, mention the ones in the system: Cape Sun Resort, Sandton Palace, Durban Escape, 
Kruger Safari Lodge, Winelands Luxury Hotel.
Always end with a practical tip or call to action."""

def get_ai_response(messages: list, user_message: str) -> str:
    chat_history = [{"role": m["role"], "content": m["content"]} for m in messages[-10:]]
    chat_history.append({"role": "user", "content": user_message})

    if ANTHROPIC_API_KEY != "YOUR_ANTHROPIC_KEY":
        try:
            headers = {
                "x-api-key": ANTHROPIC_API_KEY,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            }
            payload = {
                "model": "claude-3-5-haiku-20241022",
                "max_tokens": 400,
                "system": SYSTEM_PROMPT_TOURISM,
                "messages": chat_history,
            }
            r = requests.post("https://api.anthropic.com/v1/messages", headers=headers, json=payload, timeout=20)
            if r.status_code == 200:
                return r.json()["content"][0]["text"]
        except Exception:
            pass

    if OPENAI_API_KEY != "YOUR_OPENAI_KEY":
        try:
            headers = {"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"}
            payload = {
                "model": "gpt-4o-mini",
                "messages": [{"role": "system", "content": SYSTEM_PROMPT_TOURISM}] + chat_history,
                "max_tokens": 400,
            }
            r = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload, timeout=20)
            if r.status_code == 200:
                return r.json()["choices"][0]["message"]["content"]
        except Exception:
            pass

    return smart_fallback_response(user_message)

def smart_fallback_response(msg: str) -> str:
    msg_lower = msg.lower()
    responses = {
        ("beach", "coast", "sea", "ocean", "swim"): (
            "🏖️ For South Africa's best beaches, **Durban's Golden Mile** offers warm Indian Ocean swimming year-round, "
            "while the **Garden Route** (Plettenberg Bay, Knysna) is stunning in summer. "
            "Cape Town's **Camps Bay** is glamorous but cold! "
            "I recommend the Durban Escape Hotel for a beach getaway — right on the beachfront. 🌊"
        ),
        ("safari", "game", "wildlife", "big five", "kruger", "lion", "elephant"): (
            "🦁 **Kruger National Park** is South Africa's crown jewel for safari! "
            "The best months are May–September (dry season) when animals congregate around waterholes. "
            "Our **Kruger Safari Lodge** offers expert game drives and luxury bush accommodation. "
            "You're almost guaranteed Big Five sightings — lion, leopard, rhino, elephant, and buffalo! 🐘"
        ),
        ("cape town", "table mountain", "cape", "western cape"): (
            "🏔️ **Cape Town** is one of the world's most beautiful cities! "
            "Don't miss the Table Mountain cable car, V&A Waterfront, Cape Point, and Boulders Beach penguins. "
            "The **Cape Sun Resort** puts you right in the heart of it all. "
            "Best visited October–March for warm, sunny weather. ☀️"
        ),
        ("johannesburg", "joburg", "jozi", "sandton", "gauteng"): (
            "🏙️ **Johannesburg** is SA's economic powerhouse with a vibrant culture scene! "
            "Visit Soweto, the Apartheid Museum, and the Cradle of Humankind. "
            "**Sandton Palace Hotel** is perfect for business or luxury stays. "
            "Joburg has world-class restaurants, galleries, and nightlife. 🍷"
        ),
        ("luxury", "honeymoon", "romantic", "spa", "wine"): (
            "🥂 For luxury and romance, **Stellenbosch & Franschhoek** in the Cape Winelands are unbeatable! "
            "The **Winelands Luxury Hotel** offers wine estate tours, gourmet dining, and a world-class spa. "
            "Best for couples, honeymoons, and celebrating special occasions. "
            "The region has over 200 wine estates to explore! 🍇"
        ),
        ("family", "kids", "children", "theme park", "sun city"): (
            "👨‍👩‍👧 For family holidays, **Sun City** (North West) is a fantastic entertainment resort with waterparks and safari. "
            "**Knysna** and the **Garden Route** are also brilliant for families — whale watching, forest hikes, and beaches. "
            "Durban Escape Hotel is family-friendly with easy beach access. "
            "Book early for school holiday periods (Dec, Jul)! 🎡"
        ),
        ("adventure", "hike", "climb", "extreme", "bungee"): (
            "🧗 SA is an adventure paradise! "
            "**Cape Town** offers abseiling off Table Mountain and shark cage diving. "
            "**Bloukrans Bridge** near Plettenberg Bay has the world's highest commercial bungee jump (216m). "
            "The **Drakensberg** is world-class for hiking and rock art. "
            "Wild Coast and Tsitsikamma are great for sea kayaking and canopy tours! 🏄"
        ),
        ("culture", "history", "museum", "heritage", "township"): (
            "🎭 SA's cultural highlights are profound and moving. "
            "Visit **Robben Island** where Mandela was imprisoned, the **Apartheid Museum** in Joburg, "
            "and vibrant **Bo-Kaap** in Cape Town with its colourful Cape Malay heritage. "
            "Soweto township tours offer incredible insight into SA's history and spirit. "
            "The **cradle of humankind** near Joburg is a UNESCO World Heritage site! 🌍"
        ),
        ("budget", "cheap", "affordable", "backpack"): (
            "💰 SA is excellent value! "
            "The **Garden Route** and **Wild Coast** are budget-friendly with great camping and backpacker lodges. "
            "Hostel dorms in Cape Town and Durban from R200–R400/night. "
            "Renting a car and self-driving the Garden Route is one of SA's best budget adventures. "
            "Visit April–June or August–September for lower prices outside peak season! 🎒"
        ),
    }
    for keywords, response in responses.items():
        if any(k in msg_lower for k in keywords):
            return response

    return (
        "🌍 South Africa is an incredible destination with something for everyone! "
        "Are you interested in **beaches**, **safari**, **adventure sports**, **wine regions**, or **cultural experiences**? "
        "I can tailor specific recommendations for Cape Town, Johannesburg, Durban, Kruger Park, or the Garden Route. "
        "What type of holiday experience are you dreaming of? ✈️"
    )

# ======================================================
# FEATURE 4 — HOTEL LOCATION MAPPING (Google Maps / Folium)
# ======================================================

HOTEL_COORDINATES = {
    "Cape Sun Resort":        {"lat": -33.9249, "lng": 18.4241, "city": "Cape Town",     "address": "Strand St, Cape Town, 8001"},
    "Sandton Palace":         {"lat": -26.1076, "lng": 28.0567, "city": "Johannesburg",  "address": "Sandton City, Johannesburg, 2196"},
    "Durban Escape":          {"lat": -29.8587, "lng": 31.0218, "city": "Durban",        "address": "Marine Parade, Durban, 4001"},
    "Kruger Safari Lodge":    {"lat": -24.0103, "lng": 31.4840, "city": "Kruger Park",   "address": "Skukuza, Kruger National Park"},
    "Winelands Luxury Hotel": {"lat": -33.9321, "lng": 18.8602, "city": "Stellenbosch",  "address": "Dorp Street, Stellenbosch, 7600"},
}

def build_hotel_map(selected_city: str = "All", selected_hotel: str = "All") -> folium.Map:
    m = folium.Map(
        location=[-30.5595, 22.9375],
        zoom_start=5,
        tiles="CartoDB positron",
        min_zoom=4,
        max_zoom=15,
    )
    folium.Rectangle(
        bounds=[[-35.0, 16.3], [-22.1, 33.0]],
        color="#ff6e40",
        fill=True,
        fill_opacity=0.02,
        weight=1.5,
        tooltip="South Africa"
    ).add_to(m)

    hotels = get_hotels()
    for _, h in hotels.iterrows():
        coords = HOTEL_COORDINATES.get(h["name"])
        if not coords:
            continue
        if selected_city != "All" and coords["city"] != selected_city:
            continue
        if selected_hotel != "All" and h["name"] != selected_hotel:
            continue

        icon_color = "orange" if h["type"] == "Luxury" else (
                     "blue"   if h["type"] == "Business" else (
                     "green"  if h["type"] == "Safari" else (
                     "red"    if h["type"] == "Beach" else "gray")))

        popup_html = f"""
        <div style="font-family:sans-serif;min-width:200px;">
          <b style="font-size:14px;color:#ff6e40;">{h['name']}</b><br>
          <span style="color:#666;">📍 {coords['address']}</span><br><br>
          <b>Type:</b> {h['type']}<br>
          <b>Rating:</b> ⭐ {h['rating']}/5.0<br>
          <b>Price:</b> R{h['price']:,}/night<br>
          <b>Occupancy:</b> {h['occupancy']}%<br>
          <b>Amenities:</b> {h['amenities']}<br>
        </div>
        """
        folium.Marker(
            location=[coords["lat"], coords["lng"]],
            popup=folium.Popup(popup_html, max_width=260),
            tooltip=f"🏨 {h['name']} — R{h['price']:,}",
            icon=folium.Icon(color=icon_color, icon="home", prefix="fa"),
        ).add_to(m)

    return m

# ======================================================
# FEATURE 5 — REAL-TIME HOTEL IMAGES (Google Places)
# ======================================================

HOTEL_IMAGE_URLS = {
    "Cape Sun Resort": [
        "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800",
        "https://images.unsplash.com/photo-1582719508461-905c673771fd?w=800",
        "https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?w=800",
    ],
    "Sandton Palace": [
        "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=800",
        "https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=800",
        "https://images.unsplash.com/photo-1618773928121-c32242e63f39?w=800",
    ],
    "Durban Escape": [
        "https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=800",
        "https://images.unsplash.com/photo-1501594907352-04cda38ebc29?w=800",
        "https://images.unsplash.com/photo-1615880484746-a134be9a6ecf?w=800",
    ],
    "Kruger Safari Lodge": [
        "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=800",
        "https://images.unsplash.com/photo-1516426122078-c23e76319801?w=800",
        "https://images.unsplash.com/photo-1523805009345-7448845a9e53?w=800",
    ],
    "Winelands Luxury Hotel": [
        "https://images.unsplash.com/photo-1455587734955-081b22074882?w=800",
        "https://images.unsplash.com/photo-1544148103-0773bf10d330?w=800",
        "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=800",
    ],
}

def get_hotel_images_places(hotel_name: str, city: str) -> list:
    if GOOGLE_PLACES_API_KEY != "YOUR_GOOGLE_PLACES_KEY":
        try:
            search_url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
            params = {
                "input":     f"{hotel_name} {city} South Africa",
                "inputtype": "textquery",
                "fields":    "place_id,name,photos",
                "key":       GOOGLE_PLACES_API_KEY,
            }
            r = requests.get(search_url, params=params, timeout=10)
            if r.status_code == 200:
                candidates = r.json().get("candidates", [])
                if candidates:
                    photos = candidates[0].get("photos", [])
                    urls = []
                    for photo in photos[:4]:
                        ref = photo["photo_reference"]
                        img_url = (
                            f"https://maps.googleapis.com/maps/api/place/photo"
                            f"?maxwidth=800&photo_reference={ref}&key={GOOGLE_PLACES_API_KEY}"
                        )
                        urls.append(img_url)
                    if urls:
                        return urls
        except Exception:
            pass
    return HOTEL_IMAGE_URLS.get(hotel_name, [
        "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800"
    ])

# ======================================================
# ML MODELS
# ======================================================

def predict_cancellation(lead_time, prev_cancels):
    X_train = [[5,0],[30,1],[60,2],[2,0],[45,1],[10,0],[55,2],[25,1]]
    y_train = [0,1,1,0,1,0,1,0]
    clf = RandomForestClassifier(random_state=42)
    clf.fit(X_train, y_train)
    return "High Risk" if clf.predict([[lead_time, prev_cancels]])[0] == 1 else "Low Risk"

def predict_revenue(bookings_count):
    X = np.array([[10],[20],[30],[40],[50],[60]])
    y = np.array([15000,32000,48000,61000,79000,92000])
    model = RandomForestRegressor(random_state=42)
    model.fit(X, y)
    return model.predict([[bookings_count]])[0]

def dynamic_hotel_price(base_price, demand, occupancy, season, holiday, weather):
    m = 1.0
    if demand == "High":  m += 0.20
    elif demand == "Low": m -= 0.10
    if occupancy > 80:  m += 0.25
    elif occupancy < 40: m -= 0.15
    if season == "Peak": m += 0.30
    if holiday: m += 0.20
    if weather in ["Sunny ☀️","Humid 🌤️"]: m += 0.10
    return round(base_price * m, 2)

def analyze_sentiment(review):
    analysis = TextBlob(review)
    p = analysis.sentiment.polarity
    if p > 0: return "Positive", p
    elif p < 0: return "Negative", p
    return "Neutral", p

def get_hotels():
    return pd.DataFrame([
        {"name":"Cape Sun Resort","price":2500,"city":"Cape Town","rating":4.7,"type":"Luxury","occupancy":85,"sentiment_score":92,"amenities":"WiFi, Pool, Spa"},
        {"name":"Sandton Palace","price":3500,"city":"Johannesburg","rating":4.8,"type":"Business","occupancy":78,"sentiment_score":88,"amenities":"WiFi, Gym, Conference Rooms"},
        {"name":"Durban Escape","price":2100,"city":"Durban","rating":4.4,"type":"Beach","occupancy":70,"sentiment_score":84,"amenities":"Beach Access, Pool, Bar"},
        {"name":"Kruger Safari Lodge","price":7000,"city":"Kruger Park","rating":5.0,"type":"Safari","occupancy":95,"sentiment_score":97,"amenities":"Safari Tours, WiFi, Restaurant"},
        {"name":"Winelands Luxury Hotel","price":5200,"city":"Stellenbosch","rating":4.9,"type":"Luxury","occupancy":82,"sentiment_score":93,"amenities":"Wine Tours, Spa, Pool"},
    ])

def rank_hotels(hotels_df, bookings_df):
    scores = []
    for _, h in hotels_df.iterrows():
        hotel_bookings = bookings_df[bookings_df['hotel'] == h['name']] if not bookings_df.empty else pd.DataFrame()
        revenue = hotel_bookings['cost'].sum() if not hotel_bookings.empty else 0
        cancellations = len(hotel_bookings[hotel_bookings['status'] == 'Cancelled']) if not hotel_bookings.empty else 0
        total = len(hotel_bookings) if not hotel_bookings.empty else 1
        cancel_rate = cancellations / max(total, 1)
        score = (h['rating']*20 + h['occupancy']*0.4 + h['sentiment_score']*0.3 + min(revenue/1000,20) - cancel_rate*15)
        scores.append({
            "Hotel": h['name'], "City": h['city'], "Rating": h['rating'], "Occupancy": h['occupancy'],
            "Sentiment": h['sentiment_score'], "Revenue": revenue, "Cancel Rate": round(cancel_rate*100,1), "Score": round(score,1)
        })
    ranked = pd.DataFrame(scores).sort_values("Score", ascending=False).reset_index(drop=True)
    tiers = []
    for i, row in ranked.iterrows():
        if i == 0 or row['Score'] >= ranked['Score'].quantile(0.75): tiers.append("🏆 Top Performer")
        elif row['Score'] >= ranked['Score'].quantile(0.4):           tiers.append("⚠️ Average")
        else:                                                          tiers.append("❌ Underperforming")
    ranked['Tier'] = tiers
    return ranked

# ======================================================
# ACCESS CONTROL HELPERS
# ======================================================

def require_role(allowed_roles: list):
    role = st.session_state.get("role", "")
    if role not in allowed_roles:
        st.markdown("""
        <div class='access-denied'>
            <h2>🔒 Access Denied</h2>
            <p style='color:#94a3b8;'>You don't have permission to view this section.<br>
            Please contact your administrator if you believe this is an error.</p>
        </div>""", unsafe_allow_html=True)
        return False
    return True

def role_badge(role: str) -> str:
    badges = {
        "Tourist":       "<span class='role-badge-tourist'>🌍 Tourist</span>",
        "Hotel Manager": "<span class='role-badge-manager'>🏨 Hotel Manager</span>",
        "Admin":         "<span class='role-badge-admin'>🛡️ Admin</span>",
    }
    return badges.get(role, role)

# ======================================================
# PDF UTILITIES
# ======================================================

def safe(text):
    replacements = {
        "\u2014":"-","\u2013":"-","\u2018":"'","\u2019":"'","\u201C":'"',"\u201D":'"',
        "\u2022":"-","\u2026":"...","\u00B0":" deg",
        "🏆":"[TOP]","⚠️":"[AVG]","❌":"[LOW]","🌍":"","✅":"OK","📊":"",
        "💰":"","📅":"","🤖":"","😊":"","📄":"","🛡️":"","🔴":"[!]","🟡":"[~]","🟢":"[OK]",
    }
    for u, a in replacements.items():
        text = text.replace(u, a)
    return text.encode("latin-1", errors="replace").decode("latin-1")

# ======================================================
# MAIN APP
# ======================================================

def main():
    apply_styles()
    init_db()
    hotels = get_hotels()

    st.sidebar.title("🌍 Tourism-travel-hospitality ZA")
    if st.session_state.get("role"):
        st.sidebar.markdown(f"**Logged in as:** {st.session_state.get('user','')}")
        st.sidebar.markdown(role_badge(st.session_state.get("role", "")), unsafe_allow_html=True)
        st.sidebar.divider()
    amount = st.sidebar.number_input("Amount in ZAR", value=1000, min_value=0)
    currency = st.sidebar.selectbox("Convert To", ["USD","EUR","GBP","AUD","CNY"])
    rates = {"USD":0.053,"EUR":0.049,"GBP":0.042,"AUD":0.082,"CNY":0.38}
    st.sidebar.success(f"≈ {amount*rates[currency]:.2f} {currency}")

    for key, default in [("role", None), ("user", ""), ("user_id", None), ("full_name", ""), ("chat_history", [])]:
        if key not in st.session_state:
            st.session_state[key] = default

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # LOGIN PAGE
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    if st.session_state.role is None:
        st.markdown("""
        <div class='hero'>
            <h1 style='font-size:2.4rem;'>🌍 Welcome to Smart Tourism-travel ZA</h1>
            <p style='color:#94a3b8;font-size:1.15rem;'>Enterprise Smart Tourism & Hospitality Platform for South Africa</p>
            <p style='color:#64748b;font-size:0.9rem;margin-top:8px;'>Real-Time Data · Role-Based Access</p>
        </div>""", unsafe_allow_html=True)

        col1, col2 = st.columns([1, 1])
        with col1:
            st.subheader("🔐 Secure Login")
            username = st.text_input("Username", placeholder="e.g. tourist1")
            password = st.text_input("Password", type="password", placeholder="Your password")

            if st.button("Login", use_container_width=True):
                user = authenticate_user(username, password)
                if user:
                    st.session_state.role      = user[2]
                    st.session_state.user      = user[1]
                    st.session_state.user_id   = user[0]
                    st.session_state.full_name = user[3]
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials or account inactive.")

            st.divider()
            with st.expander("📋 Demo Credentials"):
                st.markdown("""
                | Role | Username | Password |
                |------|----------|----------|
                | Tourist | `tourist1` | `tourist123` |
                | Hotel Manager | `manager1` | `manager123` |
                | Admin | `admin1` | `admin123` |
                """)

        with col2:
            st.image("https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=700",
                     caption="South Africa — Where Every Journey Begins", use_container_width=True)
            st.markdown("""
            <div class='metric-card'>
                <h4>Platform Features</h4>
                <p style='color:#94a3b8;font-size:0.9rem;'>
                ✅ Live weather for any SA destination<br>
                ✅ AI landmark detection from photos<br>
                ✅ Intelligent SA travel chatbot<br>
                ✅ Interactive hotel map (SA-only)<br>
                ✅ Real-time hotel image galleries<br>
                ✅ Role-based secure access<br>
                ✅ AI dynamic pricing & forecasting
                </p>
            </div>""", unsafe_allow_html=True)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # TOURIST DASHBOARD
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    elif st.session_state.role == "Tourist":
        if not require_role(["Tourist"]):
            return

        name = st.session_state.full_name or st.session_state.user
        st.title(f"✈️ Welcome, {name}!")
        c1, c2, c3 = st.columns(3)
        c1.metric("Available Hotels", 5)
        c2.metric("Destinations", 5)
        c3.metric("Avg Satisfaction", "94%")

        tabs = st.tabs([
            "🏨 Hotels & Booking",
            "🌦️ Live Weather",
            "🤖 AI Recommendations",
            "⚖️ Compare Hotels",
            "🗺️ Hotel Map",
            "💬 AI Chatbot",
            "😊 Reviews",
            "📷 Landmark Detection",
        ])

        # ── Tab 0: Hotels & Booking ──
        with tabs[0]:
            st.subheader("🏨 Smart Hotel Booking")
            col1, col2 = st.columns([1, 2])
            with col1:
                check_in  = st.date_input("Check-in")
                check_out = st.date_input("Check-out")
                budget    = st.slider("Budget (ZAR)", 1000, 10000, 3000, step=500)
                sel_city  = st.selectbox("Destination", ["All", "Cape Town", "Johannesburg", "Durban", "Kruger Park", "Stellenbosch"])
                hotel_type = st.selectbox("Hotel Type", ["All", "Luxury", "Business", "Beach", "Safari"])

            filtered = hotels.copy()
            if budget:          filtered = filtered[filtered["price"] <= budget]
            if sel_city != "All":  filtered = filtered[filtered["city"] == sel_city]
            if hotel_type != "All": filtered = filtered[filtered["type"] == hotel_type]

            with col2:
                st.success(f"🔍 Found **{len(filtered)}** hotel(s) matching your criteria")

            for _, row in filtered.iterrows():
                st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
                c1, c2, c3 = st.columns([1, 3, 1])
                with c1:
                    imgs = get_hotel_images_places(row["name"], row["city"])
                    if imgs:
                        st.image(imgs[0], use_container_width=True)
                with c2:
                    st.subheader(row["name"])
                    st.write(f"📍 {row['city']}  |  💰 **R{row['price']:,}/night**  |  ⭐ {row['rating']}  |  🏷️ {row['type']}")
                    st.write(f"🛎️ {row['amenities']}  |  📊 Occupancy: {row['occupancy']}%")
                    if st.button("📷 View Gallery", key=f"gal_{row['name']}"):
                        st.session_state[f"show_gallery_{row['name']}"] = True
                with c3:
                    if st.button("✅ Book Now", key=f"bk_{row['name']}"):
                        save_booking(st.session_state.user, row["name"], row["city"], row["price"])
                        st.success(f"Booked {row['name']}! 🎉")

                if st.session_state.get(f"show_gallery_{row['name']}"):
                    imgs = get_hotel_images_places(row["name"], row["city"])
                    gcols = st.columns(min(len(imgs), 3))
                    for gi, img_url in enumerate(imgs[:3]):
                        gcols[gi].image(img_url, use_container_width=True)
                    if st.button("Close Gallery", key=f"cls_{row['name']}"):
                        del st.session_state[f"show_gallery_{row['name']}"]

                st.markdown("</div>", unsafe_allow_html=True)

        # ── Tab 1: FEATURE 1 — Live Weather ──
        with tabs[1]:
            st.subheader("🌦️ Real-Time Weather — South Africa")
            sa_cities = ["Cape Town", "Johannesburg", "Durban", "Kruger Park", "Stellenbosch",
                         "Pretoria", "Port Elizabeth", "Knysna", "Bloemfontein", "East London"]

            col1, col2 = st.columns([1, 2])
            with col1:
                weather_city    = st.selectbox("Select City", sa_cities, key="weather_city_tourist")
                custom_city     = st.text_input("Or type any SA city", placeholder="e.g. Hermanus")
                search_city     = custom_city.strip() if custom_city.strip() else weather_city
                refresh_weather = st.button("🔄 Refresh Weather")

            with col2:
                w = get_live_weather(search_city)
                if w:
                    st.markdown(f"""
                    <div class='weather-card'>
                        <h2 style='color:#38bdf8;margin-bottom:4px;'>📍 {search_city}</h2>
                        <h1 style='font-size:3.5rem;margin:0;'>{w['temp']}°C</h1>
                        <p style='color:#94a3b8;font-size:1.1rem;margin:4px 0;'>{w['condition']}</p>
                        <p style='color:#64748b;font-size:0.9rem;'>Feels like {w['feels_like']}°C</p>
                    </div>""", unsafe_allow_html=True)
                    wc1, wc2, wc3, wc4 = st.columns(4)
                    wc1.metric("💧 Humidity",    f"{w['humidity']}%")
                    wc2.metric("💨 Wind Speed",  f"{w['wind_speed']} km/h")
                    wc3.metric("🌡️ Pressure",    f"{w['pressure']} hPa")
                    wc4.metric("👁️ Visibility",  f"{w['visibility']} km")

            st.subheader("📅 5-Day Forecast")
            forecast = get_weather_forecast(search_city)
            if forecast:
                fcols = st.columns(len(forecast))
                for fi, day in enumerate(forecast):
                    fcols[fi].markdown(f"""
                    <div class='forecast-card'>
                        <b style='color:#94a3b8;font-size:0.8rem;'>{day['day'][:3].upper()}</b><br>
                        <span style='font-size:1.5rem;'>🌤️</span><br>
                        <b style='font-size:1.2rem;'>{day['temp']}°C</b><br>
                        <span style='color:#64748b;font-size:0.75rem;'>{day['desc']}</span><br>
                        <span style='color:#38bdf8;font-size:0.75rem;'>💧 {day['humidity']}%</span>
                    </div>""", unsafe_allow_html=True)

            st.subheader("🗺️ Weather Snapshot — All SA Destinations")
            all_weather = []
            for c in ["Cape Town", "Johannesburg", "Durban", "Kruger Park", "Stellenbosch"]:
                ww = get_live_weather(c)
                if ww:
                    all_weather.append({"City": c, "Temp (°C)": ww["temp"], "Humidity (%)": ww["humidity"],
                                        "Wind (km/h)": ww["wind_speed"], "Condition": ww["condition"]})
            if all_weather:
                weather_df = pd.DataFrame(all_weather)
                st.dataframe(weather_df, use_container_width=True, hide_index=True)
                st.plotly_chart(px.bar(weather_df, x="City", y="Temp (°C)", color="City",
                    title="Temperature Comparison Across SA Destinations", template="plotly_dark"),
                    use_container_width=True)

        # ── Tab 2: AI Recommendations ──
        with tabs[2]:
            st.subheader("🧠 Hotel Recommendations")
            col1, col2 = st.columns(2)
            with col1:
                ai_budget  = st.slider("Your Budget (ZAR)", 1000, 10000, 3000, step=500, key="ai_budget")
                travel_exp = st.selectbox("Travel Experience", ["Luxury", "Business", "Beach", "Safari"])
                ai_city    = st.selectbox("Preferred Area", ["All"] + ["Cape Town","Johannesburg","Durban","Kruger Park","Stellenbosch"])
            with col2:
                w_dest = get_live_weather(ai_city if ai_city != "All" else "Cape Town")
                if w_dest:
                    st.markdown(f"""
                    <div class='forecast-card'>
                        <b>Current Weather — {ai_city if ai_city != 'All' else 'Cape Town'}</b><br>
                        <span style='font-size:1.5rem;'>🌡️</span> {w_dest['temp']}°C · {w_dest['condition']}<br>
                        <span style='color:#64748b;font-size:0.8rem;'>Humidity: {w_dest['humidity']}% · Wind: {w_dest['wind_speed']} km/h</span>
                    </div>""", unsafe_allow_html=True)

            recs = hotels[hotels["price"] <= ai_budget]
            if travel_exp: recs = recs[recs["type"] == travel_exp]
            if ai_city != "All": recs = recs[recs["city"] == ai_city]
            recs = recs.sort_values(["rating", "price"], ascending=[False, True])

            if recs.empty:
                st.warning("No hotels match your criteria. Try adjusting your budget or preferences.")
            else:
                for _, h in recs.iterrows():
                    with st.expander(f"🏨 {h['name']} — R{h['price']:,}/night  ⭐ {h['rating']}"):
                        ec1, ec2 = st.columns([2, 1])
                        with ec1:
                            imgs = get_hotel_images_places(h["name"], h["city"])
                            st.image(imgs[0], use_container_width=True)
                        with ec2:
                            st.write(f"📍 {h['city']}")
                            st.write(f"🏷️ {h['type']}")
                            st.write(f"⭐ Rating: {h['rating']}/5.0")
                            st.write(f"📊 Occupancy: {h['occupancy']}%")
                            st.write(f"🛎️ {h['amenities']}")
                            wh = get_live_weather(h["city"])
                            if wh:
                                st.info(f"🌡️ {wh['temp']}°C · {wh['condition']}")
                            if st.button("Book", key=f"rec_bk_{h['name']}"):
                                save_booking(st.session_state.user, h["name"], h["city"], h["price"])
                                st.success("Booked! ✅")

        # ── Tab 3: Compare Hotels ──
        with tabs[3]:
            st.subheader("⚖️ Hotel Comparison")
            sel = st.multiselect("Select Hotels to Compare (min 2)", hotels["name"].tolist())
            if len(sel) >= 2:
                cdf = hotels[hotels["name"].isin(sel)].copy()

                img_cols = st.columns(len(sel))
                for ci, h_name in enumerate(sel):
                    imgs = get_hotel_images_places(h_name, cdf[cdf["name"]==h_name]["city"].values[0])
                    if imgs:
                        img_cols[ci].image(imgs[0], caption=h_name, use_container_width=True)

                cdf_display = cdf[["name","city","type","price","rating","occupancy","sentiment_score","amenities"]]
                cdf_display.columns = ["Hotel","City","Type","Price (ZAR)","Rating","Occupancy %","Sentiment %","Amenities"]
                st.dataframe(cdf_display, use_container_width=True, hide_index=True)

                cc1, cc2 = st.columns(2)
                cc1.plotly_chart(px.bar(cdf, x="name", y="rating", color="name", title="Rating Comparison",
                    template="plotly_dark", text="rating"), use_container_width=True)
                cc2.plotly_chart(px.bar(cdf, x="name", y="price", color="name", title="Price Comparison (ZAR)",
                    template="plotly_dark", text="price"), use_container_width=True)

                st.subheader("🌦️ Live Weather at Each Hotel Location")
                wc_cols = st.columns(len(sel))
                for wi, h_name in enumerate(sel):
                    city_name = cdf[cdf["name"]==h_name]["city"].values[0]
                    ww = get_live_weather(city_name)
                    if ww:
                        wc_cols[wi].markdown(f"""
                        <div class='forecast-card'>
                            <b>{h_name}</b><br>
                            <b style='font-size:1.4rem;'>{ww['temp']}°C</b><br>
                            <span style='color:#94a3b8;'>{ww['condition']}</span><br>
                            <span style='font-size:0.8rem;color:#64748b;'>💧 {ww['humidity']}% · 💨 {ww['wind_speed']} km/h</span>
                        </div>""", unsafe_allow_html=True)
            else:
                st.info("Please select at least 2 hotels to compare.")

        # ── Tab 4: FEATURE 4 — Hotel Map ──
        with tabs[4]:
            st.subheader("🗺️ Interactive Hotel Map — South Africa")
            mc1, mc2 = st.columns([1, 3])
            with mc1:
                map_city   = st.selectbox("Filter by City",   ["All","Cape Town","Johannesburg","Durban","Kruger Park","Stellenbosch"])
                map_hotel  = st.selectbox("Filter by Hotel",  ["All"] + hotels["name"].tolist())
                map_type = st.selectbox(
                    "Hotel Type",
                    ["All","Luxury","Business","Beach","Safari"],
                    key="hotel_type_map"
                )                
                st.markdown("""
                <div class='metric-card'>
                    <b>Map Legend</b><br>
                    🟠 Luxury hotels<br>
                    🔵 Business hotels<br>
                    🟢 Safari lodges<br>
                    🔴 Beach resorts<br>
                    ⚫ Other
                </div>""", unsafe_allow_html=True)
            with mc2:
                hotel_map = build_hotel_map(map_city, map_hotel)
                st_folium(hotel_map, width=700, height=500)

            st.subheader("📌 Hotel Quick Info")
            hcols = st.columns(len(hotels))
            for hi, (_, h) in enumerate(hotels.iterrows()):
                coords = HOTEL_COORDINATES.get(h["name"], {})
                hcols[hi].markdown(f"""
                <div class='forecast-card'>
                    <b style='font-size:0.85rem;'>{h['name']}</b><br>
                    <span style='color:#ff6e40;font-size:0.8rem;'>R{h['price']:,}</span><br>
                    <span style='color:#94a3b8;font-size:0.75rem;'>⭐ {h['rating']} · {h['type']}</span><br>
                    <span style='color:#64748b;font-size:0.7rem;'>📍 {coords.get('address','')[:30]}</span>
                </div>""", unsafe_allow_html=True)

        # ── Tab 5: FEATURE 3 — AI Chatbot ──
        with tabs[5]:
            st.subheader("💬 Zara — Your SA Tourism AI Assistant")
            st.markdown("""
            <div class='metric-card'>
                <b>🤖 Ask Zara anything about South African travel!</b><br>
                <span style='color:#94a3b8;font-size:0.9rem;'>
                Try: "Best beach destinations" · "Safari tips for Kruger" · "Luxury wine estate recommendations" · 
                "Family-friendly spots" · "Adventure activities in Cape Town" · "Budget travel tips"
                </span>
            </div>""", unsafe_allow_html=True)

            cats = ["🏖️ Beaches", "🦁 Safari", "🏔️ Adventure", "🥂 Luxury", "👨‍👩‍👧 Family", "🎭 Culture", "💰 Budget Tips"]
            cat_cols = st.columns(len(cats))
            for ci, cat in enumerate(cats):
                if cat_cols[ci].button(cat, key=f"cat_{ci}"):
                    prompt = cat.split(" ", 1)[1]
                    st.session_state.chat_history.append({"role": "user", "content": f"Tell me about {prompt} in South Africa"})
                    with st.spinner("Zara is thinking..."):
                        response = get_ai_response(st.session_state.chat_history[:-1], f"Tell me about {prompt} in South Africa")
                    st.session_state.chat_history.append({"role": "assistant", "content": response})
                    st.rerun()

            chat_container = st.container()
            with chat_container:
                for msg in st.session_state.chat_history:
                    if msg["role"] == "user":
                        st.markdown(f"<div class='chat-bubble-user'>👤 {msg['content']}</div>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<div class='chat-bubble-bot'>🤖 <b>Zara:</b> {msg['content']}</div>", unsafe_allow_html=True)

            user_msg = st.chat_input("Ask Zara about SA travel destinations, hotels, tips...")
            if user_msg:
                st.session_state.chat_history.append({"role": "user", "content": user_msg})
                with st.spinner("Zara is researching..."):
                    response = get_ai_response(st.session_state.chat_history[:-1], user_msg)
                st.session_state.chat_history.append({"role": "assistant", "content": response})
                st.rerun()

            if st.button("🗑️ Clear Chat"):
                st.session_state.chat_history = []
                st.rerun()

        # ── Tab 6: Reviews ──
        with tabs[6]:
            st.subheader("😊 Write & Analyse Your Review")
            review_hotel  = st.selectbox("Hotel", hotels["name"].tolist())
            review_rating = st.slider("Your Rating", 1, 5, 4)
            review_text   = st.text_area("Share your experience...", height=150)
            if st.button("Analyse Review"):
                if review_text.strip():
                    sentiment, polarity = analyze_sentiment(review_text)
                    sc1, sc2 = st.columns(2)
                    color = "#34d399" if sentiment == "Positive" else ("#f87171" if sentiment == "Negative" else "#f59e0b")
                    sc1.markdown(f"""
                    <div class='metric-card' style='text-align:center;border-color:{color};'>
                        <h2 style='color:{color};'>{sentiment}</h2>
                        <p>Polarity Score: {polarity:.3f}</p>
                        <p>Your Rating: {'⭐' * review_rating}</p>
                    </div>""", unsafe_allow_html=True)
                    with sc2:
                        wc = WordCloud(width=600, height=300, background_color="white").generate(review_text)
                        fig, ax = plt.subplots(figsize=(6, 3))
                        ax.imshow(wc)
                        ax.axis("off")
                        st.pyplot(fig)
                        plt.close(fig)
                else:
                    st.warning("Please write a review first.")

        # ── Tab 7: FEATURE 2 — Landmark Detection ──
        with tabs[7]:
            st.subheader("📷 AI Landmark Detection")
            st.markdown("""
            <div class='landmark-card'>
                <p style='color:#a78bfa;margin:0;'>Upload a photo of any South African landmark, attraction, or scenic spot. 
                Our AI will identify it and suggest nearby hotels and activities.</p>
            </div>""", unsafe_allow_html=True)

            ld_col1, ld_col2 = st.columns([1, 1])
            with ld_col1:
                uf = st.file_uploader("Upload Photo", type=["jpg", "jpeg", "png", "webp"])
                manual_landmark = st.selectbox("Or select a known landmark", ["Auto-detect"] + list(LANDMARK_DB.keys()))

            if uf:
                img = Image.open(uf)
                ld_col1.image(img, caption="Uploaded Image", use_container_width=True)
                uf.seek(0)
                img_bytes_data = uf.read()

                with ld_col2:
                    with st.spinner("🔍 Analysing image with AI..."):
                        result = detect_landmark_vision(img_bytes_data)
                        if not result:
                            result = identify_landmark_mock(img)
                        db_info = get_landmark_info(result.get("name", ""))
                        if db_info:
                            result.update(db_info)

                    if result:
                        st.markdown(f"""
                        <div class='landmark-card'>
                            <h3 style='color:#a78bfa;'>🏛️ {result.get('name','Unknown')}</h3>
                            <p style='color:#94a3b8;font-size:0.85rem;'>Confidence: {result.get('score','N/A')}% · {result.get('source','AI Analysis')}</p>
                            <p>📍 {result.get('city','South Africa')}</p>
                            <p>{result.get('description','A beautiful South African landmark.')}</p>
                        </div>""", unsafe_allow_html=True)

                        if result.get("activities"):
                            st.write("**🎯 Activities & Experiences:**")
                            act_cols = st.columns(min(len(result["activities"]), 3))
                            for ai, act in enumerate(result["activities"]):
                                act_cols[ai % 3].markdown(f"✅ {act}")

                        if result.get("nearby"):
                            st.write("**📍 Nearby Attractions:**")
                            st.write(" · ".join(result["nearby"]))

                        if result.get("hotels"):
                            st.write("**🏨 Recommended Hotels:**")
                            for hname in result["hotels"]:
                                h_data = hotels[hotels["name"]==hname]
                                if not h_data.empty:
                                    h = h_data.iloc[0]
                                    st.write(f"🏨 **{h['name']}** — R{h['price']:,}/night ⭐ {h['rating']}")

                        if result.get("best_time"):
                            st.info(f"📅 Best time to visit: **{result['best_time']}**")

                        if result.get("lat") and result.get("lng"):
                            lm_map = folium.Map(location=[result["lat"], result["lng"]], zoom_start=12)
                            folium.Marker(
                                [result["lat"], result["lng"]],
                                tooltip=result["name"],
                                icon=folium.Icon(color="purple", icon="star", prefix="fa")
                            ).add_to(lm_map)
                            st.write("**📍 Location on Map:**")
                            st_folium(lm_map, width=500, height=300)

            elif manual_landmark != "Auto-detect":
                with ld_col2:
                    info = LANDMARK_DB[manual_landmark]
                    st.markdown(f"""
                    <div class='landmark-card'>
                        <h3 style='color:#a78bfa;'>🏛️ {manual_landmark}</h3>
                        <p>📍 {info['city']}</p>
                        <p>{info['description']}</p>
                    </div>""", unsafe_allow_html=True)
                    if info.get("activities"):
                        st.write("**🎯 Activities:**")
                        for act in info["activities"]: st.write(f"✅ {act}")
                    if info.get("hotels"):
                        st.write("**🏨 Nearby Hotels:**")
                        for h in info["hotels"]: st.write(f"🏨 {h}")

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # HOTEL MANAGER DASHBOARD
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    elif st.session_state.role == "Hotel Manager":
        if not require_role(["Hotel Manager"]):
            return

        st.title("📊 Hotel Business Intelligence Console")
        conn = sqlite3.connect("tourism_ai.db")
        df = pd.read_sql("SELECT * FROM bookings", conn)
        conn.close()

        reviews_data = {
            "hotel":        ["Cape Sun Resort","Sandton Palace","Durban Escape","Kruger Safari Lodge","Winelands Luxury Hotel"],
            "positive":     [85,74,90,95,88],
            "neutral":      [10,15,6,3,8],
            "negative":     [5,11,4,2,4],
            "satisfaction": [4.6,4.2,4.8,4.9,4.7],
            "occupancy":    [85,78,70,95,82],
        }

        if not df.empty:
            k1, k2, k3, k4 = st.columns(4)
            k1.metric("💰 Revenue",       f"R{df['cost'].sum():,.2f}")
            k2.metric("📅 Bookings",      len(df))
            k3.metric("❌ Cancellations", len(df[df['status']=='Cancelled']))
            k4.metric("🔄 Refunds",       len(df[df['status']=='Refunded']))

        mgr_tabs = st.tabs([
            "📈 Dashboard",
            "🌦️ Destination Weather",
            "🔍 Booking Management",
            "🚩 Flagged Bookings",
            "💡 Dynamic Pricing",
            "🗺️ Hotel Map",
            "📄 Report",
        ])

        with mgr_tabs[0]:
            if not df.empty:
                st.plotly_chart(px.histogram(df, x="hotel", y="cost", color="hotel", title="Revenue by Hotel", template="plotly_dark"), use_container_width=True)
                combo = make_subplots(specs=[[{"secondary_y": True}]])
                combo.add_trace(go.Bar(x=reviews_data["hotel"], y=reviews_data["positive"], name="Positive %", marker_color='green'), secondary_y=False)
                combo.add_trace(go.Bar(x=reviews_data["hotel"], y=reviews_data["negative"], name="Negative %", marker_color='red'), secondary_y=False)
                combo.add_trace(go.Scatter(x=reviews_data["hotel"], y=reviews_data["satisfaction"], name="Satisfaction", mode="lines+markers", line=dict(color="cyan", width=3)), secondary_y=True)
                combo.update_layout(title="Sentiment & Satisfaction", template="plotly_dark", height=450, legend=dict(orientation="h"))
                st.plotly_chart(combo, use_container_width=True)
                df["risk"] = df.apply(lambda r: predict_cancellation(r["lead_time"], r["prev_cancels"]), axis=1)
                st.plotly_chart(px.pie(df["risk"].value_counts().reset_index().rename(columns={"risk":"Risk","count":"Count"}),
                    names="Risk", values="Count", color="Risk",
                    color_discrete_map={"High Risk":"#f87171","Low Risk":"#34d399"}, title="Cancellation Risk Split", template="plotly_dark"),
                    use_container_width=True)
            else:
                st.warning("No booking data yet.")

        with mgr_tabs[1]:
            st.subheader("🌦️ Live Weather — All Hotel Destinations")
            for _, h in hotels.iterrows():
                ww = get_live_weather(h["city"])
                if ww:
                    wc1, wc2 = st.columns([1, 3])
                    wc1.subheader(h["name"])
                    wc1.write(f"📍 {h['city']}")
                    wc2.markdown(f"""
                    <div class='weather-card' style='text-align:left;padding:16px;'>
                        <b style='color:#38bdf8;font-size:1.4rem;'>{ww['temp']}°C</b>
                        <span style='color:#94a3b8;'> · {ww['condition']}</span><br>
                        Humidity: {ww['humidity']}% · Wind: {ww['wind_speed']} km/h · Pressure: {ww['pressure']} hPa
                    </div>""", unsafe_allow_html=True)
                    st.divider()

        with mgr_tabs[2]:
            st.subheader("🔍 Booking Management")
            if not df.empty:
                col1, col2, col3 = st.columns(3)
                search_user  = col1.text_input("Search by User")
                search_hotel = col2.selectbox("Filter Hotel", ["All"] + hotels["name"].tolist())
                risk_filter  = col3.selectbox("AI Risk", ["All","High Risk","Low Risk"])
                filtered = df.copy()
                filtered["risk"] = filtered.apply(lambda r: predict_cancellation(r["lead_time"], r["prev_cancels"]), axis=1)
                if search_user:        filtered = filtered[filtered['user'].str.contains(search_user, case=False, na=False)]
                if search_hotel != "All": filtered = filtered[filtered['hotel'] == search_hotel]
                if risk_filter != "All":  filtered = filtered[filtered['risk'] == risk_filter]
                st.write(f"Showing **{len(filtered)}** bookings")
                for _, row in filtered.iterrows():
                    risk_label   = row.get("risk", "N/A")
                    status_color = "🔴" if row['status']=='Cancelled' else ("🟡" if row['status']=='Refunded' else "🟢")
                    risk_color   = "🔴" if risk_label=="High Risk" else "🟢"
                    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
                    cc1, cc2 = st.columns([4, 2])
                    with cc1:
                        st.write(f"**#{row['id']}** | {status_color} {row['status']} | 👤 {row['user']}")
                        st.write(f"🏨 {row['hotel']}  •  📍 {row['city']}  •  💰 R{row['cost']:,.0f}")
                        st.write(f"🗓️ {str(row['booking_date'])[:19]}  •  {risk_color} {risk_label}")
                        if row.get('flagged', 0) == 1:
                            st.markdown(f"<div class='flag-card'>🚩 {row.get('flag_reason','')}</div>", unsafe_allow_html=True)
                    with cc2:
                        if row['status'] == 'Active':
                            if st.button("🚩 Flag", key=f"mgr_flag_{row['id']}"):
                                flag_booking(row['id'], "Flagged by Hotel Manager")
                                st.rerun()
                    st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.warning("No bookings yet.")

        with mgr_tabs[3]:
            st.subheader("🚩 Flagged Bookings")
            if not df.empty and 'flagged' in df.columns:
                flagged_df = df[df['flagged'] == 1]
                if not flagged_df.empty:
                    for _, row in flagged_df.iterrows():
                        st.markdown("<div class='rank-danger'>", unsafe_allow_html=True)
                        c1, c2 = st.columns([4, 2])
                        with c1:
                            st.write(f"**#{row['id']}** | 👤 {row['user']} | 🏨 {row['hotel']} | R{row['cost']:,.0f}")
                            st.write(f"🚩 Reason: {row.get('flag_reason','Unknown')}")
                        with c2:
                            if st.button("✅ Clear", key=f"mgr_clr_{row['id']}"):
                                unflag_booking(row['id']); st.rerun()
                        st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.success("No flagged bookings!")

        with mgr_tabs[4]:
            st.subheader("💡 AI Dynamic Pricing")
            p1i, p2i, p3i = st.columns(3)
            base_price  = p1i.number_input("Base Price (ZAR)", 1000, 10000, 3000, step=100)
            demand_lvl  = p2i.selectbox("Demand Level", ["Low","Medium","High"])
            occ_pct     = p3i.slider("Occupancy %", 0, 100, 75)
            s1i, s2i, s3i = st.columns(3)
            season_t    = s1i.selectbox("Season", ["Off-Peak","Mid","Peak"])
            is_holiday  = s2i.checkbox("Public Holiday?")
            weather_n   = s3i.selectbox("Weather", ["Sunny ☀️","Cloudy ☁️","Rainy 🌧️","Humid 🌤️"])
            ai_price    = dynamic_hotel_price(base_price, demand_lvl, occ_pct, season_t, is_holiday, weather_n)
            delta_pct   = (ai_price - base_price) / base_price * 100
            st.success(f"🤖 Recommended: **R{ai_price:,.2f}** (Base R{base_price:,} → {delta_pct:+.1f}%)")

        with mgr_tabs[5]:
            st.subheader("🗺️ Hotel Locations — Management View")
            mgr_map = build_hotel_map()
            st_folium(mgr_map, width=900, height=500)

        with mgr_tabs[6]:
            st.subheader("📄 Generate Business Report")
            if not df.empty:
                if st.button("📊 Generate PDF Report"):
                    with st.spinner("Building report..."):
                        rfile = generate_detailed_report(df, reviews_data, hotels)
                    if os.path.exists(rfile):
                        st.success("✅ Report ready!")
                        with open(rfile, "rb") as f:
                            st.download_button("⬇️ Download Report", data=f,
                                file_name="AI_Hotel_Report.pdf", mime="application/pdf")
            else:
                st.warning("No booking data yet.")

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # ADMIN DASHBOARD
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    elif st.session_state.role == "Admin":
        if not require_role(["Admin"]):
            return

        st.title("🛡️ Admin Control Center")
        conn = sqlite3.connect("tourism_ai.db")
        df = pd.read_sql("SELECT * FROM bookings", conn)
        conn.close()

        reviews_data = {
            "hotel":        ["Cape Sun Resort","Sandton Palace","Durban Escape","Kruger Safari Lodge","Winelands Luxury Hotel"],
            "positive":     [85,74,90,95,88], "neutral": [10,15,6,3,8], "negative": [5,11,4,2,4],
            "satisfaction": [4.6,4.2,4.8,4.9,4.7], "occupancy": [85,78,70,95,82],
        }

        total_rev     = df['cost'].sum() if not df.empty else 0
        cancelled_rev = df[df['status']=='Cancelled']['cost'].sum() if not df.empty else 0
        refunded_rev  = df[df['status']=='Refunded']['cost'].sum() if not df.empty else 0
        active_rev    = df[df['status']=='Active']['cost'].sum() if not df.empty else 0
        high_risk     = 0
        if not df.empty:
            df["risk"] = df.apply(lambda r: predict_cancellation(r["lead_time"], r["prev_cancels"]), axis=1)
            high_risk  = len(df[df["risk"]=="High Risk"])

        k1,k2,k3,k4,k5,k6 = st.columns(6)
        k1.metric("Total Bookings",  len(df))
        k2.metric("Active Revenue",  f"R{active_rev:,.0f}")
        k3.metric("Revenue Lost",    f"R{cancelled_rev+refunded_rev:,.0f}")
        k4.metric("Cancellations",   len(df[df['status']=='Cancelled']) if not df.empty else 0)
        k5.metric("Refunds",         len(df[df['status']=='Refunded'])  if not df.empty else 0)
        k6.metric("⚠️ High Risk",    high_risk)

        admin_tabs = st.tabs([
            "📊 Analytics",
            "🎛️ Booking Control",
            "🏆 Performance Ranking",
            "💸 Loss & Risk",
            "🌦️ Weather Overview",
            "🗺️ Hotel Map",
            "👤 User Management",
            "📄 Full Report",
        ])

        with admin_tabs[0]:
            if not df.empty:
                col1, col2 = st.columns(2)
                with col1:
                    st.plotly_chart(px.histogram(df, x="hotel", y="cost", color="hotel", title="Revenue by Hotel", template="plotly_dark"), use_container_width=True)
                    st.plotly_chart(px.pie(df, names="city", title="Bookings by City", template="plotly_dark"), use_container_width=True)
                with col2:
                    st.plotly_chart(px.bar(
                        pd.DataFrame({"Hotel":reviews_data["hotel"],"Positive":reviews_data["positive"],"Negative":reviews_data["negative"],"Neutral":reviews_data["neutral"]}),
                        x="Hotel", y=["Positive","Negative","Neutral"], title="Sentiment Distribution", template="plotly_dark", barmode="stack"
                    ), use_container_width=True)
                    occ_df = pd.DataFrame({"Hotel":reviews_data["hotel"],"Occupancy":reviews_data["occupancy"]})
                    fig_occ = px.bar(occ_df, x="Hotel", y="Occupancy", title="Occupancy by Hotel", template="plotly_dark",
                                     color="Occupancy", color_continuous_scale=["red","yellow","green"])
                    fig_occ.add_hline(y=80, line_dash="dash", line_color="orange", annotation_text="80% threshold")
                    st.plotly_chart(fig_occ, use_container_width=True)
                st.dataframe(df.sort_values('booking_date', ascending=False), use_container_width=True, hide_index=True)
            else:
                st.warning("No booking data yet.")

        with admin_tabs[1]:
            st.subheader("🎛️ Booking Control Panel")
            if not df.empty:
                col1, col2 = st.columns(2)
                search    = col1.text_input("🔍 Search")
                status_f  = col2.selectbox("Status", ["All","Active","Cancelled","Refunded"])
                display_df = df.copy()
                if search:
                    display_df = display_df[
                        display_df['user'].str.contains(search, case=False, na=False) |
                        display_df['hotel'].str.contains(search, case=False, na=False) |
                        display_df['id'].astype(str).str.contains(search)]
                if status_f != "All":
                    display_df = display_df[display_df['status'] == status_f]
                st.write(f"Showing **{len(display_df)}** bookings")
                for _, row in display_df.iterrows():
                    status_icon = "🟢" if row['status']=='Active' else ("🔴" if row['status']=='Cancelled' else "🟡")
                    risk_label  = row.get("risk","N/A") if "risk" in df.columns else "N/A"
                    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
                    c1,c2,c3,c4 = st.columns([4,2,2,2])
                    with c1:
                        st.write(f"**#{row['id']}** {status_icon} {row['status']} | 👤 {row['user']}")
                        st.write(f"🏨 {row['hotel']} · 📍 {row['city']} · 💰 R{row['cost']:,.2f}")
                        if row.get('flagged',0): st.markdown(f"<div class='flag-card'>🚩 {row.get('flag_reason','')}</div>", unsafe_allow_html=True)
                    with c2:
                        if row['status']=='Active':
                            if st.button("❌ Cancel", key=f"adm_cancel_{row['id']}"):
                                cancel_booking(row['id']); st.rerun()
                        if row['status'] in ['Active','Cancelled'] and not row.get('refunded',0):
                            if st.button("💸 Refund", key=f"adm_refund_{row['id']}"):
                                refund_booking(row['id']); st.rerun()
                    with c3:
                        if row['status'] == 'Active':
                            new_h = st.selectbox("Reassign", ["—"]+hotels["name"].tolist(), key=f"adm_rs_{row['id']}")
                            if new_h != "—":
                                hr = hotels[hotels["name"]==new_h].iloc[0]
                                if st.button("🔁", key=f"adm_rsbtn_{row['id']}"):
                                    reassign_booking(row['id'], new_h, hr['city'], hr['price']); st.rerun()
                    with c4:
                        with st.expander("✏️ Edit"):
                            nu = st.text_input("User", value=row['user'], key=f"adm_eu_{row['id']}")
                            nc = st.number_input("Cost", value=float(row['cost']), key=f"adm_ec_{row['id']}")
                            if st.button("Save", key=f"adm_sv_{row['id']}"):
                                edit_booking(row['id'], nu, row['hotel'], row['city'], nc); st.rerun()
                        if not row.get('flagged',0):
                            if st.button("🚩 Flag", key=f"adm_flg_{row['id']}"):
                                flag_booking(row['id'], "Flagged by Admin"); st.rerun()
                        else:
                            if st.button("✅ Unflag", key=f"adm_uflg_{row['id']}"):
                                unflag_booking(row['id']); st.rerun()
                    st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.warning("No bookings yet.")

        with admin_tabs[2]:
            st.subheader("🏆 Hotel Performance Ranking")
            ranked = rank_hotels(hotels, df if not df.empty else pd.DataFrame())
            for i, (_, row) in enumerate(ranked.iterrows()):
                tier  = row['Tier']
                css   = "rank-gold" if "Top" in tier else ("rank-silver" if "Average" in tier else "rank-danger")
                st.markdown(f"<div class='{css}'>", unsafe_allow_html=True)
                cc1,cc2,cc3,cc4,cc5 = st.columns([1,3,2,2,2])
                cc1.markdown(f"### #{i+1}")
                cc2.write(f"**{row['Hotel']}** · {row['City']}\n{tier}")
                cc3.metric("Score",     row['Score'])
                cc4.metric("Occupancy", f"{row['Occupancy']}%")
                cc5.metric("Sentiment", f"{row['Sentiment']}%")
                st.markdown("</div>", unsafe_allow_html=True)
            st.plotly_chart(px.bar(ranked, x="Hotel", y="Score", color="Tier",
                color_discrete_map={"🏆 Top Performer":"#fbbf24","⚠️ Average":"#94a3b8","❌ Underperforming":"#f87171"},
                title="Hotel Performance Composite Score", template="plotly_dark", text="Score"), use_container_width=True)

        with admin_tabs[3]:
            st.subheader("💸 Revenue Loss & Risk")
            if not df.empty:
                col1, col2 = st.columns(2)
                with col1:
                    sr = df.groupby("status")["cost"].sum().reset_index()
                    sr.columns = ["Status","Revenue"]
                    fig_loss = px.bar(sr, x="Status", y="Revenue", color="Status",
                        color_discrete_map={"Active":"#34d399","Cancelled":"#f87171","Refunded":"#f59e0b"},
                        title="Revenue by Booking Status", template="plotly_dark", text="Revenue")
                    fig_loss.update_traces(texttemplate="R%{text:,.0f}", textposition="outside")
                    st.plotly_chart(fig_loss, use_container_width=True)
                    total_loss = cancelled_rev + refunded_rev
                    st.markdown(f"""
                    <div class='rank-danger'>
                        <b>💸 Revenue Loss Summary</b><br>
                        Cancellations: R{cancelled_rev:,.2f}<br>
                        Refunds: R{refunded_rev:,.2f}<br>
                        <b>Total: R{total_loss:,.2f} ({total_loss/max(total_rev,1)*100:.1f}%)</b>
                    </div>""", unsafe_allow_html=True)
                with col2:
                    rc = df["risk"].value_counts().reset_index()
                    rc.columns = ["Risk","Count"]
                    st.plotly_chart(px.pie(rc, names="Risk", values="Count", color="Risk",
                        color_discrete_map={"High Risk":"#f87171","Low Risk":"#34d399"},
                        title="Cancellation Risk Split", template="plotly_dark"), use_container_width=True)
            else:
                st.warning("No booking data.")

        with admin_tabs[4]:
            st.subheader("🌦️ Platform-Wide Weather Dashboard")
            all_cities = ["Cape Town","Johannesburg","Durban","Kruger Park","Stellenbosch","Pretoria","Port Elizabeth","Knysna"]
            wdata = []
            for city in all_cities:
                ww = get_live_weather(city)
                if ww:
                    wdata.append({"City": city, **ww})
            if wdata:
                wdf = pd.DataFrame(wdata)
                col1, col2 = st.columns(2)
                col1.plotly_chart(px.bar(wdf, x="City", y="temp", color="City",
                    title="Temperature Across SA", template="plotly_dark", labels={"temp":"°C"}), use_container_width=True)
                col2.plotly_chart(px.bar(wdf, x="City", y="humidity", color="City",
                    title="Humidity %", template="plotly_dark"), use_container_width=True)
                st.dataframe(wdf[["City","temp","feels_like","humidity","wind_speed","condition","pressure","visibility"]],
                    use_container_width=True, hide_index=True)

        with admin_tabs[5]:
            st.subheader("🗺️ Admin Hotel Map View")
            adm_map = build_hotel_map()
            st_folium(adm_map, width=1000, height=550)

        with admin_tabs[6]:
            st.subheader("👤 User Management & Access Control")
            users_df = get_all_users()

            u1,u2,u3,u4 = st.columns(4)
            u1.metric("Total Users",   len(users_df))
            u2.metric("Tourists",      len(users_df[users_df['role']=='Tourist']))
            u3.metric("Managers",      len(users_df[users_df['role']=='Hotel Manager']))
            u4.metric("Admins",        len(users_df[users_df['role']=='Admin']))

            st.write("**All Platform Users**")
            for _, u in users_df.iterrows():
                is_active = bool(u.get('is_active', 1))
                badge_css = "rank-gold" if u['role']=='Admin' else ("rank-silver" if u['role']=='Hotel Manager' else "metric-card")
                st.markdown(f"<div class='{badge_css}'>", unsafe_allow_html=True)
                uc1,uc2,uc3,uc4 = st.columns([3,2,2,1])
                with uc1:
                    st.write(f"**{u['full_name']}** (@{u['username']})")
                    st.write(f"📧 {u.get('email','N/A')} | 🕐 Last login: {str(u.get('last_login','Never'))[:16]}")
                with uc2:
                    st.write(f"**Role:** {u['role']}")
                    st.write(f"**Status:** {'🟢 Active' if is_active else '🔴 Inactive'}")
                with uc3:
                    st.write(f"**Created:** {str(u.get('created_at',''))[:10]}")
                with uc4:
                    if u['username'] != st.session_state.user:
                        new_status = 0 if is_active else 1
                        btn_label = "🔴 Deactivate" if is_active else "🟢 Activate"
                        if st.button(btn_label, key=f"usr_toggle_{u['id']}"):
                            toggle_user_status(u['id'], new_status); st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)

            st.divider()
            st.subheader("➕ Create New User")
            with st.expander("Add User"):
                nu1, nu2 = st.columns(2)
                new_username  = nu1.text_input("Username",   key="nu_username")
                new_password  = nu2.text_input("Password",   type="password", key="nu_password")
                new_full_name = nu1.text_input("Full Name",  key="nu_fullname")
                new_email     = nu2.text_input("Email",      key="nu_email")
                new_role      = st.selectbox("Role", ["Tourist","Hotel Manager","Admin"], key="nu_role")
                if st.button("Create User"):
                    if new_username and new_password:
                        ok, msg = create_user(new_username, new_password, new_role, new_email, new_full_name)
                        if ok: st.success(f"✅ {msg}")
                        else:  st.error(f"❌ {msg}")
                    else:
                        st.warning("Username and password are required.")

            st.divider()
            st.subheader("🔐 Role Permission Matrix")
            perm_data = {
                "Feature":               ["Hotel Booking", "Weather Data", "AI Chatbot", "Landmark Detection", "Hotel Map",
                                          "View Reviews", "Booking Management", "Flag Bookings", "Dynamic Pricing",
                                          "Analytics Dashboard", "User Management", "Generate Reports", "Cancel/Refund Bookings"],
                "Tourist 🌍":            ["✅","✅","✅","✅","✅","✅","❌","❌","❌","❌","❌","❌","❌"],
                "Hotel Manager 🏨":      ["❌","✅","❌","❌","✅","✅","✅","✅","✅","✅","❌","✅","❌"],
                "Admin 🛡️":             ["✅","✅","✅","✅","✅","✅","✅","✅","✅","✅","✅","✅","✅"],
            }
            st.dataframe(pd.DataFrame(perm_data), use_container_width=True, hide_index=True)

        with admin_tabs[7]:
            st.subheader("📄 Full Executive Report")
            if not df.empty:
                if st.button("🚀 Generate Complete PDF Report"):
                    with st.spinner("Building 8-page report..."):
                        rfile = generate_detailed_report(df, reviews_data, hotels)
                    if os.path.exists(rfile):
                        st.success("✅ Complete report ready!")
                        with open(rfile, "rb") as f:
                            st.download_button("⬇️ Download Full Report", data=f,
                                file_name="AI_Smart_Tourism_Report.pdf", mime="application/pdf")
            else:
                st.warning("No booking data yet.")

    if st.session_state.role:
        st.sidebar.divider()
        if st.sidebar.button("🚪 Logout"):
            for k in ["role","user","user_id","full_name","chat_history"]:
                st.session_state[k] = None if k != "chat_history" else []
            st.session_state.role = None
            st.rerun()


# ======================================================
# PDF REPORT GENERATOR
# ======================================================

def generate_detailed_report(df, reviews_data, hotels_df):
    chart_paths = []

    def make_chart(func):
        p = tempfile.mktemp(suffix=".png")
        chart_paths.append(p)
        func(p)
        return p

    def dark_fig(w=9, h=4):
        f, a = plt.subplots(figsize=(w, h))
        f.patch.set_facecolor("#0f172a"); a.set_facecolor("#1e293b")
        a.tick_params(colors="white"); a.spines[:].set_color("#334155")
        return f, a

    def p1_chart(p):
        rb = df.groupby("hotel")["cost"].sum().reset_index() if not df.empty else pd.DataFrame({"hotel":reviews_data["hotel"],"cost":[0]*5})
        f,a = dark_fig()
        bars = a.bar(rb["hotel"], rb["cost"], color=["#ff6e40","#38bdf8","#34d399","#f59e0b","#a78bfa"])
        a.set_title("Revenue by Hotel", color="white", fontsize=13, pad=10); a.set_ylabel("Revenue (ZAR)", color="white")
        for b in bars: a.text(b.get_x()+b.get_width()/2, b.get_height()+200, f"R{b.get_height():,.0f}", ha="center", color="white", fontsize=8)
        plt.xticks(rotation=20, ha="right"); plt.tight_layout(); plt.savefig(p, dpi=120, bbox_inches="tight", facecolor=f.get_facecolor()); plt.close(f)

    def p2_chart(p):
        f,a = dark_fig()
        x = np.arange(len(reviews_data["hotel"])); w=0.5
        a.bar(x, reviews_data["positive"], w, label="Positive", color="#34d399")
        a.bar(x, reviews_data["negative"], w, bottom=reviews_data["positive"], label="Negative", color="#f87171")
        a.set_xticks(x); a.set_xticklabels(reviews_data["hotel"], rotation=20, ha="right", color="white", fontsize=8)
        a.set_title("Guest Sentiment", color="white", fontsize=13); a.legend(facecolor="#1e293b", labelcolor="white")
        plt.tight_layout(); plt.savefig(p, dpi=120, bbox_inches="tight", facecolor=f.get_facecolor()); plt.close(f)

    def p3_chart(p):
        f,a = dark_fig()
        a.plot(reviews_data["hotel"], reviews_data["satisfaction"], marker="o", color="#38bdf8", linewidth=2.5, markersize=8)
        a.set_ylim(1,5.5); a.set_title("Guest Satisfaction", color="white", fontsize=13); a.set_ylabel("Score", color="white")
        plt.xticks(rotation=20, ha="right"); plt.tight_layout(); plt.savefig(p, dpi=120, bbox_inches="tight", facecolor=f.get_facecolor()); plt.close(f)

    def p4_chart(p):
        occ = reviews_data.get("occupancy", [75,82,91,68,88])
        f,a = dark_fig()
        a.fill_between(reviews_data["hotel"], occ, alpha=0.2, color="#a78bfa")
        a.plot(reviews_data["hotel"], occ, marker="s", color="#a78bfa", linewidth=2.5, markersize=8)
        a.axhline(80, color="#f59e0b", linestyle="--", linewidth=1.5, label="80% Threshold")
        a.set_title("Occupancy Forecast", color="white", fontsize=13); a.set_ylabel("Occupancy %", color="white")
        a.legend(facecolor="#1e293b", labelcolor="white"); plt.xticks(rotation=20, ha="right")
        plt.tight_layout(); plt.savefig(p, dpi=120, bbox_inches="tight", facecolor=f.get_facecolor()); plt.close(f)

    p1 = make_chart(p1_chart)
    p2 = make_chart(p2_chart)
    p3 = make_chart(p3_chart)
    p4 = make_chart(p4_chart)

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    def sec(t): pdf.set_font("Arial","B",13); pdf.set_text_color(255,110,64); pdf.cell(0,9,safe(t),ln=True); pdf.set_text_color(40,40,40); pdf.ln(2)
    def body(t): pdf.set_font("Arial","",10); pdf.set_text_color(40,40,40); pdf.multi_cell(0,6,safe(t)); pdf.ln(2)
    def img(p, w=180):
        if os.path.exists(p): pdf.image(p, x=15, w=w)
        pdf.ln(3)

    pdf.add_page()
    pdf.set_fill_color(15,23,42); pdf.rect(0,0,210,297,"F")
    pdf.set_y(60); pdf.set_font("Arial","B",26); pdf.set_text_color(255,110,64)
    pdf.cell(0,14,safe("AI SMART TOURISM ZA"), ln=True, align="C")
    pdf.set_font("Arial","B",14); pdf.set_text_color(255,255,255)
    pdf.cell(0,9,safe("Executive Analytics Report"), ln=True, align="C")
    pdf.set_font("Arial","",10); pdf.set_text_color(148,163,184)
    pdf.cell(0,7,safe(f"Generated: {datetime.now().strftime('%d %B %Y  |  %H:%M')}"), ln=True, align="C")
    total_rev = df['cost'].sum() if not df.empty else 0
    pdf.ln(12); pdf.set_font("Arial","B",11); pdf.set_text_color(56,189,248)
    for line in [f"Total Bookings: {len(df)}", f"Total Revenue: R{total_rev:,.2f}",
                 f"Hotels Monitored: {len(reviews_data['hotel'])}", f"Avg Satisfaction: {np.mean(reviews_data['satisfaction']):.2f}/5.0"]:
        pdf.cell(0,8,safe(line),ln=True,align="C")

    pdf.add_page()
    pdf.set_font("Arial","B",14); pdf.set_text_color(255,110,64)
    pdf.cell(0,10,safe("Analytics Overview"),ln=True,align="C"); pdf.ln(2)
    pdf.set_text_color(30,30,30)
    for cp in [p1,p2,p3,p4]: img(cp)

    pdf.add_page()
    sec("Key Performance Indicators")
    if not df.empty:
        best = df.groupby("hotel")["cost"].sum().idxmax()
        body(f"Top hotel by revenue: {best}. Total revenue: R{total_rev:,.2f}. Bookings: {len(df)}.")
    sec("Strategic Recommendations")
    body("1. Deploy AI Dynamic Pricing during peak seasons (Dec, Jan, Jul) for 15-30% revenue uplift.")
    body("2. Implement non-refundable rate tiers to reduce cancellation losses.")
    body("3. Properties with >10% negative sentiment need immediate service audits.")
    body("4. Target below-80% occupancy hotels with corporate packages and mid-week deals.")
    body("5. Capture email and satisfaction data on all bookings to improve AI model accuracy.")

    report_path = os.path.join(tempfile.gettempdir(), "AI_Hotel_Business_Report.pdf")
    pdf.output(report_path)
    for p in chart_paths:
        try: os.remove(p)
        except: pass
    return report_path


if __name__ == "__main__":
>>>>>>> fac0a472dd65abb6c62d32d6332a1cdbe873dcc4
    main()