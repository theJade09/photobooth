#/bin/sh


app_list=`ps -ef | egrep "[d]irectory_watcher|[m]ain\.py" | awk '{print $2}'`
for i in $app_list;
do
    kill -9 $i
done
