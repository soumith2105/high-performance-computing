cmake_minimum_required(VERSION 3.3)

project (mini)

# compilers to use (9.2)
set(CMAKE_C_COMPILER /opt/homebrew/Cellar/llvm@16/16.0.6_1/bin/clang)
set(CMAKE_CXX_COMPILER  /opt/homebrew/Cellar/llvm@16/16.0.6_1/bin/clang++)

set(CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/Modules)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# openmp flags
#SET(OPENMP_CXX_FLAGS "-O3 -fopenmp --target=x86_64-pc-linux-gnu")
SET(OPENMP_CXX_FLAGS "-O3 -fopenmp")
SET(CMAKE_CXX_FLAGS  "${CMAKE_CXX_FLAGS} ${OPENMP_CXX_FLAGS}" )


# app targets


add_executable(airnow-parallel src/c++/airnow/airnow-parallel.cpp)
add_executable(airnow-serial src/c++/airnow/airnow-serial.cpp)

add_executable(nyc-parallel src/c++/nyc/nyc-parallel.cpp)
add_executable(nyc-serial src/c++/nyc/nyc-serial.cpp)

add_executable(worldbank-parallel src/c++/world-bank/worldbank-parallel.cpp)
add_executable(worldbank-serial src/c++/world-bank/worldbank-serial.cpp)

add_executable(airnow-detailed-parallel src/airnow-detailed/parallel.cpp)
add_executable(airnow-detailed-serial src/airnow-detailed/serial.cpp)
