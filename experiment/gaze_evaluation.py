"""
vexptoolbox eye tracker validation experiment
version 1.1 - March 2021
immo.schuetz@psychol.uni-giessen.de
"""

import os
import time
import random

import viz
import vizact
import viztask
import vizinfo
import vizshape
import vizinput
import steamvr

import vexptoolbox as vfx


# Set EXE parameters
viz.setOption('viz.publish.persistent', 1)
viz.setOption('viz.publish.product', 'gaze_evaluation')
viz.setOption('viz.publish.company', 'fiehlerlab')
viz.setOption('viz.publish.persist_folder', '<temp>/<product>')
data_path = os.path.expandvars(r'%TEMP%\gaze_evaluation\Application\Script')
viz.setLogFile('gaze_eval_log.txt')

# ID string of the lab this tool was built for
# this is hashed and thus anonymized during analysis!
LAB = 'JLU_KF'

# File format version string
VERSION = '1.1'

# Set up Vive Pro Eye HMD
viz.setMultiSample(8)
viz.go()
 
# Select eye tracking and display hardware
opt = {}
hardware = ['VR disabled', 'Vive Pro Eye', 'Vive', 'Vive + Pupil Labs']
opt['hw'] = vizinput.choose('Select HMD/Tracker type', hardware, 0)

# Initialize the selected eye tracker
opt['et'] = False

if opt['hw'] == 1:
	
	# Vive Pro Eye eye tracker via SRanipal SDK
	hmd = steamvr.HMD()
	if not hmd.getSensor():
		sys.exit('Vive not detected')
	hmd.setMonoMirror(True)
	
	VivePro = viz.add('VivePro.dle')
	eyeTracker = VivePro.addEyeTracker()
	if not eyeTracker:
		sys.exit('Eye tracker not detected')

	navigationNode = viz.addGroup()
	viewLink = viz.link(navigationNode, viz.MainView)
	viewLink.preMultLinkable(hmd.getSensor())
	opt['et'] = True


elif opt['hw'] == 2:
	
	# Vive Classic with no eye tracking
	hmd = steamvr.HMD()
	if not hmd.getSensor():
		sys.exit('Vive not detected')
	hmd.setMonoMirror(True)
	
	navigationNode = viz.addGroup()
	viewLink = viz.link(navigationNode, viz.MainView)
	viewLink.preMultLinkable(hmd.getSensor())
	
	# Create a dummy eye tracker object facing straight ahead
	eyeTracker = vizshape.addSphere(axis=vizshape.AXIS_Z)
	eyeTracker.setEuler(0, 0, 0)
	eyeTracker.visible(False)


elif opt['hw'] == 3:
	
	# Pupil Labs HTC Vive Add-on
	hmd = steamvr.HMD()
	if not hmd.getSensor():
		sys.exit('Vive not detected')
	hmd.setMonoMirror(True)
	
	PupilLabs = viz.add('PupilLabs.dle')
	eyeTracker = PupilLabs.addEyeTracker(address='127.0.0.1:50020')
	if not eyeTracker:
		sys.exit('Eye tracker not detected')
	print('* TRACKER TYPE: "{:s}"'.format(type(eyeTracker).__name__))
	navigationNode = viz.addGroup()
	viewLink = viz.link(navigationNode, viz.MainView)
	viewLink.preMultLinkable(hmd.getSensor())
	opt['et'] = True
	
	# DEBUG while testing with TUC
	print('* TRACKER TYPE: "{:s}"'.format(type(eyeTracker).__name__))


else:
	
	# Create a dummy eye tracker object facing straight ahead
	eyeTracker = vizshape.addSphere(axis=vizshape.AXIS_Z)
	eyeTracker.setEuler(0, 0, 0)
	eyeTracker.visible(False)
	

# Set up demo scene
viz.addChild('ground_wood.osgb')
viz.MainView.getHeadLight().disable()
viz.addLight(euler=(30, 0, 0), color=viz.WHITE)
viz.addLight(euler=(-30, 0, 0), color=viz.WHITE)

# Custom validation targets
#   7x7 full square, +/- 15 deg, 6m distance
# + 7x7 major positions, +/- 10 deg, 0.5m distance
# Note: 5min license manages ~78 targets

