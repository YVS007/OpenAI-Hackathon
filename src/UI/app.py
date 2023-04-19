from flask import Flask, render_template
import csv
import requests

app = Flask(__name__)

# Define API endpoints
RESOLUTION_API = "http://localhost:5000/api/resolution/"
ROOT_CAUSE_API = "http://localhost:5000/api/root_cause/"

# Define CSV file path
CSV_FILE = "data.csv"

# Define a function to read ticket data from CSV
def read_ticket_data():
    with open(CSV_FILE, "r") as f:
        reader = csv.reader(f)
        tickets = []
        for row in reader:
            ticket = {"id": row[0], "description": row[1]}
            tickets.append(ticket)
        return tickets

# Define a function to call resolution API for a given ticket ID
def get_resolution(ticket_id):
    response = requests.get(RESOLUTION_API + ticket_id)
    if response.status_code == 200:
        return response.json()["resolution"]
    else:
        return "Error retrieving resolution"

# Define a function to call root cause API for a given ticket ID
def get_root_cause(ticket_id):
    response = requests.get(ROOT_CAUSE_API + ticket_id)
    if response.status_code == 200:
        return response.json()["root_cause"]
    else:
        return "Error retrieving root cause"

# Define a Flask route to display the list of tickets
@app.route("/")
def list_tickets():
    tickets = read_ticket_data()
    return render_template("tickets.html", tickets=tickets)

# Define a Flask route to display the dashboard for a selected ticket
@app.route("/ticket/<ticket_id>")
def ticket_dashboard(ticket_id):
    resolution = get_resolution(ticket_id)
    root_cause = get_root_cause(ticket_id)
    return render_template("ticket_dashboard.html", ticket_id=ticket_id, resolution=resolution, root_cause=root_cause)

if __name__ == "__main__":
    app.run(debug=True)
