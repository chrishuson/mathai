# Converts text file to python data structures and saves them as pickle files.
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

def savedbfile(dbfile, filename):
    """Saves persistent record using pickle

        dbfile - to be saved (problem records, standards files)
        filename -  filename.pickle in /Users/chris/GitHub/mathai/db
         ("bank", "standards_text_jmap", "standards_tree_jmap")
        """
    dbdir = "/Users/chris/GitHub/mathai/db/"
    p = dbdir + filename + '.pickle'
    with open(p, 'wb') as f:
        pickle.dump(dbfile, f, pickle.HIGHEST_PROTOCOL)

def loaddbfile(filename):
    """Retrieves persistent record using Pickle

        filename -  filename.pickle in /Users/chris/GitHub/mathai/db
         ("bank", "standards_text_jmap", "standards_tree_jmap")
        (problem records, standards files)
        """
    dbdir = "/Users/chris/GitHub/mathai/db/"
    p = dbdir + filename + '.pickle'
    with open(p, 'rb') as f:
        return pickle.load(f)


def print_tree(s):
    """Print out nested list of standardsdir

        s is a list of 4-tuples
        """
    print(s[0][0])
    print("   " + s[0][1])
    print("      " + s[0][2] + "  " + s[0][3])
    for i in range(1,len(s)):
        if not s[i-1][0] == s[i][0]:
            print(s[i][0])
            print("   " + s[i][1])
            print("      " + s[i][2] + "  " + s[i][3])
        elif not s[i-1][1] == s[i][1]:
            print("   " + s[i][1])
            print("      " + s[i][2] + "  " + s[i][3])
        elif not s[i-1][2] == s[i][2]:
            print("      " + s[i][2] + "  " + s[i][3])
        elif not s[i-1][3] == s[i][3]:
            print("                       " + s[i][3])


#run only if module is called from command line
#loads standards hierarchy and description files, saves to pickle files
if __name__ == "__main__":
    t = load_ccss_text()
    savedbfile(t, "standards_text_jmap")
    s = load_ccss_list()
    savedbfile(s, "standards_tree_jmap")

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
