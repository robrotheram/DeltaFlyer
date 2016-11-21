import numpy as np
import math

tile_size = 256
world_size = 6000 #number of blocks
pixel_size = (world_size/16)*tile_size # number of pixels based on 1 chunk = 256
max_zoom = math.ceil((np.log((pixel_size/tile_size)) / np.log(2)))
map_max_size = math.pow(2,max_zoom)*tile_size

print("world size: %d \n"
      "pixel size: %d \n"
      "max zoom: %d \n"
       "max map size: %d"
      %(world_size,pixel_size,max_zoom,map_max_size))

def istilevalid(z,x,y):
    bounds = math.pow(2,(max_zoom-z))*256
    xb = bounds+(bounds*x)
    yb = bounds+(bounds*y)
    n_chucks_width = int((bounds)/256)
    x = (xb/256)-n_chucks_width
    y = (yb/256)-n_chucks_width
    for i in range(0,(n_chucks_width*n_chucks_width),1):
        ix = i % n_chucks_width
        iy = math.floor(i / n_chucks_width)
        print("tile at:(%d,%d)"%(ix,iy))
        print("CHUNK at:(%d,%d)"%(ix+x,iy+y))



    print("xbounds: %d  \nbounds = %d \nchunk width:%d"%((xb,bounds,((bounds)/256))))





    if(xb > bounds or xb <= 0 or yb > bounds or yb <= 0):
        return False
    else:
        return True


def get_chunk_list(z,x,y):
    list = []
    bounds = math.pow(2,(max_zoom-z))*256
    xb = bounds+(bounds*x)
    yb = bounds+(bounds*y)
    n_chucks_width = int((bounds)/256)
    x = (xb/256)-n_chucks_width
    y = (yb/256)-n_chucks_width
    for i in range(0,(n_chucks_width*n_chucks_width),1):
        ix = i % n_chucks_width
        iy = math.floor(i / n_chucks_width)
        list.append((ix+x,iy+y))
    return list




print(get_chunk_list(6,3,0)[0][0])
