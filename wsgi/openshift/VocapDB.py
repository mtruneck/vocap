import os, os.path
import cgi
import re
import time
from whoosh import index, highlight
from whoosh.fields import Schema, TEXT, ID
from whoosh.analysis import StemmingAnalyzer, RegexAnalyzer, CharsetFilter
from whoosh.support.charset import accent_map
from whoosh.qparser import QueryParser
from whoosh.lang.porter import stem
import codecs
import getyoutubecc
from pysrt import SubRipFile


from collections import defaultdict
class CustomScorer(highlight.FragmentScorer): 
    def __init__(self, phrase): 
        # Get the list of words from the phrase query 
        self.words = phrase
    def __call__(self, f): 
        # Create a dictionary mapping words to the positions the word 
        # occurs at, e.g. "foo" -> [1, 5, 10] 
        d = defaultdict(list) 
        for token in f.matches: 
            d[token.text].append(token.pos) 
        # For each position the first word appears at, check to see if the 
        # rest of the words appear in order at the subsequent positions 
        firstword = self.words[0] 
        for pos in d[firstword]: 
            found = False 
            for word in self.words[1:]: 
                pos += 1 
                if pos not in d[word]: 
                    break 
            else: 
                found = True 
            if found: 
                return 100 
        return 0 


class VocapDB:
    def __init__(self, dir_name, ix_name, path):

        # DIR with the files and index - just one dir
        self.dir_name = dir_name
        self.ix_name = ix_name
        # Path to the dir_name
        self.path = path

        if not os.path.exists(self.path+"/"+dir_name):
            os.mkdir(self.path+"/"+dir_name)
        if index.exists_in(self.path+"/"+dir_name, indexname=ix_name):
            self.ix = index.open_dir(self.path+"/"+dir_name, indexname=ix_name);
        else:
            # Add an accent-folding filter to a stemming analyzer:
            # (it copes with the diacritisc)
            my_analyzer = RegexAnalyzer() | CharsetFilter(accent_map)
            schema = Schema(title=TEXT(stored=True), path=ID(stored=True), vid=ID(stored=True), content=TEXT(analyzer=my_analyzer))
            self.ix = index.create_in(self.path+"/"+dir_name, schema=schema, indexname=ix_name);

    def delete_from_index(self):
        with self.ix.searcher() as searcher:
            query = QueryParser("vid", self.ix.schema).parse(self.vid)
            num=self.ix.delete_by_query(query)
            print num

    def search(self,searched_text):
        with self.ix.searcher() as searcher:
            query = QueryParser("content", self.ix.schema).parse(searched_text)
            results = searcher.search(query)

            # Adjust the size of surrounding text
            my_cf = highlight.ContextFragmenter(maxchars=100000, surround=170)
            results.fragmenter = my_cf

            # Give mi fragments from the entire file
            results.fragmenter.charlimit = None
            results.formatter.between = u"\n###\n"
            #results.scorer = CustomScorer("honored to have you".split())

            to_return = []
            for hit in results:
                with codecs.open(self.path+"/"+hit["path"], "r", "utf-8") as fileobj:
                    filecontents = fileobj.read()
                lines = hit.highlights("content", text=filecontents).split(u"\n")

                matches = []
                for line in lines:
                    if line == u"###":
                        #print "Nematchuje only ###"
                        matches += [{'time': 0, 'text': '-------'}]
                        continue
                    m = re.match(r"^###(\d+) (.*$)", line);
                    if m == None:
                        #print "Nematchuje ### line"
                        continue
                    else:
                        groups = m.groups();
                        if len(groups) != 2:
                            #print "groups != 3"
                            print groups
                            continue
                        else:
                            human_time = time.strftime('%-H:%M:%S', time.gmtime(int(groups[0])))
                            matches += [{'time': groups[0], 'text': groups[1], 'human_time': human_time}]

                to_return += [{'title': hit["title"], 'vid': hit['vid'], 'matches': matches}]
            return to_return;

    def get_cc(self, lang="en"):
        # sets self.title
        #      self.srt_file
        #      self.vocap_file
        # and downloads self.srt_file

        if not isinstance(self.vid, unicode):
            self.vid = unicode(self.vid, 'utf-8')

        ######### Get subtitles and title
        cc = getyoutubecc.getyoutubecc(self.vid,lang)
        if not cc:
           return 0

        print cc.name
        self.title = cc.name

        self.srt_file = self.dir_name+u'/'+self.vid+u'.srt'
        if not isinstance(self.srt_file, unicode):
            self.srt_file = unicode(self.srt_file, 'utf-8')

        self.title_file = self.dir_name+u'/'+self.vid+u'.title'
        if not isinstance(self.title_file, unicode):
            self.title_file = unicode(self.title_file, 'utf-8')

        self.vocap_file = self.dir_name+u'/'+self.vid+u'.vocap'
        if not isinstance(self.vocap_file, unicode):
            self.vocap_file = unicode(self.vocap_file, 'utf-8')

        print "saving the file: "+self.srt_file
        cc.writeSrtFile(self.path+"/"+self.srt_file)

        fileobj=codecs.open(self.path+"/"+self.title_file, "w", "utf-8")
        fileobj.write(self.title)
        fileobj.close()

    def generate_vocap_file(self):

        ######### Generate subs in vocap format
        subs = SubRipFile.open(self.path+"/"+self.srt_file, encoding="utf-8")
        fileobj=codecs.open(self.path+"/"+self.vocap_file, "w", "utf-8")
        for i in range(len(subs)):
            text = subs[i].text
            text = text.replace(u"###", u"#.#.#")
            text = text.replace(u"\n", u" ")
            #text = cgi.escape(text)

            start = subs[i].start.seconds
            start += 60*subs[i].start.minutes
            start += 3600*subs[i].start.hours
            time = unicode(str(start),"utf-8")

            line = u"###"+time+u" "+text+u"\n"

            fileobj.write(line)
        fileobj.close()

    def add_to_index(self):
        ########## Add subs into index
        writer = self.ix.writer()
        u_name = self.title
        if not isinstance(u_name, unicode):
            u_name = unicode(u_name, 'utf-8')
        fileobj=codecs.open(self.path+"/"+self.vocap_file, "r", "utf-8")
        content=fileobj.read()
        fileobj.close()
        writer.add_document(title=u_name, path=self.vocap_file, vid=self.vid, content=content)
        writer.commit()

    def add(self, vid, lang="en"):
        # TOODO: error handling - captions not downloaded correctly, etc.

        if not isinstance(vid, unicode):
            vid = unicode(vid, 'utf-8')

        flag = 0
        with self.ix.searcher() as searcher:
            for item in searcher.documents():
                if item['vid'] == vid:
                    flag = 1

        if flag == 1:
            raise Exception("Video already in database!");

        self.vid = vid

        self.get_cc(lang)

        self.generate_vocap_file()

        self.add_to_index()



    def regenerate_index(self):
        with self.ix.searcher() as searcher:
            writer = self.ix.writer()
            for fields in searcher.all_stored_fields():
                fileobj=codecs.open(self.path+"/"+fields['path'], "r", "utf-8")
                content=fileobj.read()
                fileobj.close()
                writer.update_document(path=fields['path'], vid=fields['vid'], title=fields['title'], content=content)

    def index_from_scratch(self):
        directory =  self.path + self.dir_name
        title_files = [f for f in os.listdir(directory) if f.endswith(".title")]

        my_analyzer = RegexAnalyzer() | CharsetFilter(accent_map)
        schema = Schema(title=TEXT(stored=True), path=ID(stored=True), vid=ID(stored=True), content=TEXT(analyzer=my_analyzer))
        self.ix = index.create_in(self.path+"/"+self.dir_name, schema=schema, indexname=self.ix_name);

        ########## Add subs into index

        for title_file in title_files:

            # VID
            vid = title_file[:-6]
            if not isinstance(vid, unicode):
                vid = unicode(vid, 'utf-8')
            self.vid = vid

            # VOCAP FILE
            vocap_file = self.dir_name+"/"+vid + ".vocap"
            self.vocap_file = vocap_file

            # TITLE
            with codecs.open(self.path+self.dir_name+"/"+title_file, 'r', 'utf-8') as f:
                title = f.read().strip()
            if not isinstance(title, unicode):
                title = unicode(title, 'utf-8')
            self.title = title

            # CONTENT
            fileobj=codecs.open(self.path+"/"+self.vocap_file, "r", "utf-8")
            content=fileobj.read()
            fileobj.close()

            writer = self.ix.writer()
            writer.add_document(title=self.title, path=self.vocap_file, vid=self.vid, content=content)
            writer.commit()

            print ".",



