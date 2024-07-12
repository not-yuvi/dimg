import argparse
import sys
import urllib.request
import msvcrt
from PIL import Image
from termcolor import cprint

def ResizeImg(image, height, width, mode, mode_val):
    # Resize the image
    if str(mode).isalpha():
        mode_val = int(mode_val[1:])
    else:
        mode_val = int(mode_val)
    
    if mode_val > 0:
        image_width, image_height = image.size 
        aspect_ratio = image_width / image_height
        
        if not mode in ('h', 'w'): 
            mode = 'h'
        if mode == 'h':
            new_width = int(mode_val * aspect_ratio)
            resized_image = image.resize((new_width, mode_val))
        else:
            new_height = int(mode_val * aspect_ratio)
            resized_image = image.resize((mode_val, new_height))
        return resized_image
    else:
        resized_image = image.resize((width, height))
        return resized_image

def main(args):
    parser = argparse.ArgumentParser(description='Image resizing and saving from URL')
    parser.add_argument('image_url', metavar='URL', type=str, help='URL of the image to download and resize')
    parser.add_argument('-r', metavar='RESIZE', type=str, help='Resize option: specify dimensions like "heightxwidth" or just "mode_value"')
    args = parser.parse_args(args)
    
    error = False
    cprint('Working on it...', 'green')
    
    try:
        image_url = args.image_url
        
        height, width, options, mode_val = None, None, None, None
        
        if args.r:
            options = args.r
            if options[0] == '-':
                if options[1] == 'r':
                    if not options[3:].isdigit():
                        dimensions = options[2:].split('x')
                        if len(dimensions) == 2 and dimensions[0].isdigit() and dimensions[1].isdigit():
                            height, width = int(dimensions[0]), int(dimensions[1])
                        else:
                            raise ValueError
                    else:
                        mode_val = options[2:]
                else:
                    raise ValueError
            else: 
                options = None
        
        file_name = image_url.split('/')[-1]
        urllib.request.urlretrieve(image_url, file_name)
        
        # Open the downloaded image
        image = Image.open(file_name)
        
        # Resize the image if dimensions are provided
        if height is not None and width is not None and args.r is not None:
            resized_image = ResizeImg(image, height, width, 0, 0)
            resized_image.save(file_name)
        elif mode_val is not None:
            resized_image = ResizeImg(image, 0, 0, mode_val[0], mode_val[0:])
            resized_image.save(file_name)
    
    except IndexError:
        if len(sys.argv) > 1:
            print('No URL Input')
        else:
            print('How to use: github.com (replace in production)')
        error = True
    except urllib.error.HTTPError as he:
        if hasattr(he, 'code') and he.code == 404:
            if len(sys.argv) > 1:
                print(f'The URL "{sys.argv[1]}" does not exist or is not accessible.')
            else:
                print('No URL Input')
        else:
            print('An HTTP error occurred:', he)
        error = True
    except ValueError as ve:
        if str(ve).startswith("unknown url type:"):
            if len(sys.argv) > 1:
                print(f'"{sys.argv[1]}" is not a valid URL')
            else:
                print('No URL Input')
        else:
            print('Invalid Option')
        error = True
    
    if len(sys.argv) > 1:
        cprint(f'The Process Finished {"with Errors" if error else "Successfully!"}', 'red' if error else 'blue')
    
    if error:
        print("Press any key to quit...")
        msvcrt.getch()
        print("Exiting...")

if __name__ == '__main__':
    main(sys.argv[1:])
