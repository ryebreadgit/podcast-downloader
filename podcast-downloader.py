import requests
import os
import logging
import xml.etree.ElementTree as ET
from pathlib import Path
import time
from sanitize_filename import sanitize

Path("./bin/feeds").mkdir(parents=True, exist_ok=True)

def initLogging():
	log_path = "./bin/"
	Path(log_path).mkdir(parents=True, exist_ok=True)
	log = logging.getLogger(__name__)
	file_name = os.path.basename(__file__).replace(os.path.splitext(__file__)[-1], "") + ".log"
	file_handler = logging.FileHandler(log_path + file_name)
	file_handler.setFormatter(logging.Formatter("(%(asctime)s) [%(levelname)-7s] %(message)s", "%Y-%m-%dT%H:%M:%S%z"))
	log.setLevel(os.environ.get("LOGLEVEL", "INFO"))
	log.addHandler(file_handler)
	log.addHandler(logging.StreamHandler())
	return log

log = initLogging()

def convert_filename(name):
	ret = name.replace(" : "," - ")
	ret = ret.replace(": ", " - ")
	ret = ret.replace(" | "," - ")
	ret = sanitize(ret)
	return ret

def download_podcast(show_title, ep_title, url, path):
	try:
		r = requests.get(url)
		ext = url[url.rfind("."):].strip()
		if "?" in ext:
			ext = ext[:ext.find("?")].strip()
		save_path = path + show_title + " - " + ep_title + ext
		with open(save_path, "wb") as f:
			f.write(r.content)
		return 0
	except Exception as e:
		return e

def get_podcast(url):
	r = requests.get(url)
	data = []
	try:
		root = ET.fromstring(r.text).find("channel")
		title = root.find("title").text
		for item in root.findall("item"):
			ep_title = convert_filename(item.find("title").text)
			url = item.find("enclosure").get("url")
			data.append([ep_title, url])
		return [title,data]

	except Exception as e:
		raise e

os.chdir("./bin/")

with open("./rss.txt", "r+", encoding="utf-8") as rss:
		rss_feeds = []
		for item in rss.readlines():
			if item != "" and item != None:
				rss_feeds.append(item.strip())
		for item in rss_feeds:
			pod = get_podcast(item)
			pod_title = convert_filename(pod[0])


			log.info("Checking updates for: " + pod_title)

			if not os.path.exists("./feeds/" + pod_title + ".txt"):
				""" Only download latest 3 if podcast doesn't exist
				cnt = 0
				if len(pod[1]) > 3:
					cnt = 3

				output = ""
				for i in range(cnt, len(pod[1])):
					output += pod[1][i][1] + "\n"
				"""
				output = "" #Fuck the above, download all of it you pussy
				with open("./feeds/" + pod_title + ".txt", "w+", encoding="utf-8") as f:
					f.write(output)

			dl_path = "/media/NAS/Automatic Downloads/podcasts/" + pod_title + "/"
			updates = False

			for i in range(len(pod[1])):
				ep_title = pod[1][i][0]
				pod_url = pod[1][i][1]
				pod_url_mod = pod_url
				if "?" in pod_url_mod:
					pod_url_mod = pod_url_mod[:pod_url_mod.find("?")]
				with open("./feeds/" + pod_title + ".txt", "r+", encoding="utf-8") as f:
					lines = []
					for item in f.readlines():
						lines.append(item.strip())
				with open("./feeds/" + pod_title + ".txt", "a+", encoding="utf-8") as f:
					if not pod_url_mod in lines:
						if not updates:
							updates = True
							log.info("Starting downloads for: " + pod_title)
						Path(dl_path).mkdir(parents=True, exist_ok=True)
						status = download_podcast(show_title=pod_title, ep_title=ep_title, url=pod_url, path=dl_path)
						if status != 0:
							log.error("ERROR: " + pod_title + " - " + ep_title + " || " + pod_url)
						else:
							log.info("Success: " + pod_title + " - " + ep_title)
							f.write(pod_url_mod + "\n")
			
			if updates:
				log.info("Finished downloads for: " + pod_title)
			else:
				log.debug("No updates found for: " + pod_title)