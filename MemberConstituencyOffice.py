from flask.ext.pymongo import PyMongo
import json
import urllib

class MemberConstituencyOffice:
    def __init__(self):
        self.id = 0
        self.memberid = 0
        self.mpId = None
        self.constituencyName = None
        self.isMainOffice = None
        self.city = None
        self.building = None
        self.provinceCode = None
        self.addr1 = None
        self.addr2 = None
        self.addr3 = None
        
    def find_by_member_id(self, member_id, mongoCollection):
        result = mongoCollection.find_one({"id": member_id}, {"_id":False})

        if result is not None:
            return json.dumps(result)
        else:
            return None

    def add_to_cache(self, member_id, source_string, mongoCollection):
        first_office = source_string[source_string.find("<li>"):]

        first_office_prefix_1 = first_office[first_office.find("<span>")+6:] 
        first_office_component_1 = first_office_prefix_1[:first_office_prefix_1.find(" (")]
        print first_office_component_1

        self.addr1 = first_office_component_1

        first_office_prefix_2 = first_office_prefix_1[first_office_prefix_1.find("<span>")+6:]
        first_office_component_2 = first_office_prefix_2[:first_office_prefix_2.find("</")]
        print first_office_component_2

        self.addr2 = first_office_component_2

        first_office_prefix_3 = first_office_prefix_2[first_office_prefix_2.find("<span>")+6:]
        first_office_component_3 = first_office_prefix_3[:first_office_prefix_3.find("</")]
        print first_office_component_3

        self.city = first_office_component_3

        first_office_prefix_4 = first_office_prefix_3[first_office_prefix_3.find("<span>")+6:]
        first_office_component_4 = first_office_prefix_4[:first_office_prefix_4.find("</")]
        print first_office_component_4

        self.provinceCode = first_office_component_4

    # create db entry
        mongoCollection.insert_one({"id":self.memberid, \
        "mpId":self.mpId, \
        "memberid":self.memberid, \
        "constituencyName":self.constituencyName, \
        "isMainOffice":self.isMainOffice, \
        "city":self.city, \
        "building":self.building, \
        "provinceCode":self.provinceCode, \
        "addr1": self.addr1, \
        "addr2":self.addr2, \
        "addr3":self.addr3})
