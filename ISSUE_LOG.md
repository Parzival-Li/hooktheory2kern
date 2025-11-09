# 📋 Hooktheory2Kern Project Issue Log

| ID | Issue Description | Type | Solution / Action Taken | Notes |
|----|--------------------|------|--------------------------|-------|
| 1 | Most of melody notes had `octave=0`, resulting in unnaturally low pitch output | Data interpretation error | Added `octave += 4` to shift all melody notes to a realistic vocal range | Based on typical MIDI vocal pitch range |
| 2 | Redundant header/footer lines in melody spine and writing script | Structural clarity | Defined: header/footer should be handled inside `generate_kern()` and `harmony_to_kern()`, while the writer only merges the results | Prevents duplicate or misaligned output |
| 3 | Harmony spine printed chord label at every beat instead of using `.` for continuation | Logical inconsistency | Updated logic to only print chord label at chord changes and `.` elsewhere | Matches professor’s reference example |
| 4 | Harmony spine alignment failed | Data alignment issue | Revised logic to align chord labels to melody notes based on cumulative duration matching | Ensures spines remain equal-length and musically aligned |