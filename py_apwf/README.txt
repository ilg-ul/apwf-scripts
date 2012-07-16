These scripts were planned to be used to implement (and improve) the 
(quite elaborated) workflow previously used with Lightroom.


*** ilg.apwf.checkTimeZones ***

Applies to: the multiple selected photos.

Check if the time zones of the selected photos are properly set,
to allow further processing.


*** ilg.apfw.makeGpsReference ***

Applies to: a single selected photo.

If not present, or explicitly asked by the user, add a custom field
	GpsReferenceDate='11-06-2012 18:50:17+00:00'
	
If not present, add a custom field
	CameraImageDate='11-06-2012 22:00:06+03:00'

The value is computed from EXIF ImageDate, interpreted as local date, and 
adjusted to the time zone specified by the custom field 'cameraTimeZoneName'.

At the end also adjust the image time.


*** ilg.apfw.adjustTime ***

Applies to: the multiple selected photos.

Interpolate the time based on the next GPS sync photo, compute the 
offset value in seconds and adjust the EXIF ImageDate of the entire collection.

If the collection contains a (single) GPS reference photo, use it as a compute
point, otherwise use the first photo in the collection.

Add a GpgInterpolatedReferenceDate custom tag for the compute point.

If not present, add the CameraImageDate custom field.


*** ilg.apfw.rename ***

Applies to: the multiple selected photos.

Rename the collection, using a custom string, the UTC date, and the 
original sequence number (DSC09876 -> ILG _20120617_09876).

Preserve the original name in the custom tag 'CameraFileName'.

The master file name cannot be changed by writing the 'FileName' other tag, 
it requires a Batch Change rename.


*** ilg.apfw.geotag ***

Applies to: the multiple selected photos.

Set the photo Longitude/Latitude (since EXIF are read only), and the custom 
Altitude.

The first version will use a local gpx file, but future versions may 
access the myTrack data.


*** ilg.apfw.checkMissingCoordinates ***

Applies to: the multiple selected photos.

Check the selected photos, and list those without latitude/longitude, 
for manual geotagging.


*** ilg.apfw.appendGoogleAltitudes ***

Applies to: the multiple selected photos.

Append the Google altitude to the selected photos. By default, if the
GPS altitude is set, avoid the expensive Google access (use the --all
to override this).


----- Development tools -------------------------------------------------------

*** ilg.apfw.dumpMetadata ***

Applies to: a single selected photo.

Dump all available metadata.



*** ilg.apfw.dumpTimeZones ***

Applies to: the multiple selected photos.

Print the 'cameraTimeZoneName' and 'pictureTimeZoneName' custom tags, 
if present.


*** ilg.apfw.cleanGpsCoordinates ***

Applies to: the multiple selected photos.

Clean only the custom tags (write empty strings).
The image tags cannot be removed.




