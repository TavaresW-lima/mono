import cv2

BASE_SPEED = 1

HORIZONTAL_WARNING_LIMITS = (256, 1024)
HORIZONTAL_DANGER_LIMITS = (127, 1152)
HORIZONTAL_CLIP_LIMITS = (64, 1215)
VERTICAL_DANGER_LIMITS = (72, 648)
VERTICAL_CLIP_LIMITS = (36, 683)
VERTICAL_CEILING_LIMIT = 200
HORIZONTAL_CENTER = 640
VERTICAL_CENTER = 360

LEFT_DIRECTION = 1  # inverted
RIGHT_DIRECTION = 0  # inverted
UP_DIRECTION = 0
DOWN_DIRECTION = 1


def verifyTrackDisplacement(minX, minY, maxX, maxY):
    senX, velX = getAdjustmentX(minX, maxX)
    senY, velY = getAdjustmentY(minY, maxY)
    return senX, velX, senY, velY


def getAdjustmentX(minX, maxX):
    displacement = 0
    direction = 0

    tooLeft = minX <= HORIZONTAL_WARNING_LIMITS[0]
    tooRight = maxX >= HORIZONTAL_WARNING_LIMITS[1]
    if tooLeft and tooRight:
        return direction, displacement

    if tooLeft:
        displacement = BASE_SPEED
        direction = LEFT_DIRECTION
    elif tooRight:
        displacement = BASE_SPEED
        direction = RIGHT_DIRECTION

    if direction == LEFT_DIRECTION:
        if minX <= HORIZONTAL_DANGER_LIMITS[0]:
            displacement = displacement * 2
        if minX <= HORIZONTAL_CLIP_LIMITS[0]:
            displacement = displacement * 2
    else:
        if maxX >= HORIZONTAL_CLIP_LIMITS[1]:
            displacement = displacement * 2
        if maxX >= HORIZONTAL_DANGER_LIMITS[1]:
            displacement = displacement * 2
    return direction, displacement


def getAdjustmentY(minY, maxY):
    displacement = 0
    direction = 0

    if minY <= VERTICAL_DANGER_LIMITS[0]:
        displacement = BASE_SPEED
        direction = UP_DIRECTION
    elif minY >= VERTICAL_CEILING_LIMIT:
        displacement = BASE_SPEED
        direction = DOWN_DIRECTION

    if direction == UP_DIRECTION:
        if minY <= VERTICAL_CLIP_LIMITS[0]:
            displacement = displacement * 2
    else:
        if maxY >= VERTICAL_CLIP_LIMITS[1]:
            displacement = displacement * 2
    return direction, displacement


def drawRulers(img):
    cv2.rectangle(
        img,
        (HORIZONTAL_WARNING_LIMITS[0], VERTICAL_DANGER_LIMITS[0]),
        (HORIZONTAL_WARNING_LIMITS[1], VERTICAL_DANGER_LIMITS[1]),
        (0, 255, 0),
        1,
    )  # WARNING
    cv2.rectangle(
        img,
        (HORIZONTAL_DANGER_LIMITS[0], VERTICAL_DANGER_LIMITS[0]),
        (HORIZONTAL_DANGER_LIMITS[1], VERTICAL_DANGER_LIMITS[1]),
        (0, 255, 255),
        1,
    )  # DANGER
    cv2.rectangle(
        img,
        (HORIZONTAL_CLIP_LIMITS[0], VERTICAL_CLIP_LIMITS[0]),
        (HORIZONTAL_CLIP_LIMITS[1], VERTICAL_CLIP_LIMITS[1]),
        (0, 0, 255),
        1,
    )  # CLIP
