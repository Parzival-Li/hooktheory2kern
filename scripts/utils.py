def pitch_class_to_kern(pitch_class, octave):
    """
    Convert pitch class and octave to kern notation.
    Assumes:
        - pitch_class: 0 = C, 1 = C#, ..., 11 = B;
        - octave: MIDI-style integer, 4 stands for Middle C octave;

    Returns:
        kern-formatted note string (e.g. 'c', 'B', 'cc', 'AA')
    """
    note_names = ['c', 'c#', 'd', 'd#', 'e', 'f', 'f#', 'g', 'g#', 'a', 'a#', 'b']
    base = note_names[pitch_class % 12]
    octave_shift = octave
    if octave_shift > 0:
        base = base.lower() * (1 + octave_shift)
    elif octave_shift < 0:
        base = base.upper() * (abs(octave_shift))
    else:
        base = base.lower()
    return base

def duration_to_kern(duration):
    """
    Convert duration(offset-onset) in beats to kern rhythmic value
    """
    duration_map = {
        4.0: "1",     # whole note
        3.0: "2.",    # dotted half note
        2.0: "2",     # half note
        1.5: "4.",    # dotted quarter note
        1.0: "4",     # quarter note
        0.75: "8.",   # dotted eighth note
        0.5: "8",     # eighth note
        0.375: "16.", # dotted sixteenth note
        0.25: "16",   # sixteenth note
        0.125: "32",  # 32nd note
    }
    if duration in duration_map:
        return duration_map[duration]
    
    for fix_val, kern_val in duration_map.items():
        if abs(duration-fix_val) < 0.01:
            return kern_val
    print(f"[Warning] Unknown duration: {duration}, fallback to quarter note")
    return "4" # quarter note as fallback

def melody_to_kern(melody):
    """
    Covert [melody] in [annotations] into kern string list.
    Args:
        melody: list of dict，including onset, offset, pitch_class, octave;

    Returns:
        List of string：e.g. ["4B,,", "c#8", "D2."]
    """
    kern_notes = []
    for note in melody:
        onset = note['onset']
        offset = note['offset']
        octave = note['octave']
        pitch_class = note['pitch_class']
        # calculation
        duration = offset - onset
        kern_pitch = pitch_class_to_kern(pitch_class, octave)
        kern_duration = duration_to_kern(duration)
        kern_notes.append(f"{kern_duration}{kern_pitch}")
        
    return kern_notes
    
def generate_kern(score_metadata):
    """
    Generate full kern format string for a single song.
    Args:
        score_metadata: annotations["meters"], annotations["keys"], annotations["num_beats"], annotations["melody"]
    Returns:
        str: .krn content as plain text
    """
    # ---- Header ----
    kern_lines = []
    kern_lines.append("**kern")
    kern_lines.append("*clefG2")
    ## key signatures
    key = score_metadata.get('keys', [{}])[0]
    tonic_pc = key.get('tonic_pitch_class', 0) # C as fallback
    intervals = key.get('scale_degree_intervals', [])
    
    major_key_signatures = {
    0: "", 7: "f#", 2: "f#c#", 9: "f#c#g#", 4: "f#c#g#d#", 11: "f#c#g#d#a#",
    6: "f#c#g#d#a#e#", 1: "f#c#g#d#a#e#b#",
    5: "b-", 10: "b-e-", 3: "b-e-a-", 8: "b-e-a-d-"}
    note_names = ['c', 'c#', 'd', 'd#', 'e', 'f', 'f#', 'g', 'g#', 'a', 'a#', 'b']
    
    signature = major_key_signatures.get(tonic_pc, "")
    kern_lines.append(f"*k[{signature}]")
    
    ## tonic
    if intervals[:6] == [2, 2, 1, 2, 2, 2]:
        mode = 'major'
    elif intervals[:6] == [2, 1, 2, 2, 1, 2]:
        mode = 'minor'
    else:
        mode = 'unknown'

    tonic_name = note_names[tonic_pc]

    if mode == 'major':
        kern_lines.append(f"*{tonic_name.upper()}:")
    elif mode == 'minor':
        kern_lines.append(f"*{tonic_name.lower()}:")
    else:
        kern_lines.append(f"*{tonic_name}?")
        
    ## beats
    meter = score_metadata.get('meters', [{}])[0]
    beats_per_bar = meter.get('beats_per_bar', 4)
    beat_unit = meter.get('beat_unit', 4)
    kern_lines.append(f"*M{beats_per_bar}/{beat_unit}")
    
    
    # ---- Body ----
    melody = score_metadata.get('melody', [{}])
    melody_lines = melody_to_kern(melody)
    kern_lines.extend(melody_lines)
    
    # ---- Foot ----
    kern_lines.append("*-")
    
    return kern_lines

