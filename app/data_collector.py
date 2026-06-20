"""
Data Collector - Track caption generation patterns
"""

import json
import pandas as pd
from datetime import datetime
import os

class CaptionDataCollector:
    """Collect and analyze caption generation data"""
    
    def __init__(self):
        self.data_file = "data/caption_data.json"
        self.csv_file = "data/caption_stats.csv"
        self.data = []
        os.makedirs("data", exist_ok=True)
        self._load_data()
    
    def _load_data(self):
        try:
            with open(self.data_file, 'r') as f:
                self.data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.data = []
    
    def record_generation(self, topic, style, captions, response_time):
        record = {
            "timestamp": datetime.now().isoformat(),
            "topic": topic,
            "style": style,
            "num_captions": len(captions),
            "response_time": response_time,
            "avg_caption_length": sum(len(c) for c in captions) / len(captions) if captions else 0
        }
        self.data.append(record)
        self._save_data()
        return record
    
    def _save_data(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.data, f, indent=2)
        self._export_to_csv()
    
    def _export_to_csv(self):
        if not self.data:
            return
        flat_data = []
        for record in self.data:
            flat_record = {
                "timestamp": record.get("timestamp", ""),
                "topic": record.get("topic", ""),
                "style": record.get("style", ""),
                "num_captions": record.get("num_captions", 0),
                "response_time": record.get("response_time", 0),
                "avg_caption_length": record.get("avg_caption_length", 0)
            }
            flat_data.append(flat_record)
        df = pd.DataFrame(flat_data)
        df.to_csv(self.csv_file, index=False)
    
    def get_stats(self):
        if not self.data:
            return {
                "total_generations": 0,
                "top_topics": {},
                "top_styles": {},
                "avg_response_time": 0,
                "max_captions": 0
            }
        df = pd.DataFrame(self.data)
        return {
            "total_generations": len(self.data),
            "top_topics": df['topic'].value_counts().head(3).to_dict(),
            "top_styles": df['style'].value_counts().head(3).to_dict(),
            "avg_response_time": df['response_time'].mean(),
            "max_captions": df['num_captions'].max()
        }

collector = CaptionDataCollector()