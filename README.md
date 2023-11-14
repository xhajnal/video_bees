# Dave
Post-processing of faulty tracking from a 2D video (with batch mode).

Fixing video tracking of the bees made by [Loopy](http://loopbio.com/loopy/). 
Dave is designed to fix tracking from other sources, however, the parser needs to be adjusted to comply with your tracking format.

It provides an automatic solver based on given parameters and a user-guided process based on video snippets accompanied by GUI and prompt decisions.
Improved/completely solved tracking and annotated video are provided when the analysis is complete.

# Case study
1. Honeybee defence response. 352 bee videos of different group sizes. A group is put into an arena with a rotating dummy with a feather on one end which provokes the bees to sting. 

| population_size   | 1  | 3  | 5  | 7  | 10 | 15 |
| ----------------- | ---|----|----|--- |----|----|
| # videos          | 68 | 68 | 60 | 56 | 52 | 48 |

Skipping the runs that have multiple parts (3 occurrences), where probably the camera was not recording for a moment. 

## PREREQUISITES
1. Install [Python 3.9](https://www.python.org/downloads/)

## HOW TO INSTALL
As we use only Python, simply:
1. Download this repo.
2. (Optional) We recommend using a virtual environment (e.g. [conda](https://docs.conda.io/en/latest/), [pyenv](https://github.com/pyenv/pyenv)) before the following step.
3. Get non-standard libraries, which you can simply install with the command:

`>> pip install -r requirements.txt`

## DATA DOCUMENTATION
There are 2 main file types as a result of the [Loopy](http://loopbio.com/loopy/) analysis - a table in `.csv` format and tracked video. 

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
date               - global timestamp (YYYY-MM-DD"T"HH:MM:SS.Milliseconds+??:??) (we do not use this)
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
Second, there is a video file, preferably in `.mp4`, which Loopy uses to track the objects. 
Dave can use this original video to overlay the fixed tracking.
If you trimmed or cropped the video, a one-time user-guided process will save the cropping and trimming parameters of each file (see FIXING VIDEO TRIMMING AND CROPPING section).


## FOLDER STRUCTURE
Here we show the folder structure we have used, and this will be used during this README, hence we strongly recommend having it as similar as we do. 
![image](https://github.com/xhajnal/video_bees/assets/23458520/6480ce50-9f45-4977-952d-a366f7443982)



- In our analysis, we had video tracking in multiple folders enclosed in a single folder `Video_tracking` which is located in the `data` folder as shown in the picture. 
- The source code is located in `src` folder, you will be asked to edit some files according to your data.
- The `Output` folder will be used to output the final result of the analysis - tracking in the form of `csv` files and annotated videos,
- While `auxiliary` folder will be used to output partial results and decisions of the analysis.


## HOW AND WHERE TO STORE INPUT
Create a folder such as `data` in the repo. 
Get your tracking `*_nn.csv` and video `*.mp4` files, the results of Loopy analysis, into this folder with/without your folder structure. 

Now, edit `dave.py` (located in `src` folder) or use automatic dave generation `help_write_dave.py`.
`dave.py` contains lines for each file you would like to analyse.
In each line, function `analyse` calls the given file e.g.:

`analyse('../data/Video_tracking/190822/20190822_112842909_2BEE_generated_20210503_074806_nn.csv', population_size=2, has_tracked_video=True, is_first_run=a)`

where the first parameter is the path to the `.csv` file, the second is `population_size` (number of objects tracked in the video), flag has_tracked_video whether there is a video as a result of Loopy tracking and last flag, `is_first_run`, you do not need to set as this is a part of two-run setting (see more in TWO RUNS DAVE section).


### (OPTIONAL) FIXING FRAME RANGES
In our case studies, the videos were trimmed and hence the first frame of the video was not recognised by Loopy as the first. 
The script `fix_ranges.py` simply edits `frame_number` column to offset it so it starts with zero while keeping info of the original frame in column `frame_count`.
If you want to overcome this problem, move the `.csv` files in one folder deeper and name it `original` and edit the main of `fix_ranges.py` in a similar way as you edited `dave.py` e.g:

`fix_ranges('../data/Video_tracking/190822/20190822_112842909_2BEE_generated_20210503_074806_nn.csv')`

- using the call for each file to be fixed
- (ADVANCED) or use the recursive call to fix ranges of all the `_nn.csv` files. (line data_path = '../data/Video_tracking/') - this assumes the folder structure similar to ours.

If you use a different folder structure in comparison to the one we use (Figure in ## FOLDER STRUCTURE section) edit the `fix_ranges.py` accordingly.

Now run file `fix_ranges.py`
```
>> cd src
>> python fix_ranges.py
``` 
original files are moved to the folder `original` and the fixed are in the folder they have been before. 

## SETUP THE RUN
In the `analysis.py`, which dictates the sequence of the logic, visualisations, and I/O calls;
there are 10 flags, `batch_run`, `guided`, `silent`, `debug`, `show_plots`, `show_all_plots`, `allow_force_merge`, `rerun`, `save_parsed_as_pickle`, and `fast_run`.
These dictate global systematic settings such as the level of output, recalling a file with a known result as it was already run with the same setting and user-guided version. Documentation of individual flags is in the file.

In the `config.py` there are some fixed values which alter the boundaries and thresholds of the analysis. 
Documentation of individual value is in the file.
Changing these values may cause a different result of the analysis.
In principle, the most important values are at the top. 

## HOW TO RUN
In the `dave.py` there are individual lines loading and parsing individual `_nn.csv` file in the main function. Such as:

`
    analyse('../data/Video_tracking/190823/20190823_114450691_1BEE_generated_20210506_100518_nn.csv', 1)
    analyse('../data/Video_tracking/190823/20190823_153007029_1BEE_generated_20210507_091854_nn.csv', 1)
    analyse("../data/Video_tracking/190903/20190903_134034775_1BEE_generated_20210511_083234_nn.csv", 1)
` 

Hence you can run the analysis of these files by:

```
>> cd src
>> python dave.py
```

It will run the analysis for each of the files.

### (OPTIONAL, ADVANCED) HELP DAVE WRITER
There is also a script `help_write_dave.py` which can help you to write the whole `dave.py` by parsing the content of the `data` folder.
It requires to have population size in the name of the `.csv` file and to have name similarities with the video file. 

Simply edit and run `help_write_dave.py` to obtain the text to paste into `dave.py`.

### (OPTIONAL) TWO RUNS DAVE
In order to minimise the time the user needs to wait for the analysis of individual files, we created a 2-run version, where the first run executes only automatised decisions and creates a partial result file for each csv file. In the second run, user-guided analysis is done (setting flag guided as True). 

To run this version, please keep only the following line of the main of dave.py uncommented:

```
run_both()
```

In order to run the whole batch in a single run, please keep the following line:

```
run(is_first_run=True)

```

### (OPTIONAL) FIXING VIDEO TRIMMING AND CROPPING
In the case you do not use a video source which is a result of the Loopy and you either cropped or trimmed the video, for each of such files please select `has_tracked_video=False` or simply omit this parameter in the respective line in `dave.py`.

Simply put, the files with a video same as those used for the Loopy analysis the line for such files will look something like this:

```
analyse('../data/Video_tracking/{file_name}.csv', {population_size}, has_tracked_video=True, is_first_run=a)
```

and for the videos that have been either trimmed or cropped for the Loopy use this instead:

```
analyse('../data/Video_tracking/{file_name}.csv', {population_size},  is_first_run=a)
```

Now when run for the first time, a user-guided process as a part of `analyse.py` will trigger.

To set the cropping effect, for each video, a single frame video will be displayed showing the first frame any tracked object appears with points overlaying the video, press WASD keys to match the point(s) with the objects on the screen, when aligned pres `q` to continue. 

The trimming effect will be set automatically by parsing the `.csv` file.

`analyse.py` will save the cropping and trimming parameters of each video file in `transpositions.txt` in the `auxiliary` folder. 
After the parameters are saved for the video, these values will be automatically loaded when analysing the file. 

#### (ADVANCED)
if you wish to have both, the original and edited video, in the folder with the csv file, please add `movie_from_` to the file name of the original video, or edit this string in `dave_io.py` in `get_video_path(file_path)` function. Otherwise, Dave does not know which of the files to use for the analysis.

### USER-GUIDED PART
After the automatised part is finished and there are still unresolved traces (i.e. more traces than population size), a user-guided process to resolve problems one-by-one is initiated.
Here, a snippet of the video is being shown to you, where 2 traces are selected to be resolved - these two traces are highlighted with blue and orange colour respectively. 
Your task is to decide whether to merge these two traces (more info in the merging part). 

in the left upper corner, the current frame number is shown.

To work with the video, following keys can be used:
- `+`/`-` to speed up / slow down video respectively
- `a`/`d` to rewind / forward video respectively
- `r` to restart the snippet
- `q` to quit snippet

to open a table of the traces shown in the snippet, press `Ctrl+P`, 
Here you have an option to:
- Show only selected trace or to Show all traces (this reacts with the video overlay),
- Delete a trace (decision will be saved), 
- Hence there is also a button to undo this (Undelete trace). 

you can also see the frame range (starting and ending frame number) of each trace in the last column.

After the video is closed (press `q`), a question appears in the prompt on whether to merge the blue and orange trace.
- press `y` to merge and save the decision, 
- press `n` to not merge and save the decision, 
- press `d` to not merge and NOT save the decision (when you are not sure what to choose)

if you do not merge, you will be asked whether to delete any trace. 
Also, you have an option to see a larger proportion of the video, press `l` to see a larger portion or `f` to see the full video.

After this, the process continues by moving to another problematic trace pair until all problems are solved for the file.

Each user-guided decision is saved (in a pickled dictionary) and in the next run automatically used. 
Currently, to change the saved decision, the only way is to find the auxiliary file of the respective csv file and manually edit/delete the item.

### FULL-GUIDED 
After the analysis is done, if there are still more traces than there should be, a part in which all gaps and overlaps are being shown in a guided setup are shown at this point - full-guided.
In comparison with the guided version, here, there are no heuristics on which pair or triplet of traces to take, it simply starts at the start of the video and continues in a one-by-one fashion till the end of the video.

Like in the previous guided decision, all the decisions made here are being stored and reused later if rerun.


## WHAT DAVE DOES
1. deleting traces of 0 lengths in x,y  [auto]
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
10. annotating the video with the result tracking overlayed - in `output/video` folder
11. storing the final result as csv for each new result - in `output/result.csv`
12. visualisations
    1. plot of traces as lines showing their frame range
    2. position of traces in 3 plots: x-axis in time, y-axis in time, and x/y phase space (no time)
    3. overlaps and gaps of traces
    4. histogram of time to reappear another trace (showing length of gaps)
13. comparison of traces (under construction)

### DAVE's AUXILARY FUNCTIONS
1. Config file to save analysis parameters in one place
2. Automatically generate 'dave.py' from the content of the 'data' folder, adding each '.csv' to be analysed.
3. Saving trimming and cropping factors for alternative video used for Loopy (if applies)
4. Saving partial results of the 'first_run' as a pickled file with a respective hash based on the config settings
