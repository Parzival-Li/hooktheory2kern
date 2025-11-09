import os

def write_kern_file(melody_spine, harmony_spine, output_path):
    """
    Combined kern file with melody and harmony spines.
    Args:
        melody_spine: melody spine **kern;
        harmony_spine: harmony spine **mxhm;
        output_path: File path to write the .krn output.

    """
    abs_path = os.path.join(os.path.dirname(__file__), '..', output_path)
    with open(abs_path, 'w', encoding='utf-8') as f:
        f.write('!!!hooktheory2kern converter by Hongbing Li (Nov 2025)\n')
        if not harmony_spine:
            # if harmony is None, only write melody spine
            print('harmony is None')
            for m_line in melody_spine:
                f.write(f"{m_line}\n")
        else:
            for m_line, h_line in zip(melody_spine, harmony_spine):
                f.write(f"{m_line}\t{h_line}\n")
            
if __name__ == "__main__":
    from parse_json import load_json, get_train_songs
    from utils import generate_kern, harmony_to_kern
    
    # read data
    data = load_json("data/Hooktheory.json.gz")
    songs = get_train_songs(data)
    # test 1 song
    song = songs[0]
    # print(song['melody'])
    melody_spine = generate_kern(song)
    harmony_spine = harmony_to_kern(song)
    write_kern_file(melody_spine, harmony_spine, f"output/{song['title']}.krn")