Smart Tourism-travel ZA 🌍
A next-generation, AI-driven Smart Tourism and Hospitality application focused on South Africa. This application leverages advanced cloud APIs, computer vision, data structures, and role-based access controls to create an all-in-one ecosystem for tourists, accommodation managers, and system administrators.

🚀 Key Features
🔐 1. Identity & Access Management (RBAC)
Implements a secure Role-Based Access Control security model utilizing cryptographically salted password hashes (SHA-256) against an integrated SQLite data tier. The portal securely isolates features via custom dashboards:

Tourist: Features tools for travel exploration, live mapping, visual recognition, and itinerary consulting.

Hotel Manager: Yield management platform tracking metrics, property sentiment, and dynamic price optimizations.

Admin: High-level telemetry control with comprehensive audit functionality, report generation engines, and ledger management.

🌤️ 2. Real-Time Climate Intelligence
Integrates natively with the OpenWeather API to fetch dynamic local weather feeds based on location search indexes:

Temperature and "Feels Like" indices.

Atmospheric pressure, visibility, and humidity vectors.

Wind velocity profiles.

5-Day regional structural forecast blocks.

Seamless failover engine handling query context shifts cleanly during sudden provider disconnects.

📸 3. Computer Vision Landmark Core
Connects to the cloud-native Google Vision API Pipeline (LANDMARK_DETECTION) to analyze snapshot metadata from tourist uploads:

Identifies exact latitude/longitude coordinates of historical attractions.

Computes spatial precision and certainty matching metrics.

Extracts computer vision contextual semantic labels.

Suggests activities, regional travel tips, and native system hotels nearby.

🤖 4. "Zara" Advanced AI Travel Consultant
A specialized conversational agent utilizing Claude (Anthropic) or GPT-4o (OpenAI) with context history parsing:

Engineered via system instructions focusing on specific travel archetypes (Safari, Cultural Tourism, Coastal Adventures).

Recommends active network hotels dynamically.

Provides contextual fallback rules for offline stability.

🗺️ 5. Spatial Hotel Engine & Live Asset Media
An interactive geographical map module powered by Folium and Google Places API:

Strict bounds enforcement limiting the context to South Africa.

Dynamic filtering models sorting markers by city, province, or establishment type.

Rich descriptive metadata overlays mapped directly to live image galleries.

🛠️ Architecture & Core Dependencies
┌────────────────────────────────────────────────────────┐
│               Streamlit Web Interface                  │
└───────────────────┬────────────────────────────────────┘
                    ▼
┌────────────────────────────────────────────────────────┐
│             Core Application Engine                    │
│   ┌───────────────────┐    ┌───────────────────────┐   │
│   │   SQLite DB Layer │    │   SciKit-Learn Models │   │
│   └───────────────────┘    └───────────────────────┘   │
└───────────────────┬────────────────────────────────────┘
                    ▼
┌────────────────────────────────────────────────────────┐
│                  External API Layer                    │
│  [OpenWeather]  [Google Vision]  [OpenAI / Anthropic]  │
└────────────────────────────────────────────────────────┘
The system requires the following core modern stack layers:

UI Framework: streamlit, streamlit_folium, folium

Data Structures & Analytics: pandas, numpy, plotly

Security & Persistence: sqlite3, hashlib

Data Processing: scikit-learn, textblob

Document Engines: fpdf, pillow (PIL), matplotlib
