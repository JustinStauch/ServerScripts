#!/bin/bash

mediainfo "$1" | grep -m 1 "Tagged date" | awk '{print $5}'
