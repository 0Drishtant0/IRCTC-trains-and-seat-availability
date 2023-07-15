from flask import Flask, render_template, request
import requests

app = Flask(__name__)
from_station = ''
to_station = ''

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/trains', methods=['POST'])
def get_trains():
    global from_station, to_station

    from_station = request.form.get('from_station')
    to_station = request.form.get('to_station')
    journey_date = request.form.get('journey_date')

    url = "https://irctc1.p.rapidapi.com/api/v3/trainBetweenStations"
    headers = {
        "X-RapidAPI-Key": "caa058f2e1msh86e6f3a46b24d83p119562jsnaaaf563c5b0a",
        "X-RapidAPI-Host": "irctc1.p.rapidapi.com"
    }
    querystring = {
        "fromStationCode": from_station,
        "toStationCode": to_station,
        "dateOfJourney": journey_date
    }

    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()

    if response.status_code == 200 and data.get('status') and data.get('data'):
        trains = data['data']
        return render_template('trains.html', trains=trains)
    else:
        error_message = "No direct trains available for the given stations and date."
        return render_template('error.html', error_message=error_message)

@app.route('/seat_availability', methods=['POST'])
def get_seat_availability():
    global from_station, to_station

    train_number = request.form.get('train_number')
    class_type = request.form.get('class_type')
    journey_date = request.form.get('journey_date')

    url = "https://irctc1.p.rapidapi.com/api/v1/checkSeatAvailability"
    headers = {
        "X-RapidAPI-Key": "caa058f2e1msh86e6f3a46b24d83p119562jsnaaaf563c5b0a",
        "X-RapidAPI-Host": "irctc1.p.rapidapi.com"
    }
    querystring = {
        "classType": class_type,
        "fromStationCode": from_station,
        "quota": "GN",
        "toStationCode": to_station,
        "trainNo": train_number,
        "date": journey_date
    }

    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()

    if response.status_code == 200 and data.get('status') and data.get('data'):
        availability = data['data']['current_status']
        fare = data['data']['total_fare']
        return render_template('seat_availability.html', availability=availability, fare=fare)
    else:
        error_message = "Seat availability not found for the selected train and date."
        return render_template('error.html', error_message=error_message)

if __name__ == '__main__':
    app.run(debug=True)
