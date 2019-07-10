#!/bin/bash
# Usage: ./run.sh [jiki / bilibili] [10, int value]
function check() {
    count=`ps aux | grep $2 | wc -l`
    delta=`expr ${count} - $1`
    if [[ 0 == ${delta} ]]; then
        echo "Starting $2"
        nohup scrapy crawl $2 -L INFO &
    fi
}

current_count=`ps aux | grep $1 | wc -l`
sleep_time=4
if [[ $# == 0 ]]; then
    echo "Please specify which crawler to run: 'jiki', 'bilibili', or 'weibo'."
elif [[ $# == 1 ]]; then
    echo "Use default sleep duration: $sleep_time seconds."
elif [[ $# == 2 ]]; then
    sleep_time=$2
fi

while [[ 1 > 0 ]]; do
    check ${current_count} $1
    sleep ${sleep_time}
done
