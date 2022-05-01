import os

def rename_scanned(morph_dir: str, file_ext: str):
    for morph in os.listdir(morph_dir):
        new_name = morph.split('_')
        new_name = new_name[0] + '-' + new_name[1] + file_ext
        os.rename(morph_dir + '/' + morph, morph_dir + '/' + new_name)

def remove_extra_extension(morph_dir: str, file_ext: str):
    for morph in os.listdir(morph_dir):
        new_name = morph.split('.')
        new_name = new_name[0] + file_ext
        os.rename(morph_dir + '/' + morph, morph_dir + '/' + new_name)

def main():
    # rename_scanned('../data/images/frll_morphs', '.jpg')
    remove_extra_extension('../data/images/frll_morphs', '.jpg')

if __name__ == '__main__':
    main()
