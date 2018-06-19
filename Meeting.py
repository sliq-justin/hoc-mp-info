# range:
# 0 = day
# 1 = week
# 2 = month

from flask.ext.pymongo import pymongo
import datetime
import time
import json

class Meeting:
    def __init__(self):
        self.ActualEnd = "2018-06-11 18:00:47 UTC"
        self.ActualStart = "2018-06-11 14:59:53 UTC"
        self.AssemblyProgress = 0
        self.AssemblyStatus = 0
        self.CommitteeId = None
        self.Description = "Meeting No. 139 - Standing Committee"
        self.EntityStatusDesc = "Adjourned"
        self.ForeignKey = None
        self.HasArchiveStream = True
        self.IconUri = None
        self.Id = 00000
        self.LastModifiedTime = "2018-06-11 18:42:40 UTC"
        self.Location = "Centre Block - 237-C"
        self.ScheduledStart = "2018-06-11 14:59:53 UTC"
        self.ScheduledEnd = "2018-06-11 18:00:47 UTC"
        self.Tag = None
        self.ThumbnailUri = "http://parlvu.ca/Xrender/thumbnails/thumbnail_house_e.jpg"
        self.Title = "Meeting No. 139"
        self.VenueId = None
        self.EntityStatus = 0

        self.StreamURL = "http://pvcdn1.parl.gc.ca/vod-en/_definst_/2017/2017-03-21/26956_OGGO%20Meeting%20No.%2077.mp4/playlist.m3u8"

    def meetings(self, range, mongoCollection):
        if (range < 0) or (range > 2):
            return json.dumps({"error":"invalid meeting range (%s)"}) % str(range)

        results = mongoCollection.find({}, {"_id":False})

        if results.count > 0:
            result_array = []
            for item in results:
                result_array.append(item)
            
            return json.dumps({"ContentEntityDatas":result_array})
        else:
            return json.dumps({"ContentEntityDatas":[]})

    def update(self, mongoCollection):
        # empty db's meetings collection
        mongoCollection.remove()

        # populate a few fake meetings and save to db
        
        #####
        # 1
        #####
        self.Description = "Placeholder meeting 000"
        self.Title = "MISC Meeting No. 000"
        self.HasArchiveStream = True
        self.EntityStatus = 1000
        yesterday = datetime.date.today() - datetime.timedelta(days = 1)
        self.ScheduledStart = "%s-%s-%s 8:30:53" % (str(yesterday.year), str(yesterday.month), str(yesterday.day))
        self.ScheduledEnd = "%s-%s-%s  12:45:47" % (str(yesterday.year), str(yesterday.month), str(yesterday.day))

        mongoCollection.insert_one({"Description":self.Description, \
        "HasArchiveStream":self.HasArchiveStream, \
        "EntityStatus":self.EntityStatus, \
        "Id":self.Id, \
        "ScheduledStart":self.ScheduledStart, \
        "ScheduledEnd":self.ScheduledEnd, \
        "StreamURL":self.StreamURL, \
        "ThumbnailUri":self.ThumbnailUri, \
        "Title":self.Title})

        #####
        # 2
        #####
        self.Description = "Placeholder meeting 001"
        self.Title = "MISC Meeting No. 001"
        self.HasArchiveStream = True
        self.EntityStatus = 100

        today = datetime.datetime.today()
        self.ScheduledStart = "%s-%s-%s %s:15:53" % (str(today.year), str(today.month), str(today.day), str(today.hour - 4))
        self.ScheduledEnd = "%s-%s-%s  %s:45:47" % (str(today.year), str(today.month), str(today.day), str(today.hour + 4))

        mongoCollection.insert_one({"Description":self.Description, \
        "HasArchiveStream":self.HasArchiveStream, \
        "EntityStatus":self.EntityStatus, \
        "Id":self.Id, \
        "ScheduledStart":self.ScheduledStart, \
        "ScheduledEnd":self.ScheduledEnd, \
        "StreamURL":self.StreamURL, \
        "ThumbnailUri":self.ThumbnailUri, \
        "Title":self.Title})

        #####
        # 3
        #####
        self.Description = "Placeholder meeting 002"
        self.Title = "MISC Meeting No. 002"
        self.HasArchiveStream = False
        self.EntityStatus = 1000

        self.ScheduledStart = "%s-%s-%s %s:00:53" % (str(today.year), str(today.month), str(today.day), str(today.hour))
        self.ScheduledEnd = "%s-%s-%s %s:30:47" % (str(today.year), str(today.month), str(today.day), str(today.hour + 3))

        # save to db
        mongoCollection.insert_one({"Description":self.Description, \
        "HasArchiveStream":self.HasArchiveStream, \
        "EntityStatus":self.EntityStatus, \
        "Id":self.Id, \
        "ScheduledStart":self.ScheduledStart, \
        "ScheduledEnd":self.ScheduledEnd, \
        "StreamURL":"", \
        "ThumbnailUri":self.ThumbnailUri, \
        "Title":self.Title})

        #####
        # 4
        #####
        self.Description = "Placeholder meeting 003"
        self.Title = "MISC Meeting No. 003"
        self.HasArchiveStream = False
        self.EntityStatus = 1000
        today = datetime.date.today() + datetime.timedelta(days = 7)
        self.ScheduledStart = "%s-%s-%s 8:30:53" % (str(today.year), str(today.month), str(today.day))
        self.ScheduledEnd = "%s-%s-%s  12:45:47" % (str(today.year), str(today.month), str(today.day))

        mongoCollection.insert_one({"Description":self.Description, \
        "HasArchiveStream":self.HasArchiveStream, \
        "EntityStatus":self.EntityStatus, \
        "Id":self.Id, \
        "ScheduledStart":self.ScheduledStart, \
        "ScheduledEnd":self.ScheduledEnd, \
        "StreamURL":"", \
        "ThumbnailUri":self.ThumbnailUri, \
        "Title":self.Title})
        
        return json.dumps({"updated":200})
