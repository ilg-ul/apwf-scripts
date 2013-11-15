tell application "Aperture"
	repeat with selectedimage in (get selection)
		tell selectedimage
			set name to (get name)
			set cameraTz to "None"
			set pictureTz to "None"
			try
				set cameraTz to value of custom tag "cameraTimeZoneName"
			end try
			try
				set pictureTz to value of custom tag "pictureTimeZoneName"
			end try
			log name & " " & cameraTz & " " & pictureTz
		end tell
	end repeat
end tell
