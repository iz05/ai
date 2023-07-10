import urllib.request
import io, sys, random, math
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
    colors = []
    for a in range(0, round):
        for b in range(0, round):
            for c in range(0, round):
                colors.append((int(255 * a / (round - 1)), int(255 * b / (round - 1)), int(255 * c / (round - 1))))
    for i in range(0, WIDTH):
        for j in range(0, HEIGHT):
            color_index = get_min_index(pix[i,j], colors)
            pix[i,j] = colors[color_index]
    colorband(colors)
    # for i in range(0, WIDTH):
    #     for j in range(0, HEIGHT):
    #         pix[i,j] = (my_round(pix[i,j][0], round), my_round(pix[i,j][1], round), my_round(pix[i,j][2], round))
    img.save("naive" + str(K) + ".png") # Save the resulting image. Alter your filename as necessary.

def part1_dither():
    round = int(K ** (1 / 3))
    colors = []
    for a in range(0, round):
        for b in range(0, round):
            for c in range(0, round):
                colors.append((255 * a / (round - 1), 255 * b / (round - 1), 255 * c / (round - 1)))
    dither(colors)
    colorband(colors)
    img.save("naive_dithered_" + str(K) + ".png")

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

def heuristic(means):
    s = 0
    for i in range(0, K):
        for j in range(i + 1, K):
            s = sum((means[i][k] - means[j][k]) ** 2 for k in range(1, 3)) ** 0.5
    return s

def distance(color1, color2):
    return (sum((color1[i] - color2[i]) ** 2 for i in range(0, 3))) ** 0.5

def generate_starting_mean(colors):
    # means = []
    # while(len(means) < K):
    #     i = random.randint(0, WIDTH - 1)
    #     j = random.randint(0, HEIGHT - 1)
    #     if(pix[i,j] not in means):
    #         means.append(pix[i,j])
    # return means
    means = []
    means = random.sample(colors, 1)
    for i in range(0, K - 1):
        l = []
        for color in colors:
            if color not in means:
                s = 0
                for c in means:
                    s += math.log(distance(c, color))
                l.append((color, s))
        l = sorted(l, key = lambda x : -1 * x[1])
        best_color = l[0][0]
        means.append(best_color)
    return means

def add(tup1, tup2, scalar):
    return (int(tup1[0] + tup2[0] * scalar), int(tup1[1] + tup2[1] * scalar), int(tup1[2] + tup2[2] * scalar))

def dither(means):
    for j in range(0, HEIGHT):
        for i in range(0, WIDTH):
            color_index = get_min_index(pix[i,j], means)
            color = means[color_index]
            error = (pix[i,j][0] - color[0], pix[i,j][1] - color[1], pix[i,j][2] - color[2])
            pix[i,j] = (int(color[0]), int(color[1]), int(color[2]))
            if i < WIDTH - 1:
                pix[i+1,j] = add(pix[i+1,j], error, 7 / 16)
            if i < WIDTH - 1 and j < HEIGHT - 1:
                pix[i+1,j+1] = add(pix[i+1,j+1], error, 1 / 16)
            if j < HEIGHT - 1:
                pix[i,j+1] = add(pix[i,j+1], error, 5 / 16)
            if j < HEIGHT - 1 and i > 0:
                pix[i-1,j+1] = add(pix[i-1,j+1], error, 3 / 16)

def part2():
    rgb = store()
    colors = rgb.keys() 
    means = []
    generation = 0
    means = generate_starting_mean(colors)
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
    img.save("kmeans" + str(K) + ".png")

def part2_dither():
    rgb = store()
    colors = rgb.keys() 
    means = []
    generation = 0
    means = generate_starting_mean(colors)
    categories = {}
    for color in colors:
        index = get_min_index(color, means)
        categories[color] = index
    change = True
    while(change):
        # print("Generation %s" % generation)
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
    dither(means)
    colorband(means)
    # img.save("kmeans_dithered_" + str(K) + ".png")
    img.save("kmeansout.png")

def cost(categories, means):
    d = 0
    for i in range(0, len(means)):
        for color in categories:
            if categories[color] == i:
                d += distance(color, means[i])
    return d

def get(categories, i):
    s = set()
    for color in categories:
        if categories[color] == i:
            s.add(color)
    return s

def k_medoids():
    rgb = store()
    colors = rgb.keys() 
    means = []
    generation = 0
    means = generate_starting_mean(colors)
    categories = {}
    for color in colors:
        index = get_min_index(color, means)
        categories[color] = index
    change = True
    current_cost = cost(categories, means)
    count = 0
    while(change and count < 5):
        # print("Generation %s" % count)
        change = False
        for i in range(0, len(means)):
            mean = means[i]
            if not change:
                for color in get(categories, i):
                    if not change and color != mean:
                        new_means = means.copy()
                        new_means[i] = color
                        new_categories = {}
                        for c in colors:
                            index = get_min_index(c, new_means)
                            new_categories[c] = index
                        temp_cost = cost(new_categories, new_means)
                        if temp_cost < current_cost:
                            current_cost = temp_cost
                            categories = new_categories
                            means = new_means
                            change = True
                            break
        count += 1
    dither(means)
    colorband(means)
    img.save("kmedoids.png")

k_medoids()