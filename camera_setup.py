import numpy as np
import pyrealsense2 as rs

class RealSenseCamera:

    def __init__(self, ros_bag = None):

        # Used if openings stream from prerecorded ros .bag file
        # holds the path to the .bag file
        self.ros_bag = ros_bag

        # Data variables that will be set with get_data()
        self.depth_frame = None
        self.color_frame = None
        self.infrared_frame = None
        self.color_intrinsics = None
        self.depth_scale = None

        # Post Processing Filter variables with default values
        # https://dev.intelrealsense.com/docs/post-processing-filters

        # Decimation filter variable 
        self.decimation_magnitude = 2
        
        # Spatial filter variables
        self.spatial_magnitude = 5
        self.spatial_smooth_alpha = 1
        self.spatial_smooth_delta = 50
        self.spatial_holes_fill = 3

        # Temporal filter variables
        self.temporal_smooth_alpha = 0.4
        self.temporal_smooth_delta = 20
        self.persistency_index = 8

        # Holes Filling filter variable
        self.hole_filling = 1       

        # Holds the data frame after it has undergone filtering 
        self.processed_depth_frame = None

        # Configure and start streams
        self.pipeline = rs.pipeline()
        config = rs.config()
        if ros_bag:
            config.enable_device_from_file(self.ros_bag)
        else:
            config.enable_stream(rs.stream.depth, rs.format.z16, 30)
            config.enable_stream(rs.stream.color, rs.format.bgr8, 30)
            config.enable_stream(rs.stream.infrared, rs.format.y8, 30)
        self.profile = self.pipeline.start(config)

        # Get depth scale
        depth_sensor = self.profile.get_device().first_depth_sensor()
        self.depth_scale = depth_sensor.get_depth_scale()

    def get_data(self, aligned_to_color = False, aligned_to_depth = False,
                   aligned_to_infrared = False):

        # Trying to align to infrared will be ignored. Just align to depth and it is the
        # same thing since LiDAR uses infrared. TODO: remove align to infrared option

        '''Gets the frames as numpy arrays and get other data'''

        align_to_options = [aligned_to_color,aligned_to_depth,aligned_to_infrared]    
        streams = [rs.stream.color, rs.stream.depth, rs.stream.infrared]

        # Validate that only 1 aligned_to_... variable is true
        if align_to_options.count(True) > 1:
            raise Exception("Can't align to more than one type of frame")

        # Determine which frame we are aligning the other frames to
        align_to = [stream for stream in streams 
                    if align_to_options[streams.index(stream)]]

        frames = self.pipeline.wait_for_frames()

        if align_to:
            align_to = align_to.pop()
            align = rs.align(align_to)
            frames = align.process(frames)

        self.depth_frame = frames.get_depth_frame()
        self.color_frame = frames.get_color_frame()
        self.infrared_frame = frames.first(rs.stream.infrared)
        self.color_intrinsics = self.color_frame.profile \
                                .as_video_stream_profile() \
                                .intrinsics

    def filter_depth_data(self,
                          enable_decimation = False,
                          enable_spatial = False,
                          enable_temporal = False,
                          enable_hole_filling = False):

        '''Apply a cascade of filters on the depth frame'''

        depth_to_disparity = rs.disparity_transform(True)
        disparity_to_depth = rs.disparity_transform(False)

        depth = self.depth_frame
        # DECIMATION FILTER
        if enable_decimation:
            decimation = rs.decimation_filter()
            decimation.set_option(rs.option.filter_magnitude, self.decimation_magnitude)
            depth = decimation.process(depth)

        # SPATIAL FILTER
        if enable_spatial:
            spatial = rs.spatial_filter()
            spatial.set_option(rs.option.filter_magnitude, self.spatial_magnitude)
            spatial.set_option(rs.option.filter_smooth_alpha, self.spatial_smooth_alpha)
            spatial.set_option(rs.option.filter_smooth_delta, self.spatial_smooth_delta)
            
            spatial.set_option(rs.option.holes_fill, self.spatial_holes_fill)
            depth = spatial.process(depth)

        # TEMPORAL FILTER
        if enable_temporal:
            temporal = rs.temporal_filter()
            temporal.set_option(rs.option.filter_smooth_alpha, self.temporal_smooth_alpha)
            temporal.set_option(rs.option.filter_smooth_delta, self.temporal_smooth_delta)
            temporal.set_option(rs.option.holes_fill, self.persistency_index)
            depth = temporal.process(depth)

        # if enable_temporal:
        #     temporal = rs.temporal_filter(0.40, 40, 8)
        # HOLE FILLING
        if enable_hole_filling:
            hole_filling = rs.hole_filling_filter()
            hole_filling.set_option(rs.option.holes_fill, self.hole_filling)
            depth = hole_filling.process(depth)

        self.processed_depth_frame = depth
        #print(rs.options.get_option(temporal, rs.option.holes_fill))
    def frame_to_np_array(self, frame, colorize_depth = False):
        # Create colorized depth frame
        if colorize_depth:
            colorizer = rs.colorizer()
            frame_as_image = np.asanyarray(colorizer.colorize(frame).get_data())
            return frame_as_image
        frame_as_image = np.asanyarray(frame.get_data())
        return frame_as_image


    def stop(self):
        self.pipeline.stop()