def harmony_to_kern(score_metadata):
    """
    Generate harmony string for a single song.
    Args:
        score_metadata: annotations["melody"], annotations["harmony"]
    Returns:
        str: .krn content as plain text
    """
    kern_lines = ["**mxhm"]
    kern_lines.append("*clefG2")
    kern_lines.extend(['*'] * 3)
    # initialization
    harmony = score_metadata.get('harmony', [{}])
    melody = score_metadata.get('melody', [{}])
    total_beats = len(melody)
    total_beats_int = int(total_beats)
    beat_line = ['.'] * total_beats_int
    melody_idx = 0
    harmony_idx = 0
    # iterate  
    while harmony_idx < len(harmony) and melody_idx < len(melody):
        chord = harmony[harmony_idx]
        onset = chord['onset']
        offset = chord['offset']
        har_duration = offset - onset
        ## chord label
        root = chord['root_pitch_class']
        intervals = chord['root_position_intervals']
        ### major or minor
        if intervals == [4, 3]:
            suffix = ''
        elif intervals == [3, 4]:
            suffix = 'm'
        else:
            suffix = '?'
        ### concat to chord labels
        note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        chord_label = note_names[root] + suffix
        ## align melody spine
        anchor_idx = melody_idx
        total_mel_dur = 0.0

        while melody_idx < len(melody) and total_mel_dur < har_duration:
            mel = melody[melody_idx]
            mel_dur = mel["offset"] - mel["onset"]
            total_mel_dur += mel_dur
            melody_idx += 1

        beat_line[anchor_idx] = chord_label
        harmony_idx += 1

    # to kern spine
    for label in beat_line:
        kern_lines.append(label)
        
    kern_lines.append("*-")
    return kern_lines

if __name__ == "__main__":
    # test pitch_class_to_kern func
    test_cases = [
        (0, 4),   # c
        (4, 5),   # ee
        (11, 2),  # BB
        (7, 3),   # G
    ]

    for pc, octv in test_cases:
        kern_note = pitch_class_to_kern(pc, octv)
        print(f"pitch_class: {pc}, octave: {octv} → kern: {kern_note}")
    
    # test duration_to_kern func
    test_durations = [1.0, 0.5, 0.499999, 0.3]
    for dur in test_durations:
        print(f"{dur} beat → {duration_to_kern(dur)}")
        
    # test melody_to_kern func
    melody = [
        {"onset": 1.0, "offset": 2.0, "pitch_class": 11, "octave": 2},  # 4BB
        {"onset": 2.0, "offset": 3.0, "pitch_class": 0, "octave": 3},   # 4C
        {"onset": 3.0, "offset": 4.0, "pitch_class": 4, "octave": 5},   # 4ee
        {"onset": 4.0, "offset": 8.0, "pitch_class": 7, "octave": 2},   # 1GG
    ]
    result = melody_to_kern(melody)
    print("Kern melody:", result)
    
    # test generate_kern func
    sample_metadata = {
        "meters": [
            {
                "beat": 0,
                "beats_per_bar": 4,
                "beat_unit": 4
            }
        ],
        "melody": [
            {"onset": 0.0, "offset": 1.0, "octave": 3, "pitch_class": 4},   # 4E
            {"onset": 1.0, "offset": 2.0, "octave": 3, "pitch_class": 2},   # 4D
            {"onset": 2.0, "offset": 3.0, "octave": 3, "pitch_class": 0},   # 4C
            {"onset": 3.0, "offset": 4.0, "octave": 3, "pitch_class": 4},   # 4E
        ]
    }

    kern_output = generate_kern(sample_metadata)
    print("\n".join(kern_output))
    
    # test harmony_to_kern func
    sample_metadata = {
    "harmony": [
        {"onset": 0, "offset": 2, "root_pitch_class": 0, "root_position_intervals": [4, 3]},
        {"onset": 2, "offset": 4, "root_pitch_class": 9, "root_position_intervals": [3, 4]},
    ],
    "melody": [
            {"onset": 0.0, "offset": 1.0, "octave": 3, "pitch_class": 4},   # 4E
            {"onset": 1.0, "offset": 2.0, "octave": 3, "pitch_class": 2},   # 4D
            {"onset": 2.0, "offset": 3.0, "octave": 3, "pitch_class": 0},   # 4C
            {"onset": 3.0, "offset": 4.0, "octave": 3, "pitch_class": 4},   # 4E
    ],
    "num_beats": 3
    }
    lines = harmony_to_kern(sample_metadata)
    print("\n".join(lines))