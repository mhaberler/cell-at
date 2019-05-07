#!/bin/sh
./senderkataster.py
git add -A
git commit -m "$(date +%F)"
