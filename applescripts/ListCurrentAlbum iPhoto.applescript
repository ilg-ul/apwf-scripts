
(* called when clicked on *)
on run
	tell application "iPhoto"
		set currentPhotos to photos of current album
		
		repeat with i from 1 to count of currentPhotos
			tell item i of currentPhotos
				log name as string
			end tell
		end repeat
	end tell
	
end run

