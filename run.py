from app import create_app

#
# app = create_app()
# app.run(debug=True)
if __name__ == '__main__':
    app = create_app()
    app.run(host='vps54480.hyperhost.name', port=5000, debug=False)
