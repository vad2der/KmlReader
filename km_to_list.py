import os
from collections import OrderedDict
import xmltodict

BASE_ROOT = os.path.dirname(os.path.abspath(__file__))

class Parser:
    def __init__(self, filename):		
        self.filename = filename
        self.file_path = os.path.join(BASE_ROOT, self.filename)
        self.content = None

    def parse (self):
        if self.filename.lower().endswith(".kmz"):
            return "KMZ filetype"
        elif self.filename.lower().endswith(".kml"):
            self.content = self.get_the_content()
            output_OrderedDict = self.open_xml()
            output_Refined = self.refine_content(output_OrderedDict)
            #print (output_Refined)
            return output_Refined
        else:
            return "Unknown filetype"

    def get_the_content(self):
        """
        KML files have XSD and XML parts togeather, as well as at least 4 namespaces:
        1. xmlns="http://www.opengis.net/kml/2.2"
        2. xmlns:gx="http://www.google.com/kml/ext/2.2"
        3. xmlns:kml="http://www.opengis.net/kml/2.2"
        4. xmlns:atom="http://www.w3.org/2005/Atom"
        The idea is to simplify the content: get rid of XSD part and eleminate lines from namespace 2.
        Also, to substitute 'Folder' tag with 'data' tag - is it really necessary ??? we will see.
        """
        start_tag = "<Folder>"
        finish_tag = "</Folder>"
        output = "<?xml version='1.0'?>\n"
        record = False
        tags_to_exclude = ["gx:", ":atom", ":kml", ]
        with open(self.file_path) as f:
            for line in f:
                # skip some lines
                if "gx:" in line:
                    continue
                # if line does not comply, do not record it
                if finish_tag in line:
                    #print("stop record")
                    record = False
                    output += "</data>"
                # if line fits, record it
                if record:
                    output += line.rstrip()
                # see if line fits
                if start_tag in line:
                    #print("start record")
                    record = True
                    output += "<data>\n"
        #print (output)
        return output

    def open_xml (self, content=None):
        """
        consumts only pure XML
        """
        root = None
        if content is not None:
            root = xmltodict.parse(content)
        else:            
            root = xmltodict.parse(self.content)             
        return root

    def refine_content(self, d):
        output = []
        try:
            for item in d["data"]["Placemark"]:
                #print (item)
                if type(item) is OrderedDict:
                    line = {}
                    for sub_item in item.items():            
                        line[sub_item[0]] = sub_item[1]
                        if type(sub_item[1]) is OrderedDict:
                            internal_dict = {}
                            for s_i in sub_item[1].items():
                                internal_dict[s_i[0]] = s_i[1]
                            line[sub_item[0]] = internal_dict
                    output.append(line)
        except Exception as e:
            print ("Alarm, pizda")
        return output