# Codebook

Descriptions of the data collection methods are provided in the
preregistration documents and manuscript. Processed data are provided in
`RDS`-format, which can be readily imported into R using `readRDS()` (e.g., 
`dat <- readRDS(file = "path/to/file")`). Details about the data processing 
steps are available in the R Markdown files in the `analysis_and_paper` 
directory.

## Data

We provide the raw data (individual text files for each participant and each 
task) as they were saved by the experimental software, as well as processed data
files. Below we will give a detailed description of the data files, as well as 
all variables.


## Processed data

All processed data files can be found within each project folder. For example 
the processed data files for the first study are located at `otm1` > `results` >
`data_processed`.

Generally, four different types of processed data files are provided, which
include one of the following parts in their names:

- Eval = explicit attitude measure
- IAT  = implicit attitude measure
- Attitudes = both explicit and implicit attitudes
- Memory = US recognition task

Processed data files that include`_cleaned` at the end of their names are data
files after incomplete data sets or participants had been removed. 

*For a detailed description of how the processed data files were created, please
see the `manuscript.Rmd` file in the `analysis_and_paper` folder*

*For a detailed description of all variables, please see below.*


## Raw data

Raw data files can be found within each project folder. For example the raw data
files for the first study are located at `otm1` > `results` > `data_raw`.
For each task/part of the experiment (for a list of all data files see  below) 
as well as for each participant a new data file is created. To read in all data 
files for a given task or part (e.g., the IAT), one can use the `batch_read` 
function from `https://gist.githubusercontent.com/crsh/357458c41fd3d554fb24/raw/f7725d5c4894a055a1b2e461dc5c39f3db23b2b8/batch_read.R`
(see the `manuscript.Rmd` file in the `analysis_and_paper` folder for an example
of how to use the `batch_read` function).


Below all variables from each data file will be described:

**General Variables (used in multiple data sets)**

  - ParticipantNumber: Participant Number, consecutive number assigned
    by the experimenter
  - Location: Location of data collection (lab location)
  - computerName: Name of computer used
  - timeStamp: year-month-day-hour-minute-second-ms
  - Block: 1 for measures after first, 2 for measures after second
    block  
  - ValenceBlock: 1 or 2 (between subjects) - 1 means neg primes and pos
    behavior first and vice versa in the second block
  - MeasureOrder: 1 or 2 (between subjects) - 1 means implicit measure
    first, 2 means explicit measure first

**Data\_Demographics\_OTM\_xx**

  - Age: Age of participants (open response)
  - Study: Study / Job (open response)  
  - Gender: Gender (open response)
  - Goal: What do you think was the goal of the experiment?
  - Comment: Any further comments

**DataEval\_OTM\_xx**

  - Name: Name of the target character (always Bob)
  - Eval1: liking of target character on 9 point Likert
  - Eval2: evaluation of target character on 9 point Likert (bad -
    good)  
  - Eval3: evaluation of target character on 9 point Likert (mean -
    pleasant)  
  - Eval4: evaluation of target character on 9 point Likert
    (disagreeable - agreeable)  
  - Eval5: evaluation of target character on 9 point Likert (uncaring -
    caring)
  - Eval6: evaluation of target character on 9 point Likert (cruel -
    kind)
  - Eval7: feeling thermometer score ranging from 0 to 100

**DataMemTest\_OTM\_xx**

  - NumbercorrectIdent: Number of correctly identified primes (between 0
    and 20)
  - chosenItems: List of all 20 items chosen by participant
  - correctList: a list corresponding to the chosenItems, indicating for
    each item whether it was indeed a prime (“correctIdent”) or not.

**DataIAT\_OTM\_xx**

  - IATBlock: could be 1, 2, 34, 5 or 67 referring to the 20 trial
    blocks within each IAT (block 34 and 67 are the critical blocks)  
  - Stimulus: Which stimulus was shown during the trial  
  - Category: whether the stimulus was an image or a word
  - Type: whether stimulus was target character (called Bob in data
    file) or not (“NonBob”) or a positive or negative word
  - keyToPress: the correct key for the trial  
  - keyPress: the key pressed by participant at first
  - Correct: whether first key press was correct or not (“error”)
  - RT: RT after first button press  
  - RTafterError: total RT (from stimulus onset) until correct button
    was pressed - zero if correct button was pressed as first button
    press
  - Combination: could be 1 or 2 (between subjects) - 1 means target
    character and negative in Block 34 and target and positive in block
    67 and vice versa if number 2 was assigned

**DataTrials\_OTM\_xx**

*In this file a new line for each new trial during the learning phase
was created and the files can be considered a protocol of the learning
phase*

  - prime: which US was shown
  - BobImage: which image was shown after the US
  - bobName: always Bob (previously other names were also used)
  - behavior: which behavioral statement was shown
  - Valence: was the behavioral statement positive or negative
  - responseNumber: did participants answer with the c or u key
  - correctBehav: was the answer correct or incorrect (Correct, False)
  - TrialRT: what was the reaction time of the participants in that
    trial

**OTM\_Log\_xx**

*In this file the operating system, the PsychoPy version and the date is
saved*

**OTM\_ScreenLog\_xx**

*At start-up of the script, the duration of the first 9 frames was
measured. This allowed us to check whether the frame rate was set
correctly.*
