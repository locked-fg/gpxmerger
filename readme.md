# GPX Merger
A simple script to merge multiple GPX files into one large GPX file.
  
## Use Case
During holidays, one or more tracks are created for each tour / day.
In the end a single GPX Track is required for example to use in Lightroom 
in order for easy geo tagging or to get an overall map of all tracks.

Thus, a single GPX Track should be created from multiple GPX files.
  
## Usage 
```python gpxmerger.py "C:\Users\[...]\Track_1.gpx" "C:\Users\[...]\Track_2.gpx"```
The merged track is written as `merged.gpx` into the directory of the first GPX file.
 
In Windows, create a desktop link / shortcut with:
- Target: ```[path to]\python.exe gpxmerger.py```
- Execute in: ```[path to gpxmerger.py directory]```
- select multiple GPX files and drag & drop them to the link - the ```merged.gpx``` is created next to the selected tracks. 

Logging output is written to Console and into ```gpxmerger.log``` in the directory of the ```gpxmerger.py```.