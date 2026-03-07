import sqlite3
import urllib.request
import os

def create_mbtiles(filepath):
    conn = sqlite3.connect(filepath)
    c = conn.cursor()
    c.execute('CREATE TABLE metadata (name text, value text)')
    c.execute('CREATE TABLE tiles (zoom_level integer, tile_column integer, tile_row integer, tile_data blob)')

    metadata = [
        ('name', 'Offline Map'),
        ('type', 'baselayer'),
        ('version', '1.1'),
        ('description', 'A small sample of map tiles'),
        ('format', 'png')
    ]
    c.executemany('INSERT INTO metadata VALUES (?, ?)', metadata)

    # Download zoom 0 and 1
    tiles_to_download = [
        (0, 0, 0),
        (1, 0, 0),
        (1, 1, 0),
        (1, 0, 1),
        (1, 1, 1)
    ]

    headers = {'User-Agent': 'AvaOfflineMapApp/1.0'}

    for z, x, y in tiles_to_download:
        tms_y = (2**z - 1) - y

        url = f"https://tile.openstreetmap.org/{z}/{x}/{y}.png"
        print(f"Downloading {url}...")
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req) as response:
                if response.status == 200:
                    c.execute('INSERT INTO tiles VALUES (?, ?, ?, ?)', (z, x, tms_y, response.read()))
                else:
                    print(f"Failed to download {url}: {response.status}")
        except Exception as e:
            print(f"Error downloading {url}: {e}")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    mbtiles_path = os.path.join(os.path.dirname(__file__), 'map.mbtiles')
    if not os.path.exists(mbtiles_path):
        create_mbtiles(mbtiles_path)
        print(f"Created {mbtiles_path}")
    else:
        print(f"{mbtiles_path} already exists")
