import fnmatch
import json
from multiprocessing import pool, Pool
import os
import subprocess
import sys
import threading
from time import sleep

matched_files = []
look_in = [os.path.join('output', 'department'),
           os.path.join('output', 'all-services'),
           os.path.join('output', 'high-volume-services')]


if __name__ == "__main__":
    base_url = sys.argv[1] if len(sys.argv) > 1 else 'http://localhost:8080/'
    expected_outputs = []

    for path in look_in:
        for root, dirnames, filenames in os.walk(path):
            for filename in fnmatch.filter(filenames, '*.html'):
                ignore, url_fragment = os.path.join(root, filename).replace(
                    '.html', '').split('/', 1)
                matched_files.append(url_fragment)
                expected_outputs.append("output/treemaps/%s.html" % url_fragment)

    with open('treemaps.json', 'w') as out:
        json.dump(matched_files, out)

    def all_files_generated():
        return all(os.path.isfile(file) for file in expected_outputs)

    while not all_files_generated():
        process = subprocess.Popen(['phantomjs',
                                   'grab_treemap_html.js',
                                   base_url,
                                   'treemaps.json',
                                   'output'])

        sleep(30)
        if process.poll() is None:
            print "killing"
            process.terminate()

    print "Finished"
