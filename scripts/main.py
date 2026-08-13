import math


def wrap_with_svg_tag(svg_elements, width, height):
    svg_content = f'''<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">
{chr(10).join(svg_elements)}
</svg>'''
    return svg_content


def create_arc_sectors_svg(id_prefix, labels_data, center_x, center_y, data, colors, outer_radius, inner_radius, start_angle):
    """
    Creates SVG with standalone arc sectors. Fixes solid circle case.
    """
    total = sum(data)

    # Prevent division by zero if data is empty
    if total == 0:
        total = 1

    svg_elements = []

    # SPECIAL CASE: Single data item + inner_radius > 0 = full ring
    if len(data) == 1:
        if inner_radius > 0:
            if id_prefix is not None:
                path_data = (
                    f'<circle id="{id_prefix}" cx="{center_x}" cy="{center_y}" r="{outer_radius}" fill="{colors[0]}"/>'
                    # f'<circle cx="{center_x}" cy="{center_y}" r="{inner_radius}" fill="#ffffff"/>'
                )
            else:
                path_data = (
                    f'<circle cx="{center_x}" cy="{center_y}" r="{outer_radius}" fill="{colors[0]}"/>'
                    # f'<circle cx="{center_x}" cy="{center_y}" r="{inner_radius}" fill="#ffffff"/>'
                )
        else:
            if id_prefix is not None:
                path_data = (
                    f'<circle id="{id_prefix}" cx="{center_x}" cy="{center_y}" r="{outer_radius}" fill="{colors[0]}"/>'
                )
            else:
                path_data = (
                    f'<circle cx="{center_x}" cy="{center_y}" r="{outer_radius}" fill="{colors[0]}"/>'
                )

        return path_data

    # Handle regular sectors
    for i, (value, color) in enumerate(zip(data, colors)):
        angle = (value / total) * 2 * math.pi
        end_angle = start_angle + angle
        large_arc = 1 if angle > math.pi else 0

        # Outer arc coordinates
        x1 = center_x + outer_radius * math.cos(start_angle)
        y1 = center_y + outer_radius * math.sin(start_angle)
        x2 = center_x + outer_radius * math.cos(end_angle)
        y2 = center_y + outer_radius * math.sin(end_angle)

        if inner_radius <= 0:
            # SOLID CIRCLE/PIE SLICE
            path_data = (
                f"M {center_x},{center_y} "
                f"L {x1},{y1} "
                f"A {outer_radius} {outer_radius} 0 {large_arc} 1 {x2},{y2} "
                f"Z"
            )
        else:
            # RING SECTOR
            x3 = center_x + inner_radius * math.cos(end_angle)
            y3 = center_y + inner_radius * math.sin(end_angle)
            x4 = center_x + inner_radius * math.cos(start_angle)
            y4 = center_y + inner_radius * math.sin(start_angle)

            path_data = (
                f"M {x1},{y1} "
                f"A {outer_radius} {outer_radius} 0 {large_arc} 1 {x2},{y2} "
                f"L {x3},{y3} "
                f"A {inner_radius} {inner_radius} 0 {large_arc} 0 {x4},{y4} "
                f"Z"
            )

        svg_elements.append(f'<path id="{id_prefix}{labels_data[i]}" d="{path_data}" fill="{color}" stroke="#333" stroke-width="1"/>')
        start_angle = end_angle  # Update start angle for next segment

    return "".join(svg_elements)  # Return all paths as a single string


def svg_text_labels(radius, data, center_x, center_y, font_size, start_angle, colors=None):
    if colors is None:
        colors = ['#4e79a7', '#f28e2b', '#59a14f', '#76b7b2', '#e15759', '#b07aa2']

    total = len(data)
    svg_parts = []

    label_radius = radius

    for i, value in enumerate(data):
        angle = 360 / total
        end_angle = start_angle + angle

        # Midpoint angle for label position
        mid_angle = start_angle + (angle / 2)
        mid_rad = math.radians(mid_angle)
        label_x = center_x + label_radius * math.cos(mid_rad)
        label_y = center_y + label_radius * math.sin(mid_rad)

        svg_parts.append(f'<text x="{label_x}" y="{label_y}" '
                         f'text-anchor="middle" font-size="{font_size}" dominant-baseline="middle" '
                         f'font-weight="bold" fill="white" stroke="black" stroke-width="0.5">'
                         f'{value}</text>')
        #
        # svg_parts.append(
        #     f'<circle cx="{label_x}" cy="{label_y}" r="{5}" fill="#ffffff"/>'
        # )

        start_angle = end_angle

    # svg_parts.append(
    #     f'<circle cx="{center_x}" cy="{center_y}" r="{5}" fill="#ffffff"/>'
    # )

    return '\n'.join(svg_parts)


