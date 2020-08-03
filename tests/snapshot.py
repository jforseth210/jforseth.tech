from shutil import copyfile, move, copytree, rmtree
from os import remove


def backup(filename):
    try:
        copyfile(filename, filename + ".orig")
    except FileNotFoundError:
        print("File was not copied successfully: {} does not exist.".format(filename))
        raise FileNotFoundError


def restore(filename):
    try:
        remove(filename)
    except FileNotFoundError:
        print("The modified file appears to have been deleted. Recreating the old one.")
    try:
        move(filename + ".orig", filename)
    except FileNotFoundError:
        print('The file: {} has gone missing.'.format(filename))
        raise FileNotFoundError


def backuptree(foldername):
    try:
        copytree(foldername, "tests/" + foldername)
    except FileExistsError:
        print("Folder has already been backed up. Overwriting existing backup.")
        rmtree("tests/" + foldername)
        copytree(foldername, "tests/" + foldername)


def restoretree(foldername):
    rmtree(foldername)
    move("tests/" + foldername, foldername)
