#!/bin/sh
 tr -cs ",A-Za-z0-9-'/!" '[\n*]' | sort -u | comm -23 - sorted.words
