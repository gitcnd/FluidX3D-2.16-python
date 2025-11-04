mode con: lines=80 cols=160
powershell -Command "& { [console]::BufferWidth = 160; [console]::BufferHeight = 9999 }"
cd C:\Users\cnd\Downloads\repos\FluidX3D
call "C:\Program Files\Microsoft Visual Studio\2022\Community\Common7\Tools\VsDevCmd.bat" 
msbuild FluidX3D.vcxproj /p:Configuration=Release /p:Platform=x64 %*
rem msbuild FluidX3D.sln /p:Configuration=Release %*
rem msbuild FluidX3D.sln -verbosity:diag /p:Configuration=Release %* >build_log.txt
pause


rem  start "cmd.exe '/c bin\FluidX3D.exe -f ..\..\FluidX3D\stl\concord_cut_large.stl --SUBGRID -u 2084 -y 3 -z 0.5  & pause'"   ^C
rem /mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe start "cmd.exe '/c bin\FluidX3D.exe -f ..\..\UW_Glider2v7.stl --SUBGRID -u 8000 -h & pause'"
