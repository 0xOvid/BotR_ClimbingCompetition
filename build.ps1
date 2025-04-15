# Build file for Bornholm on the Rocks (BotR):
# Takes relevant assets and packs to zip file for deployment 
# Files can then be moved with scp to server and hosted there

# Create dir for zipping
$zip_dir = "release_app"
New-Item -ItemType Directory -Path ".\$zip_dir"  

# Move files
Copy-Item -Path ".\templates\" -Destination ".\$zip_dir" -Force -Recurse
Copy-Item -Path ".\static\" -Destination ".\$zip_dir" -Force -Recurse
Copy-Item -Path ".\app.py" -Destination ".\$zip_dir"
Copy-Item -Path ".\README.md" -Destination ".\$zip_dir"
Copy-Item -Path ".\requirements.txt" -Destination ".\$zip_dir"
Copy-Item -Path ".\swagger.tmp" -Destination ".\$zip_dir"

# Make zip file
Compress-Archive -Path ".\$zip_dir\" -Destination ".\botr_app.zip" -CompressionLevel "Fastest"

# Cleanup
Remove-Item -Path ".\$zip_dir" -Force -Recurse