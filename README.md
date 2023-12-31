# UmKa-1

![image](https://github.com/radio-satellites/UmKa-1/assets/114111180/77ef81cb-d1b1-4e73-bd43-7766c514a6f6)

Decode imagery from the UmKa-1 amateur telescope!

# About

As of 2023-07-04, the satellite UmKa-1 is alive and healthy in orbit. This tool decodes **S band dump transmissions** from the spacecraft. This contains high resolution imagery from the telescope on board the satellite. 

**EDIT**: As of Sept 25, 2023, the telescope *and* the S band downlink has failed. The imagery is now transmitted from an engineering camera via the 437.625 MHz downlink as 19200 baud FSK. I currently do not have any recording of this dump, so I am unable to write any decoders. SSTV is planned eventually. 

For more information, see https://telegra.ph/Otchet-o-statuse-missii-orbitalnogo-kosmicheskogo-teleskopa-UmKA-1-RS40S-09-25 (in Russian). 



# Usage

Input: Derandomized and synchronized CADU (example in repository). 

Output: FITS telescope files and converted PNG imagery. 

To decode imagery:

```
python decoder.py -f umka_1.cadu -o umka_1.fits
```

This will read CADU frames from "umka_1.cadu" and output to "umka_1.fits" and "umka_1.fits.png."

If you have very noisy frames, CRC checking should be enabled with the ```-crc``` flag. This does take **much** longer, though, so use it wisely!

# Dependencies

The decoder depends on the following packages:

PIL/Pillow
tqdm
astropy
crc
