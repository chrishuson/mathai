# Converts text file to python data structures and saves them as pickle files.
# Initiates Standards and Standards_Desc data structures.
# No longer in use
import csv
import pickle

def load_ccss_text():
    """returns dictionary standard:text description

        imports /Users/chris/GitHub/mathai/db/standards_text_jmap.csv
        standard - short string of characters with periods
        text - somewhat long sentence description, in plain text (source: JMAP)
        """
    dbdir = "/Users/chris/GitHub/mathai/db/"
    ccss_text = {}
    filename = dbdir + "standards_text_jmap.csv"
    with open(filename, "r", encoding='latin-1') as csvfile:
        standards = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in standards:
            if row[0] not in ccss_text.keys():
                ccss_text[row[0]] = row[1]
            #else:
                #print("duplicate: " + row[0])
    return ccss_text

def load_ccss_list():
    """Load standards hierarchy from file into a list of tuples
        DBcourse - algebra1, geometry, algebra2, precalculus
        section - area of related skills
        topic - useful detailed-level skill
        ccss standard - short alphanumeric id, e.g. F.BF.B.4
        """
    dbdir = "/Users/chris/GitHub/mathai/db/"
    filename = dbdir + "standards_tree_jmap.csv"
    standards = []
    with open(filename, "r", encoding='latin-1') as csvfile:
        nodes = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in nodes:
            course = row[0]
            section = row[1]
            topic = row[2]
            ccss_standard = row[3]
            node = (course, section, topic, ccss_standard)
            standards.append(node)
    return standards



#run only if module is called from command line
#loads standards hierarchy and description files, saves to pickle files
if __name__ == "__main__":
    t = load_ccss_text()
    #savedbfile(t, "standards_text_jmap")
    s = load_ccss_list()
    #savedbfile(s, "standards_tree_jmap")

#the standards file is a simple array, but could be restructured as a nested list:
#tree = ["root", [["algebra1", [["rate",[["Percents", ["7.RP.A.3"]], ["Error", "7.RP.A.3"]]]]], [["geometry", [["triangles", [["Pythagorean Theorem", ["G.SRT.C.8"]]]]]]]]]

    #a = input("1 descriptions, 2 tree, else enter standard id ")
    #if a == "1":
        #for k in t.keys():
            #print(k)
            #print(t[k])
    #elif a == "2":
        #s = load_ccss_list()
        #print_tree(s)
    #else:
        #t = load_ccss_text()
        #print(a)
        #print(t[a])
