from app import app as application
from config import host, port, debug

if __name__ == '__main__':
    application.run(host=host, port=port, debug=debug)

