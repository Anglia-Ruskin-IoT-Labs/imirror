from enum import Enum


class Position():
	"""[summary]
	
	Returns:
		[type] -- [description]
	"""
	def __init__(self, _col: int, _row: int, _align: str, _name: str):
		self.column = _col
		self.row = _row
		self.alignment = _align
		self.representation = _name
		
	def __repr__(self):
		return str(self.representation)

class Pos(Enum):
    TOPLEFT = Position(1, 1, "nw", 'TOPLEFT')
    TOPMID = Position(2, 1, "n", 'TOPMID')
    TOPRIGHT = Position(3, 1, "ne", 'TOPRIGHT')
    MIDLEFT = Position(1, 2, "w", 'MIDLEFT')
    MIDMID = Position(2, 2, "ns", 'MIDMID')
    MIDRIGHT = Position(3, 2, "e", 'MIDRIGHT')
    BOTLEFT = Position(1, 3, "sw", 'BOTLEFT')
    BOTMID = Position(2, 3, "s", 'BOTMID')
    BOTRIGHT = Position(3, 3, "se", 'BOTRIGHT')


def PositionResolver( _config: str) -> Position:
	if _config == str(Pos.TOPLEFT.name):
		return Pos.TOPLEFT
	elif _config == str(Pos.TOPMID.name):
		return Pos.TOPMID
	elif _config == str(Pos.TOPRIGHT.name):
		return Pos.TOPRIGHT
	elif _config == str(Pos.MIDLEFT.name):
		return Pos.MIDLEFT
	elif _config == str(Pos.MIDMID.name):
		return Pos.MID
	elif _config == str(Pos.MIDRIGHT.name):
		return Pos.MIDRIGHT
	elif _config == str(Pos.BOTLEFT.name):
		return Pos.BOTLEFT
	elif _config == str(Pos.BOTMID.name):
		return Pos.BOTMID
	elif _config == str(Pos.BOTRIGHT.name):
		return Pos.BOTRIGHT
	else:
		return None




