from io import BytesIO
import os
import cv2
from random import shuffle, choice;
from base64 import b64encode;
import matplotlib.pyplot as plt;
import numpy as np;
import perfplot as p;
import requests;

from fingerScanner.settings import BASE_DIR

def matcher(ss = 200):
    max_score = -1;
    file = None;
    img = None;
    kp1 = kp2 = mp = None;
    search_space = sorted(os.listdir("./static/media/prints"), key=lambda x: int(x.split("_")[0]))[:ss]; #max=5288
    # print(search_space[-5:]);
    shuffle(search_space);
    sample = cv2.imread("./static/media/prints/" + choice(search_space))
    for f in search_space:
        fimg = cv2.imread("./static/media/prints/" + f);

        sift = cv2.SIFT_create();

        ks, ds = sift.detectAndCompute(sample, None);
        ko, do = sift.detectAndCompute(fimg, None);

        matches = cv2.FlannBasedMatcher({"algorithm": 1, "trees": 10}, {}).knnMatch(ds, do, k=2);

        match_points = [p for p, q in matches if p.distance < .1*q.distance];

        kp = min(len(ks), len(ko));

        cur_score = len(match_points) / kp * 100;
        if cur_score > max_score:
            max_score = cur_score;
            file = f;
            img = fimg;
            kp1, kp2, mp = ks, ko, match_points;
    res = cv2.drawMatches(sample, kp1, img, kp2, mp, None);

    print("Best Match: " + str(file))
    print("Best Score: " + str(max_score))

    return res;

def get_graph():
    buffer = BytesIO();
    plt.savefig(buffer, format="png");
    buffer.seek(0);
    img = buffer.getvalue();
    graph = b64encode(img);
    graph = graph.decode("utf-8");
    buffer.close();
    return graph;


def get_chart(call, *args, **kwargs):
    plt.switch_backend("AGG");
    # plt.imshow(data, origin="lower");
    call(args, kwargs);
    plt.tight_layout();
    chart = get_graph();
    return chart;

def getUsers():
    url = "https://reqres.in/api/users?page=2";
    return requests.get(url).json();