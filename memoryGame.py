
import random
class tile:
    flipped=False
    def _init_(self, image):
        self.image=image
    def getImage(self):
        if(self.flipped):
            return self.image
        else:
            return "_"
def printTiles(tiles):
	mess=""
	for i in tiles:
		row=""
		for j in i:
			row+=j.getImage()+"    "
		mess+=row+"\n"
	return mess
def openTilePair(pair, tiles):
	if pair[0]==pair[1]:
		print(pair[0],"=",pair[1])
		return False
	t1=tiles[pair[0][0]][pair[0][1]]
	t2=tiles[pair[1][0]][pair[1][1]]
	t1.flipped=True
	t2.flipped=True
	
	if(t1.getImage()==t2.getImage()):
		print("Pair found")
	else:
		t1.flipped=False
		t2.flipped=False
		print("not a pair")
	if(gameEnd(tiles)):
		return "You won!"
	return printTiles(tiles)
def gameEnd(tiles):
	for i in tiles:
		for j in i:
			if(j.flipped==False):
				return False
	return True
class tileGame:
	images=["a","b","c","d","e","f","g","@","&","#","+","2","?","!","€","*","£","¢"]
	imagesTemp=[]
	def __init__(self):
		imagesTemp=[]
		for i in self.images:
			imagesTemp.append(i)
			imagesTemp.append(i)
		random.shuffle(imagesTemp)
		gridSide=6
		self.grid=[]
		for i in range(gridSide):
			self.grid.append([])
			for j in range(gridSide):
				self.grid[i].append(tile(imagesTemp.pop()))
		#return printTiles(self.grid)
		#while not(gameEnd(grid)):
		#	print("guess tile")
		#	try:
		#		x1=int(input("give x"))
		#		y1=int(input("give y"))
		#		x2=int(input("give x"))
		#		y2=int(input("give y"))
		#		openTilePair([[x1,y1],[x2,y2]],grid)
		#	except Exception as e:
		#		print(e)
