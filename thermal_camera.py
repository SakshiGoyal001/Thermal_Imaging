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