targets =  [[0.0,  0.0,   6.0],
			[5.0,  0.0,   6.0],
			[0.0,  -5.0,  6.0],
			[-5.0, 0.0,   6.0],
			[0.0,  5.0,   6.0],
			[5.0,  5.0,   6.0],
			[5.0,  -5.0,  6.0],
			[-5.0, -5.0,  6.0],
			[-5.0,  5.0,  6.0],
			[10.0, 0.0,   6.0],
			[0.0, -10.0,  6.0],
			[-10.0, 0.0,  6.0],
			[0.0,  10.0,  6.0],
			[10.0, 10.0,  6.0],
			[10.0, -10.0, 6.0],
			[-10.0,-10.0, 6.0],
			[-10.0, 10.0, 6.0],
			[10.0, 5.0,   6.0],
			[10.0, -5.0,  6.0],
			[5.0, -10.0,  6.0],
			[-5.0, -10.0, 6.0],
			[-10.0, -5.0, 6.0],
			[-10.0, 5.0,  6.0],
			[-5.0, 10.0,  6.0], 
			[5.0, 10.0,   6.0],
			[15.0, 0.0,   6.0],
			[0.0, -15.0,  6.0],
			[-15.0, 0.0,  6.0],
			[0.0, 15.0,   6.0],
			[15.0, 15.0,  6.0],
			[15.0, -15.0, 6.0],
			[-15.0,-15.0, 6.0],
			[-15.0, 15.0, 6.0],
			[15.0, 10.0,  6.0],
			[15.0, 5.0,   6.0],
			[15.0, -5.0,  6.0],
			[15.0, -10.0, 6.0],
			[10.0, -15.0, 6.0],
			[5.0, -15.0,  6.0],
			[-5.0, -15.0, 6.0],
			[-10.0,-15.0, 6.0],
			[-15.0,-10.0, 6.0],
			[-15.0, -5.0, 6.0],
			[-15.0, 5.0,  6.0],
			[-15.0, 10.0, 6.0],
			[-10.0, 15.0, 6.0],
			[-5.0, 15.0,  6.0],
			[5.0, 15.0,   6.0],
			[10.0, 15.0,  6.0], # N=49 @ 6m
			
			[0.0,  0.0,   0.5],	
			[5.0,  0.0,   0.5],
			[0.0,  -5.0,  0.5],
			[-5.0, 0.0,   0.5],
			[0.0,  5.0,   0.5],
			[5.0,  5.0,   0.5],
			[5.0,  -5.0,  0.5],
			[-5.0, -5.0,  0.5],
			[-5.0,  5.0,  0.5],
			[10.0, 0.0,   0.5],
			[0.0, -10.0,  0.5],
			[-10.0, 0.0,  0.5],
			[0.0,  10.0,  0.5],
			[10.0, 10.0,  0.5],
			[10.0, -10.0, 0.5],
			[-10.0,-10.0, 0.5],
			[-10.0, 10.0, 0.5],
			[10.0, 5.0,   0.5],
			[10.0, -5.0,  0.5],
			[5.0, -10.0,  0.5],
			[-5.0, -10.0, 0.5],				
			[-10.0, -5.0, 0.5],
			[-10.0, 5.0,  0.5],
			[-5.0, 10.0,  0.5], 
			[5.0, 10.0,   0.5]] # N=25 @ 0.5m 


def inputMetadata():
	""" Shows a vizinfo UI to collect participant metadata """
	
	ui = vizinfo.InfoPanel('', title='Participant Info', icon=False, align=viz.ALIGN_CENTER_CENTER)
	uid = {}
	uid['part_id'] = ui.addLabelItem('Participant ID', viz.addTextbox())
	uid['session'] = ui.addLabelItem('Session', viz.addTextbox())
	uid['headset'] = ui.addLabelItem('Headset', viz.addTextbox())
	ui.addSeparator()
	ui.addItem(viz.addText('These fields are only needed for\nthe first session of each participant.'))
	uid['age'] = ui.addLabelItem('Age', viz.addTextbox())
	uid['gender'] = ui.addLabelItem('Gender',viz.addDropList())
	uid['gender'].addItems([' ', 'female', 'male', 'non-binary', 'prefer not to say'])
	uid['vision'] = ui.addLabelItem('Vision correction',viz.addDropList())
	uid['vision'].addItems(['uncorrected', 'glasses', 'contacts'])
	uid['prescriptionL'] = ui.addLabelItem('Prescription (L)', viz.addTextbox())
	uid['prescriptionR'] = ui.addLabelItem('Prescription (R)', viz.addTextbox())
	ui_submit = ui.addItem(viz.addButtonLabel('Submit'), align=viz.ALIGN_RIGHT_CENTER)
	ui.renderToEye(viz.RIGHT_EYE)

	yield viztask.waitButtonDown(ui_submit)

	metadata = {}
	for elem in ['part_id', 'session', 'age', 'prescriptionL', 'prescriptionR', 'headset']:
		metadata[elem] = uid[elem].get()
	for elem in ['gender', 'vision']:
		metadata[elem] = uid[elem].getItems()[uid[elem].getSelection()]
	
	ui.remove()
	viztask.returnValue(metadata)


