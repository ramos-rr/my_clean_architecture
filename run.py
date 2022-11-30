from src.main.configs import app
from config import set_up_before_run


if __name__ == "__main__":
    set_up_before_run()
    app.run(host="0.0.0.0", debug=True)
