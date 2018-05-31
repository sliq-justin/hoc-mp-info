from flask.ext.pymongo import PyMongo
import json
import urllib

class Member:
    def __init__(self):
        self.MemberId = 0
        self.ConstituencyName = None
        self.ConstituencyProvinceTerritoryName = None
        self.Email = None
        self.PersonShortHonorific = None
        self.PersonOfficialFirstName = None
        self.PersonOfficialLastName = None
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
        data_string = urllib.urlopen(link).read()

        member_info_substring = data_string[data_string.find("profile overview header") : data_string.find("profile overview current")]

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
        mongoCollection.insert_one({"_id":self.MemberId, \
        "ConstituencyName":self.ConstituencyName, \
        "ConstituencyProvinceTerritoryName":self.ConstituencyProvinceTerritoryName, \
        "Email":self.Email, \
        "PersonShortHonorific":self.PersonShortHonorific, \
        "PersonOfficialFirstName":self.PersonOfficialFirstName, \
        "PersonOfficialLastName":self.PersonOfficialLastName, \
        "Photo":self.Photo, \
        "PoliticalAffiliation":self.PoliticalAffiliation, \
        "PreferredLanguage":self.PreferredLanguage, \
        "WebSite":self.WebSite})

    def update(self, member_id, mongoCollection):
        if mongoCollection.delete_one({"_id":str(member_id)}).deleted_count == 1:
            self.add_to_cache(member_id, mongoCollection)
