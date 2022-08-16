read -p "sleep -> " N
while [ $((i+=1)) -le $N ]; do
    sleep 1
    now="0000$(($N-$i))"
    printf "\r"${now: -4}
done

sh ../../secret/s_AtCoder/login.sh

problem_name=ahc013_a
base_url=${problem_name%_*}
url=https://atcoder.jp/contests/${base_url}/tasks/${problem_name}

#oj s --wait=0 $url "${problem_name}.py"
#oj s --wait=0 $url "${problem_name}.py" -l 4047 #PyPy3
#oj s --wait=0 --yes $url "${problem_name}.py"
#
oj s --wait=0 --yes $url "${problem_name}.py" -l 4047 #PyPy3
