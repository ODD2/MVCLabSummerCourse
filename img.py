from PIL import Image
import numpy as np
import sys
import os

def PrintHelloMessage():
    print("Hello Nice to Meet You")


if __name__=="__main__":
    print(sys.argv)
    if len(sys.argv) < 4:
        print("usage: img.py [src] [cell_size_w] [cell_size_h]")
        exit(0)
    PrintHelloMessage()
    # PIL accesses images in Cartesian co-ordinates, so it is Image[columns, rows]
    cell_size_w = int(sys.argv[2])
    cell_size_h = int(sys.argv[3])
    origin = Image.open(sys.argv[1])
    process = np.zeros((int(origin.height+origin.height/cell_size_h*2),
                        int(origin.width+origin.width/cell_size_w*2),
                        4), dtype=np.uint8)
    print(int(origin.width*(1+2/cell_size_w)))
    print(int(origin.height*(1+2/cell_size_h)))
    print(process.shape)

    for h in range(int(origin.height/cell_size_h)):    # For every row
        for w in range(int(origin.width/cell_size_w)):    # for every col:
            offset_proc_h = h*(cell_size_h+2)
            offset_proc_w = w*(cell_size_w+2)
            offset_orig_h = h*cell_size_h
            offset_orig_w = w*cell_size_w
            for _h in range(cell_size_h):
                for _w in range(cell_size_w):
                    for c, v in enumerate(origin.getpixel((offset_orig_w+_w, offset_orig_h+_h))):
                        process[offset_proc_h + _h + 1,
                                offset_proc_w + _w + 1][c] = v

            for i in range(cell_size_h):
                for c, v in enumerate(origin.getpixel((offset_orig_w, offset_orig_h+i))):
                    process[offset_proc_h+1+i, offset_proc_w][c] = v
                for c, v in enumerate(origin.getpixel((offset_orig_w+cell_size_w-1, offset_orig_h+i))):
                    process[offset_proc_h+1+i, offset_proc_w+cell_size_w+1][c] = v

            for i in range(cell_size_w):
                for c, v in enumerate(origin.getpixel((offset_orig_w+i, offset_orig_h))):
                    process[offset_proc_h, offset_proc_w+1+i][c] = v
                for c, v in enumerate(origin.getpixel((offset_orig_w+i, offset_orig_h+cell_size_h-1))):
                    process[offset_proc_h+cell_size_h+1, offset_proc_w+1+i][c] = v

            for c, v in enumerate(origin.getpixel((offset_orig_w, offset_orig_h))):
                process[offset_proc_h,
                        offset_proc_w][c] = v
            for c, v in enumerate(origin.getpixel((offset_orig_w+cell_size_w-1, offset_orig_h))):
                process[offset_proc_h,
                        offset_proc_w+1+cell_size_w][c] = v
            for c, v in enumerate(origin.getpixel((offset_orig_w+cell_size_w-1, offset_orig_h+cell_size_h-1))):
                process[offset_proc_h+1+cell_size_h,
                        offset_proc_w+1+cell_size_w][c] = v
            for c, v in enumerate(origin.getpixel((offset_orig_w, offset_orig_h+cell_size_h-1))):
                process[offset_proc_h+1+cell_size_h,
                        offset_proc_w][c] = v


    new_img = Image.fromarray(process, "RGBA")
    new_img.save(os.path.dirname(sys.argv[1])+"/"+"_"+ os.path.basename(sys.argv[1]))
