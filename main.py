from flask import Flask, render_template_string, request
from datetime import datetime
import pytz

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def display_times():
    # Define the time zones
    gmt_plus_3 = pytz.timezone('Etc/GMT-3')
    est = pytz.timezone('US/Eastern')
    pst = pytz.timezone('US/Pacific')

    # Initialize variables for displaying times
    local_time_str = est_time_str = pst_time_str = ""
    converted_local_time_str = converted_est_time_str = converted_pst_time_str = ""
    input_date_str = input_time_str = ""

    # Get the current time in GMT+3
    current_time = datetime.now(gmt_plus_3)
    local_time_str = current_time.strftime('%Y-%m-%d %H:%M:%S')
    est_time_str = current_time.astimezone(est).strftime('%Y-%m-%d %H:%M:%S')
    pst_time_str = current_time.astimezone(pst).strftime('%Y-%m-%d %H:%M:%S')

    if request.method == 'POST':
        # Get user input
        input_date_str = request.form.get('input_date')
        input_time_str = request.form.get('input_time')
        input_zone = request.form.get('input_zone')

        # Parse the input date and time
        try:
            input_datetime_str = f"{input_date_str} {input_time_str}"
            input_time = datetime.strptime(input_datetime_str, '%Y-%m-%d %H:%M')
            if input_zone == 'GMT+3':
                input_time = gmt_plus_3.localize(input_time)
            elif input_zone == 'EST':
                input_time = est.localize(input_time)
            elif input_zone == 'PST':
                input_time = pst.localize(input_time)

            # Convert to other time zones
            converted_local_time_str = input_time.astimezone(gmt_plus_3).strftime('%Y-%m-%d %H:%M:%S')
            converted_est_time_str = input_time.astimezone(est).strftime('%Y-%m-%d %H:%M:%S')
            converted_pst_time_str = input_time.astimezone(pst).strftime('%Y-%m-%d %H:%M:%S')

        except ValueError:
            input_date_str = "Invalid date or time format."

    # HTML template with CSS styling
    html_template = """
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Maluni's Real Time Converter</title>
        <style>
          body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 0;
            background: linear-gradient(to bottom, black 33%, red 33%, red 66%, green 66%);
            color: white;
            text-align: center;
          }
          header {
            background-color: white;
            color: black;
            padding: 1em 0;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
          }
          main {
            padding: 20px;
            max-width: 600px;
            margin: 20px auto;
            background-color: rgba(255, 255, 255, 0.9);
            color: black;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
          }
          h1, h2 {
            margin: 0.5em 0;
          }
          ul {
            list-style-type: none;
            padding: 0;
          }
          li {
            padding: 5px 0;
          }
          form {
            margin-top: 20px;
          }
          label, input, select {
            display: block;
            margin: 10px 0;
            text-align: left;
          }
          input[type="date"], input[type="time"], select {
            width: 100%;
            padding: 8px;
            box-sizing: border-box;
            border: 1px solid #ccc;
            border-radius: 4px;
          }
          input[type="submit"] {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 10px;
            cursor: pointer;
            border-radius: 4px;
            width: 100%;
          }
          input[type="submit"]:hover {
            background-color: #45a049;
          }
          footer {
            margin-top: 20px;
            font-size: 0.8em;
            color: #ccc;
          }
        </style>
      </head>
      <body>
        <header>
          <h1>Maluni's Real Time Converter</h1>
        </header>
        <main>
          <h2>Current Times</h2>
          <ul>
            <li>Local Time (GMT+3): {{ local_time }}</li>
            <li>Eastern Standard Time (EST): {{ est_time }}</li>
            <li>Pacific Standard Time (PST): {{ pst_time }}</li>
          </ul>
          <h2>Convert Time</h2>
          <form method="post">
            <label for="input_date">Select Date:</label>
            <input type="date" id="input_date" name="input_date" required>
            <label for="input_time">Select Time:</label>
            <input type="time" id="input_time" name="input_time" required>
            <label for="input_zone">Select Time Zone:</label>
            <select id="input_zone" name="input_zone">
              <option value="GMT+3">GMT+3</option>
              <option value="EST">EST</option>
              <option value="PST">PST</option>
            </select>
            <input type="submit" value="Convert">
          </form>
          {% if converted_local_time_str %}
          <h2>Converted Times</h2>
          <ul>
            <li>Converted Local Time (GMT+3): {{ converted_local_time_str }}</li>
            <li>Converted Eastern Standard Time (EST): {{ converted_est_time_str }}</li>
            <li>Converted Pacific Standard Time (PST): {{ converted_pst_time_str }}</li>
          </ul>
          {% endif %}
        </main>
        <footer>
          &copy; malunicreations2025
        </footer>
      </body>
    </html>
    """

    return render_template_string(html_template, 
                                  local_time=local_time_str, 
                                  est_time=est_time_str, 
                                  pst_time=pst_time_str, 
                                  input_date=input_date_str,
                                  input_time=input_time_str,
                                  converted_local_time_str=converted_local_time_str,
                                  converted_est_time_str=converted_est_time_str,
                                  converted_pst_time_str=converted_pst_time_str)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
  #app.run(host='0.0.0.0', port=8080)