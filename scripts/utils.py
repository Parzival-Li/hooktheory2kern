import re
# dicts
major_key_signatures = {
    0: "", 7: "f#", 2: "f#c#", 9: "f#c#g#", 4: "f#c#g#d#", 11: "f#c#g#d#a#",
    6: "f#c#g#d#a#e#", 
    5: "b-", 10: "b-e-", 3: "b-e-a-", 8: "b-e-a-d-", 1: "b-e-a-d-g-"}

minor_key_signatures = {
    0:  "b-e-a-", 1:  "f#c#g#d#", 2:  "b-", 3:  "b-e-a-d-g-c-",  
    4:  "f#", 5:  "b-e-a-d-", 6:  "f#c#g#", 7:  "b-e-",        
    8:  "f#c#g#d#a#", 9:  "", 10: "b-e-a-d-g-", 11: "f#c#"}

modal_key_signatures = {
    "dorian": {
        0:  "b-e-",
        1:  "f#c#g#d#a#", 
        2:  "",
        3:  "b-e-a-d-g-",
        4:  "f#c#",
        5:  "b-e-a-",
        6:  "f#c#g#d#", 
        7:  "b-",
        8:  "f#c#g#d#a#e#", 
        9:  "f#",
        10: "b-e-a-d-", 
        11: "f#c#g#",
    },
    "phrygian": {
        0:  "b-e-a-d-",
        1:  "f#c#g#", 
        2:  "b-e-",
        3:  "f#c#g#d#a#",
        4:  "", 
        5:  "b-e-a-d-g-", 
        6:  "f#c#", 
        7:  "b-e-a-",
        8:  "f#c#g#d#",
        9:  "b-",
        10: "f#c#g#d#a#e#",
        11: "f#", 
    },
    "lydian": {
        0:  "f#",
        1:  "b-e-a-d-", 
        2:  "f#c#g#", 
        3:  "b-e-",
        4:  "f#c#g#d#a#",
        5:  "",
        6:  "b-e-a-d-g-",
        7:  "f#c#",
        8:  "b-e-a-",
        9:  "f#c#g#d#",
        10: "b-",
        11: "f#c#g#d#a#e#",
    },
    "mixolydian": {
        0:  "b-", 
        1:  "f#c#g#d#a#e#", 
        2:  "f#",
        3:  "b-e-a-d-",
        4:  "f#c#g#",
        5:  "b-e-",
        6:  "f#c#g#d#a#",
        7:  "",
        8:  "b-e-a-d-g-",
        9:  "f#c#", 
        10: "b-e-a-",
        11: "f#c#g#d#",
    },
    "locrian": {
        0:  "b-e-a-d-g-",
        1:  "f#c#",
        2:  "b-e-a-", 
        3:  "f#c#g#d#",
        4:  "b-", 
        5:  "f#c#g#d#a#e#", 
        6:  "f#",
        7:  "b-e-a-d-",
        8:  "f#c#g#",
        9:  "b-e-",
        10: "f#c#g#d#a#",
        11: "", 
    },
}

pc_to_name_major = {
    0: "C", 1: "Db", 2: "D", 3: "Eb", 4: "E", 5: "F",
    6: "F#", 7: "G", 8: "Ab", 9: "A", 10: "Bb", 11: "B"
    }

pc_to_name_minor = {
        0: "c", 1: "c#", 2: "d", 3: "eb", 4: "e", 5: "f",
        6: "f#", 7: "g", 8: "g#", 9: "a", 10: "bb", 11: "b"
    }

