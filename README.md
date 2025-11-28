# Akipedidos API – Python Client

A unofficial Python client library for interacting with the Akipedidos backend.
This project uses authenticated sessions, CSRF extraction, and HTML form emulation to
communicate with the platform exactly like the browser does.

⚠ **Disclaimer:** This is not an official API.  
It relies on web-scraping techniques, hidden fields, CSRF tokens and browser-simulated
form submissions.  
Breaking changes may occur if the platform updates.

---

## Features

- 🔐 Automatic login + persistent session  
- 🛡 CSRF token extraction for each request  
- 📦 Category listing/creation/editing  
- 🍕 Item creation, item editing, hide/unhide  
- 🎯 Exact Chrome-like multipart/form-data submissions  
- 💡 Designed to be imported and used inside other Python scripts  

---

## Example Usage:

```
from akipedidos import AkipedidosClient
import json

client = AkiPedidosClient("https://yourdomain.com/")
login = client.auth.login("...", "...")
if login:
    # Create an item
    hours = [...]  # build your hours list
    result = client.items.create(
        category="109",
        name="Pizza de Mussarela",
        external_code="103",
        ncm_code="22021003",
        description="Pizza de mussarella",
        price="15",
        price_cost="10",
        days={'sun':'1','mon':'1','tue':'1','wed':'1','thu':'1','fri':'1','sat':'1'},
        hours_json=json.dumps(hours)
    )

    print(result)

    # Hide item
    client.items.hide(item_id=330, hidden=1)
```