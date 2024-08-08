# Thermal Imaging


This project demonstrates how to use a Raspberry Pi 4B and an MLX90640 thermal camera to capture and display thermal images. The thermal images can be viewed directly on the Raspberry Pi or remotely on a laptop.

## Features

- Captures thermal images using the MLX90640 sensor.
- Displays images using Matplotlib.
- Options to view results via VNC, SSH with X forwarding, or Jupyter Notebook.
- Real-time thermal image feed visualization.

## MLX90640 Thermal Camera Details

The **7Semi MLX90640** thermal camera is a key component of this project, offering:

- **Wide 110° Field of View:** 
- **32x24 Pixel IR Sensor Array:** 
- **Temperature Range:** Accurately measures temperatures from -40°C to 300°C.
- **Measurement Range:** Effective up to 7 meters for diverse applications.
  
I purchased this camera from [Evelta](https://evelta.com/7semi-mlx90640-ir-thermal-camera-breakout-110-fov-i2c/?utm_campaign=PMax_7Semi_Brand&utm_source=google&utm_medium=cpc&utm_matchtype=&utm_term=&adgroupid=&gc_id=21448253640&h_ad_id=&gad_source=4&gclid=CjwKCAjw2dG1BhB4EiwA998cqCfoiC6q-wXeibWAZKEZxu1VLhOu--OBwlfJAsDxMgRj7eU0X4_2BBoCkMoQAvD_BwE).

## Hardware Requirements

- **Raspberry Pi 4B (4GB)**
- **MLX90640 Thermal Camera**
- **Connections:**
  - SDA to GPIO2 (pin 3)
  - SCL to GPIO3 (pin 5)
  - VCC to 3.3V (pin 1)
  - GND to GND (pin 6)
 
  ![image](https://github.com/user-attachments/assets/3a93744b-e3ff-4857-a78a-31c5d37e603c)

## Software Requirements

- **Raspberry Pi OS:** Ensure your Raspberry Pi is running the latest version. Follow the [Raspberry Pi OS installation guide](https://www.raspberrypi.com/software/) if you haven't set it up yet. You can also watch this [video tutorial](https://www.youtube.com/watch?v=F5OYpPUJiOw) for a step-by-step guide on installing Raspberry Pi OS.

- **Python 3.x:** Included with Raspberry Pi OS.
- **Libraries:** `smbus2`, `numpy`, `matplotlib`, `adafruit-circuitpython-mlx90640`

## Initial Setup of Raspberry Pi

### Step 1: Update and Upgrade the System

Open a terminal on your Raspberry Pi and run the following commands:

```bash
sudo apt-get update
sudo apt-get upgrade -y
```

### Step 2: Enable I2C on the Raspberry Pi
Enable the I2C interface for communication with the MLX90640 sensor:
```bash
sudo raspi-config
```

- Select "Interfacing Options"
- Select "I2C"
- Enable I2C
- Exit and reboot the Raspberry Pi:

```bash
sudo reboot
```
### Step 3: Install Required Libraries in a Virtual Environment

Set Up a Virtual Environment:

1. Install Virtual Environment Tools:
    ```bash
    sudo apt-get install -y python3-venv
    ```

2. Create a Virtual Environment:
    ```bash
    python3 -m venv myenv
    ```

3. Activate the Virtual Environment:
    ```bash
    source myenv/bin/activate
    ```

4. Install I2C Tools and Python Packages:
    ```bash
    pip install smbus2 numpy matplotlib adafruit-circuitpython-mlx90640
    ```

### Step 4: Verify I2C Connection

Check I2C Devices:

```bash
sudo i2cdetect -y 1
 ```
You should see a device listed at address 0x33, which indicates the MLX90640 is connected correctly.

![image](https://github.com/user-attachments/assets/b484440c-ef47-4726-9b98-bff4520cf5f2)

### Step 5: Create Python Script to Capture Thermal Image

Write the Python Script: Create a file named `ImageFeed.py` and add the following code:

```python
import board
import busio
import adafruit_mlx90640
import numpy as np
import matplotlib.pyplot as plt

i2c = busio.I2C(board.SCL, board.SDA, frequency=400000)
mlx = adafruit_mlx90640.MLX90640(i2c)

mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_2_HZ

def capture_thermal_image():
    frame = np.zeros((24*32,))
    mlx.getFrame(frame)
    return frame.reshape(24, 32)

thermal_image = capture_thermal_image()
plt.imshow(thermal_image, cmap='inferno')
plt.colorbar()
plt.show()
 ```

Running the Script
```bash
python3 ImageFeed.py
```

Running the script directly on the Raspberry Pi will display the output (thermal image) on the Raspberry Pi’s own screen. If you prefer to see the results remotely, you should follow Step 6.

### Step 6: Display Results on Laptop

#### Option 1: Remote Desktop (VNC)

1. Install VNC Server on Raspberry Pi:
    ```bash
    sudo apt-get install realvnc-vnc-server
    sudo systemctl enable vncserver-x11-serviced.service
    sudo systemctl start vncserver-x11-serviced.service
    ```

2. Enable VNC in Raspberry Pi Configuration:
    ```bash
    sudo raspi-config
    ```

    - Select "Interfacing Options"
    - Select "VNC"
    - Enable VNC

3. Install VNC Viewer on Laptop:
    Download and install VNC Viewer from [here](https://www.realvnc.com/en/connect/download/viewer/).

4. Connect to Raspberry Pi:
    - Open VNC Viewer on your laptop.
    - Connect to the Raspberry Pi’s IP address.

#### Option 2: SSH with X Forwarding

1. Enable SSH on Raspberry Pi:
    ```bash
    sudo raspi-config
    ```

    - Select "Interfacing Options"
    - Select "SSH"
    - Enable SSH

2. Connect from Your Laptop:
    - Open a terminal on your laptop (Linux or macOS) and use SSH with X forwarding:
      ```bash
      ssh -X pi@<Raspberry_Pi_IP>
      ```

3. Run your Python script:
    ```bash
    python3 ImageFeed.py
    ```

#### Option 3: Use Jupyter Notebook

1. Install Jupyter Notebook on Raspberry Pi:
    ```bash
    pip install jupyter
    ```

2. Run Jupyter Notebook:
    ```bash
    jupyter notebook --ip=0.0.0.0 --no-browser
    ```

3. Access from Your Laptop:
    - Open a web browser on your laptop and go to `http://<Raspberry_Pi_IP>:8888`.

### Real-Time Thermal Image Feed

```python
import board
import busio
import adafruit_mlx90640
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

i2c = busio.I2C(board.SCL, board.SDA, frequency=400000)
mlx = adafruit_mlx90640.MLX90640(i2c)
mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_2_HZ

fig, ax = plt.subplots()
img = ax.imshow(np.zeros((24, 32)), cmap='inferno', vmin=20, vmax=40)
plt.colorbar(img, ax=ax)

def update(frame):
    frame_data = np.zeros((24*32,))
    mlx.get_frame(frame_data)
    thermal_image = frame_data.reshape((24, 32))
    img.set_data(thermal_image)
    return [img]

ani = animation.FuncAnimation(fig, update, blit=True, interval=1000)
plt.show()
 ```
Run this script using:
```bash
python3 RealTimeFeed.py
```
This will show a live feed of the thermal images from the MLX90640 sensor.

## Example Output

Here's what the output of the thermal image might look like:

![image](https://github.com/user-attachments/assets/03b91c95-8664-4b2a-aab9-751ba2433311)
![image](https://github.com/user-attachments/assets/a21749e4-aa6d-452e-88f5-d966921b53fb)


## Troubleshooting

- ### No Module Named Error

  Ensure all dependencies are installed. You can use the following command to install all required packages:

  ```bash
  pip install -r requirements.txt
  ```

- ### I2C Not Detected
    
  Verify connections and ensure the I2C interface is enabled in the Raspberry Pi configuration.
    
- ### Permissions Error
    
  Run the script with superuser privileges:
    
  ```bash
  sudo python3 ImageFeed.py
   ```

## Adafruit Library

This project utilizes the [Adafruit CircuitPython MLX90640](https://github.com/adafruit/Adafruit_CircuitPython_MLX90640) library to interface with the MLX90640 thermal camera. The Adafruit library provides a simple and efficient way to interact with the MLX90640 sensor, making it easier to capture and process thermal images. It handles the I2C communication and provides functions for retrieving the thermal image data.

### Why Adafruit Library?

- **Ease of Use:** The library offers straightforward methods to interact with the MLX90640, reducing the complexity of handling raw I2C communication.
- **Documentation:** Adafruit provides comprehensive documentation and support, making it easier to integrate and troubleshoot.
- **Community Support:** Being widely used, the library benefits from community contributions and bug fixes.


### Alternative Approaches

- **Direct I2C Communication:** You can use Python's `smbus2` library to handle direct I2C communication with the MLX90640. This method requires manual management of the I2C protocol and data processing.
  [smbus2 on GitHub](https://github.com/kplindegaard/smbus2)

- **Other Python Libraries:** Other third-party libraries and drivers may be available, depending on your programming language and platform. You might need to adapt the code to fit these libraries' APIs and documentation.

If you prefer exploring alternative methods, you can look for other MLX90640 libraries or consult the sensor's datasheet for direct communication details.


## Additional Resources

For another approach to setting up the MLX90640 thermal camera with Raspberry Pi, you can refer to this [high-resolution thermal camera guide](https://makersportal.com/blog/2020/6/8/high-resolution-thermal-camera-with-raspberry-pi-and-mlx90640) on MakersPortal. This guide provides a detailed walkthrough for connecting and using the MLX90640 thermal camera with a Raspberry Pi, including steps for setting up the hardware and software without using a virtual environment.
