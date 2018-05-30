from flask.ext.pymongo import PyMongo
import json

class Role:
    def __init__(self):
        self.MemberId = 0
        self.MemberOfParliamentRole = {}
        self.CaucusMemberRoles = {}
        self.ParliamentaryPositionRoles = {}
        self.CommitteeMemberRoles = {}
        self.ProfileParliamentaryAssociationsandInterparliamentaryGroupRoles = {}

    def find_by_member_id(self, member_id, mongoCollection):
        result = mongoCollection.find_one({"_id": member_id})

        if result is not None:
            return json.dumps(result)
        else:
            return None

    def add_to_cache(self, member_id, dataDict, mongoCollection):
        self.MemberId = member_id
        self.MemberOfParliamentRole = dataDict["Profile"]["MemberOfParliamentRole"]
        self.CaucusMemberRoles = dataDict["Profile"]["CaucusMemberRoles"]
        self.ParliamentaryPositionRoles = dataDict["Profile"]["ParliamentaryPositionRoles"]
        self.CommitteeMemberRoles = dataDict["Profile"]["CommitteeMemberRoles"]
        self.ProfileParliamentaryAssociationsandInterparliamentaryGroupRoles = dataDict["Profile"]["ProfileParliamentaryAssociationsandInterparliamentaryGroupRoles"]

        mongoCollection.insert_one({"_id":self.MemberId, \
        "MemberOfParliamentRole":self.MemberOfParliamentRole, \
        "CaucusMemberRoles":self.CaucusMemberRoles, \
        "ParliamentaryPositionRoles":self.ParliamentaryPositionRoles, \
        "CommitteeMemberRoles":self.CommitteeMemberRoles, \
        "ProfileParliamentaryAssociationsandInterparliamentaryGroupRoles":self.ProfileParliamentaryAssociationsandInterparliamentaryGroupRoles})

    def update(self, member_id, dataDict, mongoCollection):
        self.MemberId = member_id
        self.MemberOfParliamentRole = dataDict["Profile"]["MemberOfParliamentRole"]
        self.CaucusMemberRoles = dataDict["Profile"]["CaucusMemberRoles"]
        self.ParliamentaryPositionRoles = dataDict["Profile"]["ParliamentaryPositionRoles"]
        self.CommitteeMemberRoles = dataDict["Profile"]["CommitteeMemberRoles"]
        self.ProfileParliamentaryAssociationsandInterparliamentaryGroupRoles = dataDict["Profile"]["ProfileParliamentaryAssociationsandInterparliamentaryGroupRoles"]

        mongoCollection.find_one_and_update({"_id":str(self.MemberId)},
        {"$set":{"MemberOfParliamentRole":self.MemberOfParliamentRole, \
        "CaucusMemberRoles":self.CaucusMemberRoles, \
        "ParliamentaryPositionRoles":self.ParliamentaryPositionRoles, \
        "CommitteeMemberRoles":self.CommitteeMemberRoles, \
        "ProfileParliamentaryAssociationsandInterparliamentaryGroupRoles":self.ProfileParliamentaryAssociationsandInterparliamentaryGroupRoles}},
        {"upsert":True, "returnNewDocument":True})
