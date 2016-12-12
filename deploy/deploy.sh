#!/usr/bin/env bash
#Script for deploy services with travis, using the remote_commands_deploy.sh file
if [ "$TRAVIS_BRANCH" = "master" ]; then
    echo "Starting deploy."
    echo "Packing distribution package..."
    cd ..
    DIST="/tmp/wikidataviz.tar.gz"
    HOST="arachnid92@192.34.62.13"
    tar czfv "$DIST" --exclude='.idea' --exclude='venv' --exclude="__pycache__" --exclude='.git' --exclude='.gitignore' WikidataViz
    cd WikidataViz
    echo "Pushing to remote..."
    scp -o StrictHostKeyChecking=no "$DIST" "$HOST:$DIST"
    cat deploy/remote_commands_deploy.sh|ssh -o StrictHostKeyChecking=no "$HOST"
    echo "Done"
fi
