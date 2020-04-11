# -*- coding: utf-8 -*-
import imagehash
import PIL
import os
import shutil
# import sys
# import time

# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()


def IdentifyDuplicates(filelist, hashfunc=imagehash.average_hash):
    duplicates = []
    hash_keys = dict()
    printProgressBar(0, len(filelist), prefix = 'Progress:', suffix = 'Complete', length = 50)
    for index, filename in enumerate(filelist):  #listdir('.') = current directory
        if os.path.isfile(filename):
            with open(filename, 'rb') as f:
                # filehash = hashlib.md5(f.read()).hexdigest()
                try:
                    filehash = hashfunc(PIL.Image.open(f))
                except:
                    pass
            if filehash not in hash_keys: 
                hash_keys[filehash] = index
            else:
                duplicates.append((index,hash_keys[filehash]))
        printProgressBar(index + 1, len(filelist), prefix = 'Progress:', suffix = 'Complete', length = 50)
    return duplicates


# def PlotDuplilcates(dupIndexList, filepath):
#     for file_indexes in dupIndexList[:30]:
#         try:
        
#             plt.subplot(121),plt.imshow(imread(file_list[file_indexes[1]]))
#             plt.title(file_indexes[1]), plt.xticks([]), plt.yticks([])

#             plt.subplot(122),plt.imshow(imread(file_list[file_indexes[0]]))
#             plt.title(str(file_indexes[0]) + ' duplicate'), plt.xticks([]), plt.yticks([])
#             plt.show()
        
#         except OSError:
#             continue
        
def MoveDuplicates(filepath,file_list,dupIndexList,move=True):
    """# Delete Files After Printing"""

    if move:
        try:
            if len(dupIndexList) > 0:
                path = os.path.join(filepath, 'duplicates')
                os.mkdir(path)
        except FileExistsError:
            pass
        for index in dupIndexList:
            try:
                shutil.move(file_list[index[0]], path)
                shutil.move(file_list[index[1]], path)
            except:
                continue
    else:
        for index in dupIndexList:
            os.remove(file_list[index[0]])

def is_image(filename):
    f = filename.lower()
    return f.endswith(".png") or f.endswith(".jpg") or \
        f.endswith(".jpeg") or f.endswith(".bmp") or f.endswith(".gif") or '.jpg' in f


def processImages(userpaths,hashmethods):
    for userpath in userpaths:
        if userpath[0].split('\\')[-1] == "duplicates":
            continue
        for hashmethod in hashmethods:
           if hashmethod == 'ahash':
               hashfunc = imagehash.average_hash
           elif hashmethod == 'phash':
               hashfunc = imagehash.phash
           elif hashmethod == 'dhash':
               hashfunc = imagehash.dhash
           elif hashmethod == 'whash-haar':
               hashfunc = imagehash.whash
           elif hashmethod == 'whash-db4':
               hashfunc = lambda img: imagehash.whash(img, mode='db4')
           print("Scanning directory: "+str(userpath[0]))
           print("Hashing method: "+str(hashmethod))
           os.chdir(userpath[0])
           file_list = os.listdir()
           file_list = [i for i in file_list if is_image(i)]
           print("Images found: "+ str(len(file_list)))
           if len(file_list) > 0:
               duplicates = IdentifyDuplicates(file_list, hashfunc)
               MoveDuplicates(userpath[0],file_list,duplicates)


if __name__ == '__main__':

    userpaths = input("File Directory: ")
    userpaths = [x for x in os.walk(userpaths)]
    print("""
ENTER METHOD(S) TO BE USED FOR HASHING OF IMAGES:
Method:
ahash: Average hashing is the algorithm which uses only a few transformation such as scale the image, convert to greyscale, calculate the mean and binarize the greyscale based on the mean. Now convert the binary image into the integer.

phash: Perceptual hash uses similar approach but instead of averaging relies on discrete cosine transformation (popular transformation in signal processing).

dhash: Difference hash uses the same approach as a-hash, but instead of using information about average values, it uses gradients (difference between adjacent pixels).

whash-haar: Haar wavelet hash. Very similar to p-hash, but instead of DCT it uses wavelet transformation.

whash-db4:  Daubechies wavelet hash

Can select single or multiple hashing mehods. E.g. ahash,phash,dhash""")

    hashmethods = input("Specify Method name: ")
    hashmethods = [i.strip() for i in hashmethods.split(',')]
    processImages(userpaths,hashmethods)
    # print("Process Completed.")