
(* called when clicked on *)
on run
	tell application "Aperture"
		set selectedimage to item 1 of (get selection)
		set imageParent to parent of selectedimage
		set images to image versions of imageParent
		
		repeat with i from 1 to count of images
			
			tell item i of images
				
				log name as string
				
			end tell
		end repeat
	end tell
	
end run

