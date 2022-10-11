### Running server

```
docker build -t bloomreach_challenge .
docker run -d --name challenge_container -p 8000:80 bloomreach_challenge
```

### Request example

`http://127.0.0.1:8000/api/smart?timeout=500`

### Things I covered

- Server sends up to 3 HTTP requests to Exponea Testing HTTP Server
- Server returns the first sucessful response
- Server first send one request and if it doesn't receive answer in 300 ms then send another two requests
- The endpoint accepts a timeout parameter (I made it required)
- Simple tests
- Dockerfile


### Thoughts and things I would like to do better

- This is really naive solution - server creates 3 tasks to send request, but two of them are stopped for 300 ms, to give time for the first one to receive answer. Probably there should be way to do `asyncio.wait_for()` with timeout and make it continue task, instead of giving error.
- Tests are really simple, since it was challenging for me to write asynchronous test. They check just if endpoint works well and two error statuses. I would like to add more of them, e.g. checking if after 300 ms server really sends another two requests.
- I didn't have a lot to do with asynchronous code in Python before, but now I can imagine better why you use Go in some features. ;)