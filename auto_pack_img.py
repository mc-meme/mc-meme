import cv2
import numpy as np
import os


class Node:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.used = False
        self.right = None
        self.down = None


def find_node(root, width, height):
    if root.used:
        return find_node(root.right, width, height) or find_node(root.down, width, height)
    elif width <= root.width and height <= root.height:
        return root
    else:
        return None


def split_node(node, width, height):
    node.used = True
    node.down = Node(node.x, node.y + height, node.width, node.height - height)
    node.right = Node(node.x + width, node.y, node.width - width, height)
    return node


def grow_node(root, width, height):
    can_grow_down = (width <= root.width)
    can_grow_right = (height <= root.height)

    should_grow_right = can_grow_right and (root.height >= (root.width + width))
    should_grow_down = can_grow_down and (root.width >= (root.height + height))

    if should_grow_right:
        return grow_right(root, width, height)
    elif should_grow_down:
        return grow_down(root, width, height)
    elif can_grow_right:
        return grow_right(root, width, height)
    elif can_grow_down:
        return grow_down(root, width, height)
    else:
        return None


def grow_right(root, width, height):
    new_root = Node(0, 0, root.width + width, root.height)
    new_root.used = True
    new_root.down = root
    new_root.right = Node(root.width, 0, width, root.height)
    return new_root if find_node(new_root, width, height) else None


def grow_down(root, width, height):
    new_root = Node(0, 0, root.width, root.height + height)
    new_root.used = True
    new_root.right = root
    new_root.down = Node(0, root.height, root.width, height)
    return new_root if find_node(new_root, width, height) else None


def stitch_images_bin_packing(images):

    root = Node(0, 0, images[0].shape[1], images[0].shape[0])

    positions = []

    for img in images:
        node = find_node(root, img.shape[1], img.shape[0])
        if node:
            split_node(node, img.shape[1], img.shape[0])
        else:
            root = grow_node(root, img.shape[1], img.shape[0])
            node = find_node(root, img.shape[1], img.shape[0])
            split_node(node, img.shape[1], img.shape[0])
        positions.append((node.x, node.y))


    # stitched_image = np.zeros((root.height, root.width, 3), dtype=np.uint8)
    stitched_image = np.full((root.height, root.width, 3),255, dtype=np.uint8)


    for pos, img in zip(positions, images):
        x, y = pos
        stitched_image[y:y + img.shape[0], x:x + img.shape[1]] = img

    return stitched_image



def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder, filename))
        if img is not None:
            images.append(img)
    return images



folder = 'zh_cn'
images = load_images_from_folder(folder)

stitched_image = stitch_images_bin_packing(images)


cv2.imwrite('auto_img_zh_cn.png', stitched_image)
