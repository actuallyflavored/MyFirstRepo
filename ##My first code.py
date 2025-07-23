import wfdb
import numpy as np
import matplotlib.pyplot as plt

#Define the record name
#This assumes .dat and .atr are in the same directory
record_name = '419'

print(f"Attempting to read EKG data and annotations for record: {record_name}")

try:
    #1. Read the EKG signal data and header information (.data and .hea files)
    #'records' will contain EKG signal as Numpy array.
    #'fields' will contain a dictionary of header information
    record, fields = wfdb.rdsamp(record_name)

    #2. Read the annotations (.atr file)
    #'annotation' will be a wfdb.Annotation object containing details about the beats
    annotation = wfdb.rdann(record_name, 'atr')

    print("\nSuccessfully loaded EKG signal data and annotations")
    print(f"Data type of 'record' (signal data): {type(record)}")
    print(f"Shape of the EKG signal data (samples, leads): {record.shape}")
    print(f"Sampling frequency (Hz): {fields['fs']}")
    print(f"Number of leads: {fields['n_sig']}")
    print(f"Signal names (leads): {fields['sig_name']}")

    ##Plotting the EKG
    print("\nGenerating EKG plot...")

    fs = fields['fs'] #Get the sampling frequency
    n_samples = record.shape[0] # Total number of samples
    num_leads = fields['n_sig'] # Number of leads

    #Create a time vector for plotting
    #time = np.arrange(n_samples) / fs # For the entire signal

    plot_duration_seconds = 10 #10 seconds of EKG data
    end_sample = min(n_samples, int(plot_duration_seconds * fs))

    time_segment = np.arange(end_sample) / fs
    plt.figure(figsize=(15,6)) # Create a figure and set its size

    for i in range(num_leads):
        signal_data = record[:end_sample, i] #Get data for current lead
        lead_name = fields['sig_name'][i] #Get the name of the current lead
        plt.plot(time_segment, signal_data, label=f'Lead {i+1} ({lead_name})')

    plt.title(f"EKG Signal for Record {record_name} (First {plot_duration_seconds} Seonds)")
    plt.xlabel("Time (seconds)")
    plt.ylabel("Amplitude (mV)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


except FileNotFoundError:
    print(f"\nError: Could not find files for record '{record_name}'.")
    print("Please ensure '418.dat', '418.hea', and '418.atr' are all in the same directory as this script")
except Exception as e:
    print(f"\nAn unexpected error occured: {e}")
    print("Ensure the 'wfdb' library is installed and files are not corrupted.")