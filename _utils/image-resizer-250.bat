%echo off
setlocal EnableDelayedExpansion

rem Enumerate files being passed to a script
for %%i in (%*) do (

rem Create a preview version
magick convert %%i -resize "x250" "%%~di%%~pi%%~ni-p%%~xi"

rem Create a full sized version
magick convert %%i -resize "794x794>" %%i

rem Optimize both images
FileOptimizer32 %%i "%%~di%%~pi%%~ni-p%%~xi"

rem Write image dimensions:
magick convert "%%~ni" -print "%%f: %%w x %%h" null: >> "%%~di%%~pidimensions.txt"
echo. >> "%%~di%%~pidimensions.txt"

)
