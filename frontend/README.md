##Docker command

docker buildx build \                                                                                                                   
  --platform linux/amd64 \
  --build-arg VITE_API_BASE_URL=https://backend:8000 \
  --no-cache \
  -t registry/mtrack_fe:x.y.z .