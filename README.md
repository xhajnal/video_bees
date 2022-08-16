# Dave
Fixing video tracking of the bees made by [loopy](http://loopbio.com/loopy/). 

## PREREQUISITIES
install [Python 3.9](https://www.python.org/downloads/)

## HOW TO INSTALL
As we use only python, the only installation are non included libraries, which you can simply install with

`>> pip install -r requirements`


## DATA FILE TYPES AND CONVENTIONS
all data are located in `data` folder, while there are two types of files
```
\<name\>\_ai.csv
\<name\>\_nn.csv
```
as result of [loopy](http://loopbio.com/loopy/). In this analysis we use only `_nn.csv` files.

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

## HOW TO RUN
In the `dave.py` there are individual lines loading and parsing individual `_nn.csv` file. Hence you can run the analysis of selected files by:

```
>> cd src
>> python dave.py
```
