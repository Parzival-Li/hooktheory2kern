# dicts
major_key_signatures = {
    0: "", 7: "f#", 2: "f#c#", 9: "f#c#g#", 4: "f#c#g#d#", 11: "f#c#g#d#a#",
    6: "f#c#g#d#a#e#", 1: "f#c#g#d#a#e#b#",
    5: "b-", 10: "b-e-", 3: "b-e-a-", 8: "b-e-a-d-"}

pc_to_name_major = {
    0: "C", 1: "Db", 2: "D", 3: "Eb", 4: "E", 5: "F",
    6: "Gb", 7: "G", 8: "Ab", 9: "A", 10: "Bb", 11: "B"
    }

pc_to_name_minor = {
        0: "c", 1: "c#", 2: "d", 3: "eb", 4: "e", 5: "f",
        6: "f#", 7: "g", 8: "ab", 9: "a", 10: "bb", 11: "b"
    }

# chord identification funcs
def tonic_identification(key):
    intervals = key.get('scale_degree_intervals', [])
    tonic_pc = key.get('tonic_pitch_class', 0)
    if intervals[:6] == [2, 2, 1, 2, 2, 2]:
        mode = 'major'
    elif intervals[:6] == [2, 1, 2, 2, 1, 2]:
        mode = 'minor'
    else:
        mode = 'unknown'

    if mode == 'major':
        tonic_name = pc_to_name_major.get(tonic_pc, f"{tonic_pc}")
        return tonic_name
    elif mode == 'minor':
        tonic_name = pc_to_name_minor.get(tonic_pc, f"{tonic_pc}")
        return tonic_name
    else:
        tonic_name = pc_to_name_minor.get(tonic_pc, f"{tonic_pc}")
        return tonic_name+"?"

def prefer_flats_from_tonic(tonic):
    '''
    Identify if a tonic is flat
    '''
    if tonic is None:
        return False
    t = tonic.replace('♭', 'b').replace('♯', '#').strip()
    if 'b' in t:
        return True
    sharp_keys = {
        'G','D','A','E','B','F#','C#',
        'Em','Bm','F#m','C#m','G#m','D#m','A#m'
    }
    flat_keys = {
        'F','Bb','Eb','Ab','Db','Gb','Cb',
        'Dm','Gm','Cm','Fm','Bbm','Ebm','Abm','Dbm','Gbm','Cbm'
    }
    if t in flat_keys:
        return True
    if t in sharp_keys:
        return False
    return False

def root_to_name(pc, prefer_flats):
    '''
    Define root pitch
    '''
    pc = int(pc) % 12
    names_sharp = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
    names_flat  = ['C','Db','D','Eb','E','F','Gb','G','Ab','A','Bb','B']
    return names_flat[pc] if prefer_flats else names_sharp[pc]

def intervals_to_pcset(intervals):
    '''
    Intervals to pitch-class set
    '''
    pcs = []
    s = 0
    for d in intervals:
        s += int(d)
        pcs.append(s % 12)
    # drop 0
    return frozenset(p for p in pcs if p != 0)

def quality_from_intervals(intervals):
    '''
    Detect standard triads and seventh chords
    '''
    iv = list(map(int, intervals))
    if iv == [4, 3]:      return ''      
    if iv == [3, 4]:      return 'm'       
    if iv == [3, 3]:      return 'dim'   
    if iv == [4, 4]:      return 'aug'     
    if iv == [4, 3, 3]:   return '7'     
    if iv == [4, 3, 4]:   return 'maj7'   
    if iv == [3, 4, 3]:   return 'm7'    
    if iv == [3, 3, 4]:   return 'm7b5'    
    if iv == [3, 3, 3]:   return 'dim7'
    return None 

