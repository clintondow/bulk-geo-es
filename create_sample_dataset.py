<<<<<<< HEAD
import twitter

api = twitter.Api(consumer_key='5t3DLzDcI8eCrMcGCHA94hhIG',
                  consumer_secret='zyzse9kfWQCJv0GnZHTFvnv3ESrOoaEFNtTNaSe8zj5B3RJZHT',
                  access_token_key='3427938612-dsed9lZaqnelYVF8x5Vv2AzSZ0f4j605tqXGgNK',
                  access_token_secret='hrEdjFSQiFlWdyUyHJ2fV9p8YKx6NKNY3ex8BIEfJtLaN')

location_lst = ["-118.2389, 34.0373", "-118.0225, 33.8838"]
with tweetstream.LocationStream(username="GeoClintonD", password="@Test123", locations=location_lst) as stream:
    for tweet in stream:
        print tweet
=======
import tweepy
from tweepy.streaming import StreamListener
from tweepy import Stream
import json
import time
import arcpy

pos = 0

cons_tok = "5t3DLzDcI8eCrMcGCHA94hhIG"
cons_sec = "zyzse9kfWQCJv0GnZHTFvnv3ESrOoaEFNtTNaSe8zj5B3RJZHT"

app_tok = "3427938612-dsed9lZaqnelYVF8x5Vv2AzSZ0f4j605tqXGgNK"
app_sec = "hrEdjFSQiFlWdyUyHJ2fV9p8YKx6NKNY3ex8BIEfJtLaN"


#  TODO Work in progress, not yet suitable for usage without editing the keys/paths.
def jsons_to_feature_class(folder_path, tempdir, tempgdb, tempfc):
    import os
    gdb_path = tempdir + os.path.sep + tempgdb
    arcpy.env.overwriteOutput = True
    with arcpy.da.InsertCursor(os.path.join(gdb_path, tempfc), ['SHAPE@X', 'SHAPE@Y', 'MsgText']) as cursor:
        for file in os.listdir(folder_path):
            if os.path.splitext(file)[1] == r'.json':
                with open(folder_path + os.sep + file, 'rt') as txt:
                    try:
                        j = json.load(txt)
                        text = ''
                        if j['text']:
                            text = j['text']
                        if j['geo']:
                            x, y = j['geo']['coordinates']
                            print(x, y)
                            cursor.insertRow([y, x, text])  # Twitter's coords are backwards?
                            arcpy.AddMessage('Added row...')
                    except Exception:
                        pass
                os.remove(folder_path + os.sep + file)
            else:
                pass
    arcpy.AddMessage('JSON to FC Batch Completed')


class twitter_listener(StreamListener):
    def on_data(self, data):
        global pos
        j = json.loads(data)
        try:
            coords = j["coordinates"]
            if coords:
                with open(r"C:\Users\clin8331\Documents\tw_two\tw{}.json".format(pos), 'w') as f:
                    json.dump(j, f)
                pos += 1
        except KeyError:
            if j["limit"]:
                time.sleep(2)
                return True
        except:
            return False
        return True

    def on_error(self, status):
        if status == 420:  # Too many requests, sleep for a bit
            time.sleep(10)
            return True
        return False

    def on_exception(self, exception):
        print('---- {}'.format(exception))
        return False


if __name__ == "__main__":
    import os
    import tempfile
    tempdir = tempfile.gettempdir()
    tempgdb = 'scratch.gdb'
    tempfc = 'tw'
    gdb_path = tempdir + os.path.sep + tempgdb
    auth = tweepy.OAuthHandler(cons_tok, cons_sec)
    auth.set_access_token(app_tok, app_sec)
    twitter_api = tweepy.API(auth)
    instances = []
    fc = arcpy.CreateFeatureclass_management(gdb_path, tempfc, "POINT", spatial_reference=sr)
    arcpy.AddField_management(fc, 'MsgText', 'TEXT')
    while True:
        if len(instances) < 5:
            try:
                twitter_stream = Stream(auth, twitter_listener())
                #  Listens for tweets all over the world - should filter tweets with no Geo element
                twitter_stream.filter(locations=[-180, -90, 180, 90], async=True)
                print('---- New Instance')
                instances.append(twitter_stream)
            except Exception as e:
                pass
        else:
            for instance in instances:
                if not instance.running:
                    instances.remove(instance)
                    del instance
            print(len(os.listdir(r"C:\Users\clin8331\Documents\tw_two")))
            if len(os.listdir(r"C:\Users\clin8331\Documents\tw_two")) > 50:
                arcpy.AddMessage("~~~Batch creating features...")
                jsons_to_feature_class(r"C:\Users\clin8331\Documents\tw_two", tempdir, tempgdb, tempfc)
                arcpy.AddMessage("~~~Done!")
            time.sleep(10)


>>>>>>> f578346b26d815dcf4a1483f46566563f07229a4
