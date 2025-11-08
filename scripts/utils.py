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
    octave_shift = octave - 4
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
    
def generate_kern(score_metadata, melody):
    """
    Generate full kern format string for a single song.
    Args:
        score_metadata: annotations["meters"], annotations["keys"], annotations["num_beats"]
        melody: annotations["melody"]
    Returns:
        str: .krn content as plain text
    """
    # ---- Header ----
    kern_lines = []
    kern_lines.append("**kern")
    kern_lines.append("*clefG2")
    meter = score_metadata.get('meters', [{}])[0]
    beats_per_bar = meter.get('beats_per_bar', 4)
    beat_unit = meter.get('beat_unit', 4)
    kern_lines.append(f"*M{beats_per_bar}{beat_unit}")
    
    key = score_metadata.get('keys', [{}])[0]
    tonic_pc = key.get('tonic_pitch_class', 0) # C as fallback
    kern_lines.append(f"*k[{tonic_pc}]")
    
    # ---- Body ----
    melody_lines = melody_to_kern(melody)
    kern_lines.extend(melody_lines)
    
    # ---- Foot ----
    kern_lines.append("*-")
    
    return "\n".join(kern_lines)

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
        ]
    }

    sample_melody = [
        {"onset": 0.0, "offset": 1.0, "octave": 3, "pitch_class": 4},   # 4E
        {"onset": 1.0, "offset": 2.0, "octave": 3, "pitch_class": 2},   # 4D
        {"onset": 2.0, "offset": 3.0, "octave": 3, "pitch_class": 0},   # 4C
        {"onset": 3.0, "offset": 4.0, "octave": 3, "pitch_class": 4},   # 4E
    ]

    kern_output = generate_kern(sample_metadata, sample_melody)
    print(kern_output)