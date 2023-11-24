# Prusa Thumbnail Generator
A simple python script that transforms a `.png` into a thumbnail for Prusa GCode.

# Usage
## Install dependecies
This script's only dependency is [Pillow](https://pypi.org/project/Pillow/). You can easily install it using pip :
```bash
pip install Pillow
```
Or if `pip` is not in your PATH :
```bash
python3 -m pip install Pillow
```

## Get the code
You can either pull the repository :
```bash
git clone https://github.com/l-eg116/prusa-thumbnail-generator.git
cd prusa-thumbnail-generator
```
Or just download the python file :
```bash
wget https://raw.githubusercontent.com/l-eg116/prusa-thumbnail-generator/main/generate-thumbnail.py
chmod +x generate-thumbnail.py
```

## Run the code
To run the script, use :
```bash
./generate-thumbnail.py [-h] [-m] [-s [SIZE]] [--crop] input [output]
```
or
```bash
python3 generate-thumbnail.py [-h] [-m] [-s [SIZE]] [--crop] input [output]
```

### Arguments and flags
Get this list in your command line with `./generate-thumbnail.py -h` or `./generate-thumbnail.py --help`.

#### `input`
The `.png` file that you want to make a thumbnail of.

#### `output`
Destination of generated thumnail, `stdout` by default.
Unless `--merge` is set, the thumbnail will be appended to the file.

#### `--merge`, `-m`
If this flag is set, existing thumbnail data in `output` will be replaced with the one generated.
Only thumbnails with the same dimensions will be replaced. If no thumbnail is found, new thumbnail will be prepended to the file.

This is usefull for changing thumbnails of GCode previously generated by the PrusaSlicer.

#### `--size [SIZE]`, `-s [SIZE]`
> `SIZE`: `<width>x<height>` or `keep`

Specifies the size of the generated thumbnail, `220x124` by default. Use `keep` to disable image resizing.
`220x124` corresponds to the thumbnail size for Prusa Mini and Mini+ 3D printers.

#### `--crop`
If this flag is set, the image will be cropped to target aspect ratio before being resized to prevent stretching.

## Disclaimers

### Python version
This project was tested with Python 3.10.12 and should be able to run with any version >= 3.6.

### Testing
The thumbnails generated where tested on Prusa Mini and Mini+ 3D printers. The format should be the same for other Prusa printers (ie base 64 encoded PNGs) but I can't say for sure. If you have any input on this feel free.

