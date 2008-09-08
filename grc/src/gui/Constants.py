"""
Copyright 2008 Free Software Foundation, Inc.
This file is part of GNU Radio

GNU Radio Companion is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

GNU Radio Companion is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA
"""

##################################################
## Global Titles
##################################################

##The name to appear in the main window for a flow graph that has not been saved to file.
NEW_FLOGRAPH_TITLE = 'untitled'

##The prefix title on the main window.
MAIN_WINDOW_PREFIX = "GRC"

##################################################
## Signal block rotations
##################################################

##direction of rotation left.
DIR_LEFT = 'left'

##direction of rotation right.
DIR_RIGHT = 'right'

##################################################
## Dimension constraints for the various windows (in pixels)
##################################################

##main window constraints
MIN_WINDOW_WIDTH = 600
MIN_WINDOW_HEIGHT = 400

##dialog constraints
MIN_DIALOG_WIDTH = 500
MIN_DIALOG_HEIGHT = 500

##static height of reports window
REPORTS_WINDOW_HEIGHT = 100

##static width of block selection window
BLOCK_SELECTION_WINDOW_WIDTH = 200

##################################################
## Dragging, scrolling, and redrawing constants for the flow graph window in pixels
##################################################

##How close can the mouse get to the window border before mouse events are ignored.
BORDER_PROXIMITY_SENSITIVITY = 50

##How close the mouse can get to the edge of the visible window before scrolling is invoked.
SCROLL_PROXIMITY_SENSITIVITY = 30

##When the window has to be scrolled, move it this distance in the required direction.
SCROLL_DISTANCE = 15

##The redrawing sensitivity, how many seconds must pass between motion events before a redraw?
MOTION_DETECT_REDRAWING_SENSITIVITY = .02

##How close the mouse click can be to a connection and register a connection select.
CONNECTION_SELECT_SENSITIVITY = 5

##################################################
# A state is recorded for each change to the flow graph, the size dictates how many states we can record
##################################################

##The size of the state saving cache in the flow graph (for undo/redo functionality)
STATE_CACHE_SIZE = 42