def generate_board_svg_str():
    size = 1500
    width, height = size, size
    center_x, center_y = width // 2, height // 2
    radius = int(width * 0.45)
    font_size = radius / 7
    data = [10] * 20

    colors_red_green = ['#a40200', '#067d43'] * 10
    colors_white_black = ['#f0e5c7', '#0f0e0c'] * 10
    sectors_ratios = list(map(lambda x: x / 451, [170 * 2, 170 * 2, 162 * 2, 162 * 2, 107 * 2, 107 * 2,
                                                  99 * 2, 99 * 2, 32, 32, 12.7, 12.7, 0.0]))
    board_labels_data = [20, 1, 18, 4, 13, 6, 10, 15, 2, 17, 3, 19, 7, 16, 8, 11, 14, 9, 12, 5]

    start_angle = -90 - 9
    # start_angle_pi = -math.pi / 2 + (math.pi / 2) / 10
    start_angle_pi = (math.pi / 2) * (-1 + 1 / 10)

    text_labels_args = {
        'radius': radius * ((sectors_ratios[0] + 1) / 2),
        'data': board_labels_data,
        'colors': None,
        'center_x': center_x,
        'center_y': center_y,
        'font_size': font_size,
        'start_angle': start_angle
    }

    background_sector_args = {
        # 'id_prefix': 'bg_sct_',
        'id_prefix': None,
        'center_x': center_x,
        'center_y': center_y,
        'data': data[:1],
        'labels_data': board_labels_data,
        'colors': colors_white_black[1:],
        'outer_radius': radius,
        'inner_radius': radius * sectors_ratios[0],
        'start_angle': start_angle_pi
    }

    first_sector_args = {
        'id_prefix': 'fr_sct_',
        'center_x': center_x,
        'center_y': center_y,
        'data': data,
        'labels_data': board_labels_data,
        'colors': colors_red_green,
        'outer_radius': radius * sectors_ratios[1],
        'inner_radius': radius * sectors_ratios[2],
        'start_angle': start_angle_pi

    }

    second_sector_args = {
        'id_prefix': 'sc_sct_',
        'center_x': center_x,
        'center_y': center_y,
        'data': data,
        'labels_data': board_labels_data,
        'colors': colors_white_black,
        'outer_radius': radius * sectors_ratios[3],
        'inner_radius': radius * sectors_ratios[4],
        'start_angle': start_angle_pi

    }

    third_sector_args = {
        'id_prefix': 'thr_sct_',
        'center_x': center_x,
        'center_y': center_y,
        'data': data,
        'labels_data': board_labels_data,
        'colors': colors_red_green,
        'outer_radius': radius * sectors_ratios[5],
        'inner_radius': radius * sectors_ratios[6],
        'start_angle': start_angle_pi

    }

    fourth_sector_args = {
        'id_prefix': 'fth_sct_',
        'center_x': center_x,
        'center_y': center_y,
        'data': data,
        'labels_data': board_labels_data,
        'colors': colors_white_black,
        'outer_radius': radius * sectors_ratios[7],
        'inner_radius': radius * sectors_ratios[8],
        'start_angle': start_angle_pi

    }

    bull_eye_outer = {
        'id_prefix': 'beo_sct_',
        'center_x': center_x,
        'center_y': center_y,
        'data': data[:1],
        'labels_data': board_labels_data,
        'colors': colors_red_green[1:],
        'outer_radius': radius * sectors_ratios[9],
        'inner_radius': radius * sectors_ratios[10],
        'start_angle': start_angle_pi

    }

    bull_eye_inner = {
        'id_prefix': 'bei_sct_',
        'center_x': center_x,
        'center_y': center_y,
        'data': data[:1],
        'labels_data': board_labels_data,
        'colors': colors_red_green[:1],
        'outer_radius': radius * sectors_ratios[11],
        'inner_radius': radius * sectors_ratios[12],
        'start_angle': start_angle_pi

    }

    arcs_svg = wrap_with_svg_tag([
        create_arc_sectors_svg(
            **background_sector_args
        ),
        create_arc_sectors_svg(
            **first_sector_args
        ),
        create_arc_sectors_svg(
            **second_sector_args
        ),
        create_arc_sectors_svg(
            **third_sector_args
        ),
        create_arc_sectors_svg(
            **fourth_sector_args
        ),
        create_arc_sectors_svg(
            **bull_eye_outer
        ),
        create_arc_sectors_svg(
            **bull_eye_inner
        ),
        svg_text_labels(
            **text_labels_args
        )
    ],
        width, height
    )

    return arcs_svg


def test_cases():
    # arcs_svg = wrap_with_svg_tag([
    # Full solid circle
    # create_arc_sectors_svg(200, 200, [100], ['red'], 80, 0),

    # Full ring (single data item)
    # create_arc_sectors_svg(200, 200, [100], ['blue'], 80, 30),

    # Multiple sectors (original behavior)
    # create_arc_sectors_svg(200, 200, [30, 30, 40], ['red', 'green', 'blue'], 80, 30)
    # ], width=200, height=200)

    arcs_svg = svg_text_labels(radius=80, data=[20, 1, 18, 4, 13, 6, 10, 15, 2, 17, 3, 19, 7, 16, 8, 11, 14, 9, 12, 5])

    with open("board.svg", "w") as f:
        f.write(arcs_svg)


def main():
    with open("board.svg", "w") as f:
        f.write(generate_board_svg_str())

    # test_cases()


if __name__ == "__main__":
    main()
