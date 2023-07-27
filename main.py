#!/usr/bin/env python
from cloudflare.cloudflare import CloudflareStack
from cdktf import App

app = App()
CloudflareStack(app, "cloudflare-stack")
app.synth()
