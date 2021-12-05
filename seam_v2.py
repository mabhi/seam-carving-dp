"""
A re-implementation of the second step in the seam carving algorithm: finding
the lowest-energy seam in an image. In this version of the algorithm, not only
is the energy value of the seam determined, but it's possible to reconstruct the
entire seam from the top to the bottom of the image.

The function you fill out in this module will be used as part of the overall
seam carving process. If you run this module in isolation, the lowest-energy
seam will be visualized:

    python3 seam_v2.py surfer.jpg surfer-seam-energy-v2.png
"""


import sys

from energy import compute_energy
from utils import Color, read_image_into_array, write_array_into_image


class SeamEnergyWithBackPointer:
    """
    Represents the total energy of a seam along with a back pointer:

      - Stores the total energy of a seam that ends at some position in the
        image. The position is not stored because it can be inferred from where
        in a 2D grid this object appears.

      - Also stores the x-coordinate for the pixel in the previous row that led
        to this particular seam energy. This is the back pointer from which the
        entire seam can be reconstructed.

    You will implement this class as part of the second version of the vertical
    seam finding algorithm.
    """
    def __init__(self, pixel_energy_data = 0, x_backpointer_to_previous_row = None):
        self.pixel_energy_data = pixel_energy_data
        self.x_backpointer_to_previous_row = x_backpointer_to_previous_row

    # raise NotImplementedError('SeamEnergyWithBackPointer is not implemented')


def compute_vertical_seam_v2(energy_data):
    """
    Find the lowest-energy vertical seam given the energy of each pixel in the
    input image. The image energy should have been computed before by the
    `compute_energy` function in the `energy` module.

    This is the second version of the seam finding algorithm. In addition to
    storing and finding the lowest-energy value of any seam, you will also store
    back pointers used to reconstruct the lowest-energy seam.

    At the end, you will return a list of x-coordinates where you would have
    returned a single x-coordinate instead.

    This is one of the functions you will need to implement. You may want to
    copy over the implementation of the first version as a starting point.
    Expected return value: a tuple with two values:

      1. The list of x-coordinates forming the lowest-energy seam, starting at
         the top of the image.
      2. The total energy of that seam.
    """

    # raise NotImplementedError('compute_vertical_seam_v2 is not implemented')
    h = len(energy_data)
    w = len(energy_data[0])

    seam_data = [[None for _ in row] for row in energy_data]    

    # populate the first row with energy values w/o any dependency.
    for x, _ in enumerate(energy_data[0]):
        seam_data[0][x] = SeamEnergyWithBackPointer(pixel_energy_data=energy_data[0][x])
        
    for y in range(1, h):
        for x, energy_at_yx in enumerate(energy_data[y]):
            x0 = x - 1 if x > 0 else 0
            x1 = x + 1 if x < w - 1 else w - 1

# single statement to find min position, enabled by lambda func and iterable is list, so single int returned
            min_of_parents_position = min( 
                list(range(x0, x1 + 1)),
                key=lambda x_candidate: seam_data[y - 1][x_candidate].pixel_energy_data
                )

            seam_data[y][x] = SeamEnergyWithBackPointer(
                            pixel_energy_data = seam_data[y - 1][min_of_parents_position].pixel_energy_data + energy_data[y][x],
                            x_backpointer_to_previous_row = min_of_parents_position)
                

# single statement to find min position and min seam energy, enabled by lambda func and iterable is enumerated
    min_energy_pos, min_seam_energy = min(
        enumerate(seam_data[h - 1]),
        key=lambda p: p[1].pixel_energy_data)

    x_start = min_energy_pos
    x_backpointers = []
    for y in range( h - 1, -1, -1):
        x_backpointers.append(x_start)
        x_start = seam_data[y][x_start].x_backpointer_to_previous_row        
    x_backpointers.reverse()

    return (x_backpointers, min_seam_energy.pixel_energy_data)



def visualize_seam_on_image(pixels, seam_xs):
    """
    Draws a red line on the image along the given seam. This is done to
    visualize where the seam is.

    This is NOT one of the functions you have to implement.
    """

    h = len(pixels)
    w = len(pixels[0])

    new_pixels = [[p for p in row] for row in pixels]

    for y, seam_x in enumerate(seam_xs):
        min_x = max(seam_x - 2, 0)
        max_x = min(seam_x + 2, w - 1)

        for x in range(min_x, max_x + 1):
            new_pixels[y][x] = Color(255, 0, 0)

    return new_pixels


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f'USAGE: {__file__} <input> <output>')
        sys.exit(1)

    input_filename = sys.argv[1]
    output_filename = sys.argv[2]

    print(f'Reading {input_filename}...')
    pixels = read_image_into_array(input_filename)

    print('Computing the energy...')
    energy_data = compute_energy(pixels)

    print('Finding the lowest-energy seam...')
    seam_xs, min_seam_energy = compute_vertical_seam_v2(energy_data)
    
    print(f'Saving {output_filename}')
    visualized_pixels = visualize_seam_on_image(pixels, seam_xs)
    write_array_into_image(visualized_pixels, output_filename)

    print()
    print(f'Minimum seam energy was {min_seam_energy} at x = {seam_xs[-1]}')
