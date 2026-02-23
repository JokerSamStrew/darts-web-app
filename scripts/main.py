import math


def wrap_with_svg_tag(svg_elements, **args):
    width, height = args['width'], args['height']
    svg_content = f'''<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">
{chr(10).join(svg_elements)}
</svg>'''
    return svg_content


def create_arc_sectors_svg(width, height, data,
                           colors, outer_radius, inner_radius):
    """
    Creates SVG with standalone arc sectors (not filled to center).

    Args:
    - data: List of sector values
    - colors: List of colors for each arc
    - outer_radius: Outer radius of arcs
    - inner_radius: Inner radius of arcs (creates hollow ring effect)
    """
    center_x, center_y = width // 2, height // 2

    total = sum(data)
    svg_elements = []
    start_angle = -math.pi / 2  # Start from top

    for i, (value, color) in enumerate(zip(data, colors)):
        angle = (value / total) * 2 * math.pi
        end_angle = start_angle + angle

        # Arc flags
        large_arc = 1 if angle > math.pi else 0

        # Calculate arc endpoints
        x1 = center_x + outer_radius * math.cos(start_angle)
        y1 = center_y + outer_radius * math.sin(start_angle)
        x2 = center_x + outer_radius * math.cos(end_angle)
        y2 = center_y + outer_radius * math.sin(end_angle)

        x3 = center_x + inner_radius * math.cos(end_angle)
        y3 = center_y + inner_radius * math.sin(end_angle)
        x4 = center_x + inner_radius * math.cos(start_angle)
        y4 = center_y + inner_radius * math.sin(start_angle)

        # Pure arc path: outer arc -> inner arc (reverse direction)
        path_data = (
            f"M {x1},{y1} "
            f"A {outer_radius},{outer_radius} 0 {large_arc} 1 {x2},{y2} "
            f"L {x3},{y3} "
            f"A {inner_radius},{inner_radius} 0 {large_arc} 0 {x4},{y4} "
            "Z"
        )

        svg_elements.append(f'<path d="{path_data}" fill="{
                            color}" stroke="#333" stroke-width="2"/>')

        start_angle = end_angle

    svg_content = chr(10).join(svg_elements)

    return svg_content


def main():
    size = 1500
    width, height = size, size
    radius = int(width * 0.35)
    data = [10] * 20
    colors_red_green = ['#680c09', '#032d16'] * 10
    colors_black_white = ['#e6ede9', '#0e0f0e'] * 10
    sectors_ratios = [0.95, 0.95, 0.45, 0.45,
                      0.4, 0.4, 0.1, 0.1, 0.05, 0.05, 0.01]

    first_sector_args = {
        'width': width,
        'height': height,
        'data': data,
        'colors': colors_red_green,
        'outer_radius': radius,
        'inner_radius': radius * sectors_ratios[0]
    }

    second_sector_args = {
        'width': width,
        'height': height,
        'data': data,
        'colors': colors_black_white,
        'outer_radius': radius * sectors_ratios[1],
        'inner_radius': radius * sectors_ratios[2]
    }

    third_sector_args = {
        'width': width,
        'height': height,
        'data': data,
        'colors': colors_red_green,
        'outer_radius': radius * sectors_ratios[3],
        'inner_radius': radius * sectors_ratios[4]
    }

    fourth_sector_args = {
        'width': width,
        'height': height,
        'data': data,
        'colors': colors_black_white,
        'outer_radius': radius * sectors_ratios[5],
        'inner_radius': radius * sectors_ratios[6]
    }

    bull_eye_outer = {
        'width': width,
        'height': height,
        # 'data': data[:1],
        'data': data,
        'colors': colors_red_green[1:],
        'outer_radius': radius * sectors_ratios[7],
        'inner_radius': radius * sectors_ratios[8]
    }

    bull_eye_inner = {
        'width': width,
        'height': height,
        # 'data': data[:1],
        'data': data,
        'colors': colors_red_green[:1],
        'outer_radius': radius * sectors_ratios[9],
        'inner_radius': radius * sectors_ratios[10]
    }

    arcs_svg = wrap_with_svg_tag([
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
    ],
        **first_sector_args
    )

    with open("board.svg", "w") as f:
        f.write(arcs_svg)


if __name__ == "__main__":
    main()
