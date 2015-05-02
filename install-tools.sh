#! /bin/bash

if ! which fluidsynth
then
    echo Need to install fluidsynth
    sudo apt-get install fluidsynth fluid-soundfont-gm
fi
