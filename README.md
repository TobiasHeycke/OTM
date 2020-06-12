
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
(e.g. `otm1` or `otm2`). The R Markdown files in the `paper`
directory contain details of how all the analyses reported in the paper
were conducted, as well as instructions on how to rerun the analysis to
reproduce the results. With the help of the R package `papaja` the files
can be rendered into the accepted version of the manuscript in
`PDF`-format. The `results/data_raw` directories contain all the raw
data; merged and processed data files can be found in
`results/data_processed`. The preregistration document for Experiment 1
is provided in `otm1/preregistration`.

## Data

Data were collected collected at various locations (see paper) at the following
times:

-  `otm1`: between 2014-05-13 and 2014-05-23
-  `otm2pilot`: between 2014-05-13 and 2014-05-23
-  `otm2pilot2`: between 2014-05-13 and 2014-05-23

For a description of all data sets and all variables, please see the file: 
`codebook.md` in the same folder. 

## Software requirements

### Experimental software

The experiment was programmed using PsychoPy 1.82.01 and 1.83.01. All
files to reproduce the procedure can be found in the Material
sub-directories.

A folder called `data` (where output data is saved), needs to be present
in the same folder as the python script to run the experiment.

### Screen recordings

To give a vivid impression of the experimental procedure, an examplary screen recording of the procedure is available under `otm1` > `screen-recordings`.

- otm_1_sr_complete.mp4: An example of the full procedure (please note that this is not a recording of any of the participants)
- otm_1_sr_overview.mp4: A shorted version of the video to give a brief overview of all parts of the procedure (please note that the video does not reflect the actual procedure) 

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

Tobias Heycke

P.O. 122155

68072 Mannheim Germany

E-mail: <tobias.heycke@gesis.org> / <tobias.heycke@gmail.com>
