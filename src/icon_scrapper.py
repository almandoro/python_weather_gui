import requests
import time


MIN = 1
MAX = 36
SPECIAL_IMAGES = [21, 22, 23, 24, 25]

for i in range(MIN, MAX + 1):
    suffix = "a" if i in SPECIAL_IMAGES else ''
    url = f'https://worldweather.wmo.int/images/{i}{suffix}.png'
    file_destination = f'icons/icon_{i}{suffix}.png'

    try:
        t0 = time.time()
        response = requests.get(url)
        print(f'Downloading... {url} --> {file_destination}')
        with open(f'icons/icon_{i}{suffix}.png', 'wb') as f:
            f.write(response.content)

        t1 = time.time()

        total = format(t1 - t0, '.2f')

        print(f'Done! {total}ms\n')
    except:
        print('Error during downloading!!')