def quality_from_pcset(pcset: frozenset):
    """
    Identify chord from a pitch-class set relative to the root
    """
    P = pcset

    # Power chord
    if P == {7}:
        return '5'

    # Suspended triads
    if P == {2, 7}:           return 'sus2'
    if P == {5, 7}:           return 'sus4'

    # Suspended sevenths
    if P == {5, 7, 10}:       return '7sus4'
    if P == {2, 7, 10}:       return '7sus2'

    # Add chords
    if P == {2, 4, 7}:        return 'add9' 
    if P == {2, 3, 7}:        return 'm(add9)'
    if P == {4, 5, 7}:        return 'add11'
    if P == {3, 5, 7}:        return 'm(add11)'
    if P == {4, 7, 9}:        return '6' 
    if P == {3, 7, 9}:        return 'm6'
    if P == {2, 4, 7, 9}:     return '6/9'
    if P == {2, 3, 7, 9}:     return 'm6/9'

    # Standard triads
    if P == {4, 7}:           return ''
    if P == {3, 7}:           return 'm'
    if P == {3, 6}:           return 'dim'
    if P == {4, 8}:           return 'aug'

    # Seventh chords
    if P == {4, 7, 10}:       return '7'
    if P == {4, 7, 11}:       return 'maj7'
    if P == {3, 7, 10}:       return 'm7'
    if P == {3, 6, 10}:       return 'm7b5'
    if P == {3, 6, 9}:        return 'dim7'
    if P == {3, 7, 11}:       return 'm(maj7)'
    
    # Altered dominant types
    if P == {4, 8, 10}:
        return '7(#5)'
    # #5 b9
    if P == {4, 8, 10, 1}:
        return '7(#5,b9)'
    # b9
    if P == {4, 7, 10, 1}:
        return '7(b9)'

    # fallback
    return ''

def label_chord_from_harmony(harmony, tonic):
    prefer_flats = prefer_flats_from_tonic(tonic)
    root_pc = harmony.get('root_pitch_class', 0)
    root_name = root_to_name(root_pc, prefer_flats)

    intervals = harmony.get('root_position_intervals', [])
    q = quality_from_intervals(intervals)
    if q is None:
        q = quality_from_pcset(intervals_to_pcset(intervals))
    return f"{root_name}{q}"

# note name identification funcs
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
    letter = base[0]
    accidental = base[1:]
    octave_shift = octave
    if octave_shift > 0:
        base = (letter.lower() * (1 + octave_shift)) + accidental
    elif octave_shift < 0:
        base = (letter.upper() * (abs(octave_shift))) + accidental
    else:
        base = letter.lower() + accidental
    return base

# duration split
def split_duration(duration, duration_map_keys):
    result = []
    remaining = duration
    # detect triplet
    triplet_bases = [1.0, 2.0, 4.0]
    for base in triplet_bases:
        triplet_val = base * 2 / 3  # e.g. 0.6666, 1.333, 2.666
        if abs(duration - triplet_val) < 0.02:
            return [base / 3] * 3
    
    while remaining > 0.01:
        for val in sorted(duration_map_keys, reverse=True):
            if val <= remaining + 1e-6:
                result.append(val)
                remaining -= val
                break
        else:
            # avoid infinite loop
            print(f"[Warning] Cannot match remaining duration: {remaining}")
            break
    return result

