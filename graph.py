import matplotlib.pyplot as plt
import numpy as np
import os

# Make sure the output directory exists
os.makedirs('results/graphs', exist_ok=True)

#########################################
# 1. H264 vs H265 Graphs
#########################################

# Data
h264_data = {
    'Recording Time': [5, 10, 30, 60],
    'Compression Size': [0.65, 1.03, 2.78, 5.41],
    'Compression Time': [1.14, 1.16, 1.15, 1.39],
}

h265_data = {
    'Recording Time': [5, 10, 30, 60],
    'Compression Size': [0.49, 0.53, 1.60, 2.72],
    'Compression Time': [8.69, 9.92, 20.84, 30.14],
}

# Plot 1: Recording Time vs Compression Size
plt.figure(figsize=(8, 6))
plt.plot(h264_data['Recording Time'], h264_data['Compression Size'], marker='o', label='H264')
plt.plot(h265_data['Recording Time'], h265_data['Compression Size'], marker='s', label='H265')
plt.xlabel('Recording Time (s)')
plt.ylabel('Compression Size (MB)')
plt.title('Compression Size vs Recording Time')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)
plt.savefig('results/graphs/compression_size_vs_recording_time.png')
plt.close()

# Plot 2: Recording Time vs Compression Time
plt.figure(figsize=(8, 6))
plt.plot(h264_data['Recording Time'], h264_data['Compression Time'], marker='o', label='H264')
plt.plot(h265_data['Recording Time'], h265_data['Compression Time'], marker='s', label='H265')
plt.xlabel('Recording Time (s)')
plt.ylabel('Compression Time (s)')
plt.title('Compression Time vs Recording Time')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)
plt.savefig('results/graphs/compression_time_vs_recording_time.png')
plt.close()

#########################################
# 2. Compression Size & Time per Video
#########################################

# Data
video_descriptions = [
    "Some movement",
    "No Movement",
    "Excess Movement",
    "Some + No movement",
    "Recording from Far",
    "Recording from Far + Excess Movement"
]

compression_size = [0.87, 0.49, 0.86, 0.61, 0.48, 0.78]  # in MB
compression_time = [12.38, 6.38, 13.63, 11.18, 7.44, 11.50]  # in seconds

# Sort by Compression Time
combined = list(zip(video_descriptions, compression_size, compression_time))
combined.sort(key=lambda x: x[2])

video_descriptions_sorted, compression_size_sorted, compression_time_sorted = zip(*combined)

# Setup
x = np.arange(len(video_descriptions_sorted))
width = 0.35

# Plot
fig, ax = plt.subplots(figsize=(12, 6))

rects1 = ax.bar(x - width/2, compression_size_sorted, width, label='Compression Size (MB)', color='skyblue')
rects2 = ax.bar(x + width/2, compression_time_sorted, width, label='Compression Time (s)', color='salmon')

# Labels and Title
ax.set_ylabel('Value')
ax.set_xlabel('Video Description')
ax.set_title('Compression Size and Compression Time per Video (Sorted)')
ax.set_xticks(x)
ax.set_xticklabels(video_descriptions_sorted, rotation=25, ha='right')
ax.legend()
ax.grid(axis='y', linestyle='--', alpha=0.7)

fig.tight_layout()
plt.savefig('results/graphs/compression_size_time_sorted_combined.png')
plt.close()
