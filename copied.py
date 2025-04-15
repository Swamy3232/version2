import datetime
import dash
from app_layout import app  # Import app from layout file
from dash.dependencies import Input, Output, State
import requests
import numpy as np
import plotly.graph_objs as go
from example_getresult import get_oct
import pynvdrive
from pynvdrive.commands.actions import Run, Stop
from app_helpers import save_data_to_db, calculate_band_rms, fetch_base_data,save_data_to_table
from vibration_layout import app
from dash import dcc
from app_layout import app  # Import your layout
from senstivity import set_sensitivity_in_pynvdrive
from average import set_averages_in_pynvdrive
from nooflines import set_lines_in_pynvdrive
from coupling import set_coupling_in_pynvdrive
from samplingrate import set_sampling_rate_in_pynvdrive
from grpah import update_or_clear_plot
from rpm import fetch_and_calculate_defect_frequencies
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
    Output('output-rpm', 'children'),
    Input('show-defect-button', 'n_clicks'),  # Listen to the 'show-defect-button'
    Input("machine-id-dropdown", "value"),
    Input("meas-point-dropdown", "value"),
    State('rpm-input', 'value'),
    prevent_initial_call=True
)
def handle_inputs(n_clicks, selected_machine_id, selected_meas_point, rpm_value):
    messages = []
    
    if n_clicks:
        if not selected_machine_id or not selected_meas_point:
            messages.append("Select a Machine ID and Measurement Point to view defect frequencies.")
        elif not rpm_value:
            messages.append("Please enter an RPM value.")
        else:
            try:
                rpm = float(rpm_value)
                if rpm > 0:
                    messages.append(f"Entered RPM: {rpm_value}")
                    result = fetch_and_calculate_defect_frequencies(selected_machine_id, selected_meas_point, rpm)
                    
                    if isinstance(result, dict):  # If function returns frequencies
                        messages.append("Calculated Defect Frequencies (Hz):")
                        for defect, freq in result.items():
                            messages.append(f"{defect}: {freq} Hz")
                    else:  # If function returns an error message
                        messages.append(result)
                else:
                    messages.append("Please enter a valid positive number for RPM.")
            except ValueError:
                messages.append("Please enter a valid positive number for RPM.")

    return " \n".join(messages)



@app.callback(
    Output('sampling-rate-dropdown', 'value'),
    Input('sampling-rate-dropdown', 'value')
)
def update_sampling_rate(value):
    if value is not None:
        set_sampling_rate_in_pynvdrive(value)
    return value
@app.callback(
    Output('sensitivity-dropdown', 'value'),
    Input('sensitivity-dropdown', 'value')
)
def update_sensitivity(value):
    if value is not None:
        set_sensitivity_in_pynvdrive(value)
    return value
@app.callback(
    Output('averages-dropdown', 'value'),
    Input('averages-dropdown', 'value')
)
def update_averages(value):
    if value is not None:
        set_averages_in_pynvdrive(value)
    return value
@app.callback(
    Output('lines-dropdown', 'value'),
    Input('lines-dropdown', 'value')
)
def update_lines(value):
    if value is not None:
        set_lines_in_pynvdrive(value)
    return value
@app.callback(
    Output('coupling-dropdown', 'value'),
    Input('coupling-dropdown', 'value')
)
def update_coupling(value):
    if value is not None:
        set_coupling_in_pynvdrive(value)
    return value
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


# Global variable to store defect traces
# Global variable to store defect traces
# Global variable to store defect traces
defect_traces = []

