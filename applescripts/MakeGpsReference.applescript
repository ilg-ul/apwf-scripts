
(* called when clicked on *)
on run
	tell application "Aperture"
		set selectedImages to (get selection)
	end tell
	
	if selectedImages is {} then
		error "Please select an image."
	else if (count of selectedImages) > 1 then
		error "Please select a single image."
	else
		set selectedImage to item 1 of selectedImages
		makePhotoGpsReference(selectedImage)
	end if
end run

on makePhotoGpsReference(selectedImage)
	log selectedImage
	tell application "Aperture"
		--tell library 1
		tell selectedImage
			try
				set gpsRefDate to value of custom tag "GpsReferenceDate"
				set gpsRefDate to trim_tabs_and_spaces(gpsRefDate)
			on error
				set gpsRefDate to {}
			end try
			log gpsRefDate
			
			set mustUpdate to false
			set mustAdd to false
			if gpsRefDate = {} then
				set mustAdd to true
			else
				set alertResult to display alert "This photo was already configured as reference, do you want to redefine it?" buttons {"No", "Yes"} as warning default button "No"
				log alertResult
				
				if button returned of alertResult is "Yes" then
					set mustUpdate to true
				end if
			end if
			
			if mustUpdate or mustAdd then
				set dialogDate to display dialog "Enter the GPS reference date & time as 'DD-MM-YYYY hh:mm:ss GMT+00:00':" default answer ""
				log dialogDate
				
				if button returned of dialogDate is "OK" then
					set newStringDate to text returned of dialogDate
					log newStringDate
					
					if validateDate(newStringDate) of me then
						if mustAdd then
							
							(* add the new custom tag GpsReferenceDate  *)
							make new custom tag with properties {name:"GpsReferenceDate", value:newStringDate}
							
							(* add the new custom tag CameraImageDate *)
							try
								set cameraImageDate to value of custom tag "CameraImageDate"
								set cameraImageDate to trim_tabs_and_spaces(cameraImageDate, "+00:00")
							on error
								set cameraImageDate to {}
							end try
							
							if cameraImageDate = {} then
								set imageDate to ((value of EXIF tags where name is "ImageDate") as date)
								--set imageDateUTC to imageDate
								--set imageDateUTC to imageDate - (time to GMT)
								set imageDateUTC to imageDate - (time to GMT) + (2 * hours)
								set imageDateStringUTC to convertDateToString(imageDateUTC, "+02:00") of me
								make new custom tag with properties {name:"CameraImageDate", value:imageDateStringUTC}
							end if
							
						else if mustUpdate then
							(* update existing GpsReferenceDate custom tag *)
							set value of custom tag "GpsReferenceDate" to newStringDate
						end if
					else
						set alertResult to display alert "The date is not like as 'DD-MM-YYYY hh:mm:ss GMT+00:00'" as critical
					end if
				else
					log button returned of dialogDate
				end if
			end if
		end tell
		
		
	end tell
	beep
	
end makePhotoGpsReference

on validateDate(str)
	return true
end validateDate

on convertDateToString(theDate, tz)
	
	set str to ""
	set str to str & convert2chIntegerToString(day of theDate)
	set str to str & "-"
	set str to str & convert2chIntegerToString((month of theDate) as integer)
	set str to str & "-"
	(* assume year has 4 digits *)
	set str to str & ((year of theDate) as string)
	set str to str & " "
	set str to str & convert2chIntegerToString(hours of theDate)
	set str to str & ":"
	set str to str & convert2chIntegerToString(minutes of theDate)
	set str to str & ":"
	set str to str & convert2chIntegerToString(seconds of theDate)
	set str to str & " GMT" & tz
	
	return str
	
end convertDateToString

on convert2chIntegerToString(theInteger)
	if theInteger ³ 10 then
		return (theInteger as string)
	else
		return "0" & (theInteger as string)
	end if
end convert2chIntegerToString

on trim_tabs_and_spaces(the_text)
	considering hyphens, punctuation and white space
		repeat while the_text starts with space or the_text starts with tab
			if length of the_text is 1 then
				set the_text to ""
			else
				set the_text to text 2 thru -1 of the_text
			end if
		end repeat
		repeat while the_text ends with space or the_text ends with tab
			set the_text to text 1 thru -2 of the_text
		end repeat
		return the_text
	end considering
end trim_tabs_and_spaces
