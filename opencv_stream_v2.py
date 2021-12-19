import cv2
from "../camera_setup.py" import RealSenseCamera

ros_bag = "C:\\Users\\35840\\Documents\\20211217_204044.bag"

# Initialize the camera
camera = RealSenseCamera(ros_bag)
apply_filter = True

try:
    while True:
        camera.get_data() # Load the object's variables with data
        depth_frame = camera.depth_frame
        color_frame = camera.color_frame
        infrared_frame = camera.infrared_frame
        color_intrin = camera.color_intrinsics

        # apply filtering to depth data
        if apply_filter:
            camera.filter_depth_data(enable_decimation = False,
                                    enable_spatial = True,
                                    enable_temporal = False,
                                    enable_hole_filling = False)

            proc_depth_frame = camera.processed_depth_frame
            print('filters applied')

        proc_depth_image = camera.frame_to_np_array(proc_depth_frame, colorize_depth=True)

        depth_image = camera.frame_to_np_array(depth_frame, colorize_depth=True)

        image_to_be_shown = depth_image
        image_name = 'filtered depth'
        
        img = cv2.resize(image_to_be_shown, (640, 480))
        depth_image = cv2.resize(depth_image, (640, 480))

        cv2.imshow(image_name, img)
        cv2.imshow('o', depth_image)

        key = cv2.waitKey(1)

        # Press esc or 'q' to close the image window
        if key & 0xFF == ord('q') or key == 27:
            cv2.destroyAllWindows()
            break

finally:
    camera.stop()