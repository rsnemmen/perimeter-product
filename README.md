Smaller shapes, perimeter product algorithm
===================================

## My approach

Tech stack: 

- Python
- Jupyter for prototyping
- `networkx` for handling graphs

## Algorithm outline

When looking at
Our eyes immediately realize the intersections between lines and the geometrical "subshapes" they form, but the computer has no idea about them. We need to use geometry to teach the computer to identify these shapes. There are three basic steps.

1. Find intersections between lines✅
2. Establish new edges in addition to those of the original shape✅
3. Identify closed regions✅

Below I will break down steps 1 to 3.



## Problem statement

This repo tries to solve the following problem. You are given a list of line segments represented as a set of two x,y points.

```
( ((x1, y1), (x2, y2)),
((x3, y3), (x4, y4)), …. )
```

For an example of a simple square:

```
( ((1, 1), (1, 2)),
((1, 2), (2, 2)),
((2, 2), (2, 1)),
((2, 1), (1, 1)), )
```

The final result we wish to calculate is to find the multiplicative product of all perimeters of all the individual enclosed areas. For the example above, it is straightforward where there is only one enclosed area that has a perimeter of 4. So the final answer is 4.

For a stranger shape, we draw an hourglass shape:

```
( ((1, 1), (1, 2)),
((1, 2), (2, 1)),
((2, 1), (2, 2)),
((2, 2), (1, 1)), )
```

Note: There are two areas, but we do not explicitly write the intersection point at the neck of the hourglass.

Each individual triangle has a perimeter of ~2.4142 or ( 1+sqrt(2) ), so the product of all perimeters is 5.82842 or (3 + 2 * sqrt(2)). Note, we expect the floating point solution, not the exact values. They are there just for illustrative purposes.

For a more complex shape, we draw a window:
( ((1, 1), (1, 2)),
((1, 2), (2, 2)),
((2, 2), (2, 1)),
((2, 1), (1, 1)),
((1.5, 1), (1.5, 2)),
((1, 1.5), (2, 1.5)), )

In this example there are 4 areas each with a perimeter of 2. Making the final answer 16.

Note: We do NOT double count the larger original square, nor the 4 possible rectangles.