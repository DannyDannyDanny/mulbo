import config
from glob import glob
import soundfile as sf
import pandas as pd
import matplotlib.pyplot as plt
from validate import write_rawfile, get_shazam_tags
# dark mode plt
plt.style.use(['dark_background'])
# print(plt.style.available)

for filepath in glob(config.dirs['originals']+'*'):
    try:
        rawfile_data = write_rawfile(filepath)
        print(f'scannned:\t{filepath}')
    # except TypeError as e:
    #     print(f'skipping: {e}')
    except RuntimeError as e:
        print(f'skipping:\t{e}')

# %%
for raw in glob(config.dirs['rawfiles']+'*'):
    kw = dict(channels=1, samplerate=44100, format='RAW', subtype='PCM_16')
    sig, fs = sf.read(raw, **kw)
    break

response = get_shazam_tags(raw)
# %%
# %%
pd.read_pickle(resp_path)
