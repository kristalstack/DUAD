def sort_songs():

    songs = []

    # Read songs from file
    with open("songs.txt", "r") as file:
        for line in file:
            songs.append(line.strip())

    # Sort the songs alphabetically
    songs.sort()

    # Write sorted songs to a new file
    with open("sorted_songs.txt", "w") as file:
        for song in songs:
            file.write(song + "\n")


sort_songs()