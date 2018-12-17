udo docker rmi x-lab/test-scheduler:server \
                x-lab/test-scheduler:ui \
                x-lab/conductor:builder \
                conductor:ui \
                conductor:server \
                elasticsearch:2.4 \
                v1r3n/dynomite:latest \
                java:8-jre-alpine \
                python:2.7 \
                node:alpine \
                nginx:latest \
                java:latest \

echo "--- Clean Finished ---"
