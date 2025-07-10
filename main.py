import shutil
import os

from backend import app



def main():
    app.run()
    clear_folder('backend/datasets')


def clear_folder(folder_path):
    shutil.rmtree(folder_path)
    os.makedirs(folder_path)


if __name__ == '__main__':
    main()