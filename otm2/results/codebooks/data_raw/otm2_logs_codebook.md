# Descritption of variables in log files

## General log file (e.g., `OTM_Log_Florida_102.dat`)

Contains the following information:

1. Computer operating system (e.g., `Windows-7-6.1.7601-SP1`)
2. PsychoPy version (e.g., `PychoPyVersion:	1.82.01`)
3. Time stamp (e.g., `2018-01-30_15.49.44.621000`)


## Frame rate log file (e.g., `OTM_ScreenLog_Florida_102.dat`)

Comma-separated presentation durations in seconds of a single frame as assessed at the start of the experiment.
As in Experiment 1, most log files contain ten durations.
While investigating the reliability of an initial sample of 68 participants collected at Yale University, we increased the number of recorded presentation durations to 299.
We found the unreliability of the log files in question to be unrelated to the number of recorded durations.
Consequently, some files contain 299 durations.


## Learning procedure log file (e.g., `DataTrials_OTM_102.dat`)

Tab-separated data of the stimuli presented during the learning procedure and participants responses to the behavior descriptions.
Contains the following variables:

| No. | Variable          | Description           |
|-----|-------------------|-----------------------|
|  1  | ParticipantNumber | Unique participant ID |
|  2  | Location          | Data collection site (Florida, Williams, HongKong, Illinois, Yale) |
|  3  | prime             | Briefly flashed word  |
|  4  | BobImage          | File name of the image used as Bob |
|  5  | bobName           | Name used for Bob     |
|  6  | behavior          | Description of behavior |
|  7  | Valence           | Valence of described behavior (pos vs. neg) |
|  8  | responseNumber    | Response indicating whether participant guessed behavior to be typical of Bob (u = not typical vs. c = typical) |
|  9  | correctBehav      | Indicates if participant's response was correct (Correct vs. False) |
| 10  | TrialRT           | Response time        |
| 11  | Block             | Block of the learning procedure (1 vs. 2) |
| 12  | ValenceBlock      | Valence of behavior description and briefly flashed words in block (1 = Positive-negative vs. 2 = Negative-positive) |
| 13  | Valence           | Valence of described behavior (pos vs. neg) |
| 14  | computerName      | Computer used for participation |
| 15  | timeStamp         | Time of participation [YYYY-MM-DD_HH.MM.SS.SSSSSS] |
