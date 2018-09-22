'''
为 data 文件夹建立索引
'''

import os
import hashlib
import json
import gzip

packageUrl = 'https://rawgit.com/gwy15/HmNewUISucksData/master/data/'
resVersion = '20180909' + '123456'


def indexManifest():
    'index data dir to make manifest'
    base = 'data'
    manifest = []

    for dirpath, dirnames, filenames in os.walk(base):
        for filename in filenames:
            fullFileName = dirpath + os.sep + filename
            with open(fullFileName, 'rb') as f:
                md5 = hashlib.md5(f.read()).hexdigest()
                item = {
                    'size': os.path.getsize(fullFileName),
                    'name': fullFileName.replace('\\', '/')[len(base)+1:],
                    'md5': md5
                }
                manifest.append(item)
                print(item)

    if not os.path.exists('cache'):
        os.mkdir('cache')
    with open('cache/manifest.json', 'w') as f:
        json.dump(manifest, f)
    return manifest


def main():
    if os.path.exists('cache/manifest.json'):
        with open('cache/manifest.json') as f:
            manifest = json.load(f)
    else:
        manifest = indexManifest()

    data = {
        'packageUrl': packageUrl,
        'version': resVersion,
        'hot': manifest
    }

    with open('cache/warshipgirlsr.manifest.gz', 'wb') as f:
        f.write(gzip.compress(json.dumps(data).encode()))


if __name__ == '__main__':
    main()
