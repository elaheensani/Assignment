import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import seaborn as sns
import matplotlib.pyplot as plt

# Step 1: Create synthetic dataset
def create_synthetic_data(num_events=1000, start_date='2023-01-01', num_days=90):
    # Define possible values
    platforms = ['web', 'ios', 'android']
    event_types = ['login', 'play_video', 'like', 'comment', 'logout']
    user_ids = [f'user_{i}' for i in range(1, 101)]  # 100 users
    video_ids = [f'video_{i}' for i in range(1, 51)]  # 50 videos
    
    data = []
    current_time = datetime.strptime(start_date, '%Y-%m-%d')
    
    for i in range(num_events):
        event_id = i + 1
        user_id = random.choice(user_ids)
        platform = random.choice(platforms)
        event_type = random.choice(event_types)
        
        # Timestamp: random time within the range
        timestamp = current_time + timedelta(
            days=random.randint(0, num_days),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59),
            seconds=random.randint(0, 59)
        )
        timestamp_str = timestamp.strftime('%Y-%m-%d %H:%M:%S')
        
        video_id = None
        watch_time_sec = None
        video_duration_sec = None
        
        if event_type in ['play_video', 'like', 'comment']:
            video_id = random.choice(video_ids)
            video_duration_sec = random.randint(30, 600)  # 30 sec to 10 min
            if event_type == 'play_video':
                watch_time_sec = random.randint(1, video_duration_sec)  # Ensure watch_time <= duration
        
        data.append({
            'event_id': event_id,
            'user_id': user_id,
            'timestamp': timestamp_str,
            'platform': platform,
            'event_type': event_type,
            'video_id': video_id,
            'watch_time_sec': watch_time_sec,
            'video_duration_sec': video_duration_sec
        })
    
    df = pd.DataFrame(data)
    return df

# Generate the data
df = create_synthetic_data(num_events=5000)  # More events for better visualization

# Step 2: Data cleaning and feature engineering
# Convert timestamp to datetime
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Define engagement scores
engagement_map = {
    'comment': 5,
    'like': 3,
    'play_video': 1,
    'login': 0,
    'logout': 0
}

# Create engagement_score column
df['engagement_score'] = df['event_type'].map(engagement_map).fillna(0)

# Step 3: Time series aggregation
# Extract date from timestamp
df['date'] = df['timestamp'].dt.date

# Group by date and platform, sum engagement_score
aggregated_df = df.groupby(['date', 'platform'])['engagement_score'].sum().reset_index()

# Step 4: Reshape data for visualization
# Pivot to wide format
pivot_df = aggregated_df.pivot(index='date', columns='platform', values='engagement_score')

# Fill missing values with 0
pivot_df = pivot_df.fillna(0)

# Ensure all platforms are present
for plat in ['web', 'ios', 'android']:
    if plat not in pivot_df.columns:
        pivot_df[plat] = 0

# Sort by date
pivot_df = pivot_df.sort_index()

# Step 5: Visualization
plt.figure(figsize=(12, 8))
sns.heatmap(pivot_df.T, cmap='YlGnBu', annot=False, fmt='.0f')
plt.title('Daily Engagement Score Heatmap by Platform')
plt.xlabel('Date')
plt.ylabel('Platform')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()