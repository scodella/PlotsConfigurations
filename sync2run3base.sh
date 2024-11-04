#!/bin/sh -x
git checkout run3base
git fetch
#git pull
git checkout RPLME_ANALYSIS
git merge origin/run3base

