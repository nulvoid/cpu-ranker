# cpu-ranker
A Linux-first customizable Python script that ranks your processors based on single core score, multi core score, L3 cache, and TDP.

WIP, still adjusting formula to my tastes.

## Requirements
There are only two requirements: Python 3.6+ and pandas.

Ensure you are running at least version 3.6 of Python with:

`python3 --version`

Install pandas using pip with:

`pip install pandas` 

or if you're like me (using some form of Debian and just want pandas installed):

`sudo apt install python3-pandas`

## Using the script
This script reads .CSV data from a "CPUs" folder located in the same directory as wherever you place rank.py. Each .CSV file should be named "CPU Name.csv", the script will use the filename as the name for each processor.

The required 5x2 .CSV layout is as follows:
| Column 1 | Column 2 |
| ------------- | ------------- |
| Single core average | Multi core average |
| L2 cache | L3 cache |
| Cores | Threads |
| TDP | Year of release |
| Distribution | Desktop environment |

L2 cache, year of release, distribution, and desktop environment are never used in the formula as provided, and are tracked for comparison purposes in the generated .CSV containing all final data. 

With your terminal set to whatever directory you have the script in, run it with:

`python3 rank.py`

The script will search for all .CSV files (excluding any set to be ignored) in the "CPUs" folder in the same directory as the script, extract their data, run its calculations, and generate a .CSV file titled "output.csv" in a folder called "Out" in the same directory as the script that contains all supplied data for all CPUs alongside their score, ranking from first to last by score. Any .CSV files not matching the required format will be skipped. All scores will be rounded to two decimal places before being added to the final .CSV table.

## Ratings
This script is provided under the MIT license to allow you to freely use and customize the rating system to your liking. Currently, the formula is:

`score = ((performance + cache_bonus) * efficiency) * scalar`

Performance is calculated from:

`(single_core * weight_single) + (multi_core * weight_multi)`

Cache bonus is calculated from:

`((l3_cache / cores) ** cache_scaling) * l3_bonus`

Efficiency is calculated from two separate operations:

`power_cost = ((tdp / cores) + (tdp / threads)) / 2`

`efficiency = performance / (performance + power_cost * tdp_penalty)`

Constants are defined as:

```
weight_single = 0.78 (defines the importance of single core performance)
weight_multi = 0.22 (defines the importance of multi core performance)
l3_bonus = 0.50 (adjusts the overall contribution of L3 cache for each CPU)
cache_scaling = 2.5 (defines how aggressive the L3 cache bonus curve is)
tdp_penalty = 200 (defines how harshly tdp affects a score)
scalar = 70 (used to produce more readable scores)
```
