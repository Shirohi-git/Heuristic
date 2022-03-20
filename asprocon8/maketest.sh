g++ --std=c++17 -o testcase_generator testcase_generator.cpp
mkdir -p in
cd in
../testcase_generator < ../parameters_50.txt
