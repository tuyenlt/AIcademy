run:
	python app/main.py
#     python run.py

lint:
	flake8 app

format:
	black app

# Create a new migration with auto-generated unique message
TIMESTAMP := $(shell date +%Y%m%d_%H%M%S)
migration_gen:
	alembic revision --autogenerate -m "$(TIMESTAMP)_migration"

# Apply latest migration
migration_run:
	alembic upgrade head

# Rollback last migration
migration_revert:
	alembic downgrade -1

# Show current migration status
migration_current:
	alembic current

# Show history of migrations
migration_history:
	alembic history

seed:
	@echo "Seeding all files in database/seeds..."
	@for file in database/seeds/*.py; do \
		module=$$(basename $$file .py); \
		echo "Running $$module"; \
		python -m database.seeds.$$module; \
	done
