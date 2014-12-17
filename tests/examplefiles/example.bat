@ @@ echo off
::This is an example of the Windows batch language.

rem TODOs:
rem %...% in all its glory
rem capitalize some things
rem for /f usebackq %%G in ('a b c')

setlocal EnableDelayedExpansion
(cls)
set/a_tests=0,_passed=0
title=Batch test
echo %~nx0, the>,con comprehensive testing suite
ver
echo(

if cmdextversion 2 goto =)
goto :fail

     :)
echo Starting tests at:
date/t & time/t
echo(

if [%*]==[--help] (
  echo Usage: %~nx0 [--help]
  echo   --help: Display this help message and quit.
  shift
  goto :exit comment) else rem

(call :comments)
call ::io
call:control
call::internal

:exit
if /i %_tests%==%_passed% (
  color 02
) else (
  color c
  if not defined _exitCode set _exitCode=1
)
set _percentage=NaN
if defined _tests (
  if %_tests% neq 0 (set /a _percentage=100*_passed/_tests)
)
echo(
echo Tests passed: %_passed%/%_tests% (%_percentage%%%)
pause
color
exit /b %_exitCode%

:fail
rem This should never happen.
echo Internal error 1>& 269105
set /a _exitCode=0x69+(0105*1000)
break
goto :exit

:comments
rem "comment^
(rem.) & set /a _tests+=1
(rem)
(rem. ) & (rem. comment ) & echo Test %_tests%: Comments
rem )
)
) comment
)
:: comment
goto :comments1 comment
:comments1 comment
if 1==2 goto :comments1^
^
goto :comments2
goto :fail
:comments2
if 1==1 (goto :comments3)
:comments3)
goto :fail
:comments3
rem comment^
goto:fail
rem.comment comment^
goto fail
rem "comment comment"^
goto fail
rem comment comment^
set /a _passed+=1
goto :eof
goto :fail

:io
set /a _tests+=1
echo Test %_tests%: I/O
verify on
pushd .
if exist temp echo  temp already exists. & goto :eof
md temp
cd temp
mkdir 2>nul temp
chdir temp
if 1==1 echo  Checking drive... must be C or else this won't work
if not "%cd:~0,3%"=="C:\" (
  call call echo  Wrong drive (should be C^):
  vol
  goto :test)
>test0.bat echo rem Machine-generated; do not edit
call echo set /a _passed+=1 >>test0.bat
type test0.bat >"test 1.bat
ren "test 1.bat" test2.bat
rename test2.bat test.bat
call ^
C:test
del test.bat 2>nul
2>nul erase test0.bat
popd
rd temp\temp
rmdir temp
verify off
goto:eof

:control
set /a _tests+=1
echo Test %_tests%: Control statements
set _iterations=00>nul
for %%G in (,+,,-,) do @(
  for /l %%H in (,-1,,-1,,-3,) do (
    for /f tokens^=1-2^,5 %%I in ("2 %%H _ _ 10") do (
      for /f "tokens=* usebackq" %%L in (`echo %%G%%J`) do (
        for /f "tokens=*" %%M in ('echo %%L') do (
          set /a iterations+=(%%M%%M^)
        )
      )
    )
  )
)
if exist %~nx0 if not exist %~nx0 goto :fail
if exist %~nx0 (
  if not exist %~nx0 goto :fail
) else (
  if exist %~nx0 goto :fail
)
if /i %_iterations% gtr -2 (
  if /i %iterations% geq -1 (
    if /i %_iterations% lss 1 (
      if /i %_iterations% leq 0 (
        if /i %_iterations% equ 0 (
          if 1 equ 01 (
            if 1 neq "01" (
              if "1" neq 01 (
                set /a _passed+=1))))))))
) comment
goto :eof

:internal
set /a _tests+=1
echo Test %_tests%: Internal commands
path %path%
if not defined prompt prompt $P$G
prompt !prompt!rem/ $H?
echo on
rem/?
@echo off
rem /?>nul
if/?>nul || if /?>nul || if x/? >nul
for/?>nul && for /?>nul && for x/? >nul && for /?x >nul
goto/?>nul && goto /?>nul && goto:/? >nul && goto ) /? ) >nul && (goto /? )>nul
for /f "tokens=2 delims==" %%G in ('assoc .bat') do (
  set _batfile=%%G
)
ftype 1>nul %_batfile%
if errorlevel 0 if not errorlevel 1 set /a _passed+=1
goto :eof
:/?
goto :fail
