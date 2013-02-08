#!/bin/sh
nmap -sP -PE -PA21,23,80,3389 $1
