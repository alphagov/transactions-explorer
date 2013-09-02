import fnmatch
import json
from multiprocessing import pool
import os
import subprocess
import sys
import threading

matched_files = []
look_in = [os.path.join('output', 'department'),
           os.path.join('output', 'all-services'),
           os.path.join('output', 'high-volume-services')]


def do_timeout(process):
    if process.poll() is None:
        try:
            print "attempting to kill phantom because it looks like it's hanging..."
            process.kill()
        except:
            pass


if __name__ == "__main__":
    base_url = sys.argv[1] if len(sys.argv) > 1 else 'http://localhost:8080/'

    for path in look_in:
        for root, dirnames, filenames in os.walk(path):
            for filename in fnmatch.filter(filenames, '*.html'):
                ignore, url_fragment = os.path.join(root, filename).replace(
                    '.html', '').split('/', 1)
                matched_files.append(url_fragment)

    with open('treemaps.json', 'w') as out:
        json.dump(matched_files, out)

    def target():
        subprocess.call(['phantomjs',
                         'grab_treemap_html.js',
                         base_url,
                         'treemaps.json',
                         'output'])

    t = threading.Thread(target=target)
    t.start()
    t.join(timeout=5.0)

    if t.is_alive():
        print "attempting to kill phantom because it looks like it's hanging..."
        t.kill()

