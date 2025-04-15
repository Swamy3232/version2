import os
import h5py
import numpy as np
import pandas as pd
import pynvdrive
from pynvdrive.commands.actions import Run, Stop
import datetime
from projectcbm.vibration_layout import app  # Import app from layout
# from l import   # Import TestLayout class from l.py
from dash.dependencies import Input, Output, State
from projectcbm.example_getresult import get_oct
import plotly.graph_objs as go
import dash 
from dash import dcc, html, Output, Input, State
import psycopg2
import json
import requests
import dash_core_components as dcc


client = None
frequency = []
magnitude = []
base_frequency = []
base_magnitude = []
samplingrate = None
start_time = None

@app.callback(
    Output("machine-id-dropdown", "options"),
    Input("page-load-trigger", "n_intervals")  # Triggers once when the page loads
)
def load_machine_ids(_):
    print("load_machine_ids accessed")  # Debugging
    try:
        response = requests.get("http://127.0.0.1:8000/machine_ids/", timeout=5)
        print("API Response for Machine IDs:", response.text)  # Debugging
        if response.status_code == 200:
            data = response.json()
            return [{"label": mid, "value": mid} for mid in data.get("machine_ids", [])]
    except requests.exceptions.RequestException as e:
        print("Error loading machine IDs:", e)
    return []
@app.callback(
    Output('filename-input-container', 'style'),
    Input('save-excel-button', 'n_clicks')
)
def toggle_filename_input(n_clicks):
    if n_clicks > 0:
        return {'display': 'block'}  # Show the input container when the button is clicked
    return {'display': 'none'}  # Keep the input container hidden initially
@app.callback(
    Output("meas-point-dropdown", "options"),
    Input("machine-id-dropdown", "value")
)
def load_meas_points(selected_machine_id):
    print("load_meas_points accessed with:", selected_machine_id)  # Debugging
    if not selected_machine_id:
        return []
    
    url = f"http://127.0.0.1:8000/measurement-points/{selected_machine_id}/"
   
    try:
        response = requests.get(url, timeout=5)
        print("API Response for Measurement Points:", response.text)  # Debugging
        if response.status_code == 200:
            data = response.json()
            return [{"label": mp, "value": mp} for mp in data]

    except requests.exceptions.RequestException as e:
        print("Error loading measurement points:", e)
    return []

@app.callback(
    [
        Output('interval-component', 'disabled'),
        Output('status-indicator', 'children'),
        Output('sampling-rate-display', 'children')
    ],
    [
        Input('run-button', 'n_clicks'),
        Input('stop-button', 'n_clicks')
    ]
)
def start_stop_measurement(run_clicks, stop_clicks):
    global client, frequency, magnitude, samplingrate, start_time

    ctx = dash.callback_context
    if not ctx.triggered:
        return True, "⏸️ Stopped", "Range: N/A"

    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == 'run-button':
        if client is None:
            client = pynvdrive.Client()
            client.__enter__()
        client.send_command(Run())

        start_time = datetime.datetime.now()

        return False, "✅ Measurement Running...", "Range: N/A"

    if button_id == 'stop-button':
        if client:
            client.send_command(Stop())
            client.__exit__(None, None, None)
            client = None

        if frequency and magnitude:
            frequency, magnitude, samplingrate = get_oct()
            sampling_rate_display = f"Range: {samplingrate:.2f} Hz"
        else:
            sampling_rate_display = "Range: N/A"

        return True, "⏹️ Measurement Stopped", sampling_rate_display

