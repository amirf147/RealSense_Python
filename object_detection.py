'''Program is using this code with modifications: 
https://github.com/IntelRealSense/librealsense/blob/jupyter/notebooks/distance_to_object.ipynb'''


import cv2

class ObjectDetect:

    def __init__(self, color_frame, colorized_depth, depth_frame, depth_scale, filtered_depth_colored, filtered_depth):
        self.color_frame = color_frame
        self.colorized_depth = colorized_depth
        self.depth_frame = depth_frame
        self.depth_scale = depth_scale
        #self.color_intrinsics = color_intrin
        self.filtered_depth_colored = filtered_depth_colored
        self.filtered_depth = filtered_depth
    
    def detect(self):
        # Standard OpenCV boilerplate for running the net:
        height, width = self.color_frame.shape[:2]
        expected = 300
        aspect = width / height
        resized_image = cv2.resize(self.color_frame, (round(expected * aspect), expected))
        crop_start = round(expected * (aspect - 1) / 2)
        crop_img = resized_image[0:expected, crop_start:crop_start+expected]

        net = cv2.dnn.readNetFromCaffe("C:\\Users\\35840\\Downloads\\MobileNetSSD\\MobileNetSSD\\MobileNetSSD_deploy.prototxt", "C:\\Users\\35840\\Downloads\\MobileNetSSD\\MobileNetSSD\\MobileNetSSD_deploy.caffemodel")
        inScaleFactor = 0.007843
        meanVal       = 127.53
        classNames = ("background", "aeroplane", "bicycle", "bird", "boat",
                    "bottle", "bus", "car", "cat", "chair",
                    "cow", "diningtable", "dog", "horse",
                    "motorbike", "person", "pottedplant",
                    "sheep", "sofa", "train", "tvmonitor")
        #classNames = ("bottle", "chair", "diningtable", "person", "pottedplant", "tvmonitor")
        blob = cv2.dnn.blobFromImage(crop_img, inScaleFactor, (expected, expected), meanVal, False)
        net.setInput(blob, "data")
        detections = net.forward("detection_out")

        label = detections[0,0,0,1]
        conf  = detections[0,0,0,2]
        xmin  = detections[0,0,0,3]
        ymin  = detections[0,0,0,4]
        xmax  = detections[0,0,0,5]
        ymax  = detections[0,0,0,6]

        className = classNames[int(label)]

        confidence =  str(round(conf,2))[0:4]

        # cv2.rectangle(crop_img, (int(xmin * expected), int(ymin * expected)), 
        #             (int(xmax * expected), int(ymax * expected)), (255, 255, 255), 2)

        scale = height / expected
        xmin_depth = int((xmin * expected + crop_start) * scale)
        ymin_depth = int((ymin * expected) * scale)
        xmax_depth = int((xmax * expected + crop_start) * scale)
        ymax_depth = int((ymax * expected) * scale)
        xmin_depth,ymin_depth,xmax_depth,ymax_depth

        # Crop depth data:
        depth = self.depth_frame[xmin_depth:xmax_depth,ymin_depth:ymax_depth].astype(float)
        depth_filtered = self.filtered_depth_colored[xmin_depth:xmax_depth,ymin_depth:ymax_depth].astype(float)

        # Get data scale from the device and convert to meters
        depth = depth * self.depth_scale
        depth_filtered = depth_filtered * self.depth_scale
        dist,_,_,_ = cv2.mean(depth)
        dist_filtered,_,_,_ = cv2.mean(depth_filtered)

        cv2.rectangle(self.colorized_depth, (xmin_depth, ymin_depth), 
                    (xmax_depth, ymax_depth), (255, 255, 255), 2)
        cv2.rectangle(self.color_frame, (xmin_depth, ymin_depth), 
                    (xmax_depth, ymax_depth), (255, 255, 255), 2)
        cv2.rectangle(self.filtered_depth_colored, (xmin_depth, ymin_depth), 
                    (xmax_depth, ymax_depth), (255, 255, 255), 2)
        
        if className not in ["bottle", "chair", "diningtable", "person", "pottedplant", "tvmonitor"]:
            className = "unknown"
        
        text = f'{className} {dist:.2f} meters away'
        text_filt = f'{className} {dist_filtered:.2f} meters away'
        text_location = (xmin_depth, ymin_depth - 5)
        points = [xmin_depth, xmax_depth, ymin_depth, ymax_depth]
        return self.color_frame, self.colorized_depth, text, text_filt, text_location, points, confidence
