from src.utilities.colors import ALL_COLORS, GREEN, return_colored_string


def print_ring(mapping, host):
    start = next(iter(mapping))  # Start with any key in the mapping
    current = start
    result = []
    color_index = 0

    while True:
        result.append(
            return_colored_string(ALL_COLORS[color_index % len(ALL_COLORS)], current)
        )
        current = mapping[current]
        color_index += 1
        if current == start:
            break

    # Join the result and include the circular closure
    print(
        "\n\n"
        + return_colored_string(GREEN, "**RING CLOSED 🎉**\n")
        + " <-> ".join(result)
        + f" <-> {result[0]}\n"
        + return_colored_string(ALL_COLORS[0], f"CENTRAL HUB: {host}\n")
    )


def find_shortest_path(server_map, host, target):
    """
    Determines the shortest path in the ring topology to the target server.
    """
    servers = list(server_map.keys())
    current_index = servers.index(host)
    target_index = servers.index(target)

    # Calculate clockwise and counterclockwise distances
    clockwise_distance = (target_index - current_index) % len(servers)
    counterclockwise_distance = (current_index - target_index) % len(servers)

    if clockwise_distance <= counterclockwise_distance:
        return server_map[host]["right"]
    else:
        return server_map[host]["left"]
