#!/usr/bin/env python

import os
import re
import sys
import time
import fnmatch
import getpass
import json
from pprint import pprint
import signal
import shutil
import subprocess
import webbrowser

includes = ['*.pak']

# transform glob patterns to regular expressions
includes = r'|'.join([fnmatch.translate(x) for x in includes])

class main():
  global u
  u = getpass.getuser()
  global f
  f = "/Users/" + u + "/Library/Application Support/Google/Chrome/Default/Extensions/"
  global path
  global tlist
  tlist = []

  os.chdir(f)

  for root, dirs, files in os.walk(f):
    files = [os.path.join(root, f) for f in files]
    files = [ f for f in files if re.match(includes, f)]

    for fname in files:
      path = os.path.dirname(fname) + "/"
      theme = path + "Cached Theme.pak"
      man = path + "manifest.json"
      manifest = open(man, "r")

      for line in manifest:
        if re.match("(.*)(N|n)ame(.*)", line):
            name = line.replace("\"name\": \"", "").strip()
            name = name.replace("\",", "")
            tlist.append(name)
            tlist.append(theme)

  def showall():
    i = int('1')
    for theme in tlist[::2]:
      print str(i)+". "+theme
      i+=1

  def switchtheme(num):
    num = int(num)
    t = tlist[2*num-1]
    o = tlist[2*num-2]
    p = subprocess.Popen(['ps', 'A'], stdout=subprocess.PIPE)
    out, err = p.communicate()
    url = o[:25].lower().replace(" ", "-")
    ch = t[77:].split("/", 1)[0]
    chstr = str(ch)
    folder = "/Users/" + u + "/Library/Application Support/Google/Chrome/Default/Extensions/" + ch + "/"
    prefspath = "/Users/" + u + "/Library/Application Support/Google/Chrome/Default/Preferences.bak"
    #data_file = open(prefspath, "r")

    #data = json.load(data_file)

    #pprint(data["extensions"]["settings"][ch])

    output_json = json.load(open(prefspath))
    with open("/Users/sboynton/Documents/Python Projects/ThemeViewer/text", "w") as file:
      mydict = json.dumps(output_json)
      for k, v in output_json["extensions"]["settings"].items():
        if k == ch:
          del k, v
        #try:
        #  print k,v
        #except:
        #  return
        print output_json
      #print output_json
      #json.dump(output_json, file)

    #print "Closing Chrome and removing theme. This should only take a few seconds."
    # Search the Preferences file for entry for theme and delete it

    #for line in out.splitlines():
      #if 'Google Chrome' in line:
        #pid = int(line.split(None, 1)[0])
        #os.kill(pid, signal.SIGKILL)
    #time.sleep(3)
    #shutil.rmtree(folder)
    #time.sleep(2)
    #webbrowser.open("https://chrome.google.com/webstore/detail/" + url + "/" + ch + "?hl=en-US&utm_source=chrome-ntp-launcher")
    #print "Done! If the theme says it's still added, close and reopen Chrome."

  def location(num):
    for theme in tlist:
      print theme

  try:
    sys.argv[1]
  except:
      print "Chrome ThemeViewer -- See and use your installed themes\n\nBy Sam Boynton\n\n!! WARNING !! -- This utility requires Chrome to be closed and reopened; make sure to save your work before using!\n\nUsage:\n\n--list: Show list of installed themes\n--use <#>: Remove theme and open Chrome Web Store download page"
  else:
    if sys.argv[1] == "--list":
      showall()
    if sys.argv[1] == "--use" and str.isdigit(sys.argv[2]):
      switchtheme(sys.argv[2])
    if sys.argv[1] == "--loc":
      location(sys.argv[1])

if __name__ == '__main__':
  main()
