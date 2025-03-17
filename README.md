# Reddit Video Downloader and Compiler

This Python application automates the process of downloading videos from Reddit and compiling them into a single video file. It uses Selenium for web scraping, MoviePy for video compilation, and Tkinter for the graphical user interface (GUI).

---

## Table of Contents

1. [Features](#features)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Settings](#settings)
5. [Dependencies](#dependencies)
6. [Contributing](#contributing)
7. [License](#license)

---

## Features

- **Reddit Video Downloading**:
  - Fetches video links from a specified subreddit.
  - Downloads videos using an external service (`viddit.red`).
  - Removes duplicate or invalid downloads automatically.

- **Video Compilation**:
  - Combines downloaded videos into a single `.mp4` file using MoviePy.
  - Resizes videos to ensure uniform dimensions.

- **Graphical User Interface (GUI)**:
  - Provides a user-friendly interface built with Tkinter.
  - Allows users to configure settings, start downloads, and compile videos with ease.

- **Customizable Settings**:
  - Users can adjust the number of videos to download via the settings tab.

---

## Installation

### Prerequisites

- Python 3.8 or higher
- Chrome Browser installed on your system
- Git (optional, for cloning the repository)

### Steps

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/reddit-video-downloader.git
   cd reddit-video-downloader