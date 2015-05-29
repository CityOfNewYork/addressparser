#!/usr/bin/env bash

echo "Is the webserver is running?"
echo .

echo "Processing: ad-sample1.json"
echo curl -XPOST -H "Content-Type: application/json" --data-binary @ad-sample1.json http://localhost:5000/parseaddresses/
curl -XPOST -H "Content-Type: application/json" --data-binary @ad-sample1.json http://localhost:5000/parseaddresses/
echo .

echo "Processing: ad-sample2.json"
echo curl -XPOST -H "Content-Type: application/json" --data-binary @ad-sample2.json http://localhost:5000/parseaddresses/
curl -XPOST -H "Content-Type: application/json" --data-binary @ad-sample2.json http://localhost:5000/parseaddresses/
echo .

echo "Processing: ad-sample3.json"
echo curl -XPOST -H "Content-Type: application/json" --data-binary @ad-sample3.json http://localhost:5000/parseaddresses/
curl -XPOST -H "Content-Type: application/json" --data-binary @ad-sample3.json http://localhost:5000/parseaddresses/
echo .

echo "Processing: ad-sample4.json"
echo curl -XPOST -H "Content-Type: application/json" --data-binary @ad-sample4.json http://localhost:5000/parseaddresses/
curl -XPOST -H "Content-Type: application/json" --data-binary @ad-sample4.json http://localhost:5000/parseaddresses/
echo .
