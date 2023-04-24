## Image to MODELSIM testbench transcript generator
## 24/04/2023

from PIL import Image
import numpy as np

# Get the number to be classified
number = input("Enter the number: ")
# Change file extension to your need
filename = number + '.bmp'

init = """force -freeze sim:/conv_layer_1/CLK 1 0, 0 {50 ps} -r 100
force -freeze sim:/conv_layer_1/RST 1 0
force -freeze sim:/conv_layer_1/EN_STREAM 1 0
force -freeze sim:/conv_layer_1/EN_LOC_STREAM_1 1 0
run 150ps

force -freeze sim:/conv_layer_1/RST 0 0
"""

DIN = "force -freeze sim:/conv_layer_1/DIN {bits} 0"
run = "run {dur}ps"

# Create testbench text file to be copy-pasted into transcript window in MODELSIM
with open('LeNet_num8_tb.txt', 'w') as f:
    f.write(init)
    f.close()

# Open image and convert it to grayscale
img = Image.open(filename).convert("L")
# Image to numpy array
np_img = np.array(img)

# Numpy binary array representation
bin_array = np.array([np.binary_repr(x, width=8) for x in np_img.ravel()])
#bits = np.reshape(bin_array, (32, 32))

# Change bin_array to string for comparison
bin_array = np.char.mod('%s', bin_array)
print(len(bin_array))

count0 = 0
count1 = 0

for index, x in enumerate(bin_array):
    if np.char.equal(x, '11111111'):
        #print("count1:", count1)
        count1 += 1
        if (np.char.equal([bin_array[index+1] if(index < len(bin_array)-1) else bin_array[index]], '00000000')) or (index == len(bin_array)-1):
            with open('LeNet_num8_tb.txt', 'a') as f:
                f.write(DIN.format(bits=11111111)+'\n')
                f.write(run.format(dur=count1*100)+'\n\n')
                f.close()
                count1 = 0
    elif np.char.equal(x, '00000000'):
        print("count0:", count0)
        count0 += 1
        if (np.char.equal([bin_array[index+1] if(index < len(bin_array)-1) else bin_array[index]], '11111111')) or (index == len(bin_array)-1):
            print(x, index)
            with open('LeNet_num8_tb.txt', 'a') as f:
                f.write(DIN.format(bits='00000000')+'\n')
                f.write(run.format(dur=count0*100)+'\n\n')
                f.close()
                count0 = 0
    else:
        print("Error!")

end1 = """run 900ps
force -freeze sim:/conv_layer_1/EN_STREAM 0 0
run 100ps

"""

with open('LeNet_num8_tb.txt', 'a') as f:
    f.write(end1)
    f.close()