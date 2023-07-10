import math, csv, random

K_MEANS = 6

def get_stars():
    file = open('star_data.csv')
    csvreader = csv.reader(file)
    next(csvreader)
    stars = []
    for row in csvreader:
        stars.append([math.log10(int(row[0])), math.log10(float(row[1])), math.log10(float(row[2])), float(row[3]), int(row[4])])
    return stars

def get_min_index(star, means):
    min_index = -1
    min_error = 10000000000
    for i in range(0, len(means)):
        error = sum((star[j] - means[i][j]) ** 2 for j in range(0, 4))
        if error < min_error:
            min_error = error
            min_index = i
    return min_index

def average(l):
    output = [0, 0, 0, 0, 0]
    for item in l:
        output[0] += item[0]
        output[1] += item[1]
        output[2] += item[2]
        output[3] += item[3] 
        output[4] += item[4]
    output[0] /= len(l)
    output[1] /= len(l)
    output[2] /= len(l)
    output[3] /= len(l)
    output[4] /= len(l)
    return output

def k_means(stars):
    global K_MEANS
    means = random.sample(stars, K_MEANS)
    categories = {}
    for i in range(0, K_MEANS):
        categories[i] = []
    for star in stars:
        index = get_min_index(star, means)
        categories[index].append(star)
    change = True
    while(change):
        change = False
        new_means = []
        for i in range(0, len(means)):
            new_means.append(average(categories[i]))
        new_categories = {}
        for i in range(0, len(means)):
            new_categories[i] = []
        for i in range(0, len(means)):
            for star in categories[i]:
                index = get_min_index(star, new_means)
                new_categories[index].append(star)
                if index != i:
                    change = True
        means = new_means
        categories = new_categories
    return categories

def display_categories(categories):
    for i in range(0, len(categories)):
        print("GROUP %s:" % i)
        for star in categories[i]:
            print("Type %s: %s" % (star[4], star[:4]))
        print()

stars = get_stars()
categories = k_means(stars)
display_categories(categories)

# answers to kmeans stars questions
# 1) It gets pretty close. Usually only one or two groups have mixed star types.
# 2) Variations are which stars get mixed together. Usually 0, 1, 2 or 3, 4, 5 get mixed together. For 5 means, there was more mixing. For 7 means, there was separation within one type of star, usually into two groups.
# 3) The diagrams indicate that category 1 and 2 are least likely to form a successful cluster. This aligns with my results.
# 4) Strengths: can quickly categorize datasets. Weaknesses: not very accurate and results can vary greatly due to randomness.
