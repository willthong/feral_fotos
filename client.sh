#!/bin/bash

source /etc/environment

PRINTER_NAME="Canon_Selphy_CP1300"
# Selphy takes 46 seconds.
DELAY=50

check_server() {
    # Ask the server if there's something there
    if [[ $(curl -s $FERAL_FOTOS_HOST/photo_available) != "1" ]]; then
        sleep 1s
        return
    fi
    # If there's a photo to download, grab it
    wget -O temporary_photo.jpg "$FERAL_FOTOS_HOST"/get_photo?read_api_key="$API_KEY"
    # Reset 
    cupsenable $PRINTER_NAME
    lp \
        -o fit-to-page \
        -o PageSize=Postcard \
        -o orientation-requested=3 \
        ./temporary_photo.jpg  
    rm ./temporary_photo.jpg
    sleep "$DELAY"s
    return
}

while true; do
    check_server
done
