from flask import Flask, request, render_template_string, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Sprint Management Tools</title>
        <style>
            body {
                font-family: 'Arial', sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 20px;
                color: #333;
            }
            .container {
                background: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                max-width: 800px;
                margin: 20px auto;
            }
            h1, h2 {
                color: #333;
            }
            label {
                margin-top: 10px;
                display: block;
                color: #666;
            }
            input[type="text"], textarea {
                width: calc(100% - 22px);
                padding: 10px;
                margin-top: 5px;
                border: 1px solid #ddd;
                border-radius: 4px;
                box-sizing: border-box;
            }
            input[type="submit"] {
                background-color: #0056b3;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                margin-top: 20px;
            }
            input[type="submit"]:hover {
                background-color: #004494;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Sprint Management Tools</h1>
            <div>
                <h2>Feature A - Calculate Average Velocity</h2>
                <form id="velocityForm">
                    <label for="points">Enter completed points for previous sprints (comma-separated):</label>
                    <input type="text" id="points" name="points">
                    <button type="button" onclick="calculateVelocity()">Calculate Velocity</button>
                </form>
                <div id="velocityResult"style="
                       padding-top: 10px;
                       font-style: oblique;
                       font-weight: bold;">
                </div>
            </div>
            <div>
                <h2>Feature B - Calculate Team Effort-Hour Capacity</h2>
                    <form id="capacityForm">
                        <label for="days">Number of Sprint Days:</label>
                        <input type="text" id="days" name="days"><br>
                        <label for="details">Team Member Details (json format):</label>
                        <textarea id="details" name="details" rows="4" cols="50"></textarea><br><br>
                        <button type="button" onclick="calculateCapacity()">Calculate Capacity</button>
                    </form>
                    <div id="capacityResult" style="
                       padding-top: 10px;
                       font-style: oblique;
                       font-weight: bold;"
                    ></div>
            </div>
        </div>

        <script>
            function calculateVelocity() {
                const points = document.getElementById('points').value.trim();
            
                // Check if the input field is empty and display an error message directly without making a request
                if (!points) {
                    document.getElementById('velocityResult').innerText = 'Error: Please enter some points.';
                    return; // Stop the function from proceeding further
                }
            
                // Preparing the form data to send in the POST request
                const formData = new FormData();
                formData.append('points', points);
            
                fetch('/calculate_velocity', {
                    method: 'POST',
                    body: formData
                }).then(response => response.json())
                .then(data => {
                    if(data.error) {
                        document.getElementById('velocityResult').innerText = 'Error: ' + data.error;
                    } else {
                        document.getElementById('velocityResult').innerText = 'Average Velocity: ' + data.average_velocity;
                    }
                }).catch(error => {
                    console.error('Error:', error);
                    document.getElementById('velocityResult').innerText = 'Failed to calculate velocity. Please try again.';
                });
            }

                                  
            function calculateCapacity() {
                const detailsInput = document.getElementById('details').value;
                let details;
                try {
                    details = JSON.parse(detailsInput);
                } catch(e) {
                    document.getElementById('capacityResult').innerText = 'Error: Invalid JSON format in Team Member Details.';
                    return;
                }

                const days = document.getElementById('days').value;
                if (!days || isNaN(days) || parseInt(days) <= 0) {
                    document.getElementById('capacityResult').innerText = 'Error: Invalid input for Number of Sprint Days.';
                    return;
                }

                fetch('/calculate_capacity', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({days: parseInt(days), details: details})
                }).then(response => response.json())
                .then(data => {
                    if(data.error) {
                        document.getElementById('capacityResult').innerText = 'Error: ' + data.error;
                    } else {
                        document.getElementById('capacityResult').innerText = `Available Effort-Hours/Person: ${data.average_hours_per_person}, Total Available Effort-Hours for Team: ${data.total_hours}`;
                    }
                }).catch(error => {
                    console.error('Error:', error);
                    document.getElementById('capacityResult').innerText = 'Failed to communicate with the server.';
                });
            }
        </script>
    </body>
    </html>
    """)

@app.route('/calculate_velocity', methods=['POST'])
def calculate_velocity():
    try:
        points_str = request.form['points']
        points = list(map(int, points_str.split(',')))  # This might raise ValueError
        if len(points) == 0:  # Check for empty list
            raise ValueError("No points provided.")
        average_velocity = sum(points) / len(points)
        return jsonify({"average_velocity": average_velocity})
    except ValueError as e:  # Catching ValueError specifically for invalid integer conversion
        return jsonify({"error": "Invalid Input"}), 400


@app.route('/calculate_capacity', methods=['POST'])
def calculate_capacity():
    try:
        data = request.get_json(force=True)  # force=True to ensure JSON parsing even with incorrect content-type
        if not data or 'days' not in data or not isinstance(data['days'], int):
            raise ValueError("Invalid or missing 'days'.")
        if 'details' not in data or not all(isinstance(member, dict) for member in data['details']):
            raise ValueError("Invalid or missing 'details'.")

        days = data['days']
        details = data['details']

        if days <= 0:
            raise ValueError("Number of days must be positive.")

        total_hours = 0
        for member in details:
            if not all(key in member for key in ["max_hours", "min_hours", "pto_days", "ceremony_days"]):
                raise ValueError("Missing details for a team member.")
            hours_per_day = (member["max_hours"] + member["min_hours"]) / 2
            available_days = days - (member["pto_days"] + member["ceremony_days"])
            total_hours += available_days * hours_per_day

        if len(details) == 0:
            raise ValueError("Team details cannot be empty.")

        average_hours_per_person = total_hours / len(details)
        return jsonify({
            "average_hours_per_person": average_hours_per_person,
            "total_hours": total_hours
        })
    except (ValueError, TypeError) as e:
        return jsonify({"error": "Invalid Input"}), 400

    
if __name__ == '__main__':
    app.run(debug=True)