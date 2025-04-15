import requests
from dash.dependencies import Input, Output, State
from projectcbm.app_helpers import save_data_to_db
from projectcbm.vibration_layout import app

@app.callback(
    Output("machine-id-dropdown", "options"),
    Input("page-load-trigger", "n_intervals")
)
def load_machine_ids(_):
    try:
        response = requests.get("http://127.0.0.1:8000/machine_ids/", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return [{"label": mid, "value": mid} for mid in data.get("machine_ids", [])]
    except requests.exceptions.RequestException as e:
        print("Error loading machine IDs:", e)
    return []

@app.callback(
    Output("meas-point-dropdown", "options"),
    Input("machine-id-dropdown", "value")
)
def load_meas_points(selected_machine_id):
    if not selected_machine_id:
        return []
    
    url = f"http://127.0.0.1:8000/measurement-points/{selected_machine_id}/"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return [{"label": mp, "value": mp} for mp in data]
    except requests.exceptions.RequestException as e:
        print("Error loading measurement points:", e)
    return []
