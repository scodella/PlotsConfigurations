#!/bin/sh -x
git checkout run2base
git fetch
#git pull
git checkout SUS23002
git merge origin/run2base

