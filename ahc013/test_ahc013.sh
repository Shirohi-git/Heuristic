function TEST(){
    num=$1
    ./ahc013_a.py < in/${num}.txt > out/${num}out.txt
    cargo run --release --bin vis in/${num}.txt out/${num}out.txt >> score.txt
    mv -f vis.html vis/vis${num}.html
    echo "^"${num} >> score.txt
    echo "^"${num}
}

read -p "num or all? -> " res

if [ "$res" = "all" ]; then
    : > score.txt
    for idx in {0000..0099};
    do 
        num="0000${idx}"
        TEST ${num: -4}
    done
    ./calc_sum.py < score.txt >> score.txt
else
    ./ahc013_a.py < in/${res}.txt > out/${res}out.txt
    cargo run --release --bin vis in/${res}.txt out/${res}out.txt
    #open -a 'Google Chrome' vis.html
fi
