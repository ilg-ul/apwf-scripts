#! /bin/sh

#export LANG="en_US.UTF-8"
#export LC_COLLATE="en_US.UTF-8"
#export LC_ALL="en_US.UTF-8"
#export LC_CTYPE=UTF-8


cd "$(dirname "$0")"/../src

python -m ilg.apwf.dumpMetadata
