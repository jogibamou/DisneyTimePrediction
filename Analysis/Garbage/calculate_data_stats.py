from DatasetAPI import Datasets
import numpy as np
import matplotlib.pyplot as plt

data = Datasets.DataAccessor()
attraction_wait = data.get('public', 'filtered_wait_times_thunder', limit = 1000000000) 

max_wait_val = 400
min_wait_val = 0
wait_time_delimiter = 5
wait_time_val_index = 3
bins = ((max_wait_val - min_wait_val) // wait_time_delimiter) + 1

wait_time_vals = []
wait_time_vals_no_zeros = []
wait_time_vals_0_120 = []
wait_time_vals_120_240 = []
wait_time_vals_240_360 = []
wait_time_vals_300_400 = []

bins2 = np.zeros(bins)
for row in attraction_wait:

    bins2[row[3] // 5] += 1
    wait_time_vals.append(row[3])
    if(row[3] > 0.1):
        wait_time_vals_no_zeros.append(row[3])
    if(row[3] > 0 and row[3] < 120):
        wait_time_vals_0_120.append(row[3])
    if(row[3] > 120 and row[3] < 240):
        wait_time_vals_120_240.append(row[3])
    if(row[3] > 240 and row[3] < 360):
        wait_time_vals_240_360.append(row[3])
    if(row[3] > 300):
        wait_time_vals_300_400.append(row[3])

fig, axes = plt.subplots(2,3, tight_layout=True, figsize=(16.0,9.0))

for item, num in zip(bins2, range(0, len(bins2) + 1)):
    print(f"{num*5} minutes: {item}")

axes[0,0].hist(wait_time_vals, bins)
axes[0,0].set_title('All values')
axes[0,1].hist(wait_time_vals_no_zeros, bins)
axes[0,1].set_title('All values over 0')
axes[0,2].hist(wait_time_vals_0_120, bins)
axes[0,2].set_title('All values between 0 and 120')
axes[1,0].hist(wait_time_vals_120_240, bins)
axes[1,0].set_title('All values between 120 and 240')
axes[1,1].hist(wait_time_vals_240_360, bins)
axes[1,1].set_title('All values between 240 and 360')
axes[1,2].hist(wait_time_vals_300_400, bins)
axes[1,2].set_title('All values above 300')

plt.sca(axes[0,0])
plt.xticks(np.arange(min_wait_val, max_wait_val, 80))
plt.xlabel("Wait time in minutes")
plt.ylabel("Count")

plt.sca(axes[0,1])
plt.xticks(np.arange(min_wait_val, max_wait_val, 80))
plt.xlabel("Wait time in minutes")
plt.ylabel("Count")

plt.sca(axes[0,2])
plt.xticks(np.arange(min_wait_val, 120, 80))
plt.xlabel("Wait time in minutes")
plt.ylabel("Count")

plt.sca(axes[1,0])
plt.xticks(np.arange(120, 240, 80))
plt.xlabel("Wait time in minutes")
plt.ylabel("Count")

plt.sca(axes[1,1])
plt.xticks(np.arange(240, 360, 80))
plt.xlabel("Wait time in minutes")
plt.ylabel("Count")

plt.sca(axes[1,2])
plt.xticks(np.arange(300, max_wait_val, 80))
plt.xlabel("Wait time in minutes")
plt.ylabel("Count")

plt.savefig('wait_times_histograms.png')
plt.show()