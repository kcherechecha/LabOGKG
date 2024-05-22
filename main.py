import tkinter as tk
import numpy as np
import random
from scipy.spatial import ConvexHull

points = []

def simple_largest_triangle(hull):
    best_area = 0
    best_triangle = []
    n = len(hull)
    for i in range(n):
        idx_a, idx_b, idx_c = largest_triangle_from_A(hull, i)
        if idx_a >= n or idx_b >= n or idx_c >= n:
            continue
        if area(hull[idx_a], hull[idx_b], hull[idx_c]) > best_area:
            best_area = area(hull[idx_a], hull[idx_b], hull[idx_c])
            best_triangle = [idx_a, idx_b, idx_c]
    return best_triangle

def largest_triangle_from_A(P, idx_a):
    def next(i):
        return (i + 1) % len(P)
    if len(P) == 3:
        return [0, 1, 2]
    idx_b = next(idx_a)
    idx_c = next(idx_b)
    best = [idx_a, idx_b, idx_c]
    while idx_b != idx_a:
        while area(P[idx_a], P[idx_b], P[idx_c]) <= area(P[idx_a], P[idx_b], P[next(idx_c)]):
            idx_c = next(idx_c)
        if area(P[idx_a], P[idx_b], P[idx_c]) > area(P[best[0]], P[best[1]], P[best[2]]):
            best = [idx_a, idx_b, idx_c]
        idx_b = next(idx_b)
    return best

def area(a, b, c):
    return abs((a[0] - c[0]) * (b[1] - c[1]) - (a[1] - c[1]) * (b[0] - c[0])) / 2

def plot_convex_hull_with_max_triangle(points, canvas):
    if len(points) < 3:
        return

    # Побудова опуклої оболонки
    points_array = np.array(points)
    hull = ConvexHull(points_array)
    hull_points = points_array[hull.vertices]

    # Знаходження трикутника з найбільшою площею
    max_triangle_indices = simple_largest_triangle(hull_points)
    if not max_triangle_indices:
        return

    max_triangle = [hull_points[i] for i in max_triangle_indices]

    canvas.delete('all')

    # Візуалізація точок
    for x, y in points:
        canvas.create_oval(x-2, y-2, x+2, y+2, fill='red')

    # Візуалізація опуклої оболонки
    for simplex in hull.simplices:
        x1, y1 = points_array[simplex[0]]
        x2, y2 = points_array[simplex[1]]
        canvas.create_line(x1, y1, x2, y2, fill='black')

    # Візуалізація трикутника найбільшої площі
    if max_triangle is not None:
        x1, y1 = max_triangle[0]
        x2, y2 = max_triangle[1]
        x3, y3 = max_triangle[2]
        canvas.create_line(x1, y1, x2, y2, fill='blue')
        canvas.create_line(x2, y2, x3, y3, fill='blue')
        canvas.create_line(x3, y3, x1, y1, fill='blue')
        coords = [x1, y1, x2, y2, x3, y3]
        canvas.create_polygon(coords, fill='', outline='blue', stipple='gray25')

def add_point():
    for i in range(int(points_entry.get())):
        x = random.randint(int(width*0.25), int(width*0.75))
        y = random.randint(int(height*0.25), int(height*0.75))
        canvas.create_oval(x-5, y-5, x+5, y+5, fill='red')
        points.append((x, y))

def clear_canvas():
    points.clear()
    canvas.delete('all')

def draw_triangle():
    if len(points) != 0:
        plot_convex_hull_with_max_triangle(points, canvas)

window = tk.Tk()
width = window.winfo_screenwidth()
height = window.winfo_screenheight()
window.geometry("%dx%d" % (width, height))
window.title("Convex Hull with Largest Inscribed Triangle")

canvas = tk.Canvas(window, width=width, height=height)

points_label = tk.Label(window, text="Number of points:")
points_label.pack(anchor='w')

points_entry = tk.Entry(window)
points_entry.pack(anchor='w')

add_button = tk.Button(window, text="Add Point", command=add_point)
add_button.pack(anchor='w')

clear_button = tk.Button(window, text="Clear Canvas", command=clear_canvas)
clear_button.pack(anchor='w')

triangle_button = tk.Button(window, text="Draw Triangle", command=draw_triangle)
triangle_button.pack(anchor='w')

canvas.pack()

window.mainloop()