#!/bin/sh
nmap -sP -PE -PS22,25,80 -PA21,23,80,3389 -PU -PO --traceroute $1
