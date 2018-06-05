from flask.ext.pymongo import PyMongo
import json
import urllib

class Member:
    def __init__(self):
        self.MemberId = 0
        self.Caucus = None
        self.ConstituencyName = None
        self.ConstituencyProvinceTerritoryName = None
        self.CurrentPhone = None
        self.CurrentFax = None
        self.Email = None
        self.PartyColour = None
        self.PersonShortHonorific = None
        self.PersonOfficialFirstName = None
        self.PersonOfficialLastName = None
        self.Photo = None
        self.PoliticalAffiliation = None
        self.PreferredLanguage = None        
        self.WebSite = None
        
    def find_by_member_id(self, member_id, mongoCollection):
        result = mongoCollection.find_one({"id": member_id}, {"_id":False})

        if result is not None:
            return json.dumps(result)
        else:
            return None

    def add_to_cache(self, member_id, data_string, mongoCollection):
        # parse string here to populate member fields
        self.MemberId = member_id

        member_info_substring = data_string[data_string.find("profile overview header") : data_string.find("profile overview current")]

        # self.Caucus # <span class="parlementarian-label">Political Affiliation:</span><span class="caucus"><a target="_blank" title="Political Party Web Site - Opens a New Window" href="http://www.liberal.ca">Liberal</a></span>
        caucus_substring_prefix_long = member_info_substring[member_info_substring.find("Political Party Web Site"):]
        caucus_substring_prefix_short = caucus_substring_prefix_long[caucus_substring_prefix_long.find(">") + 1 :]
        caucus_substring = caucus_substring_prefix_short[:caucus_substring_prefix_short.find("</a>")]
        
        self.Caucus = caucus_substring

        # self.ConstituencyName # <a href="/Parliamentarians/en/constituencies/Ottawa-Centre(789)" title="Click to open the constituency profile">Ottawa Centre</a></span>

        constituency_name_substring_prefix = member_info_substring[member_info_substring.find("Click to open the constituency profile") : ]
        constituency_nameString = constituency_name_substring_prefix[constituency_name_substring_prefix.find(">")+1 : constituency_name_substring_prefix.find("</a>")]

        self.ConstituencyName = constituency_nameString

        # self.ConstituencyProvinceTerritoryName # <span class="parlementarian-label">Province / Territory:</span><span class="province">Quebec</span>
        cptn_substring_prefix = member_info_substring[member_info_substring.find("<span class=\"province"):]
        cptn_string = cptn_substring_prefix[cptn_substring_prefix.find(">") + 1 :cptn_substring_prefix.find("</")]

        self.ConstituencyProvinceTerritoryName = cptn_string

        # self.email # <span class="caucus"><a title="Email this Member - Sylvie.Boucher@parl.gc.ca" href="mailto:Sylvie.Boucher@parl.gc.ca">Sylvie.Boucher@parl.gc.ca</a></span>
        email_substring_prefix = member_info_substring[member_info_substring.find("Email this Member"):]
        email_string = email_substring_prefix[email_substring_prefix.find(">") + 1 : email_substring_prefix.find("</")]

        self.Email = email_string

        # names
        full_name_start_index = data_string.find("<h2>")
        full_name_end_index = data_string.find("</h2>")
        full_name_string = data_string[full_name_start_index + 4 : full_name_end_index]
        
        if full_name_string.find("The Right Honourable") is not -1: # not found
            full_name_without_honorific = full_name_string[len("The Right Honourable") + 1:]
            first_name_string = full_name_without_honorific[:full_name_without_honorific.find(" ")]
            last_name_string = full_name_without_honorific[full_name_without_honorific.find(" ") + 1:]

            self.PersonOfficialFirstName = first_name_string
            self.PersonOfficialLastName = last_name_string
            self.PersonShortHonorific = "Rt Hon."
        elif full_name_string.find("The Honourable") is not -1: # not found
            full_name_without_honorific = full_name_string[len("The Honourable") + 1:]
            first_name_string = full_name_without_honorific[:full_name_without_honorific.find(" ")]
            last_name_string = full_name_without_honorific[full_name_without_honorific.find(" ") + 1:]

            self.PersonOfficialFirstName = first_name_string
            self.PersonOfficialLastName = last_name_string
            self.PersonShortHonorific = "Hon."
        else:
            first_name_string = full_name_string[: full_name_string.find(" ")]
            
            self.PersonOfficialFirstName = first_name_string
            self.PersonOfficialLastName = full_name_string[full_name_string.find(" ") + 1:]
        
        # self.partyColour # <div id="MiniFloorPlanSeat-Highlighted" style="font-size:2px; background-color:#ed2e38"> </div>
        party_colour_prefix_long = data_string[data_string.find("MiniFloorPlanSeat-Highlighted"):]
        party_colour = party_colour_prefix_long[party_colour_prefix_long.find("#"):party_colour_prefix_long.find(">") - 1]

        self.PartyColour = party_colour

        # self.PoliticalAffiliation # <span class="caucus"><a target="_blank" title="Political Party Web Site - Opens a New Window" href="http://www.conservative.ca">Conservative</a></span>
        political_affiliation_substring_prefix = member_info_substring[member_info_substring.find("Political Party Web Site"):]
        political_affiliation_string = political_affiliation_substring_prefix[political_affiliation_substring_prefix.find(">") + 1 : political_affiliation_substring_prefix.find("</")]

        self.PoliticalAffiliation = political_affiliation_string

        # self.photo # //www.ourcommons.ca/Parlementarians/Images/OfficialMPPhotos/42/...
        photo_start_index = member_info_substring.find("src=")
        photo_substring_prefix = member_info_substring[photo_start_index + 5 :]
        photo_string = photo_substring_prefix[ : photo_substring_prefix.find("class") - 2]

        self.Photo = "https:%s" % photo_string
 
        # self.PreferredLanguage # <span class="parlementarian-label">Preferred Language:</span><span class="constituency">French</span>
        preferred_language_start_index = member_info_substring.find("Preferred Language:</span><span class=")
        preferred_language_substring_prefix = member_info_substring[preferred_language_start_index + 20 :]
        preferred_language_string = preferred_language_substring_prefix[preferred_language_substring_prefix.find("constituency") + 14 : preferred_language_substring_prefix.find("</")]

        self.PreferredLanguage = preferred_language_string

        # self.WebSite # <a target="_blank" title="Personal Web Site - Opens a New Window" href="http://www.sylvieboucher.ca/en">www.sylvieboucher.ca/en</a> </span>
        website_substring_prefix = member_info_substring[member_info_substring.find("Personal Web Site"):]
        website_string = website_substring_prefix[website_substring_prefix.find(">") + 1 : website_substring_prefix.find("</")]

        self.WebSite = website_string

        # create db entry
        mongoCollection.insert_one({"id":self.MemberId, \
        "caucus":self.Caucus, \
        "constituencyName":self.ConstituencyName, \
        "constituencyProvinceName":self.ConstituencyProvinceTerritoryName, \
        "emailAddress":self.Email, \
        "shortHonorific":self.PersonShortHonorific, \
        "firstName":self.PersonOfficialFirstName, \
        "lastName":self.PersonOfficialLastName, \
        "partyColours": self.PartyColour, \
        "PhotoUrl":self.Photo, \
        "PoliticalAffiliation":self.PoliticalAffiliation, \
        "preferredOfficiaLanguage":self.PreferredLanguage, \
        "webSite":self.WebSite})

    def update(self, member_id, source_string, mongoCollection):
        if mongoCollection.delete_one({"id":member_id}).deleted_count == 1:
            self.add_to_cache(member_id, source_string, mongoCollection)
