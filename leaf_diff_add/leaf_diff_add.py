"""

    Difference and Addition Operations Over A Leaf Image with Python and OpenCV  
    
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.
    
    You should have received a copy of the GNU General Public License
    along with this program. If not, see <http://www.gnu.org/licenses/>.
    
    Copyright (C) 2012 Enes Ates
    
    Authors: Enes Ates - enes@enesates.com

"""

import cv, sys

image_file_name = "leaf.jpg"

# create images
leaf = cv.LoadImage(image_file_name, cv.CV_LOAD_IMAGE_COLOR)
gray_leaf = cv.CreateImage( cv.GetSize(leaf), 8, 1 )
gray_3_channels = cv.CreateImage( cv.GetSize(leaf), 8, 3 )
diff = cv.CreateImage( cv.GetSize(leaf), 8, 3 )
add = cv.CreateImage( cv.GetSize(leaf), 8, 3 )

# convert bgr to gray the leaf image and again gray to bgr
cv.CvtColor(leaf, gray_leaf, cv.CV_BGR2GRAY)
cv.CvtColor(gray_leaf, gray_3_channels, cv.CV_GRAY2BGR)

# difference and addition operations
cv.AbsDiff(leaf, gray_3_channels, diff)
cv.Add(leaf, gray_3_channels, add)

# show images
cv.ShowImage("leaf", leaf)
cv.ShowImage("gray_leaf", gray_leaf)
cv.ShowImage("gray_3_channels", gray_3_channels )
cv.ShowImage("diff", diff)
cv.ShowImage("add", add)



while True:
    if cv.WaitKey(0) == 27: # ESC
        break
   
sys.exit()