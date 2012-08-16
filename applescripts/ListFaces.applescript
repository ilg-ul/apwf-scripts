(* This script looks in the faces database and gets names of the faces in the selected photos 
If then makes a new keyword with the name (and parent keyword "Face") *)

tell application "Aperture"
	activate
	-- locate the current aperture library 
	set aperture_library_path to do shell script "defaults read com.apple.aperture LibraryPath"
	-- expand the '~' if it's in there 
	set aperture_library_path to do shell script "echo " & aperture_library_path
	-- add trailing slash if necessary 
	if aperture_library_path does not end with "/" then
		set aperture_library_path to aperture_library_path & "/"
	end if
	
	-- locate the databases 
	set the faces_db_path to aperture_library_path & "Database/apdb/faces.db"
	set the library_db_path to aperture_library_path & "Database/apdb/Library.apdb"
	
	set the selected_items to (get the selection)
	
	repeat with z from 1 to the count of the selected_items
		set this_photo to item z of the selected_items
		my extract_face_record(this_photo, library_db_path, faces_db_path)
	end repeat
end tell

on extract_face_record(this_photo, library_db_path, faces_db_path)
	set the master_uuid to every paragraph of (my SQL_command(library_db_path, "select masterUuid from RKVersion where uuid=\"" & id of this_photo & "\";"))
	--get detected faces for the image key 
	set the face_keys to every paragraph of (my SQL_command(faces_db_path, "select faceKey from RKDetectedFace where masteruuid=\"" & master_uuid & "\";"))
	
	-- for each face 
	set the face_records to {}
	repeat with this_key in the face_keys
		-- get name. NOTE could select fullName instead of select name if you wished 
		set the face_name to my SQL_command(faces_db_path, "select name from rkFaceName where faceKey=\"" & this_key & "\";")
		-- add it as new key word 
		tell application "Aperture"
			tell this_photo
				--make new keyword with properties {name:face_name, parents:{"Face"}}
				log face_name
			end tell
		end tell
	end repeat
end extract_face_record

on SQL_command(faces_db_path, command_string)
	return (do shell script "sqlite3 " & (quoted form of faces_db_path) & " '" & command_string & "'")
end SQL_command