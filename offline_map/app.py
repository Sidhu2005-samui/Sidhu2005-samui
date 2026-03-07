from flask import Flask, render_template, send_file, abort
import sqlite3
import os
import io

app = Flask(__name__)

MBTILES_PATH = os.path.join(os.path.dirname(__file__), 'data', 'map.mbtiles')

def get_tile(z, x, y):
    # MBTiles uses TMS coordinates (origin is bottom-left)
    # Leaflet/OSM uses XYZ coordinates (origin is top-left)
    # Conversion: tms_y = (2**z - 1) - xyz_y
    tms_y = (2**z - 1) - y

    try:
        with sqlite3.connect(MBTILES_PATH) as conn:
            c = conn.cursor()
            c.execute('SELECT tile_data FROM tiles WHERE zoom_level=? AND tile_column=? AND tile_row=?', (z, x, tms_y))
            row = c.fetchone()
            if row:
                return row[0]
            else:
                return None
    except Exception as e:
        print(f"Error reading tile: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tiles/<int:z>/<int:x>/<int:y>.png')
def serve_tile(z, x, y):
    tile_data = get_tile(z, x, y)
    if tile_data:
        return send_file(io.BytesIO(tile_data), mimetype='image/png')
    else:
        # Return a transparent 1x1 png if tile not found to avoid 404s in leaflet
        return abort(404)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
