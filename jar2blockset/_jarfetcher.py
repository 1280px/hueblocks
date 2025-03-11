import os
import sys

import requests
# import wget

PISTON_META_URL = 'https://piston-meta.mojang.com/mc/game/version_manifest.json'


if __name__ == "__main__":
    OUTPUT_DIR = sys.argv[1] if len(sys.argv) >= 2 else '.'

versions_res = requests.get(PISTON_META_URL)
if not versions_res.ok:
    print('Unable to dl versions manifest! Errcode:', versions_res.status_code)
    sys.exit(1)
versions_data = versions_res.json()

# First we need to find the needed versions in manifest data
version_latest = versions_data['latest']['release']
version_latest_info = list(
    filter(lambda a: a['id'] == version_latest, versions_data['versions'])
)[0]
version_lastPA_info = list(
    filter(lambda a: a['id'] == '1.13.2', versions_data['versions'])
)[0]

# Now, for each version, get their JSON metadata, and from there
# get JAR files links, which we download in a given output dir
for version_meta_url in [version_latest_info['url'], version_lastPA_info['url']]:
    version_meta_res = requests.get(version_meta_url)
    if not version_meta_res.ok:
        print('Unable to dl version JSON! Errcode:', version_meta_res.status_code)
        sys.exit(1)
    version_meta_data = version_meta_res.json()

    version_name = f'Minecraft {version_meta_data["id"]}.jar'
    version_url = version_meta_data['downloads']['client']['url']
    version_size = version_meta_data['downloads']['client']['size']
    downloaded_size = 0

    version_res = requests.get(version_url, stream=True)
    if not version_meta_res.ok:
        print('Unable to dl version JAR! Errcode:', version_meta_res.status_code)
        sys.exit(1)
    print(version_url)

    os.makedirs(OUTPUT_DIR, exist_ok=True) # In case OUTPUT_DIR doesn't exist yet
    with open(
            os.path.join(OUTPUT_DIR, version_name),
        mode='wb') as version_f:
        for c in version_res.iter_content(chunk_size=1024*1024):
            version_f.write(c)

            downloaded_size += 1024*1024
            print(f'{version_name} :: {(downloaded_size / version_size)*100} %')
        print('')

print('JARs downloaded successfully!')
sys.exit(0)
