from object_detection import ObjectDetect
import cv2
from realsense_api import RealSenseCamera

# TODO: 
#   - Create a dictionary to hold multiple rosbag file paths that can be the 
#     key while the value can be a camera instantiation.  This would be for
#     when we want to view multiple rosbags at the same time.
#   - Add the ability to change filter values using key presses while viewing
#     the opencv Stream 
#   - Add the ability to save the current filter configuration to a text file 
#     or json 

# Initialize the camera
camera = RealSenseCamera()
apply_filter = True

try:
    while True:
        # Get the frameset and other data to be loaded into the class attributes
        camera.get_data()
        
        # apply filtering to frameset
        if apply_filter:
            camera.filter_depth_data(enable_decimation=True,
                                    enable_spatial=True,
                                    enable_temporal=True,
                                    enable_hole_filling=True)
            filtered_frameset = camera.filtered_frameset

        # Get desired frames and images 
        camera.get_aligned_frames(filtered_frameset, aligned_to_color=True)
        filtered_depth_frame = camera.depth_frame_aligned
        color_frame = camera.color_frame_aligned
        color_image = camera.frame_to_np_array(color_frame)
        colored_depth_image = camera.frame_to_np_array(filtered_depth_frame, colorize_depth=True)
        depth_image = camera.frame_to_np_array(filtered_depth_frame)

        # Detect object and display in image 
        detector = ObjectDetect(color_image, depth_image, camera.depth_scale)
        detector.detect()
        detector.draw_rectangle(color_image)

        # Show image
        image_name = 'filtered depth'
        cv2.imshow(image_name, color_image)
        key = cv2.waitKey(1)

        # Press esc or 'q' to close the image window
        if key & 0xFF == ord('q') or key == 27:
            cv2.destroyAllWindows()
            break

finally:
    camera.stop()