import config
from glob import glob
import sched
import time
import matplotlib.pyplot as plt
from validate import write_rawfile, get_shazam_tags, read_audio_file
from shutil import copyfile
import uuid
import librosa
import os
from os import path
from pydub import AudioSegment
# dark mode plt
plt.style.use(['dark_background'])
# print(plt.style.available)


def get_rawfiles_for_shazzaming():
    """returns set of rawfiles which have no responses
    i.e they need to be shazzamed"""
    raws = glob(config.dirs['rawfiles']+'*')
    raws = [i.split('/')[-1].split('.')[0] for i in raws]
    raws = set(raws)
    resps = glob(config.dirs['responses']+'*')
    resps = [i.split('/')[-1].split('.')[0] for i in resps]
    resps = set(resps)
    return raws - resps


def shazam_some_audio():
    """retreives some unshazammed rawfile and shazams it"""
    guid = get_rawfiles_for_shazzaming()
    if not len(guid):
        print('nothing to shazam')
        return None
    guid = guid.pop()
    print('will shazam this one->', guid)
    rawfile = config.dirs['rawfiles'] + guid + '.raw'
    response = get_shazam_tags(rawfile)
    print(response.to_markdown)
    return response

# TRY READ AUDIO FILES FROM COLLECTION AND SAVE TO ORIGINAL IF READABLE
print('###### IMPORTING FROM COLLECTION TO ORIGINALS #####')
collection = glob(config.dirs['collection'] + '**/**/*.*')
failpaths = []
for filepath in collection:
    filename, extension = os.path.splitext(filepath)
    id = uuid.uuid5(uuid.NAMESPACE_OID, filepath).hex
    fname_import = config.dirs['originals'] + id + extension
    print('---'*8)
    print('filepath', filepath)
    print('extension', extension)
    print(filepath)
    if extension == ".mp3":
        sound = AudioSegment.from_mp3(filepath)
        sound.export(fname_import, format="wav")
    elif extension == ".wav":
        try:
            read_audio_file(filepath)
            copyfile(filepath, fname_import)
        except RuntimeError as e:
            print('-->E', e)
    else:
        failpaths.append(filepath)
        print("unsupported extension")
# %%
# CONVERT TO AUDIO RAWFILES (ALREADY DONE)
print('###### GENERATING RAWFILES FROM ORIGINAL COLLECTION #####')
for filepath in glob(config.dirs['originals']+'*'):
    try:
        rawfile_data = write_rawfile(filepath)
        print(f'scannned:\t{filepath}')
    # except TypeError as e:
    #     print(f'skipping: {e}')
    except RuntimeError as e:
        print(f'skipping:\t{e}')


print('###### GENERATING RAWFILES FROM ORIGINAL COLLECTION #####')

# max 5 per second
# max 500 per month
print('retreiving rawfiles for shazzaming')
raws = get_rawfiles_for_shazzaming()
print(f'{len(raws)} rawfiles found')
s = sched.scheduler(time.time, time.sleep)
for _ in raws:
    print('adding shazam to queue')
    s.enter(delay=20, priority=1, action=shazam_some_audio)
print('starting scheduler!')
s.run()
