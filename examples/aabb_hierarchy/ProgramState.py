import FileObj3d
import copy

class ProgramState:
	def __init__(self, cam_dir):
		self.model = FileObj3d.FileObj3d()
		self.node  = None

		self.level = 0
		self.max_level = 0

		self.cam_dir   = cam_dir
		self.start_dir = copy.deepcopy(cam_dir)
		self.cam_scale = 1.0
		self.inter_x = 0
		self.inter_y = 0
		self.inter_type = -1

	def __str__ (self):
		return str(self.node) + " at level " + str(self.level)
	

