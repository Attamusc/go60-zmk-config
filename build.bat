@echo off

setlocal enabledelayedexpansion

set IMAGE=go60-zmk-config-docker

:: Set revision from first parameter, default to the tested MoErgo ZMK commit
if "%~1"=="" (
	set BRANCH=4b2f3b9b718a4508e87111cdec24cda16f3c2726
) else (
	set BRANCH=%~1
)

:: Build Docker image
docker build -t "%IMAGE%" .

:: Run Docker container
docker run --rm -v "%cd%:/config" -e UID=0 -e GID=0 -e BRANCH="%BRANCH%" "%IMAGE%"

endlocal
