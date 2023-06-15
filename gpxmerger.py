import argparse
import sys
import logging
import logging.config
import gpxpy
import gpxpy.parser as parser
from os import path

# https://fangpenlin.com/posts/2012/08/26/good-logging-practice-in-python/
logging.basicConfig(level=logging.DEBUG)
logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'gpxmerger.log',
            'formatter': 'standard'
        }
    },
    'loggers': {
        '__main__': {  # name my module
            'level': 'DEBUG',
            'propagate': True,
            'handlers': ['file']
        }
    }
})


def is_gpx(filename):
    logger = logging.getLogger(__name__)
    ext = path.splitext(filename)[1]

    logger.debug('checking {f}'.format(f=filename))
    return ext == '.gpx'


def load_segments(track_files):
    logger = logging.getLogger(__name__)
    segments = []

    for track_file in track_files:
        with open(track_file, 'r') as gpx_file:
            gpx_parser = parser.GPXParser(gpx_file)
            gpx_parser.parse()
            gpx = gpx_parser.gpx

            for track in gpx.tracks:
                segments.extend(track.segments)

    logger.debug('loaded a total of {s} segments'.format(s=len(segments)))
    return segments


def load_points(track_files):
    logger = logging.getLogger(__name__)
    segments = load_segments(track_files)
    points = []

    for segment in segments:
        points.extend(segment.points)

    points = list(filter(lambda x: x.time is not None, points))
    points = sorted(points, key=lambda p: p.time)
    logger.debug('loaded a total of {s} points'.format(s=len(points)))
    return points


def to_xml(data):
    logger = logging.getLogger(__name__)
    gpx = gpxpy.gpx.GPX()
    
    # Create first track in our GPX:
    gpx_track = gpxpy.gpx.GPXTrack()
    gpx.tracks.append(gpx_track)
    
    if isinstance(data[0], gpxpy.gpx.GPXTrackSegment):
        logger.debug('converting {s} segments to XML'.format(s=len(data)))
        gpx_track.segments.extend(data)
        
    else:
        # Create first segment in our GPX track:
        gpx_segment = gpxpy.gpx.GPXTrackSegment()
        gpx_track.segments.append(gpx_segment)
        
        logger.debug('converting {s} points to XML'.format(s=len(data)))
    
        # Add points:
        gpx_segment.points.extend(data)

    return gpx.to_xml()

def get_target(files, target=None):
    logger = logging.getLogger(__name__)

    if not target or not path.isfile(target):
        filename = "merged"
        dirname = path.dirname(files[0])

        if target and path.isdir(target):
            dirname = target

        elif target:
            filename = target

        target = path.join(dirname, filename)

    if not target.endswith(".gpx"):
        target += ".gpx"

    logger.debug("write result to: {f}".format(f=target))
    return target


def save_target(xml, target_file):
    logger = logging.getLogger(__name__)
    with open(target_file, 'w') as fp:
        logger.debug('saving "{f}"'.format(f=target_file))
        fp.write(xml)
        logger.debug('done saving')


def merge(files, target=None, segment=False):
    logger = logging.getLogger(__name__)
    logger.info("start new merge process")
    track_files = filter(is_gpx, files)

    if segment:
        data = load_segments(track_files)

    else:
        data = load_points(track_files)

    xml = to_xml(data)
    target_file = get_target(files, target)
    save_target(xml, target_file)
    logger.info("Finish")


def main():
    parser = argparse.ArgumentParser(description="A simple script to merge multiple GPX files into one large GPX file.")
    parser.add_argument("input_files", nargs="*", help="Input files to merge")
    parser.add_argument("-o", help="Output file name, path or directory")
    parser.add_argument("-s", default=False, action="store_true", help=("Merge segments"))

    if len(sys.argv[1:]) == 0:
        parser.print_help()
        parser.exit()

    args = parser.parse_args()
    merge(args.input_files, args.o, args.s)


if __name__ == '__main__':
    main()
