import math

def get_spiral_pointer(stride = 30):
	a = 5
	b = 1
	x = []
	y = []
	for angle in range(0,3*360,stride):
	    rads = math.radians(angle)
	    r = a+b*rads
	    y.append(r*math.sin(rads))
	    x.append(r*math.cos(rads))
	return x,y
