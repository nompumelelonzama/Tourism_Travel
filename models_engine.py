import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
import gymnasium as gym
from stable_baselines3 import PPO

# 1. REGRESSION: Occupancy Prediction
def train_regression_model(df):
    X = df[['season_idx', 'avg_rating', 'price_index', 'holiday_flag']]
    y = df['occupancy_rate']
    model = RandomForestRegressor(n_estimators=100)
    model.fit(X, y)
    return model

# 2. CLASSIFICATION: Cancellation Risk
def train_classification_model(df):
    X = df[['lead_time', 'previous_cancellations', 'total_guests', 'booking_changes']]
    y = df['is_cancelled']
    model = RandomForestClassifier()
    model.fit(X, y)
    return model

# 3. RECOMMENDATION: Content-Based Filtering
def get_recommendations(hotel_df, user_prefs):
    # user_prefs: [Luxury_Score, Budget_Score, Family_Score]
    features = hotel_df[['luxury', 'budget', 'family']]
    sim = cosine_similarity([user_prefs], features)
    hotel_df['sim_score'] = sim[0]
    return hotel_df.sort_values(by='sim_score', ascending=False).head(3)

# 4. REINFORCEMENT LEARNING: Dynamic Pricing Environment
class PricingEnv(gym.Env):
    def __init__(self):
        super(PricingEnv, self).__init__()
        self.action_space = gym.spaces.Discrete(3) # 0: Lower Price, 1: Keep, 2: Increase
        self.observation_space = gym.spaces.Box(low=0, high=100, shape=(1,), dtype=np.float32)
        self.state = np.array([50.0]) # Starting occupancy

    def step(self, action):
        if action == 0: self.state -= 5 # Lower price increases occupancy
        if action == 2: self.state += 5 # Higher price decreases occupancy
        reward = self.state[0] if 70 <= self.state[0] <= 90 else -10
        done = True
        return self.state, reward, done, False, {}

    def reset(self, seed=None):
        self.state = np.array([50.0])
        return self.state, {}