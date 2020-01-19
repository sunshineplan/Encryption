#!/usr/bin/python3
# -*- coding: utf-8 -*-

from flask import Flask, jsonify, render_template, request

from core import decrypt, encrypt

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/do', methods=['POST'])
def encryption():
    mode = request.form.get('mode')
    key = request.form.get('key')
    content = request.form.get('content')
    if mode == 'encrypt':
        return jsonify(result=encrypt(key, content))
    elif mode == 'decrypt':
        if (dc := decrypt(key, content)):
            return jsonify(result=dc)
        else:
            return jsonify(result=None)
    else:
        return jsonify(result=None)


if __name__ == '__main__':
    app.run()
