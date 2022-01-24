{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 307,
   "metadata": {},
   "outputs": [],
   "source": [
    "import matplotlib.pyplot as plt\n",
    "import numpy as np\n",
    "import math\n",
    "from PIL import Image"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 341,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "(459, 942, 4)\n"
     ]
    },
   ],
   "source": [
    "circuit_img = plt.imread('circuit.png')\n",
    "print(circuit_img.shape)\n",
    "plt.imshow(circuit_img)\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 342,
   "metadata": {},
   "outputs": [],
   "source": [
    "def thresholding(pixel):\n",
    "    threshold = 1\n",
    "    gray = (pixel[0]+pixel[1]+pixel[2])*pixel[3]\n",
    "    return 0 if gray < threshold else 1\n",
    "circuit = np.array([[thresholding(px) for px in line]for line in circuit_img])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 343,
   "metadata": {},
   "outputs": [],
   "source": [
    "def remove_black_near_white(circuit, minBlkNeighB, maxBlkNeighB):\n",
    "    for y in range(circuit.shape[0] - 1):\n",
    "        for x in range(circuit.shape[1] -1):\n",
    "            if(circuit[y][x] == 0):\n",
    "                nbOfBlackNeighBors = 8 - (circuit[y+1][x+1] + circuit[y+1][x] + circuit[y+1][x-1] + circuit[y][x-1] + circuit[y][x+1] + circuit[y-1][x-1] + circuit[y-1][x] + circuit[y-1][y+1])\n",
    "                are_left_white = (circuit[y+1][x-1] + circuit[y][x-1] + circuit[y-1][x-1]) == 3\n",
    "                are_right_white = (circuit[y+1][x+1] + circuit[y][x+1] + circuit[y-1][x+1]) == 3\n",
    "                are_top_white = (circuit[y+1][x+1] + circuit[y+1][x] + circuit[y+1][x-1]) == 3\n",
    "                are_bottom_white = (circuit[y-1][x-1] + circuit[y-1][x] + circuit[y-1][y+1]) == 3\n",
    "                if((are_left_white or are_right_white or are_bottom_white or are_top_white) and nbOfBlackNeighBors > 3):\n",
    "                # if(nbOfBlackNeighBors > minBlkNeighB and nbOfBlackNeighBors < maxBlkNeighB):\n",
    "                    circuit[y][x] = 1\n",
    "\n",
    "def countBlackPixel(circuit):\n",
    "    nb_black = 0\n",
    "    for line in circuit:\n",
    "        for px in line:\n",
    "            nb_black = nb_black + (1 if px == 0 else 0)\n",
    "    return nb_black"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 339,
   "metadata": {},
   "outputs": [],
   "source": [
    "remove_black_near_white(circuit, 0, 2)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 330,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "1253"
      ]
     },
     "execution_count": 330,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "countBlackPixel(circuit)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 347,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "5047\n",
      "5047\n",
      "(459, 942)\n"
     ]
    },
    {
     "ename": "OSError",
     "evalue": "cannot write mode I as JPEG",
     "output_type": "error",
     "traceback": [
      "\u001b[1;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[1;31mKeyError\u001b[0m                                  Traceback (most recent call last)",
      "\u001b[1;32m~\\anaconda3\\envs\\3a_ia\\lib\\site-packages\\PIL\\JpegImagePlugin.py\u001b[0m in \u001b[0;36m_save\u001b[1;34m(im, fp, filename)\u001b[0m\n\u001b[0;32m    628\u001b[0m     \u001b[1;32mtry\u001b[0m\u001b[1;33m:\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[1;32m--> 629\u001b[1;33m         \u001b[0mrawmode\u001b[0m \u001b[1;33m=\u001b[0m \u001b[0mRAWMODE\u001b[0m\u001b[1;33m[\u001b[0m\u001b[0mim\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mmode\u001b[0m\u001b[1;33m]\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0m\u001b[0;32m    630\u001b[0m     \u001b[1;32mexcept\u001b[0m \u001b[0mKeyError\u001b[0m \u001b[1;32mas\u001b[0m \u001b[0me\u001b[0m\u001b[1;33m:\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n",
      "\u001b[1;31mKeyError\u001b[0m: 'I'",
      "\nThe above exception was the direct cause of the following exception:\n",
      "\u001b[1;31mOSError\u001b[0m                                   Traceback (most recent call last)",
      "\u001b[1;32m~\\AppData\\Local\\Temp/ipykernel_18152/2814915325.py\u001b[0m in \u001b[0;36m<module>\u001b[1;34m\u001b[0m\n\u001b[0;32m     18\u001b[0m \u001b[0mprint\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0mcircuit_jpg\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mshape\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m     19\u001b[0m \u001b[0mim\u001b[0m \u001b[1;33m=\u001b[0m \u001b[0mImage\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mfromarray\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0mcircuit_jpg\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[1;32m---> 20\u001b[1;33m \u001b[0mim\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0msave\u001b[0m\u001b[1;33m(\u001b[0m\u001b[1;34m\"img.jpg\"\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0m\u001b[0;32m     21\u001b[0m \u001b[0mim\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mshow\u001b[0m\u001b[1;33m(\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n",
      "\u001b[1;32m~\\anaconda3\\envs\\3a_ia\\lib\\site-packages\\PIL\\Image.py\u001b[0m in \u001b[0;36msave\u001b[1;34m(self, fp, format, **params)\u001b[0m\n\u001b[0;32m   2238\u001b[0m \u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m   2239\u001b[0m         \u001b[1;32mtry\u001b[0m\u001b[1;33m:\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[1;32m-> 2240\u001b[1;33m             \u001b[0msave_handler\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0mself\u001b[0m\u001b[1;33m,\u001b[0m \u001b[0mfp\u001b[0m\u001b[1;33m,\u001b[0m \u001b[0mfilename\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0m\u001b[0;32m   2241\u001b[0m         \u001b[1;32mfinally\u001b[0m\u001b[1;33m:\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m   2242\u001b[0m             \u001b[1;31m# do what we can to clean up\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n",
      "\u001b[1;32m~\\anaconda3\\envs\\3a_ia\\lib\\site-packages\\PIL\\JpegImagePlugin.py\u001b[0m in \u001b[0;36m_save\u001b[1;34m(im, fp, filename)\u001b[0m\n\u001b[0;32m    629\u001b[0m         \u001b[0mrawmode\u001b[0m \u001b[1;33m=\u001b[0m \u001b[0mRAWMODE\u001b[0m\u001b[1;33m[\u001b[0m\u001b[0mim\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mmode\u001b[0m\u001b[1;33m]\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m    630\u001b[0m     \u001b[1;32mexcept\u001b[0m \u001b[0mKeyError\u001b[0m \u001b[1;32mas\u001b[0m \u001b[0me\u001b[0m\u001b[1;33m:\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[1;32m--> 631\u001b[1;33m         \u001b[1;32mraise\u001b[0m \u001b[0mOSError\u001b[0m\u001b[1;33m(\u001b[0m\u001b[1;34mf\"cannot write mode {im.mode} as JPEG\"\u001b[0m\u001b[1;33m)\u001b[0m \u001b[1;32mfrom\u001b[0m \u001b[0me\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0m\u001b[0;32m    632\u001b[0m \u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m    633\u001b[0m     \u001b[0minfo\u001b[0m \u001b[1;33m=\u001b[0m \u001b[0mim\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mencoderinfo\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n",
      "\u001b[1;31mOSError\u001b[0m: cannot write mode I as JPEG"
     ]
    }
   ],
   "source": [
    "previous_nb_black = 0 \n",
    "nb_black = countBlackPixel(circuit)\n",
    "\n",
    "print(nb_black)\n",
    "\n",
    "while nb_black != previous_nb_black:\n",
    "    previous_nb_black = nb_black\n",
    "    remove_black_near_white(circuit, 2, 8)\n",
    "    nb_black = countBlackPixel(circuit)\n",
    "\n",
    "remove_black_near_white(circuit, 2, 8)\n",
    "\n",
    "\n",
    "print(nb_black)\n",
    "# plt.imshow(circuit, cmap=\"gray\")\n",
    "# plt.show()\n",
    "circuit_jpg = np.array([[px*255 for px in line] for line in circuit])\n",
    "print(circuit_jpg.shape)\n",
    "im = Image.fromarray(circuit_jpg)\n",
    "im.convert('RGB').save(\"img.jpg\")\n",
    "im.show()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 111,
   "metadata": {},
   "outputs": [],
   "source": [
    "def resize(circuit, height=720, width=1220):\n",
    "    circuit_resized = np.ones((height, width))\n",
    "    factor = min(height / circuit.shape[0], width / circuit.shape[1])\n",
    "    for y in range(circuit.shape[0] -1):\n",
    "        for x in range(circuit.shape[1] -1):\n",
    "            if(circuit[y][x] == 0):\n",
    "                circuit_resized[math.floor(y*factor) - 10][math.floor(x*factor) -10] = 0\n",
    "    return circuit_resized"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 112,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "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",
      "text/plain": [
       "<Figure size 432x288 with 1 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "circuit_resized = resize(circuit)\n",
    "plt.imshow(circuit_resized, cmap=\"gray\")\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 113,
   "metadata": {},
   "outputs": [],
   "source": [
    "def getABlack(circuit):\n",
    "    px = 0\n",
    "    while circuit[px//circuit.shape[0]][px%circuit.shape[1]] == 1:\n",
    "        px += 1\n",
    "    return (px//circuit.shape[0], px%circuit.shape[1])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 114,
   "metadata": {},
   "outputs": [],
   "source": [
    "def getBlackNeighbors(circuit, pixel):\n",
    "    blackNeighbors = []\n",
    "    x = pixel[1]\n",
    "    y = pixel[0]\n",
    "    if(circuit[y+1][x-1]): blackNeighbors.append(circuit[y+1][x-1])\n",
    "    if(circuit[y+1][x]): blackNeighbors.append(circuit[y+1][x])\n",
    "    if(circuit[y+1][x+1]): blackNeighbors.append(circuit[y+1][x+1])\n",
    "\n",
    "    if(circuit[y][x+1]): blackNeighbors.append(circuit[y][x+1])\n",
    "    if(circuit[y][x-1]): blackNeighbors.append(circuit[y][x-1])\n",
    "\n",
    "    if(circuit[y-1][x-1]): blackNeighbors.append(circuit[y-1][x-1])\n",
    "    if(circuit[y-1][x]): blackNeighbors.append(circuit[y-1][x])\n",
    "    if(circuit[y-1][x+1]): blackNeighbors.append(circuit[y-1][x+1])\n",
    "    print(len(blackNeighbors))\n",
    "    return blackNeighbors"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 115,
   "metadata": {},
   "outputs": [],
   "source": [
    "def getTrack(circuit):\n",
    "    track_arr = []\n",
    "    point = getABlack()\n",
    "    \n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 116,
   "metadata": {},
   "outputs": [],
   "source": [
    "track_coord = []\n",
    "for y in range(circuit.shape[0] -1):\n",
    "    for x in range(circuit.shape[1] -1):\n",
    "        if(circuit[y][x] == 0):\n",
    "            track_coord.append((x,y))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 117,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "559\n",
      "((826, 38), (829, 38), (832, 38), (835, 38), (838, 38), (841, 38), (844, 38), (808, 39), (811, 39), (814, 39), (817, 39), (820, 39), (823, 39), (794, 40), (797, 40), (800, 40), (803, 40), (806, 40), (780, 41), (783, 41), (786, 41), (789, 41), (792, 41), (770, 42), (773, 42), (776, 42), (779, 42), (757, 43), (760, 43), (763, 43), (766, 43), (742, 44), (745, 44), (748, 44), (751, 44), (754, 44), (732, 45), (735, 45), (738, 45), (741, 45), (725, 46), (728, 46), (731, 46), (717, 47), (720, 47), (710, 48), (713, 48), (855, 48), (614, 49), (617, 49), (702, 49), (705, 49), (708, 49), (610, 50), (693, 50), (696, 50), (699, 50), (622, 51), (686, 51), (689, 51), (692, 51), (624, 52), (680, 52), (683, 52), (671, 53), (674, 53), (677, 53), (627, 54), (665, 54), (668, 54), (854, 54), (654, 55), (657, 55), (660, 55), (630, 56), (646, 56), (649, 56), (652, 56), (604, 57), (635, 57), (640, 57), (643, 57), (637, 58), (853, 59), (852, 61), (598, 64), (851, 65), (594, 67), (850, 68), (587, 69), (590, 69), (581, 70), (584, 70), (576, 71), (579, 71), (573, 72), (567, 73), (570, 73), (564, 74), (558, 75), (561, 75), (553, 76), (556, 76), (550, 77), (848, 77), (547, 78), (541, 79), (544, 79), (536, 80), (539, 80), (532, 81), (847, 81), (528, 82), (523, 83), (846, 83), (519, 84), (846, 84), (514, 85), (507, 86), (510, 86), (503, 87), (506, 87), (501, 88), (494, 89), (497, 89), (490, 90), (493, 90), (487, 91), (843, 91), (483, 92), (477, 93), (480, 93), (474, 94), (842, 94), (469, 95), (842, 95), (464, 96), (458, 97), (461, 97), (455, 98), (449, 99), (452, 99), (444, 100), (447, 100), (440, 101), (443, 101), (436, 102), (431, 103), (434, 103), (428, 104), (421, 105), (424, 105), (837, 105), (419, 106), (412, 107), (415, 107), (410, 108), (404, 109), (407, 109), (399, 110), (402, 110), (394, 111), (397, 111), (392, 112), (833, 114), (389, 117), (349, 120), (352, 120), (345, 121), (348, 121), (339, 122), (342, 122), (386, 122), (334, 123), (337, 123), (326, 124), (329, 124), (332, 124), (828, 124), (321, 125), (324, 125), (384, 125), (314, 126), (317, 126), (363, 126), (827, 126), (308, 127), (311, 127), (381, 127), (302, 128), (305, 128), (378, 128), (293, 129), (296, 129), (299, 129), (372, 129), (375, 129), (285, 130), (288, 130), (291, 130), (278, 131), (281, 131), (284, 131), (274, 132), (277, 132), (269, 133), (272, 133), (261, 134), (264, 134), (823, 134), (255, 135), (258, 135), (247, 136), (250, 136), (822, 136), (242, 137), (245, 137), (235, 138), (238, 138), (229, 139), (232, 139), (220, 140), (223, 140), (226, 140), (214, 141), (217, 141), (819, 141), (209, 142), (212, 142), (204, 143), (818, 143), (197, 144), (200, 144), (188, 145), (191, 145), (194, 145), (181, 146), (184, 146), (175, 147), (178, 147), (170, 148), (173, 148), (165, 149), (168, 149), (161, 150), (164, 150), (155, 151), (158, 151), (151, 152), (813, 152), (148, 153), (142, 154), (145, 154), (137, 155), (140, 155), (135, 156), (131, 157), (127, 158), (123, 159), (126, 159), (120, 160), (116, 161), (808, 161), (115, 162), (112, 163), (107, 164), (806, 164), (105, 165), (101, 166), (96, 167), (93, 168), (804, 168), (92, 169), (87, 170), (82, 171), (85, 171), (81, 172), (79, 173), (74, 174), (800, 174), (72, 175), (69, 176), (66, 177), (64, 178), (61, 179), (59, 180), (55, 181), (52, 182), (51, 183), (48, 184), (44, 185), (42, 186), (41, 187), (792, 188), (791, 189), (36, 190), (33, 191), (30, 193), (787, 195), (28, 198), (784, 200), (29, 202), (781, 204), (30, 207), (25, 209), (31, 211), (775, 212), (773, 215), (772, 217), (28, 219), (769, 221), (768, 222), (36, 225), (765, 226), (38, 228), (39, 230), (34, 232), (35, 234), (37, 236), (756, 238), (754, 240), (752, 242), (47, 244), (50, 244), (53, 244), (56, 244), (59, 244), (62, 245), (73, 245), (749, 246), (75, 248), (746, 250), (744, 252), (75, 255), (741, 256), (739, 258), (72, 261), (736, 262), (734, 264), (68, 266), (731, 268), (729, 270), (727, 272), (725, 274), (724, 275), (723, 277), (68, 279), (63, 281), (65, 284), (67, 286), (714, 287), (73, 289), (76, 289), (79, 290), (82, 290), (711, 290), (710, 291), (94, 293), (94, 295), (93, 297), (703, 298), (702, 300), (699, 303), (91, 305), (682, 306), (685, 306), (688, 306), (691, 306), (694, 306), (676, 307), (679, 307), (674, 308), (673, 310), (673, 312), (94, 314), (673, 314), (105, 317), (107, 320), (107, 322), (100, 325), (674, 327), (669, 329), (674, 331), (674, 333), (114, 336), (110, 339), (670, 340), (118, 342), (120, 345), (675, 347), (663, 349), (666, 349), (669, 349), (672, 349), (675, 349), (651, 350), (654, 350), (657, 350), (660, 350), (642, 351), (645, 351), (648, 351), (118, 352), (633, 352), (636, 352), (639, 352), (628, 353), (631, 353), (622, 354), (625, 354), (617, 355), (620, 355), (613, 356), (121, 357), (610, 357), (605, 358), (601, 359), (604, 359), (599, 360), (595, 361), (593, 362), (591, 363), (590, 364), (587, 365), (584, 366), (583, 367), (580, 368), (579, 369), (577, 370), (130, 372), (482, 373), (485, 373), (132, 374), (477, 374), (480, 374), (569, 374), (471, 375), (474, 375), (468, 376), (566, 376), (467, 377), (565, 377), (564, 378), (494, 379), (463, 380), (141, 381), (496, 381), (460, 382), (459, 383), (146, 384), (458, 385), (151, 386), (499, 386), (456, 387), (157, 388), (557, 388), (454, 389), (164, 390), (556, 390), (168, 391), (314, 391), (317, 391), (320, 391), (323, 391), (326, 391), (329, 391), (332, 391), (335, 391), (338, 391), (341, 391), (344, 391), (347, 391), (350, 391), (353, 391), (356, 391), (171, 392), (308, 392), (311, 392), (359, 392), (364, 392), (367, 392), (370, 392), (373, 392), (376, 392), (379, 392), (382, 392), (385, 392), (388, 392), (391, 392), (394, 392), (397, 392), (400, 392), (403, 392), (406, 392), (451, 392), (175, 393), (450, 393), (178, 394), (449, 394), (182, 395), (448, 395), (186, 396), (305, 396), (554, 396), (192, 397), (305, 397), (194, 398), (292, 398), (509, 398), (199, 399), (297, 399), (416, 399), (204, 400), (207, 400), (291, 400), (301, 400), (552, 400), (213, 401), (216, 401), (290, 401), (513, 401), (221, 402), (224, 402), (227, 402), (514, 402), (231, 403), (234, 403), (441, 403), (237, 404), (241, 404), (440, 404), (243, 405), (246, 405), (249, 405), (252, 405), (255, 405), (258, 405), (261, 405), (264, 405), (285, 405), (438, 405), (546, 405), (269, 406), (272, 406), (275, 406), (278, 406), (281, 406), (284, 406), (437, 406), (425, 407), (433, 407), (523, 407), (543, 407), (429, 408), (526, 408), (528, 409), (531, 409), (534, 409), (537, 409))\n"
     ]
    }
   ],
   "source": [
    "keepOneOutOf = 3\n",
    "\n",
    "c = 1\n",
    "track = []\n",
    "for coord in track_coord:\n",
    "    if( c == keepOneOutOf):\n",
    "        track.append(coord)\n",
    "        c = 1\n",
    "    else:\n",
    "        c += 1\n",
    "\n",
    "print(len(track))\n",
    "track_tuple = tuple(track)\n",
    "print(track_tuple)"
   ]
  }
 ],
 "metadata": {
  "interpreter": {
   "hash": "a17b1771daf03b1d85d31ea4392b44e89eacd342f0c053a96519d076e7afe3b2"
  },
  "kernelspec": {
   "display_name": "Python 3.9.7 64-bit ('3a_ia': conda)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.9.7"
  },
  "orig_nbformat": 4
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
