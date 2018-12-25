from app_files import app

if __name__ == '__main__':
	app.run(debug=False, use_debugger=False)

# To deploy the website, the debug mode needs to be off (debug=False)
# for secure reasons - in case of error thrown, users won`t have error info shown (ie. pahts, code snippets)
