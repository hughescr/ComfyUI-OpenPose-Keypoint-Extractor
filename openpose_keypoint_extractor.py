import json
from nodes import MAX_RESOLUTION

class OpenPoseKeyPointExtractor:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "pose_keypoint": ("POSE_KEYPOINT",),
                "image_width": ("INT", { "min": 0, "max": MAX_RESOLUTION }),
                "image_height": ("INT", { "min": 0, "max": MAX_RESOLUTION }),
                "points_list": ("STRING", {"multiline": True, "default": ""}),
            },
            "optional": {
                "person_number": ("INT", { "default": 0 }),
            }
        }

    RETURN_TYPES = ("INT", "INT", "INT", "INT")
    RETURN_NAMES = ("x", "y", "width", "height")
    FUNCTION = "box_keypoints"
    CATEGORY = "utils"

    def get_keypoint_from_list(self, list, item):
        idx_x = item*3
        idx_y = idx_x + 1
        idx_conf = idx_y + 1
        return (list[idx_x], list[idx_y], list[idx_conf])

    def box_keypoints(self, pose_keypoint, image_width, image_height, points_list, person_number=0):
        points_we_want = [int(element) for element in points_list.split(",")]

        min_x = MAX_RESOLUTION
        min_y = MAX_RESOLUTION
        max_x = 0
        max_y = 0
        for element in points_we_want:
            (x,y,z) = self.get_keypoint_from_list(pose_keypoint[0]["people"][person_number]["pose_keypoints_2d"], element)
            if x < min_x:
                min_x = x
            if y < min_y:
                min_y = y
            if x > max_x:
                max_x = x
            if y > max_y:
                max_y = y
        return (int(min_x*image_width), int(min_y*image_height), int((max_x-min_x)*image_width), int((max_y-min_y)*image_height))

NODE_CLASS_MAPPINGS = {
    "Openpose Keypoint Extractor": OpenPoseKeyPointExtractor,
}
