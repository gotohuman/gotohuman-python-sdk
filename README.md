<div align="center">

<img src="./img/logo.png" alt="gotoHuman Logo" width="360px"/>

</div>

# gotoHuman - Human in the Loop for AI workflows

[gotoHuman](https://gotohuman.com) helps you build production-ready AI workflows by making it really easy to include human approvals. Keep a human in the loop to review AI‑generated content, approve critical actions or provide input.

Set up a fully customized review step capturing any relevant data (text, images, markdown,...) and required human input (buttons, checkboxes, inputs,...). Then trigger it from your application whenever human review from your team is needed.

### Install

`pip install gotohuman`

### Init

Setup an environment variable with your API key:
```
GOTOHUMAN_API_KEY=YOUR_API_KEY
```
If you're using a .env file, don't forget to load it:
```
from dotenv import load_dotenv
load_dotenv()
```
Initialize the SDK:
```
gotoHuman = GotoHuman()
```

### Send request

[Read the docs](https://docs.gotohuman.com/send-requests) for more details.

Example request:
```
review = gotoHuman.create_review("YOUR_FORM_ID")
review.add_field_data("exampleField1", value1)
review.add_field_data("exampleField2", value2)
review.add_meta_data("threadId", threadId)
review.assign_to_users(["jess@acme.org"])
try:
    response = review.send_request()
    print("Review sent successfully:", response)
except Exception as e:
    print("An error occurred:", e)
```

#### Example review

![gotoHuman - Human approval example](./img/repo-review-example.jpg)