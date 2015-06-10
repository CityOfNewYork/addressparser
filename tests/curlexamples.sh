#!/usr/bin/env bash

echo "Is the webserver is running?"
echo .

echo "Processing: ad-sample1.json"
echo curl -XPOST -H "Content-Type: application/json" -d @data/ad-sample1.json http://localhost:5000/api/parseaddresses
curl -XPOST -H "Content-Type: application/json" -d @data/ad-sample1.json http://localhost:5000/api/parseaddresses
echo .

echo "Processing: ad-sample2.json"
echo curl -XPOST -H "Content-Type: application/json" -d @data/ad-sample2.json http://localhost:5000/api/parseaddresses
curl -XPOST -H "Content-Type: application/json" -d @data/ad-sample2.json http://localhost:5000/api/parseaddresses
echo .

echo "Processing: ad-sample3.json"
echo curl -XPOST -H "Content-Type: application/json" -d @data/ad-sample3.json http://localhost:5000/api/parseaddresses
curl -XPOST -H "Content-Type: application/json" -d @data/ad-sample3.json http://localhost:5000/api/parseaddresses
echo .

echo "Processing: ad-sample4.json"
echo curl -XPOST -H "Content-Type: application/json" -d @data/ad-sample4.json http://localhost:5000/api/parseaddresses
curl -XPOST -H "Content-Type: application/json" -d @data/ad-sample4.json http://localhost:5000/api/parseaddresses
echo .
