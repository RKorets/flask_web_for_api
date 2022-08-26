import json

from flask import current_app as app
from flask import request, render_template
import requests as rq
from collections import defaultdict
from .site_parser import load_site_data


@app.route('/')
def index():

    return render_template('index.html')


@app.route('/get', methods=['GET', 'POST'])
def get_data():
    result_dict = defaultdict(list)
    result_dict.clear()
    if request.method == 'POST':
        category = request.form.get('category')
        params = request.form.get('params')
        item_id = request.form.get('id')
        if params is None or params == 'all' and item_id == '':
            get_result = rq.get(url=f'http://127.0.0.1:8000/items/{category}')
            result_dict['result'].append(get_result.json())
            return render_template('get.html', api_answer=result_dict)

        if params is None or params == 'all' and item_id:
            item_id = abs(int(item_id))
            get_result = rq.get(url=f'http://127.0.0.1:8000/items/{category}/{item_id}')
            result_dict['result'].append(get_result.json())
            return render_template('get.html', api_answer=result_dict)

        if params and item_id:
            item_id = abs(int(item_id))
            get_result = rq.get(url=f'http://127.0.0.1:8000/items/{category}/{item_id}/{params}')
            result_dict['result'].append(get_result.json())
            return render_template('get.html', api_answer=result_dict)

    return render_template('get.html', api_answer=result_dict)


@app.route('/post', methods=['GET', 'POST'])
async def post():
    result_dict = defaultdict(list)
    if request.method == 'POST':
        result = await load_site_data(request.form.get('site_category'))
        for item in result.values():
            send_result = rq.post(url='http://127.0.0.1:8000/items', json=item)
            result_dict['result'].append(send_result.json())
    return render_template('post.html', api_answer=result_dict)


@app.route('/put', methods=['GET', 'POST'])
def put():
    result_dict = defaultdict(list)
    if request.method == 'POST':
        price = request.form.get('price')
        name = request.form.get('name')
        item_id = request.form.get('id')
        if item_id.isdigit():
            item_id = abs(int(item_id))
            data = {'id': item_id, 'name': name, 'price': price}
            x = json.dumps(data)
            send_result = rq.put(url=f'http://127.0.0.1:8000/items/{item_id}/put', json=data)
            result_dict['result'].append(send_result.json())

    return render_template('put.html', api_answer=result_dict)


@app.route('/delete', methods=['GET', 'POST'])
def delete():
    result_dict = defaultdict(list)
    if request.method == 'POST':
        item_id = request.form.get('id')
        if item_id.isdigit():
            item_id = abs(int(item_id))
            send_result = rq.delete(url=f'http://127.0.0.1:8000/items/{item_id}/delete')
            result_dict['result'].append(send_result.json())
    return render_template('delete.html', api_answer=result_dict)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404



