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
1. **Python's Multiprocessing interface**: Distributed computing tasks across multiple CPU cores.
2. **OpenMP**: Enhanced parallelism within individual tasks.
3. **Filesystem operations**: Efficient data management for large volumes of data.

## World Bank Dataset
We decided to take it as simple as we can get and decided to calculate total population count for each specific year for all countries so we can get started and figure out basic implementations.

We decided to take two variations for this taking the concepts that was taught in class and check which one is better for our implementation:
1. Object of Arrays (Serial and Parallel)
2. Array of Objects (Serial and Parallel)

>These were the first two approaches we decided (in first discussion) trying to implement the basic code (making it easily approachable) to get our code rolling. 

### Python
**File Structure for world-bank dataset:**
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

2 Threads: Execution Time: `0.0077781677` seconds
3 Threads: Execution Time: `0.0076081753` seconds
4 Threads: Execution Time: `0.0070760250` seconds
5 Threads: Execution Time: `0.0072669983` seconds
6 Threads: Execution Time: `0.0069668293` seconds
7 Threads: Execution Time: `0.0056529045` seconds
8 Threads: Execution Time: `0.0065350533` seconds
9 Threads: Execution Time: `0.0077199936` seconds
10 Threads: Execution Time: `0.0084431171` seconds

**Observation for 5:** There seems to be a performance improvement until 8 Threads and seem to decrease after 9 threads due to overhead.


**Execution 6:** Threading Object of Arrays (expecting better results due to serial performance)
File path: `src/python/world-bank/P_threading_OoA.py`

2 Threads: Execution Time: `0.0066339970` seconds
3 Threads: Execution Time: `0.0064759254` seconds
4 Threads: Execution Time: `0.0062949657` seconds
5 Threads: Execution Time: `0.0057489872` seconds
6 Threads: Execution Time: `0.0053729217` seconds
7 Threads: Execution Time: `0.0057210922` seconds
8 Threads: Execution Time: `0.0059280396` seconds
9 Threads: Execution Time: `0.0070710182` seconds
10 Threads: Execution Time: `0.0079627037` seconds

**Observation for 6:** There seems to be a performance improvement until 6 Threads and seem to decrease from 7th thread due to overhead.

**Execution 7:** Threading for Numpy and Pandas Version
File path: `src/python/world-bank/P_numpy_pandas_version.py`

2 Threads: Execution Time: `0.0034129620` seconds
3 Threads: Execution Time: `0.0031547546` seconds
4 Threads: Execution Time: `0.0029499531` seconds
5 Threads: Execution Time: `0.0029289722` seconds
6 Threads: Execution Time: `0.0029170513` seconds
7 Threads: Execution Time: `0.0031442642` seconds
8 Threads: Execution Time: `0.0059280396` seconds
9 Threads: Execution Time: `0.0034310818` seconds
10 Threads: Execution Time: `0.0034186840` seconds

**Observation for 7:** There seems to be a performance improvement until 6 Threads and seem to decrease from 7th thread due to overhead as well.  This is the most performance we could get for this particular query and dataset.

**Best Execution Time for World Population Dataset: `0.0029170513` seconds -> Numpy and Pandas Threading (6 Threads) version.**


### C++

**Execution 1:** Serial Implementation
Serial : 0.0211242 Seconds
```
soumith@Soumiths-MacBook-Pro airnow % tree
.
├── airnow-parallel.cpp
├── airnow-parallel.o
├── airnow-serial.cpp
└── airnow-serial.o
```

**Execution 2:** Parallel Implementation

2 Threads: Execution Time: `0.0297182` seconds  
3 Threads: Execution Time: `0.018239` seconds  
4 Threads: Execution Time: `0.020087` seconds  
5 Threads: Execution Time: `0.015717` seconds  
6 Threads: Execution Time: `0.0151269` seconds  
7 Threads: Execution Time: `0.014868` seconds  
8 Threads: Execution Time: `0.0136459` seconds  
9 Threads: Execution Time: `0.019254` seconds  
10 Threads: Execution Time: `0.0133171` seconds

## Airnow Dataset
**Query of Execution:** Most Problematic Pollutant
### Python
**File Structure of Airnow Dataset:**
```
veera@Veeras-MacBook-Pro airnow % tree
.
├── P_numpy_pandas_version.py
├── S_AoO.py
├── S_OoA.py
└── S_and_P_threading.py
```

**Execution 1:** Array of Objects
File Path: `src/python/airnow/S_AoO.py`
Execution Time: 2.5033950805

**Execution 2:** Object of Arrays
File Path: `src/python/airnow/S_OoA.py`
Execution Time: 2.7894973754

**Execution 3:** Threading
File Path: `src/python/airnow/S_and_P_threading.py`

1 Thread(Serial) Execution Time: `2.3807098865` seconds
2 Threads: Execution Time: `1.2833068370` seconds
3 Threads: Execution Time: `1.3552389145` seconds
4 Threads: Execution Time: `1.3770728111` seconds
5 Threads: Execution Time: `1.4129259586` seconds
6 Threads: Execution Time: `1.3867528439` seconds
7 Threads: Execution Time: `1.3953461647` seconds
8 Threads: Execution Time: `1.4017021656` seconds
9 Threads: Execution Time: `1.4006757736` seconds
10 Threads: Execution Time: `1.3939142227` seconds

**Execution 4:** Pandas Threading
File Path: `src/python/airnow/P_numpy_pandas_version.py`
Execution Time: 1.2171008586


## C++
```
soumith@Soumiths-MacBook-Pro airnow % tree
.
├── airnow-parallel.cpp
├── airnow-parallel.o
├── airnow-serial.cpp
└── airnow-serial.o
```

