#!/Library/Frameworks/Python.framework/Versions/3.8/bin/python3 -u

import sys
import os
import shutil
import sqlite3
from PIL import Image, ImageDraw, ImageFont

def format( val, len=0 ):
	val = str(val)
	if len >0:
		val = val.rjust(len)
	return val

def minutes( val ):
	val = F'{(int(val)//60)}'
	return format( val, 3)

def po2( mv, ratio ):
	val = round(float(mv) *ratio, 2)
	val = '%.2f' % val
	if val[0] == '0':
		val = val.replace( '0.', '  .')
	return val

def depth( val):
	val = round(float(val))
	return format( F'{val}', 3)

def dil( o2, he):
	if float(o2) < .10:
		space = 6
	else:
		space = 5

	if he == '0':
		return format( '%d/00' % (float(o2) * 100), space)
	else:
		return format( '%d/%d' % ( float(o2) * 100, float(he) * 100), space)
 
def to_int( f ):
	return int(round(f))

def draw(log_dict, ceils, Sensors, count):

	k = 1.5 #set the frame size
	size = (to_int(320 * k), to_int(240 * k))

	row1 = 0
	row2 = to_int(25 * k)
	row3 = to_int(90 * k)
	row4 = to_int(158 * k)
	row5 = to_int(182 * k)

	cell1 = to_int(7 * k)
	cell2 = to_int(95 * k)
	cell3 = to_int(181 * k)
	cell4 = to_int(255 * k)

	try:
		shutil.rmtree('output')
	except OSError as e:
		print (F"Error1: {e.filename} - {e.strerror}.")

	os.makedirs('output')

	for i in range( count ):
		img = Image.new('RGB', size, color = (0, 0, 0))
		path = os.path.dirname(os.path.realpath(__file__))
		fnt1 = ImageFont.truetype( path + '/tahoma.ttf', to_int(25 * k))
		fnt2 = ImageFont.truetype( path + '/ARIALN.TTF', to_int(55 * k))
		d = ImageDraw.Draw(img)
	
		#write text
		d.text((to_int(2 * k), row1), "DEPTH", font=fnt1, fill=(35, 204, 252))
		d.text((to_int(100 * k), row1), "TIME", font=fnt1, fill=(35, 204, 252))
		d.text((to_int(182 * k), row1), "STOP", font=fnt1, fill=(35, 204, 252))
		d.text((to_int(260 * k), row1), "TIME", font=fnt1, fill=(35, 204, 252))
 	
	
		d.text((to_int(79 * k), row4), "O2/HE", font=fnt1, fill=(35, 204, 252))
		if ceils[i] > 0:
			d.text((to_int(190 * k), row4), " CEIL", font=fnt1, fill=(35, 204, 252))
		else:
			d.text((to_int(190 * k), row4), " NDL", font=fnt1, fill=(35, 204, 252))
	
		d.text((to_int(270 * k), row4), "TTS", font=fnt1, fill=(35, 204, 252))
	
		#write data
		d.text((cell1, row2), depth(log_dict['currentDepth'][i]), font=fnt2, fill=(255, 255, 255))
		d.text((cell2, row2), minutes(log_dict['currentTime'][i]), font=fnt2, fill=(255, 255, 255))
		if log_dict['firstStopDepth'][i] != '0':
			d.text((cell3, row2), format(log_dict['firstStopDepth'][i], 3), font=fnt2, fill=(255, 255, 255))
			d.text((cell4, row2), format(log_dict['firstStopTime'][i], 3),font=fnt2, fill=(255, 255, 255))
	
		val = po2(log_dict['sensor1Millivolts'][i], Sensors[0])
		if float( val ) > 1.6 or float( val ) < 0.4:
			d.text((2,row3), val, font=fnt2, fill=(255, 0, 0))
		else:
			d.text((2,row3), val, font=fnt2, fill=(255, 255, 255))

		val = po2(log_dict['sensor2Millivolts'][i], Sensors[1])
		if float( val ) > 1.6 or float( val ) < 0.4:
			d.text((to_int(117 * k), row3), val, font=fnt2, fill=(255, 0, 0))
		else:
			d.text((to_int(117 * k), row3), val, font=fnt2, fill=(255, 255, 255))

		val = po2(log_dict['sensor3Millivolts'][i], Sensors[2])
		if float( val ) > 1.6 or float( val ) < 0.4:
			d.text((to_int(229 * k), row3), val, font=fnt2, fill=(255, 0, 0))
		else:
			d.text((to_int(229 * k), row3), val, font=fnt2, fill=(255, 255, 255))

		# write CC
		d.text((to_int(2 * k), row5), '0', font=fnt2, fill=(255, 255, 255))
		d.rectangle((to_int((2 + 18) * k), row5 + (21 * k), to_int((2 + 28) * k), row5 + to_int((41 * k ))), fill=(0, 0, 0))
		d.text((27 * k, row5), '0', font=fnt2, fill=(255, 255, 255))
		d.rectangle((to_int((27 + 18) * k), row5 + to_int((21 * k)), to_int((27 + 28) * k), row5 + to_int((41 * k))), fill=(0, 0, 0))

		d.text((to_int(57 * k), row5), dil( log_dict['FractionO2'][i], log_dict['FractionHe'][i]), font=fnt2, fill=(255, 255, 255))
	
		if ceils[i] > 0:
			d.text((cell3, row5), format( '%d' % ceils[i], 3), font=fnt2, fill=(255, 255, 255))
		else:
			d.text((cell3, row5), format(log_dict['currentNDL'][i], 3), font=fnt2, fill=(255, 255, 255))
	
		d.text((cell4,row5), format(log_dict['ttsMins'][i], 3), font=fnt2, fill=(255, 255, 255))
		img.save(F'output/divelog{i}.png')

