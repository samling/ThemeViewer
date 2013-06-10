#!/usr/bin/env python

import os
import re
import sys
import time
import fnmatch
import getpass
import json
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

    ch = t[77:].split("/", 1)[0]

    print """

    Closing Chrome and removing theme. This should only take a few seconds.

    """

    # Search for running Chrome process and kill it
    p = subprocess.Popen(['ps', 'A'], stdout=subprocess.PIPE)
    out, err = p.communicate()
    for line in out.splitlines():
      if 'Google Chrome' in line:
        pid = int(line.split(None, 1)[0])
        os.kill(pid, signal.SIGKILL)
    print "Killilng Google Chrome process"

    # Wait 1 second
    time.sleep(1)

    # Remove the theme folder
    # Unused theme folders are removed when Chrome quits
    folder = "/Users/" + u + "/Library/Application Support/Google/Chrome/Default/Extensions/" + ch + "/"
    shutil.rmtree(folder)
    print "Removing "+folder

    # Backup Preferences and remove the theme entry from it
    prefspath = "/Users/" + u + "/Library/Application Support/Google/Chrome/Default/Preferences"
    prefsbak = "/Users/" + u + "/Library/Application Support/Google/Chrome/Default/Preferences.bak"
    shutil.move(prefspath, prefsbak)
    print "Making backup of "+prefspath
    data_file = open(prefsbak, "r")
    with open(prefspath, "w") as file:
      parsed_input = json.load(data_file)

      parsed_input["extensions"]["settings"].pop(ch)
      print "Removing "+ch+" from /Default/Extensions/"
      parsed_input["extensions"].pop("theme")
      print "Removing "+ch+" from /Default/Preferences file"

      json.dump(parsed_input, file)

    # Wait 1 second
    time.sleep(1)

    # Reopen Chrome to the theme page
    url = o[:25].lower().replace(" ", "-")
    themeurl = "https://chrome.google.com/webstore/detail/" + url + "/" + ch + "?hl=en-US&utm_source=chrome-ntp-launcher"
    webbrowser.open(themeurl)
    print themeurl

    print "Done! If the theme says it's still added, close and reopen Chrome."

  def location(num):
    for theme in tlist:
      print theme

  try:
    sys.argv[1]
  except:
      print """Chrome ThemeViewer -- See and reuse your installed themes

      By Sam Boynton

      !! WARNING !! -- This utility requires Chrome to be closed and reopened; make sure to save your work before using!


      Usage:

      list: Show list of installed themes
      use <#>: Remove theme and open Chrome Web Store download page

      """
  else:
    if sys.argv[1] == "list":
      showall()
    if sys.argv[1] == "use" and str.isdigit(sys.argv[2]):
      switchtheme(sys.argv[2])
    if sys.argv[1] == "location":
      location(sys.argv[1])

if __name__ == '__main__':
  main()
