import twitter

api = twitter.Api(consumer_key='5t3DLzDcI8eCrMcGCHA94hhIG',
                  consumer_secret='zyzse9kfWQCJv0GnZHTFvnv3ESrOoaEFNtTNaSe8zj5B3RJZHT',
                  access_token_key='3427938612-dsed9lZaqnelYVF8x5Vv2AzSZ0f4j605tqXGgNK',
                  access_token_secret='hrEdjFSQiFlWdyUyHJ2fV9p8YKx6NKNY3ex8BIEfJtLaN')

location_lst = ["-118.2389, 34.0373", "-118.0225, 33.8838"]
with tweetstream.LocationStream(username="GeoClintonD", password="@Test123", locations=location_lst) as stream:
    for tweet in stream:
        print tweet
