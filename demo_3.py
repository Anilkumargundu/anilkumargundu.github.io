import serial
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.patches as patches

# Configure the serial port
ser = serial.Serial('COM5', baudrate=9600, timeout=1)  # Replace 'COM5' with your COM port name

# Initialize empty lists to store timestamps and data points for value1 and value2
timestamps = []
data_points1 = []
data_points2 = []

# Load and display the image
image_path_1 = 'VLSI.png'
img1 = plt.imread(image_path_1)
image_path_2 = 'greenIC.jpg'
img2 = plt.imread(image_path_2)
image_path_3 = 'nus1.jpg'
img3 = plt.imread(image_path_3)
image_path_4 = 'SHINE.jpg'
img4 = plt.imread(image_path_4)


try:
    plt.ion()  # Turn on interactive mode for live updating plot

    # Create a figure with a grid layout (1 row, 3 columns)
    fig = plt.figure(figsize=(24, 9))
    gs = GridSpec(2, 2, width_ratios=[2, 1])
    fig.suptitle("World's First Batteryless Smart T-Shirt with Step Count", fontsize=22, color='green', fontweight='bold')

    # Create subplots for value1 and value2
    ax1 = plt.subplot(gs[0, 0])
    ax2 = plt.subplot(gs[1, 0])

    ax1.set_xlabel('Time (seconds)')
    ax1.set_ylabel('Rectified Voltage')
    #ax1.legend(['Value 1'], loc='upper right')

    ax2.set_xlabel('Time (seconds)')
    ax2.set_ylabel('Step Count')
    #ax2.legend(['Value 2'], loc='upper right')

    # Load and display the image on the right side of the plot
    ax3 = plt.subplot(gs[0:, 1])
    imagebox = OffsetImage(img1, zoom=0.5)  # Adjust the zoom factor as needed
    ab = AnnotationBbox(imagebox, (0.12, 0.9), frameon=False, xycoords='axes fraction')
    ax3.add_artist(ab)
    ax3.axis('off')  # Hide the axis for the image subplot
    
    ax4 = plt.subplot(gs[0:, 1])
    imagebox = OffsetImage(img2, zoom=0.095)  # Adjust the zoom factor as needed
    ab = AnnotationBbox(imagebox, (0.54, 0.72), frameon=False, xycoords='axes fraction')
    ax4.add_artist(ab)
    ax4.axis('off')  # Hide the axis for the image subplot

    ax5 = plt.subplot(gs[0:, 1])
    imagebox = OffsetImage(img3, zoom=0.1)  # Adjust the zoom factor as needed
    ab = AnnotationBbox(imagebox, (0.5, 0.9), frameon=False, xycoords='axes fraction')
    ax5.add_artist(ab)
    ax5.axis('off')  # Hide the axis for the image subplot

    ax6 = plt.subplot(gs[0:, 1])
    imagebox = OffsetImage(img4, zoom=0.2)  # Adjust the zoom factor as needed
    ab = AnnotationBbox(imagebox, (1, 0.9), frameon=False, xycoords='axes fraction')
    ax6.add_artist(ab)
    ax6.axis('off')  # Hide the axis for the image subplot

    # Create boxes to display value1 and value2 below the image
    value1_box = patches.Rectangle((0.08, 0.4), 0.8, 0.2, linewidth=3.5, edgecolor='red', facecolor='none')
    value2_box = patches.Rectangle((0.08, 0.08), 0.8, 0.2, linewidth=3.5, edgecolor='red', facecolor='none')
    ax3.add_patch(value1_box)
    ax3.add_patch(value2_box)

    # Display value1 and value2 inside the boxes
    value1_text = ax3.text(0.22, 0.42, '', color='green', fontsize=18)
    value3_text = ax3.text(0.14, 0.30, '', color='red', fontsize=16)
    value2_text = ax3.text(0.22, 0.13, '', color='green', fontsize=18)

    while True:
        # Read a line of data from the serial port
        data = ser.readline().decode('utf-8').strip()
        data_values = data.split()

        if len(data_values) == 2:
            try:
                # Interpret the two values as float and int
                value1 = float(data_values[0])
                value2 = int(data_values[1])

                # Update the lists with new data
                timestamps.append(len(timestamps) + 1)
                data_points1.append(value1)
                data_points2.append(value2)

                # Plot the updated data on the respective subplots
                ax1.clear()
                ax2.clear()

                ax1.plot(timestamps, data_points1, label='Rectified Voltage', color='green')
                ax2.plot(timestamps, data_points2, label='Step count', color='blue')

                ax1.set_xlabel('Time (seconds)')
                ax1.set_ylabel('Harvested Voltage')
                #ax1.legend(['Value 1'], loc='upper right')

                ax2.set_xlabel('Time (seconds)')
                ax2.set_ylabel('Step Count')
                #ax2.legend(['Value 2'], loc='upper right')

                # Display value1 and value2 inside the boxes
                value1_text.set_text(f'\nInstantaneous\nPower (pW):\n   {value1 * 55:.{4}f}')
                value3_text.set_text(f'~1 Million X\nlower than Apple watch')
                value2_text.set_text(f'\n  Step Count:\n        {value2:.{0}f}')

                # Pause briefly to update the plot
                plt.pause(0.01)

            except ValueError:
                print("Invalid data received")

except KeyboardInterrupt:
    # Close the serial port when the program is interrupted (Ctrl+C)
    ser.close()
    plt.ioff()  # Turn off interactive mode before exiting

plt.show()  # Keep the final plot displayed after the loop