@app.callback(
    Output('vibration-graph', 'figure'),
    [
        Input('interval-component', 'n_intervals'),
        Input('clear-button', 'n_clicks'),
        Input('plot-type', 'value'),
        Input('fetch-base-button', 'n_clicks'),
        Input('log-x', 'value'),  # Log X input
        Input('log-y', 'value')   # Log Y input
    ],
    [State('machine-id-dropdown', 'value'), State('meas-point-dropdown', 'value')]
)
def update_or_clear_plot(n, clear_clicks, plot_type, fetch_base_clicks, log_x, log_y, machine_id, meas_point):
    global frequency, magnitude, samplingrate, base_frequency, base_magnitude

    ctx = dash.callback_context

   
    if clear_clicks > 0:
        frequency = []
        magnitude = []
        base_frequency = []
        base_magnitude = []
        return go.Figure()

   
    if 'fetch-base-button' in [ctx.triggered_id]:
        base_frequency, base_magnitude = fetch_base_data(machine_id, meas_point, plot_type)


    if n > 0:
        frequency, magnitude, samplingrate = get_oct()


    rms_value = np.sqrt(np.sum(np.array(magnitude) ** 2) / 1.5)
    base_rms_value = np.sqrt(np.sum(np.array(base_magnitude) ** 2) / 1.5) if len(base_magnitude) > 0 else 0

   
    original_magnitude = np.array(magnitude)
    original_base_magnitude = np.array(base_magnitude)

    if plot_type == 'peak':
        magnitude = original_magnitude * np.sqrt(2)
        base_magnitude = original_base_magnitude * np.sqrt(2)
    elif plot_type == 'ptp':
        magnitude = original_magnitude * 2 * np.sqrt(2)
        base_magnitude = original_base_magnitude * 2 * np.sqrt(2)

    # Create the plot
    figure = go.Figure()

    # Plot base data if available and only if it's fetched
    if len(base_frequency) > 0 and len(base_magnitude) > 0:
        figure.add_trace(go.Scatter(x=base_frequency, y=base_magnitude, mode='lines', name='Base Data', line=dict(color='red', width=2)))

    # Plot actual data
    if len(frequency) > 0 and len(magnitude) > 0:
        figure.add_trace(go.Scatter(x=frequency, y=magnitude, mode='lines', name='Vibration', line=dict(color='#3498DB', width=2)))

    # Apply log scaling if selected
    if log_x:
        figure.update_xaxes(type="log")
    if log_y:
        figure.update_yaxes(type="log")

    # Update layout
    figure.update_layout(
        title='📈 Vibration Data',
        xaxis_title='Frequency (Hz)',
        yaxis_title='Magnitude',
        plot_bgcolor='#F5F5F5',
        hovermode='x unified',
        hoverlabel=dict(
            bgcolor="white",
            font_size=16,
            font_family="Rockwell"
        ),
        annotations=[ 
            dict(
                x=1,
                y=1,
                xref='paper', 
                yref='paper',
                text=f'RMS = {rms_value:.2f}',
                showarrow=False,
                font=dict(size=16, color='black'),
                align='right',
                bgcolor='rgba(255, 255, 255, 0.7)',
                borderpad=4,
                bordercolor='black',
                borderwidth=1
            ),
            dict(
                x=1,
                y=0.9,
                xref='paper',
                yref='paper',
                text=f'Base RMS = {base_rms_value:.2f}' if len(base_magnitude) > 0 else '',
                showarrow=False,
                font=dict(size=16, color='black'),
                align='right',
                bgcolor='rgba(255, 255, 255, 0.7)',
                borderpad=4,
                bordercolor='black',
                borderwidth=1
            )
        ]
    )

    return figure

@app.callback(
    Output(dcc.Location(id='url', refresh=True), 'href'),
    [Input("refresh-button", "n_clicks")]
)
def refresh_page(n_clicks):
    if n_clicks > 0:
        return '/'  # This will trigger the page to refresh to the root URL
    return dash.no_update

def fetch_base_data(machine_id, meas_point, plot_type):
    try:
        url = f"http://localhost:8000/vibration_values/base/{machine_id}/{meas_point}/"
        print("Requesting URL:", url)  # Debug print
        
        response = requests.get(url)
        print("API Response Status Code:", response.status_code)  # Debug print
        print("Raw API Response:", response.text)  # Debug print
        
        if response.status_code == 200:
            data = response.json()
            vibration_values = data.get("vibration_values", [])
            
            if not vibration_values:
                print("No vibration values found.")  # Debug print
                return [], []

            # Extract frequency and magnitude from vibration values
            frequency = [entry["frequency"] for entry in vibration_values]
            magnitude = [entry["vibration_value"] for entry in vibration_values]
            
            print("Extracted Frequency:", frequency)  
            print("Extracted Magnitude:", magnitude)  

            # Apply transformations based on selected plot type
            if plot_type == 'peak':
                magnitude = np.array(magnitude) * np.sqrt(2)
            elif plot_type == 'ptp':
                magnitude = np.array(magnitude) * 2 * np.sqrt(2)
            
            return frequency, magnitude
        else:
            print("Error: API returned status", response.status_code)
    
    except Exception as e:
        print(f"Error fetching base data: {e}")

    return [], []
