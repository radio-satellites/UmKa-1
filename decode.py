from PIL import Image
import os
import struct
from tqdm import tqdm
from astropy.io import fits
from astropy.utils.data import get_pkg_data_filename
import argparse
from crc import Calculator, Crc32

buffsize = 8192
buffsize_bytes = int(buffsize/8)

argparser = argparse.ArgumentParser()
argparser.add_argument("--source_file", "-f", required=True, action="store")
argparser.add_argument("--crc_check", "-crc", action="store_true")
argparser.add_argument("--output_file", "-o", required=True, action="store")
args = argparser.parse_args()

bytes_noframes = os.path.getsize(args.source_file)

f = open(args.source_file,'rb')

lines = int(bytes_noframes/buffsize_bytes)


cur_x = 0
cur_y = 0

f_out = open(args.output_file,'wb')

calculator = Calculator(Crc32.CRC32, optimized=True)

check_crc = False

if args.crc_check:
    check_crc = True
    print("CRC checking is enabled")




for i in tqdm(range(lines)):
    frame = f.read(buffsize_bytes)
    asm = frame[0:3]
    vcid = frame[4]

    counter = int.from_bytes(frame[5:8], "big")

    payload = frame[9:1017]
    crc = frame[1018:1022]

    if hex(vcid) == "0x41":
        #Filter out all others... 0x41 is imagery!
        if check_crc == True:
            crc_calc = calculator.checksum(payload)
            #crc = int.from_bytes(crc)
            crc_matches = calculator.verify(crc,crc_calc)
            if crc_matches:
                #print("WRITE!")
                f_out.write(payload)
        elif check_crc == False:
            f_out.write(payload)


f.close()
f_out.close()

image_file = get_pkg_data_filename(args.output_file)
print("\n-----TELESCOPE FITS FILE INFORMATION-----")
print(fits.info(image_file))
try:
    image_data = fits.getdata(image_file, ext=0)
except:
    print("[ERROR] FITS error, incomplete/corrupt dump")
    exit()

image = Image.fromarray(image_data, 'I;16')
        
image.save(args.output_file+".png")
