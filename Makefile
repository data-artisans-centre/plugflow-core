# Define variables for plugin and arguments
PLUGIN = youtube-review
VIDEO_URL = https://www.youtube.com/watch?v=ScMzIvxBSi4
MAX_COMMENTS = 10

# Default target
.PHONY: all
all: help

# Target to display help
.PHONY: help
help:
	@echo "Available targets:"
	@echo "  make health                    Check health of all plugins"
	@echo "  make extract-yt-review         Execute the youtube-review plugin with default arguments"
	@echo "  make extract-yt-review VIDEO_URL=<url> MAX_COMMENTS=<number>  Execute youtube-review with custom arguments"

# Target to check plugin health
.PHONY: health
health:
	@python main.py health

# Target to execute the youtube-review plugin
.PHONY: extract-yt-review
yt-review:
	@python3.10 main.py execute $(PLUGIN) --params '{"video_url": "$(VIDEO_URL)", "max_comments": $(MAX_COMMENTS)}'

