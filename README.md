# Thermal_Imaging


This project demonstrates how to use a Raspberry Pi 4B and an MLX90640 thermal camera to capture and display thermal images. The thermal images can be viewed directly on the Raspberry Pi or remotely on a laptop.

## Features

- Captures thermal images using the MLX90640 sensor.
- Displays images using Matplotlib.
- Options to view results via VNC, SSH with X forwarding, or Jupyter Notebook.

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

- **Raspberry Pi OS:** Ensure your Raspberry Pi is running the latest version.
- **Python 3.x:** Included with Raspberry Pi OS.
- **Libraries:** `smbus2`, `numpy`, `matplotlib`, `adafruit-circuitpython-mlx90640`

## Initial Setup of Raspberry Pi

### Step 1: Update and Upgrade the System

Open a terminal on your Raspberry Pi and run the following commands:

```bash
sudo apt-get update
sudo apt-get upgrade -y
