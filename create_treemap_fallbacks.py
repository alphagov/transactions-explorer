import fnmatch
import json
import os
import subprocess
import sys
import threading
from time import sleep


if len(sys.argv) is not 4:
    print "Usage\n\t python create_treemap_fallbacks.py [base_url] [timeout] [max_retries]"
    exit(1)


base_url = sys.argv[1]
timeout = int(sys.argv[2])
max_retries = int(sys.argv[3])

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

    def timeout_callback(p):
      if p.poll() is None:
        try:
          print "[TREEMAP RENDERING] Phantom seems to be hanging... killing process"
          p.kill()
        except:
          pass

    process = subprocess.Popen(['phantomjs',
                               'grab_treemap_html.js',
                               base_url,
                               'treemaps.json',
                               'output'])

    timer = threading.Timer(timeout, timeout_callback, [process])
    timer.start()
    process.wait()


def diff(a, b):
    return [aa for aa in a if aa not in b]

if __name__ == "__main__":
    input_files = find_html_files(input_paths, 1)
    retries = 0
    running = True

    while input_files and running:
        print "[TREEMAP RENDERING] Generating treemap HTML. Retries left %i." % (max_retries - retries)
        generate_treemaps(input_files)
        retries = retries + 1
        input_files = diff(input_files, find_html_files(output_path, 2))
        running = retries < max_retries

    print "Finished"
