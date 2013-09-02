import fnmatch
import json
import os
import subprocess
import sys
from time import sleep

input_paths = [os.path.join('output', 'department'),
               os.path.join('output', 'all-services'),
               os.path.join('output', 'high-volume-services')]
output_path = [os.path.join('output', 'treemaps')]

def find_html_files(paths, no_of_dirs_to_ignore):
    matched_files = []
    for path in paths:
        for root, dirnames, filenames in os.walk(path):
            for filename in fnmatch.filter(filenames, '*.html'):
                parts = os.path.join(root, filename).replace(
                    '.html', '').split('/', no_of_dirs_to_ignore)
                matched_files.append(parts[-1])
    return matched_files


def generate_treemaps(input_files):
    with open('treemaps.json', 'w') as out:
        json.dump(input_files, out)

    process = subprocess.Popen(['phantomjs',
                               'grab_treemap_html.js',
                               base_url,
                               'treemaps.json',
                               'output'])

    sleep(30)
    if process.poll() is None:
        print "killing"
        process.terminate()


def diff(a, b):
    return [aa for aa in a if aa not in b]

if __name__ == "__main__":
    base_url = sys.argv[1] if len(sys.argv) > 1 else 'http://localhost:8080/'
    input_files = find_html_files(input_paths, 1)

    while input_files:
        generate_treemaps(input_files)
        input_files = diff(input_files, find_html_files(output_path, 2))

    print "Finished"
