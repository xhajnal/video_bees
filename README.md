# Dave
Post-processing of faulty tracking from a 2D video.

Fixing video tracking of the bees made by [loopy](http://loopbio.com/loopy/). 
Dave is capable of fixing other sources, however, the parser needs to be adjusted to comply with your tracking format.

# Case study
1. Honeybee defence response. 352 bee videos of different group sizes. A group is put into an arena with a rotating dummy with a feather on one end which provokes the bees to sting. 

| population_size   | 1  | 3  | 5  | 7  | 10 | 15 |
| ----------------- | ---|----|----|--- |----|----|
| # videos          | 68 | 68 | 60 | 56 | 52 | 48 |

Skipping the runs which have multiple parts (3 occurrences), where probably the camera was not recording for a moment. 

## PREREQUISITES
1. install [Python 3.9](https://www.python.org/downloads/)

## HOW TO INSTALL
1. As we use only Python.  
2. (Optional) We recommend using a virtual environment (e.g. [conda](https://docs.conda.io/en/latest/), [pyenv](https://github.com/pyenv/pyenv)) before the following step
3. get non-standard libraries, which you can simply install with the command:

`>> pip install -r requirements`

## DATA DOCUMENTATION
There are 2 main file types as a result of the [loopy](http://loopbio.com/loopy/) analysis - a table in `.csv` format and tracked video. 

### CSV FILE
`.csv` file which tracks the position of the individual agent in each tracked frame line by line.
There are two files:

```
\<name\>\_ai.csv
\<name\>\_nn.csv
```

In this analysis, we use only `_nn.csv` files.
These files are tables with the following column names:

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

### VIDEO FILE
Second, there is a video, preferably in `.mp4`, which produces an overlay of your original video with the tracking. 
In the case you did not save the video, Dave is capable of annotating the original video as well.
If you trimmed or cropped the video, a one-time user-guided process will save the cropping and trimming parameters of each file (see FIXING VIDEO TRIMMING AND CROPPING section).


## HOW AND WHERE TO STORE INPUT
Select a folder such as `data`. 
Get your `*_nn.csv` and `*.mp4` files, the results of loopy analysis, into this folder with/without your folder structure. 

Now, edit `dave.py` (located in `src` folder) that the files you would like to analyse are in the main class and function `analyse` calls the given file with `population_size` (Or simply edit the paths and population sizes of already given calls in the file.) e.g.:

`analyse('../data/Video_tracking/190822/20190822_112842909_2BEE_generated_20210503_074806_nn.csv', 2, has_tracked_video=True)`

where the first argument is the relative path to the file, 2nd is the population size, and the third is flag whether there is the tracked video of loopy.

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

## SETUP THE RUN
In the `analysis.py`, which dictates the sequence of the logic, visualisations, and I/O calls;
there are 6 flags, `batch_run`, `silent`, `debug`, `show_plots`, `guided`, and `rerun`.
These dictate global systematic settings such as the level of output, recalling a file with a known result as it was already run with the same setting, and user-guided version. Documentation of individual flag is in the file.


In the `config.py` there are some fixed values which alter the boundaries and thresholds of the analysis. 
Documentation of individual value is in the file.
Changing these values may cause a different result of the analysis.
In principe, the most important values are at the top. 

## HOW TO RUN
In the `dave.py` there are individual lines loading and parsing individual `_nn.csv` file in the main function. Such as:

`
    analyse('../data/Video_tracking/190823/20190823_114450691_1BEE_generated_20210506_100518_nn.csv', 1)
    analyse('../data/Video_tracking/190823/20190823_153007029_1BEE_generated_20210507_091854_nn.csv', 1)
    analyse("../data/Video_tracking/190903/20190903_134034775_1BEE_generated_20210511_083234_nn.csv", 1)
` 

Hence you can run the analysis of selected files by:

```
>> cd src
>> python dave.py
```

It will run the analysis for each of the selected files.

### (OPTIONAL, ADVANCED) HELP DAVE WRITER
There is also a script `help_write_dave.py` which can help you to write the whole `dave.py` by parsing the content of the `data` folder.
It requires to have population size in the name of the csv file and to have name similarities with the video file. 

Simply edit and run `help_write_dave.py` to obtain the text to paste into `dave.py`.

### (OPTIONAL) FIXING VIDEO TRIMMING AND CROPPING
In the case you do not use video source which is result of the loopy and you either cropped or trimmed the video, please select `has_tracked_video=False` or omit these parameters in the `dave.py`. Now, a one-time user-guided process in `analyse.py` will save the cropping and trimming parameters of each file in `transpositions.txt` in `auxiliary` folder. In the second run, these values will be automatically loaded. 

Hence, consider commenting the whole analysis in order to guide this process in the first run and running the actual analysis on the second run.

In this process, to set cropping effect, for each video a single frame video will be displayed, this is use the first frame, press WASD keys to match the point to the objects on the screen, then pres `q` to continue. 

The trimming effect will be set automatically by parsing the `.csv` file.

the parameters are automatically saved. 

## WHAT DAVE DOES
1. deleting traces of 0 lengths in x,y [auto]
2. deleting traces outside of the arena [auto]
3. smoothening traces with jumps there and back (when a trace jumps (long range in few steps) somewhere and in a short frame range it gets to a point close to the start)
4. tracking of swapped traces [auto, whitelist, or user-guided version]
5. deleting traces with an overlap over enough traces (according to population_size) [auto]
6. merging traces with a gap [auto]
7. merging traces with an overlap 
    1. pairs of overlapping traces [auto until no trace with single overlap found]
    2. triplets of overlapping traces [auto (shortest of triplet skipped) or user-guided]
8. Gap/overlap by gap/overlap resolution [only user-guided]
9. saving the result as csv and pickle file - in `output` folder
10. annotating a given video with the result - in `output/video` folder
    1. overlay loopy result video
    2. overlay of original video, crop and trimming factors recognised via user-guided process
11. storing config and result as csv for each new result - in `output/result.csv`
12. visualisations
    1. plot of traces as lines showing their frame range
    2. position of traces in 3 plots: x-axis in time, y-axis in time, and x/y phase space (no time)
    3. overlaps and gaps of traces
    4. histogram of time to reappear another trace (showing length of gaps)
13. comparison of traces (under construction)
