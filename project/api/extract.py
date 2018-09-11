from flask import Flask, request


@app.route('/extract', method['POST'])
def extract():
    if(request.method == 'POST'):
        if