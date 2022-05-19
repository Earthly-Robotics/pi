class Camera:
    camera = None

    def __init__(self, robot, time_step):
        self.camera = robot.getDevice('camera')
        self.camera.enable(time_step)

    def get_image_array_from_camera(self):
        if self.camera is not None:
            img = self.camera.getImageArray()
            return img
        else:
            print("Camera does not exist. Try calling setup()")
            return None

    def get_width(self):
        if self.camera is not None:
            return self.camera.getWidth()
        else:
            print("Camera does not exist. Try calling setup()")
            return None
