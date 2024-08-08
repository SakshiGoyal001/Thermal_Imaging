import board
import busio
import adafruit_mlx90640
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Set up I2C and MLX90640
i2c = busio.I2C(board.SCL, board.SDA, frequency=400000)
mlx = adafruit_mlx90640.MLX90640(i2c)
mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_2_HZ

# Initialize plot
fig, ax = plt.subplots()
img = ax.imshow(np.zeros((24, 32)), cmap='inferno', vmin=20, vmax=40)
plt.colorbar(img, ax=ax)

def update(frame):
    # Capture a new thermal image
    frame_data = np.zeros((24*32,))
    mlx.get_frame(frame_data)
    thermal_image = frame_data.reshape((24, 32))
    
    # Update the image
    img.set_data(thermal_image)
    return [img]

# Create animation
ani = animation.FuncAnimation(fig, update, blit=True, interval=1000)

# Show plot
plt.show()
