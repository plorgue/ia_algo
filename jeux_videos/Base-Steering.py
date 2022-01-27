from operator import length_hint
from pickletools import string1
import sys, math
import pygame
import pygame.draw
import random as rd

__circuit__ = (
    (100, 160),
    (110, 150),
    (170, 150),
    (240, 150),
    (300, 150),
    (350, 180),
    (350, 190),
    (340, 220),
    (310, 240),
    (280, 240),
    (240, 250),
    (210, 250),
    (180, 250),
    (150, 250),
    (140, 280),
    (160, 300),
    (190, 320),
    (200, 330),
    (230, 340),
    (270, 360),
    (290, 360),
    (330, 370),
    (350, 370),
    (390, 360),
    (400, 340),
    (410, 300),
    (410, 280),
    (440, 240),
    (450, 230),
    (470, 200),
    (500, 170),
    (510, 170),
    (560, 170),
    (570, 180),
    (610, 190),
    (640, 210),
    (660, 220),
    (700, 250),
    (750, 280),
    (770, 290),
    (800, 310),
    (830, 330),
    (840, 330),
    (880, 320),
    (890, 280),
    (850, 250),
    (810, 230),
    (800, 210),
    (820, 180),
    (840, 170),
    (880, 180),
    (900, 180),
    (950, 200),
    (960, 260),
    (960, 270),
    (980, 310),
    (990, 330),
    (980, 370),
    (980, 390),
    (950, 420),
    (920, 430),
    (880, 430),
    (850, 430),
    (820, 430),
    (790, 430),
    (750, 430),
    (720, 430),
    (680, 430),
    (660, 430),
    (620, 430),
    (590, 430),
    (550, 430),
    (520, 430),
    (490, 430),
    (460, 430),
    (420, 430),
    (390, 430),
    (360, 430),
    (330, 430),
    (290, 430),
    (260, 430),
    (230, 430),
    (180, 420),
    (170, 420),
    (150, 370),
    (130, 350),
    (110, 330),
    (80, 320),
    (60, 310),
    (20, 270),
    (30, 210),
    (40, 200),
    (60, 170),
)

__screenSize__ = (1080, 720)

# Utility functions for handling points
# I should probably build a class of vectors
def vecDiff(v1, v2):
    return (v1[0] - v2[0], v1[1] - v2[1])


def vecAdd(v1, v2):
    return (v2[0] + v1[0], v2[1] + v1[1])


def vecScalarMult(v, s):
    return (v[0] * s, v[1] * s)


def vecDot(v1, v2):
    return v1[0] * v2[0] + v1[1] * v2[1]


def vecInter(scalar, v1, v2):
    return (v1[0] + scalar * (v2[0] - v1[0]), v1[1] + scalar * (v2[1] - v2[0]))


def approximateLength(v1):
    """This should be rewritten with an approximate length function (approximating it with no sqrt calls)"""
    return math.sqrt(v1[0] ** 2 + v1[1] ** 2)


def approximateDistance(v1, v2):
    return approximateLength(vecDiff(v1, v2))


def isAhead(speed, pos1, pos2, vision):
    """
        Détermine si pos2 est dans un rectangle devant pos1.
        
        Params:
        - speed (vecteur) qui donne la direction du rectangle par rapport à pos1
        - pos1 (position)
        - pos2 (position)
        - vision (entier naturel) donne la longueur du rectangle 
    """
    l1 = speed[1] / speed[0] * (pos2[0] - pos1[0] + speed[1]) + pos1[1] + speed[0]
    l2 = speed[1] / speed[0] * (pos2[0] - pos1[0] - speed[1]) + pos1[1] - speed[0]

    l3 = speed[0] / speed[1] * (- pos2[0] + pos1[0]) + pos1[1]
    l4 = speed[0] / speed[1] * (- pos2[0] + pos1[0]  + vision * speed[0]) + pos1[1] + vision * speed[1]

    sign1 = 1 if speed[0] > 0 else -1
    sign2 = 1 if speed[1] > 0 else -1
    return (
        l1 * sign1 > pos2[1] * sign1
        and l2 * sign1 < pos2[1] * sign1
        and l3 * sign2 < pos2[1] * sign2
        and l4 * sign2 > pos2[1] * sign2
    )