# chord identification funcs
def tonic_and_signature_identification(key):
    # mapping common modal tonic
    pc_to_name_sharp = {
    0: "C", 1: "C#", 2: "D", 3: "D#", 4: "E", 5: "F",
    6: "F#", 7: "G", 8: "G#", 9: "A", 10: "A#", 11: "B"
    }

    pc_to_name_flat = {
        0: "C", 1: "Db", 2: "D", 3: "Eb", 4: "E", 5: "F",
        6: "Gb", 7: "G", 8: "Ab", 9: "A", 10: "Bb", 11: "B"
    }
    
    intervals = key.get('scale_degree_intervals', [])
    tonic_pc = key.get('tonic_pitch_class', 0)
    if intervals[:6] == [2, 2, 1, 2, 2, 2]:
        mode = 'major'
    elif intervals[:6] == [2, 1, 2, 2, 1, 2]:
        mode = 'minor'
    elif intervals[:7] == [2, 1, 2, 2, 2, 1]:
        mode = 'dorian'
    elif intervals[:7] == [1, 2, 2, 2, 1, 2]:
        mode = 'phrygian'
    elif intervals[:7] == [2, 2, 2, 1, 2, 2]:
        mode = 'lydian'
    elif intervals[:7] == [2, 2, 1, 2, 2, 1]:
        mode = 'mixolydian'
    elif intervals[:7] == [1, 2, 2, 1, 2, 2]:
        mode = 'locrian'
    else:
        mode = 'unknown'

    if mode == 'major':
        tonic_name = pc_to_name_major.get(tonic_pc, f"{tonic_pc}")
        signature = major_key_signatures.get(tonic_pc, "")
        return tonic_name, signature
    
    elif mode == 'minor':
        tonic_name = pc_to_name_minor.get(tonic_pc, f"{tonic_pc}")
        signature = minor_key_signatures.get(tonic_pc, "")
        return tonic_name, signature
    
    elif mode in modal_key_signatures:
        signature = modal_key_signatures[mode].get(tonic_pc, "")
        if "b" in signature and "#" not in signature:
            # flat
            tonic_name = pc_to_name_flat.get(tonic_pc, f"{tonic_pc}") + f"@{mode}"
        elif "#" in signature and "b" not in signature:
            # sharp
            tonic_name = pc_to_name_sharp.get(tonic_pc, f"{tonic_pc}") + f"@{mode}"
        else:
            # major as fallback
            tonic_name = pc_to_name_major.get(tonic_pc, f"{tonic_pc}") + f"@{mode}"
        return tonic_name, signature
    
    else:
        # major as fallback
        signature = major_key_signatures.get(tonic_pc, "")
        tonic_name = pc_to_name_major.get(tonic_pc, f"{tonic_pc}")
        return tonic_name+"?", signature

def prefer_flats_from_tonic(signature):
    '''
    Identify if a tonic is flat
    '''
    if '-' in signature:
        return True
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

def label_chord_from_harmony(harmony, signature):
    prefer_flats = prefer_flats_from_tonic(signature)
    root_pc = harmony.get('root_pitch_class', 0)
    root_name = root_to_name(root_pc, prefer_flats)

    intervals = harmony.get('root_position_intervals', [])
    q = quality_from_intervals(intervals)
    if q is None:
        q = quality_from_pcset(intervals_to_pcset(intervals))
    return f"{root_name}{q}"

