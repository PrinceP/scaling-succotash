# Parking Slot Detection and Occupancy Monitoring

## Description

This repository contains the source code for a custom NX AI Manager postprocessor and a tiny Python HTTP server that servers a live webpage displaying the results from Parking Spot Occupancy.

To learn more about custom NX AI Manager postprocessors, see the [Scailable Integration SDK](https://github.com/scailable/sclbl-integration-sdk).

## Requirements

- NX Meta Server
- NX Meta Client
  ```bash
  sudo dpkg -i ~/Downloads/metavms-server-5.1.3.38363-linux_x64.deb
  sudo dpkg -i ~/Downloads/metavms-client-5.1.3.38363-linux_x64.deb
  ```


## Instructions

1. Follow the [NX AI Manager installation documentation](https://nx.docs.scailable.net/).
2. Choose the ARM64 version of the NX Server: [Download here](https://updates.networkoptix.com/metavms/6.0.0.38488/arm/metavms-server-6.0.0.38488-linux_arm64-beta.deb).
3. Clone this repository.
4. Navigate to the repository directory:
    ```bash
    cd <repository-directory>
    ```
5. Run the build script:
    ```bash
    cd postprocessor-python-example
    mkdir build
    cd build
    cmake ..
    make 
    sudo cp ./postprocessor-python-example/postprocessor-python-example /opt/networkoptix-metavms/mediaserver/bin/plugins/nxai_plugin/nxai_manager/postprocessors/
    sudo chmod -R 777 /opt/networkoptix-metavms/mediaserver/bin/plugins/nxai_plugin/nxai_manager/postprocessors
    
    ```
6. Start the Demo API server:
    ```bash
    cd frontend
    pip3 install -r requirements.txt
    python3 app.py
    ```
7. Run a sample test video:
    ```bash
    sudo apt install vlc
    cvlc parking_lot_2.mp4 --loop --sout '#transcode{vcodec=h264,acodec=none}:rtp{sdp=rtsp://0.0.0.0:8554/live}' --rtsp-host=172.16.67.128
    ```
8. Add the Optional plugins
   ```bash
   /opt/networkoptix-metavms/mediaserver/bin$ sudo cp -r plugins_optional/* plugins/
   sudo systemctl restart networkoptix-metavms-mediaserver.service
   ```


 
