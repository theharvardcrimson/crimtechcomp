def size_spec_to_size(size_spec, img_width, img_height, upscale=False):
    """
    converts a size_spec into actual image dimensions for the resulting image
    """
    max_w, max_h, crop_w, crop_h = size_spec[:4]

    """
    If upscale is true, this function will enlarge the image if necessary.
    By default it won't make images bigger than they began, because then images
    at the top of articles would be blown way up even if they just weren't
    big enough to begin with.
    """
    if not upscale:
        max_w = min(img_width, max_w) if max_w else img_width
        max_h = min(img_height, max_h) if max_h else img_height
    else:
        max_w = max_w or img_width
        max_h = max_h or img_height

    if not crop_w:
        crop_w, crop_h = img_width, img_height

    h_ratio = float(max_h) / crop_h
    w_ratio = float(max_w) / crop_w
    ratio = min(h_ratio, w_ratio)

    max_w = int(ratio * crop_w)
    max_h = int(ratio * crop_h)

    return max_w, max_h
