############################ this code is not mine i have taken it from internet ####################
from kivy.app import App
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.properties import ObjectProperty, NumericProperty
import numpy
import cv2


class KivyCamera(Image):
    source = ObjectProperty()
    fps = NumericProperty(30)

    def __init__(self, **kwargs):
        super(KivyCamera, self).__init__(**kwargs)
        self._capture = None
        if self.source is not None:
            self._capture = cv2.VideoCapture(self.source)
        Clock.schedule_interval(self.update, 1.0 / self.fps)

    def on_source(self, *args):
        if self._capture is not None:
            self._capture.release()
        self._capture = cv2.VideoCapture(self.source)

    @property
    def capture(self):
        return self._capture

    def update(self, dt):
        ret, frame = self.capture.read()
        print(type(frame))
        if ret:
            ###################### open cv to kivy texture ###################
            buf1 = cv2.flip(frame, 0)
            buf = buf1.tostring()
            image_texture = Texture.create(
                size=(frame.shape[1], frame.shape[0]), colorfmt="bgr"
            )
            image_texture.blit_buffer(buf, colorfmt="bgr", bufferfmt="ubyte")

            self.texture = image_texture
            ###################################################
            ############################# kivy texture texture too opencv ###################
            height, width = self.texture.height, self.texture.width

            newvalue = numpy.frombuffer(self.texture.pixels, numpy.uint8)
            newvalue = newvalue.reshape(height, width, 4)
            gray = cv2.cvtColor(newvalue, cv2.COLOR_RGBA2BGR)

            gray = cv2.flip(gray, 0)
            #######################################################
            cv2.imwrite('xffg.jpg', gray)


class testcameraApp(App):
    pass


if __name__ == "__main__":
    testcameraApp().run()