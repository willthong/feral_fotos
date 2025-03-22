#!/bin/bash

# Selphy takes 46 seconds.
DELAY=50

check_server() {
    # Ask the server if there's something there
    if [[ $(curl -s $FERAL_FOTOS_HOST/photo_available != "1") ]]; then
        sleep 1s
        return
    # If there's a photo to download, grab it
    wget -O temporary_photo.jpg "$FERAL_FOTOS_HOST"/get_photo?api_key="$API_KEY"
    # print_command temporary_photo.jpg
    rm temporary_photo.jpg
    sleep "$DELAY"s
    return
}

while true; do
    check_server
done

