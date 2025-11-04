mode con: lines=80 cols=160
powershell -Command "& { [console]::BufferWidth = 160; [console]::BufferHeight = 9999 }"
cd C:\Users\cnd\Downloads\repos\FluidX3D
call "C:\Program Files\Microsoft Visual Studio\2022\Community\Common7\Tools\VsDevCmd.bat" 
rem msbuild FluidX3D.sln /p:Configuration=Release %*




CL.exe /c /IC:src\OpenCL\include /Zi /nologo /W3 /WX- /diagnostics:column /sdl /MP /O2 /Oi /Ot /GL /D _MBCS /Gm- /EHsc /MD /GS /Gy /Qpar /fp:fast /permissive- /Zc:wchar_t /Zc:forScope /Zc:inline /std:c++17 /Fo"temp\\" /Fd"temp\vc142.pdb" /external:W3 /Gd /TP /wd26451 /wd6386 /FC /errorReport:queue src\graphics.cpp src\info.cpp src\kernel.cpp src\lbm.cpp src\lodepng.cpp src\main.cpp src\setup.cpp src\shapes.cpp


rc.exe /l"0x0409" /nologo /fo"temp\resource.res" src\resource.rc


link.exe /ERRORREPORT:QUEUE /OUT:"bin\FluidX3D.exe" /NOLOGO /LIBPATH:src\OpenCL\lib OpenCL.lib kernel32.lib user32.lib gdi32.lib winspool.lib comdlg32.lib advapi32.lib shell32.lib ole32.lib oleaut32.lib uuid.lib odbc32.lib odbccp32.lib kernel32.lib user32.lib gdi32.lib winspool.lib comdlg32.lib advapi32.lib shell32.lib ole32.lib oleaut32.lib uuid.lib odbc32.lib odbccp32.lib /MANIFEST /MANIFESTUAC:"level='asInvoker' uiAccess='false'" /manifest:embed /DEBUG:FULL /PDB:"bin\FluidX3D.pdb" /SUBSYSTEM:CONSOLE /OPT:REF /OPT:ICF /LTCG:incremental /LTCGOUT:"temp\FluidX3D.iobj" /TLBID:1 /DYNAMICBASE /NXCOMPAT /IMPLIB:"bin\FluidX3D.lib" /MACHINE:X64 temp\resource.res

pause


rem  start "cmd.exe '/c bin\FluidX3D.exe -f ..\..\FluidX3D\stl\concord_cut_large.stl --SUBGRID -u 2084 -y 3 -z 0.5  & pause'"   ^C
rem /mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe start "cmd.exe '/c bin\FluidX3D.exe -f ..\..\UW_Glider2v7.stl --SUBGRID -u 8000 -h & pause'"
