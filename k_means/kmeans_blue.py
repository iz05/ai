import urllib.request
import io, sys, random
from PIL import Image

K = int(sys.argv[2])
URL = sys.argv[1]
f = io.BytesIO(urllib.request.urlopen(URL).read()) # Download the picture at the url as a file object
img = Image.open(f) # You can also use this on a local file; just put the local filename in quotes in place of f.
WIDTH, HEIGHT = img.size # A tuple. Note: width first THEN height. PIL goes [x, y] with y counting from the top of the frame.
pix = img.load() # Pix is a pixel manipulation object; we can assign pixel values and img will change as we do so.

def my_round(num, round):
    for i in range(1, round + 2):
        if num <= 255 * i // (round + 1):
            return 255 * (i - 1) // round

def part1():
    round = int(K ** (1 / 3))
    for i in range(0, WIDTH):
        for j in range(0, HEIGHT):
            color = (my_round(pix[i,j][0], round), my_round(pix[i,j][1], round), my_round(pix[i,j][2], round))
            # print(color)
            pix[i,j] = color
    img.save("my_image_8_naive.png") # Save the resulting image. Alter your filename as necessary.

def store():
    rgb = {}
    for i in range(0, WIDTH):
        for j in range(0, HEIGHT):
            if pix[i,j] not in rgb:
                rgb[pix[i,j]] = set()
            rgb[pix[i,j]].add((i, j))
    return rgb

def get_min_index(star, means):
    min_index = -1
    min_error = 10000000000
    for i in range(0, len(means)):
        error = sum((star[j] - means[i][j]) ** 2 for j in range(0, 3))
        if error < min_error:
            min_error = error
            min_index = i
    return min_index

def average(l, i):
    output = (0, 0, 0)
    count = 0
    for item in l:
        if l[item] == i:
            output = (output[0] + item[0], output[1] + item[1], output[2] + item[2])
            count += 1
    return (output[0] / count, output[1] / count, output[2] / count)

def colorband(means):
    width = WIDTH // K
    height = min(width, HEIGHT // 10)
    for i in range(0, K):
        mean_color = (int(means[i][0]), int(means[i][1]), int(means[i][2]))
        for x in range(width * i, width * (i + 1)):
            for y in range(HEIGHT - 1, HEIGHT - height, -1):
                pix[x,y] = mean_color

def part2():
    rgb = store()
    colors = rgb.keys() 
    means = []
    generation = 0
    while(len(means) < K):
        i = random.randint(0, WIDTH - 1)
        j = random.randint(0, HEIGHT - 1)
        if(pix[i,j] not in means):
            means.append(pix[i,j])
    categories = {}
    for color in colors:
        index = get_min_index(color, means)
        categories[color] = index
    change = True
    while(change):
        print("Generation %s" % generation)
        change = False
        means = []
        for i in range(0, K):
            means.append(average(categories, i))
        for color in categories:
            index = get_min_index(color, means)
            if index != categories[color]:
                change = True
            categories[color] = index
        generation += 1
    for color in categories:
        mean_color = means[categories[color]]
        for i, j in rgb[color]:
            pix[i,j] = (int(mean_color[0]), int(mean_color[1]), int(mean_color[2]))
    colorband(means)
    img.save("kmeansout_blue.png")

part2()