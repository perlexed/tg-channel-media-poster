# TG Channel Media Poster

A Python CLI tool for distributing and scheduling image posts to a Telegram channel for a specified number of days using a user account.

## Features
- Distributes images from a source folder into daily batches
- Schedules posts to a Telegram channel at 23:00 KRAT for each day using user account
- Automatically manages folder structure and marks days as closed
- Logs all actions to `app.log`

## Requirements
- Python 3.8+
- [telethon](https://docs.telethon.dev/) - Telegram client library
- [python-dotenv](https://pypi.org/project/python-dotenv/)

## Installation
1. Clone the repository:
   ```sh
   git clone <your-repo-url>
   cd <project-folder>
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Telegram Setup
1. Get your API credentials from https://my.telegram.org:
   - Go to "API development tools"
   - Create a new application
   - Note down your `api_id` and `api_hash`

## Configuration
Create a `.env` file in the project root with the following variables:

```
daysToFillCount=3
sourceFolder=/absolute/path/to/source
targetRootFolder=/absolute/path/to/target
batchSize=5
TELEGRAM_API_ID=your_api_id
TELEGRAM_API_HASH=your_api_hash
TELEGRAM_PHONE=your_phone_number
TELEGRAM_CHAT_ID=your_chat_id
```

- `daysToFillCount`: Number of days to schedule posts for
- `sourceFolder`: Path to the folder with source images
- `targetRootFolder`: Path to the root folder where year/month/day folders are managed
- `batchSize`: Number of images per day
- `TELEGRAM_API_ID`: Your Telegram API ID from my.telegram.org
- `TELEGRAM_API_HASH`: Your Telegram API hash from my.telegram.org
- `TELEGRAM_PHONE`: Your phone number (with country code, e.g., +1234567890)
- `TELEGRAM_CHAT_ID`: Channel or group chat ID where to post

## Usage
1. (Recommended) Create and activate a virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   # or
   venv\Scripts\activate    # On Windows
   ```
2. Prepare your source and target folders as described above.
3. Run the script:
   ```sh
   python main.py
   ```
4. On first run, you'll need to enter the verification code sent to your Telegram.
5. If you have 2FA enabled, you'll be prompted to enter your password securely.
6. Check `app.log` for logs and errors.

## Folder Structure Example
```
sourceFolder/
  _2024/
    _01/
      ...
  2025/
    _01/
      _01/
      _02/
      ...
```

## Notes
- The tool will only work if the number of images in the source folder is exactly `daysToFillCount * batchSize`.
- The tool will rename day folders to mark them as closed after posting.
- Make sure you have permission to post in the target channel/group.
- The first run will create a session file for authentication.

## License
MIT 