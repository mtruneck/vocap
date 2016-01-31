from apiclient.discovery import build
from optparse import OptionParser
from VocapDB import VocapDB
from pprint import pprint
from time import sleep
from whoosh.qparser import QueryParser

DEVELOPER_KEY = "AIzaSyCCGa_gQm0A8RpcLLwXpeIPJ9rFjonyBu0"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY)

vdb = VocapDB("/stt_dir", "main", "../../")
searcher = vdb.ix.searcher()
video_list = []
good=0
bad=0
badlist = []
for item in searcher.documents():
    print item['vid'], item['title']
    videos_response = youtube.videos().list(part="id,snippet,contentDetails",id=item['vid']).execute()
    if videos_response[u'items']:
      good += 1
      print "OK OK OK"
    else:
      bad += 1
      badlist.append(item['vid']);
      print "BAD BAD BAD"
      query = QueryParser("vid", vdb.ix.schema).parse(item['vid'])
      num=vdb.ix.delete_by_query(query)
      print "result", num

print "Bad: %d" % bad
print "Good: %d" % good

#pprint(videos_response)
#if videos_response[u'items']:
	#print "yes"
#else:
	#print "no"
#videos_response = youtube.videos().list(part="id,snippet,contentDetails",id="lA4R84xfLOQ").execute()
#pprint(videos_response)
#if videos_response[u'items']:
	#print "yes"
#else:
	#print "no"
#search_response = youtube.search().list(q="Black Books",part="id,snippet",videoCaption="closedCaption",type="video").execute()
#print search_response;
