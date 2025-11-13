print("H")
print(5 + 5)

# Simple plot example: sequence from -100 to 100
# Create x and y vectors and draw a line plot
x <- seq(-100, 100, 1)
y <- x
plot(x, y,
	type = "b",     # line plot; use "p" for points, "b" for both
	col = "yellow",
	lwd = 0.5,
	main = "Line plot: y = x",
	xlab = "x",
	ylab = "y")

# Uncomment additional examples to try them interactively or via Rscript
# Scatter (points):
# plot(x, x^2, type = "p", pch = 19, col = "red", main = "Points: y = x^2")
# Histogram:
# hist(rnorm(1000), breaks = 30, col = "lightgray", main = "Histogram of normal samples")
