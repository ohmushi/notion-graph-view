from flask import Flask, request, send_file, render_template
import os
import datetime
import hashlib
from notion_graph import Parser, NOTION_VERSION

app = Flask(__name__)

DEFAULT_TTL_MINUTES = 60
CACHE_DIR = '/tmp/graphs_cache'

if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

def get_cache_path(page, token):
    unique_string = f"{page}_{token}"
    hash_string = hashlib.md5(unique_string.encode()).hexdigest()
    return os.path.join(CACHE_DIR, f"graph_{hash_string}.html")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate')
def generate():
    token = request.args.get('token', '')
    page = request.args.get('page', '')
    ttl = int(request.args.get('ttl', DEFAULT_TTL_MINUTES))
    
    if not token or not page:
        return 'Missing token or page parameter', 400

    cache_path = get_cache_path(page, token)

    if os.path.exists(cache_path):
        file_mod_time = datetime.datetime.fromtimestamp(os.path.getmtime(cache_path))
        delta_last_generated = datetime.datetime.now() - file_mod_time
        print(f"last generated : {delta_last_generated}\nttl : {ttl_datetime}")
        ttl_datetime = datetime.timedelta(minutes=ttl)
        if delta_last_generated < ttl_datetime:
            return send_file(cache_path)

    parser = Parser(NOTION_VERSION, token)
    parser.parse(page)
    parser.export_to_html(cache_path)

    return send_file(cache_path)

if __name__ == '__main__':
    app.run(debug=True)
