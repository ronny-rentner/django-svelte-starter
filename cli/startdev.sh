#!/bin/bash

PROJECT_DIR=`dirname $0`
PROJECT_DIR=`realpath $PROJECT_DIR/../`

# Path to your Python virtual environment
VENV_PATH="$PROJECT_DIR/backend/venv"

# Command to activate the virtual environment
ACTIVATE="source $VENV_PATH/bin/smartactivate"

#Potentially have to trap signal INT
#trap 'exec bash' INT;

read -r -d '' CMD <<EOC

  gnome-terminal --tab -- bash -ic "
    date; 
    set-title 'Svelte Frontend'; 
    ./dm run front; 
    history -s './dm run front' && exec bash
  ";

  gnome-terminal --tab -- bash -ic "
    $ACTIVATE; 
    date; 
    exec bash
  ";

  bash -ic "
    $ACTIVATE; 
    date;
    set-title 'Django Backend'; 
    ./dm run back;
    history -s './dm run back' && exec bash
  "
EOC

gnome-terminal --window --working-directory="$PROJECT_DIR" -- bash -ic "$CMD"

