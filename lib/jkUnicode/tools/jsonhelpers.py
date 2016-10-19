import codecs, json, os

json_path = os.path.join(os.path.split(os.path.dirname(os.path.realpath(__file__)))[0], "json")

def json_to_file(path, file_name, obj):
	with codecs.open(os.path.join(path, "%s.json" % file_name), "w", "utf-8") as f:
		json.dump(obj, f, ensure_ascii=False, indent=4, sort_keys=True)

def dict_from_file(path, file_name):
	with codecs.open(os.path.join(path, "%s.json" % file_name), "r", "utf-8") as f:
		return json.load(f)
