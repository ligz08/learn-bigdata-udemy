#!/usr/bin/env bash

cd /home/maria_dev/learn-bigdata-udemy
git pull origin master
export SPARK_MAJOR_VERSION=2
spark-submit spark2_lowestRatedMovies.py