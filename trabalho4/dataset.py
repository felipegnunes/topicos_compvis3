import numpy as np

import image_manip

class Dataset:
	
	def __init__(self, X, y, batch_size):
		self.X = X
		self.y = y
		self.num_samples = X.shape[0]
		self.batch_size = batch_size
		self.index = 0
	
	def next_batch(self, augment = False):
		if self.index + self.batch_size > self.num_samples:
			X_batch = np.copy(self.X[self.index : ])
			y_batch = np.copy(self.y[self.index : ])
			
			permutation = np.random.permutation(self.num_samples)
			self.X = self.X[permutation]
			self.y = self.y[permutation]
			
			self.index = (self.index + self.batch_size) % self.num_samples
		
			X_batch = np.concatenate((X_batch, self.X[ : self.index]), axis = 0)
			y_batch = np.concatenate((y_batch, self.y[ : self.index]), axis = 0)
			
		else:	
			X_batch = self.X[self.index : self.index + self.batch_size]
			y_batch = self.y[self.index : self.index + self.batch_size] 
			self.index = (self.index + self.batch_size) % self.num_samples
		
		if augment:
			X_batch = image_manip.perturbate_randomly(X_batch, 
													  horizontal_shift_range = (-10, 10), 
													  vertical_shift_range = (-10, 10), 
													  angle_range = (-10, 10), 
													  contrast_alpha_range = (.8, 1.2), 
													  zoom_factor_range = (.8, 1.2)
													 )
			
		return X_batch, y_batch
	
	def on_last_batch(self):
		return self.index + self.batch_size >= self.num_samples	
