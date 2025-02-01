import socket
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib

# Use an interactive backend
matplotlib.use("tkAgg")  # Change to "Qt5Agg" if needed

# 🛰️ **UDP Configuration**
UDP_IP = "0.0.0.0"  # ESP32 Port
UDP_PORT = 5005
SAMPLES = 64  # Must match ESP32 settings

# **Set up UDP socket**
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 8192)  # Increase buffer
sock.settimeout(0.5)  # Avoids blocking indefinitely

# **Initialize Matplotlib figure for real-time spectrogram**
fig, ax = plt.subplots()
spec_data = np.zeros((128, SAMPLES // 2 + 1))  # Spectrogram buffer
im = ax.imshow(spec_data, aspect='auto', cmap='magma', origin='lower', vmin=-100, vmax=0)
plt.colorbar(im, ax=ax)

def update_spectrogram(frame):
    global spec_data
    try:
        # 📡 **Receive UDP packet**
        data, _ = sock.recvfrom(SAMPLES * 2)  # Each sample is 2 bytes (int16)
        if len(data) != SAMPLES * 2:
            print(f"⚠️ Warning: Unexpected packet size ({len(data)} bytes)")
            return im,

        samples = np.frombuffer(data, dtype=np.int16)  # Convert bytes to int16

        # 🔍 **Compute FFT (Fast Fourier Transform)**
        spectrum = np.abs(np.fft.rfft(samples))
        spectrum = 20 * np.log10(spectrum + 1e-6)  # Convert to dB scale (avoid log(0) issues)

        # 📈 **Update Spectrogram**
        spec_data = np.roll(spec_data, -1, axis=0)  # Scroll data
        spec_data[-1, :] = spectrum  # Insert new FFT row

        # Adjust visualization dynamically
        im.set_clim(spec_data.min(), spec_data.max())  
        im.set_data(spec_data)  # Update image

        # **Save spectrogram as PNG**
        if frame % 100 == 0:  # Save every 20th frame
            plt.savefig(f"spectrogram_{frame}.png")  # Save each frame as a PNG file
            print(f"Spectrogram saved as spectrogram_{frame}.png")

    except socket.timeout:
        print("No connection")

    return im,

# 🖥️ **Run Real-Time Animation**
global ani
ani = animation.FuncAnimation(fig, update_spectrogram, interval=100, blit=False, save_count=200)

plt.xlabel("Frequency Bin")
plt.ylabel("Time")
plt.title("🎵 Real-Time Spectrogram")
plt.show()
