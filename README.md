<div align="center">

<img src="./img/logo.png" alt="gotoHuman Logo" width="360px"/>

</div>

# gotoHuman - Human in the Loop for AI workflows

[![MIT License](https://img.shields.io/badge/License-MIT-red.svg?style=flat-square)](https://opensource.org/licenses/MIT)
[![PyPI Version](https://img.shields.io/pypi/v/gotohuman.svg?style=flat-square&label=pypi+gotohuman)](https://pypi.python.org/pypi/gotohuman)
[![GitHub Repo stars](https://img.shields.io/github/stars/gotohuman?style=flat-square&logo=GitHub&label=gotohuman)](https://github.com/langfuse/langfuse)
[![Discord](https://img.shields.io/discord/1301983673616171090?style=flat-square&logo=Discord&logoColor=white&label=Discord&color=%23434EE4)](https://discord.gg/yDSQtf2SSg)

[gotoHuman](https://gotohuman.com) is a web app where you can approve actions of your AI agents. Keep a human in the loop to review AI‑generated content, approve critical actions or provide input.

### Install

```bash
pip install gotohuman
```

### Init

Create a review form in [gotoHuman](https://app.gotohuman.com) adding fields to capture the content to review and the input and feedback you want to collect.

Setup an environment variable with your API key.
```
GOTOHUMAN_API_KEY=YOUR_API_KEY
```

Initialize the SDK:
```python
from gotohuman import GotoHuman

gotoHuman = GotoHuman()
```

### Send request

Request a new review and include the data for your form's content fields.  
[Read the docs](https://docs.gotohuman.com/send-requests) for more details.

Example request:
```python
review = gotoHuman.create_review("YOUR_FORM_ID")
review.add_field_data("ai_social_media_post", ai_text_draft)
review.add_field_data("ai_image", ai_image_url)
review.add_meta_data("threadId", threadId)
review.assign_to_users(["jess@acme.org"])
try:
    response = review.send_request()
    print("Review sent successfully:", response)
except Exception as e:
    print("An error occurred:", e)
```

Or asynchronously:
```python
response = await review.async_send_request()
```

#### Example review

![gotoHuman - Human approval example](./img/repo-review-example.jpg)