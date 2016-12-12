from wikidataviz import app, cache
if __name__ == '__main__':
    with app.app_context():
        cache.clear()

    app.run(host='0.0.0.0', port=5001, debug=True)