def duration_to_kern(duration, beat_unit=4):
    """
    Convert duration(offset-onset) in beats to kern rhythmic value
    """
    duration_in_quarter = duration * (4 / beat_unit)
    
    duration_map = {
        4.0: "1",     # whole note
        3.0: "2.",    # dotted half note
        2.0: "2",     # half note
        1.5: "4.",    # dotted quarter note
        1.0: "4",     # quarter note
        0.75: "8.",   # dotted eighth note
        0.6666667: "4", # quarter triplet
        0.5: "8",     # eighth note
        0.375: "16.", # dotted sixteenth note
        0.3333333: "8", # eighth triplet
        0.25: "16",   # sixteenth note
        0.125: "32",  # 32nd note
    }
    keys = duration_map.keys()
    split = split_duration(duration_in_quarter, keys)
    # detect triplet
    is_triplet = False
    if len(split) == 3 and all(abs(split[0] - s) < 0.01 for s in split):
        total = sum(split)
        if abs(total - 2.0) < 0.1 or abs(total - 1.0) < 0.1 or abs(total - 0.5) < 0.05:
            is_triplet = True
    
    kern_parts = []
    for i, dur in enumerate(split):
        # kern_val = duration_map.get(dur)
        def lookup_kern_value(duration, duration_map, tolerance=0.0001):
            for dur_val, kern in duration_map.items():
                if abs(duration - dur_val) < tolerance:
                    return kern
        kern_val = lookup_kern_value(dur, duration_map)
        
        if not kern_val:
            print(f"[Warning] Unexpected sub-duration: {dur}")
            kern_val = "4"  # fallback
        if is_triplet:
            if i == 0:
                kern_val += "L"
            elif i == 2:
                kern_val += "J"
        else:
            # add tie if more than one element
            if i < len(split) - 1:
                kern_val += "["  
        kern_parts.append(kern_val)
    return kern_parts

def r_to_duration(r):
    """
    Convert kern rest symbol (e.g. "8r", "8.Lr", "4Jr") to duration in quarter notes.
    Supports triplet markers: L (start), J (end).
    """
    r = r.replace("r", "").replace("[", "")
    is_triplet = "L" in r or "J" in r
    r = r.replace("L", "").replace("J", "")

    duration_map = {
        "1": 4.0, "2.": 3.0, "2": 2.0, "4.": 1.5, "4": 1.0,
        "8.": 0.75, "8": 0.5, "16.": 0.375, "16": 0.25, "32": 0.125
    }

    dur = duration_map.get(r, 1.0)
    if is_triplet:
        dur *= 2 / 3
    return dur

def d_to_duration(kern_val):
    """
    Convert kern note symbol (e.g. "8L", "8J", "4[") to duration in quarter notes.
    Removes tie symbols and interprets triplet markers.
    """
    val = kern_val.replace("[", "").replace("_", "")
    is_triplet = "L" in val or "J" in val
    val = val.replace("L", "").replace("J", "")

    duration_map = {
        "1": 4.0, "2.": 3.0, "2": 2.0, "4.": 1.5, "4": 1.0,
        "8.": 0.75, "8": 0.5, "16.": 0.375, "16": 0.25, "32": 0.125
    }

    dur = duration_map.get(val, 1.0)
    if is_triplet:
        dur *= 2 / 3
    return dur

# melody spine generation
def melody_to_kern(melody, meter, num_beats):
    """
    Covert [melody] in [annotations] into kern string list.
    Args:
        melody: list of dict，including onset, offset, pitch_class, octave;

    Returns:
        List of string：e.g. ["4B,,", "c#8", "D2."]
    """
    kern_notes = []
    onsets = []
    
    beat_unit = meter['beat_unit']
    def add_rest(start, end):
        rest_duration = end - start
        rest_kerns = duration_to_kern(rest_duration, beat_unit)
        if not isinstance(rest_kerns, list):
            rest_kerns = [rest_kerns]
        for r in rest_kerns:
            r = r.replace("[", "")
            kern_notes.append(f"{r}r")
            onsets.append(start)
            start += r_to_duration(r)
    
    melody = sorted(melody, key=lambda x: x['onset'])
    prev_offset = 0.0
    for note in melody:
        onset = note['onset']
        offset = note['offset']
        octave = note['octave']
        pitch_class = note['pitch_class']
        # calculation
        duration = offset - onset
        
        # If there's a rest before this note
        if onset > prev_offset:
            add_rest(prev_offset, onset)
        
        kern_duration = duration_to_kern(duration, beat_unit)
        if not isinstance(kern_duration, list):
            kern_duration = [kern_duration]
        
        kern_pitch = pitch_class_to_kern(pitch_class, octave)
        for i, dur in enumerate(kern_duration):
            if i == 0:
                kern_notes.append(f"{dur}{kern_pitch}")
            else:
                kern_notes.append(f"{dur}{kern_pitch}")
            onsets.append(onset)  # 🔴 对应 melody_onsets
            onset += d_to_duration(dur)
        
        prev_offset = offset
        
    # Final rest if song ends early
    if prev_offset < num_beats:
        add_rest(prev_offset, num_beats)
            
    return kern_notes, onsets
    
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
    signature = major_key_signatures.get(tonic_pc, "")
    kern_lines.append(f"*k[{signature}]")
    
    ## tonic
    tonic_name = tonic_identification(key)
    kern_lines.append(f"*{tonic_name}:")
        
    ## beats
    meter = score_metadata.get('meters', [{}])[0]
    beats_per_bar = meter.get('beats_per_bar', 4)
    beat_unit = meter.get('beat_unit', 4)
    kern_lines.append(f"*M{beats_per_bar}/{beat_unit}")
    
    # ---- Body ----
    melody = score_metadata.get('melody', [{}])
    num_beats = score_metadata.get('num_beats')
    melody_lines, melody_onsets = melody_to_kern(melody, meter, num_beats)
    kern_lines.extend(melody_lines)
    
    # ---- Foot ----
    kern_lines.append("*-")
    
    return kern_lines, melody_onsets

