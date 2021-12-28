from object_detection import ObjectDetect
import cv2
from realsense_api import RealSenseCamera
from realsense_api.post_processing.option import OptionType

# TODO: 
#   - Create a dictionary to hold multiple rosbag file paths that can be the 
#     key while the value can be a camera instantiation.  This would be for
#     when we want to view multiple rosbags at the same time.
#   - Add the ability to change filter values using key presses while viewing
#     the opencv Stream 
#   - Add the ability to save the current filter configuration to a text file 
#     or json 

ros_bag = "C:\\Users\\35840\\Documents\\20211221_120843_2d.bag"

# Initialize the camera
camera = RealSenseCamera(ros_bag=ros_bag)
apply_filter = True
apply_align = False
enable_detection = False

try:
    while True:
        # Get the frameset and other data to be loaded into the class attributes
        camera.get_data()
        
        if apply_filter:
            camera.filter_depth_data(enable_decimation=True,
                                    enable_spatial=True,
                                    enable_temporal=True,
                                    enable_hole_filling=True)
            frameset = camera.filtered_frameset
        else:
            frameset = camera.frameset
        if apply_align:
            camera.get_aligned_frames(frameset, aligned_to_color=True)
            depth_frame = camera.depth_frame_aligned
            color_frame = camera.color_frame_aligned
        else:
            depth_frame = frameset.get_depth_frame()
            #color_frame = frameset.get_color_frame()

        # color_image = camera.frame_to_np_array(color_frame)
        colored_depth_image = camera.frame_to_np_array(depth_frame, colorize_depth=True)
        depth_image = camera.frame_to_np_array(depth_frame)

        if enable_detection:
            detector = ObjectDetect(color_image, depth_image, camera.depth_scale)
            detector.detect()
            detector.draw_rectangle(color_image)

        # Show image
        image_name = 'filtered depth'
        cv2.imshow(image_name, colored_depth_image)
        key = cv2.waitKey(1)



        # Press esc or 'q' to close the image window
        if key & 0xFF == ord('q') or key == 27:
            cv2.destroyAllWindows()
            break

        if key & 0xFF == ord('d'):
            decimation_magnitude = camera.decimation.options[OptionType.MAGNITUDE]
            camera.decimation.increment(decimation_magnitude)
finally:
    camera.stop()