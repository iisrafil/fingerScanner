import os
import cv2
from time import time;

from fingerScanner.settings import BASE_DIR

directory = os.path.join(BASE_DIR, "static", "media", "finger_scan")
# directory = str(BASE_DIR) + "/SOCOFing/"


def scanner(suspect):
    sample = cv2.imread(suspect)
    # sample = cv2.imread(os.path.join(directory, '174__F_Left_little_finger.BMP'))

    best_score = 0
    filename = None
    image = None
    kp1, kp2, np = None, None, None

    counter = 0
    lim = 100
    start_time = time();
    for file in [file for file in os.listdir(directory)][:lim]:
        if counter == lim/10:
            print(counter)
        counter += 1
        fingerprint_image = cv2.imread(os.path.join(directory, file))
        sift = cv2.SIFT_create()

        keypoints_1, descriptors_1 = sift.detectAndCompute(sample, None)
        keypoints_2, descriptors_2 = sift.detectAndCompute(fingerprint_image, None)

        matches = cv2.FlannBasedMatcher({"algorithm": 1, "trees": 10}, {}).knnMatch(
            descriptors_1, descriptors_2, k=2
        )

        match_points = []

        for p, q in matches:
            if p.distance < 0.1 * q.distance:
                match_points.append(p)

        keypoints = 0
        if len(keypoints_1) < len(keypoints_2):
            keypoints = len(keypoints_1)
        else:
            keypoints = len(keypoints_2)

        if len(match_points) / keypoints * 100 > best_score:
            best_score = len(match_points) / keypoints * 100
            filename = file
            image = fingerprint_image
            kp1, kp2, np = keypoints_1, keypoints_2, match_points

    print("Best Match: " + str(filename))
    print("Best Score: " + str(best_score))

    return str(filename), time()-start_time, best_score;


def padd_bytes(bts: bytes):
    bts: bytearray = bytearray(bts)
    new: bytearray = []
    for b in bts:
        new.append(b & 0xF0)
        new.append((b & 0x0F) << 4)
    return bytes(new)
