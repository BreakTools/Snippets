def get_smart_frame_list(input_frame_range: str, chunk_size: int) -> str:
    """This function receives a frame range and a chunk size. It then
    calculations a 'smart' frame list for deadline. This list is formatted
    as follows: First the first frame, then the last frame, then the frame
    between those frames, then the frame between those frames, etc, etc until
    it fills in the rest. It also takes into account chunk size,
    which is useful when one job consists of rendering multiple frames.
    This 'smart' list is handy because this way we can spot render
    problems throughout the frame range quickly.

    Example input: '1001-1005', 1
    Example output: '1001,1005,1003,1002,1004'
    """

    if "-" not in input_frame_range:
        # Single frames can't be rearranged
        return input_frame_range

    first_frame = int(input_frame_range.split("-")[0])
    last_frame = int(input_frame_range.split("-")[1])

    total_frames = last_frame - first_frame + 1
    full_chunks = total_frames // chunk_size
    leftover_frames = total_frames - full_chunks * chunk_size

    if total_frames == 2:
        # Two frames can't be rearranged
        return f"{first_frame},{last_frame}"

    frame_list = []

    if chunk_size > 1:
        for chunk in range(full_chunks):
            first_frame_in_chunk = chunk * chunk_size + first_frame
            last_frame_in_chunk = chunk * chunk_size + chunk_size + first_frame - 1
            frame_list.append(f"{first_frame_in_chunk}-{last_frame_in_chunk}")
    else:
        for chunk in range(full_chunks):
            frame_list.append(f"{chunk+first_frame}")

    if leftover_frames >= 1:
        first_leftover_frame_in_chunk = full_chunks * chunk_size + first_frame
        frame_list.append(f"{first_leftover_frame_in_chunk}-{last_frame}")

    frame_list_length = len(frame_list)
    smart_frame_index_list = [0, (frame_list_length - 1)]

    # First two items are already added
    chunks_to_build = len(frame_list) - 2

    two_indexes_with_largest_difference = [
        smart_frame_index_list[0],
        smart_frame_index_list[1],
    ]

    for chunk in range(chunks_to_build):
        # This is the most important part, took me a while to figure out.
        # It loops over our list, calculating the next addition every loop.
        # It calculates it like this: Example input: 1001-1005.
        # First we have [0, 4]. The biggest difference is between 0 and 4.
        # The center of 0 and 4 is 2, so we add it to the list.
        # The list is now [0, 4, 2]. We sort that to get [0,2,4].
        # Now we find the biggest difference again, which is between
        # 0 and 2 or 2 and 4. We take the first one, get the center point
        # and add it to the list. The list is now [0, 4, 2, 1].
        # We sort that, find the biggest difference, which is now
        # between 2 and 4. The center is 3, so we add that.
        # Our list is now [0, 4, 2, 1, 3], which is what we want.

        sorted_smart_index_list = sorted(smart_frame_index_list)
        biggest_difference = 0

        for index in range(len(sorted_smart_index_list)):
            index -= 1
            difference = (
                sorted_smart_index_list[index + 1] - sorted_smart_index_list[index]
            )
            if difference > biggest_difference:
                two_indexes_with_largest_difference[0] = sorted_smart_index_list[index]
                two_indexes_with_largest_difference[1] = sorted_smart_index_list[
                    index + 1
                ]
                biggest_difference = difference

        smart_frame_index_list.append(
            round(
                (
                    two_indexes_with_largest_difference[0]
                    + two_indexes_with_largest_difference[1]
                )
                / 2
            )
        )

    smart_frame_list = []

    for index in smart_frame_index_list:
        smart_frame_list.append(frame_list[index])

    formatted_smart_frame_list = ",".join(smart_frame_list)

    return formatted_smart_frame_list


print(get_smart_frame_list("1001-1005", 1))
# Output: "1001,1005,1003,1002,1004"

print(get_smart_frame_list("1001-1009", 2))
# Output: "1001-1002,1009-1009,1005-1006,1003-1004,1007-1008"
