for f in *.p; do mv "$f" "$(echo "$f" | sed s/parsing/test/)"; done
