
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
		dumpMetadata(selectedImage)
	end if
end run

on dumpMetadata(selectedImage)
	--log selectedImage
	tell application "Aperture"
		tell selectedImage
			
			log "color label:" & color label as string
			log "flagged:" & flagged as string
			log "height:" & height as string
			log "id:" & id as string
			log "latitude:" & latitude as string
			log "longitude:" & longitude as string
			log "main rating:" & main rating as string
			log "name:" & name as string
			log "online:" & online as string
			log "parent:" & name of parent as string
			log "picked:" & picked as string
			log "referenced:" & referenced as string
			log "selected:" & selected as string
			log "width:" & width as string
			
			repeat with i from 1 to count of EXIF tags
				set pName to name of item i of EXIF tags
				set pValue to value of item i of EXIF tags as string
				log "EXIF " & pName & ":" & pValue
			end repeat
			
			repeat with i from 1 to count of IPTC tags
				set pName to name of item i of IPTC tags
				set pValue to value of item i of IPTC tags as string
				log "IPTC " & pName & ":" & pValue
			end repeat
			
			repeat with i from 1 to count of custom tags
				set pName to name of item i of custom tags
				set pValue to value of item i of custom tags as string
				log "custom " & pName & ":" & pValue
			end repeat
			
			repeat with i from 1 to count of other tags
				try
					set pName to name of item i of other tags
					set pValue to value of item i of other tags as string
					log "other " & pName & ":" & pValue
				on error number -1700
					log "!other " & pName & " error -1700"
				end try
			end repeat
			
			repeat with i from 1 to count of keywords
				set pName to name of item i of keywords
				set pValue to value of item i of keywords as string
				log "keyword " & pName & ":" & pValue
			end repeat
			
			--get value of every keyword
			
		end tell
		--end tell
	end tell
	beep
	
end dumpMetadata

