from app import create_app

app = create_app()

if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.INFO)
    
    app.run(host='0.0.0.0', port=9000, debug=True)