@app.callback(
    Output('vibration-graph', 'figure'),
    [
        Input('interval-component', 'n_intervals'),
        Input('clear-button', 'n_clicks'),
        Input('plot-type', 'value'),
        Input('fetch-base-button', 'n_clicks'),
        Input('log-x', 'value'),
        Input('log-y', 'value'),
        Input('type', 'value'),  # Input for type (acceleration, velocity, displacement)
        Input('show-defect-button', 'n_clicks')  # Input for "Show Defect"
    ],
    [
        State('machine-id-dropdown', 'value'), 
        State('meas-point-dropdown', 'value'),
        State('rpm-input', 'value')  # State for RPM input
    ]
)
def vibration_graph_callback(n, clear_clicks, plot_type, fetch_base_clicks, log_x, log_y, selected_type, show_defect_clicks, machine_id, meas_point, rpm_value):
    global frequency, magnitude, base_frequency, base_magnitude, defect_traces
    
    # Call the modified update_or_clear_plot function
    frequency, magnitude, base_frequency, base_magnitude, figure, defect_traces = update_or_clear_plot(
        n, clear_clicks, plot_type, fetch_base_clicks, log_x, log_y, selected_type, machine_id, meas_point,
        frequency, magnitude, base_frequency, base_magnitude, defect_traces
    )

    # Define colors and labels for each defect type
    defect_colors = {
        'outer_race': 'green',
        'inner_race': 'orange',
        'ball_defect': 'purple'
    }

    # Map the defect frequency keys to match the keys in defect_colors
    defect_key_mapping = {
        'Outer Race Frequency': 'outer_race',
        'Inner Race Frequency': 'inner_race',
        'Ball Defect Frequency': 'ball_defect'
    }

    # Handle "Show Defect" button click
    if show_defect_clicks and show_defect_clicks > 0:
        if machine_id and meas_point and rpm_value:
            try:
                rpm = float(rpm_value)
                if rpm > 0:
                    # Fetch defect frequencies
                    defect_frequencies = fetch_and_calculate_defect_frequencies(machine_id, meas_point, rpm)
                    
                    if isinstance(defect_frequencies, dict):  # If function returns frequencies
                        # Debugging: Print the defect frequencies and their types
                        print("Defect Frequencies:", defect_frequencies)
                        print("Defect Types:", defect_frequencies.keys())
                        
                        # Clear existing defect traces
                        defect_traces = []
                        
                        # Add vertical lines for each defect frequency
                        for defect, freq in defect_frequencies.items():
                            if freq > 0:  # Ensure frequency is valid
                                # Map the defect key to match the defect_colors keys
                                mapped_defect = defect_key_mapping.get(defect, defect)
                                # Get the color for the defect type, default to red if not found
                                color = defect_colors.get(mapped_defect, 'red')
                                print(f"Defect: {defect}, Mapped Defect: {mapped_defect}, Frequency: {freq}, Color: {color}")
                                
                                # Create a trace for the defect frequency
                                defect_trace = go.Scatter(
                                    x=[freq, freq],  # Vertical line at the defect frequency
                                    y=[0, max(magnitude) if magnitude else 1],  # Span the entire y-axis
                                    mode='lines',
                                    line=dict(color=color, width=2, dash='dash'),
                                    name=f'{mapped_defect.replace("_", " ").title()} Defect'
                                )
                                # Add the trace to the global defect_traces list
                                defect_traces.append(defect_trace)
            except ValueError:
                pass  # Handle invalid RPM input

    # Update layout for log scale if needed
    figure.update_layout(
        xaxis_type='log' if log_x else 'linear',
        yaxis_type='log' if log_y else 'linear'
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
    Output('measurement-table', 'data'),
    [
        Input('interval-component', 'n_intervals'),
        Input('clear-button', 'n_clicks'),
        Input('save-button', 'n_clicks'),
        Input('run-button', 'n_clicks'),
        Input('fetch-base-button', 'n_clicks')  # Add this input for base data
    ],
    [
        State('machine-id-dropdown', 'value'),
        State('meas-point-dropdown', 'value'),
        State('remarks-point', 'value')
    ]
)
def update_table(n, clear_clicks, save_clicks, run_clicks, fetch_base_clicks, machine_id, meas_point, remarks):
    global frequency, magnitude, base_frequency, base_magnitude, start_time

    # Initialize data list
    data = []

    # Fetch base data if the 'fetch-base-button' is clicked
    if fetch_base_clicks > 0:
        base_frequency, base_magnitude = fetch_base_data(machine_id, meas_point, 'peak')  # Adjust plot_type as needed

    if n > 0 and len(frequency) > 0 and len(magnitude) > 0:
        # Calculate RMS values for current data (overall RMS)
        magnitude = np.concatenate(([magnitude[0]], np.array(magnitude[1:]) / (-2 * np.pi * np.array(frequency[1:]))))

        overall_rms = np.sqrt(np.sum(np.array(magnitude) ** 2) / 1.5)

        # Calculate RMS for each frequency band for current data
        band1_rms = calculate_band_rms(frequency, magnitude, (0, 1000))   # 0-1k Hz
        band2_rms = calculate_band_rms(frequency, magnitude, (1000, 3000)) # 1k-3k Hz
        band3_rms = calculate_band_rms(frequency, magnitude, (3000, 5000)) # 3k-5k Hz
        band4_rms = calculate_band_rms(frequency, magnitude, (5000, 10000)) # 5k-10k Hz

        # Prepare the data for the current measurement
        data.append({
            'machine_id': machine_id,
            'meas_point': meas_point,
            'date': str(start_time.date()) if start_time else 'N/A',
            'band1': f'{band1_rms:.10f}',  # Band 1 RMS
            'band2': f'{band2_rms:.10f}',  # Band 2 RMS
            'band3': f'{band3_rms:.10f}',  # Band 3 RMS
            'band4': f'{band4_rms:.10f}',  # Band 4 RMS
            'overall_rms': f'{overall_rms:.10f}',  # Overall RMS
            'remarks': remarks,  # Remarks
        })
        
        # If base data is available, calculate RMS for base data
        if len(base_frequency) > 0 and len(base_magnitude) > 0:
            base_rms_value = np.sqrt(np.sum(np.array(base_magnitude) ** 2) / 1.5)

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
                'band1': f'{base_band1_rms:.10f}',  # Base Band 1 RMS
                'band2': f'{base_band2_rms:.10f}',  # Base Band 2 RMS
                'band3': f'{base_band3_rms:.10f}',  # Base Band 3 RMS
                'band4': f'{base_band4_rms:.10f}',  # Base Band 4 RMS
                'overall_rms': f'{base_rms_value:.10f}',  # Base RMS
                'remarks': remarks,  # Remarks for base data
            })
            
    # Clear data if the clear button is clicked
    if clear_clicks > 0:
        return []

    return data

@app.callback(
    Output('save-db-button', 'children'),
    Input('save-db-button', 'n_clicks'),
    State('machine-id-dropdown', 'value'),
    State('meas-point-dropdown', 'value'),
    State('base-button', 'n_clicks'),
    State('remarks-point', 'value'),
    State('measurement-table', 'data')  # Capture the table data
)
def save_data(n_clicks, machine_id, meas_point, base_button_clicks, remarks, table_data):
    global start_time

    if n_clicks > 0 and len(table_data) > 0:
        is_base = base_button_clicks > 0  # Determine if base data is selected

        if start_time:  # Ensure valid start time
            # Iterate through the table data and save each row
            for row in table_data:
                # Assuming the table has columns for the frequency bands
                band1 = row.get('band1', 0)
                band2 = row.get('band2', 0)
                band3 = row.get('band3', 0)
                band4 = row.get('band4', 0)

                # Save data to table
                save_data_to_table(machine_id, meas_point, band1, band2, band3, band4, row['overall_rms'], remarks, start_time)
            
            return '✅ Data Saved!'
        else:
            return '⛔ Measurement Not Started Yet'
    return '💾 Save Data'

    


