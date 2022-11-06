import argparse


def generate(title: str, transcript_file: str, youtube_id: str, save_file: str) -> None:

    with open(transcript_file, "r") as fp:
        text = fp.read().splitlines()

    # get timestamps and sentences
    times = [t for t in text if "-->" in t]
    sentences = [text[i] for i in range(len(text) - 1) if text[i + 1] == ""]

    # create html
    html = f"""
        <!DOCTYPE html>
        <html>
            <head> </head>
            <body>
                <h1>{title}</h1>
        """

    for time, sentence in zip(times, sentences):
        # extract hours, minutes seconds to link in the video
        h, m, s = time.split("-->")[0].strip().split(":")
        # remove ms
        s = s.split(",")[0]
        # combine to get seconds from start
        start = int(h) * 3600 + int(m) * 60 + int(s.split(",")[0])

        html += f"<a href='https://www.youtube.com/watch?v={youtube_id}&t={start}' target='__blank'>{time}</a> {sentence} <br/>"

        html += "</body>"
        html += "</html>"

    # save
    with open(save_file, "w") as fp:
        fp.write(html)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Generate html of podcast transcription")
    parser.add_argument("--title", type=str, help="Title of the page")
    parser.add_argument("--transcript_file", type=str, help="Path to transcript file")
    parser.add_argument("--youtube_id", type=str, help="youtube video id")
    parser.add_argument("--save_file", type=str, help="File name to save")

    args = parser.parse_args()
    generate(**vars(args))
