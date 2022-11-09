# Dave
Fixing video tracking of the bees made by [loopy](http://loopbio.com/loopy/). 

# Case study
1. Honeybee defence response. 352 bees videos of different group sizes. A group is put into an arena with a rotating dummy with a feather on one end which provokes the bees to sting. 

| population_size   | 1  | 3  | 5  | 7  | 10 | 15 |
| ----------------- | ---|----|----|--- |----|----|
| # videos          | 68 | 68 | 60 | 56 | 52 | 48 |

## PREREQUISITES
1. install [Python 3.9](https://www.python.org/downloads/)

## HOW TO INSTALL
1. As we use only Python.  
2. (Optional) We recommend using virtual environment (e.g. [conda](https://docs.conda.io/en/latest/), [pyenv](https://github.com/pyenv/pyenv)) before the following step
3. get non-standard libraries, which you can simply install with the command:

`>> pip install -r requirements`


## DATA FILE TYPES AND CONVENTIONS
all data are located in `data` folder, while there are two types of files
```
\<name\>\_ai.csv
\<name\>\_nn.csv
```
as result of [loopy](http://loopbio.com/loopy/). In this analysis, we use only `_nn.csv` files.

## DATA DOCUMENTATION
```                  
                   - tracking number (this is probably only up to 1000 (eg. see data/190822/<1bee>))
date               - global time stamp (YYYY-MM-DD"T"HH:MM:SS.Milliseconds+??:??) (we do not use this)
err                - error message
frame_count        - frame id
frame_number       - frame id 
frame_timestamp    - approximate time from (do not use this)
name               - name of the tracked object
oid                - id of tracked object
type               - entry type
x                  - position, horizontal axis, (0,0) is left bottom
y                  - position, vertical axis, (0,0) is left bottom
```

## HOW AND WHERE TO STORE INPUT
Select a folder such as `data`. 
Get your `*_nn.csv` files into this folder with/without your folder structure. 

Now, edit `dave.py` (located in `src` folder) that the files you would like to analyse are in the main class and function `analyse` calls the given file with `population_size` (Or simply edit the paths and population sizes of already given calls in the file.) e.g.:

`analyse('../data/Video_tracking/190822/20190822_112842909_2BEE_generated_20210503_074806_nn.csv', 2)`

where the first argument is the relative path to the file and 2 is the population size.

### (OPTIONAL) FIXING FRAME RANGES
In our case studies, the videos were trimmed and hence the first frame of the video was not recognised by loopy as the first. 
If you want to overcome this problem, put the files in one deeper folder `original` and edit `fix_ranges.py` in a similar way as `dave.py` e.g:

`fix_ranges('../data/Video_tracking/190822/20190822_112842909_2BEE_generated_20210503_074806_nn.csv', 2)`

(Or simply edit the paths and population sizes of already given calls in the file.)

Now run file `fix_ranges.py`
```
>> cd src
>> python fix_ranges.py
```
it saves fixed frame ranges by editing `frame_number` column, while keeping column `frame_count` intact. 
if these are the same (in our case they were) you can now delete `original` folder, since all information is stored in the new files. 


## HOW TO RUN
In the `dave.py` there are individual lines loading and parsing individual `_nn.csv` file. Hence you can run the analysis of selected files by:

```
>> cd src
>> python dave.py
```
## WHAT DAVE DOES
MAIN
1. deleting traces of 0 length in x,y [auto]
2. deleting traces outside of arena [auto]
3. smoothening traces with jumps there and back (when a trace jumps (long range in few steps) somewhere and in a short frame range it gets to a point close to the start)
4. tracking of swapped traces [auto, whitelist, or user guided version]
5. deleting traces with an overlap over enough traces (according to population_size) [auto]
6. merging traces with a gap [auto]
7. merging traces with an overlap 
    1. pairs of overlapping traces [auto until no trace with single overlap found]
    2. triplets of overlapping traces [auto (shortest of triplet skipped) or user guided]
8. saving the result as csv and pickle file - in `output` folder
9. annotating a given video with the result - in `output/video` folder
10. storing config and result as csv for each new result - in `output/result.csv`
11. visualisations
    1. plot of traces as lines showing their frame range
    2. position of traces in 3 plots: x-axis in time, y-axis in time, and x/y phase space (no time)
    3. overlaps and gaps of traces
    4. histogram of time to reappear another trace (showing lenght of gaps)
9. comparison of traces (under construction)