# note name identification funcs
def pitch_class_to_kern(pitch_class, octave, prefer_flats=False):
    """
    Convert pitch class and octave to kern notation.
    Assumes:
        - pitch_class: 0 = C, 1 = C#, ..., 11 = B;
        - octave: MIDI-style integer, 4 stands for Middle C octave;

    Returns:
        kern-formatted note string (e.g. 'c', 'B', 'cc', 'AA')
    """
    sharp_names = ['c', 'c#', 'd', 'd#', 'e', 'f', 'f#', 'g', 'g#', 'a', 'a#', 'b']
    flat_names  = ['c', 'd-', 'd', 'e-', 'e', 'f', 'g-', 'g', 'a-', 'a', 'b-', 'b']
    
    base = flat_names[pitch_class] if prefer_flats else sharp_names[pitch_class]
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
    triplet_bases = [1.0, 2.0, 4.0, 0.25, 0.5, 0.125, 0.0625]
    for base in triplet_bases:
        triplet_val = base * 2 / 3  # e.g. 0.6666, 1.333, 2.666
        if abs(duration - triplet_val) < 0.01:
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
        0.166667: "16", 
        0.125: "32",  # 32nd note
        0.0833333: "32", # sixteenth triplet
        0.0625: "64", # 64nd note
        0.04166: "64" # 64nd triplet
    }
    keys = duration_map.keys()
    split = split_duration(duration_in_quarter, keys)
    # detect triplet
    is_triplet = False
    if len(split) == 3 and all(abs(split[0] - s) < 0.01 for s in split):
        total = sum(split)
        if (
            abs(total - 2.0) < 0.01 or
            abs(total - 1.0) < 0.01 or
            abs(total - 0.5) < 0.01 or
            abs(total - 0.25) < 0.01 or
            abs(total - 0.125) < 0.01
        ):
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
            elif (i > 0) and (i == len(split) - 1):
                kern_val += "]"
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
def melody_to_kern(melody, meter, num_beats, signature):
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
        
        if "-" in signature:
            prefer_flats = True
        else:
            prefer_flats = False

        kern_pitch = pitch_class_to_kern(pitch_class, octave, prefer_flats)
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
    tonic_name, signature = tonic_and_signature_identification(key)
    
    kern_lines.append(f"*k[{signature}]")
    kern_lines.append(f"*{tonic_name}:")
        
    ## beats
    meter = score_metadata.get('meters', [{}])[0]
    beats_per_bar = meter.get('beats_per_bar', 4)
    beat_unit = meter.get('beat_unit', 4)
    kern_lines.append(f"*M{beats_per_bar}/{beat_unit}")
    
    # ---- Body ----
    melody = score_metadata.get('melody', [{}])
    num_beats = score_metadata.get('num_beats')
    melody_lines, melody_onsets = melody_to_kern(melody, meter, num_beats, signature)
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
    # melody = score_metadata.get('melody')
    _, signature = tonic_and_signature_identification(key)
    
    total_beats = len(melody_onsets)
    total_beats_int = int(total_beats)
    beat_line = ['.'] * total_beats_int
    
    for chord in harmony:
        onset = chord['onset']
        chord_label = label_chord_from_harmony(chord, signature)
        
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

def insert_barlines(melody_spine, harmony_spine, meter):
    """
    Insert barlines into both melody and harmony spines based on meter.
    """
    beats_per_bar = meter.get('beats_per_bar', 4)
    beat_unit = meter.get('beat_unit', 4)

    melody_body = melody_spine[:-1] if melody_spine[-1] == "*-" else melody_spine
    harmony_body = harmony_spine[:-1] if harmony_spine and harmony_spine[-1] == "*-" else harmony_spine


    output_melody = []
    output_harmony = [] if harmony_spine else None
    beat_counter = 0.0
    bar_index = 1

    for idx, m_line in enumerate(melody_body):
        output_melody.append(m_line)
        if harmony_body:
            h_line = harmony_body[idx]
            output_harmony.append(h_line)

        if m_line.startswith("*") or m_line.startswith("="):
            continue

        # Extract duration value from the melody line
        match = re.match(r"^(\d+\.?)(?:_|\[|r|[a-gA-Gr#-]+)?", m_line)
        if match:
            dur_str = match.group(1)
            dur_val_map = {
                "1": 4, "2.": 3, "2": 2, "4.": 1.5, "4": 1,
                "8.": 0.75, "8": 0.5, "16.": 0.375, "16": 0.25, "32": 0.125
            }
            dur = dur_val_map.get(dur_str, 0)
            beat_counter += dur * (beat_unit / 4)

            if beat_counter >= beats_per_bar - 1e-6:
                output_melody.append(f"={bar_index}")
                if output_harmony is not None:
                    output_harmony.append(f"={bar_index}")
                bar_index += 1
                beat_counter = 0.0

    # Add back footers
    output_melody.append("*-")
    if output_harmony is not None:
        output_harmony.append("*-")

    return output_melody, output_harmony


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