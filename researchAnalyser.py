# This is a script that will analyze a json produced by the University of worcester's WRAP database
import sys
import json
import os
import re
# import tsv

# Setup keyword regex
keywordList = ["\\bAccess to Justice","Accountable Institutions","Affordable Energy","All ages--elderly","Biodiviersity","Cities","Climate Change","Conserve Oceans","Consumption","Decent Work","Desertification","Economic Growth","Ecosystems","Employment","Empower women","Energy","Equitable Education","Food Security","Foster Innovation","Gender Equality","Girls","Global Partnership for Sustainable Development","Healthy Lives","Human Settlements","Hunger","Inclusive Cities","Inclusive Education","Inclusive Human Settlements","Inclusive Institutions","Inclusive Societies","Industrialization","Inequality","Infrastructure","Innovation","Justice","Land Degradation","Land","Manage Forests","Marine","Nutrition","Oceans","Opportunities for all","Peaceful Societies","Poverty","Productive Employment","Productive Patterns","Reduce Inequality","Reliable Energy","Resilient Infrastructure","Sanitation","Seas","Sustainability","Sustainable Agriculture","Sustainable Consumption","Sustainable Economic Growth","Sustainable Energy","Sustainable Growth","Sustainable Industrialization","Sustainable Oceans","Sustainable","Terrestrial Ecosystems","Water","Well-Being","Women\\b"]
keywordRegex = re.compile('\\b|\\b'.join(keywordList), flags=re.I|re.U)

# Json File from database
file_name = "export_worceprints2013.json"
if(len(sys.argv) > 1):
    file_name = sys.argv[1]

# Get the json from the file
rjson = json.load(open(file_name, 'r', encoding="utf-8"))

print("Loaded Json")

# TSV file for research output
rtsv = open("researchAnalysed.tsv", 'w', encoding="utf-8")
rtsv.write('Title\tAbstract\tKeywords\n')

# Accumulators
articles = 0
susArticles = 0
susAuthors = []
allAuthors = []

# For all the results in the json 
for robj in rjson:
    try:
        articles+=1
        rTitle = robj['title'].replace('\n',' ').replace('\r',' ').replace('\t', ' ')
        rAbs = robj['abstract'].replace('\n',' ').replace('\r',' ').replace('\t', ' ')

        # Get all the authors into a list
        creators = []
        for auth in robj["creators"]:
            aLast = auth["name"]["family"]
            aFirst = auth["name"]["given"]
            if(aLast and aFirst):
                creators.append(aLast +", "+ aFirst)
        allAuthors += creators

        # If its got a keyword in the title or abstract
        if(keywordRegex.search(rTitle) or keywordRegex.search(rAbs)):
            susArticles+=1
            # Get the list of keyword hits, and sort/remove duplicates
            matchesL = keywordRegex.findall(rTitle) + keywordRegex.findall(rAbs)
            matchesL = sorted(list(set([el.lower() for el in matchesL])))
            rtsv.write("{}\t{}\t{}\n".format(
                rTitle, rAbs, ','.join(matchesL)))
            susAuthors += creators
                
    except KeyError:
            continue
rtsv.close()

susAuthors = sorted(list(set(susAuthors)))
allAuthors = sorted(list(set(allAuthors)))

# TSV file for authors
atsv = open("susAuthors.tsv", 'w', encoding="utf-8")
# Write authors
atsv.write('\n'.join(susAuthors))
atsv.close()

# # And the same for all authors
# aatsv = open("allAuthors.tsv", 'w', encoding="utf-8")
# aatsv.write('\n'.join(allAuthors))
# aatsv.close()

# Print Results
print("Done")
print("Analysed {} research articles".format(articles))
print("Found {} sustainability research articles".format(susArticles))
print("Found {} authors, {} writing sustainability related articles"
      .format(len(allAuthors), len(susAuthors)))
