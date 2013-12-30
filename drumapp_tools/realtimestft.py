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
	
	## Set initial view bounds
	view.setRange(QtCore.QRectF(0, 0, howmanycols, framesize))
	
	# initialize first "chunk" is silence
	data1 = np.zeros(chunksize)
	
	# loop as long as window is not closed              
	while not win.isHidden():
	
		# record next chunk
		data2 = utils.chunks_to_numpy([audioio.record_single_chunk(channels=1, chunk=chunksize)])
		# compute fft
		new_col = np.abs(np.fft.rfft(np.append(data1, data2) * np.hamming(fftsize)))
		# new fft is last column in data to be displayed
		data = np.append(data[1:], new_col.reshape(1, framesize), axis=0)
		
		# display data
		img.setImage(data)
		pg.QtGui.QApplication.processEvents()
		
		# new chunk in this loop pass is the chunk before in next loop pass
		data2 = data1
	
	QtGui.QApplication.quit()