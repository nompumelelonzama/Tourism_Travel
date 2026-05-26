
# 🌍 Smart Tourism-Travel ZA

### AI-Powered Tourism & Hospitality Intelligence Platform for South Africa

Smart Tourism Travel ZA is an advanced AI-driven tourism and hospitality platform designed to modernize travel experiences across South Africa. The application combines artificial intelligence, real-time APIs, computer vision, interactive geospatial mapping, and analytics into a unified smart tourism ecosystem for travelers, hotel managers, and administrators.

*Real-time weather · AI chatbot · Landmark detection · Interactive maps · Booking analytics · Executive reporting*


## 🚀 Live Demo

https://tourism-travel-j6vy.onrender.com/


## 🔍 Overview

**Smart Tourism-Travel ZA** is a multi-role tourism management platform built for the South African hospitality industry. It combines real-time external APIs, machine learning, natural language AI, and a rich analytics engine into a single Streamlit application backed by a local SQLite database.

The platform is designed for three distinct user types:

- **Tourists** — browse destinations, check live weather, chat with an AI guide, detect landmarks from photos, and book hotels
- **Hotel Managers** — manage bookings, analyse guest sentiment, set dynamic pricing, and generate business reports
- **Admins** — full system access including user management, booking oversight, fraud flagging, and executive PDF reports

---

## ✨ Features

### 🌤️ Real-Time Weather

Live weather data for major South African cities powered by the OpenWeather API.

- Current conditions: temperature, feels-like, humidity, wind speed, pressure, visibility
- 5-day daily forecast with weather icons
- City coverage: Cape Town, Johannesburg, Durban, Kruger Park, Stellenbosch, Pretoria, Port Elizabeth, Knysna
- Full mock-data fallback — works out of the box without an API key

---

### 🤖 AI Tourism Chatbot — *Zara*

A conversational South African travel consultant powered by Claude (Anthropic) or GPT-4o Mini (OpenAI).

- Covers beaches, safari, adventure, luxury, family, cultural, and budget travel
- Maintains up to 10 messages of conversation history per session
- Falls back gracefully to a local keyword-driven response engine if no LLM API key is set
- Styled chat interface with distinct user and bot message bubbles

---

### 🏔️ Landmark Detection

Upload any travel photo to identify South African landmarks.

- Powered by the **Google Vision API** (Landmark Detection + Label Detection + Object Localisation)
- Returns: landmark name, confidence score, GPS coordinates, description, activities, nearby attractions, recommended hotels, and best visiting season
- Built-in landmark database includes: Table Mountain, Kruger National Park, V&A Waterfront, Drakensberg, and Robben Island
- Demo mode uses image colour analysis as a fallback when no Vision API key is configured

---

### 🗺️ Interactive Hotel Map

An interactive Folium map of all partner hotels plotted across South Africa.

- Filter by city or hotel name
- Clickable markers with address and booking quick-links
- Centred on South Africa with appropriate zoom and bounds

---

### 🏨 Hotel Booking System

End-to-end room browsing and booking for Tourist accounts.

- SQLite-backed booking records
- Booking status lifecycle: Active → Cancelled / Refunded
- Dynamic pricing indicators based on demand signals

---

### 📊 Analytics Dashboard

A multi-chart analytics suite for Hotel Managers and Admins.

- **Revenue by Hotel** — bar chart with per-hotel totals
- **Guest Sentiment** — stacked positive/negative breakdown via TextBlob
- **Satisfaction Scores** — line chart across all properties
- **Occupancy Forecast** — area chart with an 80% threshold reference line
- **Word Cloud** — generated from aggregated guest review text
- **Cancellation Risk** — Random Forest classifier predicting high-risk bookings
- **Dynamic Pricing** — Random Forest regressor recommending optimal room rates

---

### 🚩 Booking Management & Fraud Flagging

Granular booking controls for Hotel Managers and Admins.

- View, edit, reassign, cancel, and refund individual bookings
- Flag suspicious bookings with a free-text reason
- Bulk unflag resolved cases
- Flagged bookings displayed in a dedicated review queue

---

### 👥 User Management

Full user administration for Admin accounts.

- Create new users with any role
- Activate or deactivate accounts
- View last login timestamps and account creation dates
- Role permission matrix rendered as an in-app data table

---

### 📄 Executive PDF Report

One-click generation of a multi-page professional PDF report.

- Cover page with key KPIs (total bookings, total revenue, hotel count, average satisfaction)
- Revenue, sentiment, satisfaction, and occupancy charts embedded as high-resolution images
- Strategic recommendations section with five data-driven action items
- Download directly from the browser

---

## 🛠️ Tech Stack

### Core Framework

