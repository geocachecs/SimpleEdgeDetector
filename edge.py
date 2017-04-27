from PIL import Image,ImageOps
import heapq

def edge_detect(image,depth=1,brightness=1):
	image = ImageOps.grayscale(image)
	width,height = image.size
	pixels = image.load()
	
	newImage = Image.new("L",(width,height),'black')
	newPixels = newImage.load()
	
	sum=0
	sumB=0
	
	thresh = 0 # thresh over 0 may be unnecessary here

	for i in range(depth,width-depth):
		for j in range(depth,height-depth):
			for x in range(-depth,depth+1):
				for y in range(-depth,depth+1):
					if(x<0):
						sum+=pixels[i+x,j+y]#*(2*(depth+1)-abs(x)-abs(y))
					elif(x>0):
						sum-=pixels[i+x,j+y]#*(2*(depth+1)-abs(x)-abs(y))
					
					if(y<0):
						sumB+=pixels[i+x,j+y]
					elif(y>0):
						sumB-=pixels[i+x,j+y]
			sum = brightness*(sum+sumB)/2
			if(abs(sum)>thresh):
				if(sum>255):
					sum = 255
				sum = int(sum)
				newPixels[i,j] = sum
			sum = 0
			sumB = 0
	newImage.show()
	return newImage

	
	
class Pixel(object):
	def __init__(self,coordinates,color): # coordinates is a tuple, color is a single int
		self.coord = coordinates
		self.color = color # single integer color (for grayscale images)
	
	def getCoord(self):
		return self.coord
	def getColor(self):
		return color
	
	def __eq__(self,other):
		if isinstance(other,self.__class__):
			return self.color == other.color
		elif isinstance(other,int):
			return self.color == other
		else:
			return false
	def __lt__(self,other):
		if isinstance(other,self.__class__):
			return self.color < other.color
		elif isinstance(other,int):
			return self.color < other
	def __gt__(self,other):
		if isinstance(other,self.__class__):
			return self.color > other.color
		elif isinstance(other,int):
			return self.color > other
			

	
def edge_refine(image,square_size=60,freq=50,heapsize=50):
	width,height = image.size
	pixels = image.load()
	
	newImage = Image.new('1',(width,height),"black")
	newPixels = newImage.load()
	
	heap = []
	
	output = []
	
	for i in range(0,width,freq):
		for j in range(0,height,freq):
			for x in range(-square_size/2,square_size/2): # using half sqare_size so that square_size will more accurately represent the length of the square
				for y in range(-square_size/2,square_size/2):
					if i+x >= 0 and i+x <width and j+y >=0 and j+y<height:
						if(len(heap)>0):
							if pixels[i+x,j+y] > heap[0]:
								heapq.heappush(heap,Pixel((i+x,j+y),pixels[i+x,j+y]))
						else:
							heapq.heappush(heap,Pixel((i+x,j+y),pixels[i+x,j+y]))
						if(len(heap)>heapsize):
							heapq.heappop(heap)
			for pix in heap:
				newPixels[(pix.getCoord)] = 1
			output+=heap
			heap = []
				
	newImage.show()
	return output			



def main():
	filename = raw_input("Enter location and name of image: ")
	image = Image.open(filename)
	newImage = edge_detect(image)
	edge_refine(newImage)
main()