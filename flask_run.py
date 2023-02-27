"""
Flask Run
"""
# .pycを作成しない
import sys
sys.dont_write_bytecode = True

from ProgramFiles.flaskr import app

if __name__ == "__main__":
#	app.run()
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False,
        threaded=True
    )