# Handles Vehicules
class Vehicule:
    _coords = (0, 0)  # vector
    _speed = (2, 4)  # vector
    _maxspeed = 50
    _force = (0, 0)  # accelerating force
    _maxAccForce = 10
    _color = (200, 100, 100)
    _colorfg = tuple([int(c / 2) for c in _color])
    _radius = 6
    _seeInFuture = 3
    _id_overtaked = None

    def __init__(
        self,
        coords=(0, 0),
        speed=(1, 1),
        maxspeed=50,
        force=(1, 1),
        maxforce=20,
        color=(200, 100, 100),
        radius=6,
        seeInFuture=3,
    ):
        self._coords = coords
        self._speed = speed
        self._force = force
        self._maxspeed = maxspeed
        self._color = color
        self._maxforce = maxforce
        self._radius = radius
        self._seeInFuture = seeInFuture
        self._colorfg = tuple([int(c / 2) for c in color])
        self._objective = coords
        self._proj = coords

    def position(self):
        return self._pos

    def steerUpdate(self, track, vehicules):
        self._force = (0, 0)
        self._force = vecAdd(self._force, self.steerPathFollow(track))

    def steerPathFollow(self, track):
        (s, p, _) = track._closestSegmentPointToPoint(self._coords)

        self._proj = p
        
        # Récupération de 2 positions futures sur la piste à plus ou moins long terme
        (_, futurePosition) = track._segmentPointAddLength(
            s, p, max(10, approximateLength(self._speed)) * self._seeInFuture
        )
        (_, farFuturePosition) = track._segmentPointAddLength(
            s, p, approximateLength(self._speed) * self._seeInFuture * 2
        )
        self._objective = farFuturePosition

        # Calcul des angles entre ces position et la position future si le vehicule allé tout droit 
        # Ces angles permettent de savoir à l'avance s'il y aura un virage
        # On calcule deux angles à long et moyen terme pour détecter les chicanes 
        objective = vecDiff(futurePosition, self._coords)
        farTurn = math.acos(
            vecDot(objective, self._speed)
            / (approximateLength(self._speed) * approximateLength(objective))
        )
        objective = vecDiff(farFuturePosition, self._coords)
        closeTurn = math.acos(
            vecDot(objective, self._speed)
            / (approximateLength(self._speed) * approximateLength(objective))
        )
        
        # On récupère l'angle le plus aigu car il nécessitera de plus ralentir
        # Le virage a moyen terme doit impliqué un freinage plus important d'ou le coefficient 1.2
        angle = max(farTurn, 1.2 * closeTurn)

        # Calcul de la force pour atteindre la position future sur la piste
        force = vecDiff(futurePosition, self._coords)
        force = vecScalarMult(force, self._maxAccForce / approximateLength(force))

        # Calcul de la force de freinage colinéaire et inverse à la vitesse et proportionnelle à l'angle du 
        # prochain virage
        slowForce = vecScalarMult(self._speed, -1.2 * angle)
        slowForce = (slowForce[0] / (abs(angle) + 1), slowForce[1] / (abs(angle) + 1))

        # Ajout de la force de freinage à la force initial
        force = vecAdd(force, slowForce)
        return force

    def drawMe(self, screen):
        pygame.draw.circle(screen, self._color, self._coords, Vehicule._radius, 0)
        pygame.draw.circle(screen, self._colorfg, self._coords, Vehicule._radius, 1)
        # pygame.draw.circle(screen, self._colorfg, self._objective, Vehicule._radius/2, 1)
        # pygame.draw.circle(screen, self._colorfg, self._proj, Vehicule._radius/2, 0)


