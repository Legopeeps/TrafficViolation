@echo off
set CONTAINER_NAME=cool_handcrafted_container
set IMAGE_NAME=handcrafted_docker_image

echo --- Full Stack System Startup ---

rem Cleanup old containers to avoid "Name already in use" errors
echo Checking for existing containers...
docker stop %CONTAINER_NAME% >nul 2>&1
docker rm %CONTAINER_NAME% >nul 2>&1

rem option to rebuild the Docker image (was a huge resource clog before)
set /p REBUILD="Rebuild Docker image (if launching for the first time I recommend it) (y/n): "
if /i "%REBUILD%"=="y" (
    echo Building Docker image...
    docker build -t %IMAGE_NAME% .
) else (
    echo Skipping build, using existing image...
)

rem Run the API (Backend folder) in detached mode
echo Launching API on port 9000...
docker run -d -p 9000:9000 --name %CONTAINER_NAME% %IMAGE_NAME%

rem Launch the Web Server (Frontend)
rem Keeps a window open to see the web server's logs
echo Launching Frontend Server on port 5500...
start "Frontend_Server" cmd /k "python -m http.server 5500 --directory ./frontend"

rem Open the browser to index.html after a short delay to ensure the server is up
timeout /t 3 >nul
echo Opening Application...
start http://localhost:5500/index.html


rem Displaying status and instructions once it's all running
echo.
echo --- STATUS ---
echo API : http://localhost:9000/docs
echo Web: http://localhost:5500/index.html
echo To stop, run the command: docker stop %CONTAINER_NAME%
echo --------------
pause