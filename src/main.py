import os
import shutil
get_public_dir = f"{os.getcwd()}/public"

def make_public_dir():
  if (os.path.exists(get_public_dir) == False):
    os.mkdir(get_public_dir)

def clean_up():
  _, directories, files = next(os.walk(get_public_dir))
  clean_up_files(files)
  clean_up_directories(directories)

def clean_up_files(files):
  if (len(files) > 0):
    os.remove(f"{get_public_dir}/{files[0]}")
    if (len(files[1:]) > 0):
      clean_up_files(files[1:])
     
def clean_up_directories(directories):
  if (len(directories) > 0):
    shutil.rmtree(f"{get_public_dir}/{directories[0]}")
    if (len(directories[1:]) > 0):
      clean_up_directories(directories[1:])

def copy_files(files, from_path, to_path):
  if (len(files) > 0):
    shutil.copy(f"{from_path}/{files[0]}", to_path)
    if (len(files[1:]) > 0):
      copy_files(files[1:], from_path, to_path)

def copy_dirs(from_path, to_path):
  _, directories, files = next(os.walk(from_path))
  if (len(directories) > 0):
    for dir in directories:
      end_path = f"{from_path}/{dir}"
      pl_path = f"{to_path}/{dir}"
      _, sub_dirs, _ = next(os.walk(end_path))
      os.mkdir(pl_path)
      if (len(sub_dirs) > 0):
        copy_dirs(end_path, pl_path)
  if (len(files) > 0):
    copy_files(files, from_path, to_path)

def move_files():
  make_public_dir()
  clean_up()
  get_static_dir = f"{os.getcwd()}/static"
  copy_dirs(get_static_dir, get_public_dir)

def main():
  move_files()
main()
