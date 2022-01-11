from flask import Flask, render_template, request
import parseSchedule

app = Flask(__name__, static_url_path='/static')

@app.route('/getInfo' )
def collect_info():

	user = request.args.get("user")
	password = request.args.get("pass")

	phone = request.args.get("phone")
	week  = request.args.get("week")

	file = request.args.get("schedule")


	#basicTwil.send_info(user,password,phone,week)
	#readFile.readSchedule(scooby)

	parseSchedule.mainFunction(user,password,phone,week,file)


	return render_template('success.html')


@app.route('/')
def send_form():
	return render_template('mainPage.html')


if __name__ == '__main__':
	app.run(debug=True)