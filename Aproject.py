# import the necessary packages
import sys

sys.path.append('C:\Python36\Lib\site-packages\cv2')
import numpy as np
import cv2
import math

# load the image
first_read_image = cv2.imread("res.jpg")

# convert image from BGR to RGB
image = cv2.cvtColor(first_read_image, cv2.COLOR_BGR2RGB)

rows, columns, channels = image.shape
# rows,columns,channels

# print the shape of image
print('Image shape: ', image.shape)

# get mean color value of the image
mean_color = cv2.mean(image)
# print the mean
print('mean: ', mean_color)

# make 3 new arrays with size equal to number of columns in small image
numbers_of_dark_pixels_in_each_column = [0 for i in range(columns)]
addition_of_row_numbers_having_dark_pixels_in_each_column = [0 for i in range(columns)]
average_of_row_numbers_having_dark_pixels_in_each_column = [0 for i in range(columns)]

# travel row by row downwards in each column from left to right in small image
global num
for x in range(0, columns):
    num = 0
    for y in range(0, rows):
        # get pixel value in small image and assign to a new variable res
        res = image[y, x]

        # res is empty if no image loaded, then continue
        if res is None:
            continue
        # if the respecitve values stored in res are greater than half of the respective values in the mean color of the small image
        # then pass (these are the light parts of the image)
        # if not, increment num by 1 and set respective array position of avgy equal to column number as the value already stored plus y
        if res[0] > mean_color[0] * 0.5 and res[1] > mean_color[1] * 0.5 and res[2] > mean_color[2] * 0.5:
            pass
        else:
            num += 1
            addition_of_row_numbers_having_dark_pixels_in_each_column[x] += y

    # once the iteration of rows along a column is over,
    # if num is greater than 2, set value in nums at index equal to column number, as num
    # and set value in avgy at index equal to column number, as (value already there divided by num)
    if num > 2:
        numbers_of_dark_pixels_in_each_column[x] = num
        average_of_row_numbers_having_dark_pixels_in_each_column[x] = (
                    (addition_of_row_numbers_having_dark_pixels_in_each_column[x]) / num)

average_dark_pixels = 0
count = 0
for x in range(0, columns):
    if numbers_of_dark_pixels_in_each_column[x] > 0:  # if nums(column number) is greater than 0, then do this
        average_dark_pixels += numbers_of_dark_pixels_in_each_column[
            x]  # add the values in nums array that are greater than 0
        count += 1  # count the number of values greater than 0

# gettin row and column values to extract out part of image and draw rectangle
x_min = -1
x_max = 0

if count > 0:  # if there are values greater than 0 in nums array
    average_dark_pixels /= count  # get the average times the num has been greater than 0 by dividing total by number of values greater than 0
    for x in range(0, columns):
        if numbers_of_dark_pixels_in_each_column[x] > average_dark_pixels + 15:  # if nums(column number) is greater than ((average times the num has been greater than 0) + 15)
            if x_min < 0:  # this will happen only in first iteration as minx is -1 and after that minx is updated to x
                x_min = x  # set minx as respective index of nums array
            x_max = x  # set maxx as respective index of nums array

if x_min >= 0:  # if minx is greater than or equal to 0 (ie. respective index of nums array saved above is higher than 0)
    y_min = average_of_row_numbers_having_dark_pixels_in_each_column[x_min]
    y_max = average_of_row_numbers_having_dark_pixels_in_each_column[x_max]
    x_min_2 = x_min - 20

    if x_min_2 < 0:
        x_min_2 = 0
    if x_min_2 > len(average_of_row_numbers_having_dark_pixels_in_each_column) - 1:
        x_min_2 = len(average_of_row_numbers_having_dark_pixels_in_each_column) - 1

    x_max_2 = x_max + 20
    if x_max_2 < 0:
        x_max_2 = 0
    if x_max_2 > len(average_of_row_numbers_having_dark_pixels_in_each_column) - 1:
        x_max_2 = len(average_of_row_numbers_having_dark_pixels_in_each_column) - 1

    ratio = (average_of_row_numbers_having_dark_pixels_in_each_column[x_max_2] -
             average_of_row_numbers_having_dark_pixels_in_each_column[x_min_2]) / ((x_max_2) - (x_min_2))
    y_min = (int)(ratio * (x_min - x_min_2) + average_of_row_numbers_having_dark_pixels_in_each_column[x_min_2])
    y_max = (int)(ratio * (x_max - x_max_2) + average_of_row_numbers_having_dark_pixels_in_each_column[x_max_2])

    w = x_max - x_min #width of part of image to be extracted out