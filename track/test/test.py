import track
import json


class Rect:

    def __init__(self, attrs):
        for a in attrs:
            setattr(self, a, attrs[a])

    def area(self):
        return self.width * self.height

    def intersection(self, rect):

        if (((self.x + self.width) < rect.x)
            or (self.x > (rect.x + rect.width))
            or ((self.y + self.height) < rect.y)
                or (self.y > (rect.y + rect.height))):
                return 0

        width = (min(self.x + self.width, rect.x + rect.width)
                 - max(self.x, rect.x))
        height = (min(self.y + self.height, rect.y + rect.height)
                  - max(self.y, rect.y))

        return width * height


def _match_common_frames(exp, gen):
    common_frames = {}

    for result in exp:
        common_frames[result['frame']] = {
            'exp': result['rectangles'][0]
        }

    for result in gen:
        frame_num = result['frame']
        if frame_num in common_frames:
            common_frames[frame_num]['gen'] = result['rectangles'][0]

    return {k: v for k, v in common_frames.items() if 'gen' in v}


def _generate_overlap_pcts(frames):
    frame_overlap_pcts = []

    for (frame_num, frame) in frames.items():
        expRect = Rect(frame['exp'])
        genRect = Rect(frame['gen'])

        overlap_pct = 100 * expRect.intersection(genRect) / expRect.area()
        frame_overlap_pcts.append(overlap_pct)

    return frame_overlap_pcts


def generate_frame_overlaps(video, jsonfile):
    """Generates frame overlap data given a video path and JSON path."""
    generated_json = json.loads(track.JSON_from_video(video))
    expected_json = json.load(open(jsonfile, 'r'))

    common_frames = _match_common_frames(expected_json, generated_json)
    return _generate_overlap_pcts(common_frames)
