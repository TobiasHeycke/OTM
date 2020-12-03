
# Of Two Minds: A registered replication

Tobias Heycke<sup>†,1,2</sup>, Frederik Aust<sup>†,1,9</sup>, Mahzarin
R. Banaji<sup>3</sup>, Jeremy Cone<sup>8</sup>, Pieter Van
Dessel<sup>5</sup>, Melissa J. Ferguson<sup>10</sup>, Xiaoqing
Hu<sup>6</sup>, Congjiao Jiang<sup>4</sup>, Benedek
Kurdi<sup>3,10</sup>, Robert Rydell<sup>7</sup>, Lisa
Spitzer<sup>1</sup>, Christoph Stahl<sup>1</sup>, Christine
Vitiello<sup>4</sup>, & Jan De Houwer<sup>5</sup>

<sup>1</sup> University of Cologne <sup>2</sup> GESIS - Leibniz
Institute for the Social Sciences <sup>3</sup> Harvard University
<sup>4</sup> University of Florida <sup>5</sup> Ghent University
<sup>6</sup> The University of Hong Kong <sup>7</sup> Indiana University
<sup>8</sup> Williams College <sup>9</sup> University of Amsterdam
<sup>10</sup> Yale University

<sup>†</sup> Tobias Heycke and Frederik Aust contributed equally to this
work.

-----

## Abstract

Several dual-process theories of evaluative learning posit two distinct
implicit (or automatic) and explicit (or controlled) evaluative learning
processes. As such, one may like a person explicitly but simultaneously
dislike them implicitly. Dissociations between direct measures (e.g.,
Likert scales), reflecting explicit evaluations, and indirect measures
(e.g., Implicit Association Test), reflecting implicit evaluations,
support this claim. Rydell et al. (2006) found a striking dissociation
when they brief flashed either positive or negative words prior to
presenting a photograph of a person was with behavioral information of
the opposite valence was presented: IAT scores reflected the valence of
the flashed words whereas rating scores reflected the opposite valence
of the behavioral information. A recent study, however, suggests that
this finding may not be replicable. Given its theoretical importance, we
report two new replication attempts (n = 153 recruited in Belgium,
Germany and the USA; n = TBD recruited in Hong Kong and the USA).

-----

This repository research products associated with the publication. We
provide the experimental software and stimulus material that we are
permitted to share in the `material` directories of each experiment
(e.g. `otm1` or `otm2`). The R Markdown files in the `paper` directory
contain details of how all the analyses reported in the paper were
conducted, as well as instructions on how to rerun the analysis to
reproduce the results. With the help of the R package `papaja` the files
can be rendered into the accepted version of the manuscript in
`PDF`-format. The `results/data_raw` directories contain all the raw
data; merged and processed data files can be found in
`results/data_processed`. The preregistration document for Experiment 1
is provided in `otm1/preregistration`.

## Data

Data were collected at various locations (see paper).

| Study        | Data collection period  |
| ------------ | ----------------------- |
| `otm1`       | 2014-05-13 - 2014-05-23 |
| `otm2pilot`  | 2014-05-13 - 2014-05-23 |
| `otm2pilot2` | 2014-05-13 - 2014-05-23 |

For a description of all data sets and all variables, please see the
file `codebook.md` in this folder.

## Software requirements

### Experimental software

The experiment was programmed using PsychoPy 1.82.01 and 1.83.01. All
files to reproduce the procedure can be found in the Material
sub-directories.

A folder called `data` (where output data is saved), needs to be present
in the same folder as the python script to run the experiment.

### Screen recordings

To give a vivid impression of the experimental procedure, an examplary
screen recording of the procedure is available under `otm1` \>
`screen-recordings`.

  - otm\_1\_sr\_complete.mp4: An example of the full procedure (please
    note that this is not a recording of any of the participants)
  - otm\_1\_sr\_overview.mp4: A shorted version of the video to give a
    brief overview of all parts of the procedure (please note that the
    video does not reflect the actual procedure)

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
