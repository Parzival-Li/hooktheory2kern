# 📋 Hooktheory2Kern Project Issue Log

| ID | Issue Description | Type | Solution / Action Taken | Notes |
|----|--------------------|------|--------------------------|-------|
| 1 | Most of melody notes had `octave=0`, resulting in unnaturally low pitch output | Data interpretation error | Added `octave += 4` to shift all melody notes to a realistic vocal range | Based on typical MIDI vocal pitch range |
| 2 | Redundant header/footer lines in melody spine and writing script | Structural clarity | Defined: header/footer should be handled inside `generate_kern()` and `harmony_to_kern()`, while the writer only merges the results | Prevents duplicate or misaligned output |
| 3 | Harmony spine printed chord label at every beat instead of using `.` for continuation | Logical inconsistency | Updated logic to only print chord label at chord changes and `.` elsewhere | Matches professor’s reference example |
| 4 | Harmony spine alignment failed | Data alignment issue | Revised logic to align chord labels to melody notes based on cumulative duration matching | Ensures spines remain equal-length and musically aligned |
| 5 | Key signature detection failed | Typo | Uses different indexes in json and functions(`key` in json, but `key` in function) | Unifies into `keys` |
| 6 | Duration values were interpreted assuming quarter note as one beat, ignoring actual beat unit (e.g., 6/8 should use eighth note as one beat) | Misinterpretation of rhythmic unit | Fixed by converting duration using `duration * (4 / beat_unit)` to normalize into quarter note units | Prevents incorrect note value mapping in non-4/4 meters |
| 7 | Sharp notes in higher octaves rendered incorrectly as double-sharps (e.g., `f#f#`) in kern | Pitch rendering bug | Refactored `pitch_class_to_kern()` to separate pitch letter and accidental, then apply octave logic only to the letter | Prevents illegal accidental duplication in Humdrum output |