import os

def rename_scanned(morph_dir: str, file_ext:str):
    for morph in os.listdir(morph_dir):
        new_name = morph.split('-')
        new_name = new_name[0] + '-' + new_name[1] + file_ext
        os.rename(morph_dir + '/' + morph, morph_dir + '/' + new_name)

def main():
    rename_scanned('../data/images/morphs_renamed_scanned', '.png')

if __name__ == '__main__':
    main()
