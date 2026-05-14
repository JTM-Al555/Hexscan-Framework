from rich.progress import track


def progress_bar(items, description):

    return track(
        items,
        description=description
    )