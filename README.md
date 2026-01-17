# v1.0.0 2026/1/16
A Linux-first customizable Python script that ranks your processors based on single core score, multi core score, L3 cache, and TDP.

My processor benchmarking tool of choice is cpubench1a 5.0, which can be found [here](https://github.com/AmadeusITGroup/cpubench1A). If you choose to use single and multi core scores from another benchmarking tool, you will need to adjust constants. An example output is provided for your convenience to reference to see how the formula calculates a score using the provided constants.

As implied, this script is not meant to be a definitive ranking of processors, it's merely a tool to compare processors according to a certain criteria. Scores should not be used to definitively say "X CPU is better than Y CPU" or "X CPU is 2x better than Y CPU", it is a subjective comparison that you can adjust to your liking. The scores are only a tool used to rank the processors.

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

The required 6x2 .CSV layout is as follows:
| Column 1 | Column 2 |
| ------------- | ------------- |
| Single core average | Multi core average |
| L2 cache (MB) | L3 cache (MB) |
| Cores | Threads |
| TDP (Watts) | Year of release |
| Distribution | Desktop environment |
| Kernel | Notes |

Year of release, distribution, desktop environment, kernel, and (obviously) notes are never used in the formula as provided, and are tracked for comparison purposes in the generated .CSV containing all final data. 

With your terminal set to whatever directory you have the script in, run it with:

`python3 rank.py`

The script will search for all .CSV files (excluding any set to be ignored) in the "CPUs" folder in the same directory as the script, extract their data, run its calculations, and generate a .CSV file titled "output.csv" in a folder called "Out" in the same directory as the script that contains all supplied data for all CPUs alongside their score, ranked from first to last by score. Any .CSV files not matching the required format will be skipped. All scores will be rounded to two decimal places before being added to the final .CSV table for readability.

## Scoring
This script is provided under the MIT license to allow you to freely use and customize the rating system to your liking. Currently, the formula is:

`score = ((performance + cache) * efficiency) * scalar`

Performance is calculated from:

`(single_core * weight_single) + (multi_core * weight_multi)`

Cache is calculated from three operations:

```
l2 = ((l2_cache / cores) ** l2_exponent) * l2_bonus * l2_scalar
l3 = ((l3_cache / cores) ** l3_exponent) * l3_bonus
cache = (l2 + l3) ** cache_scalar
```

Note: while the L3 cache bonus is exponential, it alone is not enough to overpower general CPU performance as shipped. As such, a 7800X3D for example will not dominate rankings purely based off of L3 cache.

Efficiency is calculated from two operations:

```
power_cost = ((tdp / cores) + (tdp / threads)) / 2

efficiency = performance / (performance + power_cost * tdp_penalty)
```

Constants are adjustable and defined as:

```
weight_single = 0.8 (defines the importance of single core performance)
weight_multi = 0.2 (defines the importance of multi core performance)
l2_bonus = 0.5 (adjusts the overall contribution of L2 cache for each CPU)
l2_exponent = 2.3 (defines how aggressive the L2 cache bonus curve is)
l2_scalar = 10 (scales the L2 cache bonus to provide a more or less meaningful bonus)
l3_bonus = 0.5 (adjusts the overall contribution of L3 cache for each CPU)
l3_exponent = 2.3 (defines how aggressive the L3 cache bonus curve is)
cache_scalar = 1.1 (defines how aggressive the overall cache bonus curve is)
tdp_penalty = 65 (defines how harshly TDP affects a score)
scalar = 70 (used to produce more readable scores only, and does not affect CPU rankings)
```