class SetOfVehicules:
    _vehicules = []

    def handleCollisions(self):
        "Simple collision checking. Not a very good one, but may do the job for simple simulations"
        for i, v1 in enumerate(self._vehicules):
            for v2 in self._vehicules[i + 1 :]:
                offset = vecDiff(v2._coords, v1._coords)
                al = approximateLength(offset)
                if al != 0 and al < v1._radius + v2._radius - 1:  # collision
                    v1._coords = (
                        int(v1._coords[0] + offset[0] / al * (v1._radius + v2._radius)),
                        int(v2._coords[1] + offset[1] / al * (v1._radius + v2._radius)),
                    )

    def updatePositions(self):
        for v in self._vehicules:
            v._speed = vecAdd(v._speed, v._force)
            v._speed = (min(v._maxspeed, v._speed[0]), min(v._maxspeed, v._speed[1]))

            # Pour chaque véhicule s'il y a un autre véhicule proche autour
            # on regarde s'il se situe devant ( avec la méthode isAhead() )
            # si oui on ralenti proportionnelement à la distance à laquelle il se trouve
            # Si le vehicule devant est juste collé alors on arrête le vehicule 
            for v2 in self._vehicules:
                dist = approximateDistance(v._coords, v2._coords)
                length = v._seeInFuture * approximateLength(v._speed)
                if dist < length and isAhead(v._speed, v._coords, v2._coords, v._seeInFuture):
                    v._speed = vecScalarMult(v._speed, min(1, dist/length))

            v._coords = (
                v._coords[0] + int(v._speed[0]),
                v._coords[1] + int(v._speed[1]),
            )

    def append(self, item):
        self._vehicules.append(item)

    def drawMe(self, screen, scene=None):
        for v in self._vehicules:
            v.drawMe(screen)


class Track:
    _circuit = None
    _cback = (128, 128, 128)
    _cfore = (10, 10, 10)
    _width = 35
    _screen = None
    _cachedLength = []
    _cachedNormals = []

    def __init__(self, screen):
        self._circuit = __circuit__
        self._screen = screen
        for i in range(len(self._circuit)):
            self._cachedNormals.append(
                vecDiff(
                    self._circuit[i],
                    self._circuit[len(self._circuit) - 1 if i - 1 < 0 else i - 1],
                )
            )
            self._cachedLength.append(approximateLength(self._cachedNormals[i]))
            self._cachedNormals[i] = (
                self._cachedNormals[i][0] / self._cachedLength[i],
                self._cachedNormals[i][1] / self._cachedLength[i],
            )

    def _segmentPointAddLength(self, segment, point, length):
        """
        get the segment and point (on it) after adding length to the segment and point (on it), by following the path
        """
        nextStep = approximateDistance(point, self._circuit[segment])
        if nextStep > length:  # We stay on the same segment
            nextPoint = vecAdd(
                point, vecScalarMult(self._cachedNormals[segment], length)
            )
            return (segment, (int(nextPoint[0]), int(nextPoint[1])))
        length -= nextStep
        segment = segment + 1 if segment + 1 < len(self._circuit) else 0
        while length > self._cachedLength[segment]:
            length -= self._cachedLength[segment]
            segment = segment + 1 if segment + 1 < len(self._circuit) else 0
        nextPoint = vecAdd(
            self._circuit[segment - 1 if segment > 0 else len(self._circuit) - 1],
            vecScalarMult(self._cachedNormals[segment], length),
        )
        return (segment, (int(nextPoint[0]), int(nextPoint[1])))

    def _closestSegmentPointToPoint(self, point):
        """
        return (
                   index element du circuit,
                   projection du point de la piste leplus proche,
                   distance au centre de la piste
               )
        """
        bestLength = None
        bestPoint = None
        bestSegment = None
        for i in range(0, len(self._circuit)):
            p = self._closestPointToSegment(i, point)
            l = approximateDistance(p, point)
            if bestLength is None or l < bestLength:
                bestLength = l
                bestPoint = p
                bestSegment = i
        return (bestSegment, bestPoint, bestLength)

    def _closestPointToSegment(self, numSegment, point):
        """Returns the closest point on the circuit segment from point"""
        p0 = self._circuit[
            len(self._circuit) - 1 if numSegment - 1 < 0 else numSegment - 1
        ]
        p1 = self._circuit[numSegment]
        local = vecDiff(point, p0)
        projection = vecDot(local, self._cachedNormals[numSegment])
        if projection < 0:
            return p0
        if projection > self._cachedLength[numSegment]:
            return p1
        return vecAdd(p0, vecScalarMult(self._cachedNormals[numSegment], projection))

    def drawMe(self, scene=None):

        for p in self._circuit:  # Draw simple inner joins
            pygame.draw.circle(
                self._screen, self._cback, p, int(self._width / 2) - 1, 0
            )
        pygame.draw.lines(self._screen, self._cback, True, self._circuit, self._width)
        pygame.draw.lines(self._screen, self._cfore, True, self._circuit, 1)

        if True:
            for i, p in enumerate(self._circuit):
                pygame.draw.line(
                    self._screen,
                    (0, 0, 250),
                    p,
                    vecAdd(p, vecScalarMult(self._cachedNormals[i], 50)),
                )


