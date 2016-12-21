#!/bin/bash

if hash python3 2>/dev/null; then
    ./halite -d "30 30" "python3 MyBot.py" "python3 OverkillBot.py" "node AliceBot.js" -t
else
    ./halite -d "30 30" "python OverkillBot.py" "python DiscerningBot.py" "python BorderBot.py" -t
fi

count=`ls -1 *.hlt 2>/dev/null | wc -l`
if [ $count != 0 ]; then
    mv *.hlt replays/
fi

count=`ls -1 *.log 2>/dev/null | wc -l`
if [ $count != 0 ]; then
    mv *.log logs/
fi
