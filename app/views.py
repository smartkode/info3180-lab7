"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/

This file creates your application.
"""


from flask import Flask, jsonify, abort, request, make_response, url_for
from app import app
import requests
from bs4 import BeautifulSoup
import urlparse


@app.route('/api/thumbnail/process', methods=['POST'])
def process():
    url = request.form['url']
    data = requests.get(url)
    soup = BeautifulSoup(data.text, 'html.parser')

    links = []
    og_image = (soup.find('meta', property='og:image') or
                        soup.find('meta', attrs={'name': 'og:image'}))
    if og_image and og_image['content']:
        links.append(og_image['content'])
        print og_image['content']

    thumbnail_spec = soup.find('link', rel='image_src')
    if thumbnail_spec and thumbnail_spec['href']:
        links.append(thumbnail_spec['href'])
        print thumbnail_spec['href']

    for img in soup.find_all("img", class_="a-dynamic-image", src=True):
        if "sprite" not in img["src"]:
            links.append(urlparse.urljoin(url, img["src"]))
            print urlparse.urljoin(url, img["src"])

    response = jsonify({'error': '1', 'data':'', 'message':'Unable to extract thumbnails'})

    if len(links)>0:
        response = jsonify({'error': 'null', 'data': {'thumbnails': links }, 'message':'success'})
    return response

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8080)