#get avearge PO2/mv ratio for each sensor
def calibrate( log_dict, count):
	Sensors = [0, 0, 0]
	for i in range( count ):
		for j in range(3):
			Sensors[j] += float(log_dict['averagePPO2'][i])/float(log_dict[F'sensor{j+1}Millivolts'][i])

	for j in range(3):
		Sensors[j] = Sensors[j] / count;

	return Sensors

def normalize( log_dict, ceils, count ): #removing ceiling peaks

	window = 4
	threshold = 0.14
	norm_ceils = [value for value in ceils]
	for i in range(count):
		if ceils[i] > 10: #ignore shallow depths
			avg = 0
			for j in range( i - window, i + window + 1 ):
				avg += ceils[j]
			avg = avg/float(window*2 + 1)
			if abs((avg-ceils[i])/avg) > threshold:
				norm_ceils[i] = min(int(avg), int(log_dict['firstStopDepth'][i]))

	return norm_ceils

def ceiling( log_dict, count):

	ceils = [0 for i in range( count)]

	t1 = 0
	d1 = 0
	d2 = 0
	calc = '' 
	for i in range( count ):
		if int(log_dict['firstStopDepth'][i]) != d1:
			if d1 != 0:
				if int(log_dict['firstStopDepth'][i]) > d2: #descent

					for j in range( t1, i ):
						ceils[j] = max(d2 + ((d1-d2) * (j - t1 + 1) )/(i - t1), d2 + 1 )

				elif int(log_dict['firstStopDepth'][i]) == d2: #flat
					for j in range( t1, i ):
						ceils[j] = d1 - 9

				else: #ascent
					for j in range( t1, i ):
						ceils[j] = max( d1 - ((d2-d1) * (j - t1 + 1) )/(i - t1), int(log_dict['firstStopDepth'][i]) + 1)

			d2 = d1
			d1 = int(log_dict['firstStopDepth'][i])
			t1 = i

	return normalize( log_dict, ceils, count )
	
def main():
	if len(sys.argv) < 2:
		print ("use ./divelog.py <ShearWater.db> <diveNumber>")
		exit()

	conn = sqlite3.connect(sys.argv[1])
	cur = conn.cursor()
	sql = F"SELECT currentTime, currentDepth, ttsMins, averagePPO2, FractionO2, FractionHe, currentNDL, firstStopDepth, firstStopTime, \
	              decoCeiling, sensor1Millivolts, sensor2Millivolts, sensor3Millivolts\
	       FROM dive_log_records dlr \
	       JOIN dive_logs dl on (dlr.DiveLogId = dl.diveId) \
	      WHERE number = {sys.argv[2]} \
	      ORDER BY dlr.id"

	cur.execute( sql )
	rows = cur.fetchall()
	count = len(rows)

	headings = ("currentTime", "currentDepth", "ttsMins", "averagePPO2", "FractionO2", "FractionHe", "currentNDL", "firstStopDepth", "firstStopTime", "decoCeiling", "sensor1Millivolts", "sensor2Millivolts", "sensor3Millivolts" )
	log_dict = {}

	for row in rows:
		for col_header, data_column in zip( headings, row ):
			log_dict.setdefault(col_header, []).append(data_column)
			

#	print( headings )
#	print(F'Processed {len(rows)} lines.') 

	Sensors = calibrate( log_dict, count)
	ceils = ceiling( log_dict, count )

	draw( log_dict, ceils, Sensors, count )
	exit()

if __name__ == "__main__":
	main()

