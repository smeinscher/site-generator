import os
import shutil


def copy_contents_to_directory(source_dir, destination_dir):
    if not os.path.exists(source_dir):
        raise Exception("Invalid source path")
    if os.path.exists(destination_dir):
        # confirm = input(f"Remove {destination_dir}? (y/n)")
        # if confirm != "y":
        # raise Exception(f"User denied clearing {destination_dir}")
        shutil.rmtree(destination_dir)
    print(f"Creating {destination_dir}")
    os.mkdir(destination_dir)
    child_items = os.listdir(source_dir)
    for child in child_items:
        relative_source_path = os.path.join(source_dir, child)
        relative_destination_path = os.path.join(destination_dir, child)
        if os.path.isfile(relative_source_path):
            print(f"Copying {relative_source_path} to {destination_dir}")
            shutil.copy(relative_source_path, relative_destination_path)
        else:
            copy_contents_to_directory(
                relative_source_path, relative_destination_path)
