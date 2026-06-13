# C2hat for Home Assistant

A notify integration for [C2hat](https://tora.c-2.co.uk/). Lets Home
Assistant post messages into c2hat channels and DMs from automations.

This is a fork of the official `notify.slack` integration — the c2hat
server speaks Slack's Web API contract, so the only functional change
is the base URL.

## Installation (via HACS)

1. In Home Assistant, open **HACS → Integrations**.
2. Click the three-dot menu (top right) → **Custom repositories**.
3. Paste this repo's URL: `https://github.com/cpass-watch/hass-c2hat`
   Category: **Integration**. Click **Add**.
4. Search HACS for **C2hat**, click **Download**, then restart Home
   Assistant.

## Configuration

### Step 1 — Generate a bot token

In c2hat: **Preferences → Integrations → Bot tokens → New token**.
Copy the token (it starts with `c2hat-bot-` followed by 48 hex
characters). You only see the plaintext once.

### Step 2 — Add the integration to HA

**Settings → Devices & Services → Add integration → C2hat**.

Fill in:
- **API key**: paste the bot token from step 1
- **Default channel**: a channel name (e.g. `general`) or numeric id
- **Server base URL**: leave the default unless you self-host
- **Username** *(optional)*: bot display name override
- **Icon** *(optional)*: emoji shortcode or URL

### Step 3 — Use it from an automation

```yaml
automation:
  - alias: "Doorbell rings"
    trigger:
      - platform: state
        entity_id: binary_sensor.front_door_bell
        to: "on"
    action:
      - service: notify.c2hat
        data:
          message: "Someone's at the front door"
          target: "#alerts"
```

`target` accepts:
- channel names (`general`, `#alerts`)
- numeric channel ids (`42`)
- multiple comma-separated values to fan out

## File uploads

```yaml
action:
  - service: notify.c2hat
    data:
      message: "Garage cam grab"
      target: "#security"
      data:
        file:
          path: /config/www/garage-grab.jpg
```

Remote URL files (with optional Basic-Auth):

```yaml
data:
  file:
    url: https://camera.example/snapshot.jpg
    username: user
    password: pass
```

## Bot token scope

When you create the token in c2hat you can scope it to a specific
channel allowlist. A token scoped to `#alerts` only can't post to
`#general` even if your automation tries to.

## Self-hosting

Override **Server base URL** in the config flow. The base URL must
point at the c2hat slack-compat endpoint root, e.g.
`https://your-c2hat.example.com/api/c2hat-slack/`.

## Troubleshooting

- **invalid_auth** — token wrong, disabled, or revoked. Regenerate
  from c2hat Preferences.
- **Channel not found** — the bot token can't see that channel.
  Check the channel allowlist on the token in c2hat.
- **cannot_connect** — server URL unreachable from this HA instance.

## License

MIT. See `LICENSE`.
