# slack-exporter

A Slack bot and standalone script for exporting messages and file attachments from public and private channels, using Slack's new Conversations API.

A similar service is provided by Slack for workspace admins at [https://my.slack.com/services/export](https://my.slack.com/services/export) (where `my` can be replaced with your full workspace name to refer to a workspace different than your default). However, it can only access public channels, while `slack-exporter` can retrieve data from any channel accessible to your user account.

## Enhancements in This Fork

This fork extends the original slack-exporter with comprehensive CSV export capabilities:

- **Direct CSV Export**: Use `--csv` flag to export directly to CSV format from the main exporter
- **Standalone CSV Converter**: Post-process JSON exports with `converter_to_csv.py` for advanced customization
- **Media File Embedding**: Automatically download and embed media files as base64 data URIs in CSV exports
- **User ID Mapping**: Replace Slack user IDs with email addresses for improved readability
- **User Mention Processing**: Convert `` mentions in message text to email addresses
- **Channel Name Mapping**: Transform JSON filenames into human-readable channel names
- **Message Filtering**: Automatically exclude bot messages (USLACKBOT) from exports

These enhancements provide flexible CSV export options for data analysis, backup, and migration purposes.

## Authentication with Slack

There are two ways to use `slack-exporter` (detailed below). Both require a Slack API token to be able to communicate with your workspace.

1. Visit [https://api.slack.com/apps/](https://api.slack.com/apps/) and sign in to your workspace.
2. Click `Create New App`. If prompted to select "how you'd like to configure your app's scopes", choose the `App Manifest` option. You can configure the app manually instead, but you will be prompted to enter an app name and additional steps to set up permissions instead of the single step below. Once created, select your workspace.
3. You should then be prompted for an app manifest. Paste the contents of the `slack.yaml` file (in the root of this repo) into the YAML box.
4. Select `Install to Workspace` at the top of that page (or `Reinstall to Workspace` if you have done this previously) and accept at the prompt.
5. Copy the `OAuth Access Token` (which will generally start with `xoxp` for user-level permissions and may be located in a section like "OAuth & Permissions" in the sidebar).

## Usage

### As a standalone script

`exporter.py` can create an archive of all conversation history in your workspace which is accessible to your user account.

1. Either add 

    ```text
    SLACK_USER_TOKEN = xoxp-xxxxxxxxxxxxx...
    ```
    
    to a file named `.env` in the same directory as `exporter.py`, or run the following in your shell (replacing the value with the user token you obtained in the [Authentication with Slack](#authentication-with-slack) section above).

    ```shell script
    export SLACK_USER_TOKEN=xoxp-xxxxxxxxxxxxx...
    ```

2. If you cloned this repo, make sure that dependencies are installed by running `pip install -r requirements.txt` in the repo root directory.
3. Run `python exporter.py --help` to view the available export options. You can test that access to Slack is working by listing available conversations: `python exporter.py --lc`.

### CSV Export

This fork provides two methods for CSV export:

#### Method 1: Direct CSV Export
Export directly to CSV format using the main exporter:

```
python exporter.py --csv [other options]
```

**CSV Structure:**
- `timestamp`: Message timestamp
- `user`: User name (resolved from user ID)
- `text`: Message content
- `thread_ts`: Thread timestamp (if message is part of a thread)
- `reply_count`: Number of replies (for thread parent messages)
- `media_data`: Base64-encoded media files as data URIs (separated by `||`)

#### Method 2: Standalone CSV Converter
First export to JSON, then convert using the dedicated converter:

1. Export to JSON: `python exporter.py --json [other options]`
2. Run the CSV converter: `python converter_to_csv.py`

**Converter Features:**
- **User ID Mapping**: Automatically replaces Slack user IDs with configured email addresses
- **Channel Name Mapping**: Converts JSON filenames to readable channel names
- **Mention Processing**: Replaces `` mentions with email addresses
- **Customizable Mappings**: Edit `USER_MAP` and `channel_mapping` dictionaries for your workspace

**CSV Output Format:**
- `timestamp`: Message timestamp
- `channel`: Human-readable channel name
- `user`: User email address
- `text`: Message content with processed mentions

#### Media File Handling
When using the `--csv` flag, the exporter automatically:
- Downloads all attached files and images
- Converts them to base64 data URIs
- Embeds them in the `media_data` column
- Supports various file types with proper MIME type detection

#### CSV Export Examples

**Direct export with CSV format:**
```
python exporter.py --csv --channel general
```

**Export specific channels to CSV:**
```
python exporter.py --csv --channel-list "general,random,tech"
```

**Post-process existing JSON exports:**
```
python converter_to_csv.py
```
(Note: Update the `json_dir` path in the script to match your export directory)

### As a Slack bot

`bot.py` is a Slack bot that responds to "slash commands" in Slack channels (e.g., `/export-channel`). To connect the bot to the Slack app generated in [Authentication with Slack](#authentication-with-slack), create a file named `.env` in the root directory of this repo, and add the following line:

```text
SLACK_USER_TOKEN = xoxp-xxxxxxxxxxxxx...
```

Save this file and run the Flask application in `bot.py` such that the application is exposed to the Internet. This can be done via a web server (e.g., Heroku), as well as via the ngrok service, which assigns your `localhost` server a public URL.

To use the ngrok method:

1. [Download](https://ngrok.com/download) the appropriate binary.
2. Run `python bot.py`
3. Run the ngrok binary with `path/to/ngrok http 5000`, where `5000` is the port on which the Flask application (step 2) is running. Copy the forwarding HTTPS address provided.

4. Create the following slash commands will be created (one for each applicable Flask route in `bot.py`):

    | Command         | Request URL                               | Arguments    | Example Usage        |
    |-----------------|-------------------------------------------|--------------|----------------------|
    | /export-channel | https://`[host_url]`/slack/export-channel | json \| text | /export-channel text |
    | /export-replies | https://`[host_url]`/slack/export-replies | json \| text | /export-replies json |

    To do this, uncomment the `slash-commands` section in `slack.yaml` and replace `YOUR_HOST_URL_HERE` with something like `https://xxxxxxxxxxxx.ngrok.io` (if using ngrok). Then navigate back to `OAuth & Permissions` and click `(Re)install to Workspace` to add these slash commands to the workspace (ensure the OAuth token in your `.env` file is still correct).

## Contributors

- **Original Author**: [Seb Seager](https://github.com/sebseager)
- **Fork Enhancements**: [g8rdier](https://github.com/g8rdier) - CSV export functionality and media file support

## License

This software is available under the [GPL](LICENSE).
