.PHONY: docs-server
docs-server:
	@echo "Starting docs server..."
	mkdocs serve
.PHONY: docs2py
docs2py:
	@echo "Converting markdown to python..."
	sh ./scripts/docs2.sh . script
.PHONY: docs2md
docs2md:
	@echo "Converting python to markdown..."
	sh ./scripts/docs2.sh . markdown

