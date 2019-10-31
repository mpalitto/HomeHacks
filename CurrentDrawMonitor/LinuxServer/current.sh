#!/bin/bash
pt=$(date +%H:%M) #previous minute
pd="" #$(date +%F) #previous date
max=0
avg=0
cnt=0
alarm="OFF"

#subscribe to mqtt channel and receive reading every sec.
mosquitto_sub -h broker.mqtt-dashboard.com -t CsoMAX60scalaEapt11-current | \
 while read line # process data one minute at the time
 do 
  current=$(echo $line | sed 's/\[max\]//;s/[^0-9].*//')
  t=$(date +%H:%M) # this minute
  s=$(date +%S)
  if [ $current -gt 300 ]; then
    if ! [ "$(date +%F)" = "$pd" ]; then
      pd=$(date +%F)
      echo "DATE: $pd" >> /root/critical-current.log
    fi
    echo "$t:$s $current" >> /root/critical-current.log
  fi
  echo $s $current
  if [ $t = $pt ]; then #we are in the current minute
    #if [ $current -gt $max ]; then max=$current; fi
    let cnt++
    let avg+=current
  else #we are at the NEXT time, thus publish the current value and start over
    echo

    d="$(date +%a)$(date +%d)"
    H="$(date +%-H)"
    M="$(date +%-M)"
    let min=$H*60+$M
    let avg/=cnt
    echo $min $t $avg
    if [ $avg -gt 200 ] && [ $alarm = "OFF" ]; then
        alarm="ON"
        echo "ALARM: ON" >> /root/critical-current.log
        ssh -p 19999 root@localhost 'screen -S arduino433tx -X stuff "s:5EAAC1"'
    elif [ $avg -le 200 ] && [ $alarm = "ON" ]; then
        alarm="OFF"
        echo "ALARM: OFF" >> /root/critical-current.log
        ssh -p 19999 root@localhost 'screen -S arduino433tx -X stuff "s:5EAAC1"'
    fi
    curl -k "https://script.google.com/macros/s/AKfycbwfz3NysGRmLx-HSDen-GHBFwV1_wdcU0tDYsdOs6MMsjSMv-bz/exec?MIN=$min&TIMESTAMP=$t&$d=$avg"
    echo "MIN=$min TIMESTAMP=$t $d=$avg"
    pt=$t 
    max=0
    avg=0
    cnt=0
  fi
done
