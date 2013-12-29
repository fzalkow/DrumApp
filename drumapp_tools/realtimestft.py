from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
import pyqtgraph as pg
import pyaudio
import audioio
import utils

def real_time_spectogram (fftsize=2**9):

	# start application
	app = QtGui.QApplication([])
	
	## Create window with GraphicsView widget
	win = pg.GraphicsLayoutWidget()
	win.show()  ## show widget alone in its own window
	win.setWindowTitle("Real-Time Spectogram")
	view = win.addViewBox()
	
	## lock the aspect ratio so pixels are always square
	view.setAspectLocked(True)
	
	## build loopup table
	pos = np.array([0.0, 0.5, 1.0])
	color = np.array([[0,0,0,255], [255,255,0,255], [255,0,0,255]], dtype=np.ubyte)
	map = pg.ColorMap(pos, color)
	lut = map.getLookupTable(0.0, 1.0, 256)
	
	## Create image item
	img = pg.ImageItem(border="w")
	view.addItem(img)
	img.setLookupTable(lut)
	
	## create empty data for initialization
	chunksize = fftsize/2
	framesize = len(np.fft.rfft(np.zeros(fftsize)))
	howmanycols = fftsize
	data = np.zeros((howmanycols, framesize))
	bordersize = (fftsize-chunksize)/2
	
	## Set initial view bounds
	view.setRange(QtCore.QRectF(0, 0, howmanycols, framesize))
	
	# read first data chunk, rest are zeros
	data1 = data[-2]
	data2 = data[-1]
	data3 =  utils.chunks_to_numpy([audioio.record_single_chunk(channels=1, chunk=chunksize)])
	
	# start inifinte loop                    
	while not win.isHidden():
	
		data1 = data2
		data2 = data3
		data3 = utils.chunks_to_numpy([audioio.record_single_chunk(channels=1, chunk=chunksize)])
										
		new_col = np.abs(np.fft.rfft(
								np.concatenate((data1[bordersize:], data2, data3[:bordersize]))))
		
		data = np.append(data[1:], new_col.reshape(1, framesize), axis=0)
		
		img.setImage(data)
		pg.QtGui.QApplication.processEvents()
	# how to really close the pg application??
	#pg.exit() # causes python to exist