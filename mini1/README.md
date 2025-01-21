# CMPE 275: Mini 1 Project  Report
### Team Members:
1. Soumith Reddy Podduturi (016706612)
2. Veera Vivek Telagani (017503915) 
## Introduction

We developed an efficient distributed computing solution to process and analyze three distinct datasets simultaneously: 
1. **World Bank data**: Total population count 
2. **AirNow data**: Air quality analysis 
3. **NYC Crime data**: Repeated offender calculation 

Key Technologies Our implementation leveraged several key technologies: 
1. **Python's Multiprocessing interface**: Distributed computing tasks across multiple CPU cores 
2. **OpenMP**: Enhanced parallelism within individual tasks 
3. **Filesystem operations**: Efficient data management for large volumes of data

## World Bank Dataset
We decided to take it as simple as we can get and decided to calculate total population count for each specific year for all countries so we can get started and figure out basic implementations.

We decided to take two variations for this taking the concepts that was taught in class and check which one is better for our implementation:
1. Object of Arrays (Serial and Parallel)
2. Array of Objects (Serial and Parallel)

>These were the first two approaches we decided (in first discussion) trying to implement the basic code (making it easily approachable) to get our code rolling. 

### Python

File Structure for world-bank dataset:
```
veera@Veeras-MacBook-Pro world-bank % tree
.
├── Failed_Versions
│   ├── S_OoA_numba.py
│   └── tempCodeRunnerFile.py
├── P_numpy_pandas_version.py
├── P_threading_AoO.py
├── P_threading_OoA.py
├── S_AoO.py
├── S_OoA.py
├── S_numpy_pandas_version.py
├── __pycache__
│   └── numpy.cpython-312.pyc
├── tempCodeRunnerFile.py
├── test.py
└── worldbank-base.ipynb
```

**Execution 1:** Serial Implementation of Array of Objects
File path: `src/python/world-bank/S_AoO.py`
Execution time: `0.0111370087` seconds

**Execution 2:** Serial Implementation of Object of Arrays
File path: `src/python/world-bank/S_OoA.py`
Execution time: `0.0062079430` seconds

**Observation for 1 & 2:** There seem to be a `79.3%` *increase* in performance when comparing both data structures. This was expected, as discussed in class due to:
1. Faster in accessing elements
2. Memory efficiency
(We were still aware that Array of Objects has their own advantage in cases of preserving order, insertion or deletion from certain objects. It is a tradeoff between performance and data Flexibility(or Usability))

**Execution 3:** Numba Package

What is this? :
>Numba's @njit decorator compiles Python functions to optimized machine code using LLVM, enabling near-C speed for numerical operations. It's particularly useful for accelerating computationally intensive tasks involving numerical arrays and loops, often providing significant performance improvements with minimal code changes.

File path: `src/python/world-bank/Failed_Versions/S_OoA_numba.py`
Execution time: `0.3784062862` seconds
Result: `98.36%` *decrease* in performance comparing with Object of Arrays versions. So we decided that this is not working as expected and decided to scrap it.


**Execution 4:** Numpy and Pandas version
File Path: `src/python/world-bank/S_numpy_pandas_version.py`
Execution time: `0.0047119087` seconds
Result: There seems to be `24.10%` *increase* in performance over Object of Arrays version. - We found that Numpy and Pandas seem to have performance increase in simple queries so decided we will explore in parallel version of this as well.

**Execution 5:** Threading Array of Objects (we just wanted to know how much would it change compared to serial version even though Object of Arrays version is faster)
File path: `src/python/world-bank/P_threading_AoO.py`

*Execution 5-1:*  2 Threads
Execution Time: `0.0077781677` seconds

*Execution 5-2:* 3 Threads
Execution Time: `0.0076081753` seconds

*Execution 5-3:* 4 Threads
Execution Time: `0.0070760250` seconds

*Execution 5-4:* 5 Threads
Execution Time: `0.0072669983` seconds

*Execution 5-5:* 6 Threads
Execution Time: `0.0069668293` seconds

*Execution 5-6:* 7 Threads
Execution Time: `0.0056529045` seconds

*Execution 5-7:* 8 Threads
Execution Time: `0.0065350533` seconds

*Execution 5-8:* 9 Threads
Execution Time: `0.0077199936` seconds

*Execution 5-9:* 10 Threads
Execution Time: `0.0084431171` seconds

**Observation for 5:** There seems to be a performance improvement until 8 Threads and seem to decrease after 9 threads due to overhead.


**Execution 6:** Threading Object of Arrays (expecting better results due to serial performance)
File path: `src/python/world-bank/P_threading_OoA.py`

*Execution 6-1:*  2 Threads
Execution Time: `0.0066339970` seconds

*Execution 6-2:* 3 Threads
Execution Time: `0.0064759254` seconds

*Execution 6-3:* 4 Threads
Execution Time: `0.0062949657` seconds

*Execution 6-4:* 5 Threads
Execution Time: `0.0057489872` seconds

*Execution 6-5:* 6 Threads
Execution Time: `0.0053729217` seconds

*Execution 6-6:* 7 Threads
Execution Time: `0.0057210922` seconds

*Execution 6-7:* 8 Threads
Execution Time: `0.0059280396` seconds

*Execution 6-8:* 9 Threads
Execution Time: `0.0070710182` seconds

