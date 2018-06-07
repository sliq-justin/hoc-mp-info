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
        result = mongoCollection.find_one({"id": member_id}, {"_id":False})

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

        tmpDict = {}
        if len(self.MemberOfParliamentRole) > 0:
            for key in self.MemberOfParliamentRole.keys():
                newkey = key[:1].lower() + key[1:]
                tmpDict[newkey] = self.MemberOfParliamentRole[key]
            self.MemberOfParliamentRole = tmpDict

        tmpDict = {}
        if len(self.CaucusMemberRoles) > 0:
            for key in self.CaucusMemberRoles["CaucusMemberRole"].keys():
                newkey = key[:1].lower() + key[1:]
                tmpDict[newkey] = self.CaucusMemberRoles["CaucusMemberRole"][key]
            self.CaucusMemberRoles["CaucusMemberRole"] = tmpDict

        tmpDict = {}
        if "ParliamentaryPositionRole" in self.ParliamentaryPositionRoles.keys():
            # print "self.ParliamentaryPositionRoles = %s" % self.ParliamentaryPositionRoles
            for key in self.ParliamentaryPositionRoles["ParliamentaryPositionRole"].keys():
                newkey = key[:1].lower() + key[1:]
                tmpDict[newkey] = self.ParliamentaryPositionRoles["ParliamentaryPositionRole"][key]
            self.ParliamentaryPositionRoles["ParliamentaryPositionRole"] = tmpDict

        tmpDict = {}
        if "CommitteeMemberRole" in self.CommitteeMemberRoles.keys():
            for key in self.CommitteeMemberRoles["CommitteeMemberRole"].keys():
                newkey = key[:1].lower() + key[1:]
                tmpDict[newkey] = self.CommitteeMemberRoles["CommitteeMemberRole"][key]
            self.CommitteeMemberRoles["CommitteeMemberRole"] = tmpDict
            self.CommitteeMemberRoles["CommitteeMemberRole"]["parliamentNumber"] = int(self.CommitteeMemberRoles["CommitteeMemberRole"]["parliamentNumber"])
            self.CommitteeMemberRoles["CommitteeMemberRole"]["sessionNumber"] = int(self.CommitteeMemberRoles["CommitteeMemberRole"]["sessionNumber"])

        # tmpDict = {}
        # for rolesList in self.ProfileParliamentaryAssociationsandInterparliamentaryGroupRoles:
        #     for key in rolesList["ProfileParliamentaryAssociationsandInterparliamentaryGroupsExport"].keys():
        #         newkey = key[:1].lower() + key[1:]
        #         # print newkey
        #         tmpDict[newkey] = rolesList["ProfileParliamentaryAssociationsandInterparliamentaryGroupsExport"][key]
        #     self.ProfileParliamentaryAssociationsandInterparliamentaryGroupRoles[rolesList] = tmpDict

        mongoCollection.insert_one({"id":self.MemberId, \
        "MemberOfParliamentRole":self.MemberOfParliamentRole, \
        "CaucusMemberRoles":self.CaucusMemberRoles, \
        "ParliamentaryPositionRoles":self.ParliamentaryPositionRoles, \
        "CommitteeMemberRoles":self.CommitteeMemberRoles, \
        "ProfileParliamentaryAssociationsandInterparliamentaryGroupRoles":self.ProfileParliamentaryAssociationsandInterparliamentaryGroupRoles})

    def update(self, member_id, dataDict, mongoCollection):
        if mongoCollection.delete_one({"id":member_id}).deleted_count == 1:
            self.add_to_cache(member_id, dataDict, mongoCollection)