| Library | Purpose |
|---|---|
| [Streamlit](https://streamlit.io) | UI framework and state management |
| [SQLite3](https://docs.python.org/3/library/sqlite3.html) | Local relational database |
| [Pandas](https://pandas.pydata.org) | Data manipulation and tabular display |
| [NumPy](https://numpy.org) | Numerical operations and array handling |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Streamlit Frontend                       │
│   Tourist View │ Hotel Manager View │ Admin View                │
└────────────────────────┬────────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────────┐
│                      Application Layer                          │
│  Auth │ Weather │ Chatbot │ Landmark │ Map │ Booking │ Reports  │
└──────┬──────────┬──────────┬──────────┬──────────────┬──────────┘
       │          │          │          │              │
  ┌────▼───┐ ┌───▼────┐ ┌───▼───┐ ┌───▼────┐   ┌────▼─────┐
  │SQLite  │ │OpenWx  │ │Claude │ │Google  │   │scikit-   │
  │tourism │ │API     │ │/ GPT  │ │Vision  │   │learn ML  │
  │_ai.db  │ │        │ │API    │ │API     │   │Models    │
  └────────┘ └────────┘ └───────┘ └────────┘   └──────────┘
```

## 🔑 Role Permissions

| Feature | Tourist 🌍 | Hotel Manager 🏨 | Admin 🛡️ |
|---|:---:|:---:|:---:|
| Hotel Booking | ✅ | ❌ | ✅ |
| Weather Data | ✅ | ✅ | ✅ |
| AI Chatbot (Zara) | ✅ | ❌ | ✅ |
| Landmark Detection | ✅ | ❌ | ✅ |
| Hotel Map | ✅ | ✅ | ✅ |
| View Reviews | ✅ | ✅ | ✅ |
| Booking Management | ❌ | ✅ | ✅ |
| Flag Bookings | ❌ | ✅ | ✅ |
| Dynamic Pricing | ❌ | ✅ | ✅ |
| Analytics Dashboard | ❌ | ✅ | ✅ |
| Cancel / Refund Bookings | ❌ | ❌ | ✅ |
| User Management | ❌ | ❌ | ✅ |
| Generate PDF Reports | ❌ | ✅ | ✅ |

---

## 🏨 Hotels & Destinations

| Hotel | City | Province | Coordinates |
|---|---|---|---|
| Cape Sun Resort | Cape Town | Western Cape | -33.9249, 18.4241 |
| Sandton Palace | Johannesburg | Gauteng | -26.1076, 28.0567 |
| Durban Escape | Durban | KwaZulu-Natal | -29.8587, 31.0218 |
| Kruger Safari Lodge | Skukuza | Mpumalanga | -24.0103, 31.4840 |
| Winelands Luxury Hotel | Stellenbosch | Western Cape | -33.9321, 18.8602 |

### Supported Destinations

The app covers weather, landmark data, and travel advice for the following cities:

`Cape Town` · `Johannesburg` · `Durban` · `Kruger Park` · `Stellenbosch` · `Pretoria` · `Port Elizabeth` · `Knysna` · `Franschhoek` · `Drakensberg` · `Blyde River Canyon` · `Garden Route`

---

## 🔌 API Integrations

### OpenWeather API
Provides current conditions and 5-day forecasts. Endpoint used: `/data/2.5/weather` and `/data/2.5/forecast`. Mock data is provided for all 8 cities when the key is absent.

### Anthropic Claude (`claude-3-5-haiku-20241022`)
Primary LLM for the Zara chatbot. Sends up to 10 messages of conversation history per request. Falls back to OpenAI if unavailable.

### OpenAI (`gpt-4o-mini`)
Secondary LLM. Used when Anthropic API is unavailable or not configured.

### Google Vision API
Performs Landmark Detection, Label Detection, and Object Localisation on uploaded images. Returns name, confidence score, and GPS coordinates for identified landmarks.

### Google Maps & Places API
Used for hotel map tile rendering and destination detail enrichment via Folium.

---

## 🔒 Security Considerations

- All passwords are hashed with **SHA-256** before storage — plaintext passwords are never persisted.
- Never commit `.streamlit/secrets.toml` — add it to `.gitignore`.
- Default demo credentials should be changed or removed before any public production deployment.
- Consider adding rate limiting and HTTPS termination (e.g. via Nginx or a cloud load balancer) for production environments.

---

## 📦 Requirements

A `requirements.txt` for this project should include:

```
streamlit>=1.30.0
pandas>=2.0.0
numpy>=1.24.0
plotly>=5.18.0
scikit-learn>=1.3.0
textblob>=0.17.1
wordcloud>=1.9.3
matplotlib>=3.7.0
Pillow>=10.0.0
folium>=0.15.0
streamlit-folium>=0.15.0
fpdf>=1.7.2
requests>=2.31.0
```

---
