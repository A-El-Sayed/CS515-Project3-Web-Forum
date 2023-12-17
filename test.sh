#!/bin/sh

set -e # exit immediately if newman complains
trap 'kill $PID' EXIT # kill the server on exit

./run.sh &
PID=$! # record the PID

newman run forum_multiple_posts.postman_collection.json -e env.json # use the env file
newman run forum_post_read_delete.postman_collection.json -n 50 # 50 iterations
newman run CS515-Test1-Replies.postman_collection.json
newman run CS515-Test2-Threads.postman_collection.json
newman run CS515-Test3-FullTextSearch.postman_collection.json
newman run CS515-Test4-DateTimeSearch.postman_collection.json