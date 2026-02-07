# Instagram DM Automation Workflow for n8n

This n8n workflow automates sending Direct Messages (DMs) to a list of Instagram users using the Instagram Graph API.

## Features
- **Schedule Trigger**: Runs automatically every day at 9:00 AM.
- **Batch Processing**: Sends messages one by one to avoid rate limits.
- **Error Handling**: Logs successes and failures to local files.
- **Customizable**: Easy to change the recipient list and message content.

## Prerequisites
- An n8n instance (self-hosted or cloud).
- An Instagram Business Account connected to a Facebook Page.
- A Facebook Developer App with the `instagram_manage_messages` permission.
- Valid `IG_USER_ID` (Your Instagram Business User ID) and `ACCESS_TOKEN` (Long-lived User Access Token).

## Setup Instructions

### 1. Import the Workflow
1. Open your n8n dashboard.
2. Go to **Workflows** > **Import from File**.
3. Select `instagram_dm_workflow.json` from this directory.

### 2. Configure Environment Variables
You need to set up the following environment variables in your n8n instance (or replace them directly in the nodes):

- `IG_USER_ID`: The ID of your Instagram Business account.
- `ACCESS_TOKEN`: A valid access token with permissions to send messages.

Alternatively, you can edit the **Send DM** node:
- Replace `{{ $env.IG_USER_ID }}` in the URL with your actual ID.
- Replace `{{ $env.ACCESS_TOKEN }}` in the Header with your actual token.

### 3. Update Recipient List
The workflow currently uses a **Set Users** node with mock data.
1. Open the **Set Users** node.
2. Update the JSON code with your real list of recipients and messages.
   ```javascript
   return [
     {
       json: {
         recipient_id: "REAL_IG_USER_ID_1",
         message: "Hello!"
       }
     },
     // ...
   ];
   ```
   *Note: To send DMs, the recipient must have interacted with your business account recently, or you must be using an approved tag if supported.*

### 4. Logs
The workflow logs activity to:
- `/home/node/.n8n/instagram_dm_log.txt` (Success)
- `/home/node/.n8n/instagram_dm_error.txt` (Errors)

Ensure n8n has write permissions to these paths or change them in the **Log Success** / **Log Error** nodes.

## detailed Graph API Reference
- [Send Messages](https://developers.facebook.com/docs/instagram-api/guides/content-publishing#single-media-posts) (Refer to Messaging specific docs)
- endpoint: `POST /v19.0/{ig-user-id}/messages`
