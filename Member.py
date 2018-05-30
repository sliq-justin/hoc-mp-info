from flask.ext.pymongo import PyMongo
import json
import urllib

class Member:
    def __init__(self):
        self.MemberId = 0
        self.ConstituencyName = None
        self.ConstituencyProvinceTerritoryName = None
        self.Email = None
        self.Photo = None
        self.PoliticalAffiliation = None
        self.PreferredLanguage = None        
        self.WebSite = None
        
    def find_by_member_id(self, member_id, mongoCollection):
        result = mongoCollection.find_one({"_id": member_id})

        if result is not None:
            return json.dumps(result)
        else:
            return None

    def add_to_cache(self, member_id, mongoCollection):
        # parse string here to populate member fields
        self.MemberId = member_id

        link = "http://www.ourcommons.ca/Parliamentarians/en/members/%s" % member_id
        dataString = urllib.urlopen(link).read()

        startIndex = dataString.find("profile overview header")
        endIndex = dataString.find("profile overview current")

        member_substring = dataString[startIndex : endIndex]

        # print member_substring

        # self.ConstituencyName:
        #   <span class="constituency"><a href="/Parliamentarians/en/constituencies/Beauport-Cote-de-Beaupre-Ile-dOrleans-Charlevoix(656)" title="Click to open the constituency profile">Beauport-C&#244;te-de-Beaupr&#233;-&#206;le d&#39;Orl&#233;ans-Charlevoix</a></span>
        cnStartIndex = member_substring.find("Click to open the constituency profile")
        constituencyName_substring_start = member_substring[cnStartIndex : ]
        constituencyName_substring_end = constituencyName_substring_start[constituencyName_substring_start.find(">")+1 : constituencyName_substring_start.find("</a>")]

        # print constituencyName_substring_end
        self.ConstituencyName = constituencyName_substring_end

        # self.ConstituencyProvinceTerritoryName:
        #   
        #   <span class="parlementarian-label">Province / Territory:</span><span class="province">Quebec</span>
        cptnStartIndex = member_substring.find("<span class=\"province")
        cptnString_long = member_substring[cptnStartIndex:]
        cptnString_trimmed = cptnString_long[cptnString_long.find(">") + 1 :cptnString_long.find("</")]

        # print cptnString_trimmed
        self.ConstituencyProvinceTerritoryName = cptnString_trimmed

        # self.email
        #   <span class="caucus"><a title="Email this Member - Sylvie.Boucher@parl.gc.ca" href="mailto:Sylvie.Boucher@parl.gc.ca">Sylvie.Boucher@parl.gc.ca</a></span>
        emailStartIndex = member_substring.find("Email this Member")
        emailString_long = member_substring[emailStartIndex:]
        emailString_trimmed = emailString_long[emailString_long.find(">") + 1 : emailString_long.find("</")]

        # print emailString_trimmed
        self.Email = emailString_trimmed

        # self.PoliticalAffiliation:
        #   <span class="caucus"><a target="_blank" title="Political Party Web Site - Opens a New Window" href="http://www.conservative.ca">Conservative</a></span>
        paStartIndex = member_substring.find("Political Party Web Site")
        paString_long = member_substring[paStartIndex:]
        paString_trimmed = paString_long[paString_long.find(">") + 1 : paString_long.find("</")]

        # print paString_trimmed
        self.PoliticalAffiliation = paString_trimmed

         # self.photo: 
        #   from //www.ourcommons.ca/Parlementarians/Images/OfficialMPPhotos/42/ to class = "picture"
        photoStartIndex = member_substring.find("src=")
        photoString_long = member_substring[photoStartIndex + 5 :]
        photoString_trimmed = photoString_long[ : photoString_long.find("class") - 2]

        # print photoString_trimmed
        self.Photo = photoString_trimmed
 
        # self.PreferredLanguage:
        #   <span class="parlementarian-label">Preferred Language:</span><span class="constituency">French</span>
        plStartIndex = member_substring.find("Preferred Language:</span><span class=")
        plString_long = member_substring[plStartIndex + 20 :]
        plString_trimmed = plString_long[plString_long.find("constituency") + 14 : plString_long.find("</")]

        # print plString_trimmed
        self.PreferredLanguage = plString_trimmed

        # self.WebSite:
        #   <a target="_blank" title="Personal Web Site - Opens a New Window" href="http://www.sylvieboucher.ca/en">www.sylvieboucher.ca/en</a> </span>
        wsStartIndex = member_substring.find("Personal Web Site")
        wsString_long = member_substring[wsStartIndex:]
        wsString_trimmed = wsString_long[wsString_long.find(">") + 1 : wsString_long.find("</")]

        # print wsString_trimmed
        self.WebSite = wsString_trimmed

        # create db entry
        mongoCollection.insert_one({"_id":self.MemberId, \
        "constituencyName":self.ConstituencyName, \
        "constituencyProvinceTerritoryName":self.ConstituencyProvinceTerritoryName, \
        "email":self.Email, \
        "photo":self.Photo, \
        "politicalAffiliation":self.PoliticalAffiliation, \
        "preferredLanguage":self.PreferredLanguage, \
        "webSite":self.WebSite})

        # return "Member.py | add_to_cache() | return"

    def update(self, member_id, dataDict, mongoCollection):
        pass

        # self.MemberId = member_id
        # self.Email = dataDict["Profile"]["MemberOfParliamentRole"]
        # self.Photo = ""
        # self.PoliticalAffiliation = ""
        # self.PreferredLanguage = dataDict["Profile"]["CaucusMemberRoles"]
        # self.ConstituencyName = dataDict["Profile"]["ParliamentaryPositionRoles"]
        # self.ConstituencyProvinceTerritoryName = dataDict["Profile"]["CommitteeMemberRoles"]
        # self.WebSite = dataDict["Profile"]["ProfileParliamentaryAssociationsandInterparliamentaryGroupRoles"]

        # mongoCollection.find_one_and_update({"_id":str(self.MemberId)},
        # {"$set":{"constituencyName":self.ConstituencyName, \
        # "constituencyProvinceTerritoryName":self.ConstituencyProvinceTerritoryName, \
        # "email":self.Email, \
        # "photo":self.Photo, \
        # "politicalAffiliation":self.PoliticalAffiliation, \
        # "preferredLanguage":self.PreferredLanguage, \
        # "webSite":self.WebSite}},
        # {"upsert":True, "returnNewDocument":True})
