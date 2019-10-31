
# Of Two Minds: A registered replication

Tobias Heycke, Frederik Aust, Mahzarin R. Banaji, Pieter Van Dessel,
Xiaoqing Hu, Congjiao Jiang, Benedek Kurdi, Robert Rydell, Lisa Spitzer,
Christoph Stahl, Christine A. Vitiello, & Jan De Houwer

-----

Findings of dissociations between implicit (i.e., automatic) and
explicit (i.e., non-automatic) evaluations that are based on distinct
associative (i.e., co-occurrence based) and propositional (i.e.,
rule-based) learning procedures have fueled the dominance of
dual-process theories of evaluative learning for decades. Arguably the
most influential evidence has been found in a study by Rydell,
McConnell, Mackie, and Strain (2006) in which participants learned about
a person named Bob. It was observed that implicit evaluations reflected
the valence of brief pairings of valenced words with the image of Bob
whereas explicit evaluations reflected the (opposite) valence of the
behavioral statements that were instructed to be characteristic of Bob.
A recent study by Heycke and colleagues (2018) was unable to reproduce
this data pattern independently. Given the theoretical importance of the
findings by Rydell et al., we present a series of additional replication
attempts conducted by an international collective of researchers
including the first author of the original finding.

-----

This repository research products associated with the publication. We
provide the experimental software and stimulus material that we are
permitted to share in the `material` directories of each experiment
(e.g. `ml-otm1` or `ml-otm2`). The R Markdown files in the `paper`
directory contain details of how all the analyses reported in the paper
were conducted, as well as instructions on how to rerun the analysis to
reproduce the results. With the help of the R package `papaja` the files
can be rendered into the accepted version of the manuscript in
`PDF`-format. The `results/data_raw` directories contain all the raw
data; merged and processed data files can be found in
`results/data_processed`. The preregistration document for Experiment 1
is provided in `ml-otm1/preregistration`.

## Dataset description

Data were collected collected at various locations (see paper).

| Study        | Data collection period  |
| ------------ | ----------------------- |
| `otm1`       | 2014-05-13 - 2014-05-23 |
| `otm2pilot`  | 2014-05-13 - 2014-05-23 |
| `otm2pilot2` | 2014-05-13 - 2014-05-23 |

Descriptions of the data collection methods are provided in the
preregistration documents and manuscript. Processed data are provided
`RDS`-format, which can be readily imported into R using `loadRDS()`.
Details about the data processing steps are available in the R Markdown
files in the `paper` directory.

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

## Software requirements

### Experimental software

The experiment was programmed using PsychoPy 1.82.01 and 1.83.01. All
files to reproduce the procedure can be found in the Material
sub-directories.

A folder called `data` (where output data is saved), needs to be present
in the same folder as the python script to run the experiment.

### Analyses

Analyses were originally run on Ubuntu 14.04 using R (Version 3.5.3; 217
R Core Team, 2018) and the R-packages afex (Version 0.23.0; Singmann,
Bolker, Westfall, & Aust, 2018), BayesFactor (Version 0.9.12.4.2; Morey
& Rouder, 2018), emmeans (Version 1.3.3; Lenth, 2018), and papaja
(Version 0.1.0.9842; Aust & Barth, 2018).

To install [papaja](https://github.com/crsh/papaja#installation) please
review the installation instructions.

## Funding

The reported research was supported by Methusalem Grant BOF16/MET\_V/002
of Ghent University to Jan De Houwer.

## Licensing information

Manuscript: [CC-BY-4.0](http://creativecommons.org/licenses/by/4.0/)

Code: [MIT](http://opensource.org/licenses/MIT) 2019 Frederik Aust &
Tobias Heycke

Data: [CC-BY-4.0](http://creativecommons.org/licenses/by/4.0/)

Material:

  - Experimental software:
    [CC-BY-4.0](http://creativecommons.org/licenses/by/4.0/)
  - Stimulus material:
    [CC-BY-4.0](http://creativecommons.org/licenses/by/4.0/)

## Contact

Tobias Heycke P.O. 122155 68072 Mannheim Germany

E-mail: <tobias.heycke@gesis.org> / <tobias.heycke@gmail.com>
