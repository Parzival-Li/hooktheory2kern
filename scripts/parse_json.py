import gzip
import os
import json

def load_json(filepath):
    abs_path = os.path.join(os.path.dirname(__file__), '..', filepath)
    with gzip.open(abs_path, 'rt', encoding='utf-8') as f:
        data = json.load(f)
    return data

def extract_key_fields(song_data):
    return {
    "title": song_data["hooktheory"]["song"],
    "artist": song_data["hooktheory"]["artist"],
    "meters": song_data["annotations"]["meters"],
    "keys": song_data["annotations"]["keys"],
    "melody": song_data["annotations"]["melody"],
    "harmony": song_data["annotations"]["harmony"],
    "num_beats": song_data["annotations"].get("num_beats", None)
    }
    
def get_train_songs(data_dict):
    parsed = []
    for song_id, song in data_dict.items():
        if song['split'] == 'TRAIN':
            parsed.append({
                'id': song_id,
                **extract_key_fields(song)
            }
            )
    return parsed
            
if  __name__ == "__main__":
    data = load_json('data/Hooktheory.json.gz')
    songs = get_train_songs(data)
    print(f"Loaded {len(songs)} TRAIN songs.")
    print("Example:", songs[0]["title"], "-", songs[0]["artist"])