class Scene:
    _track = None
    _vehicules = None
    _screen = None
    _font = None

    _mouseCoords = (0, 0)

    def __init__(self, screenSize=__screenSize__):
        pygame.init()
        self._screen = pygame.display.set_mode(screenSize)
        self._track = Track(self._screen)
        self._vehicules = SetOfVehicules()
        # self._font = pygame.font.SysFont('Arial', 25)

    def drawMe(self):
        self._screen.fill((0, 0, 0))
        self._track.drawMe(scene=self)
        self._vehicules.drawMe(self._screen, scene=self)

        # Illustrate the closestSegmentPointToPoint function
        (s, p, l) = self._track._closestSegmentPointToPoint(self._mouseCoords)
        pygame.draw.line(self._screen, (128, 255, 128), p, self._mouseCoords)
        # print(self._track._segmentPointAddLength(s,p,150))
        pygame.draw.circle(
            self._screen,
            (128, 255, 128),
            self._track._segmentPointAddLength(s, p, 150)[1],
            20,
            1,
        )

        pygame.display.flip()

    def drawText(self, text, position, color=(255, 128, 128)):
        self._screen.blit(self._font.render(text, 1, color), position)

    def update(self):
        for v in self._vehicules._vehicules:
            v.steerUpdate(self._track, self._vehicules)
        self._vehicules.updatePositions()
        self._vehicules.handleCollisions()
        self.drawMe()

    def eventClic(self, coord, b):
        print("Adding Vehicule at ", coord[0], ",", coord[1])
        self._vehicules.append(
            Vehicule(
                (coord[0], coord[1]),
                color=(rd.randint(0, 255), rd.randint(0, 255), rd.randint(0, 255)),
            )
        )

    def recordMouseMove(self, coord):
        self._mouseCoords = coord


def main():
    scene = Scene()
    done = False
    pause = False
    clock = pygame.time.Clock()
    while done == False:
        clock.tick(10)
        scene.update()
        scene.drawMe()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause = True
                    while pause and not done:
                        clock.tick(10)
                        for ev in pygame.event.get():
                            if ev.type == pygame.KEYDOWN:
                                pause = ev.key != pygame.K_p
                                done = ev.key == pygame.K_q
                else:
                    done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                scene.eventClic(event.dict["pos"], event.dict["button"])
            elif event.type == pygame.MOUSEMOTION:
                scene.recordMouseMove(event.dict["pos"])

    pygame.quit()


if not sys.flags.interactive:
    main()
