"""

    Image Processing Program with OpenCV and PyGTK 
    
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

import cv
import pygtk
pygtk.require('2.0')
import gtk

class ImageProcessing:
    
    image_file_name = "images/tux.png"
    image = cv.LoadImage(image_file_name, cv.CV_LOAD_IMAGE_COLOR)
    pix = gtk.gdk.pixbuf_new_from_file("images/tux.png")
    window_width  = 980
    window_height = 680
    darea_width   = 560
    darea_height  = 560

    # FILTERS AND DETECTORS
    def smooth(self, widget, cv_smooth):
        
        cv.Smooth(self.image, self.image, cv_smooth, 3, 0, 0, 0)
        cv.ShowImage(self.image_file_name, self.image)
       
        
    def sobel(self, widget, gx, gy):
        
        cv.Sobel(self.image, self.image, gx, gy)
        cv.ShowImage(self.image_file_name, self.image)
        
        
    def laplace(self, widget):
        
        cv.Laplace(self.image, self.image)
        cv.ShowImage(self.image_file_name, self.image)
        
        
    def canny(self, widget):
        
        gray_image = cv.CreateImage(cv.GetSize(self.image), self.image.depth, 1)
        
        if self.image.nChannels != 1:
            cv.CvtColor(self.image, gray_image, cv.CV_BGR2GRAY)
            
        edge = cv.CreateImage(cv.GetSize(self.image), self.image.depth, 1)
        
        cv.Canny(gray_image, edge, 20, 100)
        
        self.image = edge
        cv.ShowImage(self.image_file_name, self.image)
        
        
    def corner_harris(self, widget):
        
        image = cv.CreateImage(cv.GetSize(self.image), self.image.depth, 1)
        
        if self.image.nChannels != 1:
            cv.CvtColor(self.image, image, cv.CV_BGR2GRAY)
        
        #image = cv.LoadImage(self.image_file_name, cv.CV_LOAD_IMAGE_GRAYSCALE)
        cornerMap = cv.CreateMat(image.height, image.width, cv.CV_32FC1)
        
        cv.CornerHarris(image, cornerMap, 5)
        
        for y in range(0, image.height):
            for x in range(0, image.width):
                harris = cv.Get2D(cornerMap, y, x) # get the x,y value
                # check the corner detector response
                if harris[0] > 10e-05:
                        # draw a small circle on the original image
                    cv.Circle(self.image, (x,y), 1, cv.RGB(155, 0, 25))
        
        cv.ShowImage(self.image_file_name, self.image)
    
        
    # MORPHOLOGY            
    def morphology_ex(self, widget, cv_mop):
        
        morph_image = cv.CloneImage(self.image)
        cv.MorphologyEx(self.image, morph_image, None, None, cv_mop, 1)
        
        self.image = morph_image
        cv.ShowImage(self.image_file_name, self.image) 
    
        
    # INTENSITY TRANSFORMATION
    def negative(self, widget):
        
        cv.Not(self.image, self.image)
        cv.ShowImage(self.image_file_name, self.image)
          
        
    def gamma_transformation(self, widget):

        cv.Pow(self.image, self.image, 2)
        cv.ShowImage(self.image_file_name, self.image)
      
  
    def histogram_equalization(self, widget):
        
        gray_image = cv.CreateImage(cv.GetSize(self.image), self.image.depth, 1)
       
        if self.image.nChannels != 1:
            cv.CvtColor(self.image, gray_image, cv.CV_BGR2GRAY)
        
        self.image = gray_image
    
        cv.EqualizeHist(self.image, self.image)
        cv.ShowImage(self.image_file_name, self.image)



    # VIDEO PROCESSING
    def play_video(self, widget):
        
        dialog = gtk.FileChooserDialog("Choose a Video", None, gtk.FILE_CHOOSER_ACTION_OPEN,
                               (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        dialog.set_default_response(gtk.RESPONSE_OK)
        file_filter = gtk.FileFilter()
        file_filter.set_name("Videos")
        file_filter.add_mime_type("video/avi")
        file_filter.add_pattern("*.avi")
        dialog.add_filter(file_filter)

        response = dialog.run()
        
        if response == gtk.RESPONSE_OK:
            
            video_file_name = dialog.get_filename()
            capture = cv.CaptureFromFile(video_file_name)
            fps = cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FPS)
            
            dialog.destroy()
            
            while True:
                
                frame = cv.QueryFrame(capture)
                
                if frame == None:
                    break;
                
                cv.ShowImage(video_file_name, frame)
            
                if fps!=0 :
                    wait_key = cv.WaitKey(int(1000/fps))
                else:
                    wait_key = cv.WaitKey(40)

                
                if wait_key == 27: # ESC
                    break
                
        elif response == gtk.RESPONSE_CANCEL:
            print "No file selected"

    
    # TOOLBAR FUNCTIONS
    def resize_image(self, widget):
        
        r_width  = int(self.resize_w_entry.get_text())
        r_height = int(self.resize_h_entry.get_text())

        r_image  = cv.CreateImage((r_width, r_height), self.image.depth, self.image.nChannels)
        cv.Resize(self.image, r_image)
        
        self.image = r_image
        
        cv.ShowImage(self.image_file_name, self.image)
                
    
    def crop_image(self, widget):
        
        c_left   = int(self.crop_l_entry.get_text())
        c_top    = int(self.crop_t_entry.get_text())
        c_width  = int(self.crop_w_entry.get_text())
        c_height = int(self.crop_h_entry.get_text())
        
        cropped = cv.CreateImage( (int(c_width), int(c_height)), self.image.depth, self.image.nChannels)
        src_region = cv.GetSubRect(self.image, (c_left, c_top, c_width, c_height))
        cv.Copy(src_region, cropped)
        
        self.image = cropped
        
        cv.ShowImage(self.image_file_name, self.image)
        
           
    def rotate_image(self, widget, flipMode):
        
        trans_image = cv.CreateImage((self.image.height,self.image.width), self.image.depth, self.image.channels)
        cv.Transpose(self.image, trans_image)
        cv.Flip(trans_image, trans_image, flipMode)
        
        self.image = trans_image
        cv.ShowImage(self.image_file_name, self.image)
   
   
    def open_image(self, widget):
        
        dialog = gtk.FileChooserDialog("Choose an Image", None, gtk.FILE_CHOOSER_ACTION_OPEN,
                               (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        dialog.set_default_response(gtk.RESPONSE_OK)
        file_filter = gtk.FileFilter()
        file_filter.set_name("Images")
        file_filter.add_mime_type("image/png")
        file_filter.add_mime_type("image/jpeg")
        file_filter.add_mime_type("image/gif")
        file_filter.add_pattern("*.png")
        file_filter.add_pattern("*.jpg")
        file_filter.add_pattern("*.gif")
        file_filter.add_pattern("*.tif")
        file_filter.add_pattern("*.xpm")
        dialog.add_filter(file_filter)

        response = dialog.run()
        
        if response == gtk.RESPONSE_OK:
            
            self.image_file_name = dialog.get_filename()
            self.image = cv.LoadImage(self.image_file_name, cv.CV_LOAD_IMAGE_COLOR)

            self.pix = gtk.gdk.pixbuf_new_from_file(dialog.get_filename())
            
            height = self.pix.get_height()
            width = self.pix.get_width()        
            
            if width > self.darea_width or height > self.darea_height :
                
                if width > height:
                   height = self.darea_height * height/width
                   width  = self.darea_width
                else:
                   width  = self.darea_width * width/height
                   height = self.darea_height
                   
            self.pix = self.pix.scale_simple(width, height, gtk.gdk.INTERP_BILINEAR)
            
        elif response == gtk.RESPONSE_CANCEL:
            print "No file selected"
            #raise SystemExit()
            
        dialog.destroy()
        
        
    def save_image(self, widget):
        
        print self.image_file_name
        cv.SaveImage(self.image_file_name, self.image)    
    
    
    def save_as_image(self, widget):
        
        dialog = gtk.FileChooserDialog("Write image name", None, gtk.FILE_CHOOSER_ACTION_SAVE,
                               (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                gtk.STOCK_SAVE_AS, gtk.RESPONSE_OK))
        dialog.set_default_response(gtk.RESPONSE_OK)
        file_filter = gtk.FileFilter()
        file_filter.set_name("Images")
        file_filter.add_mime_type("image/png")
        file_filter.add_mime_type("image/jpg")
        file_filter.add_pattern("*.png")
        file_filter.add_pattern("*.jpg")
        file_filter.add_pattern("*.jpeg")
        dialog.add_filter(file_filter)

        response = dialog.run()
        
        if response == gtk.RESPONSE_OK:
            file_name = dialog.get_filename()
            cv.SaveImage(file_name, self.image)
            
        dialog.destroy()
                  
        
    def about_win(self, widget):
        about = gtk.AboutDialog()
        about.set_program_name("PyOpenCV")
        about.set_version("0.1")
        about.set_license("GPL v3 http://www.gnu.org/licenses/gpl-3.0.txt")
        about.set_authors(['Enes Ates'])
        about.set_comments("Image Processing Program with OpenCV and PyGTK")
        about.set_website("https://github.com/nsates/PyOpenCV")
        about.set_website_label("PyOpenCV on github")
        about.set_logo(gtk.gdk.pixbuf_new_from_file("images/icon.png"))
        about.run()
        about.destroy()
        
        
    def destroy(self, widget, data=None):
        
        print("You clicked the close button")
        gtk.main_quit()
        
             
    def redraw_drawing_area(self, widget, event): 
           
        gc = self.darea.get_style().fg_gc[gtk.STATE_NORMAL]
        self.darea.window.draw_pixbuf(gc, self.pix, 0, 0, 
                                     (self.darea_width - self.pix.get_width()) / 2, 
                                     (self.darea_height - self.pix.get_height()) / 2)
       
       
    def __init__(self):        
        
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_position(gtk.WIN_POS_CENTER)
        self.window.set_size_request(self.window_width, self.window_height)
        self.window.set_title("Image Processing with PyGTK and OpenCV")
        self.window.set_tooltip_text("Image Processing GUI\n     Python-OpenCV")
        
        self.darea = gtk.DrawingArea()
        self.darea.set_size_request(self.darea_width, self.darea_height)
        self.darea.connect("expose-event", self.redraw_drawing_area)
        
        
        # TOOLBAR FUNCTIONS
        self.open_button = gtk.ToolButton(gtk.STOCK_OPEN)
        self.open_button.set_tooltip_text("Open")
        self.open_button.connect("clicked", self.open_image)
        
        self.save_button = gtk.ToolButton(gtk.STOCK_SAVE)
        self.save_button.set_tooltip_text("Save")
        self.save_button.connect("clicked", self.save_image)
        
        self.save_as_button = gtk.ToolButton(gtk.STOCK_SAVE_AS)
        self.save_as_button.set_tooltip_text("Save As")
        self.save_as_button.connect("clicked", self.save_as_image)
         
        self.resize_w_label = gtk.Label("W:")
        self.resize_w_entry = gtk.Entry()
        self.resize_w_entry.set_size_request(45, 20)
        self.resize_h_label = gtk.Label("H:")
        self.resize_h_entry = gtk.Entry()
        self.resize_h_entry.set_size_request(45, 20)
        self.resize_button  = gtk.ToolButton(gtk.STOCK_ZOOM_FIT)
        self.resize_button.set_tooltip_text("Resize Image")
        self.resize_button.connect("clicked", self.resize_image)     
        
        self.crop_l_label = gtk.Label("L:")
        self.crop_l_entry = gtk.Entry()
        self.crop_l_entry.set_size_request(45, 20)
        self.crop_t_label = gtk.Label("T:")
        self.crop_t_entry = gtk.Entry()
        self.crop_t_entry.set_size_request(45, 20)
        self.crop_w_label = gtk.Label("W:")
        self.crop_w_entry = gtk.Entry()
        self.crop_w_entry.set_size_request(45, 20)
        self.crop_h_label = gtk.Label("H:")
        self.crop_h_entry = gtk.Entry()
        self.crop_h_entry.set_size_request(45, 20)
        self.crop_button = gtk.ToolButton(gtk.STOCK_CUT)
        self.crop_button.set_tooltip_text("Crop Image")
        self.crop_button.connect("clicked", self.crop_image)
               
        self.rotate_left_button  = gtk.ToolButton(gtk.STOCK_UNDO)      
        self.rotate_left_button.set_tooltip_text("Rotate Left")
        self.rotate_left_button.connect("clicked", self.rotate_image, 0)
        
        self.rotate_right_button = gtk.ToolButton(gtk.STOCK_REDO)
        self.rotate_right_button.set_tooltip_text("Rotate Right")
        self.rotate_right_button.connect("clicked", self.rotate_image, 1)
        
        self.about_button = gtk.ToolButton(gtk.STOCK_ABOUT)
        self.about_button.set_tooltip_text("About")
        self.about_button.connect("clicked", self.about_win)
        
        self.quit_button = gtk.ToolButton(gtk.STOCK_QUIT)
        self.quit_button.set_tooltip_text("Quit")
        self.quit_button.connect("clicked", self.destroy)
        
        
        # FUNCTIONS
        self.filter_smooth_blur = gtk.Button("Smooth(Blur)")
        self.filter_smooth_blur.connect("clicked", self.smooth, cv.CV_BLUR)   
        self.filter_smooth_gauss = gtk.Button("Smooth(Gauss)")
        self.filter_smooth_gauss.connect("clicked", self.smooth, cv.CV_GAUSSIAN)     
        self.filter_smooth_median = gtk.Button("Smooth(Median)")
        self.filter_smooth_median.connect("clicked", self.smooth, cv.CV_MEDIAN)
        self.filter_sobel_x = gtk.Button("Sobel Vertical")
        self.filter_sobel_x.connect("clicked", self.sobel, 1, 0)  
        self.filter_sobel_y = gtk.Button("Sobel Horizontal")
        self.filter_sobel_y.connect("clicked", self.sobel, 0, 1)  
        self.filter_laplace = gtk.Button("Laplacian")
        self.filter_laplace.connect("clicked", self.laplace)  
        self.filter_canny = gtk.Button("Canny Edge Det.")
        self.filter_canny.connect("clicked", self.canny)  
        self.filter_corner_harris = gtk.Button("Corner Harris")
        self.filter_corner_harris.connect("clicked", self.corner_harris)  
        
        self.morph_ex_blackhat = gtk.Button("Blackhat")
        self.morph_ex_blackhat.connect("clicked", self.morphology_ex, cv.CV_MOP_BLACKHAT)
        self.morph_ex_open = gtk.Button("Open")
        self.morph_ex_open.connect("clicked", self.morphology_ex, cv.CV_MOP_OPEN)
        self.morph_ex_close = gtk.Button("Close")
        self.morph_ex_close.connect("clicked", self.morphology_ex, cv.CV_MOP_CLOSE)
        self.morph_ex_gradient = gtk.Button("Gradient")
        self.morph_ex_gradient.connect("clicked", self.morphology_ex, cv.CV_MOP_GRADIENT)
        self.morph_ex_tophat = gtk.Button("Tophat")
        self.morph_ex_tophat.connect("clicked", self.morphology_ex, cv.CV_MOP_TOPHAT)
        
        self.intensity_negative = gtk.Button("Negative")
        self.intensity_negative.connect("clicked", self.negative)
        self.intensity_gamma_transform = gtk.Button("Gamma Trans.")
        self.intensity_gamma_transform.connect("clicked", self.gamma_transformation)      
        self.intensity_histogram = gtk.Button("Histogram Eq.")
        self.intensity_histogram.connect("clicked", self.histogram_equalization)
     
        self.video_play = gtk.Button("Play Video")
        self.video_play.connect("clicked", self.play_video)  
                        

        # TOOLBAR FUNCTIONS        
        self.sep_file   = gtk.SeparatorToolItem()
        self.sep_resize = gtk.SeparatorToolItem()
        self.sep_crop   = gtk.SeparatorToolItem()
        self.sep_rotate = gtk.SeparatorToolItem() 
        self.hbox = gtk.HBox(False, 0)
        self.hbox.pack_start(self.open_button, False, False, 3)
        self.hbox.pack_start(self.save_button, False, False, 3)
        self.hbox.pack_start(self.save_as_button, False, False, 3)
        self.hbox.pack_start(self.sep_file, False, False, 15)
        self.hbox.pack_start(self.resize_w_label, False, False, 3)
        self.hbox.pack_start(self.resize_w_entry, False, False, 3)
        self.hbox.pack_start(self.resize_h_label, False, False, 3)
        self.hbox.pack_start(self.resize_h_entry, False, False, 3)
        self.hbox.pack_start(self.resize_button, False, False, 3)
        self.hbox.pack_start(self.sep_resize, False, False, 15)
        self.hbox.pack_start(self.crop_l_label, False, False, 3)
        self.hbox.pack_start(self.crop_l_entry, False, False, 3)
        self.hbox.pack_start(self.crop_t_label, False, False, 3)
        self.hbox.pack_start(self.crop_t_entry, False, False, 3)
        self.hbox.pack_start(self.crop_w_label, False, False, 3)
        self.hbox.pack_start(self.crop_w_entry, False, False, 3)
        self.hbox.pack_start(self.crop_h_label, False, False, 3)
        self.hbox.pack_start(self.crop_h_entry, False, False, 3)
        self.hbox.pack_start(self.crop_button, False, False, 3)
        self.hbox.pack_start(self.sep_crop, False, False, 15)
        self.hbox.pack_start(self.rotate_left_button, False, False, 3)
        self.hbox.pack_start(self.rotate_right_button, False, False, 3)
        self.hbox.pack_start(self.sep_rotate, False, False, 15)
        self.hbox.pack_start(self.about_button, False, False, 3)
        self.hbox.pack_start(self.quit_button, False, False, 3)
        
        
        self.hSep = gtk.HSeparator()
        self.vbox = gtk.VBox(False, 0)
        self.vbox.pack_start(self.hbox, False, False, 0)
        self.vbox.pack_start(self.hSep, True, True, 10)
        
        
        # FUNCTIONS
        self.vbox_func = gtk.VBox(False, 0)
        self.hSep_func = gtk.HSeparator()
        self.label_func = gtk.Label("====== FUNCTIONS ======")
        self.vbox_func.pack_start(self.label_func, False, False, 10)
        self.vbox_func.pack_start(self.hSep_func, False, False, 5)
        
        
        # FILTERS AND DETECTORS
        self.label_filter = gtk.Label("FILTERS AND DETECTORS")
        self.vbox_func.pack_start(self.label_filter, False, False, 20)
        
        self.hbox_filter = gtk.HBox(True, 5)
        self.hbox_filter.pack_start(self.filter_smooth_blur, False, False, 3)
        self.hbox_filter.pack_start(self.filter_smooth_gauss, False, False, 3)
        self.hbox_filter.pack_start(self.filter_smooth_median, False, False, 3)
        
        self.hbox_filter2 = gtk.HBox(True, 0)
        self.hbox_filter2.pack_start(self.filter_sobel_x, False, False, 3)
        self.hbox_filter2.pack_start(self.filter_sobel_y, False, False, 3)
        
        self.hbox_filter3 = gtk.HBox(True, 0)
        self.hbox_filter3.pack_start(self.filter_laplace, False, False, 3)
        self.hbox_filter3.pack_start(self.filter_canny, False, False, 3)
        self.hbox_filter3.pack_start(self.filter_corner_harris, False, False, 3)
        
        self.hSep_filter = gtk.HSeparator()
        self.vbox_func.pack_start(self.hbox_filter, False, False, 0)
        self.vbox_func.pack_start(self.hbox_filter2, False, False, 10)
        self.vbox_func.pack_start(self.hbox_filter3, False, False, 10)
        self.vbox_func.pack_start(self.hSep_filter, False, False, 6)
          
                   
        # MORPHOLOGY
        self.label_morph = gtk.Label("MORPHOLOGY")
        self.vbox_func.pack_start(self.label_morph,False, False, 20)
        
        self.hbox_morph = gtk.HBox(True, 0)
        self.hbox_morph.pack_start(self.morph_ex_blackhat, False, False, 3)
        self.hbox_morph.pack_start(self.morph_ex_open, False, False, 3)
        self.hbox_morph.pack_start(self.morph_ex_close, False, False, 3)
        self.hbox_morph.pack_start(self.morph_ex_gradient, False, False, 3)
        self.hbox_morph.pack_start(self.morph_ex_tophat, False, False, 3)
        
        self.hSep_morph = gtk.HSeparator()
        self.vbox_func.pack_start(self.hbox_morph,False, False, 10)
        self.vbox_func.pack_start(self.hSep_morph,False, False, 5)
        
        
        # INTENSITY TRANSFORMATION
        self.label_intensity = gtk.Label("INTENSITY TRANSFORMATION")
        self.vbox_func.pack_start(self.label_intensity,False, False, 20)
        
        self.hbox_intensity = gtk.HBox(True, 0)
        self.hbox_intensity.pack_start(self.intensity_negative, False, False, 3)
        self.hbox_intensity.pack_start(self.intensity_gamma_transform, False, False, 3)
        self.hbox_intensity.pack_start(self.intensity_histogram, False, False, 3)
        
        self.hSep_intensity = gtk.HSeparator()
        self.vbox_func.pack_start(self.hbox_intensity, False, False, 10)
        self.vbox_func.pack_start(self.hSep_intensity, False, False, 5)
        
        
        # VIDEO PROCESSING
        self.label_video = gtk.Label("VIDEO PROCESSING")
        self.vbox_func.pack_start(self.label_video, False, False, 20)      
      
        self.hSep_video = gtk.HSeparator()
        self.vbox_func.pack_start(self.video_play, False, False, 0)
        self.vbox_func.pack_start(self.hSep_video, False, False, 10)
        
        
 
        self.fixed = gtk.Fixed()
        self.fixed.put(self.vbox, 0, 10)
        self.fixed.put(self.darea, 30, 70) 
        self.fixed.put(self.vbox_func, 600, 70)
        
        self.window.add(self.fixed)    
        self.window.show_all()
        self.window.connect("destroy", self.destroy)
      
      
    def main(self):
        gtk.main()
        
        
if __name__ == "__main__":
    IP = ImageProcessing()
    IP.main()