def buildRandomScene(num_objs=15):
	""" Create a simple scene with random geometric objects """
	COLORS = [[0.8941, 0.102 , 0.1098], # colorbrewer Set1
			  [0.2157, 0.4941, 0.7216],
			  [0.302 , 0.6863, 0.2902],
			  [0.5961, 0.3059, 0.6392],
			  [1.    , 0.498 , 0.    ],
			  [1.    , 1.    , 0.2   ],
			  [0.651 , 0.3373, 0.1569],
			  [0.9686, 0.5059, 0.749 ],
			  [0.6   , 0.6   , 0.6   ]]

	obj_list = []
	for c in range(0, num_objs):
		size = random.random() * 1.0
		pos = [(random.random() - 0.5) * 10,
				float(size) / 2,
				(random.random() * 10) + 2.0]
		color = random.sample(COLORS, 1)[0]		
		if random.random() > 0.5:
			obj = vizshape.addCube(size=size, pos=pos, color=color)
			otype = 'cube'
		else:
			obj = vizshape.addSphere(radius=size/2, pos=pos, color=color)
			otype = 'sphere'

		obj_list.append({'type': otype, 'size': size, 'color': str(color), 
					     'x': pos[0], 'y': pos[1], 'z': pos[2]})
	return obj_list


def MainTask():
	""" Main experimental task """
	
	# Get participant metadata
	m = yield inputMetadata()
	
	# Add hardware metadata
	m['lab'] = LAB
	m['task_version'] = VERSION
	m['engine'] = 'vizard'
	m['engine_version'] = viz.version()
	m['platform'] = viz.getOption('platform.name')
	m['eye_tracker'] = type(eyeTracker).__name__
	
	# Set output file name
	file_out = 'eval_{:s}_{:s}_{:s}'.format(m['part_id'], m['session'], time.strftime('%Y%m%d_%H%M%S', time.localtime()))

	# Run manufacturer calibration
	gtool = vfx.SampleRecorder(eyeTracker, DEBUG=True)
	if opt['et']:
		mt = yield vfx.waitVRText('Press SPACE to start eye tracker calibration, S to skip!', keys=(' ', 's'))
		if mt.key != 's':
			print(eyeTracker.calibrate())

	# Keep a recording of validation session
	yield gtool.startRecording(force_update=True)
	yield viztask.waitTime(1)

	# Static validation task
	yield vfx.waitVRText('Press SPACE to start validation task!\nFixate the center dot of each target until it turns green.')
	vdata = yield gtool.validateEyeTracker(targets=targets, randomize=True, metadata=m)	
	print(vdata)
	
	# VOR validation task
	msg = 'Please rotate your head around while keeping your eyes fixed on the red sphere (20s).\n'
	msg += 'Press SPACE to start!'
	yield vfx.waitVRText(msg, keys=(' '))
	gtool.recordEvent('VOR_START')
	vor_tar = vizshape.addSphere(radius=0.05, color=[1.0, 0.0, 0.0])
	vor_tar.setPosition([0.0, 1.5, 6.0])
	yield viztask.waitTime(20)
	gtool.recordEvent('VOR_END')
	vor_tar.remove()
	
	# Free viewing (30 sec)
	yield vfx.waitVRText('Please look at the random objects in the scene (30s).\nPress SPACE to start!')
	scene = buildRandomScene()
	gtool.recordEvent('FREEVIEW_START')
	yield viztask.waitTime(30)
	gtool.recordEvent('FREEVIEW_END')

	yield vfx.showVRText('Finished. Thank you!')

	# Save data
	m['scene'] = scene # Keep displayed random object data
	vdata.metadata.update(m)
	vdata.toJSONFile(json_file='{:s}_res.json'.format(file_out))
	vdata.toPickleFile(pickle_file='{:s}_res.pkl'.format(file_out))
	gtool.stopRecording()
	gtool.saveRecording('{:s}_samp.csv'.format(file_out), '{:s}_ev.csv'.format(file_out))

	print('Finished. Total runtime:  {:.1f} seconds / {:.1f} min'.format(viz.tick(), viz.tick()/60))
	
	if viz.res.isPublished():
		# In published mode, data goes into a temporary folder
		msg = 'Finished. Data files are in: {:s}'.format(data_path)
		print(msg)
		os.startfile(data_path) # Show data folder
		viz.message(msg)		
	viz.quit()


viztask.schedule(MainTask)