*Execution 6-9:* 10 Threads
Execution Time: `0.0079627037` seconds

**Observation for 6:** There seems to be a performance improvement until 6 Threads and seem to decrease from 7th thread due to overhead.

**Execution 7:** Threading for Numpy and Pandas Version
File path: `src/python/world-bank/P_numpy_pandas_version.py`

*Execution 7-1:*  2 Threads
Execution Time: `0.0034129620` seconds

*Execution 7-2:* 3 Threads
Execution Time: `0.0031547546` seconds

*Execution 7-3:* 4 Threads
Execution Time: `0.0029499531` seconds

*Execution 7-4:* 5 Threads
Execution Time: `0.0029289722` seconds

*Execution 7-5:* 6 Threads
Execution Time: `0.0029170513` seconds

*Execution 7-6:* 7 Threads
Execution Time: `0.0031442642` seconds

*Execution 7-7:* 8 Threads
Execution Time: `0.0059280396` seconds

*Execution 7-8:* 9 Threads
Execution Time: `0.0034310818` seconds

*Execution 7-9:* 10 Threads
Execution Time: `0.0034186840 seconds

**Observation for 7:** There seems to be a performance improvement until 6 Threads and seem to decrease from 7th thread due to overhead as well.  This is the most performance we could get for this particular query and dataset.


**Best Execution Time for World Population Dataset: `0.0029170513` seconds -> Numpy and Pandas Threading (6 Threads) version.**


### C++


## Airnow Dataset
**Query of Execution:**
### Python
**File Structure of Airnow Dataset:**
```
soumith@Soumiths-MacBook-Pro airnow % tree
.
├── P_numpy_pandas_version.py
├── S_AoO.py
├── S_OoA.py
└── S_and_P_threading.py
```

**Execution 1:** Array of Objects
File Path: `src/python/airnow/S_AoO.py`
Execution Time: 

**Execution 2:** Object of Arrays
File Path: `src/python/airnow/S_OoA.py`
Execution Time:

**Execution 3:** Threading
File Path: `src/python/airnow/S_and_P_threading.py`
Execution Time:

**Execution 4:** Pandas Threading
File Path: `src/python/airnow/P_numpy_pandas_version.py`
Execution Time: 

## NYC Dataset
**Query of Execution:** Number of Repeated offenders
### Python
**File Structure of NYC Dataset:**
```
veera@Veeras-MacBook-Pro NYC % tree
.
├── P_multiprocessing_Version.py
├── P_threading_Version.py
├── S_AoO.py
├── S_OoA.py
├── Serial_Version.py
├── color-analysis
│   └── serialcode.py
├── failedVersions
│   └── S_numba.py
└── tempCodeRunnerFile.py
```


**Execution 1:** Serial Version - Normal
File Path: `src/python/NYC/Serial_Version.py`
Execution Time: `48.3547` seconds -> Taking it as *Benchmark*

**Execution 2:** Serial Version - Array of Objects
File Path: `src/python/NYC/S_AoO.py`
Execution Time: `48.4283` seconds -> not a significant difference

**Execution 3:** Serial Version - Object of Arrays
File Path: `src/python/NYC/S_OoA.py`
Execution Time: `47.6643` seconds -> not a significant difference

**Execution 4:** Serial Version - Numba Version
File Path: `src/python/NYC/failedVersions/S_numba.py`
Execution Time: `59.7492` seconds -> *decrease* in performance

**Execution 5:** Parallel Version - Threading

*Execution 5-1:*  2 Threads
Execution Time: `25.4702` seconds

*Execution 5-2:* 3 Threads
Execution Time: `25.2106` seconds

*Execution 5-3:* 4 Threads
Execution Time: `24.9493` seconds

*Execution 5-4:* 5 Threads
Execution Time: `24.6441` seconds

*Execution 5-5:* 6 Threads
Execution Time: `24.3913` seconds

*Execution 5-6:* 7 Threads
Execution Time: `24.3153` seconds

*Execution 5-7:* 8 Threads
Execution Time: `25.3398` seconds

*Execution 5-8:* 9 Threads
Execution Time: `25.5919` seconds

*Execution 5-9:* 10 Threads
Execution Time: `25.6738` seconds


**Observation for 5:** There seems to be a performance improvement until 7 Threads and seem to decrease from 8th thread.

**Execution 6:** Multiprocessing with Threading
File path: `src/python/NYC/P_multiprocessing_Version.py`

*Execution 6-1:*  2 Threads
Execution Time: `18.2201` seconds

*Execution 6-2:* 3 Threads
Execution Time: `17.9460` seconds

*Execution 6-3:* 4 Threads
Execution Time: `17.9037` seconds

*Execution 6-4:* 5 Threads
Execution Time: `17.8980` seconds

*Execution 6-5:* 6 Threads
Execution Time: `17.9228` seconds

*Execution 6-6:* 7 Threads
Execution Time: `17.8109` seconds

*Execution 6-7:* 8 Threads
Execution Time: `17.7854` seconds

*Execution 6-8:* 9 Threads
Execution Time: `17.8714` seconds

*Execution 6-9:* 10 Threads
Execution Time: `18.4825` seconds

**Observation for 6:** There seems to be a performance improvement until 8 Threads and seem to decrease from 9th thread.

### C++