def save_data_to_db(machine_id,meas_point, magnitude, frequency, is_base, start_time,remarks):
    conn = psycopg2.connect(
        dbname="vb_data",
        user="postgres",
        password="1234",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()

    current_date = start_time.date()
    current_time = start_time.strftime('%H:%M:%S')  # Format time without fractional seconds
    base_value = 'BASE' if is_base else None

    # Convert magnitude and frequency to native Python float types
    magnitude = [float(mag) for mag in magnitude]
    frequency = [float(freq) for freq in frequency]

    for mag, freq in zip(magnitude, frequency):
        cursor.execute(''' 
            INSERT INTO data (machine_id,date, vibration_value, meas_point, base, time, frequency,remarks)
            VALUES (%s, %s, %s, %s, %s, %s, %s,%s)
        ''', (machine_id,  current_date, mag, meas_point, base_value, current_time, freq,remarks))

    conn.commit()
    cursor.close()
    conn.close()
    # return machine_id,,current_date,meas_point,mag,freq
# Callback to save data
@app.callback(
    Output('save-button', 'children'),
    Input('save-button', 'n_clicks'),
    State('machine-id-dropdown', 'value'),
    State('meas-point-dropdown', 'value'),
    State('base-button', 'n_clicks'),
    State('remarks-point','value'),
)
def save_data(n_clicks, machine_id,  meas_point, base_button_clicks, remarks):
    global start_time

    if n_clicks > 0 and len(frequency) > 0 and len(magnitude) > 0:
        is_base = base_button_clicks > 0  # Determine if base data is selected

        if start_time:  # Ensure valid start time
            save_data_to_db(machine_id,  meas_point, magnitude, frequency, is_base, start_time, remarks)
            return '✅ Data Saved!'
        else:
            return '⛔ Measurement Not Started Yet'
    return '💾 Save Data'
@app.callback(
    Output("download-excel", "data"),
    Input("save-excel-button", "n_clicks"),
    State("filename-input", "value"),
    State("machine-id-dropdown", "value"),
    State("meas-point-dropdown", "value"),
    prevent_initial_call=True
)
def save_to_excel(n_clicks, filename, machine_id, meas_point):
    global frequency, magnitude

    if len(frequency) == 0 or len(magnitude) == 0:
        print("No data to save!")
        return None  # Do nothing if there's no data

    if not filename:
        print("No filename provided!")
        return None  # Ensure filename is provided

    # Calculate overall RMS
    overall_rms = np.sqrt(np.sum(np.array(magnitude) ** 2) / 1.5)

    # Debugging
    print(f"Saving data for - {machine_id} - {meas_point}")
    print(f"Filename: {filename}")
    print(f"Overall RMS: {overall_rms:.4f}")

    # Create DataFrame
    df = pd.DataFrame({
        "Machine ID": [machine_id] * len(frequency),
        "Measurement Point": [meas_point] * len(frequency),
        "Frequency (Hz)": frequency,
        "Magnitude": magnitude
    })

    # Append overall RMS as a separate row
    df = pd.concat([df, pd.DataFrame({
        "Machine ID": ["Overall RMS"],
        "Measurement Point": [""],
        "Frequency (Hz)": [""],
        "Magnitude": [overall_rms]
    })], ignore_index=True)

    # Save in Downloads folder
    downloads_path = os.path.expanduser("~/Downloads")
    file_path = os.path.join(downloads_path, f"{filename}.xlsx")
    print(f"File path: {file_path}")

    try:
        df.to_excel(file_path, index=False)
        print(f"File saved successfully at {file_path}")
    except Exception as e:
        print(f"Error saving file: {e}")
        return None

    return dcc.send_file(file_path)


def calculate_band_rms(frequency, magnitude, band_range):
    frequency = np.array(frequency)
    magnitude = np.array(magnitude)
    band_indices = np.where((frequency >= band_range[0]) & (frequency < band_range[1]))[0]
    if len(band_indices) == 0:
        return 0
    band_magnitude = magnitude[band_indices]
    return np.sqrt(np.sum(band_magnitude ** 2) / 1.5)

# Callback to update the table and show RMS values
@app.callback(
    Output('measurement-table', 'data'),
    [
        Input('interval-component', 'n_intervals'),
        Input('clear-button', 'n_clicks'),
        Input('save-button', 'n_clicks'),
        Input('run-button', 'n_clicks'),
        Input('fetch-base-button', 'n_clicks')  # Add this input for base data
    ],
    [State('machine-id-dropdown', 'value'),State('meas-point-dropdown', 'value'),State('remarks-point', 'value')]
)
def update_table(n, clear_clicks, save_clicks, run_clicks, fetch_base_clicks, machine_id,meas_point,remarks):
    global frequency, magnitude, base_frequency, base_magnitude, start_time

    # remarks = ''  # Default remarks value (empty)

    # Fetch base data if the 'fetch-base-button' is clicked
    if fetch_base_clicks > 0:
        base_frequency, base_magnitude = fetch_base_data(machine_id, meas_point, 'peak')  # Change plot_type if needed

    data = []

    if n > 0 and len(frequency) > 0 and len(magnitude) > 0:
        # Calculate RMS values for current data (overall RMS)
        overall_rms = np.sqrt(np.sum(np.array(magnitude) ** 2) / 1.5)

        # Calculate RMS for each frequency band for current data
        band1_rms = calculate_band_rms(frequency, magnitude, (0, 1000))   # 0-1k Hz
        band2_rms = calculate_band_rms(frequency, magnitude, (1000, 3000)) # 1k-3k Hz
        band3_rms = calculate_band_rms(frequency, magnitude, (3000, 5000)) # 3k-5k Hz
        band4_rms = calculate_band_rms(frequency, magnitude, (5000, 10000)) # 5k-10k Hz

        # Prepare the data for the current measurement
        data.append({
            'machine_id': machine_id,
            # '': ,
            'meas_point': meas_point,
            'date': str(start_time.date()) if start_time else 'N/A',
            'band1': f'{band1_rms:.2f}',  # Band 1 RMS
            'band2': f'{band2_rms:.2f}',  # Band 2 RMS
            'band3': f'{band3_rms:.2f}',  # Band 3 RMS
            'band4': f'{band4_rms:.2f}',  # Band 4 RMS
            'overall_rms': f'{overall_rms:.2f}',  # Overall RMS
            'remarks': remarks,  # Empty or default remarks
        })
        
        # If base data is available, calculate RMS for base data
        if n > 0 and len(base_frequency) > 0 and len(base_magnitude) > 0:
            # Calculate base RMS using the provided formula
            base_rms_value = np.sqrt(np.sum(np.array(base_magnitude) ** 2) / 1.5)
            base_rms_value = np.sqrt(np.sum(np.array(base_magnitude) ** 2) / 1.5) if len(base_magnitude) > 0 else 0

            # Calculate RMS for each frequency band for base data
            base_band1_rms = calculate_band_rms(base_frequency, base_magnitude, (0, 1000))   # 0-1k Hz
            base_band2_rms = calculate_band_rms(base_frequency, base_magnitude, (1000, 3000)) # 1k-3k Hz
            base_band3_rms = calculate_band_rms(base_frequency, base_magnitude, (3000, 5000)) # 3k-5k Hz
            base_band4_rms = calculate_band_rms(base_frequency, base_magnitude, (5000, 10000)) # 5k-10k Hz

            # Append base data to the table
            data.append({
                'machine_id': machine_id,
                
                'meas_point': meas_point,
                'date': 'Base Data',  # Differentiate the base data
                'band1': f'{base_band1_rms:.2f}',  # Base Band 1 RMS
                'band2': f'{base_band2_rms:.2f}',  # Base Band 2 RMS
                'band3': f'{base_band3_rms:.2f}',  # Base Band 3 RMS
                'band4': f'{base_band4_rms:.2f}',  # Base Band 4 RMS
                'overall_rms': f'{base_rms_value:.2f}',  # Base RMS
                'remarks':remarks,  # Empty or default remarks
            })
        return data
    # Clear data if the clear button is clicked
    if clear_clicks > 0:
        return []

    # Return data for the actual and base data
    return data
    

if __name__ == '__main__':
    
    app.run_server(debug=True)