# harmony spine generation
def harmony_to_kern(score_metadata, melody_onsets):
    """
    Generate harmony string for a single song.
    Args:
        score_metadata: annotations["melody"], annotations["harmony"]
    Returns:
        str: .krn content as plain text
    """
    ## if harmony is None, return None as harmony spine
    if score_metadata.get('harmony') is None:
        return None
    
    kern_lines = []

    # initialization
    key = score_metadata.get('keys', [{}])[0]
    harmony = score_metadata.get('harmony')
    melody = score_metadata.get('melody')
    tonic_name = tonic_identification(key)
    
    total_beats = len(melody_onsets)
    total_beats_int = int(total_beats)
    beat_line = ['.'] * total_beats_int
    
    # melody_idx = 0
    # harmony_idx = 0
    # # iterate  
    # while harmony_idx < len(harmony) and melody_idx < len(melody):
    #     chord = harmony[harmony_idx]
    #     onset = chord['onset']
    #     offset = chord['offset']
    #     har_duration = offset - onset
    #     # identify chord
    #     chord_label = label_chord_from_harmony(chord, tonic_name)
        
    #     ## align melody spine
    #     anchor_idx = melody_idx
    #     total_mel_dur = 0.0

    #     while melody_idx < len(melody) and total_mel_dur < har_duration:
    #         mel = melody[melody_idx]
    #         mel_dur = mel["offset"] - mel["onset"]
    #         total_mel_dur += mel_dur
    #         melody_idx += 1

    #     beat_line[anchor_idx] = chord_label
    #     harmony_idx += 1
    for chord in harmony:
        onset = chord['onset']
        chord_label = label_chord_from_harmony(chord, tonic_name)
        
        # find the closet index in melody_onsets
        anchor_idx = next((i for i, t in enumerate(melody_onsets) if t >= onset), None)
        if anchor_idx is not None and anchor_idx < len(beat_line):
            beat_line[anchor_idx] = chord_label

    # to kern spine
    for label in beat_line:
        kern_lines.append(label)
  
    header = ["**mxhm", "*clefG2", "*", "*", "*"]
    kern_lines = header + kern_lines
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
        print(f"{dur} beat → {duration_to_kern(dur, 8)}")
        
    # test melody_to_kern func
    melody = [
        {"onset": 1.0, "offset": 2.0, "pitch_class": 11, "octave": 2},  # 4BB
        {"onset": 2.0, "offset": 3.0, "pitch_class": 0, "octave": 3},   # 4C
        {"onset": 3.0, "offset": 4.0, "pitch_class": 4, "octave": 5},   # 4ee
        {"onset": 4.0, "offset": 8.0, "pitch_class": 7, "octave": 2},   # 1GG
    ]
    result = melody_to_kern(melody, meter = {'beat': 0, 'beats_per_bar': 3, 'beat_unit': 4})
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