import kivy
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
import cv2
from kivy.clock import Clock
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.slider import MDSlider

class Cartoon(Image):
    def __init__(self, fps,**kwargs):
        super(Cartoon, self).__init__(**kwargs)
        self.cap = cv2.VideoCapture(0)
        Clock.schedule_interval(self.Frame, 1.0/fps)

    def Frame(self,fps):
        ret,frame = self.cap.read()
        self.image = frame      

        if ret:
            flip = cv2.flip(frame, 0).tobytes()
            frame_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr' )
            frame_texture.blit_buffer(flip, colorfmt='bgr', bufferfmt='ubyte')
            self.texture = frame_texture

    def cartoon(self,*args):
        noise_sigmaColor = 300
        noise_sigmaSpace = 300
        thresh_block_size = 27
        thresh_constant = 9
        maxIntensityValue = 255
        kernel_size = 9

        frame = self.image
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
        smooth = cv2.medianBlur(gray, kernel_size)
        thresh = cv2.adaptiveThreshold(smooth,maxIntensityValue, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, thresh_block_size, thresh_constant)
        noise = cv2.bilateralFilter(frame,9,noise_sigmaColor,noise_sigmaSpace)
        cartonn = cv2.bitwise_and(noise,noise, mask=thresh)
        flip = cv2.flip(cartonn, 0).tobytes()
        frame_texture = Texture.create(size=(cartonn.shape[1], cartonn.shape[0]), colorfmt='bgr' )
        frame_texture.blit_buffer(flip, colorfmt='bgr', bufferfmt='ubyte')
        self.texture = frame_texture
        

    def cartoonAction(self, *args):
        Clock.schedule_interval(self.cartoon, 1.0/30.0)
        print("cartoon")


    def frames(self, *args):
        path = "new_capure.png"
        image = cv2.imread(path)
        print(image)


    def captureAction(self, *args):
        Clock.schedule_interval(self.frames, 1.0/30.0)
        print("captured")




class MainWindow(MDApp):
    def build(self):
        screen = MDScreen()
        self.cartoonScreen = Cartoon(fps=30.0)

        self.capturebtn = MDRectangleFlatButton(text="Caputure", pos_hint={'center_x':0.3, 'center_y':0.15} )
        self.cartoonify = MDRectangleFlatButton(text="Cartoonify", pos_hint={'center_x':0.7, 'center_y':0.15})
        screen.add_widget(self.cartoonScreen)
        screen.add_widget(self.capturebtn)
        screen.add_widget(self.cartoonify)
        

        self.btnAction()
        return screen

    def btnAction(self):
        self.capturebtn.bind(on_press=self.cartoonScreen.captureAction)
        self.cartoonify.bind(on_press=self.cartoonScreen.cartoonAction)

if __name__ == '__main__':
    MainWindow().run()