1 Thread(Serial) Execution Time: `2.49024` seconds  
2 Threads: Execution Time: `1.47089` seconds  
3 Threads: Execution Time: `1.08279` seconds  
4 Threads: Execution Time: `0.807371` seconds  
5 Threads: Execution Time: `0.682772` seconds  
6 Threads: Execution Time: `0.629989` seconds  
7 Threads: Execution Time: `0.619206` seconds  
8 Threads: Execution Time: `0.642305` seconds  
9 Threads: Execution Time: `0.631205` seconds  
10 Threads: Execution Time: `0.63124` seconds

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

2 Threads: Execution Time: `25.4702` seconds  
3 Threads: Execution Time: `25.2106` seconds  
4 Threads: Execution Time: `24.9493` seconds  
5 Threads: Execution Time: `24.6441` seconds  
6 Threads: Execution Time: `24.3913` seconds  
7 Threads: Execution Time: `24.3153` seconds  
8 Threads: Execution Time: `25.3398` seconds  
9 Threads: Execution Time: `25.5919` seconds  
10 Threads: Execution Time: `25.6738` seconds

**Observation for 5:** There seems to be a performance improvement until 7 Threads and seem to decrease from 8th thread.



**Execution 6:** Parallel Version - Threading - Numpy

2 Threads: Execution Time: `25.4702` seconds  
3 Threads: Execution Time: `25.2106` seconds  
4 Threads: Execution Time: `24.9493` seconds  
5 Threads: Execution Time: `24.6441` seconds  
6 Threads: Execution Time: `24.3913` seconds  
7 Threads: Execution Time: `24.3153` seconds  
8 Threads: Execution Time: `25.3398` seconds  
9 Threads: Execution Time: `25.5919` seconds  
10 Threads: Execution Time: `25.6738` seconds

**Observation for 6:** There seems to be a performance improvement until 7 Threads and seem to decrease from 8th thread.


**Execution 7:** Multiprocessing with Threading
File path: `src/python/NYC/P_multiprocessing_Version.py`

2 Threads: Execution Time: `18.2201` seconds  
3 Threads: Execution Time: `17.9460` seconds  
4 Threads: Execution Time: `17.9037` seconds  
5 Threads: Execution Time: `17.8980` seconds  
6 Threads: Execution Time: `17.9228` seconds  
7 Threads: Execution Time: `17.8109` seconds  
8 Threads: Execution Time: `17.7854` seconds  
9 Threads: Execution Time: `17.8714` seconds  
10 Threads: Execution Time: `18.4825` seconds

**Observation for 7:** There seems to be a performance improvement until 8 Threads and seem to decrease from 9th thread.

### C++
```
soumith@Soumiths-MacBook-Pro nyc % tree
.
├── nyc-parallel.cpp
├── nyc-parallel.o
├── nyc-serial.cpp
└── nyc-serial.o
```

1 Thread(Serial) Execution Time: `32.2553` seconds  
2 Threads: Execution Time: `37.9534` seconds  
3 Threads: Execution Time: `29.3402` seconds  
4 Threads: Execution Time: `24.2093` seconds  
5 Threads: Execution Time: `25.3933` seconds  
6 Threads: Execution Time: `27.1043` seconds  
7 Threads: Execution Time: `29.1833` seconds  
8 Threads: Execution Time: `29.8862` seconds  
9 Threads: Execution Time: `31.0063` seconds  
10 Threads: Execution Time: `30.2773` seconds






## Improvement after Presentation:
After fixing C++:
![[output.png]]

These are the fixes and Optimizations we performed:

**Inefficient Line Reading:** Using getline(file, line, ',')  for reading lines and string tokenization at commas significantly slowed down execution time, adding approximately 5-6 seconds.
**Buffered File Streams:** Switching from ifstream mode to buffered streams enhanced file read performance, contributing to overall speed improvements.
**String Cleanup Overhead:** The operation line.erase(remove(line.begin(), line.end(), '"'), line.end()), which removes quotation marks from strings, introduced an additional delay of around 3 seconds during single processing.
**Execution Time Reduction:** The overall execution time was reduced from over 12 seconds to 2.25 seconds for single-threaded processing, and from 6 seconds to 1.67 seconds for multi-threaded execution.
**String vs. Numeric Data in Memory:** Storing string data makes it slower than numeric data due to higher memory overhead, more complex operations, and reduced cache efficiency. Numeric data is fixed-size and faster to process, while strings are variable-length and require more resources.

### C++
1 Thread(Serial) Execution Time: `1.86819` seconds  
2 Threads: Execution Time: `0.892469` seconds  
3 Threads: Execution Time: `0.629788` seconds  
4 Threads: Execution Time: `0.55429` seconds  
5 Threads: Execution Time: `0.507181` seconds  
6 Threads: Execution Time: `0.570808` seconds  
7 Threads: Execution Time: `0.534204` seconds  
8 Threads: Execution Time: `0.590988` seconds  
9 Threads: Execution Time: `0.585817` seconds  
10 Threads: Execution Time: `0.586577` seconds

### Python
1 Thread(Serial) Execution Time: `2.247382` seconds  
2 Threads: Execution Time: `2.073159` seconds  
3 Threads: Execution Time: `1.964109` seconds  
4 Threads: Execution Time: `1.969028` seconds  
5 Threads: Execution Time: `1.960971` seconds  
6 Threads: Execution Time: `2.000520` seconds  
7 Threads: Execution Time: `1.934773` seconds  
8 Threads: Execution Time: `2.023425` seconds  
9 Threads: Execution Time: `1.974349` seconds  
10 Threads: Execution Time: `1.983548` seconds