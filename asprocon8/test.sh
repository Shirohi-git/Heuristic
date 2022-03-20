function TEST(){
    num=$1
    ./asprocon8_a.py < in/input${num}.txt > out/output${num}.txt
    ./output_checker in/input${num}.txt out/output${num}.txt >> score.txt
}

g++ --std=c++17 -o output_checker output_checker.cpp
read -p "num or all? -> " res
: > score.txt

if [ "$res" = "all" ]; then
    for idx in {0001..0050};
    do 
        num="0000${idx}"
        TEST ${num: -4}
        echo "^"${num: -4} >> score.txt
        echo "^"${num: -4}
    done
    python3 sumcalc.py
else
    TEST ${res}
    open -a 'Google Chrome' "visualizer/build/index.html"
fi

