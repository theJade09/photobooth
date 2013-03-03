#!/bin/bash

log_dir='logs'

if [ -d $log_dir ];
then 
    rm -f $log_dir/*
else
    mkdir $log_dir
fi


python directory_watcher.py &> $log_dir/directory_watcher.log &
python main.py > $log_dir/main.log 2>&1 &
