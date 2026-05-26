Smart Tourism Travel ZA 🌍
AI-Powered Tourism & Hospitality Intelligence Platform for South Africa

Smart Tourism Travel ZA is an advanced AI-driven tourism and hospitality platform designed to modernize travel experiences across South Africa. The application combines artificial intelligence, real-time APIs, computer vision, interactive geospatial mapping, and analytics into a unified smart tourism ecosystem for travelers, hotel managers, and administrators.

🌐 Live Demo

https://tourism-travel-j6vy.onrender.com/


🚀 Live Application:
Smart Tourism Travel ZA Live Demo

📂 GitHub Repository:
GitHub Repository

✨ Core Features
🔐 Role-Based Access Control (RBAC)

The platform implements a secure authentication and authorization system using SHA-256 cryptographic password hashing integrated with an SQLite database.

User Roles
👤 Tourist Dashboard

Tourists can:

Explore destinations across South Africa
Access real-time weather intelligence
Discover landmarks using AI image recognition
View hotel locations on live maps
Receive personalized travel recommendations
Chat with the AI travel assistant
🏨 Hotel Manager Dashboard

Managers can:

Monitor hotel analytics and occupancy trends
Track customer sentiment insights
Analyze tourism activity metrics
Generate operational reports
Manage hospitality performance indicators
🛡️ Admin Dashboard

Administrators have access to:

Platform monitoring and telemetry
User and access management
Audit logs and activity tracking
Report generation systems
System-wide operational controls
🌤️ Real-Time Weather Intelligence

The application integrates with the OpenWeather API to deliver live weather insights for destinations across South Africa.

Features
Current temperature and “feels like” conditions
Wind speed and atmospheric visibility
Humidity and pressure analysis
5-day weather forecasting
Dynamic location-based weather search
Error handling and API failover support
📸 AI Landmark Detection System

The platform utilizes Google Vision AI (LANDMARK_DETECTION) to analyze uploaded travel images and identify famous landmarks.

Capabilities
Landmark recognition from uploaded images
Geographic coordinate extraction
Confidence score analysis
Semantic image labeling
Nearby hotel and activity suggestions
Regional travel insights
🤖 Zara — AI Travel Assistant

Zara is an intelligent conversational travel assistant powered by modern large language models such as OpenAI GPT-4o or Anthropic Claude.

AI Features
Smart destination recommendations
South African tourism guidance
Safari, beach, cultural, and adventure travel support
Hotel and accommodation suggestions
Context-aware travel conversations
Offline fallback response handling
🗺️ Smart Hotel Mapping System

An interactive hotel discovery engine powered by Folium and mapping APIs.

Features
Live hotel location visualization
South Africa-only geographic restriction
Dynamic city and province filtering
Hotel category filtering
Interactive map markers
Real-time image integration
Nearby attraction discovery
📊 Analytics & Intelligence

The system includes intelligent analytics modules for tourism and hospitality insights.

Analytics Features
Sentiment analysis using TextBlob
Tourism trend visualization
Predictive hospitality analytics
Interactive Plotly dashboards
Machine learning integration with Scikit-learn
Occupancy and engagement metrics
🏗️ System Architecture
┌────────────────────────────────────────────────────────┐
│                 Streamlit Web Interface                │
└───────────────────┬────────────────────────────────────┘
                    ▼
┌────────────────────────────────────────────────────────┐
│                Core Application Engine                 │
│                                                        │
│   ┌───────────────────┐   ┌────────────────────────┐   │
│   │   SQLite Database │   │  Machine Learning Core │   │
│   └───────────────────┘   └────────────────────────┘   │
└───────────────────┬────────────────────────────────────┘
                    ▼
┌────────────────────────────────────────────────────────┐
│                  External API Services                 │
│                                                        │
│  OpenWeather • Google Vision • OpenAI • Anthropic     │
└────────────────────────────────────────────────────────┘
⚙️ Technology Stack
Frontend & UI
Streamlit
Folium
Streamlit-Folium
Plotly
Backend & Data Processing
Python
Pandas
NumPy
Scikit-learn
TextBlob
Security & Storage
SQLite3
Hashlib (SHA-256)
AI & Computer Vision
OpenAI GPT-4o
Anthropic Claude
Google Vision API
Visualization & Reporting
Matplotlib
FPDF
Pillow (PIL)
