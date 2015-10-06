import json
import time
import os
import tempfile
import arcpy
from tweepy.streaming import StreamListener
from tweepy import Stream, OAuthHandler, API
from .twitter_oauth_strings import *


class Toolbox(object):
    def __init__(self):
        self.label = "Toolbox"
        self.alias = "toolbox"
        self.tools = [GeoTwitterToFeatureClass]


class GeoTwitterToFeatureClass():

    class TwitterListener(StreamListener):
        def __init__(self):
            super().__init__()
            self.pos = 1

        def on_data(self, data):
            j = json.loads(data)
            try:
                coords = j["coordinates"]
                if coords:
                    with open(r"C:\Users\clin8331\Documents\tw_two\tw{}.json".format(self.pos), 'w') as f:
                        json.dump(j, f)
                    self.pos += 1
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

    @staticmethod
    def jsons_to_feature_class(folder_path, tempdir, tempgdb, tempfc):
        import os
        gdb_path = tempdir + os.path.sep + tempgdb
        arcpy.env.overwriteOutput = True
        with arcpy.da.InsertCursor(os.path.join(gdb_path, tempfc),
                                   ['SHAPE@X', 'SHAPE@Y', 'MsgText']) as cursor:
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
                        except:
                            pass
                    os.remove(folder_path + os.sep + file)
                else:
                    pass
        arcpy.AddMessage('JSON to FC Batch Completed')

    def getParameterInfo(self):
        out_fc = arcpy.Parameter(displayName="Output Feature Class",
                                 name="out_fc",
                                 datatype="DEFeatureClass",
                                 parameterType="Required",
                                 direction="Output")
        return [out_fc]

    def execute(self, paramaters):
        tempdir = tempfile.gettempdir()
        tempgdb = 'scratch.gdb'
        tempfc = 'tw'
        gdb_path = tempdir + os.path.sep + tempgdb
        auth = OAuthHandler(cons_tok, cons_sec)
        auth.set_access_token(app_tok, app_sec)
        instances = []
        fc = arcpy.CreateFeatureclass_management(gdb_path, tempfc, "POINT")
        arcpy.AddField_management(fc, 'MsgText', 'TEXT')
        while True:
            if len(instances) < 5:
                try:
                    twitter_stream = Stream(auth, GeoTwitterToFeatureClass.TwitterListener())
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
                    GeoTwitterToFeatureClass.jsons_to_feature_class(r"C:\Users\clin8331\Documents\tw_two",
                                                                    tempdir,
                                                                    tempgdb,
                                                                    tempfc)
                    arcpy.AddMessage("~~~Done!")
                time.sleep(10)


# Params - out_fc