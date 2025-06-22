docker compose down -v --remove-orphans; `
docker rmi -f $(docker images -f 'dangling=true' -q); `
docker compose up --build;