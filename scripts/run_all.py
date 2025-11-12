import os
from parse_json import load_json, get_train_songs
from utils import generate_kern, harmony_to_kern, insert_barlines
from convert_to_kern import write_kern_file

def ensure_output_folder(path="outputs"):
    if not os.path.exists(path):
        os.makedirs(path)

def main():
    data = load_json('data/Hooktheory.json.gz')
    train_songs = get_train_songs(data)
    
    ensure_output_folder("outputs")

    print(f"Processing {len(train_songs)} songs...")

    for idx, song in enumerate(train_songs):
        print(f"[{idx+1}/{len(train_songs)}] {song['id']}")
        melody = song.get('melody')
        # if melody is None, pass
        if not melody:
            print(f"Skipped: melody is None.")
            continue
        
        melody_spine, melody_onsets = generate_kern(song)
        harmony_spine = harmony_to_kern(song, melody_onsets)
        melody_spine, harmony_spine = insert_barlines(melody_spine, harmony_spine, song['meters'][0])
        write_kern_file(melody_spine, harmony_spine, f"outputs/{song['id']}.krn")

    print("All songs processed.")

if __name__ == "__main__":
    main()