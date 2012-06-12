import sys
import kalman
from numpy import *

dt = 1.0 / 2500.0
process_sigmasq = 3.0
measurement_sigmasq = 1.0

t = kalman.kalman(
	x=zeros((9,1)),
	P=array([
		[10., 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
		[0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
		[0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
		[0.0, 0.0, 0.0, 10., 0.0, 0.0, 0.0, 0.0, 0.0],
		[0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0],
		[0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0],
		[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 10., 0.0, 0.0],
		[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
		[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]]),
)

process = kalman.process_model(
	F=array([
		[1.0,  dt, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
		[0.0, 1.0,  dt, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
		[0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
		[0.0, 0.0, 0.0, 1.0,  dt, 0.0, 0.0, 0.0, 0.0],
		[0.0, 0.0, 0.0, 0.0, 1.0,  dt, 0.0, 0.0, 0.0],
		[0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0],
		[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0,  dt, 0.0],
		[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0,  dt],
		[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]]),
	Q=array([
		[dt ** 4 / 4, dt ** 3 / 3,         0.0,         0.0,         0.0,         0.0,         0.0,         0.0,         0.0],
		[dt ** 3 / 3,     dt ** 2, dt ** 3 / 3,         0.0,         0.0,         0.0,         0.0,         0.0,         0.0],
		[        0.0, dt ** 3 / 3,          dt, dt ** 3 / 3,         0.0,         0.0,         0.0,         0.0,         0.0],
		[        0.0,         0.0, dt ** 3 / 3, dt ** 4 / 4, dt ** 3 / 3,         0.0,         0.0,         0.0,         0.0],
		[        0.0,         0.0,         0.0, dt ** 3 / 3,     dt ** 2, dt ** 3 / 3,         0.0,         0.0,         0.0],
		[        0.0,         0.0,         0.0,         0.0, dt ** 3 / 3,          dt, dt ** 3 / 3,         0.0,         0.0],
		[        0.0,         0.0,         0.0,         0.0,         0.0, dt ** 3 / 3, dt ** 4 / 4, dt ** 3 / 3,         0.0],
		[        0.0,         0.0,         0.0,         0.0,         0.0,         0.0, dt ** 3 / 3,     dt ** 2, dt ** 3 / 3],
		[        0.0,         0.0,         0.0,         0.0,         0.0,         0.0,         0.0, dt ** 3 / 3,          dt]]) * process_sigmasq
)

accel = kalman.observation_model(
	H = [
		[0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
		[0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0],
		[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]],
	R = [
		[measurement_sigmasq, 0.0, 0.0],
		[0.0, measurement_sigmasq, 0.0],
		[0.0, 0.0, measurement_sigmasq]]
)

gps = kalman.observation_model(
	H = [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0]],
	R = [[measurement_sigmasq]]
)

for line in sys.stdin:
	li = line.split('\t')
	if li[0] == 'accel':
		t.update(accel, float(li[2]), float(li[3]), -float(li[4]) - 9.80665)
	elif li[0] == 'pressure':
		t.update(gps, float(li[2]))
	else:
		continue
	t.predict(process)
	print li[1], t.x[6][0], t.x[7][0], t.x[8][0]
