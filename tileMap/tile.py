from PIL import Image, ImageFilter
import json
import math
import io
import numpy as np
import math
import os


class Tile:

    tile_size = 256
    block_size = 32
    chunk_image_size = block_size*16;
    world_size = 6000 #number of blocks
    pixel_size = (world_size/16)*tile_size # number of pixels based on 1 chunk = 256
    max_zoom = math.ceil((np.log((pixel_size/tile_size)) / np.log(2)))
    map_max_size = math.pow(2,max_zoom)*tile_size

    def __init__(self):
        dir = os.path.dirname(__file__)
        path = "SERVER.json"
        path = os.path.join(dir, path)
        with open(path) as data_file:
            data = json.load(data_file)
        self.chunk_data = data["Worlds"][0]["loadedChunks"] #.pop()["map"]
        self.x = 'init!'
        self.rendered_chunks = {}
        #print(self.x)

    def getimg(self, i):
        if (i >= len(self.chunk_data)):
            return "Textures/blocks/bedrock.png"
        if (self.chunk_data[i] is None):
            return "Textures/blocks/bedrock.png"
        path = self.get_img_path(self.chunk_data.pop()["map"][i].lower())
        return path

    def get_img_path(self,block_name):

        dir = os.path.dirname(__file__)
        path = "Textures/blocks/"+(block_name.lower())+".png"
        path = os.path.join(dir, path)
        return path


    def get_chunk_list(self, z,x,y):
        list = []
        bounds = math.pow(2,(self.max_zoom-z))*256
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

    def get_img(self,block):
        try:
            return Image.open(self.get_img_path(block))
        except EnvironmentError:
            print("ERROR: %s" % self.get_img_path(block) )
            return Image.new('RGB',(32,32))

    def render_chunk(self,blocks):
        img = Image.new('RGB', (self.chunk_image_size,self.chunk_image_size)) #512 x 512
        img_hash = hash(tuple(blocks))
        width =16;
        if(img_hash in self.rendered_chunks):
            print("Found!!!")
            return self.rendered_chunks[img_hash]
        else:
            print("rendering new chunk")
            #blocks.reverse();
            for i in range(0,(width*width),1):
                x = int(math.floor(i / width))
                y = int(i % width)

                im = self.get_img(blocks[i])
                img.paste(im, ((x*self.block_size),(y*self.block_size)))
            self.rendered_chunks[img_hash]=img
            return img#.rotate(270)#.transpose(Image.FLIP_LEFT_RIGHT)

    def rendertile(self,z,x,y):
        chunklist = self.get_chunk_list(z,x,y)
        print(chunklist)
        chunk_width = math.pow(2,self.max_zoom-z);
        image_size = int(self.chunk_image_size/chunk_width)
        tile = Image.new('RGB', (self.chunk_image_size,self.chunk_image_size)) #512 x 512
        print(chunk_width)
        print(image_size)

        for i in range(0,len(chunklist),1):
            cl = chunklist[i]
            x = i % chunk_width
            y = math.floor(i / chunk_width)
            print("%d,%d"%(x,y))
            res = list(filter(lambda x: x["location"]["x"] == cl[0] and x["location"]["z"] == cl[1], self.chunk_data))
            img = None
            if not (res):
                print("(%d,%d) Empty List"%(x,y))
                img = Image.new('RGB',(32,32))
            else:
                chunk = (res.pop())
                print("(%d,%d) | Chunk: (%d,%d)"%(x,y,chunk["location"]["x"],chunk["location"]["z"]))
                blocks = chunk["map"]
                img = self.render_chunk(blocks)


            img = img.resize((image_size, image_size), Image.BILINEAR)
            tile.paste(img, (int(x*image_size),int(y*image_size)))
        return tile





if __name__ == "__main__":
     tile = Tile()
     tile.rendertile(8,5,-6).show();


     # image = tile.get4chunks()
    # output = io.BytesIO()
    # image.save(output,format="jpeg")
    # print(output)
