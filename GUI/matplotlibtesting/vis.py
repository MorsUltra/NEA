def print_cube(string: str) -> None:
    import matplotlib.pyplot as plt

    from GUI.matplotlibtesting import colours

    figure = plt.figure()
    ax = figure.add_subplot(111, projection="3d")

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.xaxis.set_ticks([])
    ax.yaxis.set_ticks([])
    ax.zaxis.set_ticks([])
    ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))

    def plot_it(x, y, z, colour):
        ax.plot_wireframe(x, y, z, rstride=1, cstride=1, color=colour)

    string = string.replace(" ", "")

    for f, col in enumerate(colours.col_coords):
        plot_it(*col.value, colours.cccolours[colours.ccolours[string[f]]])

    alpha_plotX, alpha_plotY = colours.numpy.meshgrid(colours.numpy.arange(-3, 4, 1), colours.numpy.arange(-3, 4, 1))
    neg32 = colours.numpy.full_like(alpha_plotX, -3)
    pos32 = colours.numpy.full_like(alpha_plotX, 3)
    ax.plot_surface(alpha_plotX, pos32, alpha_plotY, alpha=0.1, color="black")
    ax.plot_surface(alpha_plotX, alpha_plotY, neg32, alpha=0.1, color="black")
    ax.plot_surface(neg32, alpha_plotX, alpha_plotY, alpha=0.1, color="black")

    plt.show()