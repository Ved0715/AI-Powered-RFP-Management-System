# Check if running
docker ps --filter name=rfp-postgres

# View logs
docker logs rfp-postgres

# Stop container
docker stop rfp-postgres

# Start container again
docker start rfp-postgres

# Connect via psql
docker exec -it rfp-postgres psql -U rfp_user -d rfp_db

# Remove container (⚠️ keeps data in volume)
docker rm -f rfp-postgres

# Remove container + data (⚠️ deletes everything)
docker rm -f rfp-postgres && docker volume rm rfp_postgres_data







# Create new migration
alembic revision --autogenerate -m "Your message"

# Apply migrations
alembic upgrade head

# Check current version
alembic current

# Rollback one migration
alembic downgrade -1

# View history
alembic history