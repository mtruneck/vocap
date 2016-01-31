import os
from time import gmtime, strftime
from django.shortcuts import render_to_response
import getyoutubecc
from django.http import HttpResponse
from django.utils import simplejson
from pysrt import SubRipFile
import time
import datetime
import codecs
from whoosh.fields import Schema, TEXT, ID
import os.path
from  whoosh import index
from whoosh.qparser import QueryParser
from VocapDB import VocapDB


def howto(request):
    return render_to_response('howto.html')

def whatisit(request):
    return render_to_response('whatisit.html')

def about(request):
    return render_to_response('about.html')

def turnoncc(request):
    return render_to_response('turnoncc.html')

def home(request):
    cc = getyoutubecc.getyoutubecc(u'T8X15QkS-N8')
    return render_to_response('home/home.html', {'name': cc.name})

def index(request):
    on_openshift = 0
    if os.environ.has_key('OPENSHIFT_REPO_DIR'):
        on_openshift = 1

    if 'OPENSHIFT_REPO_DIR' in os.environ:
        filename = os.environ.get('OPENSHIFT_REPO_DIR') + "/stt_dir/log.txt"
    else:
        filename = "../../log.txt"

    fileobj=codecs.open(filename, "a", "utf-8")
    fileobj.write(strftime("%Y-%m-%d %H:%M:%S", gmtime()) + 
                  "\t" + 
                  request.META['HTTP_ACCEPT_LANGUAGE'] +
                  "\t" + 
                  request.META['REMOTE_ADDR'] +
                  "\t" + 
                  request.META['HTTP_USER_AGENT'] +
                  "\t" + 
                  request.META['HTTP_HOST'] +
                  "\n")
    fileobj.close()

    return render_to_response('index.html', {'on_openshift': on_openshift})

def list(request):
    if 'OPENSHIFT_REPO_DIR' in os.environ:
        vdb = VocapDB("/stt_dir", "main", os.environ.get('OPENSHIFT_REPO_DIR'))
    else:
        vdb = VocapDB("/stt_dir", "main", "../../")
    searcher = vdb.ix.searcher()
    video_list = []
    for item in searcher.documents():
        #print item['title']
        #video_list += [ { 'vid': item['title']  }  ]
        video_list += [  ( item['vid'], item['title'] ) ]
    count = vdb.ix.doc_count()
    return render_to_response('list.html', {'video_list': video_list, 'count': count})

def search(request):
    searched_text = request.GET["search"];

    if 'OPENSHIFT_REPO_DIR' in os.environ:
        filename = os.environ.get('OPENSHIFT_REPO_DIR') + "/stt_dir/search_log.txt"
    else:
        filename = "../../search_log.txt"

    fileobj=codecs.open(filename, "a", "utf-8")
    fileobj.write(strftime("%Y-%m-%d %H:%M:%S", gmtime()) + 
                  "\t" + 
                  request.META['REMOTE_ADDR'] +
                  "\t" + 
                  searched_text +
                  "\n")
    fileobj.close()

    if 'OPENSHIFT_REPO_DIR' in os.environ:
        vdb = VocapDB("/stt_dir", "main", os.environ.get('OPENSHIFT_REPO_DIR'))
    else:
        vdb = VocapDB("/stt_dir", "main", "../../")
    results = vdb.search(searched_text)

    message = {'results': results}
    json = simplejson.dumps(message)
    return HttpResponse(json, mimetype='application/json')

def add(request):
    vid = request.GET["vid"]
    if 'OPENSHIFT_REPO_DIR' in os.environ:
        vdb = VocapDB("/stt_dir", "main", os.environ.get('OPENSHIFT_REPO_DIR'))
    else:
        vdb = VocapDB("/stt_dir", "main", "../../")
    vdb.add(vid);
    return render_to_response('add.html', {'title': vdb.title})


def delete(request):
    vid = request.GET["vid"]
    if 'OPENSHIFT_REPO_DIR' in os.environ:
        vdb = VocapDB("/stt_dir", "main", os.environ.get('OPENSHIFT_REPO_DIR'))
    else:
        vdb = VocapDB("/stt_dir", "main", "../../")
    vdb.vid=vid
    vdb.delete_from_index()
    return render_to_response('add.html')





