#!/bin/bash
# Run "./run.sh help" to see usage (or read below).
# Note: sudo is used as otherwise permission will likely be denied (docker requires root by default).

CMD="sudo docker"
UP="${CMD} compose up"
BUILD="${UP} --build"
DOWN="${CMD} compose down"
PRUNE="${CMD} image prune"
LIST_P="${CMD} ps"
LIST_I="${CMD} image list"

if [ "$#" -eq 0 ]; then
    echo "$UP"
    $UP

elif [ "$1" == "build" ]; then
    echo "$BUILD"
    $BUILD
    echo "Removing old images..."
    $PRUNE

elif [ "$1" == "down" ]; then
    echo "$DOWN"
    $DOWN

elif [ "$1" == "list" ]; then
    echo "======= CONTAINERS ======="  
    echo ""
    $LIST_P
    echo ""
    echo "======= IMAGES ======="
    echo ""
    $LIST_I

elif [ "$1" == "help" ] || [ "$#" -gt 1 ]; then
    printf "\n%s\n" "Usage: ./run.sh <COMMAND>"
    printf "%s\n\n" "If no command is given, then 'sudo docker compose up' will be used."
    printf "%10s\n\n" "Commands:"
    
    col="  %-10s%s\n"
    printf "$col" "build" "This will rebuild the containers before starting them as well as prune old images."
    printf "${col}\n" "" "runs: 'sudo docker compose up --build' followed by 'sudo docker image prune'."
    
    printf "$col" "down" "This will stop and remove the containers."
    printf "${col}\n" "" "runs: 'sudo docker compose down'."
    
    printf "$col" "list" "This will list running containers and created images."
    printf "${col}\n" "" "runs: 'sudo docker ps' and 'sudo docker image list'."
fi

