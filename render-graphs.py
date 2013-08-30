import fnmatch
import os
import json
import subprocess

matched_files = []
domain = "http://localhost:8080/"
look_in = [ os.path.join('output', 'department'),
            os.path.join('output', 'all-services'),
            os.path.join('output', 'high-volume-services') ]


if __name__ == "__main__":
    for path in look_in:
        for root, dirnames, filenames in os.walk(path):
            for filename in fnmatch.filter(filenames, '*.html'):
                ignore, url_fragment = os.path.join(root, filename).replace('.html', '').split('/', 1)
                matched_files.append(url_fragment)

    with open('treemaps.json', 'w') as out:
        json.dump(matched_files, out)

    subprocess.call(['phantomjs', 'un-js.js', 'http://localhost:8080/', 'treemaps.json', 'output'])

