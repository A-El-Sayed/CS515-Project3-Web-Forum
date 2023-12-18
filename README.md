# CS515 - Project3 - Web Forum
- Ali El Sayed aelsaye1@stevens.edu
- URL to github repo: https://github.com/A-El-Sayed/CS515-Project3-Web-Forum
- Estimate on how many hours i spent on this project: 6 hours
- i tested my code using postman as well as using breakpoints for each step for each endpoint
- i have no bugs or issues in my code. However, I cant seem to fix the issue in the datetime search where the i miss milliseconds when i input the date time range.
- In order to 'fix' this issue that i have with the datetime search, I ended up saving the posts when i post without the milliseconds, which fixes the issue for datetime search but causes an assertian failure in the baseline behavior.
- I was only able to do 4 extensions:
1. Replies (threaded replies)
2. Thread-based range queries
3. FullText Search
4. Date- and time-based range queries
## Extensions + tests
### Replies
- The way replies (threaded replies) work is by sending a body to this endpoint:
  ```
  127.0.0.1:5000/post
  ```
  - the body contains the ```msg``` and ```reply_to```, as such:
    ```
    {
      "msg": "This is a reply to post #1",
      "reply_to": 1
    }
    ```
    with "msg" being the content that is being posted and "reply_to" is where you decide what the message is replying to.

- For Testing:
  - I ended up creating a case where i first posted without the "reply_to", and in order to check whether it works, i created a request that gets the post as well as its information. After doing so, i created another request called "post a reply to post", which posts a reply to the inital post using the "reply_to" where you input the id of the inital post that is being replied to. It should return 200 for successfull cases and 400 for cases where "msg" is not in the json body.

### Thread-Based range queries
- The way replies (threaded replies) work is by sending a body to this endpoint:
  ```
  127.0.0.1:5000/post/thread/<int:post_id>
  ```
We then get the a thread-list of post of "post_id" as well as all the threaded replies to it.

- For Testing:
  - I started up by creating a case where i first posted a post and in order to check whether it works, i created a request that gets the post as well as its information. After doing so, i created another request called "post a reply to post", which posts a reply to the inital post using the "reply_to" where you input the id of the inital post that is being replied to. i made another request that posts a second reply to the inital post, and I also posted a third post that is unrelated to the first three threaded posts. After doing so, i created a request called "post a reply to post 4" which posts a reply to the unrelated-unthreaded post, which now means that we have 5 posts. Lastly, i made get post requests to make sure it all worked fine, and then used the ```127.0.0.1:5000/post/thread/1``` endpoint to get all the threaded replies range for post #1. this endpoint should return post #1,#2, and #3. However, ```127.0.0.1:5000/post/thread/2``` returns post #2 and #3. Lastly, ```127.0.0.1:5000/post/thread/4``` endpoint request should only return post #4 and post #5. All of this should return 200 for successfull cases and [] if there is no post with the selected "post_id" in ```127.0.0.1:5000/post/thread/<int:post_id>```

### FullText Search
- The way FullText Search works is by sending a body to this endpoint:
  ```
  127.0.0.1:5000/post/fulltext_search?query=<value>
  ```
We then get a list of posts that with messages/content that contains a "query" params with the value "<value>". For example if we want to find posts that contain the word "earth", our request would be ```127.0.0.1:5000/post/fulltext_search?query=earth```

- For Testing:
  - I first created a post that contained the word "earth", and then i also created a reply to that post that also contained the word "earth". After doing so, i posted a post that did not have the word "earth" but had the word "Boston" with B being uppercase. I finally did three seperate requests, each being ```127.0.0.1:5000/post/fulltext_search?query=earth```, which returns the first post as well as its reply that contained the word "earth", ```127.0.0.1:5000/post/fulltext_search?query=earth```, which returns the same list as ```127.0.0.1:5000/post/fulltext_search?query=earth``` since i made sure to test that the endpoint/query was not case-sensitive, and finally ```127.0.0.1:5000/post/fulltext_search?query=Boston```, which returns the post #3 that contained the word "Boston". These all return 200 and [] in case there is no post that contained a value inputted in the "query" params.
 
### DateTime Search
- The way FullText Search works is by sending a body to this endpoint:
  ```
  127.0.0.1:5000/date_time_range_search?start_datetime=<YYYY-MM-DDTHH:MM:SS>&end_datetime=<YYYY-MM-DDTHH:MM:SS>
  ```
We then get a list of posts that with messages/content that were posted within the range of "start_datetime" and "end_datetime".

- For Testing:
  - I first created a post. After doing so, I used the "date_time_range_search" with params "start_datetime" with a value of "2023-11-01T00:00:00" and an "end_datetime" with a value of "2023-12-31T01:38:28", as such ```127.0.0.1:5000/date_time_range_search?start_datetime=2023-11-01T00:00:00&end_datetime=2023-12-31T01:38:28``` and this will return all the posts that were posted within this range. I also ended up creating another endpoint that would mot return any post and only return an empty list, []. All this should return 200 status code if working properly, and 400 if the request is missing any of the required params "start_datetime" and "end_datetime".
