# img-makeover
GUI tool which converts a series of RGB images to HSL, then autoscales the saturation and lightness to [0, 255] before converting back to RGB and resaving.

Domain bounds for autoscaling are MAX & MIN of S & L. But pixels at edges and corners can be cropped from extremum detection.
