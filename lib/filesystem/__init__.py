import os


def create_directory(output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
