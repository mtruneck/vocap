from VocapDB import VocapDB
new = VocapDB("stt_dir", "main", "../../")
new.ix.doc_count()

reader = new.ix.reader()

for item in reader.all_terms():
    print item
