#!/bin/bash

if hash python3 2>/dev/null; then
    ./halite -d "30 30" "python3 MyBot.py" "python3 DiscerningBot.py" "python3 ImprovedBot.py" -t -q
else
    ./halite -d "30 30" "python OverkillBot.py" "python DiscerningBot.py" "python BorderBot.py" -t
fi

if [ -e *.hlt ]; then mv *.hlt ./replays/; fi
